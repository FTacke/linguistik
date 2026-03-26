from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = SCRIPT_DIR.parent
DEFAULT_AUDIO_ROOT = ASSETS_DIR / "audiofiles"
DEFAULT_REPORTS_DIR = SCRIPT_DIR / "reports"


@dataclass
class AuditConfig:
    audio_root: Path
    reports_dir: Path
    duration_warn_seconds: float
    min_sample_rate: int
    max_sample_rate: int
    min_bitrate_kbps: int
    max_bitrate_kbps: int
    ffmpeg_path: Path | None
    ffprobe_path: Path | None


def parse_args() -> AuditConfig:
    parser = argparse.ArgumentParser(description="Audit MP3 files under docs/assets/audiofiles.")
    parser.add_argument("--audio-root", type=Path, default=DEFAULT_AUDIO_ROOT)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    parser.add_argument("--duration-warn-seconds", type=float, default=60.0)
    parser.add_argument("--min-sample-rate", type=int, default=16000)
    parser.add_argument("--max-sample-rate", type=int, default=48000)
    parser.add_argument("--min-bitrate-kbps", type=int, default=48)
    parser.add_argument("--max-bitrate-kbps", type=int, default=320)
    parser.add_argument("--ffmpeg", type=Path, default=None)
    parser.add_argument("--ffprobe", type=Path, default=None)
    args = parser.parse_args()
    return AuditConfig(
        audio_root=args.audio_root.resolve(),
        reports_dir=args.reports_dir.resolve(),
        duration_warn_seconds=args.duration_warn_seconds,
        min_sample_rate=args.min_sample_rate,
        max_sample_rate=args.max_sample_rate,
        min_bitrate_kbps=args.min_bitrate_kbps,
        max_bitrate_kbps=args.max_bitrate_kbps,
        ffmpeg_path=args.ffmpeg.resolve() if args.ffmpeg else None,
        ffprobe_path=args.ffprobe.resolve() if args.ffprobe else None,
    )


def safe_float(value: Any) -> float | None:
    try:
        if value in (None, "", "N/A"):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_int(value: Any) -> int | None:
    try:
        if value in (None, "", "N/A"):
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def format_seconds(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.3f}"


def format_kib(value: int | None) -> str:
    if value is None:
        return ""
    return f"{value / 1024:.1f}"


