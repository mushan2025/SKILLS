# Biomni Share Link Discovery

Use this reference when the user provides a Biomni share URL and expects Codex to download the execution trace, code, output files, and notes.

## Goal

A Biomni share link is often a viewer page, not a direct file URL. Codex must discover the real content behind it before analyzing the project.

If Python and network access are available, start with the bundled helper:

```powershell
python scripts/download_biomni_share.py "<BIOMNI_SHARE_URL>" --out biomni_traces
```

The helper is deliberately conservative: it saves raw responses, follows discovered links, tries common public replay/manifest routes, writes `download_manifest.tsv`, and records failures instead of hiding them. After it runs, Codex must still audit the downloaded files and decide which outputs are corrected evidence.

## Known Public Replay Entry Points

For a user-facing link such as:

```text
https://biomni.phylo.bio/replay/share_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

the `biomni.phylo.bio` page is the viewer, not the main data endpoint. Extract the `share_...` token and look for the API base used by the frontend JavaScript/config. In recent traces this API base resolved to:

```text
https://api.phylo.bio
```

The route shapes observed from the Biomni frontend were:

```text
GET <API_BASE>/v2/public/replays/<share_token>
GET <API_BASE>/v2/public/replays/<share_token>/results
GET <API_BASE>/v2/public/replays/<share_token>/files/<result_id>/download
GET <API_BASE>/v2/public/replays/<share_token>/files/<result_id>/download?inline=true
```

Use them as the first concrete download entry points:

- `/v2/public/replays/<share_token>` returns the shared replay/session/context payload when public access is available.
- `/v2/public/replays/<share_token>/results` returns result-file metadata, including result identifiers used for file downloads.
- `/v2/public/replays/<share_token>/files/<result_id>/download` returns or redirects to file download content, often through a signed URL.
- `?inline=true` is useful for previewable text/table/figure content when the server supports inline rendering.

Save raw JSON bodies and headers separately, for example:

```text
raw_responses/api_phylo_v2_public_replay.json
raw_responses/api_phylo_v2_public_replay.headers.txt
raw_responses/api_phylo_v2_public_replay_results.json
raw_responses/api_phylo_v2_public_replay_results.headers.txt
```

These route shapes are known working entry points, but do not hard-code the API base forever. If the current viewer page or JavaScript chunks expose a different API base, use the current value, save the evidence, and record it in the manifest.

The output of discovery should be:

- source URL;
- API base used for replay/results/file downloads;
- share token or stable identifier;
- downloaded HTML/API responses;
- manifest or file index if present;
- list of file URLs or storage keys;
- local download folder;
- notes about missing, private, expired, or blocked files.

## Step 1: Normalize the URL

From the user-provided URL:

- keep the full original URL;
- extract the hostname;
- extract likely share identifiers from path segments, query parameters, or fragments;
- preserve query parameters because some shares encode access tokens there.

Common identifiers may look like:

```text
share_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
replay id
trace id
run id
public replay token
```

Do not assume one fixed URL shape. Inspect the actual link.

## Step 2: Fetch the Viewer Page

Download the share page HTML first.

Save:

- response headers;
- final redirected URL;
- HTML body;
- cookies only if needed for the current session and allowed by the environment.

Search the HTML for:

- `__NEXT_DATA__`
- `script src=`
- `/_next/static/`
- `buildId`
- `public`
- `replay`
- `trace`
- `results`
- `manifest`
- `download`
- `s3`
- `.json`
- `.tsv`
- `.csv`
- `.txt`
- `.png`
- `.pdf`

If the page is a JavaScript app, fetch referenced JavaScript chunks and search them too.

## Step 3: Try Discovered API and Manifest Routes

Use URLs discovered from the page/chunks first. If the page hints at API paths, test them with `GET` or `HEAD`.

Useful route patterns to look for or test when supported by the page:

```text
/v2/public/replays/<token>
/v2/public/replays/<token>/results
/v2/public/replays/<token>/files/<result_id>/download
/public/replays/<token>
/api/...<token>...
/download_plan.json
/s3_download_plan.json
/results.json
/files/...
/execution_trace/...
```

Do not treat these patterns as guaranteed. They are probes guided by the page and previous Biomni traces.

For each response:

- save the body if it is text/JSON;
- save headers;
- record status code;
- follow redirects;
- avoid repeatedly hammering failing endpoints.

## Step 4: Build a File Inventory

From manifests, JSON, HTML, and code chunks, collect file candidates:

- absolute URLs;
- relative URLs;
- S3 or object-storage links;
- file paths under `files/`, `tables/`, `figures/`, `execution_trace/`, `logs/`;
- filenames mentioned in notes or result metadata.

Resolve relative links against the final viewer URL or API base that produced them.

Classify files before analysis:

- execution trace / replay metadata;
- code snippets or notebooks;
- result tables;
- figures;
- notes and limitations;
- manifests and download plans;
- deprecated or superseded outputs;
- corrected canonical outputs.

## Step 5: Download Reachable Files

Download all reachable files into the local trace folder.

Preserve enough structure to make provenance clear, for example:

```text
biomni_traces/<share_token>_<YYYYMMDD>/
  raw_responses/
  files/
  derived/
  download_manifest.tsv
  SOURCE_URL.txt
```

Create a local manifest with at least:

- original URL;
- local path;
- HTTP status;
- content type;
- size;
- timestamp;
- note or error message.

If a file is private, expired, too large, or blocked, record that fact instead of silently ignoring it.

## Step 6: Decide What Counts as Evidence

Prefer evidence in this order:

1. explicit corrected notes or final interpretation notes;
2. corrected output tables;
3. execution trace code and logs;
4. manifests and result metadata;
5. figures;
6. deprecated files only as historical warning material.

Never use deprecated files as the source of a default local reproduction path.

## When to Ask the User

Ask the user when:

- the share link requires login or interactive authentication;
- multiple traces or run ids are present and none is clearly latest;
- downloading will be very large or slow;
- a key manifest is missing and there are multiple plausible reconstructions;
- using an alternate mirror or manually provided file bundle would affect the analysis.

Do not ask the user to identify files that can be discovered by inspecting the page, manifests, or local repo.
