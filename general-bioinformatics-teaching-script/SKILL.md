---
name: general-bioinformatics-teaching-script
description: Rewrite or author bioinformatics analysis scripts in a beginner-friendly, teaching-oriented style, with clear explanations of inputs, outputs, methods, biological meaning, and reproducibility expectations.
version: 1.0.0
---

# Skill: 生信项目通用“小白教学型分析脚本”写作规范

## 1. Skill 目标

这个 skill 用于把任何生物信息学项目中的分析脚本，改写或新写成“小白教学型脚本”。

目标不是只让代码能跑，而是让没有生信基础的学习者看完后能理解：

1. 现在在做什么分析；
2. 为什么要做这个分析；
3. 输入数据是什么；
4. 输出结果是什么；
5. 用了什么统计方法或算法；
6. 这些结果有什么生物学意义；
7. 怎样判断结果是否合理；
8. 如果以后遇到类似任务，自己应该如何写代码。

最终脚本应同时满足三个要求：

- **能运行**：代码路径清楚，依赖明确，输出可复现。
- **能学习**：注释解释“是什么、为什么、怎么做、怎么看”。
- **能交接**：别人接手项目时，能理解分析逻辑和结果位置。

---

## 2. 适用范围

这个 skill 适用于几乎所有常见生物信息学项目，包括但不限于：

### 2.1 数据类型

- bulk RNA-seq
- single-cell RNA-seq
- single-nucleus RNA-seq
- spatial transcriptomics
- ATAC-seq
- ChIP-seq
- DNA methylation
- WGS / WES / mutation data
- CNV / SV 分析
- proteomics / phosphoproteomics
- metabolomics
- microbiome
- multi-omics integration
- clinical cohort analysis
- public database mining
- machine learning / prognostic model
- biomarker discovery
- drug sensitivity prediction
- pathway / network / enrichment analysis

### 2.2 语言和工具

优先适用于 R 和 Python，也可用于 Shell、Snakemake、Nextflow、Jupyter Notebook、R Markdown、Quarto 等。

常见工具包括但不限于：

- R: Seurat, SingleCellExperiment, DESeq2, edgeR, limma, clusterProfiler, GSVA, survival, WGCNA, CellChat, inferCNV, Monocle, Slingshot
- Python: scanpy, anndata, pandas, numpy, scipy, sklearn, matplotlib, seaborn, squidpy
- Command line: fastqc, multiqc, STAR, HISAT2, Salmon, kallisto, samtools, bedtools, bcftools, GATK
- Workflow: Snakemake, Nextflow, Docker, Conda, renv, mamba

---

## 3. 总体写作原则

### 3.1 每个脚本都要回答四个问题

每个脚本开头必须说明：

```text
这个脚本要解决什么问题？
为什么这个问题值得分析？
输入数据是什么？
运行后会得到什么结果？
```

不要只写：

```text
Run differential expression analysis.
```

应该写成：

```text
本脚本用于比较肿瘤组和正常组的基因表达差异。
差异表达分析可以帮助我们找到在肿瘤中异常上调或下调的基因。
这些基因可能参与肿瘤发生、免疫逃逸、代谢重编程或耐药。
输入是 count 表达矩阵和样本分组信息。
输出包括差异基因表、火山图、热图和可用于后续富集分析的基因列表。
```

---

### 3.2 注释必须解释“为什么”，不能只翻译代码

低质量注释：

```r
# 读取文件
expr <- read.csv("expr.csv")
```

高质量注释：

```r
# 读取表达矩阵。
# 表达矩阵是生信分析最核心的数据之一。
# 通常行是基因，列是样本或细胞。
# 后续差异分析、聚类、通路分析都基于这个矩阵。
expr <- read.csv("expr.csv", row.names = 1)
```

每个关键步骤应尽量解释：

- 这一步在做什么；
- 为什么需要这一步；
- 输入是什么；
- 输出是什么；
- 结果应该怎么看；
- 如果结果异常，可能说明什么。

---

### 3.3 优先使用清晰代码，不追求炫技

面向小白的教学脚本应避免过度复杂写法。

不推荐：

```r
res <- lapply(split(meta, meta$group), \(x) foo(x)) |> bind_rows()
```

