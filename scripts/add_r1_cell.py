"""Insert the reviewer-round-1 analysis cell (section 13b) into the pipeline notebook, before section 14."""
import json, sys
path = sys.argv[1]
nb = json.load(open(path, encoding="utf8"))

md = """## 13b. Reviewer round 1 (biomedicines-4694076) — CDK9 by genotype group (Reviewer 2, Figure 5A)
Reviewer 2 asked (i) to add NPM1-mutated / KMT2A-rearranged patients as a comparison group for CDK9 and (ii) to compare CDK9 expression of HOX-high patients overall with HOX-high patients without NPM1/KMT2A lesions. Because the overall HOX-high group contains the non-canonical cases, (ii) is tested as canonical versus non-canonical HOX-high (independent groups). We also (iii) fit CDK9 ~ HOX-high + canonical genotype (+ reference-subtype flag) and (iv) repeat the HOX-high vs HOX-low comparison after excluding the HOX-low reference subtypes (CBF-AML, APL, CEBPA double-mutant), which could otherwise drive the difference. Patient-level CDK9 values are exported so that the manuscript figure can be redrawn outside Colab."""

code = r'''checkpoint('13b reviewer R1: CDK9 by genotype group')
import sys, platform
import statsmodels.formula.api as smf
log.info(f'Python {sys.version.split()[0]} | {platform.platform()}')
r1_rows, r1_lm, r1_pat = [], [], []
GENO = ['TCGA', 'BeatAML', 'GSE14468']           # cohorts with NPM1/KMT2A annotation
for n in GENO:
    c = COHORTS.get(n)
    if c is None or 'CDK9' not in c['expr'].index: continue
    e, cl = c['expr'], c['clin'].copy()
    cl['CDK9'] = e.loc['CDK9', cl.index]
    canon = cl['genotype_group'].isin(['NPM1mut', 'KMT2Ar', 'NPM1mut+KMT2Ar'])
    other = cl['genotype_group'] == 'Other'
    hi, lo = cl['HOX_group'] == 'HOX-high', cl['HOX_group'] == 'HOX-low'
    ref = cl['HOXlow_anchor'].fillna(0).astype(int) == 1
    grp = pd.Series(np.nan, index=cl.index, dtype=object)
    grp[hi & canon] = 'HOX-high canonical'; grp[hi & other] = 'HOX-high NPM1-wt/KMT2A-nr'
    grp[lo & canon] = 'HOX-low canonical'; grp[lo & other & ~ref] = 'HOX-low non-reference'; grp[lo & ref] = 'HOX-low reference'
    r1_pat.append(pd.DataFrame({'cohort': n, 'sample': cl.index, 'CDK9': cl['CDK9'].values, 'HOX_score': cl['HOX_score'].values,
                                'HOX_group': cl['HOX_group'].values, 'genotype_group': cl['genotype_group'].values,
                                'HOXlow_reference': ref.astype(int).values, 'plot_group': grp.values}))
    x = cl['CDK9']
    def comp(label, a, b):
        a, b = x[a].dropna(), x[b].dropna()
        if min(len(a), len(b)) < 5: return
        u, p = stats.mannwhitneyu(a, b, alternative='two-sided')
        r1_rows.append({'cohort': n, 'comparison': label, 'n_a': len(a), 'n_b': len(b), 'mean_a': a.mean(), 'mean_b': b.mean(),
                        'log2FC': a.mean() - b.mean(), 'fold_change': 2 ** (a.mean() - b.mean()),
                        'AUC_effect': u / (len(a) * len(b)), 'p_MWU': p})
    comp('HOX-high (all) vs HOX-low (all)', hi, lo)                                    # = Table9 'all'
    comp('HOX-high canonical vs HOX-low (all)', hi & canon, lo)
    comp('HOX-high NPM1-wt/KMT2A-nr vs HOX-low (all)', hi & other, lo)
    comp('HOX-high NPM1-wt/KMT2A-nr vs HOX-low NPM1-wt/KMT2A-nr', hi & other, lo & other)   # = Table9 'Other'
    comp('HOX-high canonical vs HOX-high NPM1-wt/KMT2A-nr', hi & canon, hi & other)
    comp('HOX-high (all) vs HOX-low, reference subtypes excluded', hi & ~ref, lo & ~ref)
    comp('HOX-high NPM1-wt/KMT2A-nr vs HOX-low NPM1-wt/KMT2A-nr, reference excluded', hi & other & ~ref, lo & other & ~ref)
    comp('NPM1mut HOX-high vs NPM1mut HOX-low', hi & (cl['genotype_group'] == 'NPM1mut'), lo & (cl['genotype_group'] == 'NPM1mut'))
    d = pd.DataFrame({'CDK9': x, 'HOXhigh': hi.astype(int), 'canonical': canon.astype(int), 'reference': ref.astype(int)}).dropna()
    d = d[cl.loc[d.index, 'genotype_group'].notna()]
    for form in ['CDK9 ~ HOXhigh + canonical', 'CDK9 ~ HOXhigh + canonical + reference']:
        f = smf.ols(form, data=d).fit()
        for term in f.params.index.drop('Intercept'):
            r1_lm.append({'cohort': n, 'model': form, 'term': term, 'beta_log2': f.params[term],
                          'ci_low': f.conf_int().loc[term, 0], 'ci_high': f.conf_int().loc[term, 1], 'p': f.pvalues[term], 'n': int(f.nobs)})
r1 = pd.DataFrame(r1_rows); r1['FDR'] = bh(r1['p_MWU'])
r1_lm = pd.DataFrame(r1_lm); r1_pat = pd.concat(r1_pat, ignore_index=True)
save_table(r1, 'R1_TableR1_CDK9_by_genotype_group.csv', index=False)
save_table(r1_lm, 'R1_TableR2_CDK9_linear_models.csv', index=False)
save_table(r1_pat, 'R1_TableR3_CDK9_patient_level.csv', index=False)
display(r1.round(4)); display(r1_lm.round(4))

order = ['HOX-low reference', 'HOX-low non-reference', 'HOX-high NPM1-wt/KMT2A-nr', 'HOX-high canonical']
fig, axes = plt.subplots(1, len(GENO), figsize=(4.2 * len(GENO), 3.6), squeeze=False)
for ax, n in zip(axes[0], GENO):
    d = r1_pat[(r1_pat.cohort == n) & r1_pat.plot_group.isin(order)]
    sns.boxplot(data=d, x='plot_group', y='CDK9', order=order, ax=ax, fliersize=0, width=.6, color='#dddddd')
    sns.stripplot(data=d, x='plot_group', y='CDK9', order=order, ax=ax, size=1.6, alpha=.5, color='k')
    ax.set_title(n, fontsize=9); ax.set_xlabel(''); ax.set_ylabel('CDK9 (log2)')
    ax.set_xticklabels([f"{o}\n(n={int((d.plot_group == o).sum())})" for o in order], rotation=30, ha='right', fontsize=7)
fig.tight_layout(); save_fig(fig, 'FigR1_CDK9_by_genotype_group'); plt.show()
'''

cells = nb["cells"]
idx = next(i for i, c in enumerate(cells) if "".join(c["source"]).startswith("## 14."))
if any("13b. Reviewer round 1" in "".join(c["source"]) for c in cells):
    sys.exit("cell already present")
new_md = {"cell_type": "markdown", "metadata": {}, "source": md}
new_code = {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": code}
cells[idx:idx] = [new_md, new_code]
json.dump(nb, open(path, "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("inserted before cell", idx)
