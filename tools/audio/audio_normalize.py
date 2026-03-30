from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
DEFAULT_AUDIO_ROOT = REPO_ROOT / "docs" / "assets" / "audiofiles"
DEFAULT_OUTPUT_ROOT = SCRIPT_DIR / "normalized"
DEFAULT_REPORTS_DIR = SCRIPT_DIR / "reports"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize MP3 files to a more consistent speech loudness using ffmpeg loudnorm."
    )
    parser.add_argument("--audio-root", type=Path, default=DEFAULT_AUDIO_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    parser.add_argument("--integrated-loudness", type=float, default=-19.0)
    parser.add_argument("--true-peak", type=float, default=-1.5)
    parser.add_argument("--lra", type=float, default=7.0)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--filter", dest="name_filter", default="")
    parser.add_argument("--ffmpeg", type=Path, default=None)
    parser.add_argument("--ffprobe", type=Path, default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--promote", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


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


def resolve_tool_path(name: str, explicit_path: Path | None = None) -> str | None:
    if explicit_path:
        return str(explicit_path.resolve())

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


def collect_audio_stream(metadata: dict[str, Any] | None) -> dict[str, Any] | None:
    if not metadata:
        return None
    for stream in metadata.get("streams", []):
        if stream.get("codec_type") == "audio":
            return stream
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
            "NUL",
        ]
    )
    if result.returncode == 0:
        return "ok", ""
    message = (result.stderr or result.stdout).strip()
    if not message:
        return "failed", "decode test failed"
    return "failed", message.splitlines()[-1]


def verify_output(ffprobe_exe: str, ffmpeg_exe: str, file_path: Path) -> tuple[dict[str, Any], list[str]]:
    metadata = ffprobe_metadata(ffprobe_exe, file_path)
    stream = collect_audio_stream(metadata)
    fmt = metadata.get("format", {}) if metadata else {}
    notes: list[str] = []

    codec = stream.get("codec_name") if stream else None
    duration_s = safe_float((stream or {}).get("duration")) or safe_float(fmt.get("duration"))
    sample_rate_hz = safe_int((stream or {}).get("sample_rate"))
    channels = safe_int((stream or {}).get("channels"))
    bitrate_bps = safe_int((stream or {}).get("bit_rate")) or safe_int(fmt.get("bit_rate"))
    bitrate_kbps = round(bitrate_bps / 1000, 1) if bitrate_bps else None
    decode_status, decode_note = decode_test(ffmpeg_exe, file_path)

    if not metadata:
        notes.append("ffprobe validation failed")
    if not stream:
        notes.append("no audio stream detected")
    if codec and codec.lower() != "mp3":
        notes.append(f"unexpected output codec: {codec}")
    if duration_s is not None and duration_s <= 0:
        notes.append("output duration <= 0")
    if decode_status != "ok":
        notes.append(decode_note)

    return {
        "output_codec": codec or "",
        "output_duration_s": f"{duration_s:.3f}" if duration_s is not None else "",
        "output_sample_rate_hz": sample_rate_hz or "",
        "output_channels": channels or "",
        "output_bitrate_kbps": bitrate_kbps if bitrate_kbps is not None else "",
        "output_decode_status": decode_status,
    }, notes


def last_message(result: subprocess.CompletedProcess[str]) -> str:
    message = (result.stderr or result.stdout).strip()
    if not message:
        return "command failed"
    return message.splitlines()[-1]


def parse_loudnorm_json(output: str) -> dict[str, Any] | None:
    matches = re.findall(r"\{\s*\"input_i\".*?\}", output, flags=re.DOTALL)
    if not matches:
        return None
    try:
        return json.loads(matches[-1])
    except json.JSONDecodeError:
        return None


def build_pass1_filter(args: argparse.Namespace) -> str:
    return (
        f"loudnorm=I={args.integrated_loudness}:TP={args.true_peak}:"
        f"LRA={args.lra}:print_format=json"
    )


def build_pass2_filter(args: argparse.Namespace, measured: dict[str, Any]) -> str:
    return (
        f"loudnorm=I={args.integrated_loudness}:TP={args.true_peak}:LRA={args.lra}:"
        f"measured_I={measured['input_i']}:measured_LRA={measured['input_lra']}:"
        f"measured_TP={measured['input_tp']}:measured_thresh={measured['input_thresh']}:"
        f"offset={measured['target_offset']}:linear=true:print_format=summary"
    )


