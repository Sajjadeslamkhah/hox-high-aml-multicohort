"""Redraw manuscript Figure 1 from reference-run outputs (26 Oct 2026).
Changes vs submitted version (Reviewer 1, comment 5): panel C no longer has an unlabeled dotted line running
through the bar labels; the ΔBIC = 10 reference line is labelled, BC values sit in their own column, and the
panel-A legend / GMM note no longer overlap the bars.
Usage: python make_fig1.py <results_dir> <out_prefix>"""
import sys, os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint

R, out = sys.argv[1], sys.argv[2]
BLUE, ORANGE, GREEN, GREY = "#2a7ad5", "#ea6a35", "#1aa875", "#8a8a85"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": "#444"})
T2 = pd.read_csv(os.path.join(R, "tables/Table2_HOX_calling_stats.csv")).set_index("cohort")
C = [("TCGA", "TCGA-LAML"), ("BeatAML", "BeatAML"), ("GSE14468", "HOVON\n(GSE14468)"),
     ("GSE37642_GPL96", "AMLCG U133A\n(GSE37642)"), ("GSE37642_GPL570", "AMLCG U133 Plus 2.0\n(GSE37642)")]
S = {k: pd.read_csv(os.path.join(R, f"processed/{k}_annotated_samples.csv"), index_col=0) for k, _ in C}

fig = plt.figure(figsize=(14, 10.2))
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1.05], hspace=0.62, wspace=0.45)
for j, (k, lab) in enumerate(C):
    ax = fig.add_subplot(gs[0, j]); d = S[k].dropna(subset=["HOX_score", "HOX_group"])
    bins = np.linspace(d.HOX_score.min(), d.HOX_score.max(), 31)
    for g, col in [("HOX-low", BLUE), ("HOX-high", ORANGE)]:
        ax.hist(d.HOX_score[d.HOX_group == g], bins=bins, color=col, label=g, rwidth=0.85)
    ymax = ax.get_ylim()[1]
    ref = d.HOX_score[d.HOXlow_anchor == 1]
    ax.plot(ref, np.full(len(ref), -0.08 * ymax), "|", color="#555", ms=9)
    ax.set_ylim(-0.15 * ymax, ymax * 1.05)
    thr = T2.loc[k, "threshold"]
    if pd.notna(thr):
        ax.axvline(thr, ls="--", color="k", lw=1.3)
    else:
        pass
    n_hi, n = int((d.HOX_group == "HOX-high").sum()), len(d)
    gmm = "" if pd.notna(thr) else "; GMM split"
    ax.set_title(f"{lab}\n{n_hi}/{n} HOX-high ({100 * n_hi / n:.0f}%){gmm}", fontsize=10)
    ax.set_xlabel("HOX score (mean z)")
    ax.set_yticks([t for t in ax.get_yticks() if 0 <= t <= ymax])
    if j == 0:
        ax.set_ylabel("Patients")
        ax.text(-0.35, 1.25, "A", transform=ax.transAxes, fontsize=17, fontweight="bold")
fig.legend(*fig.axes[0].get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(0.5, 0.995), ncol=3, frameon=False)

# B: HOX-high by genotype group (95% Wilson CI)
ax = fig.add_subplot(gs[1, :3])
groups = [("NPM1mut", BLUE, "NPM1mut"), ("KMT2Ar", ORANGE, "KMT2Ar"), ("Other", GREEN, "NPM1-wt/KMT2A-nr"), ("ref", GREY, "HOX-low reference")]
for i, (k, lab) in enumerate(C[:3]):
    d = S[k]
    for m, (g, col, glab) in enumerate(groups):
        sub = d[d.HOXlow_anchor == 1] if g == "ref" else d[d.genotype_group == g]
        x, nn = int((sub.HOX_group == "HOX-high").sum()), len(sub)
        lo, hi = proportion_confint(x, nn, method="wilson"); p = x / nn
        xpos = i + (m - 1.5) * 0.2
        ax.bar(xpos, 100 * p, width=0.19, color=col, label=glab if i == 0 else None)
        ax.errorbar(xpos, 100 * p, yerr=[[max(0, 100 * (p - lo))], [max(0, 100 * (hi - p))]], color="k", capsize=3, lw=1.2)
        ax.text(xpos, 100 * hi + 2, str(nn), ha="center", fontsize=8.5, color="#444")
ax.set_xticks(range(3)); ax.set_xticklabels([l.replace("\n", " ") for _, l in C[:3]])
ax.set_ylim(0, 115); ax.set_ylabel("HOX-high (% of group, 95% CI)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.16), ncol=4, frameon=False, fontsize=9.5)
ax.text(1.0, -0.17, "Numbers above bars: patients per group", transform=ax.transAxes, ha="right", fontsize=8.5, color="#444")
ax.text(-0.1, 1.12, "B", transform=ax.transAxes, fontsize=17, fontweight="bold")

# C: ΔBIC with bimodality coefficient in a separate column
ax = fig.add_subplot(gs[1, 3:]); ax.set_position(ax.get_position().translated(0.04, 0).expanded(0.93, 1))
short = ["TCGA", "BeatAML", "HOVON", "AMLCG\nU133A", "AMLCG\nU133 Plus 2.0"]
y = np.arange(len(C))[::-1]
db = [T2.loc[k, "dBIC"] for k, _ in C]; bc = [T2.loc[k, "bimodality_coef"] for k, _ in C]
ax.barh(y, db, color="#9cc3ee", height=0.55)
ax.axvline(10, ls=":", color="k", lw=1.2)
ax.text(12, len(C) - 0.45, "ΔBIC = 10", fontsize=8.5, color="#333", va="bottom")
ax.axvline(0, color="#444", lw=0.8)
ax.set_yticks(y); ax.set_yticklabels(short)
ax.set_xlim(-20, 235); ax.set_ylim(-0.6, len(C) - 0.1)
for yi, b in zip(y, bc):
    ax.text(1.03, yi, f"{b:.2f}", transform=ax.get_yaxis_transform(), va="center", fontsize=9.5,
            color="k" if b > 0.555 else "#777")
ax.text(1.03, len(C) - 0.35, "BC", transform=ax.get_yaxis_transform(), va="center", fontsize=9.5, fontweight="bold")
ax.set_xlabel("ΔBIC, 1- vs 2-component mixture")
ax.text(-0.30, 1.12, "C", transform=ax.transAxes, fontsize=17, fontweight="bold")

fig.savefig(out + ".png", dpi=600, bbox_inches="tight"); fig.savefig(out + ".pdf", bbox_inches="tight")
for (k, _), d, b in zip(C, db, bc): print(k, round(d, 1), b)
