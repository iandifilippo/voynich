import csv
import pathlib
from collections import Counter, defaultdict

from ivtff import load

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "ZL3b-n.txt"
OUT = ROOT / "results" / "zodiac_labels.csv"

# page -> (sign, month written in the margin). still need to check these against the scans
PAGES = {
    "f70v2": ("Pisces", "mars"),
    "f70v1": ("Aries dark", "abril"),
    "f71r":  ("Aries light", "abril"),
    "f71v":  ("Taurus light", "may"),
    "f72r1": ("Taurus dark", "may"),
    "f72r2": ("Gemini", "yony"),
    "f72r3": ("Cancer", "jollet"),
    "f72v3": ("Leo", "augst"),
    "f72v2": ("Virgo", "setembre"),
    "f72v1": ("Libra", "octembre"),
    "f73r":  ("Scorpio", "nouembre"),
    "f73v":  ("Sagittarius", "dezembre"),
}

lines, _ = load(DATA)
rows = []
n = defaultdict(int)
for l in lines:
    if l["section"] != "Z" or l["type"] == "P":
        continue
    sign, month = PAGES.get(l["page"], ("?", "?"))
    for w in l["words"]:
        n[l["page"]] += 1
        rows.append([l["page"], sign, month, l["locus"], l["type"], n[l["page"]], w])

OUT.parent.mkdir(exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["page", "sign", "month", "locus", "type", "order", "word"])
    w.writerows(rows)

counts = Counter(r[0] for r in rows)
for page, (sign, month) in PAGES.items():
    print(f"{page:6} {sign:13} {month:9} {counts[page]}")
print(len(rows), "->", OUT)
