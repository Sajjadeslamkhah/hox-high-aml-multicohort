"""Small tracked-change toolkit for word/document.xml (MDPI manuscripts).

Inline markup in new text: *italic*, ~bold~, ^superscript^.
All functions take and return the XML string. Each old/anchor string must lie inside a single <w:t>.
"""
import re, itertools
from xml.sax.saxutils import escape

AUTHOR = "Sajjad Eslamkhah"
DATE = "2026-11-21T12:00:00Z"
_ids = itertools.count(910000)
RUN_RE = re.compile(r"<w:r(?: [^>]*)?>(?:(?!</w:r>).)*?</w:r>", re.S)
T_RE = re.compile(r"<w:t(?: [^>]*)?>([^<]*)</w:t>")


def _attrs():
    return f'w:id="{next(_ids)}" w:author="{AUTHOR}" w:date="{DATE}"'


def _rpr_add(rpr, tag):
    """Return rPr with an extra empty toggle element (e.g. <w:i/>), keeping schema order roughly right."""
    if not rpr:
        return f"<w:rPr>{tag}</w:rPr>"
    if tag in rpr:
        return rpr
    if tag.startswith("<w:vertAlign"):
        m = re.search(r"<w:rtl|<w:cs[ />]|<w:em |<w:lang|<w:eastAsianLayout|<w14:|</w:rPr>", rpr)
        return rpr[:m.start()] + tag + rpr[m.start():]
    # put <w:i/> / <w:vertAlign> after rStyle/rFonts/b if present, else first
    m = re.match(r"(<w:rPr>(?:<w:rStyle[^>]*/>)?(?:<w:rFonts[^>]*/>)?(?:<w:b/>)?(?:<w:bCs/>)?)", rpr)
    return rpr[:m.end()] + tag + rpr[m.end():]


def _get_rpr(run_xml):
    """Outer <w:rPr> of a run (handles nested rPr inside rPrChange); tracked-change history is dropped."""
    i = run_xml.find("<w:rPr>")
    if i < 0 or not re.match(r"<w:r(?: [^>]*)?>$", run_xml[:i]):
        return ""
    j = run_xml.find("</w:rPrChange></w:rPr>", i)
    if j >= 0:
        full = run_xml[i:j + len("</w:rPrChange></w:rPr>")]
        return re.sub(r"<w:rPrChange .*?</w:rPrChange>", "", full, flags=re.S)
    return run_xml[i:run_xml.index("</w:rPr>", i) + len("</w:rPr>")]


def _runs(text, rpr):
    """Build plain runs from markup text with a base rPr."""
    out = []
    for tok in re.split(r"(\*[^*]+\*|\^[^^]+\^|~[^~]+~)", text):
        if not tok:
            continue
        r = rpr
        if tok.startswith("*"):
            tok = tok[1:-1]; r = _rpr_add(rpr, "<w:i/>")
        elif tok.startswith("~"):
            tok = tok[1:-1]; r = _rpr_add(rpr, "<w:b/>")
        elif tok.startswith("^"):
            tok = tok[1:-1]; r = _rpr_add(rpr, '<w:vertAlign w:val="superscript"/>')
        out.append(f'<w:r>{r}<w:t xml:space="preserve">{escape(tok)}</w:t></w:r>')
    return "".join(out)


def _strip_markup(s):
    return re.sub(r"[*^]", "", s)


def _find_run(x, text, nth=None):
    et = escape(text)
    hits = [m for m in RUN_RE.finditer(x) if re.search(r"<w:t(?: [^>]*)?>[^<]*" + re.escape(et), m.group(0))
            and "<w:delText" not in m.group(0)]
    if nth is None:
        if len(hits) != 1:
            raise ValueError(f"{len(hits)} runs contain {text!r}")
        return hits[0], et
    return hits[nth], et


def _split(x, m, et, mid_xml_fn):
    run = m.group(0)
    rpr = _get_rpr(run)
    tm = next(t for t in T_RE.finditer(run) if et in t.group(1))
    text = tm.group(1); i = text.index(et)
    before, after = text[:i], text[i + len(et):]
    pre, suf = run[:tm.start()], run[tm.end():]
    s = pre + (f'<w:t xml:space="preserve">{before}</w:t>' if before else "") + "</w:r>"
    s += mid_xml_fn(rpr, et)
    s += f"<w:r>{rpr}" + (f'<w:t xml:space="preserve">{after}</w:t>' if after else "") + suf
    return x[:m.start()] + s + x[m.end():]


def replace(x, old, new, nth=None):
    m, et = _find_run(x, old, nth)
    def mid(rpr, et):
        s = f'<w:del {_attrs()}><w:r>{rpr}<w:delText xml:space="preserve">{et}</w:delText></w:r></w:del>'
        if new:
            s += f'<w:ins {_attrs()}>{_runs(new, rpr)}</w:ins>'
        return s
    return _split(x, m, et, mid)


