---
name: general-bioinformatics-teaching-script-enhanced
version: 1.1.0
last_updated: 2026-05-07
description: Rewrite or author bioinformatics analysis scripts in a beginner-friendly, teaching-oriented style, with extremely detailed explanations for users with weak coding and bioinformatics foundations. This enhanced version explains code syntax, functions, parameters, data types, algorithms, biological meaning, result interpretation, and reproducibility expectations in more depth than the standard skill.
---

# Skill: 生信项目通用“小白教学型分析脚本”写作规范（强化版）

## 0. 这个 skill 解决什么问题

这个 skill 用于把任何生物信息学项目中的分析脚本，改写或新写成 **“代码基础薄弱也能边看边运行、边运行边学习”** 的教学型脚本。

它的目标不是只让代码能跑，而是让刚接触 R / Python / 生信分析的学习者看完后能理解：

1. 这一步在分析什么问题；
2. 为什么必须做这一步；
3. 输入数据是什么格式；
4. 输出结果是什么格式；
5. 每个函数是什么意思；
6. 每个重要参数是什么意思；
7. 每个常见符号怎么读；
8. 用了什么算法或统计思想；
9. 结果怎么看才算正常；
10. 异常结果可能说明什么；
11. 这一步如何连接后续分析；
12. 以后遇到类似任务时，自己应该怎么写代码。

最终脚本必须同时满足三个标准：

- **能运行**：路径清楚，依赖明确，输出可复现；
- **能学习**：注释解释“是什么、为什么、怎么做、怎么看、错了怎么办”；
- **能交接**：别人接手项目时，能理解分析逻辑、对象结构、结果位置和下一步接口。

---

## 1. 最重要的底层原则

这个 skill 的核心不是“多写注释”，而是：

```text
把生信分析的隐性思路显性化。
```

一个好的小白教学型脚本应该让读者知道：

```text
我为什么要做这个分析？
我拿什么数据做？
数据是什么结构？
我用了什么方法？
这个方法的假设是什么？
代码每一段在改变哪个对象？
结果说明了什么？
结果不能说明什么？
下一步应该怎么接？
以后遇到类似问题，我该怎么自己写？
```

如果脚本只告诉小白“运行这行代码”，但没有告诉他“为什么运行这行代码、这行代码怎么读、运行后应该检查什么”，那就不是合格的教学型脚本。

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
- Python: scanpy, anndata, pandas, numpy, scipy, sklearn, matplotlib, squidpy
- Command line: fastqc, multiqc, STAR, HISAT2, Salmon, kallisto, samtools, bedtools, bcftools, GATK
- Workflow: Snakemake, Nextflow, Docker, Conda, renv, mamba

---

## 3. 用户画像：默认读者是“代码和生信双小白”

生成脚本时必须默认读者满足以下特点：

1. 刚接触 RStudio；
2. 不熟悉 R 语法；
3. 不知道什么是表达矩阵、metadata、counts、normalized data；
4. 不知道函数和参数的关系；
5. 不知道对象、向量、矩阵、data.frame、list、Seurat object 是什么；
6. 看到 `if`、`for`、`lapply`、`%>%`、`[[ ]]`、`$`、`@` 容易迷糊；
7. 不知道单细胞分析中 QC、标准化、HVG、PCA、Harmony、UMAP、cluster、marker、annotation 的含义；
8. 需要在 RStudio 中一节一节运行，而不是一口气 Run All。

因此脚本必须写得像“边运行边教学的课程讲义”，不是专家之间的简短 pipeline。

---

## 4. 每个脚本开头必须说明什么

每个脚本开头必须包含：

```text
脚本名称
项目名称
分析模块
适用数据类型
运行环境
运行方式
是否依赖前一步脚本
输入文件
输出文件
核心问题
本脚本不会做什么
重要注意事项
```

### 示例

