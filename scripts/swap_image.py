"""Replace an embedded image (by relationship id) and rescale its frame height to the new aspect ratio.
Usage: python swap_image.py <unpacked_dir> <rId> <new_png> [target_width_px]"""
import re, sys
from PIL import Image
d, rid, png = sys.argv[1:4]; tw = int(sys.argv[4]) if len(sys.argv) > 4 else 4400
rels = open(f"{d}/word/_rels/document.xml.rels", encoding="utf8").read()
target = re.search(rf'Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1)
x = open(f"{d}/word/document.xml", encoding="utf8").read()
i = x.index(f'r:embed="{rid}"'); s = x.rfind("<w:drawing>", 0, i); e = x.index("</w:drawing>", i)
dr = x[s:e]; im = Image.open(png); w, h = im.size
cx = int(re.search(r'<wp:extent cx="(\d+)"', dr).group(1)); cy = round(cx * h / w)
dr = re.sub(r'(<wp:extent cx="\d+" cy=")\d+', rf"\g<1>{cy}", dr); dr = re.sub(r'(<a:ext cx="\d+" cy=")\d+', rf"\g<1>{cy}", dr)
open(f"{d}/word/document.xml", "w", encoding="utf8").write(x[:s] + dr + x[e:])
im.resize((tw, round(tw * h / w)), Image.LANCZOS).save(f"{d}/word/{target}", dpi=(600, 600))
print(rid, target, cx, cy)
