"""Supplementary Figure S3 + Table S9 (Reviewer 2): HOX-high frequency in NPM1-mutated and/or KMT2A-rearranged
versus NPM1-wt/KMT2A-nr AML, per cohort and pooled (DerSimonian-Laird, logit scale, as in the main analysis).
Usage: python make_figS3.py <results_dir> <out_prefix>"""
import sys, os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.proportion import proportion_confint

R, out = sys.argv[1], sys.argv[2]
COH = [("TCGA", "TCGA-LAML"), ("BeatAML", "BeatAML 2.0"), ("GSE14468", "HOVON (GSE14468)")]
S = {k: pd.read_csv(os.path.join(R, f"processed/{k}_annotated_samples.csv"), index_col=0) for k, _ in COH}

def dl_pool(x, n):
    """Identical to pooled_prop() in the pipeline notebook (section 6)."""
    x, n = np.asarray(x, float), np.asarray(n, float)
    p = (x + .5) / (n + 1); y = np.log(p / (1 - p)); v = 1 / (n * p * (1 - p)); w = 1 / v
    yf = (w * y).sum() / w.sum(); Q = (w * (y - yf) ** 2).sum(); k = len(y)
    tau2 = max(0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum()))
    ws = 1 / (v + tau2); ym = (ws * y).sum() / ws.sum(); se = np.sqrt(1 / ws.sum())
    inv = lambda z: 1 / (1 + np.exp(-z))
    I2 = max(0, (Q - (k - 1)) / Q) * 100 if Q > 0 else 0
    return inv(ym), inv(ym - 1.96 * se), inv(ym + 1.96 * se), I2

groups = {"NPM1mut": lambda d: d.genotype_group == "NPM1mut",
          "KMT2Ar": lambda d: d.genotype_group == "KMT2Ar",
          "NPM1mut and/or KMT2Ar": lambda d: d.genotype_group.isin(["NPM1mut", "KMT2Ar", "NPM1mut+KMT2Ar"]),
          "NPM1-wt/KMT2A-nr": lambda d: d.genotype_group == "Other",
          "NPM1-wt/KMT2A-nr, NUP98r excluded": lambda d: (d.genotype_group == "Other") & (d.NUP98r.fillna(0) != 1)}
rows = []
for g, f in groups.items():
    xs, ns = [], []
    for k, lab in COH:
        d = S[k]; sub = d[f(d)]; x, n = int((sub.HOX_group == "HOX-high").sum()), len(sub)
        lo, hi = proportion_confint(x, n, method="wilson")
        rows.append({"group": g, "cohort": lab, "HOX_high": x, "N": n, "pct": 100 * x / n, "ci_lo": 100 * lo, "ci_hi": 100 * hi})
        xs.append(x); ns.append(n)
    p, lo, hi, I2 = dl_pool(xs, ns)
    rows.append({"group": g, "cohort": "Pooled (random effects)", "HOX_high": sum(xs), "N": sum(ns),
                 "pct": 100 * p, "ci_lo": 100 * lo, "ci_hi": 100 * hi, "I2": I2})
T = pd.DataFrame(rows)

cmp = []
for k, lab in COH:
    d = S[k]; can = d.genotype_group.isin(["NPM1mut", "KMT2Ar", "NPM1mut+KMT2Ar"]); oth = d.genotype_group == "Other"
    a, b = int((d[can].HOX_group == "HOX-high").sum()), int(can.sum()); c, e = int((d[oth].HOX_group == "HOX-high").sum()), int(oth.sum())
    orr, p = stats.fisher_exact([[a, b - a], [c, e - c]])
    cmp.append({"cohort": lab, "canonical": f"{a}/{b}", "NPM1-wt/KMT2A-nr": f"{c}/{e}", "odds_ratio": orr, "P_Fisher": p})
CMP = pd.DataFrame(cmp)
with pd.ExcelWriter(out + "_TableS9.xlsx") as xw:
    T.to_excel(xw, "frequency", index=False); CMP.to_excel(xw, "canonical_vs_noncanonical", index=False)
T.to_csv(out + "_frequency.csv", index=False); CMP.to_csv(out + "_fisher.csv", index=False)
print(T.round(1).to_string()); print(CMP.to_string())

# figure: forest plot
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
show = ["NPM1mut", "KMT2Ar", "NPM1mut and/or KMT2Ar", "NPM1-wt/KMT2A-nr"]
col = {"NPM1mut": "#2a7ad5", "KMT2Ar": "#ea6a35", "NPM1mut and/or KMT2Ar": "#7b4fb3", "NPM1-wt/KMT2A-nr": "#1aa875"}
fig, ax = plt.subplots(figsize=(7.6, 7.2))
y = 0; ticks, labels = [], []
for g in show:
    sub = T[T.group == g]
    for _, r in sub.iterrows():
        pooled = r.cohort.startswith("Pooled")
        ax.errorbar(r.pct, y, xerr=[[max(0, r.pct - r.ci_lo)], [max(0, r.ci_hi - r.pct)]], fmt="D" if pooled else "s",
                    ms=9 if pooled else 6, color=col[g], capsize=3, lw=1.4)
        ax.text(103, y, f"{int(r.HOX_high)}/{int(r.N)}  {r.pct:.1f}% ({r.ci_lo:.1f}–{r.ci_hi:.1f})", va="center", fontsize=8.5)
        ticks.append(y); labels.append(("" if pooled else "   ") + (r.cohort if not pooled else f"{g}: pooled"))
        y -= 1
    y -= 0.6
ax.set_yticks(ticks); ax.set_yticklabels(labels, fontsize=9)
for t, lab in zip(ax.get_yticklabels(), labels):
    if "pooled" in lab: t.set_fontweight("bold")
ax.set_xlim(0, 100); ax.set_xlabel("HOX-high (% of patients, 95% CI)")
ax.text(103, 0.9, "HOX-high/N  % (95% CI)", fontsize=8.5, fontweight="bold")
fig.savefig(out + ".png", dpi=600, bbox_inches="tight"); fig.savefig(out + ".pdf", bbox_inches="tight")
