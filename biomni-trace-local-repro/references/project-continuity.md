# Project Continuity Rules

Use this reference when the same project uses this skill more than once.

## Before Writing a New Script

Read existing local scripts in order. Identify:

- project directory variable and path style;
- script sequence;
- inputs and outputs;
- object names and table names;
- package-loading style;
- stop/error message style;
- how much background has already been explained;
- which concepts are still new to the reader.

Do not ask the user where these files are if they can be discovered from the repository.

## Interface Map

Create a mental or written map like:

```text
F1 output:
  data/processed/F1_objects/F1_processed_seurat.rds
  results/F1_scRNA/tables/F1_cell_annotation_table.tsv

F2A output:
  results/F2_CNV/tables/F2_CNV_scores.tsv
  results/F2_CNV/tables/F2_malignancy_classification.tsv

F2B input:
  F1 object + F1 annotation + F2A CNV tables
```

The new script's first required input should be a previous script's documented output.

## Avoid Content Gaps

Avoid two opposite failure modes:

- repeating earlier modules so much that the new script loses focus;
- assuming concepts or files that earlier scripts never introduced.

When a concept was introduced earlier, briefly remind the reader and point to the prior script. When a concept is new, explain it fully.

## Conflict Handling

If a new Biomni trace contradicts an older local script:

1. Confirm the conflict from trace evidence and local script text.
2. Identify the blast radius: comments only, code path, output interface, candidate definition, or downstream scripts.
3. Ask the user before changing high-impact behavior.
4. If approved, update the minimal set of scripts needed for continuity.

## Continuity Handoff

At the end of each local script, include a short "next step" section:

- what files should now exist;
- what the reader should inspect;
- which script to run next;
- what must not be concluded yet.

