# STAD F2 Case Reference

This reference captures the current STAD F2 local reproduction pattern. Use it as an example, not as a universal rule for every Biomni project.

## Local Script Chain

The current F2 chain is:

```text
F2A_CNV_validation_详解.R
  -> F2B_tumor_epithelial_recluster_详解.R
  -> F2C_function_ribo_EP11_详解.R
  -> F2step4_monocle3_trajectory_详解.R
```

Older `F2_step1_2_详解.R` is a historical reference, not the current entrypoint.

## Candidate Framework

The final corrected structural candidate universe has 120 rows:

- 16 `EP_subtype`
- 10 `RC_cluster`
- 90 `EPxRC_intersection`
- 4 `CNV_sensitivity_cluster`

The four CNV sensitivity candidates are:

```text
A_primary_240__C0
A_primary_240__C1
A_primary_240__C2
A_primary_240__C3
```

`consensus_stemness_high` is not a candidate row. It is a functional evidence layer.

## EP11 Trajectory Interpretation

The corrected interpretation is:

- EP11 is a strong candidate state supported by multiple evidence layers.
- Corrected Monocle3 trajectory support places EP11 mainly in an intermediate position.
- EP11 must not be described as root-proximal based on the old pct_rank mistake.
- CNV discordance, patient skew, reverse-root sensitivity, and internal heterogeneity remain caution points.

The old pct_rank mistake is comment-only teaching material.

## Local Runtime Rule

Final scripts use:

```text
D:/STAD_bioinformation/STAD
```

Downloaded trace folders are evidence for writing, not runtime dependencies.

