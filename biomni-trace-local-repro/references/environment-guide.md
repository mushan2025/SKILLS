# Beginner Environment Word Guide

Use this reference when the skill needs to create or update a project-level Word `.docx` guide that teaches zero-background learners how to prepare the software environment before running local reproduction scripts.

## Purpose

The Word guide is a prerequisite for beginner-facing reproduction projects. It should help a learner install the right tools, open the project correctly, run scripts safely, and restore their working state later.

The guide must be grounded in the downloaded Biomni trace and the local repo. Do not assume the project is R-based. A project may use R, Python, notebooks, shell commands, external bioinformatics tools, or a mixed stack.

## Required Content

The guide should be written in Chinese and should explain:

- which language/runtime the project uses and why;
- which software to download and install;
- exact software versions, package versions, seeds, and system assumptions from Biomni when available;
- how to open the project in the appropriate tool;
- how local folders such as `data/`, `results/`, `figures/`, `logs/`, notebooks, scripts, and teaching-script folders are used;
- why scripts must use local project paths rather than Biomni runtime paths;
- how to install or check required packages without silently changing analysis versions;
- how to run scripts or notebooks section by section;
- why expensive workflows should not be run with one-click Run All, Run All Cells, or full pipeline execution unless explicitly intended;
- what files should appear after each major script;
- how to save and restore the working state in a language-appropriate way;
- common beginner errors and how to diagnose them.

## Runtime-Specific Examples

For R projects, cover the relevant items:

- R version;
- RStudio or Positron;
- Rtools on Windows when source package compilation is needed;
- Bioconductor version when relevant;
- `renv`, `install.packages()`, or project-specific package restoration;
- `.Rproj`;
- `.RData`;
- `.Rhistory`;
- `readRDS()`, `saveRDS()`, `fread()`, and other reproducible reload/save functions used by the scripts.

For Python projects, cover the relevant items:

- Python version;
- Conda, mamba, or `venv`;
- Jupyter, VS Code, or another notebook/editor environment;
- `environment.yml`;
- `requirements.txt`;
- `pyproject.toml`;
- `.ipynb` notebooks;
- serialized objects such as `.pkl` or `.joblib` only when the trace or local scripts truly use them;
- `pandas.read_csv()`, `pickle.load()`, `joblib.load()`, or other reproducible reload/save functions used by the scripts.

For command-line or external-tool projects, cover the relevant items:

- shell type and operating system assumptions;
- exact executable names and versions;
- PATH configuration;
- input/output folders;
- command history or shell scripts that reproduce the run;
- how to check that each external tool is callable before running the analysis.

## Save/Restore Guidance

Teach learners that interactive session state is convenient but not the main reproducibility guarantee.

The guide should distinguish:

- project files that define the workflow, such as scripts, notebooks, project files, and environment files;
- analysis output files that later scripts should reload, such as `.rds`, `.tsv`, `.csv`, `.h5ad`, `.pkl`, or `.joblib` files;
- interactive history files, such as `.Rhistory`, notebook checkpoints, shell history, or editor workspace state;
- full environment specifications, such as `renv.lock`, `environment.yml`, `requirements.txt`, or container/tool-version records.

Prefer reproducible reloads from saved output files over relying only on whatever happens to be visible in an interactive Environment panel.

## Common Beginner Errors

Explain the likely symptoms and fixes for:

- wrong working directory;
- missing package or wrong package version;
- missing external executable;
- missing previous-step output;
- using Biomni trace files as runtime inputs by mistake;
- non-ASCII path or space-in-path issues when a tool cannot handle them;
- running an expensive full workflow accidentally;
- mixing outputs from different Biomni share links or different project attempts.
