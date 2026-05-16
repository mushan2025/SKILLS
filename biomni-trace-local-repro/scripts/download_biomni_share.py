#!/usr/bin/env python3
"""Discover and download reachable files behind a Biomni share URL.

This helper intentionally uses only the Python standard library so a Codex
agent can run it in minimal environments. It is a discovery assistant, not a
guarantee that every private or expired Biomni artifact can be fetched.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html.parser
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TEXT_HINTS = (
    "text/",
    "application/json",
    "application/javascript",
    "application/x-javascript",
    "application/xml",
    "application/x-ndjson",
)

FILE_EXT_RE = re.compile(
    r"""(?ix)
    (?:
      https?://[^\s"'<>\\)]+
      |
      /[A-Za-z0-9_\-./%?=&:]+
      |
      [A-Za-z0-9_\-./]+
    )
    \.(?:json|csv|tsv|txt|md|r|R|py|ipynb|html|png|jpg|jpeg|svg|pdf|gz|zip)
    (?:\?[A-Za-z0-9_\-./%=&:]+)?
    """
)

TOKEN_RE = re.compile(r"(share_[A-Za-z0-9]+|replay[_\-]?[A-Za-z0-9]+|trace[_\-]?[A-Za-z0-9]+)")


@dataclass
class FetchResult:
    url: str
    final_url: str
    status: int | str
    content_type: str
    data: bytes
    error: str = ""


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key.lower() in {"href", "src"} and value:
                self.links.append(value)


def safe_name(text: str, max_len: int = 120) -> str:
    parsed = urllib.parse.urlparse(text)
    base = parsed.path.strip("/").replace("/", "__") or parsed.netloc or "response"
    if parsed.query:
        base += "__" + hashlib.sha1(parsed.query.encode("utf-8")).hexdigest()[:10]
    base = re.sub(r"[^A-Za-z0-9_.=-]+", "_", base)
    return (base[:max_len] or "response").strip("._")


def extract_token(url: str) -> str:
    matches = TOKEN_RE.findall(url)
    if matches:
        return matches[0]
    parsed = urllib.parse.urlparse(url)
    for part in reversed([p for p in parsed.path.split("/") if p]):
        if len(part) >= 8:
            return re.sub(r"[^A-Za-z0-9_-]+", "_", part)[:80]
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


def fetch(url: str, timeout: int, max_bytes: int) -> FetchResult:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Codex Biomni trace downloader/1.0",
            "Accept": "*/*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read(max_bytes + 1)
            if len(data) > max_bytes:
                data = data[:max_bytes]
                error = f"truncated_at_{max_bytes}_bytes"
            else:
                error = ""
            return FetchResult(
                url=url,
                final_url=resp.geturl(),
                status=getattr(resp, "status", "OK"),
                content_type=resp.headers.get("Content-Type", ""),
                data=data,
                error=error,
            )
    except urllib.error.HTTPError as exc:
        body = exc.read(min(max_bytes, 65536))
        return FetchResult(url, exc.geturl(), exc.code, exc.headers.get("Content-Type", ""), body, str(exc))
    except Exception as exc:  # noqa: BLE001 - downloader records failures instead of crashing.
        return FetchResult(url, url, "ERROR", "", b"", repr(exc))


def is_text(content_type: str, data: bytes) -> bool:
    lowered = content_type.lower()
    if any(hint in lowered for hint in TEXT_HINTS):
        return True
    sample = data[:2048]
    if b"\x00" in sample:
        return False
    try:
        sample.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def save_response(result: FetchResult, root: Path, subdir: str) -> Path:
    target_dir = root / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    suffix = mimetypes.guess_extension(result.content_type.split(";")[0].strip()) or ""
    name = safe_name(result.final_url or result.url)
    if suffix and not name.lower().endswith(suffix.lower()):
        name += suffix
    path = target_dir / name
    if path.exists():
        stem, ext = path.stem, path.suffix
        path = target_dir / f"{stem}_{hashlib.sha1(result.url.encode()).hexdigest()[:8]}{ext}"
    path.write_bytes(result.data)
    (path.with_suffix(path.suffix + ".headers.txt")).write_text(
        f"url: {result.url}\nfinal_url: {result.final_url}\nstatus: {result.status}\ncontent_type: {result.content_type}\nerror: {result.error}\n",
        encoding="utf-8",
    )
    return path


def html_links(data: bytes) -> list[str]:
    parser = LinkParser()
    try:
        parser.feed(data.decode("utf-8", errors="replace"))
    except Exception:
        return []
    return parser.links


def regex_links(text: str) -> list[str]:
    found = set()
    for match in FILE_EXT_RE.findall(text):
        found.add(match.strip())
    for match in re.findall(r"""(?i)(?:api|public|replay|trace|result|manifest|download)[A-Za-z0-9_\-./?=&:%]+""", text):
        if "/" in match or "." in match:
            found.add(match)
    return sorted(found)


def resolve_links(base_url: str, candidates: Iterable[str]) -> list[str]:
    urls = []
    for candidate in candidates:
        candidate = candidate.strip().strip('"').strip("'")
        if not candidate or candidate.startswith(("data:", "mailto:", "javascript:")):
            continue
        urls.append(urllib.parse.urljoin(base_url, candidate))
    return sorted(set(urls))


def common_probe_urls(original_url: str, final_url: str, token: str) -> list[str]:
    bases = []
    for url in [original_url, final_url]:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme and parsed.netloc:
            bases.append(f"{parsed.scheme}://{parsed.netloc}")
    bases = list(dict.fromkeys(bases))
    paths = [
        f"/v2/public/replays/{token}",
        f"/public/replays/{token}",
        f"/api/v2/public/replays/{token}",
        f"/api/public/replays/{token}",
        f"/api/replays/{token}",
        f"/download_plan.json",
        f"/s3_download_plan.json",
        f"/results.json",
        f"/files/execution_trace/NOTES.md",
        f"/execution_trace/NOTES.md",
    ]
    return [urllib.parse.urljoin(base, path) for base in bases for path in paths]


def write_manifest(rows: list[dict[str, str]], path: Path) -> None:
    columns = ["url", "final_url", "status", "content_type", "bytes", "local_path", "error", "note"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(columns) + "\n")
        for row in rows:
            handle.write("\t".join(str(row.get(col, "")).replace("\t", " ") for col in columns) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download reachable content behind a Biomni share URL.")
    parser.add_argument("url", help="Biomni share URL")
    parser.add_argument("--out", default="biomni_traces", help="Output root directory")
    parser.add_argument("--max-files", type=int, default=250, help="Maximum URLs to fetch")
    parser.add_argument("--max-bytes", type=int, default=50_000_000, help="Maximum bytes per response")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument("--no-common-probes", action="store_true", help="Do not try common public replay routes")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = extract_token(args.url)
    date = _dt.datetime.now().strftime("%Y%m%d")
    out_root = Path(args.out) / f"{token}_{date}"
    raw_dir = out_root / "raw_responses"
    files_dir = out_root / "files"
    out_root.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    files_dir.mkdir(parents=True, exist_ok=True)

    (out_root / "SOURCE_URL.txt").write_text(args.url + "\n", encoding="utf-8")

    queue: list[str] = [args.url]
    seen: set[str] = set()
    manifest: list[dict[str, str]] = []
    discovered: set[str] = set()

    while queue and len(seen) < args.max_files:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        result = fetch(url, args.timeout, args.max_bytes)
        subdir = "raw_responses" if url == args.url or is_text(result.content_type, result.data) else "files"
        local_path = save_response(result, out_root, subdir) if result.data else Path("")
        manifest.append(
            {
                "url": result.url,
                "final_url": result.final_url,
                "status": str(result.status),
                "content_type": result.content_type,
                "bytes": str(len(result.data)),
                "local_path": str(local_path),
                "error": result.error,
                "note": "text_or_initial" if subdir == "raw_responses" else "binary_or_asset",
            }
        )

        if not result.data or not is_text(result.content_type, result.data):
            continue

        text = result.data.decode("utf-8", errors="replace")
        link_candidates = html_links(result.data) + regex_links(text)
        resolved = resolve_links(result.final_url or url, link_candidates)
        for new_url in resolved:
            discovered.add(new_url)
            if new_url not in seen and len(queue) + len(seen) < args.max_files:
                queue.append(new_url)

        if url == args.url and not args.no_common_probes:
            for probe in common_probe_urls(args.url, result.final_url, token):
                if probe not in seen and probe not in queue:
                    queue.append(probe)

        time.sleep(0.05)

    write_manifest(manifest, out_root / "download_manifest.tsv")
    (out_root / "discovered_urls.txt").write_text("\n".join(sorted(discovered)) + "\n", encoding="utf-8")
    print(f"Saved Biomni share discovery to: {out_root}")
    print(f"Fetched {len(manifest)} URL(s); discovered {len(discovered)} candidate URL(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
