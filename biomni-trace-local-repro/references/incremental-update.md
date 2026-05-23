# Incremental Update Rules

Use this reference when a project already has local teaching scripts and the user asks to continue from newer Biomni trace evidence.

## Default Behavior

Treat existing local teaching scripts as the active reproduction chain unless the user explicitly asks for a rewrite.

Before writing a new script:

- inspect the formal local project directory;
- identify the teaching-script directory, often named `详解/`;
- list existing teaching scripts in their intended order;
- inspect earlier scripts enough to understand `PROJECT_DIR`, input files, output files, object names, stop-message style, and terminology;
- inspect existing project outputs enough to verify which files are produced by earlier scripts;
- inspect downloaded Biomni trace folders and cross-trace notes enough to locate the new continuation point.

## Directory Boundary

The `详解/` directory is learner-facing. It should contain final teaching scripts only.

Do not write these into `详解/`:

- Biomni trace downloads;
- raw viewer/API responses;
- download manifests;
- cross-trace inventory or chronology files;
- incremental interface maps;
- audit notes;
- environment guides;
- temporary files;
- extracted notebooks or logs.

Put evidence and metadata under `biomni_traces/` or another project-level evidence/metadata directory.

## Required Metadata Files

Create or update these files outside `详解/` when doing incremental work:

```text
local_repro_script_inventory.tsv
local_repro_interface_map.md
incremental_update_decision_note.md
```

`local_repro_script_inventory.tsv` should record:

- script filename;
- script order;
- biological or computational purpose;
- key inputs;
- key outputs;
- whether the script is current, deprecated, or historical;
- notes about required upstream scripts.

`local_repro_interface_map.md` should explain:

- the script chain, for example `F0 -> F1 -> F2A -> F2B -> F2C -> F2step4 -> F2step5`;
- which output files from each script are consumed downstream;
- where the next script should start;
- which output filenames and table schemas must remain stable.

`incremental_update_decision_note.md` should explain:

- which newly downloaded Biomni trace(s) are being added;
- how they relate to older trace(s);
- what the corrected route is;
- which Biomni outputs are canonical;
- which outputs are deprecated, audit-only, or historical warning material;
- why the next local script starts at the chosen point.

## Writing the Next Script

The new script should:

- continue the existing naming and project path conventions;
- read only local-uploaded originals or earlier local-script outputs;
- stop with clear learner-facing messages when required upstream files are missing;
- preserve downstream-facing filenames and schemas unless a correction requires a change;
- document historical Biomni mistakes only in comments;
- avoid rewriting earlier scripts unless the new trace proves a conflict with the final corrected path.

If a conflict exists between existing local scripts and newer corrected trace evidence, make the smallest correction that restores the final path and document why.
