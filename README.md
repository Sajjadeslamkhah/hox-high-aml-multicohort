# HOX-high AML: multi-cohort transcriptomic analysis

Analysis code, output tables and figures for the manuscript

> **HOX-High Acute Myeloid Leukemia: A Reproducible State Beyond NPM1/KMT2A with CDK9 Upregulation Unlinked to Drug Sensitivity**
> Ozkose B, Eslamkhah S, Gulmez H, Yavas C, Arvas YE, Yilmaz I.
> *Biomedicines* (MDPI), manuscript ID biomedicines-4694076 (under revision).

This repository is private. It is not linked from the manuscript: the Data Availability Statement says that code and outputs are available from the corresponding author on reasonable request.

## Study in brief

- 1,787 adult AML transcriptomes from five public cohorts: TCGA-LAML, BeatAML 2.0, HOVON (GSE14468), and AMLCG (GSE37642) on HG-U133A and on HG-U133 Plus 2.0.
- HOX score: the mean z-score of HOXA5, HOXA6, HOXA7, HOXA9, HOXA10, MEIS1 and PBX3, computed within each cohort.
- HOX-high calling: median + 3 × MAD of HOX-low reference subtypes (CBF-AML, APL, CEBPA double-mutant). A two-component GMM is used when there are fewer than 15 reference cases.
- Analyses:
  - HOX-high frequency outside NPM1/KMT2A lesions
  - reproducible program (meta-analysis) and transfer of a HOX-family-free signature
  - CDK9 / P-TEFb expression
  - BeatAML ex vivo sensitivity to four multi-target CDK inhibitors
  - DepMap CRISPR dependency
  - overall survival

## Layout

| Folder | Contents |
|---|---|
| `notebook/` | `Bengisu_HOX_AML_pipeline.ipynb`, the complete Colab pipeline (fixed seed 2026) |
| `notebook/logs/` | configuration, run log and `pip_freeze.txt` of the reference run (26 Oct 2026, 18:17) |
| `results/tables/` | all output tables of the reference run, including differential expression per cohort and contrast, meta-analysis, GSEA, Cox models, drug sensitivity and DepMap |
| `results/processed/` | patient-level harmonized annotation per cohort and DepMap AML cell-line table |
| `figures/pipeline/` | figures written by the pipeline (PDF) |
| `figures/manuscript/` | final manuscript figures (PNG 600 dpi + PDF) |
| `scripts/` | helper scripts for manuscript figures and tracked-change edits |
| `manuscript/submitted/` | submitted manuscript and Supplementary Materials |
| `manuscript/revision_R1/` | revised manuscript (tracked changes) and responses to reviewers |
| `reviews/` | reviewer comments (round 1) |

## Reproducing the analysis

1. Open `notebook/Bengisu_HOX_AML_pipeline.ipynb` in Google Colab.
2. Mount Google Drive. The pipeline reads from and writes to `MyDrive/Bengisu_HOX_AML/`.
3. Raw inputs are not stored here because of their size. They go in `00_raw/` on Drive:
   - **TCGA-LAML:** UCSC Xena log2(RSEM + 1) expression; cBioPortal `laml_tcga_pub` and `laml_tcga_pan_can_atlas_2018`.
   - **BeatAML 2.0:** expression, clinical, mutation and drug-response files from https://biodev.github.io/BeatAML2/.
   - **GEO:** GSE14468 and GSE37642 (downloaded by GEOparse).
   - **DepMap Public 25Q2:** `CRISPRGeneEffect.csv`, `Model.csv` and `OmicsExpressionProteinCodingGenesTPMLogp1.csv`.
4. Run all cells. Outputs are written to `01_processed/` … `05_reports/`, together with a time-stamped zip archive.

Package versions are listed in `notebook/logs/pip_freeze.txt`. The main ones are pandas 2.2.3, NumPy 2.1.3, SciPy 1.16.3, statsmodels 0.15.0, scikit-learn 1.6.1, lifelines 0.30.3, GSEApy 1.3.1 and GEOparse 2.0.4.

## Not in this repository

The following stay on Google Drive:
- raw data (`00_raw/`; the DepMap files alone are about 1 GB)
- the full output archives `HOX_AML_outputs_*.zip`
- older notebook copies

## Use of generative AI

Claude (Anthropic) was used to help write and debug the analysis code and to draft and edit the manuscript. All code, outputs and text were checked by the authors.