```r
# ================================================================
# Script: F1_详解.R
# Project: 胃癌 STAD 单细胞亚群研究
# Module: F1 单细胞全细胞图谱
# Data type: single-cell RNA-seq raw UMI counts
#
# 本脚本解决什么问题？
#   本脚本用于从 raw UMI count matrix 和 metadata 出发，
#   构建一个可用于后续 F2–F8 的全细胞 Seurat 对象，
#   并完成 QC、标准化、降维、聚类、细胞注释和 F1 图表输出。
#
# 为什么值得做？
#   F1 是整个单细胞项目的地基。
#   如果细胞注释、样本标签或 QC 错了，后面的 CNV、细胞通讯、marker 筛选、预后分析都会跟着错。
#
# 输入文件：
#   data/raw/scRNA/raw_counts.csv
#   data/raw/scRNA/cell_metadata.csv
#
# 输出文件：
#   data/processed/F1_objects/F1_processed_seurat.rds
#   results/F1_scRNA/tables/F1_cell_annotation_table.tsv
#   results/F1_scRNA/tables/F1_epithelial_cell_ids.tsv
#   figures/F1_scRNA/*.pdf / *.png / *.svg
#   logs/F1_scRNA/F1_sessionInfo.txt
#
# 运行方式：
#   在 RStudio 中打开本脚本。
#   不要 Ctrl + A 全选运行。
#   建议一小节一小节运行。
#   每一节运行后检查 Console 是否有红色报错。
# ================================================================
```

---

## 5. 如果前一步已经运行过，必须删除冗余内容

如果用户说明已经运行过 F0 / 环境配置脚本 / 下载脚本 / 上一步分析脚本，新脚本必须衔接已有结果，而不是重复做前一步工作。

### 5.1 不应该重复的内容

如果 F0 已经完成，不要在 F1 中重复：

- 大批量安装 R 包；
- 创建完整 F1–F8 总目录；
- 设置 CRAN / Bioconductor 镜像；
- 检查 Rtools；
- 下载全部 bulk 队列；
- 重复保存 F0 的 sessionInfo；
- 重复解释“这版脚本和上一版有什么区别”。

### 5.2 应该改成检查式衔接

应该写成：

```r
# 本脚本假设你已经运行过 F0 环境配置脚本。
# 因此这里不再重复安装包，只检查关键包是否可以加载。
# 如果 library() 报错，说明 F0 中对应包没有安装成功，需要回到 F0 修复。
library(data.table)
library(Matrix)
library(Seurat)
```

### 5.3 禁止写版本交付说明

脚本中不要写：

```text
这版脚本和上一版最大的区别是……
本次修改包括……
根据你的反馈我删除了……
```

这些内容对脚本使用者没有价值。

脚本只保留实际运行需要的信息：

```text
运行前准备
输入文件
输出文件
路径设置
参数解释
代码运行
结果检查
异常处理
后续接口
```

---

## 6. 注释必须解释“为什么”，不能只翻译代码

低质量注释：

```r
# 读取文件
expr <- read.csv("expr.csv")
```

高质量注释：

```r
# 读取表达矩阵。
# 表达矩阵是生信分析最核心的数据之一。
# 在单细胞 RNA-seq 中，通常：
#   行 = 基因
#   列 = 细胞
#   数值 = 这个细胞中这个基因检测到的 UMI count
#
# row.names = 1 的意思是：
#   把 CSV 文件的第一列作为行名。
#   如果第一列是 gene symbol，例如 EPCAM、CD3D、COL1A1，
#   就应该把它设为行名，而不是普通数据列。
expr <- read.csv("expr.csv", row.names = 1)
```

每个关键步骤必须解释：

- 这一步在做什么；
- 为什么需要这一步；
- 输入是什么；
- 输出是什么；
- 代码怎么读；
- 函数是什么意思；
- 参数是什么意思；
- 结果应该怎么看；
- 如果结果异常，可能说明什么；
- 这一步如何影响后续分析。

---

## 7. 必须解释 R 代码基础符号

