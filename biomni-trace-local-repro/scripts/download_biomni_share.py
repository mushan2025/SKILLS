#!/usr/bin/env python3
"""Discover and download reachable files behind one or more Biomni share URLs.

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
            if max_bytes and max_bytes > 0:
                data = resp.read(max_bytes + 1)
            else:
                data = resp.read()
            if max_bytes and max_bytes > 0 and len(data) > max_bytes:
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


def replay_api_bases(original_url: str, final_url: str) -> list[str]:
    bases = []
    for url in [original_url, final_url]:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme and parsed.netloc:
            bases.append(f"{parsed.scheme}://{parsed.netloc}")
            if parsed.netloc.lower().endswith("phylo.bio"):
                bases.append(f"{parsed.scheme}://api.phylo.bio")
    return list(dict.fromkeys(bases))


def common_probe_urls(original_url: str, final_url: str, token: str) -> list[str]:
    bases = replay_api_bases(original_url, final_url)
    paths = [
        f"/v2/public/replays/{token}",
        f"/v2/public/replays/{token}/results",
        f"/public/replays/{token}",
        f"/public/replays/{token}/results",
        f"/api/v2/public/replays/{token}",
        f"/api/v2/public/replays/{token}/results",
        f"/api/public/replays/{token}",
        f"/api/public/replays/{token}/results",
        f"/api/replays/{token}",
        f"/api/replays/{token}/results",
        f"/download_plan.json",
        f"/s3_download_plan.json",
        f"/results.json",
        f"/files/execution_trace/NOTES.md",
        f"/execution_trace/NOTES.md",
    ]
    return [urllib.parse.urljoin(base, path) for base in bases for path in paths]


def result_download_urls(text: str, current_url: str, token: str) -> list[str]:
    try:
        payload = json.loads(text)
    except Exception:
        return []

    ids: set[str] = set()
    direct_urls: set[str] = set()

    def walk(value: object) -> None:
        if isinstance(value, dict):
            for key, inner in value.items():
                lowered = key.lower()
                if lowered in {"result_id", "file_id"} and isinstance(inner, str):
                    ids.add(inner)
                elif lowered in {"download_url", "url"} and isinstance(inner, str) and inner.startswith("http"):
                    direct_urls.add(inner)
                walk(inner)
        elif isinstance(value, list):
            for inner in value:
                walk(inner)

    walk(payload)

    parsed = urllib.parse.urlparse(current_url)
    if not parsed.scheme or not parsed.netloc:
        return sorted(direct_urls)
    base = f"{parsed.scheme}://{parsed.netloc}"
    for result_id in ids:
        direct_urls.add(urllib.parse.urljoin(base, f"/v2/public/replays/{token}/files/{result_id}/download"))
    return sorted(direct_urls)


def classify_download(result: FetchResult, local_path: Path, skipped: bool = False) -> tuple[str, str]:
    if skipped:
        return "skipped_existing", "yes"
    if result.error.startswith("truncated_at_"):
        return "truncated", "no"
    if str(result.status) == "ERROR":
        return "failed", "no"
    try:
        status_code = int(result.status)
    except Exception:
        status_code = 200 if result.data else 0
    if status_code in {401, 403}:
        return "private_or_forbidden", "no"
    if status_code == 404:
        return "missing", "no"
    if status_code == 410:
        return "expired", "no"
    if status_code >= 400:
        return "failed_http", "no"
    if result.data and local_path:
        return "success", "yes"
    return "failed_empty", "no"


def read_existing_manifest(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines:
        return {}
    columns = lines[0].split("\t")
    rows: dict[str, dict[str, str]] = {}
    for line in lines[1:]:
        values = line.split("\t")
        row = {col: values[index] if index < len(values) else "" for index, col in enumerate(columns)}
        url = row.get("url", "")
        local_path = row.get("local_path", "")
        status = row.get("download_status", "")
        complete = row.get("complete", "")
        reusable_status = status in {"success", "skipped_existing"} or (not status and not row.get("error", ""))
        if url and local_path and Path(local_path).exists() and reusable_status and complete != "no":
            rows[url] = row
    return rows


def write_manifest(rows: list[dict[str, str]], path: Path) -> None:
    columns = [
        "url",
        "final_url",
        "status",
        "download_status",
        "complete",
        "content_type",
        "bytes",
        "local_path",
        "error",
        "note",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(columns) + "\n")
        for row in rows:
            handle.write("\t".join(str(row.get(col, "")).replace("\t", " ") for col in columns) + "\n")


def download_status_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        status = row.get("download_status", "unknown") or "unknown"
        counts[status] = counts.get(status, 0) + 1
    return counts


def write_download_summary(rows: list[dict[str, str]], path: Path, max_files_reached: bool, byte_limit_enabled: bool) -> None:
    counts = download_status_counts(rows)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("metric\tvalue\n")
        handle.write(f"total_manifest_rows\t{len(rows)}\n")
        for status in sorted(counts):
            handle.write(f"download_status:{status}\t{counts[status]}\n")
        handle.write(f"max_files_reached\t{str(max_files_reached).lower()}\n")
        handle.write(f"byte_limit_enabled\t{str(byte_limit_enabled).lower()}\n")


def write_cross_trace_inventory(rows: list[dict[str, str]], out_base: Path) -> None:
    columns = [
        "source_url",
        "token",
        "download_date",
        "trace_folder",
        "fetched_urls",
        "discovered_urls",
        "apparent_project_step",
        "relationship_to_other_links",
        "notes",
    ]
    inventory_path = out_base / "cross_trace_inventory.tsv"
    with inventory_path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(columns) + "\n")
        for row in rows:
            handle.write("\t".join(str(row.get(col, "")).replace("\t", " ") for col in columns) + "\n")

    chronology_path = out_base / "cross_trace_chronology.md"
    lines = [
        "# Cross-Trace Chronology",
        "",
        "Use this file to audit how multiple Biomni share links from the same project relate to each other.",
        "Fill in the project step, date order, correction relationship, canonical outputs, and deprecated outputs after inspecting the downloaded traces.",
        "",
        "| Order | Token | Trace folder | Apparent project step | Relationship / correction note |",
        "| --- | --- | --- | --- | --- |",
    ]
    for index, row in enumerate(rows, start=1):
        lines.append(
            f"| {index} | {row.get('token', '')} | {row.get('trace_folder', '')} | TODO | TODO |"
        )
    lines.extend(
        [
            "",
            "## Final Corrected Route Decision",
            "",
            "- TODO: Explain which trace(s) define the final corrected path and why.",
            "- TODO: Explain which trace outputs are deprecated, audit-only, or historical warning material.",
            "- TODO: Explain which local scripts/outputs must connect to the next reproduction step.",
        ]
    )
    chronology_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download reachable content behind one or more Biomni share URLs.")
    parser.add_argument("urls", nargs="+", help="One or more Biomni share URLs from the same project or related agent windows")
    parser.add_argument("--out", default="biomni_traces", help="Output root directory")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum URLs to fetch; lower values are partial discovery, not complete evidence")
    parser.add_argument("--max-bytes", type=int, default=0, help="Maximum bytes per response; 0 means no truncation")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument("--no-resume", action="store_true", help="Do not reuse complete files already listed in an existing manifest")
    parser.add_argument("--no-common-probes", action="store_true", help="Do not try common public replay routes")
    return parser.parse_args()


def download_one(args: argparse.Namespace, source_url: str, date: str) -> dict[str, str]:
    token = extract_token(source_url)
    out_root = Path(args.out) / f"{token}_{date}"
    raw_dir = out_root / "raw_responses"
    files_dir = out_root / "files"
    out_root.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    files_dir.mkdir(parents=True, exist_ok=True)

    (out_root / "SOURCE_URL.txt").write_text(source_url + "\n", encoding="utf-8")

    queue: list[str] = [source_url]
    seen: set[str] = set()
    manifest: list[dict[str, str]] = []
    discovered: set[str] = set()
    existing_manifest = {} if args.no_resume else read_existing_manifest(out_root / "download_manifest.tsv")

    while queue and len(seen) < args.max_files:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)

        if url in existing_manifest:
            row = dict(existing_manifest[url])
            row["download_status"] = "skipped_existing"
            row["complete"] = "yes"
            row["note"] = "reused_complete_file_from_existing_manifest"
            manifest.append(row)
            local_path = Path(row.get("local_path", ""))
            if local_path.exists():
                data = local_path.read_bytes()
                if is_text(row.get("content_type", ""), data):
                    text = data.decode("utf-8", errors="replace")
                    link_candidates = html_links(data) + regex_links(text) + result_download_urls(text, row.get("final_url", url) or url, token)
                    resolved = resolve_links(row.get("final_url", url) or url, link_candidates)
                    for new_url in resolved:
                        discovered.add(new_url)
                        if new_url not in seen and len(queue) + len(seen) < args.max_files:
                            queue.append(new_url)
            if url == source_url and not args.no_common_probes:
                for probe in common_probe_urls(source_url, row.get("final_url", url) or url, token):
                    if probe not in seen and probe not in queue:
                        queue.append(probe)
            continue

        result = fetch(url, args.timeout, args.max_bytes)
        subdir = "raw_responses" if url == source_url or is_text(result.content_type, result.data) else "files"
        local_path = save_response(result, out_root, subdir) if result.data else Path("")
        download_status, complete = classify_download(result, local_path)
        manifest.append(
            {
                "url": result.url,
                "final_url": result.final_url,
                "status": str(result.status),
                "download_status": download_status,
                "complete": complete,
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
        link_candidates = html_links(result.data) + regex_links(text) + result_download_urls(text, result.final_url or url, token)
        resolved = resolve_links(result.final_url or url, link_candidates)
        for new_url in resolved:
            discovered.add(new_url)
            if new_url not in seen and len(queue) + len(seen) < args.max_files:
                queue.append(new_url)

        if url == source_url and not args.no_common_probes:
            for probe in common_probe_urls(source_url, result.final_url, token):
                if probe not in seen and probe not in queue:
                    queue.append(probe)

        time.sleep(0.05)

    write_manifest(manifest, out_root / "download_manifest.tsv")
    max_files_reached = len(seen) >= args.max_files
    byte_limit_enabled = bool(args.max_bytes and args.max_bytes > 0)
    write_download_summary(manifest, out_root / "download_summary.tsv", max_files_reached, byte_limit_enabled)
    (out_root / "discovered_urls.txt").write_text("\n".join(sorted(discovered)) + "\n", encoding="utf-8")
    print(f"Saved Biomni share discovery to: {out_root}")
    print(f"Fetched {len(manifest)} URL(s); discovered {len(discovered)} candidate URL(s).")
    print("Download status counts: " + ", ".join(f"{key}={value}" for key, value in sorted(download_status_counts(manifest).items())))
    if max_files_reached:
        print("WARNING: max-files limit was reached; treat this as partial discovery until rerun with a higher limit.")
    if byte_limit_enabled:
        print("WARNING: max-bytes limit is enabled; truncated rows are not complete evidence.")
    notes = []
    if max_files_reached:
        notes.append("partial_due_to_max_files")
    if byte_limit_enabled:
        notes.append("byte_limit_enabled")
    return {
        "source_url": source_url,
        "token": token,
        "download_date": date,
        "trace_folder": str(out_root),
        "fetched_urls": str(len(manifest)),
        "discovered_urls": str(len(discovered)),
        "apparent_project_step": "",
        "relationship_to_other_links": "",
        "notes": ";".join(notes),
    }


def main() -> int:
    args = parse_args()
    date = _dt.datetime.now().strftime("%Y%m%d")
    out_base = Path(args.out)
    out_base.mkdir(parents=True, exist_ok=True)

    inventory_rows = []
    for source_url in args.urls:
        inventory_rows.append(download_one(args, source_url, date))

    if len(inventory_rows) > 1:
        write_cross_trace_inventory(inventory_rows, out_base)
        print(f"Saved cross-trace inventory to: {out_base / 'cross_trace_inventory.tsv'}")
        print(f"Saved cross-trace chronology template to: {out_base / 'cross_trace_chronology.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
