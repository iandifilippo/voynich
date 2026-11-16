"""Rozanova & Temerev (arXiv:2608.17096): uncertain spaces (',' in ZL) behave
like word-internal breaks, not like real spaces. Two text-only checks:

1. Joining test: glue the two pieces on each side of a separator. How often is
   the result a word that occurs elsewhere in the manuscript as one token?
   Do it for ',' and for '.', and for random splits of real words as a
   reference for "really one word".
2. Edge coupling: mutual information between the glyph before and the glyph
   after the separator, for ',', '.', and adjacent glyphs inside words.
"""
import math
import pathlib
import random
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich.corpus import DATA
from voynich.metrics import mutual_info

HERE = pathlib.Path(__file__).parent

pairs = {".": [], ",": []}
vocab = Counter()
for raw in open(DATA / "ZL3b-n.txt", encoding="latin-1"):
    m = re.match(r"^<(f\d+[rv]\d?)\.(\d+),[+@=&~*]?P\w*>\s*(.*)$", raw.rstrip("\n"))
    if not m:
        continue
    t = m.group(3)
    t = re.sub(r"<![^>]*>", "", t)
    t = re.sub(r"\[([^:\]]*)[^\]]*\]", r"\1", t)
    t = re.sub(r"\{([^}]*)\}", r"\1", t)
    t = re.sub(r"<[^>]*>", ".", t).replace("'", "")
    toks = re.split(r"([.,])", t)
    pieces = [x for x in toks if x not in (".", ",")]
    seps = [x for x in toks if x in (".", ",")]
    for w in "".join(toks).replace(",", ".").split("."):
        pass
    for a, s, b in zip(pieces, seps, pieces[1:]):
        if a and b and "?" not in a + b and "*" not in a + b and "@" not in a + b:
            pairs[s].append((a, b))
    for w in re.split(r"[.,]", t):
        if w and not re.search(r"[?*@!]", w):
            vocab[w] += 1

rng = random.Random(0)
whole = [w for w, c in vocab.items() for _ in range(c) if len(w) >= 4]
splits = []
for _ in range(20000):
    w = rng.choice(whole)
    k = rng.randrange(1, len(w))
    splits.append((w[:k], w[k:]))


def join_rate(ps, min_count=2):
    ok = sum(vocab.get(a + b, 0) >= min_count for a, b in ps)
    return ok / len(ps) if ps else 0.0


def edge_mi(ps):
    return mutual_info((a[-1], b[0]) for a, b in ps)


inside = [(w[i - 1], w[i]) for w, c in vocab.items() for _ in range(c) for i in range(1, len(w))]
rows = []
for name, ps in (("certain space '.'", pairs["."]), ("uncertain space ','", pairs[","]),
                 ("random cut inside a word", splits)):
    rows.append({"boundary": name, "n": len(ps), "joins_into_known_word": join_rate(ps),
                 "edge_mi_bits": edge_mi(ps)})
rows.append({"boundary": "adjacent glyphs inside words", "n": len(inside), "joins_into_known_word": None,
             "edge_mi_bits": mutual_info(inside)})

# the comma pieces themselves: how often is each side a standalone word?
def standalone(ps):
    return sum(vocab.get(a, 0) >= 2 and vocab.get(b, 0) >= 2 for a, b in ps) / len(ps)


for r, ps in zip(rows[:3], (pairs["."], pairs[","], splits)):
    r["both_sides_known_words"] = standalone(ps)

# what share of commas would have to be word-internal to give the observed join rate,
# if the rest behaved like certain spaces
jd, jc, ji = rows[0]["joins_into_known_word"], rows[1]["joins_into_known_word"], rows[2]["joins_into_known_word"]
mix = (jc - jd) / (ji - jd)
save(HERE, "uncertain_spaces", {"rows": rows, "implied_internal_share": mix})
md = "# c02 uncertain spaces\n\n" + table(rows, ["boundary", "n", "joins_into_known_word", "both_sides_known_words", "edge_mi_bits"])
md += "\n`joins_into_known_word`: gluing the two sides gives a word seen 2+ times elsewhere. `both_sides_known_words`: each side is a word seen 2+ times on its own.\n"
md += f"\nIf uncertain spaces were a mix of real spaces (like '.') and word-internal cuts, the join rate implies about **{mix:.0%}** of them are word-internal.\n"
write_md(HERE, "uncertain_spaces", md)
print(md)
