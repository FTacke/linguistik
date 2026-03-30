from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tomllib
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "zensical.toml"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "exports" / "einzelkapitel"
DEFAULT_BASE_URL = "http://127.0.0.1:8000/"
DEFAULT_MARGIN_MM = {"top": "11mm", "right": "13mm", "bottom": "16mm", "left": "13mm"}


@dataclass(frozen=True)
class Chapter:
    title: str
    md_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Export all regular chapter pages as individual PDFs via a live browser print run "
            "against the local preview server."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to zensical.toml (default: repository root zensical.toml).",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Base URL of the running local preview server (default: http://127.0.0.1:8000/).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for the generated chapter PDFs.",
    )
    parser.add_argument(
        "--browser",
        default=None,
        help="Optional path to a Chromium-based browser executable. Defaults to local Edge/Chrome detection.",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=0.7,
        help="PDF print scale (default: 0.7).",
    )
    parser.add_argument(
        "--wait-ms",
        type=int,
        default=2000,
        help="Extra wait time after page load before printing (default: 2000).",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=120000,
        help="Navigation timeout per chapter in milliseconds (default: 120000).",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        default=None,
        metavar="MD_PATH_OR_TITLE",
        help="Optional subset of chapters by markdown path or visible navigation title.",
    )
    parser.add_argument(
        "--include-index",
        action="store_true",
        help="Include index.md in the export set. Default is to export only regular chapters.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print the resolved chapter list without generating PDFs.",
    )
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else (ROOT / path).resolve()


def flatten_nav(items: list[dict[str, object]]) -> list[Chapter]:
    flat: list[Chapter] = []
    for item in items:
        for title, value in item.items():
            if isinstance(value, str):
                flat.append(Chapter(title=title, md_path=value))
            else:
                flat.extend(flatten_nav(value))
    return flat


def load_chapters(config_path: Path, include_index: bool, only: list[str] | None) -> list[Chapter]:
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    chapters = flatten_nav(config["project"]["nav"])

    if not include_index:
        chapters = [chapter for chapter in chapters if chapter.md_path != "index.md"]

    if only:
        requested = set(only)
        filtered = [
            chapter
            for chapter in chapters
            if chapter.md_path in requested or chapter.title in requested
        ]
        missing = requested.difference({chapter.md_path for chapter in filtered}).difference(
            {chapter.title for chapter in filtered}
        )
        if missing:
            raise ValueError(
                "Unknown chapter selector(s): " + ", ".join(sorted(missing))
            )
        chapters = filtered

    return chapters


def normalize_base_url(base_url: str) -> str:
    return base_url if base_url.endswith("/") else base_url + "/"


def chapter_url(base_url: str, md_path: str) -> str:
    base_url = normalize_base_url(base_url)
    if md_path == "index.md":
        return base_url
    return urljoin(base_url, md_path.removesuffix(".md") + "/")


def slugify(md_path: str) -> str:
    value = md_path.removesuffix(".md").replace("/", "-")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def check_server(base_url: str) -> None:
    request = Request(
        normalize_base_url(base_url),
        headers={"User-Agent": "linguistik-hispanistica-pdf-export"},
    )
    try:
        with urlopen(request, timeout=10) as response:
            status = getattr(response, "status", 200)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(
            f"Preview server not reachable at {base_url}. Start 'zensical serve' first."
        ) from exc

    if status >= 400:
        raise RuntimeError(
            f"Preview server returned HTTP {status} for {base_url}."
        )


def browser_candidates() -> list[str]:
    candidates: list[str] = []

    env_browser = os_environ_browser()
    if env_browser:
        candidates.append(env_browser)

    candidates.extend(
        [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
    )

    for executable in [
        "microsoft-edge",
        "microsoft-edge-stable",
        "google-chrome",
        "chrome",
        "chromium",
        "chromium-browser",
    ]:
        resolved = shutil.which(executable)
        if resolved:
            candidates.append(resolved)

    return candidates


def os_environ_browser() -> str | None:
    return os.environ.get("PDF_EXPORT_BROWSER")


def resolve_browser(browser: str | None) -> Path:
    if browser:
        browser_path = Path(browser)
        if browser_path.exists():
            return browser_path
        which_browser = shutil.which(browser)
        if which_browser:
            return Path(which_browser)
        raise RuntimeError(f"Browser executable not found: {browser}")

    for candidate in browser_candidates():
        candidate_path = Path(candidate)
        if candidate_path.exists():
            return candidate_path

    raise RuntimeError(
        "No Chromium-based browser found. Install Edge/Chrome locally or pass --browser."
    )


def export_chapters(
    chapters: list[Chapter],
    *,
    base_url: str,
    output_dir: Path,
    browser_path: Path,
    scale: float,
    wait_ms: int,
    timeout_ms: int,
) -> list[Path]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency 'playwright'. Install it with 'pip install -r tools/pdf-export/requirements.txt'."
        ) from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=str(browser_path),
            headless=True,
        )
        page = browser.new_page()

        try:
            for index, chapter in enumerate(chapters, start=1):
                url = chapter_url(base_url, chapter.md_path)
                output_path = output_dir / f"{index:02d}-{slugify(chapter.md_path)}.pdf"

                page.goto(url, wait_until="networkidle", timeout=timeout_ms)
                page.emulate_media(media="print")
                page.wait_for_timeout(wait_ms)
                page.pdf(
                    path=str(output_path),
                    format="A4",
                    scale=scale,
                    print_background=False,
                    display_header_footer=False,
                    margin=DEFAULT_MARGIN_MM,
                    prefer_css_page_size=True,
                )

                written.append(output_path)
                print(f"[{index}/{len(chapters)}] {chapter.title} -> {output_path}")
        finally:
            browser.close()

    return written


def main() -> int:
    args = parse_args()

    config_path = resolve_path(args.config)
    output_dir = resolve_path(args.output_dir)

    try:
        chapters = load_chapters(config_path, args.include_index, args.only)
    except (FileNotFoundError, KeyError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.dry_run:
        for index, chapter in enumerate(chapters, start=1):
            print(f"{index:02d} {chapter.title} :: {chapter.md_path} :: {chapter_url(args.base_url, chapter.md_path)}")
        return 0

    try:
        check_server(args.base_url)
        browser_path = resolve_browser(args.browser)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        written = export_chapters(
            chapters,
            base_url=args.base_url,
            output_dir=output_dir,
            browser_path=browser_path,
            scale=args.scale,
            wait_ms=args.wait_ms,
            timeout_ms=args.timeout_ms,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Exported {len(written)} chapter PDF(s) to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())