推荐：

```r
# 先按照 group 把样本信息分组。
meta_split <- split(meta, meta$group)

# 对每个分组分别运行分析。
# lapply() 的意思是：对列表中的每一个元素执行同一个操作。
result_list <- lapply(meta_split, function(one_group_meta) {
  foo(one_group_meta)
})

# 把多个分组的结果合并成一个表。
res <- dplyr::bind_rows(result_list)
```

原则：

- 少用过度嵌套；
- 少用一行写完很多操作；
- 少用隐藏副作用；
- 函数、循环、管道可以用，但必须解释；
- 如果使用高级写法，先用注释解释逻辑。

---

### 3.4 每个脚本都要能分节运行

脚本应分成清晰章节，例如：

```text
第 1 节：设置路径和参数
第 2 节：读取数据
第 3 节：检查数据结构
第 4 节：数据清洗和过滤
第 5 节：标准化或归一化
第 6 节：核心分析
第 7 节：结果可视化
第 8 节：保存结果
第 9 节：保存运行环境
```

每节都要能单独理解，最好能单独运行和检查。

不要让新手一次性 Run All。脚本开头应明确提醒：

```text
不要一次性全选运行。
建议一节一节运行。
每节运行后检查输出是否合理。
如果出现红色报错，先停止，不要继续往下跑。
```

---

## 4. 推荐脚本总结构

一个通用生信教学脚本建议使用以下结构。

---

### 4.1 脚本头部

每个脚本开头必须包含：

```text
脚本名称
项目名称
分析模块
作者/维护者
日期
适用数据类型
主要软件包
输入文件
输出文件
运行方式
注意事项
```

示例：

```r
# ================================================================
# Script: F2_differential_expression_beginner.R
# Project: Cancer biomarker discovery project
# Module: F2 Differential expression analysis
# Data type: bulk RNA-seq count matrix
# Purpose:
#   Compare tumor and normal samples to identify differentially expressed genes.
#
# Main biological question:
#   Which genes are abnormally upregulated or downregulated in tumors?
#
# Input:
#   data/processed/count_matrix.rds
#   data/processed/sample_metadata.csv
#
# Output:
#   results/F2_DEG/DEG_all.csv
#   results/F2_DEG/DEG_significant.csv
#   figures/F2_DEG/volcano_plot.pdf
#   figures/F2_DEG/heatmap_top50.pdf
#
# How to run:
#   Open this script in RStudio.
#   Run section by section with Ctrl + Enter.
#   Do not click Run All at the beginning.
# ================================================================
```

---

### 4.2 参数区

把所有容易修改的参数放在脚本前面。

示例：

```r
# ================================================================
# 第 1 节：设置分析参数
# ================================================================
#
# 为什么把参数放在前面？
#   因为以后你可能需要调整阈值。
#   如果参数散落在脚本各处，很容易改漏。
#
# logFC_cutoff:
#   log2 fold change 阈值。
#   绝对值越大，表示两组差异越明显。
#
# padj_cutoff:
#   多重检验校正后的 P 值阈值。
#   常用 0.05。
# ================================================================

PROJECT_DIR <- "D:/bio_project"

logFC_cutoff <- 1

padj_cutoff <- 0.05

top_gene_number <- 50
```

所有参数必须解释生物学或统计学意义。

---

### 4.3 输入检查区

读取数据后必须检查：

- 数据维度；
- 行名列名；
- 分组数量；
- 缺失值；
- 重复样本或重复细胞；
- 数据类型是否正确；
- 表达矩阵方向是否正确。

示例：

```r
# 查看表达矩阵有多少行和列。
# 如果行是基因、列是样本，那么：
#   行数 = 基因数量
#   列数 = 样本数量
dim(expr)

# 查看前几个基因名，确认行名确实是基因。
head(rownames(expr))

# 查看前几个样本名，确认列名确实是样本。
head(colnames(expr))

# 查看每个分组有多少样本。
# 如果某一组样本太少，后续统计结果可能不稳定。
table(meta$group)
```

教学脚本必须告诉小白“看到什么结果才算正常”。

---

### 4.4 核心分析区

