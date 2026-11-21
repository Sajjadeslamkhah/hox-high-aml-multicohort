"""Add Figure S3 and Tables S9-S11 (tracked insertions) to the Supplementary Materials.
Usage: python revise_supplementary.py <unpacked_supp_dir> <repo_dir>"""
import sys, os, re, shutil
import pandas as pd
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import docx_track as T

D, R = sys.argv[1], sys.argv[2]
xml_p = f"{D}/word/document.xml"
x = open(xml_p, encoding="utf8").read()
A = lambda: T._attrs()


def para(style, text, bold_lead=None):
    runs = ""
    if bold_lead:
        runs += T._runs(bold_lead, "<w:rPr><w:b/></w:rPr>")
    runs += T._runs(text, "")
    return (f'<w:p><w:pPr><w:pStyle w:val="{style}"/><w:rPr><w:ins {A()}/></w:rPr></w:pPr>'
            f'<w:ins {A()}>{runs}</w:ins></w:p>')


def cell(text, w, top=None, bottom=None, bold=False, left=False):
    b = lambda v: f'w:val="single" w:sz="{v}" w:space="0" w:color="000000"' if v else 'w:val="nil"'
    borders = f'<w:tcBorders><w:top {b(top)}/><w:left w:val="nil"/><w:bottom {b(bottom)}/><w:right w:val="nil"/></w:tcBorders>'
    rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + '<w:sz w:val="18"/></w:rPr>'
    jc = '<w:jc w:val="left"/>' if left else ""
    return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{borders}</w:tcPr><w:p><w:pPr><w:pStyle w:val="MDPI42tablebody"/>{jc}'
            f'<w:rPr><w:ins {A()}/></w:rPr></w:pPr><w:ins {A()}>{T._runs(str(text), rpr)}</w:ins></w:p></w:tc>')


def table(df, widths):
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    out = (f'<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/><w:tblLayout w:type="fixed"/>'
           f'<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
           f'<w:tblGrid>{grid}</w:tblGrid>')
    out += f'<w:tr><w:trPr><w:tblHeader/><w:jc w:val="center"/><w:ins {A()}/></w:trPr>' + "".join(
        cell(h, w, top=8, bottom=4, bold=True, left=(i == 0)) for i, (h, w) in enumerate(zip(df.columns, widths))) + "</w:tr>"
    n = len(df)
    for r_i, (_, r) in enumerate(df.iterrows()):
        last = r_i == n - 1
        out += f'<w:tr><w:trPr><w:jc w:val="center"/><w:ins {A()}/></w:trPr>' + "".join(
            cell(v, w, bottom=8 if last else None, left=(i == 0)) for i, (v, w) in enumerate(zip(r.values, widths))) + "</w:tr>"
    return out + "</w:tbl>"


def image_para(png, rid, name, docpr_id, width_emu=5943600):
    w, h = Image.open(png).size; cy = round(width_emu * h / w)
    return (f'<w:p><w:pPr><w:pStyle w:val="MDPI52figure"/><w:rPr><w:ins {A()}/></w:rPr></w:pPr><w:ins {A()}><w:r><w:rPr><w:noProof/></w:rPr><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{width_emu}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{docpr_id}" name="Picture {docpr_id}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="0" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:ins></w:p>')