def write_reports(reports_dir: Path, rows: list[dict[str, Any]], args: argparse.Namespace) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)
    csv_path = reports_dir / "audio_normalization.csv"
    md_path = reports_dir / "audio_normalization.md"

    fieldnames = [
        "source_path",
        "output_path",
        "status",
        "input_i",
        "input_tp",
        "input_lra",
        "target_offset",
        "output_codec",
        "output_duration_s",
        "output_sample_rate_hz",
        "output_channels",
        "output_bitrate_kbps",
        "output_decode_status",
        "notes",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    success_count = sum(1 for row in rows if row["status"] in {"normalized", "promoted"})
    fail_count = sum(1 for row in rows if row["status"] == "failed")
    skipped_count = sum(1 for row in rows if row["status"].startswith("skipped"))

    lines = [
        "# Audio Normalization Report",
        "",
        f"- Audio root: `{Path(args.audio_root).resolve()}`",
        f"- Output root: `{Path(args.output_root).resolve()}`",
        f"- Target integrated loudness: {args.integrated_loudness} LUFS",
        f"- Target true peak: {args.true_peak} dBTP",
        f"- Target loudness range: {args.lra} LU",
        f"- Promote to source tree: {'yes' if args.promote else 'no'}",
        f"- Dry run: {'yes' if args.dry_run else 'no'}",
        f"- Normalized: {success_count}",
        f"- Failed: {fail_count}",
        f"- Skipped: {skipped_count}",
        "",
        "| Source | Output | Status | Notes |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['source_path']}` | `{row['output_path']}` | {row['status']} | {row['notes'] or '-'} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    audio_root = Path(args.audio_root).resolve()
    output_root = Path(args.output_root).resolve()
    reports_dir = Path(args.reports_dir).resolve()

    ffmpeg_exe = resolve_tool_path("ffmpeg", args.ffmpeg)
    ffprobe_exe = resolve_tool_path("ffprobe", args.ffprobe)
    if not ffmpeg_exe or not ffprobe_exe:
        write_reports(
            reports_dir,
            [
                {
                    "source_path": "",
                    "output_path": "",
                    "status": "blocked-prerequisite",
                    "input_i": "",
                    "input_tp": "",
                    "input_lra": "",
                    "target_offset": "",
                    "output_codec": "",
                    "output_duration_s": "",
                    "output_sample_rate_hz": "",
                    "output_channels": "",
                    "output_bitrate_kbps": "",
                    "output_decode_status": "",
                    "notes": "ffmpeg and/or ffprobe not available on PATH",
                }
            ],
            args,
        )
        print("ffmpeg and ffprobe are required for loudnorm processing.", file=sys.stderr)
        return 1

    if not audio_root.exists():
        print(f"audio root not found: {audio_root}", file=sys.stderr)
        return 1

    source_files = sorted(audio_root.rglob("*.mp3"))
    if args.name_filter:
        source_files = [path for path in source_files if args.name_filter.lower() in path.as_posix().lower()]
    if args.limit > 0:
        source_files = source_files[: args.limit]

    output_root.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    for source_path in source_files:
        relative_path = source_path.relative_to(audio_root)
        output_path = output_root / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        row = {
            "source_path": relative_path.as_posix(),
            "output_path": output_path.relative_to(output_root).as_posix(),
            "status": "",
            "input_i": "",
            "input_tp": "",
            "input_lra": "",
            "target_offset": "",
            "output_codec": "",
            "output_duration_s": "",
            "output_sample_rate_hz": "",
            "output_channels": "",
            "output_bitrate_kbps": "",
            "output_decode_status": "",
            "notes": "",
        }

        if output_path.exists() and not args.overwrite:
            row["status"] = "skipped-existing"
            row["notes"] = "output already exists; use --overwrite to replace it"
            rows.append(row)
            continue

        pass1 = run_command(
            [
                ffmpeg_exe,
                "-hide_banner",
                "-nostats",
                "-i",
                str(source_path),
                "-af",
                build_pass1_filter(args),
                "-f",
                "null",
                "-",
            ]
        )
        measured = parse_loudnorm_json(pass1.stderr + "\n" + pass1.stdout)
        if pass1.returncode != 0 or not measured:
            row["status"] = "failed"
            row["notes"] = last_message(pass1)
            rows.append(row)
            continue

        row["input_i"] = measured.get("input_i", "")
        row["input_tp"] = measured.get("input_tp", "")
        row["input_lra"] = measured.get("input_lra", "")
        row["target_offset"] = measured.get("target_offset", "")

        if args.dry_run:
            row["status"] = "skipped-dry-run"
            row["notes"] = "analysis only"
            rows.append(row)
            continue

        pass2 = run_command(
            [
                ffmpeg_exe,
                "-hide_banner",
                "-y",
                "-i",
                str(source_path),
                "-af",
                build_pass2_filter(args, measured),
                "-codec:a",
                "libmp3lame",
                "-q:a",
                "2",
                str(output_path),
            ]
        )
        if pass2.returncode != 0:
            row["status"] = "failed"
            row["notes"] = last_message(pass2)
            rows.append(row)
            continue

        verification, verification_notes = verify_output(ffprobe_exe, ffmpeg_exe, output_path)
        row.update(verification)
        if verification_notes:
            row["status"] = "failed"
            row["notes"] = "; ".join(dict.fromkeys(verification_notes))
            rows.append(row)
            continue

        if args.promote:
            try:
                shutil.copy2(output_path, source_path)
            except OSError as exc:
                row["status"] = "failed"
                row["notes"] = f"promotion failed: {exc}"
                rows.append(row)
                continue
            row["status"] = "promoted"
            row["notes"] = "two-pass loudnorm completed, validated, and copied over source"
        else:
            row["status"] = "normalized"
            row["notes"] = "two-pass loudnorm completed and validated"
        rows.append(row)

    write_reports(reports_dir, rows, args)
    print(f"Wrote {reports_dir / 'audio_normalization.csv'}")
    print(f"Wrote {reports_dir / 'audio_normalization.md'}")
    print(f"Processed {len(rows)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())