核心分析区必须先解释方法原理。

例如差异分析：

```text
差异表达分析的目的：
比较两组样本中每个基因的表达是否显著不同。

为什么不能只看平均值？
因为样本之间存在生物学差异和技术噪音。
统计模型可以估计这种变异，并判断差异是否超过随机波动。

为什么要做多重检验校正？
因为一次会检测上万个基因。
如果每个基因都用 P < 0.05，会产生大量假阳性。
padj 是校正后的 P 值，更适合作为显著性标准。
```

例如单细胞聚类：

```text
单细胞聚类的目的：
把表达模式相似的细胞分到同一类。

生物学意义：
同一类细胞可能代表相同细胞类型、相似细胞状态或相似肿瘤亚群。

注意：
聚类结果不是天然真理。
需要结合 marker 基因、样本来源、已知生物学知识进行解释。
```

---

### 4.5 结果解释区

每个结果输出后，必须添加解释。

不要只写：

```r
write.csv(res, "DEG.csv")
```

应该写成：

```r
# 保存完整差异分析结果。
# 这个表包含每个基因的：
#   log2FoldChange：肿瘤组相对正常组的表达变化方向和幅度
#   pvalue：原始 P 值
#   padj：多重检验校正后的 P 值
#
# 后续可以用这个表筛选候选基因，也可以做通路富集分析。
write.csv(res, "results/F2_DEG/DEG_all.csv")
```

所有图片都要解释怎么看：

```text
火山图怎么看？
横轴是 log2 fold change，表示差异方向和大小。
纵轴是 -log10(padj)，越高表示统计显著性越强。
右上角通常是肿瘤中显著上调基因。
左上角通常是肿瘤中显著下调基因。
```

---

### 4.6 保存结果区

必须保存：

- 关键 R/Python 对象；
- 结果表；
- 图片；
- 参数；
- sessionInfo 或包版本；
- 可选日志。

R 示例：

```r
saveRDS(object, "data/processed/F2_object.rds")

write.csv(result_table, "results/F2_result.csv", row.names = FALSE)

ggsave("figures/F2_plot.pdf", width = 6, height = 5)

session_info <- sessionInfo()
sink("logs/F2_sessionInfo.txt")
print(session_info)
sink()
```

Python 示例：

```python
adata.write("data/processed/F2_adata.h5ad")

result_table.to_csv("results/F2_result.csv", index=False)

plt.savefig("figures/F2_plot.pdf", bbox_inches="tight")
```

---

## 5. 每类分析都要解释的内容

---

### 5.1 质量控制 QC

必须解释：

- QC 的目的；
- 每个指标是什么意思；
- 为什么要过滤；
- 阈值是不是绝对标准；
- 过滤前后保留多少数据；
- 是否可能误删真实生物学信号。

单细胞 QC 示例：

```text
nFeature_RNA：
每个细胞检测到的基因数量。
太低可能是空液滴或低质量细胞。
太高可能是 doublet。

nCount_RNA：
每个细胞的 UMI 总数。
太低说明测序深度不足。
太高可能是 doublet 或高 RNA 含量细胞。

percent.mt：
线粒体基因比例。
太高常提示细胞受损或死亡。
```

bulk QC 示例：

```text
样本相关性：
同组样本应该整体相似。
如果某个样本和所有样本都不相似，可能是离群样本。

PCA：
用于观察样本是否按生物学分组分开。
也可以发现批次效应或异常样本。
```

---

### 5.2 标准化 / 归一化

必须解释：

- 为什么原始 counts 不能直接比较；
- 标准化解决什么问题；
- 标准化后数据能用于什么；
- 哪些分析必须用 counts，哪些可以用 normalized data。

示例：

```text
原始 counts 受测序深度影响。
一个样本 reads 多，很多基因 counts 都会偏高。
标准化的目的是减少测序深度差异，让样本之间更可比。

注意：
DESeq2 / edgeR 差异分析通常需要原始整数 counts。
不要把 log-normalized 表达矩阵直接给 DESeq2。
```

---

### 5.3 降维和聚类

必须解释：