对于代码基础薄弱的用户，脚本应在第一次出现时解释常见 R 语法。

### 7.1 赋值符号 `<-`

```r
# `<-` 是 R 里最常用的赋值符号。
# 可以读作“把右边的结果保存到左边这个名字里”。
#
# 下面这行的意思是：
#   把字符串 "D:/STAD_bioinformation/STAD" 保存到变量 PROJECT_DIR 中。
#   后面只要写 PROJECT_DIR，就代表这个路径。
PROJECT_DIR <- "D:/STAD_bioinformation/STAD"
```

### 7.2 函数和参数

```r
# dir.create() 是创建文件夹的函数。
# 函数名后面的括号里是参数。
#
# path = PROJECT_DIR：要创建哪个文件夹。
# recursive = TRUE：如果上级文件夹不存在，也一起创建。
# showWarnings = FALSE：如果文件夹已经存在，不显示警告。
dir.create(path = PROJECT_DIR, recursive = TRUE, showWarnings = FALSE)
```

### 7.3 `c()`

```r
# c() 的意思是 combine，组合。
# 它可以把多个元素合成一个向量。
#
# 下面这行创建了一个字符向量，里面有 3 个包名。
packages_needed <- c("data.table", "Matrix", "Seurat")
```

### 7.4 `$`

```r
# `$` 用于从 data.frame 或 metadata 中取某一列。
#
# meta$Tissue 的意思是：
#   从 meta 这个表中取出 Tissue 这一列。
table(meta$Tissue)
```

### 7.5 `[[ ]]`

```r
# `[[ ]]` 也可以取某一列，但适合列名保存在变量里的情况。
#
# 如果 meta_cell_id_col = "cell_id"，
# 那么 meta[[meta_cell_id_col]] 等价于 meta$cell_id。
cell_ids <- meta[[meta_cell_id_col]]
```

### 7.6 `if` 和 `stop()`

```r
# if 用于判断条件。
# 如果括号里的条件为 TRUE，就执行大括号里的代码。
#
# stop() 会主动停止脚本，并显示错误信息。
# 这样可以避免在输入文件不对的情况下继续往下跑，产生错误结果。
if (!file.exists(raw_counts_file)) {
  stop("找不到 raw_counts.csv，请先确认数据是否下载成功。")
}
```

### 7.7 `@`

```r
# `@` 常用于 S4 对象，例如 Seurat 对象或 inferCNV 对象。
# 它表示取对象内部的某个 slot。
# 小白阶段不需要深入理解 S4，只要知道这是访问复杂对象内部内容的方式。
```

### 7.8 `%>%`

```r
# `%>%` 叫管道符，可以读作“然后”。
# 它把左边的结果传给右边的函数。
#
# 新手脚本中尽量少用很长的管道。
# 如果使用，必须解释每一步。
```

---

## 8. 参数解释必须具体到“这个参数控制什么”

脚本中第一次出现重要函数时，必须解释关键参数。

### 示例：`fread()`

```r
# fread() 来自 data.table 包，用于快速读取大表格。
# 它比 read.csv() 更适合读取几百 MB 或几 GB 的文件。
#
# nrows = 0 的意思是：
#   只读取表头，不读取真正的数据。
#   这可以快速知道 raw_counts.csv 有哪些列，避免一开始就把 5GB 文件全部读进内存。
header <- names(data.table::fread(raw_counts_file, nrows = 0))
```

### 示例：`CreateSeuratObject()`

```r
# CreateSeuratObject() 用于创建 Seurat 对象。
# Seurat 对象可以理解成一个“单细胞项目文件”，里面同时保存：
#   1. 原始表达矩阵 counts；
#   2. 每个细胞的 metadata；
#   3. 后续生成的 QC 指标；
#   4. PCA / UMAP / cluster 等分析结果。
#
# counts = count_matrix：输入原始 UMI count 矩阵。
# meta.data = metadata：输入每个细胞的身份信息。
# project = "STAD_F1"：给这个 Seurat 对象起一个项目名。
seurat_obj <- CreateSeuratObject(
  counts = count_matrix,
  meta.data = metadata,
  project = "STAD_F1"
)
```

