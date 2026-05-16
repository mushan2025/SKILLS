# Biomni Share Link Discovery

Use this reference when the user provides a Biomni share URL and expects Codex to download the execution trace, code, output files, and notes.

## Goal

A Biomni share link is often a viewer page, not a direct file URL. Codex must discover the real content behind it before analyzing the project.

The output of discovery should be:

- source URL;
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