- PCA / UMAP / t-SNE 是什么；
- 降维图不能直接等同于真实空间距离；
- 聚类分辨率影响结果；
- 聚类结果要用 marker 验证；
- 批次效应可能影响聚类。

示例：

```text
PCA：
把上万个基因压缩成少数主成分。
主成分保留主要变化来源，减少噪音。

UMAP：
用于可视化细胞整体结构。
UMAP 上距离近的细胞通常表达相似，但不能过度解释精确距离。

聚类：
把表达模式相似的细胞分为一组。
不同 resolution 会得到不同数量的 cluster。
```

---

### 5.4 细胞类型注释

必须解释：

- 注释不是单纯靠软件；
- marker 基因证据最重要；
- 自动注释只能辅助；
- 注释要结合组织背景和文献知识；
- 混合 marker 可能提示 doublet、过渡状态或低质量 cluster。

示例：

```text
细胞类型注释的逻辑：
先看每个 cluster 的高表达 marker。
再对照已知细胞类型 marker。
最后结合样本来源和研究背景命名。

例如：
EPCAM、KRT8、KRT18 高表达提示上皮细胞。
PTPRC 高表达提示免疫细胞。
COL1A1、DCN 高表达提示成纤维细胞。
PECAM1、VWF 高表达提示内皮细胞。
```

---

### 5.5 差异表达分析

必须解释：

- 比较对象是谁；
- 使用什么统计模型；
- logFC 代表什么；
- pvalue 和 padj 区别；
- 上调/下调的方向；
- 结果如何用于后续富集或候选基因筛选。

示例：

```text
log2FoldChange > 0：
表示基因在实验组更高。

log2FoldChange < 0：
表示基因在对照组更高。

padj < 0.05：
表示经过多重检验校正后仍然显著。
```

---

### 5.6 富集分析

必须解释：

- 富集分析回答什么问题；
- 输入基因列表如何来；
- 背景基因集是什么；
- GO / KEGG / Reactome / Hallmark 区别；
- 富集结果不能证明因果；
- 富集结果需要结合方向和原始基因解释。

示例：

```text
富集分析不是看单个基因，而是看一批基因是否集中在某些功能通路。
如果上调基因富集在 cell cycle，说明实验组可能具有更强增殖能力。
但富集结果是统计关联，不等于证明这个通路一定驱动表型。
```

---

### 5.7 CNV / mutation / genomic alteration

必须解释：

- CNV 是什么；
- 为什么肿瘤细胞可能有 CNV；
- inferCNV / CopyKAT 等工具的输入和假设；
- reference cells 的重要性；
- CNV 结果是推断，不是 DNA 测序真值；
- 结果要和其他证据交叉验证。

示例：

```text
CNV 指染色体片段拷贝数增加或减少。
很多恶性肿瘤细胞会出现大范围 CNV。
在单细胞 RNA-seq 中，inferCNV 通过基因表达沿染色体位置的连续偏移来推断 CNV。
这种方法是间接推断，不等于真正的 DNA CNV 测序。
```

---

### 5.8 生存分析和临床验证

必须解释：

- OS / DFS / PFS 等终点含义；
- 高低表达分组如何定义；
- Kaplan-Meier 曲线怎么看；
- Cox 回归回答什么问题；
- HR > 1 和 HR < 1 的意义；
- 单因素和多因素 Cox 区别；
- 不能把相关性直接解释成因果。

示例：

```text
HR > 1：
高风险组死亡风险更高。

HR < 1：
高风险组死亡风险更低，或者该变量可能是保护因素。

P 值显著：
说明两组生存差异不太可能由随机波动造成。

注意：
生存分析显示的是统计相关，不直接证明某基因导致预后变差。
```

---

### 5.9 机器学习和预测模型

必须解释：

- 训练集 / 测试集；
- 过拟合；
- 特征选择；
- 交叉验证；
- AUC、accuracy、sensitivity、specificity；
- 为什么不能在全数据上选特征再测试；
- 外部验证的重要性。

示例：

```text
训练集用于建立模型。
测试集用于评估模型在新数据上的表现。
如果模型在训练集很好、测试集很差，说明可能过拟合。
过拟合意味着模型记住了训练数据噪音，而没有学到可推广规律。
```

---

### 5.10 多组学整合

