"""Rebuild manuscript Figure 6 (A, B from Table7; C from DepMap_AML_lines_HOX_CDK9.csv, 26 Oct 2026 run)."""
import sys, re
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

t7, dep, out = sys.argv[1], sys.argv[2], sys.argv[3]
T = pd.read_csv(t7); D = pd.read_csv(dep, index_col=0)
BLUE, GREEN, ORANGE, GREY = "#2272d9", "#1aa875", "#ea6a35", "#8a8a85"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": "#444", "axes.linewidth": 1.1})

def ci(s):
    a, b = re.findall(r"-?\d+\.\d+", s); return float(a), float(b)

fig = plt.figure(figsize=(13.4, 9.4))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0], hspace=0.42, wspace=0.42)

# ---- A
ax = fig.add_subplot(gs[0, :])
cdk = T[T["class"] == "CDK9i"].reset_index(drop=True)
ax.axhspan(-0.2, 0.2, color="#f1f0ed", zorder=0); ax.axhline(0, color="#444", lw=1)
for j, (col, lab, c) in enumerate([("CDK9", "CDK9 mRNA", BLUE), ("PTEFb_score", "P-TEFb module score", GREEN),
                                   ("HOX_score", "HOX score", ORANGE)]):
    x = np.arange(len(cdk)) + (j - 1) * 0.22
    r = cdk[f"rho_{col}"].values; lo, hi = zip(*cdk[f"rho_{col}_CI"].map(ci))
    ax.errorbar(x, r, yerr=[r - np.array(lo), np.array(hi) - r], fmt="o", color=c, ms=8, capsize=3, lw=1.6, label=lab)
ax.set_xticks(range(len(cdk))); ax.set_xticklabels([f"{d}\n(n={n})" for d, n in zip(cdk.drug, cdk.n)], color="#444")
ax.set_ylim(-0.35, 0.35); ax.set_ylabel("Spearman ρ with ex vivo AUC\n(positive = less sensitive)")
ax.text(len(cdk) - 0.5, 0.21, "equivalence bounds ±0.2", ha="right", va="bottom", fontsize=9.5, color="#444")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.13), ncol=3, frameon=False)
ax.text(-0.07, 1.08, "A", transform=ax.transAxes, fontsize=17, fontweight="bold")

# ---- B
ax = fig.add_subplot(gs[1, 0])
ctrl = T[T["class"] != "CDK9i"]
rows = [(f"{d.split(' (')[0]} · {'FLT3-ITD' if g == 'FLT3_ITD' else g}", dl, p, GREY)
        for d, g, dl, p in zip(ctrl.drug, ctrl.genotype, ctrl.cliffs_delta_genotype, ctrl.p_genotype_MWU)]
rows += [(f"{d.split(' (')[0]} · HOX-high", dl, p, ORANGE) for d, dl, p in zip(cdk.drug, cdk.cliffs_delta_HOX, cdk.p_HOX_MWU)]
y = np.arange(len(rows))[::-1]
for yi, (lab, dl, p, c) in zip(y, rows):
    ax.barh(yi, dl, color=c, height=0.6)
    ps = f"p={p:.1e}" if p < 1e-3 else f"p={p:.3f}"
    ax.text(max(dl, 0) + 0.02, yi, ps, va="center", fontsize=9.5, color="#333")
ax.axvline(0, color="#444", lw=1); ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=10, color="#444")
ax.set_xlim(-0.7, 0.35); ax.set_xlabel("Cliff's δ for AUC (negative = more sensitive)")
ax.set_title("Positive controls (grey) vs CDK inhibitors by HOX status", fontsize=11.5)
ax.text(-0.75, 1.06, "B", transform=ax.transAxes, fontsize=17, fontweight="bold")

# ---- C
ax = fig.add_subplot(gs[1, 1])
c = D.dropna(subset=["CDK9_effect"])
re_ = stats.spearmanr(c.CDK9_expr, c.CDK9_effect); rh = stats.spearmanr(c.HOX_score, c.CDK9_effect)
for grp, col in [("HOX-low", BLUE), ("HOX-high", ORANGE)]:
    s = c[c.HOX_group == grp]
    ax.scatter(s.CDK9_expr, s.CDK9_effect, color=col, s=36, label=f"{grp} (n={len(s)})", zorder=3)
ax.axhline(-1, ls=":", color="#444", lw=1.2)
ax.text(ax.get_xlim()[1] if False else c.CDK9_expr.max(), -1.04, "gene effect = −1", ha="right", va="top", fontsize=9.5, color="#444")
ax.set_xlabel("CDK9 mRNA, log2(TPM+1)"); ax.set_ylabel("CDK9 CRISPR gene effect (Chronos)")
ax.set_ylim(-2.45, -0.75)
ax.set_title(f"DepMap AML lines (n = {len(c)}): ρ(expr)={re_.statistic:.2f} (p={re_.pvalue:.2f}); "
             f"ρ(HOX)={rh.statistic:.2f} (p={rh.pvalue:.2f})", fontsize=10.5)
ax.legend(loc="lower center", ncol=2, frameon=False)
ax.text(-0.2, 1.06, "C", transform=ax.transAxes, fontsize=17, fontweight="bold")

fig.savefig(out + ".png", dpi=600, bbox_inches="tight"); fig.savefig(out + ".pdf", bbox_inches="tight")
print("n CRISPR", len(c), "rho expr", re_, "rho hox", rh)
