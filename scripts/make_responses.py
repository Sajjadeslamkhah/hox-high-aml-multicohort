"""Build the point-by-point responses (one .docx per reviewer) for biomedicines-4694076, round 1.
Usage: python make_responses.py <out_dir> [r2_fig5_json]"""
import sys, os, json
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

out = sys.argv[1]
R2 = json.load(open(sys.argv[2], encoding="utf8")) if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else None
TITLE = ("HOX-High Acute Myeloid Leukemia: A Reproducible State Beyond NPM1/KMT2A with CDK9 Upregulation "
         "Unlinked to Drug Sensitivity")
BLUE = RGBColor(0x1F, 0x4E, 0x9A)


def base_doc(rev):
    d = Document()
    st = d.styles["Normal"]; st.font.name = "Palatino Linotype"; st.font.size = Pt(11)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2.0)
    p = d.add_paragraph(); r = p.add_run(f"Response to Reviewer {rev}"); r.bold = True; r.font.size = Pt(14)
    p = d.add_paragraph(); p.add_run("Manuscript ID: ").bold = True; p.add_run("biomedicines-4694076")
    p = d.add_paragraph(); p.add_run("Title: ").bold = True; p.add_run(TITLE)
    return d


def intro(d, text):
    d.add_paragraph(text)
    p = d.add_paragraph(); r = p.add_run(
        "All changes are shown with tracked changes in the revised manuscript and Supplementary Materials. Below, the "
        "reviewer's comments are in bold italics, and our responses follow. Quoted manuscript text is shown in blue. "
        "Locations refer to section numbers of the revised manuscript.")
    r.italic = True


def point(d, n, comment, response, changes=None):
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(10)
    r = p.add_run(f"Comment {n}. "); r.bold = True
    r = p.add_run(comment); r.bold = True; r.italic = True
    for para in response:
        p = d.add_paragraph();
        if para is response[0]:
            p.add_run("Response: ").bold = True
        p.add_run(para)
    for loc, txt in (changes or []):
        p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.8)
        r = p.add_run(f"{loc}: "); r.bold = True; r.font.size = Pt(10)
        r = p.add_run(f"“{txt}”"); r.font.color.rgb = BLUE; r.font.size = Pt(10)


def closing(d):
    d.add_paragraph("We thank the reviewer again for the careful reading and the constructive comments, which have "
                    "improved the manuscript.")
    d.add_paragraph("On behalf of all authors,")
    d.add_paragraph("Sajjad Eslamkhah")


# ======================================================================================== Reviewer 1
d = base_doc(1)
intro(d, "We thank the reviewer for the time spent on our manuscript and for the comments on its scope, its "
         "references and its presentation. We have addressed each point as described below.")