必须解释：

- 每种组学反映不同层面；
- 表达变化不一定等于蛋白变化；
- 甲基化变化可能影响表达；
- 突变不一定导致表达改变；
- 多组学结果应寻找一致证据链。

示例：

```text
RNA-seq 反映转录水平。
蛋白组反映蛋白水平。
甲基化可能调控基因表达。
突变可能改变蛋白功能。
多组学整合的目标是寻找更完整的机制证据链，而不是简单把结果拼在一起。
```

---

## 6. 教学脚本中的“生物学意义”写法

每个关键分析后都要加一个“生物学意义”注释块。

模板：

```text
生物学意义：
本分析用于判断 ________。
如果结果显示 ________，说明可能存在 ________。
这可以支持我们关于 ________ 的假设。
但需要注意，当前结果只能说明 ________，不能直接证明 ________。
```

示例：

```r
# ---------------------------------------------------------------
# 生物学意义
# ---------------------------------------------------------------
# 如果某个肿瘤亚群高表达 MKI67、TOP2A、STMN1 等基因，
# 说明该亚群可能具有较强的增殖能力。
#
# 如果该亚群同时在患者中与较差预后相关，
# 它可能代表更具侵袭性或治疗抵抗的肿瘤细胞状态。
#
# 但这仍然是表达层面的证据。
# 如果要证明因果关系，还需要实验验证。
# ---------------------------------------------------------------
```

---

## 7. 结果检查和质量判断

每个脚本都应包含结果检查代码。

### 7.1 通用检查

```r
# 查看结果表前几行，确认列名和内容是否正常。
head(result_table)

# 查看结果表维度。
dim(result_table)

# 检查是否有缺失值。
sum(is.na(result_table))

# 查看关键分组数量。
table(metadata$group)
```

### 7.2 单细胞检查

```r
# 查看 Seurat 对象中有多少基因和细胞。
seurat_obj

# 查看每个 cluster 有多少细胞。
table(seurat_obj$seurat_clusters)

# 查看每个样本贡献多少细胞。
table(seurat_obj$sample)
```

### 7.3 差异分析检查

```r
# 查看显著上调和下调基因数量。
table(result_table$change)

# 查看最显著的几个基因。
head(result_table[order(result_table$padj), ])
```

### 7.4 生存分析检查

```r
# 查看高低风险组样本数。
table(clinical_data$risk_group)

# 检查生存时间是否有 0 或缺失。
summary(clinical_data$time)
sum(is.na(clinical_data$status))
```

---

## 8. 报错处理写法

教学脚本应告诉小白遇到错误怎么办。

推荐在关键位置写：

```text
如果这里报错：
1. 先不要继续往下运行。
2. 复制完整红色报错。
3. 检查输入文件路径是否正确。
4. 检查前一步对象是否成功生成。
5. 检查包是否已经 library() 成功。
```

避免只写：

```text
If error, debug.
```

应该写成：

```r
# 如果 readRDS() 报错：
#   1. 检查文件路径是否写错；
#   2. 检查这个 .rds 文件是否真的存在；
#   3. 检查前一个脚本是否成功保存该文件；
#   4. 不要继续运行后面的分析，因为数据对象还没读进来。
obj <- readRDS("data/processed/F1_seurat_object.rds")
```

---

## 9. 文件和目录规范

所有脚本必须使用清晰目录结构。

推荐：

```text
project/
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── F1_scRNA/
│   ├── F2_DEG/
│   └── F3_enrichment/
├── figures/
│   ├── F1_scRNA/
│   ├── F2_DEG/
│   └── F3_enrichment/
├── logs/
├── scripts/
└── docs/
```

命名原则：

- 文件名包含分析模块；
- 文件名包含数据来源；
- 文件名包含关键参数或版本；
- 不使用中文文件名；
- 不使用空格；
- 使用下划线 `_`。

示例：

```text
F1_scRNA_seurat_qc.rds
F2_DEG_tumor_vs_normal_all.csv
F2_DEG_tumor_vs_normal_volcano.pdf
F3_GO_enrichment_upregulated_genes.csv
```

---

## 10. 可复现性要求

每个脚本末尾必须保存：