### 示例：`NormalizeData()`

```r
# NormalizeData() 用于标准化单细胞表达矩阵。
# 为什么要标准化？
#   不同细胞测到的总 UMI 数不同。
#   如果不标准化，总 UMI 高的细胞看起来所有基因都偏高。
#
# normalization.method = "LogNormalize"：
#   Seurat 常用标准化方法。
#
# scale.factor = 10000：
#   把每个细胞按总 UMI 归一化到 10000 的尺度。
#   这个 10000 是单细胞分析中常用的约定值。
seurat_obj <- NormalizeData(
  object = seurat_obj,
  normalization.method = "LogNormalize",
  scale.factor = 10000
)
```

### 示例：`RunUMAP()`

```r
# RunUMAP() 用于把高维表达数据压缩到二维平面，方便画图。
#
# reduction = "harmony"：使用 Harmony 批次校正后的低维结果。
# dims = 1:30：使用前 30 个维度。
# seed.use = 42：固定随机种子，让每次运行结果尽量一致。
seurat_obj <- RunUMAP(
  object = seurat_obj,
  reduction = "harmony",
  dims = 1:30,
  seed.use = 42
)
```

---

## 9. 优先使用清晰代码，不追求炫技

面向小白的教学脚本应避免过度复杂写法。

不推荐：

```r
res <- lapply(split(meta, meta$group), \(x) foo(x)) |> bind_rows()
```

推荐：

```r
# 先按照 group 把样本信息分组。
meta_split <- split(meta, meta$group)

# lapply() 的意思是：
#   对列表中的每一个元素执行同一个操作。
# 这里的 one_group_meta 代表某一个分组里的 metadata。
result_list <- lapply(meta_split, function(one_group_meta) {
  foo(one_group_meta)
})

# bind_rows() 的意思是：
#   把多个表格按行合并成一个大表。
result_table <- dplyr::bind_rows(result_list)
```

原则：

- 少用过度嵌套；
- 少用一行写完很多操作；
- 少用隐藏副作用；
- 函数、循环、管道可以用，但必须解释；
- 如果使用高级写法，先用注释解释逻辑。

---

## 10. 每个脚本都要能分节运行

脚本应分成清晰章节，例如：

```text
第 0 节：运行前说明
第 1 节：设置路径和参数
第 2 节：检查包是否可用
第 3 节：读取数据
第 4 节：检查数据结构
第 5 节：数据清洗和过滤
第 6 节：标准化或归一化
第 7 节：核心分析
第 8 节：结果可视化
第 9 节：保存结果
第 10 节：保存运行环境
```

每节都要能单独理解，最好能单独运行和检查。

脚本开头必须提醒：

```text
不要一次性全选运行。
建议一节一节运行。
每节运行后检查输出是否合理。
如果出现红色报错，先停止，不要继续往下跑。
```

---

## 11. 参数区必须放在前面

所有容易修改的参数必须集中放在脚本前面。

### 示例

```r
# ================================================================
# 第 1 节：设置分析参数
# ================================================================
# 为什么把参数放在前面？
#   因为以后你可能需要调整阈值。
#   如果参数散落在脚本各处，很容易改漏。
#
# PROJECT_DIR：项目总目录。
#   这个目录应该和 F0 中设置的项目目录一致。
#
# QC_MIN_FEATURES：每个细胞至少检测到多少个基因。
#   太低可能是低质量细胞或空液滴。
#
# QC_MAX_MT：线粒体基因比例上限。
#   太高通常提示细胞受损或死亡。
# ================================================================

PROJECT_DIR <- "D:/STAD_bioinformation/STAD"

QC_MIN_FEATURES <- 200

QC_MAX_MT <- 20

N_HVG <- 3000

N_PCS <- 50

UMAP_DIMS <- 1:30

CLUSTER_RESOLUTION <- 0.6
```

