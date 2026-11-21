"""Apply tracked (w:del/w:ins) replacements to word/document.xml. Each old string must sit inside one <w:t>."""
import re, sys, json
from xml.sax.saxutils import escape

path, edits_json, author, date = sys.argv[1:5]
edits = json.load(open(edits_json, encoding="utf8"))
x = open(path, encoding="utf8").read()
nid = [900000]

def nxt():
    nid[0] += 1; return nid[0]

run_re = re.compile(r"<w:r(?: [^>]*)?>(?:(?!</w:r>).)*?</w:r>", re.S)
for old, new in edits:
    eo = escape(old)
    hits = [m for m in run_re.finditer(x) if re.search(r"<w:t(?: [^>]*)?>[^<]*" + re.escape(eo), m.group(0))]
    if len(hits) != 1:
        sys.exit(f"'{old}': {len(hits)} runs match")
    m = hits[0]; run = m.group(0)
    rpr = re.search(r"<w:rPr>.*?</w:rPr>", run, re.S); rpr = rpr.group(0) if rpr else ""
    tm = re.search(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", run)
    text = tm.group(1); i = text.index(eo)
    before, after = text[:i], text[i + len(eo):]
    pre, suf = run[:tm.start()], run[tm.end():]
    parts = pre + (f'<w:t xml:space="preserve">{before}</w:t>' if before else '') + '</w:r>'
    parts += f'<w:del w:id="{nxt()}" w:author="{author}" w:date="{date}"><w:r>{rpr}<w:delText xml:space="preserve">{eo}</w:delText></w:r></w:del>'
    if new:
        parts += f'<w:ins w:id="{nxt()}" w:author="{author}" w:date="{date}"><w:r>{rpr}<w:t xml:space="preserve">{escape(new)}</w:t></w:r></w:ins>'
    parts += f'<w:r>{rpr}' + (f'<w:t xml:space="preserve">{after}</w:t>' if after else '') + suf
    x = x[:m.start()] + parts + x[m.end():]
    print("ok:", old, "->", new)
open(path, "w", encoding="utf8").write(x)