point(d, "1 (general)",
      "I can't say whether this manuscript falls into the article or review category because nothing was actually "
      "done in the laboratory (no experiments). It is more of a review: an analysis based on databases. In addition, "
      "the analyzed data include older or very old references in the bibliography (some more than 10 years old). "
      "Considering that, at least in 2025, the Harmony Alliance Foundation upgraded a lot of information at the "
      "genetic level regarding the classification of AML (EHA 2025), or that in the period 2024-2025 a series of "
      "articles regarding HOX high/low expression or NPM1 in AML appeared, I don't see the relevance of the study "
      "presented in this manuscript.",
      ["Article type. We respectfully disagree that the manuscript is a review. A review summarizes published findings. "
       "Our study instead reports new results from a primary analysis of patient-level data: 1,787 adult AML "
       "transcriptomes from five cohorts, ex vivo sensitivity of 452 BeatAML patients to four CDK inhibitors and "
       "genome-scale CRISPR dependency data. None of the main results (the calibrated frequency of HOX-high AML "
       "outside NPM1/KMT2A lesions, the cross-cohort program, the CDK9–sensitivity analysis and the survival models) "
       "has been reported before. Secondary analysis of public datasets is an established form of original "
       "research. We agree, however, that the absence of wet-laboratory validation is a real limitation; it is stated "
       "explicitly in Section 4.5, and our conclusions are framed as hypotheses for experimental testing.",
       "References. Most of the older references are primary sources that should be cited in their original form: "
       "the first descriptions of HOX/MEIS1/PBX3 expression in AML, menin dependence, P-TEFb biology, the cohort "
       "publications whose data we analyzed, and statistical methods (for example, Wilson 1927, Cox 1972 and "
       "DerSimonian–Laird 1986). We agree that recent literature was under-represented. We have added 11 references "
       "published in 2023–2026 (new references 77–87), all checked in PubMed. They cover the phase 2 results and "
       "regulatory approval of the menin inhibitors revumenib and ziftomenib, combination trials, menin inhibition "
       "in NUP98-rearranged leukemia, MEN1-mediated resistance, newer selective CDK9 inhibitors, and the recent "
       "HARMONY Alliance co-mutation-based risk classification of NPM1-mutated AML [87].",
       "HARMONY/EHA 2025 and relevance. We could not find a peer-reviewed publication of the specific EHA 2025 "
       "presentation, so we cite the peer-reviewed HARMONY analysis [87]. These genomic refinements and our study "
       "address different questions. HARMONY and the ELN/WHO/ICC systems refine risk within genotype-defined "
       "groups. Our study asks how often a transcriptional state that is usually attributed to NPM1 and KMT2A lesions "
       "occurs without them. This question has become more relevant, not less, because menin inhibitors that act by "
       "suppressing this program are now approved for NPM1-mutated and KMT2A-rearranged leukemia [77–82]. Our data "
       "indicate that about two in five patients without these lesions (pooled 42.7%) share the HOX-high program. "
       "We have added a short paragraph on this point to Section 4.2."],
      [("Section 4.2 (new text)",
        "Since then, the phase 2 parts of phase 1/2 trials have confirmed the activity of revumenib in relapsed or "
        "refractory KMT2A-rearranged acute leukemia [77] and NPM1-mutated AML [78] and of ziftomenib in NPM1-mutated "
        "AML [79]. Revumenib has been approved for relapsed or refractory KMT2A-rearranged acute leukemia and "
        "ziftomenib for relapsed or refractory NPM1-mutated AML [78,80–82], … These developments make the size of the "
        "non-canonical HOX-high fraction clinically relevant."),
       ("Section 4.4 (new text)",
        "This agrees with a recent HARMONY Alliance analysis of a large harmonized cohort, in which risk within "
        "NPM1-mutated AML was refined by combinations of co-mutations [87]."),
       ("Section 4.3 (new text)",
        "More selective CDK9 inhibitors such as AZD4573 and enitociclib are being tested preclinically in combination "
        "with venetoclax and azacitidine in AML [85] or with a menin inhibitor in KMT2A-rearranged infant leukemia "
        "cells [86]; …")])

point(d, 2,
      "There are many abbreviations in the text that do not appear in the table at the end of the manuscript (HOX, "
      "BetAML CRISPR, DepMap, cBioPortal application, GSEApy, Python, HOVON/SAKK protocol, etc.). This makes it look "
      "like a coded document. There is no mention of the program type or the version used. Not everyone uses the same "
      "programs, but they would like to know which ones were used.",
      ["Thank you. We have checked every abbreviation in the text. We added 18 entries to the Abbreviations table: "
       "APL, BC, BeatAML, CRISPR, DepMap, GDSC, GMM, HOX, KEGG, MCL-1, MLL, MSigDB, NA, RNA-seq, RSEM, SAKK, TPM "
       "and UCSC. We also spelled out the resources at first use: Beat AML project (BeatAML), Cancer Dependency Map "
       "(DepMap), University of California Santa Cruz (UCSC) Xena, cBioPortal for Cancer Genomics, and Dutch–Belgian "
       "Hemato-Oncology Cooperative Group/Swiss Group for Clinical Cancer Research (HOVON/SAKK). GSEApy and Python "
       "are software names rather than abbreviations; they are now listed with their versions.",
       "Software and data versions. Section 2.12 now gives the environment and the version of every package used. "
       "The data releases were already specified and are unchanged: DepMap Public 25Q2, BeatAML 2.0 (waves 1–4), "
       "the cBioPortal study identifiers, and the GEO accessions. The full package list of each run is saved "
       "automatically and is available on request together with the code."],
      [("Section 2.12", "Analyses were run in {PYVER} on Google Colaboratory with pandas 2.2.3, NumPy 2.1.3, SciPy 1.16.3, "
        "statsmodels 0.15.0, scikit-learn 1.6.1, lifelines 0.30.3, GSEApy 1.3.1, GEOparse 2.0.4, matplotlib 3.10.0 and "
        "seaborn 0.13.2; the complete list of package versions was saved with each run.")])

