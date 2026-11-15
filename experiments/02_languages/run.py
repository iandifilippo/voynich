"""Where does Voynichese sit among 294 Wikipedia languages and 18 historical texts?

Only glyph-level and word-level statistics are compared (no line effects:
plain texts have no real lines). Every text is cut to the same length.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, metrics, historical, wikipedia, list_historical, list_wikipedia

HERE = pathlib.Path(__file__).parent
N = 10000
KEYS = ["h1", "h2", "word_len", "word_len_sd", "hapax_ratio", "zipf"]


def prof(words):
    words = words[:N]
    _, h1, h2 = metrics.char_entropies(words)
    lens = [len(w) for w in words]
    m = sum(lens) / len(lens)
    from collections import Counter
    c = Counter(words)
    return {"h1": h1, "h2": h2, "word_len": m,
            "word_len_sd": (sum((x - m) ** 2 for x in lens) / len(lens)) ** .5,
            "hapax_ratio": sum(1 for x in c.values() if x == 1) / len(c),
            "zipf": metrics.zipf_slope(words)}


rows = []
for t in ["ZL", "GC", "CD"]:
    rows.append({"text": "VMS " + t, "kind": "voynich", **prof(Voynich(t).words(unit="P"))})
for n in list_historical():
    w = historical(n, N)
    if len(w) >= 3000:
        rows.append({"text": n, "kind": "historical", **prof(w)})
for n in list_wikipedia():
    w = wikipedia(n, N)
    if len(w) >= 3000:
        rows.append({"text": n, "kind": "wikipedia", **prof(w)})

# scripts with combining vowel signs (Brahmic, Thaana, Hebrew with points...) get
# chopped into 1-glyph "words" by the \w regex; their h2 is an artifact
for r in rows:
    r["tokenization_ok"] = r["word_len"] >= 2.0
others = [r for r in rows if r["kind"] != "voynich" and r["tokenization_ok"]]
dropped = [r["text"] for r in rows if not r["tokenization_ok"]]
sd = {k: (sum((r[k] - sum(x[k] for x in others) / len(others)) ** 2 for r in others) / len(others)) ** .5 for k in KEYS}


def dist(a, b, keys):
    return math.sqrt(sum(((a[k] - b[k]) / sd[k]) ** 2 for k in keys) / len(keys))


vms = rows[0]
for r in others:
    r["dist_all"] = dist(r, vms, KEYS)
    r["dist_h"] = dist(r, vms, ["h1", "h2"])
near = sorted(others, key=lambda r: r["dist_all"])[:15]
near_h = sorted(others, key=lambda r: r["dist_h"])[:15]
low_h2 = sorted(others, key=lambda r: r["h2"])[:15]
below = sum(r["h2"] <= vms["h2"] for r in others)

save(HERE, "languages", {"n_texts": len(others), "rows": rows, "below_vms_h2": below, "dropped": dropped})
cols = ["text", "kind", "h1", "h2", "word_len", "hapax_ratio", "zipf"]
md = f"# 02 languages\n\n{len(others)} comparison texts, first {N} words each.\n\n"
md += f"Texts with h2 at or below VMS (ZL, {vms['h2']:.2f}): **{below}**\n\n"
md += f"Dropped {len(dropped)} texts whose script the tokenizer breaks into 1-glyph words (mean word length < 2): " + ", ".join(dropped) + "\n\n"
md += "## the VMS rows\n\n" + table(rows[:3], cols)
md += "\n## lowest h2 among natural texts\n\n" + table(low_h2, cols)
md += "\n## nearest on all six metrics\n\n" + table(near, cols + ["dist_all"])
md += "\n## nearest on h1/h2 only\n\n" + table(near_h, cols + ["dist_h"])
write_md(HERE, "languages", md)
print(md)