所有参数必须解释生物学或统计学意义。

---

## 12. 输入检查区必须详细

读取数据后必须检查：

- 数据维度；
- 行名列名；
- 分组数量；
- 缺失值；
- 重复样本或重复细胞；
- 数据类型是否正确；
- 表达矩阵方向是否正确。

### 示例

```r
# 查看表达矩阵有多少行和列。
# 如果行是基因、列是细胞，那么：
#   行数 = 基因数量
#   列数 = 细胞数量
#
# 正常情况下，单细胞数据通常有上万基因和成千上万个细胞。
dim(count_matrix)

# 查看前几个基因名，确认行名确实是基因。
head(rownames(count_matrix))

# 查看前几个细胞名，确认列名确实是细胞 barcode。
head(colnames(count_matrix))

# 查看每个 Tissue 有多少细胞。
# 如果 Tumor 或 Normal 一类完全没有，后续比较就不能做。
table(metadata$Tissue)
```

教学脚本必须告诉小白“看到什么结果才算正常”。

---

## 13. 单细胞 F1 类脚本必须解释的概念

如果脚本涉及单细胞基础流程，必须解释以下概念。

### 13.1 raw counts / UMI

```text
raw counts 是最原始的表达计数。
UMI 是 unique molecular identifier，可以粗略理解为“原始分子计数”。
在 raw_counts 矩阵中：
  行 = 基因
  列 = 细胞
  数值 = 某个细胞中某个基因检测到的 UMI 数
```

### 13.2 metadata

```text
metadata 是每个细胞的身份表。
它通常记录 Sample、Patient、Tissue、cell type、cluster、QC 指标等信息。
表达矩阵告诉我们“这个细胞表达了什么基因”。
metadata 告诉我们“这个细胞来自哪里、属于什么类别”。
```

### 13.3 cell barcode / cell_id

```text
cell barcode 是每个单细胞的编号。
它类似身份证号。
表达矩阵的列名必须和 metadata 的 cell_id 对上。
如果 cell_id 错配，后续所有细胞身份都会错。
```

### 13.4 sparse matrix

```text
单细胞表达矩阵中绝大多数数值是 0。
稀疏矩阵只保存非 0 值，可以大幅节省内存。
```

### 13.5 Seurat object

```text
Seurat object 可以理解成一个单细胞项目文件。
它同时保存 counts、metadata、QC、PCA、UMAP、cluster、marker 等结果。
```

### 13.6 QC 指标

必须解释：

- nFeature_RNA
- nCount_RNA
- percent.mt
- percent.ribo
- doublet

### 13.7 标准化与降维

必须解释：

- NormalizeData
- FindVariableFeatures / HVG
- ScaleData
- PCA
- Harmony
- UMAP
- tSNE
- FindNeighbors
- FindClusters
- resolution

### 13.8 细胞注释

必须解释：

- marker gene
- DotPlot
- FeaturePlot
- 作者注释 vs 自动注释 vs 手动注释
- 为什么不能只看一个 marker 就下结论

---

## 14. 各类分析必须解释的内容

### 14.1 质量控制 QC

必须解释：

- QC 的目的；
- 每个指标是什么意思；
- 为什么要过滤；
- 阈值是不是绝对标准；
- 过滤前后保留多少数据；
- 是否可能误删真实生物学信号。

### 14.2 标准化 / 归一化

必须解释：

- 为什么原始 counts 不能直接比较；
- 标准化解决什么问题；
- 标准化后数据能用于什么；
- 哪些分析必须用 counts，哪些可以用 normalized data。

### 14.3 降维和聚类

必须解释：

- PCA / UMAP / t-SNE 是什么；
- 降维图不能直接等同于真实空间距离；
- 聚类分辨率影响结果；
- 聚类结果要用 marker 验证；
- 批次效应可能影响聚类。

### 14.4 细胞类型注释

必须解释：