def insert_after(x, anchor, new, nth=None):
    m, et = _find_run(x, anchor, nth)
    def mid(rpr, et):
        return f'<w:r>{rpr}<w:t xml:space="preserve">{et}</w:t></w:r><w:ins {_attrs()}>{_runs(new, rpr)}</w:ins>'
    return _split(x, m, et, mid)


def italicize_all(x, term, skip_italic=True):
    """Tracked formatting change: make every non-italic occurrence of term italic."""
    n = 0
    while True:
        et = escape(term)
        cand = None
        for m in RUN_RE.finditer(x):
            r = m.group(0)
            if "<w:delText" in r or "<w:rPrChange" in r:
                continue
            if re.search(r"<w:t(?: [^>]*)?>[^<]*" + re.escape(et), r) and not (skip_italic and "<w:i/>" in r):
                cand = m; break
        if cand is None:
            return x, n
        def mid(rpr, et):
            new_rpr = _rpr_add(rpr, "<w:i/>")
            old_inner = rpr[len("<w:rPr>"):-len("</w:rPr>")] if rpr else ""
            chg = f'<w:rPrChange {_attrs()}><w:rPr>{old_inner}</w:rPr></w:rPrChange>'
            new_rpr = new_rpr[:-len("</w:rPr>")] + chg + "</w:rPr>"
            return f'<w:r>{new_rpr}<w:t xml:space="preserve">{et}</w:t></w:r>'
        x = _split(x, cand, et, mid); n += 1


def new_paragraph_after(x, anchor, text, nth=None):
    """Insert a tracked new paragraph (same style as the anchor's paragraph) after the paragraph containing anchor."""
    m, et = _find_run(x, anchor, nth)
    p_start = x.rfind("<w:p ", 0, m.start()); p_start2 = x.rfind("<w:p>", 0, m.start()); p_start = max(p_start, p_start2)
    p_end = x.index("</w:p>", m.end()) + len("</w:p>")
    para = x[p_start:p_end]
    ppr = re.search(r"<w:pPr>.*?</w:pPr>", para, re.S); ppr = ppr.group(0) if ppr else "<w:pPr></w:pPr>"
    # mark paragraph mark as inserted (drop any change marks copied from a previously inserted paragraph)
    ppr = re.sub(r"<w:(ins|del) [^>]*/>", "", ppr)
    if "<w:rPr>" in ppr:
        ppr = ppr.replace("<w:rPr>", f"<w:rPr><w:ins {_attrs()}/>", 1)
    else:
        ppr = ppr.replace("</w:pPr>", f"<w:rPr><w:ins {_attrs()}/></w:rPr></w:pPr>")
    first = RUN_RE.search(para)
    rpr = _get_rpr(first.group(0)) if first else ""
    rpr = re.sub(r"<w:i/>|<w:b/>|<w:vertAlign[^>]*/>", "", rpr)
    newp = f"<w:p>{ppr}<w:ins {_attrs()}>{_runs(text, rpr)}</w:ins></w:p>"
    return x[:p_end] + newp + x[p_end:]


def add_table_row_after(x, anchor_cell_text, cells, start=0):
    """Clone the table row whose first cell is exactly anchor_cell_text; insert a tracked new row after it."""
    m = re.compile(r"<w:t(?: [^>]*)?>" + re.escape(escape(anchor_cell_text)) + "</w:t>").search(x, start)
    s = x.rfind("<w:tr ", 0, m.start()); e = x.index("</w:tr>", m.end()) + len("</w:tr>")
    row = x[s:e]
    tcs = re.findall(r"<w:tc>.*?</w:tc>", row, re.S)
    new_tcs = []
    for tc, txt in zip(tcs, cells):
        fr = RUN_RE.search(tc); rpr = _get_rpr(fr.group(0)) if fr else ""
        ppr = re.search(r"<w:pPr>.*?</w:pPr>", tc, re.S).group(0)
        ppr_ins = ppr.replace("</w:pPr>", f"<w:rPr><w:ins {_attrs()}/></w:rPr></w:pPr>") if "<w:rPr>" not in ppr else ppr
        tcpr = re.search(r"<w:tcPr>.*?</w:tcPr>", tc, re.S).group(0)
        new_tcs.append(f"<w:tc>{tcpr}<w:p>{ppr_ins}<w:ins {_attrs()}>{_runs(txt, rpr)}</w:ins></w:p></w:tc>")
    trpr = re.search(r"<w:trPr>.*?</w:trPr>", row, re.S)
    trpr = trpr.group(0).replace("</w:trPr>", f"<w:ins {_attrs()}/></w:trPr>") if trpr else f"<w:trPr><w:ins {_attrs()}/></w:trPr>"
    new_row = f"<w:tr>{trpr}{''.join(new_tcs)}</w:tr>"
    return x[:e] + new_row + x[e:]
