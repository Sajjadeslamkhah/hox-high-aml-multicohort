"""Revised Figure 5 (Reviewer 2): (A) CDK9 log2FC vs HOX-low for all, canonical and NPM1-wt/KMT2A-nr patients;
(B) P-TEFb / CDK9-responsive genes heatmap (unchanged data, Table9); (C) CDK9 by HOX status and genotype group.
Usage: python make_fig5.py <results_dir> <out_prefix>"""
import sys, os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

R, out = sys.argv[1], sys.argv[2]
t9 = pd.read_csv(f"{R}/tables/Table9_CDK9_PTEFb_by_HOX.csv")
r1 = pd.read_csv(f"{R}/tables/R1_TableR1_CDK9_by_genotype_group.csv")
pat = pd.read_csv(f"{R}/tables/R1_TableR3_CDK9_patient_level.csv")
GREY, GREEN, BLUE, ORANGE, LBLUE = "#4a4a48", "#1aa875", "#2a7ad5", "#ea6a35", "#9cc3ee"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
COH = [("TCGA", "TCGA-LAML"), ("BeatAML", "BeatAML"), ("GSE14468", "HOVON (GSE14468)"),
       ("GSE37642_GPL96", "AMLCG U133A (GSE37642)"), ("GSE37642_GPL570", "AMLCG U133 Plus 2.0 (GSE37642)")]
fp = lambda p: f"p={p:.1e}" if p < 1e-3 else f"p={p:.3f}"

fig = plt.figure(figsize=(15, 11))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.85], hspace=0.38, wspace=0.42)

# A
ax = fig.add_subplot(gs[0, 0])
series = [("all", "HOX-high (all) vs HOX-low (all)", GREY, "All patients"),
          ("can", "HOX-high canonical vs HOX-low (all)", BLUE, "Canonical HOX-high vs HOX-low"),
          ("oth", "HOX-high NPM1-wt/KMT2A-nr vs HOX-low NPM1-wt/KMT2A-nr", GREEN, "NPM1-wt/KMT2A-nr")]
yt, yl = [], []
for i, (k, lab) in enumerate(COH):
    y0 = -i * 1.0
    for j, (key, comp, col, leg) in enumerate(series):
        if key == "all":
            r = t9.query("cohort == @k and gene == 'CDK9' and stratum == 'all'")
            if not len(r): continue
            fc, p = r.log2FC.iloc[0], r.p_MWU.iloc[0]
        else:
            r = r1[(r1.cohort == k) & (r1.comparison == comp)]
            if not len(r): continue
            fc, p = r.log2FC.iloc[0], r.p_MWU.iloc[0]
        yy = y0 + 0.25 - j * 0.25
        ax.scatter(fc, yy, color=col, s=55, zorder=3, label=leg if i == 0 else None)
        ax.text(0.52, yy, fp(p), color=col, va="center", fontsize=8.5)
    yt.append(y0); yl.append(lab)
ax.axvline(0, ls="--", color="#444", lw=1)
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=9.5); ax.set_xlim(-0.1, 0.62)
ax.set_xlabel("CDK9 log2 fold change vs HOX-low")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=3, frameon=False, fontsize=8.5)
ax.text(-0.42, 1.08, "A", transform=ax.transAxes, fontsize=17, fontweight="bold")

# B
ax = fig.add_subplot(gs[0, 1])
genes = ["CDK9", "CCNT1", "CCNT2", "HEXIM1", "LARP7", "MEPCE", "AFF4", "ELL2", "BRD4", "MLLT1", "MLLT3", "MCL1", "MYC", "PIM1", "BCL2A1", "XIAP"]
a = t9[t9.stratum == "all"]
M = a.pivot(index="gene", columns="cohort", values="log2FC").reindex(index=genes, columns=[c for c, _ in COH])
F = a.pivot(index="gene", columns="cohort", values="FDR").reindex(index=genes, columns=[c for c, _ in COH])
cmap = LinearSegmentedColormap.from_list("bo", [BLUE, "#f2f2f0", ORANGE])
im = ax.imshow(M.values, aspect="auto", cmap=cmap, norm=TwoSlopeNorm(0, -1.25, 1.25))
for (gi, ci), v in np.ndenumerate(F.values):
    if v < 0.05: ax.plot(ci, gi, "k.", ms=4)
ax.axhline(10.5, color="white", lw=3)
ax.set_yticks(range(len(genes))); ax.set_yticklabels(genes, style="italic", fontsize=9.5)
ax.set_xticks(range(len(COH))); ax.set_xticklabels(["TCGA", "BeatAML", "HOVON", "AMLCG-A", "AMLCG-P2"], rotation=40, ha="right")
cb = fig.colorbar(im, ax=ax, fraction=0.05); cb.set_label("log2FC (• FDR < 0.05)")
ax.set_title("P-TEFb/SEC components (top) and\nCDK9-dependent transcripts (bottom)", fontsize=10.5)
ax.text(-0.3, 1.08, "B", transform=ax.transAxes, fontsize=17, fontweight="bold")

# C
order = ["HOX-low reference", "HOX-low non-reference", "HOX-high NPM1-wt/KMT2A-nr", "HOX-high canonical"]
short = ["HOX-low\nreference", "HOX-low\nother", "HOX-high\nNPM1-wt/\nKMT2A-nr", "HOX-high\ncanonical"]
cols = [LBLUE, BLUE, GREEN, ORANGE]
sub = gs[1, :].subgridspec(1, 3, wspace=0.3)
for j, (k, lab) in enumerate(COH[:3]):
    ax = fig.add_subplot(sub[0, j]); d = pat[pat.cohort == k]
    data = [d.CDK9[d.plot_group == g].dropna().values for g in order]
    bp = ax.boxplot(data, widths=0.6, patch_artist=True, showfliers=False, medianprops=dict(color="k"))
    for b, c in zip(bp["boxes"], cols): b.set_facecolor(c); b.set_alpha(0.75)
    rng = np.random.default_rng(1)
    for i, v in enumerate(data):
        ax.scatter(i + 1 + rng.uniform(-0.18, 0.18, len(v)), v, s=4, color="k", alpha=0.35, zorder=3)
    ax.set_xticks(range(1, 5)); ax.set_xticklabels([f"{s}\n(n={len(v)})" for s, v in zip(short, data)], fontsize=8)
    r = r1[(r1.cohort == k) & (r1.comparison == "HOX-high canonical vs HOX-high NPM1-wt/KMT2A-nr")]
    ttl = lab + (f"\ncanonical vs NPM1-wt/KMT2A-nr HOX-high: Δ={r.log2FC.iloc[0]:.2f}, {fp(r.p_MWU.iloc[0])}" if len(r) else "")
    ax.set_title(ttl, fontsize=9)
    if j == 0:
        ax.set_ylabel("CDK9 (log2 expression)")
        ax.text(-0.3, 1.12, "C", transform=ax.transAxes, fontsize=17, fontweight="bold")
fig.savefig(out + ".png", dpi=600, bbox_inches="tight"); fig.savefig(out + ".pdf", bbox_inches="tight")
print("ok")
