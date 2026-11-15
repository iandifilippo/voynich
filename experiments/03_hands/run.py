"""Five scribes (Davis 2020), two 'languages' (Currier). How do they differ?

- vocabulary distance (Jensen-Shannon over word frequencies) between every pair of hands
- the words most characteristic of each hand (log-odds with a small prior)
- whether hand and Currier language are the same split or not
"""
import math
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.metrics import jsd

HERE = pathlib.Path(__file__).parent
v = Voynich("ZL")

hands = {h: Counter(v.words(hand=h)) for h in "12345"}
total = Counter(v.words())
N = sum(total.values())

pairs = []
for a in "12345":
    for b in "12345":
        if a < b:
            pairs.append({"a": "hand " + a, "b": "hand " + b, "jsd": jsd(hands[a], hands[b])})

# A/B split inside each hand
cross = Counter((l.hand, l.language) for l in v.lines for _ in l.words)
cross_rows = [{"hand": h, "A": cross[(h, "A")], "B": cross[(h, "B")]} for h in "12345"]


def log_odds(sub, rest, k=15, prior=0.5):
    ns, nr = sum(sub.values()), sum(rest.values())
    out = []
    for w, c in sub.items():
        if c < 8:
            continue
        r = rest.get(w, 0)
        lo = math.log((c + prior) / (ns - c + prior)) - math.log((r + prior) / (nr - r + prior))
        se = math.sqrt(1 / (c + prior) + 1 / (r + prior))
        out.append((w, c, r, lo / se))
    return sorted(out, key=lambda x: -x[3])[:k]


markers = {}
for h, c in hands.items():
    rest = total - c
    markers[h] = [{"word": w, "count": n, "elsewhere": r, "z": z} for w, n, r, z in log_odds(c, rest)]

# how much of each hand's vocabulary is shared with the others
shared = []
for h, c in hands.items():
    others = set().union(*[set(hands[o]) for o in hands if o != h])
    tok_shared = sum(n for w, n in c.items() if w in others) / sum(c.values())
    shared.append({"hand": h, "tokens": sum(c.values()), "types": len(c), "tokens_with_shared_word": tok_shared})

save(HERE, "hands", {"pairs": pairs, "cross": cross_rows, "markers": markers, "shared": shared})
md = "# 03 hands and Currier languages\n\n## vocabulary distance between hands (JSD, bits)\n\n"
md += table(sorted(pairs, key=lambda r: r["jsd"]), ["a", "b", "jsd"])
md += "\n## hand vs Currier language (tokens)\n\n" + table(cross_rows, ["hand", "A", "B"])
md += "\n## share of each hand's tokens that are words also used by another hand\n\n"
md += table(shared, ["hand", "tokens", "types", "tokens_with_shared_word"])
md += "\n## most characteristic words per hand (log-odds z)\n\n"
for h, m in markers.items():
    md += f"- hand {h}: " + ", ".join(f"{x['word']} ({x['count']}/{x['elsewhere']}, z={x['z']:.1f})" for x in m[:10]) + "\n"
write_md(HERE, "hands", md)
print(md)