- 注释不是单纯靠软件；
- marker 基因证据最重要；
- 自动注释只能辅助；
- 注释要结合组织背景和文献知识；
- 混合 marker 可能提示 doublet、过渡状态或低质量 cluster。

### 14.5 差异表达分析

必须解释：

- 比较对象是谁；
- 使用什么统计模型；
- logFC 代表什么；
- pvalue 和 padj 区别；
- 上调/下调的方向；
- 结果如何用于后续富集或候选基因筛选。

### 14.6 富集分析

必须解释：

- 富集分析回答什么问题；
- 输入基因列表如何来；
- 背景基因集是什么；
- GO / KEGG / Reactome / Hallmark 区别；
- 富集结果不能证明因果；
- 富集结果需要结合方向和原始基因解释。

### 14.7 CNV / mutation / genomic alteration

必须解释：

- CNV 是什么；
- 为什么肿瘤细胞可能有 CNV；
- inferCNV / CopyKAT 等工具的输入和假设；
- reference cells 的重要性；
- CNV 结果是推断，不是 DNA 测序真值；
- 结果要和其他证据交叉验证。

### 14.8 生存分析和临床验证

必须解释：

- OS / DFS / PFS 等终点含义；
- 高低表达分组如何定义；
- Kaplan-Meier 曲线怎么看；
- Cox 回归回答什么问题；
- HR > 1 和 HR < 1 的意义；
- 单因素和多因素 Cox 区别；
- 不能把相关性直接解释成因果。

### 14.9 机器学习和预测模型

必须解释：

- 训练集 / 测试集；
- 过拟合；
- 特征选择；
- 交叉验证；
- AUC、accuracy、sensitivity、specificity；
- 为什么不能在全数据上选特征再测试；
- 外部验证的重要性。

---

## 15. 结果解释区必须写“怎么看”

每个结果输出后，必须添加解释。

### 示例：保存表格

```r
# 保存完整差异分析结果。
# 这个表后续可以用于：
#   1. 筛选显著差异基因；
#   2. 做 GO / KEGG 富集分析；
#   3. 和其他数据集取交集；
#   4. 作为候选 marker 或 biomarker 来源。
write.csv(result_table, "results/F2_DEG/DEG_all.csv", row.names = FALSE)
```

### 示例：解释火山图

```r
# 火山图怎么看？
#   横轴是 log2 fold change，表示表达变化方向和幅度。
#   越往右，表示在实验组越高表达。
#   越往左，表示在对照组越高表达。
#   纵轴是 -log10(padj)，越高说明统计显著性越强。
#
# 注意：
#   火山图只能说明统计相关，不能证明某基因导致疾病。
```

### 示例：解释 UMAP

```r
# UMAP 图怎么看？
#   每个点代表一个细胞。
#   颜色代表细胞类型或 cluster。
#   点之间越近，通常表示表达模式越相似。
#
# 注意：
#   UMAP 是二维可视化，不是细胞在真实身体里的空间位置。
#   不要过度解释两个点之间的精确距离。
```

---

## 16. 生物学意义注释块

每个关键分析后都要加“生物学意义”注释块。

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

## 17. 结果检查和质量判断

每个脚本都应包含结果检查代码。

### 17.1 通用检查

```r
head(result_table)

dim(result_table)

sum(is.na(result_table))

table(metadata$group)
```

### 17.2 单细胞检查

```r
# 查看 Seurat 对象中有多少基因和细胞。
seurat_obj

# 查看每个 cluster 有多少细胞。
table(seurat_obj$seurat_clusters)

# 查看每个样本贡献多少细胞。
table(seurat_obj$Sample)
```

### 17.3 差异分析检查

```r
# 查看显著上调和下调基因数量。
table(result_table$change)

# 查看最显著的几个基因。
head(result_table[order(result_table$padj), ])
```

### 17.4 生存分析检查