- 结果对象；
- 关键参数；
- sessionInfo 或包版本；
- 可选随机种子；
- 输入输出路径。

R 示例：

```r
set.seed(1234)

analysis_parameters <- list(
  logFC_cutoff = logFC_cutoff,
  padj_cutoff = padj_cutoff,
  date = Sys.Date()
)

saveRDS(
  analysis_parameters,
  "logs/F2_analysis_parameters.rds"
)

sink("logs/F2_sessionInfo.txt")
print(sessionInfo())
sink()
```

Python 示例：

```python
import sys
import platform
import scanpy as sc
import pandas as pd

with open("logs/session_info.txt", "w") as f:
    f.write(f"Python: {sys.version}\n")
    f.write(f"Platform: {platform.platform()}\n")
    f.write(f"scanpy: {sc.__version__}\n")
    f.write(f"pandas: {pd.__version__}\n")
```

---

## 11. 面向小白的语言风格

### 11.1 应该使用的表达

使用清晰、具体、教学型表达：

```text
这一步的目的是……
这里的输入是……
这里的输出是……
如果结果正常，你应该看到……
如果结果异常，可能说明……
这个参数越大，意味着……
这个图的横轴表示……
这个图的纵轴表示……
从生物学角度看……
但要注意，这只能说明相关性，不能说明因果。
```

### 11.2 避免使用的表达

避免只写术语，不解释：

```text
Run PCA.
Do clustering.
Perform DE.
Calculate enrichment.
Visualize results.
```

避免过度自信：

```text
This proves gene X drives cancer.
```

应改成：

```text
This result suggests gene X may be associated with cancer progression.
Further experimental validation is needed to prove causality.
```

---

## 12. 代码复杂度控制

### 12.1 新手阶段推荐

- 一个代码块只做一件事；
- 每个对象命名清晰；
- 尽量不用过短变量名；
- 少写嵌套函数；
- 少写过长管道；
- 必要时拆成多步；
- 每步后面加检查。

示例：

```r
# 不推荐：一行做太多事
res <- expr %>% filter(rowMeans(.) > 1) %>% log2(. + 1) %>% t() %>% prcomp()

# 推荐：拆成几步
expr_filtered <- expr[rowMeans(expr) > 1, ]

expr_log <- log2(expr_filtered + 1)

expr_for_pca <- t(expr_log)

pca_result <- prcomp(expr_for_pca)
```

---

## 13. 图表解释规范

每个图都应包含：

- 这张图的目的；
- 横轴是什么；
- 纵轴是什么；
- 颜色代表什么；
- 每个点/线/柱子代表什么；
- 正常情况下应该看到什么；
- 异常情况意味着什么；
- 生物学解释。

示例：

```r
# 这张 PCA 图用于观察样本整体表达模式。
# 每个点代表一个样本。
# 点之间越近，说明表达谱越相似。
# 如果肿瘤和正常样本明显分开，说明两组转录组差异较大。
# 如果点主要按 batch 分开，而不是按 group 分开，说明可能存在批次效应。
```

---

## 14. 决策点必须显式写清楚

生信项目中经常需要做选择，例如：

- QC 阈值；
- 是否去除某个样本；
- cluster resolution；
- 差异基因阈值；
- 是否纳入某类细胞；
- 是否使用某个数据集；
- 是否做批次校正。

每个决策点都要写明：

```text
我们有哪些选择？
选择了哪个？
为什么这样选？
这个选择有什么风险？
有没有敏感性分析？
```

示例：

```r
# 决策点：是否过滤线粒体比例高的细胞？
#
# 选择：
#   保留 percent.mt < 20% 的细胞。
#
# 理由：
#   线粒体比例过高通常提示细胞受损。
#   去除这些细胞可以减少低质量细胞对聚类的影响。
#
# 风险：
#   某些真实细胞类型可能天然线粒体比例较高。
#   因此阈值不能机械套用，需要结合数据分布检查。
```

---

## 15. 生信项目脚本类型模板

### 15.1 环境配置脚本

必须包含：

- R/Python 版本；
- 包安装；
- 镜像设置；
- 依赖检查；
- sessionInfo；
- 不建议自动升级所有包。

