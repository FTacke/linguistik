from __future__ import annotations

import html
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://api.github.com/repos/FTacke/linguistik/releases/latest"
FALLBACK_VERSION = os.environ.get("FOOTER_RELEASE_FALLBACK", "development")
FALLBACK_URL = "https://github.com/FTacke/linguistik/releases"
TARGET_PATH = Path("overrides/partials/footer-release.html")


def fetch_latest_release() -> tuple[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "linguistik-hispanistica-footer-build",
    }

    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    request = Request(API_URL, headers=headers)

    try:
        with urlopen(request, timeout=10) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return FALLBACK_VERSION, FALLBACK_URL

    version = payload.get("tag_name") or payload.get("name") or FALLBACK_VERSION
    release_url = payload.get("html_url") or FALLBACK_URL
    return str(version), str(release_url)


def write_partial(version: str, release_url: str) -> None:
    TARGET_PATH.parent.mkdir(parents=True, exist_ok=True)
    TARGET_PATH.write_text(
        (
            f'<a class="footer-version-link" href="{html.escape(release_url, quote=True)}">'
            f"{html.escape(version)}"
            "</a>\n"
        ),
        encoding="utf-8",
    )


def main() -> None:
    version, release_url = fetch_latest_release()
    write_partial(version, release_url)


if __name__ == "__main__":
    main()