```r
# 查看高低风险组样本数。
table(clinical_data$risk_group)

# 检查生存时间是否有 0 或缺失。
summary(clinical_data$time)
sum(is.na(clinical_data$status))
```

---

## 18. 报错处理写法

教学脚本应告诉小白遇到错误怎么办。

推荐在关键位置写：

```r
# 如果这里报错：
#   1. 先不要继续往下运行；
#   2. 复制完整红色报错；
#   3. 检查输入文件路径是否正确；
#   4. 检查前一步对象是否成功生成；
#   5. 检查包是否已经 library() 成功。
```

示例：

```r
# 如果 readRDS() 报错：
#   1. 检查文件路径是否写错；
#   2. 检查这个 .rds 文件是否真的存在；
#   3. 检查前一个脚本是否成功保存该文件；
#   4. 不要继续运行后面的分析，因为数据对象还没读进来。
seurat_obj <- readRDS("data/processed/F1_objects/F1_processed_seurat.rds")
```

---

## 19. 文件和目录规范

所有脚本必须使用清晰目录结构。

推荐：

```text
project/
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── F1_scRNA/
│   ├── F2_subcluster_CNV/
│   └── F3_function/
├── figures/
│   ├── F1_scRNA/
│   ├── F2_subcluster_CNV/
│   └── F3_function/
├── logs/
├── scripts/
└── docs/
```

命名原则：

- 文件名包含分析模块；
- 文件名包含数据来源；
- 文件名包含关键参数或版本；
- 不使用中文文件名作为机器读取路径；
- 不使用空格；
- 使用下划线 `_`。

示例：

```text
F1_processed_seurat.rds
F1_cell_annotation_table.tsv
F2_cnv_classification_table.tsv
F3_GO_enrichment_candidate_subcluster.csv
```

---

## 20. 可复现性要求

每个脚本末尾必须保存：

- 关键对象；
- 结果表；
- 图片；
- 参数；
- sessionInfo 或包版本；
- 可选日志。

R 示例：

```r
set.seed(42)

analysis_parameters <- list(
  seed = 42,
  qc_min_features = QC_MIN_FEATURES,
  qc_max_mt = QC_MAX_MT,
  cluster_resolution = CLUSTER_RESOLUTION,
  date = Sys.Date()
)

saveRDS(
  analysis_parameters,
  "logs/F1_scRNA/F1_analysis_parameters.rds"
)

sink("logs/F1_scRNA/F1_sessionInfo.txt")
print(sessionInfo())
sink()
```

---

## 21. 图表解释规范

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
# 这张 UMAP 图用于观察细胞整体表达结构。
# 每个点代表一个细胞。
# 颜色代表细胞类型。
# 如果相同细胞类型聚在一起，说明注释和降维结果比较合理。
# 如果同一细胞类型被样本完全分开，可能提示批次效应没有被校正好。
```

---

## 22. 决策点必须显式写清楚

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

## 23. 面向小白的语言风格

### 23.1 应该使用的表达

使用清晰、具体、教学型表达：

```text
这一步的目的是……
这里的输入是……
这里的输出是……
这行代码可以读作……
这个函数的作用是……
这个参数控制……
如果结果正常，你应该看到……
如果结果异常，可能说明……
这个参数越大，意味着……
这个图的横轴表示……
这个图的纵轴表示……
从生物学角度看……
但要注意，这只能说明相关性，不能说明因果。
```

### 23.2 避免使用的表达

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

避免交付过程说明：

```text
这版脚本和上一版最大的区别是……
根据你刚才的要求，我修改了……
```

---

## 24. 代码复杂度控制

新手阶段推荐：

- 一个代码块只做一件事；
- 每个对象命名清晰；
- 尽量不用过短变量名；
- 少写嵌套函数；
- 少写过长管道；
- 必要时拆成多步；
- 每步后面加检查；
- 如果必须使用 if / for / lapply，要解释循环变量代表什么。

不推荐：

```r
res <- expr %>% filter(rowMeans(.) > 1) %>% log2(. + 1) %>% t() %>% prcomp()
```

推荐：

```r
# 第一步：过滤低表达基因。
# rowMeans(expr) > 1 的意思是：
#   只保留平均表达量大于 1 的基因。
expr_filtered <- expr[rowMeans(expr) > 1, ]

