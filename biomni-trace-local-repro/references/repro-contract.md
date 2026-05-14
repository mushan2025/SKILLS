# Biomni Trace Local Reproduction Contract

Use this reference when converting a Biomni trace into local reproduction code.

## Download Contract

- A Biomni share URL is a source artifact, not a script input path.
- Download all reachable trace materials before analysis:
  - execution trace notes or JSON;
  - code snippets;
  - file manifests and download plans;
  - result metadata;
  - tables, figures, logs, and notes.
- Store downloads under a project-local trace folder, preferably:
  - `biomni_traces/<share_token>_<YYYYMMDD>/`
- Preserve older downloads and prefer the newest download unless the user says otherwise.
- Record source URL, token, download date, and file inventory.

## Runtime Path Contract

Final local scripts must use the local project directory, for example:

```r
PROJECT_DIR <- "D:/STAD_bioinformation/STAD"
```

Do not use these as default runtime paths:

- `share_*`
- `.tmp_*`
- `/mnt/...`
- `/workspace/...`
- Biomni server paths
- the downloaded trace folder

Trace files may be mentioned in comments as evidence used while writing the script, but not as the path the reader must run.

## Corrected-Only Contract

Executable code must implement only the final corrected path.

Historical mistakes must be comments only:

```r
# Historical mistake: an earlier trace used median_raw_pt / max_raw_pt as pct_rank.
# Correct path: pct_rank is the fraction of finite-pseudotime cells below the candidate median.
```

Never add executable branches such as:

- `RUN_DEPRECATED_*`
- `USE_OLD_FORMULA`
- `READ_DEPRECATED_RESULTS`
- fallback reads of `*_DEPRECATED_DO_NOT_USE*`
- code blocks that reproduce a known wrong formula

Do not write output tables whose purpose is to reproduce or preserve the wrong path.

## Prerequisite Contract

If a script requires earlier outputs, check them before analysis and stop clearly when missing.

Good pattern:

```r
if (!file.exists(F2_CNV_SCORE_FILE)) {
  stop(
    "找不到 F2A 生成的 CNV 分数表：\n",
    F2_CNV_SCORE_FILE, "\n",
    "请先运行 F2A_CNV_validation_详解.R。"
  )
}
```

Avoid silent downgrade:

```r
# Bad: continues without a required evidence layer.
if (!file.exists(F2_CNV_SCORE_FILE)) {
  cat("CNV missing; continuing.\n")
}
```

## Teaching Contract

The user-facing scripts are not terse pipelines. They are teaching scripts for readers with no coding or bioinformatics background.

Each major code block should explain:

- what question the block answers;
- why the block is needed;
- what input it reads;
- what object it changes;
- what output it writes;
- what normal output looks like;
- what common abnormal output means.

Explain first appearances of core syntax:

- `<-`
- `if`
- `for`
- `file.exists()`
- `stop()`
- `fread()` / `fwrite()`
- `merge()`
- `%in%`
- data.table grouping

## Static Validation

Run static checks before handoff:

- no trace runtime paths in scripts;
- deprecated/error-path terms only in comments;
- required inputs exist in prior-script outputs;
- key missing prerequisites use `stop()`;
- parse/syntax check if the language runtime is available.