def add_image(png, name, rid):
    im = Image.open(png); tw = 4400
    im.resize((tw, round(tw * im.size[1] / im.size[0])), Image.LANCZOS).save(f"{D}/word/media/{name}", dpi=(600, 600))
    rels_p = f"{D}/word/_rels/document.xml.rels"; rels = open(rels_p, encoding="utf8").read()
    rels = rels.replace("</Relationships>", f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{name}"/></Relationships>')
    open(rels_p, "w", encoding="utf8").write(rels)

f = lambda v, d=1: f"{v:.{d}f}"
blocks = []
# ---- Figure S3 + Table S9
add_image(f"{R}/figures/supplementary/FigureS3.png", "FigureS3.png", "rIdS3")
blocks.append(image_para(f"{R}/figures/supplementary/FigureS3.png", "rIdS3", "FigureS3.png", 30))
blocks.append(para("MDPI51figurecaption",
    " HOX-high status was assessed in each genotyped cohort among patients with an NPM1 mutation, a KMT2A rearrangement, "
    "either lesion (canonical; includes the three BeatAML patients with both) and neither lesion (NPM1-wt/KMT2A-nr). Squares, "
    "per-cohort proportions with Wilson 95% CIs; diamonds, DerSimonian–Laird random-effects pooled estimates on the logit "
    "scale (the same procedure as in the main analysis). Values are listed in Table S9.",
    bold_lead="Figure S3. HOX-high frequency in NPM1-mutated and/or KMT2A-rearranged versus NPM1-wt/KMT2A-nr AML."))

freq = pd.read_csv(f"{R}/results/reviewer_R1/FigureS3_frequency.csv")
t9 = pd.DataFrame({"Genotype group": freq.group, "Cohort": freq.cohort,
                   "HOX-high, n/N": [f"{a}/{b}" for a, b in zip(freq.HOX_high, freq.N)],
                   "HOX-high, % (95% CI)": [f"{f(p)} ({f(l)}–{f(h)})" for p, l, h in zip(freq.pct, freq.ci_lo, freq.ci_hi)],
                   "I² (%)": [("" if pd.isna(i) else f(i, 0)) for i in freq.I2]})
t9["Genotype group"] = t9["Genotype group"].where(t9["Genotype group"] != t9["Genotype group"].shift(), "")
blocks.append(para("MDPI41tablecaption", " HOX-high frequency by genotype group and comparison of canonical with NPM1-wt/KMT2A-nr AML.",
                   bold_lead="Table S9."))
blocks.append(table(t9, [2700, 2200, 1300, 1900, 900]))
fis = pd.read_csv(f"{R}/results/reviewer_R1/FigureS3_fisher.csv")
t9b = pd.DataFrame({"Cohort": fis.cohort, "Canonical HOX-high, n/N": fis.canonical,
                    "NPM1-wt/KMT2A-nr HOX-high, n/N": fis["NPM1-wt/KMT2A-nr"],
                    "Odds ratio": ["∞ (no HOX-low canonical case)" if o == float("inf") else f(o) for o in fis.odds_ratio],
                    "Fisher P": [f"{p:.1e}".replace("e-", " × 10^−").replace("e+", " × 10^") + "^" for p in fis.P_Fisher]})
blocks.append(table(t9b, [2000, 2000, 2300, 2100, 1500]))
blocks.append(para("MDPI43tablefooter",
    "Pooled estimates (rows labelled 'Pooled') are DerSimonian–Laird random-effects estimates on the logit scale; n/N in "
    "pooled rows are summed counts. Canonical, NPM1-mutated and/or KMT2A-rearranged. The NUP98r-excluded row removes the two "
    "NUP98-rearranged TCGA patients; NUP98 rearrangements were not annotated in BeatAML or HOVON."))

# ---- Table S10: DepMap AML lines
dep = pd.read_csv(f"{R}/results/processed/DepMap_AML_lines_HOX_CDK9.csv", index_col=0).sort_values("HOX_score", ascending=False)
t10 = pd.DataFrame({"Cell line": dep.name, "DepMap ID": dep.index, "HOX score": dep.HOX_score.map(lambda v: f(v, 2)),
                    "HOX group": dep.HOX_group, "CDK9 mRNA, log2(TPM+1)": dep.CDK9_expr.map(lambda v: f(v, 2)),
                    "CDK9 gene effect (Chronos)": dep.CDK9_effect.map(lambda v: "NA" if pd.isna(v) else f(v, 2))})
blocks.append(para("MDPI41tablecaption", " DepMap AML cell lines with HOX score, CDK9 expression and CDK9 dependency (DepMap Public 25Q2).",
                   bold_lead="Table S10."))
blocks.append(table(t10, [1500, 1500, 1200, 1300, 2100, 2100]))
blocks.append(para("MDPI43tablefooter",
    f"Lines are sorted by HOX score. HOX group: median split of the HOX score across the {len(dep)} AML lines. CRISPR data "
    f"were available for {dep.CDK9_effect.notna().sum()} lines; NA, not screened. A gene effect of −1 corresponds to the median "
    "effect of common essential genes."))

S11 = f"{R}/results/reviewer_R1/TableS11_rows.csv"
if os.path.exists(S11):
    t11 = pd.read_csv(S11, dtype=str).fillna("")
    blocks.append(para("MDPI41tablecaption", " CDK9 expression by HOX status and genotype group.", bold_lead="Table S11."))
    blocks.append(table(t11, [1300, 3600, 900, 1100, 1300, 1100]))
    blocks.append(para("MDPI43tablefooter", open(f"{R}/results/reviewer_R1/TableS11_footer.txt", encoding="utf8").read().strip()))

end = x.index("<w:sectPr", x.rindex("</w:tbl>"))
x = x[:end] + "".join(blocks) + x[end:]

# contents list (tracked new paragraphs)
x = T.new_paragraph_after(x, "Figure S2. Robustness of the main findings to the HOX-high definition",
                          "Figure S3. HOX-high frequency in NPM1-mutated and/or KMT2A-rearranged versus NPM1-wt/KMT2A-nr AML")
prev = "Table S8. Expression platforms and availability of key genes"
items = ["Table S9. HOX-high frequency by genotype group and comparison of canonical with NPM1-wt/KMT2A-nr AML",
         "Table S10. DepMap AML cell lines with HOX score, CDK9 expression and CDK9 dependency"]
if os.path.exists(S11):
    items.append("Table S11. CDK9 expression by HOX status and genotype group")
for it in items:
    x = T.new_paragraph_after(x, prev, it); prev = it
open(xml_p, "w", encoding="utf8").write(x)
print("added blocks:", len(blocks))