point(d, 3,
      "The notion of cohort refers to a group of over 600 patients (except for rare diseases, obviously). In this "
      "study, I do not see this (yes, we are talking about a cohort of all AML patients analyzed, but not about those "
      "split into categories).",
      ["We use “cohort” in its usual epidemiological sense: an independently assembled and published series of "
       "patients. It does not imply a minimum size. Each of our five series is a separate study population with its "
       "own patient selection, sample processing and expression platform (140–591 patients each; 1,787 in total). "
       "Analyzing them separately, rather than pooling raw data, is what allows us to test reproducibility across "
       "cohorts. We agree that the term needed a definition and that the genotype-defined subsets are smaller. We now "
       "define the term in Section 2.1 and refer to genotype subsets as strata. Their sizes are reported in Table 1 "
       "and next to every estimate, and the pooled estimates are given with confidence intervals and I² so that the "
       "precision of each subgroup estimate is visible."],
      [("Section 2.1", "Here, a cohort denotes an independently collected, processed and published series of patients "
        "with AML profiled on one expression platform; the five cohorts comprised 140–591 patients each (1,787 in "
        "total). Genotype-defined subsets within a cohort are referred to as strata, and their sizes are reported "
        "wherever they are analyzed.")])

point(d, 4, "Check italics/capital letters for mouse genes.",
      ["Corrected. Mouse gene symbols are now written with an initial capital and in italics throughout the text and "
       "the reference titles (for example, Hoxa9, Meis1, Meis1a, Pbx1b and Mll). Human gene symbols are in "
       "italic capitals, and protein names are in roman type."])

point(d, 5, "Mark ex vivo/in vitro in italics.",
      ["Corrected. All 16 occurrences of “ex vivo” and both occurrences of “in vivo” are now in italics. The "
       "manuscript does not contain “in vitro”."])

point(d, 6, "Fig. 1C: It seems that there is an extra line left in the graph.",
      ["Thank you for spotting this. The vertical dotted line marked a ΔBIC of 10, the conventional threshold for "
       "strong evidence in favor of the two-component model. It had no label and crossed the bimodality-coefficient "
       "labels, so it looked like a leftover line. We redrew Figure 1 from the original output tables. The line is "
       "now labelled, the bimodality coefficients are shown in a separate column, and overlapping labels in panel A "
       "were removed. The data are unchanged."],
      [("Figure 1 legend, panel C", "… and bimodality coefficient (BC; values above the benchmark of 0.555 are shown "
        "in black).")])
closing(d)
d.save(os.path.join(out, "Response_to_Reviewer_1.docx"))

# ======================================================================================== Reviewer 2
d = base_doc(2)
intro(d, "We thank the reviewer for the accurate summary of our work and for the constructive suggestions. We have "
         "carried out the additional analyses that were requested. The new results are presented in a revised "
         "Figure 5, a new Figure S3 and new Tables S9 and S11.")

point(d, 1,
      "One concern is that the reported differences in HOX expression between HOX-high and HOX-low groups across 4 "
      "databases are relatively modest (max log2 fold change of 0.401, which is a 1.32-fold increase).",
      ["We agree. The values the reviewer cites are the CDK9 differences between HOX-high and HOX-low AML. They are "
       "small: 1.11- to 1.28-fold in all patients and 1.23- to 1.32-fold in the NPM1-wt/KMT2A-nr stratum. They "
       "were consistent in direction across all five cohorts (FDR < 0.05 in four). The HOX genes themselves differ "
       "far more between the groups, as the HOX-score distributions in Figure 1A and the program in Figure 3B show. We "
       "now state the magnitude of the CDK9 difference explicitly in the Abstract and in Section 3.4, including the "
       "probability of superiority (0.61–0.68). We have also replaced “selectively upregulated” with “consistently but "
       "modestly upregulated” (see also Comment 4). The small size of the CDK9 difference agrees with our main "
       "conclusion: CDK9 abundance does not identify patients who are more sensitive to CDK inhibitors."],
      [("Abstract", "CDK9, but no other P-TEFb component, was modestly higher (1.1- to 1.3-fold) in HOX-high AML in all "
        "five cohorts (FDR < 0.05 in four)."),
       ("Section 3.4", "The differences were modest: they correspond to 1.11- to 1.28-fold higher expression in all "
        "patients and 1.23- to 1.32-fold higher expression within the NPM1-wt/KMT2A-nr stratum, and the probability "
        "that a HOX-high patient had higher CDK9 expression than a HOX-low patient was 0.61–0.68.")])

