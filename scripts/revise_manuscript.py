"""Round-1 revision edits (tracked) for biomedicines-4694076. Usage: python revise_manuscript.py <document.xml>
Phase A: text edits that do not depend on the new Colab run."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import docx_track as T

p = sys.argv[1]
x = open(p, encoding="utf8").read()
log = []
def do(fn, *a, **k):
    global x
    x = fn(x, *a, **k); log.append((fn.__name__, a[0][:60]))

# ---------- Reviewer 2: modest CDK9 difference (Abstract, Results, headings, Conclusions)
do(T.replace, "was higher in HOX-high AML in all five cohorts (FDR < 0.05 in four). However",
   "was modestly higher (1.1- to 1.3-fold) in HOX-high AML in all five cohorts (FDR < 0.05 in four). However")
do(T.replace, "is selectively upregulated in HOX-high AML", "is consistently but modestly upregulated in HOX-high AML", nth=0)
do(T.replace, "is selectively upregulated in HOX-high AML", "is consistently but modestly upregulated in HOX-high AML", nth=0)
do(T.replace, "is selectively but modestly upregulated", "is consistently but modestly upregulated")
do(T.insert_after, "1.8 × 10⁻¹²) and 0.346 (P = 6.8 × 10⁻⁸) in TCGA, BeatAML and HOVON.",
   " The differences were modest: they correspond to 1.11- to 1.28-fold higher expression in all patients and 1.23- to "
   "1.32-fold higher expression within the NPM1-wt/KMT2A-nr stratum, and the probability that a HOX-high patient had higher "
   "*CDK9* expression than a HOX-low patient was 0.61–0.68.")

# ---------- Reviewer 1: cohort definition, abbreviations spelled out at first use
do(T.insert_after, "Cohort characteristics are summarized in Table 1.",
   " Here, a cohort denotes an independently collected, processed and published series of patients with AML profiled on "
   "one expression platform; the five cohorts comprised 140–591 patients each (1,787 in total). Genotype-defined subsets "
   "within a cohort are referred to as strata, and their sizes are reported wherever they are analyzed.")
do(T.replace, "ex vivo drug-sensitivity data from BeatAML [42,43]",
   "ex vivo drug-sensitivity data from the Beat AML project (BeatAML) [42,43]")
do(T.replace, "dependency data from DepMap [44,45]", "dependency data from the Cancer Dependency Map (DepMap) [44,45]")
do(T.replace, "from the UCSC Xena hub", "from the University of California Santa Cruz (UCSC) Xena hub")
do(T.replace, "through the cBioPortal application programming interface",
   "through the application programming interface of cBioPortal for Cancer Genomics")
do(T.replace, "treated in HOVON/SAKK protocols",
   "treated in protocols of the Dutch–Belgian Hemato-Oncology Cooperative Group and the Swiss Group for Clinical Cancer Research (HOVON/SAKK)")
do(T.replace, "Analyses used Python with pandas, NumPy, SciPy, statsmodels [66], scikit-learn [60], lifelines [71], GSEApy [62] and GEOparse.",
   "Analyses were run in Python 3 on Google Colaboratory with pandas 2.2.3, NumPy 2.1.3, SciPy 1.16.3, statsmodels 0.15.0 [66], "
   "scikit-learn 1.6.1 [60], lifelines 0.30.3 [71], GSEApy 1.3.1 [62], GEOparse 2.0.4, matplotlib 3.10.0 and seaborn 0.13.2; "
   "the complete list of package versions was saved with each run.")

# ---------- Reviewer 2: why the classifier transfers without retraining (Methods 2.6)
do(T.insert_after, "It was then applied without retraining to the other cohorts, and its AUC was recorded in all patients and in the NPM1-wt/KMT2A-nr stratum.",
   " Retraining was not needed for two reasons. Every feature was z-scored within its own cohort before the classifier was "
   "applied, which removes platform-specific differences in scale. In addition, the signature genes had been selected for a "
   "concordant direction of change in at least four of the five cohorts, so their association with HOX-high status is shared "
   "across cohorts (the 200 most up- and downregulated genes overlapped 17.5- to 44.6-fold more than expected; Table S3). "
   "Because the signature genes were selected with data from all cohorts, the transfer measures the consistency of a shared "
   "program rather than providing a fully independent validation.")

# ---------- Reviewer 2: HOX-high frequency in canonical vs non-canonical AML (Results 3.2)
do(T.replace, "-rearranged patients. The size",
   "-rearranged patients. With both lesions combined, 98.1% (82.8–99.8) of canonical patients were HOX-high. In every "
   "genotyped cohort, HOX-high status was much less frequent among NPM1-wt/KMT2A-nr than among canonical patients (54.8% vs. "
   "100% in TCGA, 36.7% vs. 91.3% in BeatAML and 39.2% vs. 100% in HOVON; Fisher P ≤ 5.2 × 10^−12^; Figure S3; Table S9). The size")

# ---------- Figure 1C legend (Reviewer 1, comment 5)
do(T.replace, "and bimodality coefficient (BC).",
   "and bimodality coefficient (BC; values above the benchmark of 0.555 are shown in black).")

# ---------- Discussion: recent literature (refs 77–88, numbered in order of first citation)
do(T.replace, "-activating lesions [29,30].",
   "-activating lesions [29,30]. Since then, the phase 2 parts of phase 1/2 trials have confirmed the activity of revumenib "
   "in relapsed or refractory *KMT2A*-rearranged acute leukemia [77] and *NPM1*-mutated AML [78] and of ziftomenib in "
   "*NPM1*-mutated AML [79]. Revumenib has been approved for relapsed or refractory *KMT2A*-rearranged acute leukemia and "
   "ziftomenib for relapsed or refractory *NPM1*-mutated AML [78,80–82], and combinations with azacitidine and venetoclax "
   "are being evaluated in phase 1 trials [80,83]. Ziftomenib is also active in *NUP98*-rearranged cells and primary "
   "samples [81], whereas acquired *MEN1* mutations can mediate clinical resistance to menin inhibition [84]. These "
   "developments make the size of the non-canonical HOX-high fraction clinically relevant.")
do(T.insert_after, "itself is unlikely to serve as a selection marker.",
   " More selective CDK9 inhibitors such as AZD4573 and enitociclib are being tested preclinically in combination with "
   "venetoclax and azacitidine in AML [85] or with a menin inhibitor in *KMT2A*-rearranged infant leukemia cells [86]; our "
   "results suggest that such studies should look for response predictors other than *CDK9* abundance.")
do(T.insert_after, "add prognostic information to current genetic risk classification.",
   " This agrees with a recent HARMONY Alliance analysis of a large harmonized cohort, in which risk within *NPM1*-mutated "
   "AML was refined by combinations of co-mutations [87].")

# ---------- Author contributions typo
do(T.replace, "manuscript. . B.O.", "manuscript. B.O.")

# ---------- Supplementary Materials list
do(T.insert_after, "Robustness of the main findings to the HOX-high definition;",
   " Figure S3: HOX-high frequency in NPM1-mutated and/or KMT2A-rearranged versus NPM1-wt/KMT2A-nr AML;")
do(T.insert_after, "Expression platforms and availability of key genes",
   "; Table S9: HOX-high frequency by genotype group and comparison of canonical with NPM1-wt/KMT2A-nr AML; "
   "Table S10: DepMap AML cell lines with HOX score, CDK9 expression and CDK9 dependency; "
   "Table S11: CDK9 expression by HOX status and genotype group")

# ---------- Italics: ex vivo, mouse gene symbols (Reviewer 1, comments 3 and 4)
tot = {}
for term in ["ex vivo", "in vivo", "Hoxa9", "HoxA9", "Hoxa7", "Hoxa10", "Meis1a", "Meis1", "Pbx1b", "Npm1", "Flt3", "Cd34", "Hoxa", "Mll"]:
    x, n = T.italicize_all(x, term); tot[term] = n

# ---------- Abbreviations (Reviewer 1, comment 1)
new_rows = {"APL": "Acute promyelocytic leukemia", "BC": "Bimodality coefficient",
            "BeatAML": "Beat AML project (functional genomic landscape of AML)",
            "CRISPR": "Clustered regularly interspaced short palindromic repeats", "DepMap": "Cancer Dependency Map",
            "GDSC": "Genomics of Drug Sensitivity in Cancer", "GMM": "Gaussian mixture model", "HOX": "Homeobox (genes)",
            "KEGG": "Kyoto Encyclopedia of Genes and Genomes", "MCL-1": "Myeloid cell leukemia 1 (protein)",
            "MLL": "Mixed-lineage leukemia (former name of KMT2A)", "MSigDB": "Molecular Signatures Database",
            "NA": "Not available", "RNA-seq": "RNA sequencing", "RSEM": "RNA-Seq by Expectation-Maximization",
            "SAKK": "Swiss Group for Clinical Cancer Research", "TPM": "Transcripts per million",
            "UCSC": "University of California Santa Cruz"}
import re as _re
start = x.index("The following abbreviations")
tbl_end = x.index("</w:tbl>", start)
existing = []
for tr in _re.finditer(r"<w:tr[ >].*?</w:tr>", x[start:tbl_end], _re.S):
    t = _re.search(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", tr.group(0))
    if t: existing.append(t.group(1))
merged = sorted(set(existing) | set(new_rows), key=lambda k: k.lower())
for k in [k for k in merged if k in new_rows]:
    prev = merged[merged.index(k) - 1]
    x = T.add_table_row_after(x, prev, [k, new_rows[k]], start=start); log.append(("row", k))
print("existing abbreviations:", existing)

# ---------- New references 77-88 (PubMed-verified), appended after reference 76
import json as _json
_refs = _json.load(open(os.path.join(os.path.dirname(__file__), "new_references_R1.json"), encoding="utf8"))
anchor = "Ogawara, Y.;"
for r in _refs:
    x = T.new_paragraph_after(x, anchor, r); log.append(("ref", r[:40]))
    anchor = r[:70]   # author string of the reference just added (unique)

open(p, "w", encoding="utf8").write(x)
print(len(log), "edits;", "italicized:", tot)