def tool_path(name: str, explicit_path: Path | None = None) -> str | None:
    if explicit_path:
        return str(explicit_path)

    found = shutil.which(name)
    if found:
        return found

    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        return None

    exe_name = name if name.lower().endswith(".exe") else f"{name}.exe"
    link_path = Path(local_appdata) / "Microsoft" / "WinGet" / "Links" / exe_name
    if link_path.exists():
        return str(link_path)

    packages_root = Path(local_appdata) / "Microsoft" / "WinGet" / "Packages"
    for candidate in sorted(packages_root.glob(f"**/{exe_name}")):
        if candidate.exists():
            return str(candidate)
    return None


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def ffprobe_metadata(ffprobe_exe: str, file_path: Path) -> dict[str, Any] | None:
    result = run_command(
        [
            ffprobe_exe,
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(file_path),
        ]
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def decode_test(ffmpeg_exe: str, file_path: Path) -> tuple[str, str]:
    result = run_command(
        [
            ffmpeg_exe,
            "-v",
            "error",
            "-i",
            str(file_path),
            "-f",
            "null",
            os.devnull,
        ]
    )
    if result.returncode == 0:
        return "ok", ""
    message = (result.stderr or result.stdout).strip()
    return "failed", message.splitlines()[-1] if message else "decode test failed"


def collect_audio_stream(metadata: dict[str, Any] | None) -> dict[str, Any] | None:
    if not metadata:
        return None
    for stream in metadata.get("streams", []):
        if stream.get("codec_type") == "audio":
            return stream
    return None


def assess_file(path: Path, cfg: AuditConfig, ffprobe_exe: str | None, ffmpeg_exe: str | None) -> dict[str, Any]:
    relative_path = path.relative_to(cfg.audio_root).as_posix()
    exists = path.exists()
    readable = os.access(path, os.R_OK) if exists else False
    size_bytes = path.stat().st_size if exists else None
    warnings: list[str] = []
    errors: list[str] = []

    metadata = ffprobe_metadata(ffprobe_exe, path) if ffprobe_exe and exists and readable else None
    stream = collect_audio_stream(metadata)
    fmt = metadata.get("format", {}) if metadata else {}

    codec = stream.get("codec_name") if stream else None
    duration_s = safe_float((stream or {}).get("duration")) or safe_float(fmt.get("duration"))
    sample_rate_hz = safe_int((stream or {}).get("sample_rate"))
    channels = safe_int((stream or {}).get("channels"))
    bitrate_bps = safe_int((stream or {}).get("bit_rate")) or safe_int(fmt.get("bit_rate"))
    bitrate_kbps = round(bitrate_bps / 1000, 1) if bitrate_bps else None

    if not exists:
        errors.append("file missing")
    if exists and not readable:
        errors.append("file not readable")

    if not ffprobe_exe:
        warnings.append("ffprobe missing; technical metadata not collected")
    elif not metadata:
        errors.append("ffprobe failed")

    if ffprobe_exe and not stream:
        errors.append("no audio stream detected")
    if codec and codec.lower() != "mp3":
        errors.append(f"unexpected codec: {codec}")
    if duration_s is not None and duration_s <= 0:
        errors.append("duration <= 0")

    if duration_s and duration_s > cfg.duration_warn_seconds:
        warnings.append(f"duration > {cfg.duration_warn_seconds:.0f}s")
    if sample_rate_hz is not None and not (cfg.min_sample_rate <= sample_rate_hz <= cfg.max_sample_rate):
        warnings.append(
            f"sample rate outside {cfg.min_sample_rate}-{cfg.max_sample_rate} Hz: {sample_rate_hz}"
        )
    if channels is not None and channels not in (1, 2):
        warnings.append(f"unusual channel count: {channels}")
    if bitrate_kbps is not None and not (cfg.min_bitrate_kbps <= bitrate_kbps <= cfg.max_bitrate_kbps):
        warnings.append(
            f"bitrate outside {cfg.min_bitrate_kbps}-{cfg.max_bitrate_kbps} kbps: {bitrate_kbps}"
        )

    if ffmpeg_exe and exists and readable:
        decode_status, decode_note = decode_test(ffmpeg_exe, path)
        if decode_status != "ok":
            errors.append(f"decode failed: {decode_note}")
    else:
        decode_status = "not-run"
        decode_note = "ffmpeg missing; decode test not run" if not ffmpeg_exe else ""
        if not ffmpeg_exe:
            warnings.append("ffmpeg missing; decode test not run")

    if errors:
        machine_status = "fail"
    elif warnings:
        machine_status = "warn"
    else:
        machine_status = "pass"

    note_items: list[str] = []
    for note in errors + warnings + ([decode_note] if decode_note else []):
        if note and note not in note_items:
            note_items.append(note)

    return {
        "relative_path": relative_path,
        "exists": "yes" if exists else "no",
        "readable": "yes" if readable else "no",
        "size_bytes": size_bytes or "",
        "size_kib": format_kib(size_bytes),
        "audio_stream_present": "yes" if stream else "no",
        "codec": codec or "",
        "duration_s": format_seconds(duration_s),
        "sample_rate_hz": sample_rate_hz or "",
        "channels": channels or "",
        "bitrate_kbps": bitrate_kbps if bitrate_kbps is not None else "",
        "decode_status": decode_status,
        "machine_status": machine_status,
        "machine_notes": "; ".join(note_items),
        "manual_status": "",
        "manual_comment": "",
        "normalization_candidate": "",
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "relative_path",
        "exists",
        "readable",
        "size_bytes",
        "size_kib",
        "audio_stream_present",
        "codec",
        "duration_s",
        "sample_rate_hz",
        "channels",
        "bitrate_kbps",
        "decode_status",
        "machine_status",
        "machine_notes",
        "manual_status",
        "manual_comment",
        "normalization_candidate",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    cfg: AuditConfig,
    ffprobe_exe: str | None,
    ffmpeg_exe: str | None,
) -> None:
    counts = {"pass": 0, "warn": 0, "fail": 0}
    for row in rows:
        counts[row["machine_status"]] += 1

    flagged_rows = [row for row in rows if row["machine_status"] != "pass"]
    lines = [
        "# Audio Audit Report",
        "",
        f"- Audio root: `{cfg.audio_root}`",
        f"- Files scanned: {len(rows)}",
        f"- ffprobe: `{ffprobe_exe or 'missing'}`",
        f"- ffmpeg: `{ffmpeg_exe or 'missing'}`",
        f"- Pass: {counts['pass']}",
        f"- Warn: {counts['warn']}",
        f"- Fail: {counts['fail']}",
        "",
        "## Manual Review Files",
        "",
        "- `audio_audit.csv`: technical audit with manual review columns.",
        "- `audio_manual_review.csv`: identical checklist copy for hands-on QA updates.",
        "",
    ]

    if flagged_rows:
        lines.extend(["## Flagged Files", ""])
        lines.append("| File | Status | Notes |")
        lines.append("| --- | --- | --- |")
        for row in flagged_rows:
            lines.append(
                f"| `{row['relative_path']}` | {row['machine_status']} | {row['machine_notes'] or '-'} |"
            )
    else:
        lines.extend(["## Flagged Files", "", "No machine-detected issues."])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    cfg = parse_args()
    cfg.reports_dir.mkdir(parents=True, exist_ok=True)

    if not cfg.audio_root.exists():
        print(f"audio root not found: {cfg.audio_root}", file=sys.stderr)
        return 1

    ffprobe_exe = tool_path("ffprobe", cfg.ffprobe_path)
    ffmpeg_exe = tool_path("ffmpeg", cfg.ffmpeg_path)
    files = sorted(cfg.audio_root.rglob("*.mp3"))
    rows = [assess_file(path, cfg, ffprobe_exe, ffmpeg_exe) for path in files]

    audit_csv = cfg.reports_dir / "audio_audit.csv"
    manual_csv = cfg.reports_dir / "audio_manual_review.csv"
    audit_md = cfg.reports_dir / "audio_audit.md"

    write_csv(audit_csv, rows)
    shutil.copyfile(audit_csv, manual_csv)
    write_markdown(audit_md, rows, cfg, ffprobe_exe, ffmpeg_exe)

    fail_count = sum(1 for row in rows if row["machine_status"] == "fail")
    warn_count = sum(1 for row in rows if row["machine_status"] == "warn")

    print(f"Wrote {audit_csv}")
    print(f"Wrote {manual_csv}")
    print(f"Wrote {audit_md}")
    print(f"Scanned {len(rows)} MP3 files: {fail_count} fail, {warn_count} warn")
    if not ffprobe_exe or not ffmpeg_exe:
        print("ffprobe/ffmpeg missing: reports contain a manual checklist but technical audit is partial.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())