### 15.2 数据下载脚本

必须包含：

- 数据库来源；
- accession ID；
- 下载文件类型；
- 保存路径；
- 文件完整性检查；
- 下载失败时如何续跑。

### 15.3 数据预处理脚本

必须包含：

- 原始数据格式；
- 清洗规则；
- 过滤阈值；
- 标准化方法；
- 输出中间对象。

### 15.4 主分析脚本

必须包含：

- 生物学问题；
- 核心方法；
- 参数；
- 结果表；
- 图片；
- 结果解释。

### 15.5 验证分析脚本

必须包含：

- 验证数据来源；
- 验证指标；
- 和发现队列的对应关系；
- 一致性或不一致性解释。

### 15.6 可视化脚本

必须包含：

- 每张图回答什么问题；
- 图中元素解释；
- 适合论文还是探索；
- 输出尺寸和格式。

### 15.7 交接脚本

必须包含：

- 当前进度；
- 已完成内容；
- 未完成内容；
- 关键文件路径；
- 重要参数；
- 下一步建议；
- 风险和注意事项。

---

## 16. 生成脚本时的输出要求

当用户要求“应用这个 skill 写脚本”时，输出应尽量包括：

1. 一个完整脚本文件；
2. 清晰文件名；
3. 脚本开头说明；
4. 分节编号；
5. 详细注释；
6. 运行顺序建议；
7. 必须运行和可选运行部分；
8. 输出文件路径；
9. 结果解释；
10. sessionInfo / 版本保存；
11. 如果创建文件，提供下载链接。

如果不能确定某些路径或数据列名，不要编造。可以用明显占位符：

```r
# TODO: 请把这里改成你的真实分组列名
group_column <- "group"
```

---

## 17. 质量检查清单

生成脚本前后，应检查：

### 17.1 教学性

- 是否解释了分析目的？
- 是否解释了生物学意义？
- 是否解释了输入输出？
- 是否解释了关键参数？
- 是否说明图怎么看？
- 是否告诉新手异常结果意味着什么？

### 17.2 可运行性

- 路径是否清楚？
- 文件夹是否自动创建？
- 包是否加载？
- 输出路径是否存在？
- 是否避免一次性全跑导致卡住？
- 是否保存中间对象？

### 17.3 生信合理性

- 数据类型是否匹配方法？
- counts / normalized data 是否区分清楚？
- 是否避免错误使用统计模型？
- 是否说明阈值不是绝对真理？
- 是否避免把相关性说成因果？
- 是否保留可复现信息？

### 17.4 新手友好

- 是否避免过度复杂代码？
- 是否少用难懂缩写？
- 是否解释专业名词？
- 是否用清晰变量名？
- 是否一节只做一类事情？

---

## 18. 推荐给模型使用的提示词模板

用户以后可以这样说：

```text
请应用“生信项目通用小白教学型分析脚本 skill”，
把下面这段代码改写成教学型脚本。

要求：
1. 代码能运行；
2. 结构清晰，分节编号；
3. 注释要解释每一步在做什么；
4. 解释为什么要这么做；
5. 解释输入和输出；
6. 解释统计学或算法原理；
7. 解释生物学意义；
8. 解释结果怎么看；
9. 适合无基础小白学习；
10. 不要写太复杂的 if / for / 自定义函数，除非必要；
11. 关键结果要保存；
12. 末尾保存 sessionInfo。
```

也可以这样说：

```text
请应用这个 skill，为我的生信项目写一个 F2 差异表达分析脚本。
我是小白，请把代码写得能运行、能学习、能交接。
```

---

## 19. 最重要的底层原则

这个 skill 的核心不是“多写注释”，而是：

```text
把生信分析的隐性思路显性化。
```

一个好的小白教学型生信脚本，应该让读者知道：

```text
我为什么要做这个分析？
我拿什么数据做？
我用了什么方法？
这个方法的假设是什么？
结果说明了什么？
结果不能说明什么？
下一步应该怎么验证？
以后遇到类似问题，我该怎么自己写？
```

如果脚本只告诉小白“运行这行代码”，但没有告诉他“为什么运行这行代码”，那就还不是合格的教学型生信脚本。