point(d, 2,
      "Fig 2: Please add a supplementary figure showing the frequency of HOX-high patients among those with NPM1 "
      "mutations and/or KMT2A rearrangements. Is the frequency comparable to that in patients without these "
      "alterations?",
      ["We added Figure S3 and Table S9. HOX-high frequencies were as follows:",
       "• NPM1-mutated patients: pooled 98.0% (95% CI 86.8–99.7).",
       "• KMT2A-rearranged patients: pooled 85.9% (73.4–93.1).",
       "• Either lesion: pooled 98.1% (82.8–99.8).",
       "• NPM1-wt/KMT2A-nr patients: pooled 42.7% (34.2–51.7).",
       "The frequencies are therefore not comparable. In every genotyped cohort, HOX-high status was much more "
       "frequent in canonical than in non-canonical patients: 100% vs. 54.8% in TCGA, 91.3% vs. 36.7% in BeatAML "
       "and 100% vs. 39.2% in HOVON (Fisher P ≤ 5.2 × 10⁻¹²). The per-cohort values were also shown in Figure 1B. "
       "We have added this comparison to Section 3.2."],
      [("Section 3.2", "With both lesions combined, 98.1% (82.8–99.8) of canonical patients were HOX-high. In every "
        "genotyped cohort, HOX-high status was much less frequent among NPM1-wt/KMT2A-nr than among canonical patients "
        "(54.8% vs. 100% in TCGA, 36.7% vs. 91.3% in BeatAML and 39.2% vs. 100% in HOVON; Fisher P ≤ 5.2 × 10⁻¹²; "
        "Figure S3; Table S9).")])

point(d, 3,
      "Fig3D: Clarify why the BeatAML-derived classifier could be applied to TCGA-AML and HOVON without retraining. "
      "Was this due to substantial overlap in the upregulated genes across these datasets?",
      ["Two features of the design allow this, and the reviewer's suggestion is part of the answer.",
       "First, every feature was z-scored within its own cohort before the classifier was applied. This puts "
       "RNA-seq and microarray data on a common relative scale, so the coefficients learned in BeatAML can be "
       "applied to the other cohorts without platform-specific recalibration.",
       "Second, the signature genes were chosen for a concordant direction of change in at least four of the five "
       "cohorts. Their association with HOX-high status is therefore shared across cohorts. Consistent with this, the "
       "200 most up- and downregulated genes overlapped 17.5- to 44.6-fold more than expected by chance between every "
       "pair of cohorts (Table S3).",
       "The unweighted signature score, which involves no training at all, gave similar AUCs. Because the signature "
       "genes were selected with data from all cohorts, the transfer shows that the program is consistent across "
       "cohorts; it is not a fully independent validation. We now say this explicitly in Section 2.6, in addition to "
       "the existing statement in Sections 3.3 and 4.2."],
      [("Section 2.6", "Retraining was not needed for two reasons. Every feature was z-scored within its own cohort "
        "before the classifier was applied, which removes platform-specific differences in scale. In addition, the "
        "signature genes had been selected for a concordant direction of change in at least four of the five cohorts, "
        "so their association with HOX-high status is shared across cohorts (the 200 most up- and downregulated genes "
        "overlapped 17.5- to 44.6-fold more than expected; Table S3). Because the signature genes were selected with "
        "data from all cohorts, the transfer measures the consistency of a shared program rather than providing a "
        "fully independent validation.")])

r2_4 = R2["response"] if R2 else ["{{R2_FIG5_RESPONSE}}"]
r2_4_changes = [tuple(c) for c in R2["changes"]] if R2 else []
point(d, 4,
      "Fig5A: To support the claim that CDK9 is selectively upregulated in HOX-high AML, I suggest including patients "
      "with NPM1 mutations and/or KMT2A rearrangements as an additional comparison group. I would also reconsider the "
      "term \"selectively upregulated,\" because the difference between HOX-high and HOX-low groups does not appear "
      "particularly significant. It might be also beneficial to run a statistical analysis comparing CDK9 expression "
      "in HOX high patients between all patients' vs NPM1-wt/KMT2A-nr.",
      r2_4 + ["Terminology. We agree and have replaced “selectively upregulated” with “consistently but modestly "
              "upregulated” in the Section 3.4 heading, the Figure 5 title and the Conclusions. “Selectively” was meant "
              "to say that CDK9 was the only P-TEFb component that changed, but it could be read as implying a large "
              "or specific effect."],
      r2_4_changes + [("Section 3.4 heading / Figure 5 title", "CDK9 is consistently but modestly upregulated in "
                                                                 "HOX-high AML")])
closing(d)
d.save(os.path.join(out, "Response_to_Reviewer_2.docx"))
print("written")