# 第二步：做 log2 转换。
# +1 是为了避免 log2(0) 无法计算。
expr_log <- log2(expr_filtered + 1)

# 第三步：转置矩阵。
# prcomp() 要求行是样本、列是变量。
expr_for_pca <- t(expr_log)

# 第四步：运行 PCA。
pca_result <- prcomp(expr_for_pca)
```

---

## 25. 常见脚本类型模板

### 25.1 环境配置脚本

必须包含：

- R/Python 版本；
- 包安装；
- 镜像设置；
- 依赖检查；
- sessionInfo；
- 不建议自动升级所有包。

### 25.2 数据下载脚本

必须包含：

- 数据库来源；
- accession ID；
- 下载文件类型；
- 保存路径；
- 文件完整性检查；
- 下载失败时如何续跑。

### 25.3 数据预处理脚本

必须包含：

- 原始数据格式；
- 清洗规则；
- 过滤阈值；
- 标准化方法；
- 输出中间对象。

### 25.4 主分析脚本

必须包含：

- 生物学问题；
- 核心方法；
- 参数；
- 结果表；
- 图片；
- 结果解释。

### 25.5 验证分析脚本

必须包含：

- 验证数据来源；
- 验证指标；
- 和发现队列的对应关系；
- 一致性或不一致性解释。

### 25.6 可视化脚本

必须包含：

- 每张图回答什么问题；
- 图中元素解释；
- 适合论文还是探索；
- 输出尺寸和格式。

### 25.7 交接脚本

必须包含：

- 当前进度；
- 已完成内容；
- 未完成内容；
- 关键文件路径；
- 重要参数；
- 下一步建议；
- 风险和注意事项。

---

## 26. 生成脚本时的输出要求

当用户要求“应用这个 skill 写脚本”时，应尽量包括：

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

## 27. 质量检查清单

生成脚本前后，应检查：

### 27.1 教学性

- 是否解释了分析目的？
- 是否解释了生物学意义？
- 是否解释了输入和输出？
- 是否解释了关键参数？
- 是否解释了关键函数？
- 是否解释了常见 R 语法？
- 是否说明图怎么看？
- 是否告诉新手异常结果意味着什么？

### 27.2 可运行性

- 路径是否清楚？
- 文件夹是否自动创建？
- 包是否加载？
- 输出路径是否存在？
- 是否避免一次性全跑导致卡住？
- 是否保存中间对象？
- 是否检查前一步产物是否存在？

### 27.3 生信合理性

- 数据类型是否匹配方法？
- counts / normalized data 是否区分清楚？
- 是否避免错误使用统计模型？
- 是否说明阈值不是绝对真理？
- 是否避免把相关性说成因果？
- 是否保留可复现信息？

### 27.4 新手友好

- 是否避免过度复杂代码？
- 是否少用难懂缩写？
- 是否解释专业名词？
- 是否用清晰变量名？
- 是否一节只做一类事情？
- 是否不写无关的版本差异说明？

---

## 28. 推荐给模型使用的提示词模板

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
9. 解释函数和参数；
10. 解释常见 R/Python 语法；
11. 适合代码基础薄弱、没有生信基础的新手学习；
12. 不要写太复杂的 if / for / 自定义函数，除非必要；
13. 如果用了复杂写法，必须解释怎么读；
14. 关键结果要保存；
15. 末尾保存 sessionInfo；
16. 不要写“这版和上一版区别”这类交付说明。
```

也可以这样说：

```text
请应用这个 skill，为我的生信项目写一个 F1 单细胞分析脚本。
我代码基础很薄弱，请把代码写得能运行、能学习、能交接。
每个函数和关键参数都要解释。
```
