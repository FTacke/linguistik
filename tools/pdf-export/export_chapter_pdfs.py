from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import sys
from tempfile import TemporaryDirectory
import tomllib
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "zensical.toml"
DEFAULT_EXPORT_DIR = ROOT / "docs" / "exports"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "exports" / "einzelkapitel"
DEFAULT_BASE_URL = "http://127.0.0.1:8000/"
DEFAULT_MARGIN_MM = {"top": "11mm", "right": "13mm", "bottom": "16mm", "left": "13mm"}
DEFAULT_COVER_SCALE = 0.92
PAGE_NUMBER_FONT_PATH = "assets/fonts/source-serif-4/source-serif-4-latin-normal.woff2"
PAGE_NUMBER_FONT_SIZE_PT = 10
PAGE_NUMBER_BOTTOM_MM = 11


@dataclass(frozen=True)
class Chapter:
    title: str
    md_path: str


@dataclass(frozen=True)
class ExportSettings:
    chapters: list[Chapter]
    cover_chapter: Chapter | None
    public_base_url: str | None
    site_name: str


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
        "--public-base-url",
        default=None,
        help=(
            "Public base URL to embed in cross-page chapter links inside the PDFs. "
            "Defaults to project.site_url from zensical.toml."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for the generated chapter PDFs.",
    )
    parser.add_argument(
        "--combined-output",
        type=Path,
        default=None,
        help=(
            "Optional path for the combined PDF. Defaults to docs/exports/<site_name>.pdf."
        ),
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
        "--cover-scale",
        type=float,
        default=DEFAULT_COVER_SCALE,
        help="PDF print scale for index.md when used as the combined PDF title page (default: 0.92).",
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


def load_export_settings(
    config_path: Path,
    include_index: bool,
    only: list[str] | None,
    public_base_url: str | None,
) -> ExportSettings:
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    site_name = str(config["project"]["site_name"])
    all_chapters = flatten_nav(config["project"]["nav"])
    chapters = list(all_chapters)
    config_public_base_url = config["project"].get("site_url")
    cover_chapter = next((chapter for chapter in all_chapters if chapter.md_path == "index.md"), None)

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

    resolved_public_base_url = public_base_url or config_public_base_url
    normalized_public_base_url = (
        normalize_base_url(str(resolved_public_base_url)) if resolved_public_base_url else None
    )

    return ExportSettings(
        chapters=chapters,
        cover_chapter=cover_chapter,
        public_base_url=normalized_public_base_url,
        site_name=site_name,
    )


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


def rewrite_local_links(page: object, *, local_base_url: str, public_base_url: str | None) -> None:
    if not public_base_url:
        return

    page.evaluate(
        """
        ({ localBaseUrl, publicBaseUrl }) => {
            const localBase = localBaseUrl.endsWith('/') ? localBaseUrl : `${localBaseUrl}/`;
            const publicBase = publicBaseUrl.endsWith('/') ? publicBaseUrl : `${publicBaseUrl}/`;
            const currentUrl = new URL(window.location.href);

            for (const anchor of document.querySelectorAll('a[href]')) {
                const rawHref = anchor.getAttribute('href') || '';
                if (!rawHref || rawHref.startsWith('#')) {
                    continue;
                }

                const protocolMatch = rawHref.match(/^[a-zA-Z][a-zA-Z0-9+.-]*:/);
                if (protocolMatch && !rawHref.startsWith(localBase)) {
                    continue;
                }

                const resolvedHref = anchor.href;
                if (!resolvedHref.startsWith(localBase)) {
                    continue;
                }

                const resolvedUrl = new URL(resolvedHref);
                const isSamePage = (
                    resolvedUrl.pathname === currentUrl.pathname
                    && resolvedUrl.search === currentUrl.search
                );

                if (isSamePage) {
                    continue;
                }

                anchor.href = `${publicBase}${resolvedHref.slice(localBase.length)}`;
            }
        }
        """,
        {
            "localBaseUrl": normalize_base_url(local_base_url),
            "publicBaseUrl": public_base_url,
        },
    )


def render_pdf(
    page: object,
    chapter: Chapter,
    *,
    base_url: str,
    public_base_url: str | None,
    output_path: Path,
    scale: float,
    wait_ms: int,
    timeout_ms: int,
) -> Path:
    url = chapter_url(base_url, chapter.md_path)

    page.goto(url, wait_until="networkidle", timeout=timeout_ms)
    rewrite_local_links(
        page,
        local_base_url=base_url,
        public_base_url=public_base_url,
    )
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

    return output_path


def wait_for_fonts(page: object) -> None:
    page.evaluate(
        """
        async () => {
            if (document.fonts) {
                await document.fonts.ready;
            }
        }
        """
    )


def page_number_font_url(base_url: str) -> str:
    return urljoin(normalize_base_url(base_url), PAGE_NUMBER_FONT_PATH)


def to_roman(number: int) -> str:
    if number <= 0:
        raise ValueError("Roman numerals require a positive integer.")

    numerals = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    result: list[str] = []
    remainder = number

    for value, symbol in numerals:
        while remainder >= value:
            result.append(symbol)
            remainder -= value

    return "".join(result)


def render_page_number_overlay_pdf(
    page: object,
    *,
    base_url: str,
    output_path: Path,
    page_labels: list[str | None],
) -> Path:
    overlay_sections = "".join(
        (
            '<section class="overlay-page">'
            + (
                f'<div class="page-number">{html.escape(page_label)}</div>'
                if page_label is not None
                else ""
            )
            + "</section>"
        )
        for page_label in page_labels
    )

    markup = f"""
        <!doctype html>
        <html lang="de">
          <head>
            <meta charset="utf-8">
            <style>
              @page {{
                size: A4;
                margin: 0;
              }}

              @font-face {{
                font-family: "Source Serif 4";
                font-style: normal;
                font-weight: 400;
                src: url("{html.escape(page_number_font_url(base_url), quote=True)}") format("woff2");
              }}

              html, body {{
                margin: 0;
                padding: 0;
                background: transparent;
              }}

              body {{
                font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
              }}

              .overlay-page {{
                position: relative;
                width: 210mm;
                height: 297mm;
                break-after: page;
                page-break-after: always;
              }}

              .overlay-page:last-child {{
                break-after: auto;
                page-break-after: auto;
              }}

              .page-number {{
                position: absolute;
                left: 0;
                right: 0;
                bottom: {PAGE_NUMBER_BOTTOM_MM}mm;
                text-align: center;
                font-size: {PAGE_NUMBER_FONT_SIZE_PT}pt;
                line-height: 1;
                color: #222;
              }}
            </style>
          </head>
          <body>
            {overlay_sections}
          </body>
        </html>
    """

    page.set_content(markup, wait_until="load")
    wait_for_fonts(page)
    page.pdf(
        path=str(output_path),
        format="A4",
        scale=1,
        print_background=False,
        display_header_footer=False,
        margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
        prefer_css_page_size=True,
    )

    return output_path


def export_chapters(
    chapters: list[Chapter],
    *,
    base_url: str,
    public_base_url: str | None,
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
                output_path = output_dir / f"{index:02d}-{slugify(chapter.md_path)}.pdf"

                written.append(
                    render_pdf(
                        page,
                        chapter,
                        base_url=base_url,
                        public_base_url=public_base_url,
                        output_path=output_path,
                        scale=scale,
                        wait_ms=wait_ms,
                        timeout_ms=timeout_ms,
                    )
                )
                print(f"[{index}/{len(chapters)}] {chapter.title} -> {output_path}")
        finally:
            browser.close()

    return written


def combined_output_path(output_path: Path | None, site_name: str) -> Path:
    if output_path is not None:
        return resolve_path(output_path)
    return DEFAULT_EXPORT_DIR / f"{site_name}.pdf"


def append_pdf(writer: object, pdf_path: Path) -> None:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    for page in reader.pages:
        writer.add_page(page)


def first_page_size(pdf_path: Path) -> tuple[float, float]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    if not reader.pages:
        raise RuntimeError(f"Generated PDF contains no pages: {pdf_path}")

    first_page = reader.pages[0]
    return float(first_page.mediabox.width), float(first_page.mediabox.height)


def last_page_has_text(pdf_path: Path) -> bool:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    if not reader.pages:
        raise RuntimeError(f"Generated PDF contains no pages: {pdf_path}")

    text = (reader.pages[-1].extract_text() or "").strip()
    return bool(text)


def page_count(pdf_path: Path) -> int:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    return len(reader.pages)


def chapter_numbering_style(chapter: Chapter) -> str:
    return "roman" if chapter.md_path == "vorwort.md" else "arabic"


def build_chapter_page_labels(
    chapter: Chapter,
    chapter_page_count: int,
    roman_page_number: int,
    arabic_page_number: int,
) -> tuple[list[str | None], int, int, str]:
    numbering_style = chapter_numbering_style(chapter)

    if numbering_style == "roman":
        labels = [to_roman(number) for number in range(roman_page_number, roman_page_number + chapter_page_count)]
        return labels, roman_page_number + chapter_page_count, arabic_page_number, numbering_style

    labels = [str(number) for number in range(arabic_page_number, arabic_page_number + chapter_page_count)]
    return labels, roman_page_number, arabic_page_number + chapter_page_count, numbering_style


def fallback_combined_output_path(output_path: Path) -> Path:
    return output_path.with_name(f"{output_path.stem}_neu{output_path.suffix}")


def export_combined_pdf(
    *,
    cover_chapter: Chapter | None,
    chapters: list[Chapter],
    chapter_pdf_paths: list[Path],
    base_url: str,
    public_base_url: str | None,
    output_path: Path,
    browser_path: Path,
    cover_scale: float,
    wait_ms: int,
    timeout_ms: int,
) -> Path:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency 'playwright'. Install it with 'pip install -r tools/pdf-export/requirements.txt'."
        ) from exc

    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency 'pypdf'. Install it with 'pip install -r tools/pdf-export/requirements.txt'."
        ) from exc

    if cover_chapter is None and not chapter_pdf_paths:
        raise RuntimeError("No pages available for combined PDF export.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory(prefix="pdf-export-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        cover_pdf_path: Path | None = None
        overlay_pdf_path: Path | None = None
        blank_page_width = 595.276
        blank_page_height = 841.89

        if cover_chapter is not None:
            cover_pdf_path = temp_dir / "00-cover.pdf"
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(
                    executable_path=str(browser_path),
                    headless=True,
                )
                page = browser.new_page()
                try:
                    render_pdf(
                        page,
                        cover_chapter,
                        base_url=base_url,
                        public_base_url=public_base_url,
                        output_path=cover_pdf_path,
                        scale=cover_scale,
                        wait_ms=wait_ms,
                        timeout_ms=timeout_ms,
                    )
                finally:
                    browser.close()

        writer = PdfWriter()
        page_labels: list[str | None] = []
        roman_page_number = 1
        arabic_page_number = 1
        last_numbering_style: str | None = None

        if cover_pdf_path is not None:
            append_pdf(writer, cover_pdf_path)
            cover_page_total = page_count(cover_pdf_path)
            page_labels.extend([None] * cover_page_total)
            blank_page_width, blank_page_height = first_page_size(cover_pdf_path)
            if chapters and last_page_has_text(cover_pdf_path):
                writer.add_blank_page(width=blank_page_width, height=blank_page_height)
                page_labels.append(None)

        for chapter, chapter_pdf_path in zip(chapters, chapter_pdf_paths, strict=False):
            if writer.pages and (len(writer.pages) + 1) % 2 == 0:
                writer.add_blank_page(width=blank_page_width, height=blank_page_height)
                page_labels.append(None)
                if last_numbering_style == "roman":
                    roman_page_number += 1
                elif last_numbering_style == "arabic":
                    arabic_page_number += 1

            append_pdf(writer, chapter_pdf_path)
            chapter_page_total = page_count(chapter_pdf_path)
            blank_page_width, blank_page_height = first_page_size(chapter_pdf_path)
            chapter_labels, roman_page_number, arabic_page_number, last_numbering_style = build_chapter_page_labels(
                chapter,
                chapter_page_total,
                roman_page_number,
                arabic_page_number,
            )
            page_labels.extend(chapter_labels)

        if any(label is not None for label in page_labels):
            overlay_pdf_path = temp_dir / "page-number-overlay.pdf"
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(
                    executable_path=str(browser_path),
                    headless=True,
                )
                page = browser.new_page()
                try:
                    render_page_number_overlay_pdf(
                        page,
                        base_url=base_url,
                        output_path=overlay_pdf_path,
                        page_labels=page_labels,
                    )
                finally:
                    browser.close()

            overlay_reader = PdfReader(str(overlay_pdf_path))
            for page_index, page_label in enumerate(page_labels):
                if page_label is None:
                    continue
                writer.pages[page_index].merge_page(overlay_reader.pages[page_index])

        try:
            with output_path.open("wb") as file_handle:
                writer.write(file_handle)
            return output_path
        except PermissionError:
            fallback_output_path = fallback_combined_output_path(output_path)
            try:
                with fallback_output_path.open("wb") as file_handle:
                    writer.write(file_handle)
            except PermissionError as exc:
                raise RuntimeError(
                    f"Cannot write combined PDF to {output_path} or fallback file {fallback_output_path}. Close the file in any PDF viewer/editor and run the export again."
                ) from exc
            print(f"Combined PDF target locked; wrote fallback file to {fallback_output_path}")
            return fallback_output_path

    return output_path


def main() -> int:
    args = parse_args()

    config_path = resolve_path(args.config)
    output_dir = resolve_path(args.output_dir)

    try:
        settings = load_export_settings(
            config_path,
            args.include_index,
            args.only,
            args.public_base_url,
        )
    except (FileNotFoundError, KeyError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    combined_pdf_path = combined_output_path(args.combined_output, settings.site_name)
    combined_chapters = [chapter for chapter in settings.chapters if chapter.md_path != "index.md"]

    if args.dry_run:
        for index, chapter in enumerate(settings.chapters, start=1):
            print(f"{index:02d} {chapter.title} :: {chapter.md_path} :: {chapter_url(args.base_url, chapter.md_path)}")
        cover_title = settings.cover_chapter.title if settings.cover_chapter else "<none>"
        print(f"COMBINED COVER :: {cover_title}")
        print(f"COMBINED OUTPUT :: {combined_pdf_path}")
        return 0

    try:
        check_server(args.base_url)
        browser_path = resolve_browser(args.browser)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        written = export_chapters(
            settings.chapters,
            base_url=args.base_url,
            public_base_url=settings.public_base_url,
            output_dir=output_dir,
            browser_path=browser_path,
            scale=args.scale,
            wait_ms=args.wait_ms,
            timeout_ms=args.timeout_ms,
        )
        combined_pdf = export_combined_pdf(
            cover_chapter=settings.cover_chapter,
            chapters=combined_chapters,
            chapter_pdf_paths=[
                pdf_path
                for chapter, pdf_path in zip(settings.chapters, written, strict=False)
                if chapter.md_path != "index.md"
            ],
            base_url=args.base_url,
            public_base_url=settings.public_base_url,
            output_path=combined_pdf_path,
            browser_path=browser_path,
            cover_scale=args.cover_scale,
            wait_ms=args.wait_ms,
            timeout_ms=args.timeout_ms,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Exported {len(written)} chapter PDF(s) to {output_dir}")
    print(f"Exported combined PDF to {combined_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())