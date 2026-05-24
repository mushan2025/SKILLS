---
name: research-group-report-writer
description: Write or update research-group-style progress reports, project summaries, thesis-group briefings, technical handoff reports, or Chinese “课题组汇报” documents from analysis traces, notes, tables, scripts, and result files. Use when the user wants a report that explains research chronology, decisions, methods, definitions, evidence strength, caveats, and next-step boundaries for readers who may have little bioinformatics or coding background, especially when converting raw execution records into a human-facing scientific narrative without platform/run-log narration.
---

# Research Group Report Writer

## Core Goal

Create a report that reads like a research-group briefing, not a tool log. The report should let a non-specialist reader understand what the project has done, why decisions were made, what methods and parameters mean, what evidence supports each conclusion, and what must not be over-interpreted.

## Source Handling

Use original source artifacts as the evidence base:

- Raw traces, notebooks, execution exports, notes, tables, result summaries, figures, scripts, and prior reports.
- Treat prior reports as integration references, not replacements for source artifacts.
- Prefer exact values from tables and notes over memory.
- Keep platform mechanics out of the report body unless the user explicitly asks for an operational audit.

Separate four kinds of content:

- **Fact**: measured numbers, file-derived outputs, accepted definitions.
- **Decision**: chosen thresholds, candidate sets, analysis scope.
- **Interpretation**: what the findings suggest biologically.
- **Boundary**: what the evidence cannot yet prove.

## Report Style

Write in a “课题组汇报 + 技术交接” voice:

- Use chronology as the backbone: data preparation → atlas → candidate definition → evidence layers → correction/audit → current conclusion → next boundary.
- Explain research decisions as choices made under constraints, not as a list of commands.
- Avoid saying “the platform ran”, “the agent did”, “trace shows”, or similar run-log wording.
- Use tables for definitions, thresholds, candidate sets, and status summaries.
- Use short paragraphs around tables to explain why each table matters.
- Define jargon when it appears, and repeat short reminders when a term reappears several sections later.

For zero-bioinformatics readers, explain algorithm concepts at first use and again briefly when reused:

- What the method is trying to infer.
- What input it uses.
- What the output means.
- What can bias or confound it.
- What conclusion it cannot prove.

## Required Structure

Use this structure unless the user provides a different outline:

1. Project background and overall roadmap.
2. Current research question and stage status.
3. Data sources and key input decisions.
4. Stage-by-stage chronology.
5. Candidate definition and decision chain.
6. Methods and parameters with plain-language explanations.
7. Results and evidence strength.
8. Corrections, failed paths, downgraded paths, and why.
9. Current conclusions.
10. Interpretation boundaries.
11. Next-step recommendations and stop conditions.

If the project has a major “before next stage” framework lock, add a dedicated subsection such as:

```text
Monocle 前候选框架锁定
进入下游分析前的候选名单冻结
F3 前证据框架锁定
```

This makes the real research progression visible.

## Decision and Definition Writing

Never leave a classification as a black box. For each key category, state the rule and the rationale.

Bad:

```text
Likely malignant means weaker but acceptable CNV support.
```

Good:

```text
Likely malignant means the cell has at least inferCNV mean+1SD support and no explicit CopyKAT diploid counter-evidence, or has inferCNV mean+2SD support while CopyKAT is not.defined. If CopyKAT is explicitly diploid, weak inferCNV-only support is not accepted.
```

When writing thresholds or metrics, include:

- The exact formula or rule.
- The reference population.
- The interpretation of high/low values.
- Why this threshold was chosen.
- Whether it is primary, sensitivity, or descriptive only.

## Explain Metrics Repeatedly Enough

Readers forget definitions. Add brief reminders when important metrics reappear after a gap.

Examples:

- `z-score`: standardized score; 0 is average, positive is higher than average, negative is lower.
- `top 20%`: cells in the highest 20% of that score within the defined cell population.
- `mean_stemness_z`: average of selected standardized stemness scores; a ranking aid, not a direct experimental measurement.
- `pct_rank`: percentile position within the same pseudotime root strategy; not raw pseudotime and not comparable across roots.
- `CV`: coefficient of variation; lower means bootstrap results are more stable.
- `finite pseudotime fraction`: fraction of cells connected to the learned trajectory and assigned finite pseudotime.

## Algorithm Explanation Pattern

For each algorithm, use this mini-pattern:

```text
Method:
What it does:
Input:
Output:
How this project used it:
Main caveat:
```

For common single-cell methods:

- **Seurat/Harmony**: explain normalization, dimensionality reduction, clustering, and batch correction.
- **inferCNV**: explain chromosome-position-based expression shifts and reference cells.
- **CopyKAT**: explain aneuploid/diploid prediction from expression patterns.
- **CytoTRACE2**: explain developmental potency inference and QC/ribosomal confounding.
- **Monocle3**: explain principal graph, root, pseudotime, root sensitivity, and why pseudotime is not lineage proof.
- **Gene-set scoring**: explain that scores summarize a group of genes, not a single marker.

## Candidate Coverage

When a project has many candidates, distinguish:

- **Uniform table-level analysis**: metrics generated for all candidates.
- **Focused biological interpretation**: deeper discussion only for candidates that are relevant, stable, risky, or prioritized.

Do not imply every candidate received the same depth of validation if only summary fields were generated for all. Say explicitly which analyses were global and which were focused.

## Sensitivity and Root Logic

When a result depends on parameter choices or root choices, explain:

- Which setting is the primary reference.
- Which settings are sensitivity checks.
- Whether the final conclusion uses one setting or aggregated evidence.
- What would cause the result to be downgraded.

For Monocle-style analysis:

- Define root as the chosen starting region for reading pseudotime.
- Explain that changing root changes pseudotime direction and scale.
- Avoid saying a trajectory proves causal differentiation.
- Prefer statements like “supports a trajectory-position hypothesis” over “proves lineage”.

## Boundary Language

Use conservative language for unvalidated biology:

- “candidate”, “supports”, “consistent with”, “suggests”, “requires validation”.
- Avoid “confirmed”, “proves”, “definitive”, “true CSC subtype”, unless functional validation exists.

Explicitly flag:

- patient skew,
- small cell count,
- tool discordance,
- ribosomal or QC confounding,
- threshold sensitivity,
- root sensitivity,
- scope not yet started.

## Final Quality Checklist

Before finishing, check that the report:

- Preserves chronological research progression.
- Explains major concepts and parameters near where they are used.
- States candidate definitions and decision rules explicitly.
- Separates primary analysis, sensitivity analysis, and descriptive overlays.
- Does not turn platform traces into run-log narration.
- Does not overstate candidates as validated biology.
- Includes key numbers and enough reproducibility clues.
- Marks F3/F4/etc. as not completed unless actually done.

