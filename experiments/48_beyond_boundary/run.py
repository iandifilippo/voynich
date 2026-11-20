"""Does anything pass from word to word except through the boundary?

Exp. 46: most of what links neighbouring Voynich words is the last sign of
one and the first sign of the next. A writer's habit at the boundary makes
that, with no message. A message makes something else: the choice made in
one word (its start, its gallows, its ending) tells you something about the
choices in the next word *beyond* what the boundary glyphs carry.

Conditional mutual information I(X_i ; Y_i+1 | last sign of word i, first
sign of word i+1): how much a feature X of a word predicts a feature Y of the
next once the two glyphs at the boundary are known. Bias-corrected by
permuting X among words that share the boundary context (last sign of word i
and first sign of word i+1), which keeps every boundary pair and breaks only
the link that goes around it.

Features: start of word (first two signs), gallows, ending (last two signs),
length. Texts: Currier A and B; the exp. 36 generator, whose words only see
the boundary; the one-key cipher of Latin made of Voynich words (exp. 44/47);
Latin and Italian (letters as signs).
"""
import math
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "44_word_classes"))
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
PERMS = 30
GAL = ("t", "k", "p", "f", "cth", "ckh", "cph", "cfh")
FEATS = {"start": lambda s: tuple(s[:2]), "gallows": lambda s: next((x for x in s if x in GAL), "-"),
         "ending": lambda s: tuple(s[-2:]), "length": lambda s: min(len(s), 6)}


def cmi(triples):
    """I(X;Y|Z) from (x, y, z) triples, plug-in, bits."""
    nz, nxz, nyz, nxyz = Counter(), Counter(), Counter(), Counter()
    for x, y, z in triples:
        nz[z] += 1
        nxz[x, z] += 1
        nyz[y, z] += 1
        nxyz[x, y, z] += 1
    n = len(triples)
    return sum(c / n * math.log2(c * nz[z] / (nxz[x, z] * nyz[y, z])) for (x, y, z), c in nxyz.items())


def run_text(lines, split, rng):
    seqs = [[split(w) for w in l] for l in lines]
    pairs = [(a, b) for l in seqs for a, b in zip(l, l[1:]) if a and b]
    out = {}
    for fx, gx in FEATS.items():
        for fy, gy in FEATS.items():
            trip = [(gx(a), gy(b), (a[-1], b[0])) for a, b in pairs]
            obs = cmi(trip)
            by_z = defaultdict(list)
            for k, (_, _, z) in enumerate(trip):
                by_z[z].append(k)
            base = 0
            for _ in range(PERMS):
                xs = [t[0] for t in trip]
                for idx in by_z.values():
                    vals = [xs[k] for k in idx]
                    rng.shuffle(vals)
                    for k, v in zip(idx, vals):
                        xs[k] = v
                base += cmi([(x, t[1], t[2]) for x, t in zip(xs, trip)])
            out[fx, fy] = obs - base / PERMS
    return out


import importlib.util  # noqa: E402

import synthetic  # noqa: E402  (loads exp. 44's run.py as "run")

_spec = importlib.util.spec_from_file_location("sheet_keys", HERE.parent / "47_sheet_keys" / "run.py")
r47 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r47)

rng = random.Random(0)
B, A = r47.B, r47.A
flat = lambda sheets: [l for s in sheets for l in s]  # noqa: E731
texts = {"Currier B": (flat(B), signs), "Currier A": (flat(A), signs),
         "generator, boundary habit only (exp. 36)": (flat(r47.generator_sheets(B, rng)), signs),
         "cipher of Latin, one key, Voynich words": (flat(r47.cipher_sheets(B, False, rng)), signs),
         "Latin (letters as signs)": (synthetic.run.lines_of(synthetic.latin[:20000]), list),
         "Italian (letters as signs)": (synthetic.run.lines_of(
             synthetic.run.plain(synthetic.run.historical("Rettorica"))[:20000]), list)}
rows, full = [], {}
for name, (lines, split) in texts.items():
    res = run_text(lines, split, rng)
    full[name] = {f"{a} -> {b}": x for (a, b), x in res.items()}
    row = {"text": name, "pairs": sum(max(0, len(l) - 1) for l in lines)}
    for f in FEATS:
        row[f"{f} -> {f}"] = res[f, f]
    row["sum of all 16"] = sum(res.values())
    rows.append(row)
    print({k: (round(x, 4) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
save(HERE, "beyond_boundary", {"rows": rows, "full": full})
md = ("# 48 links between neighbouring words beyond the boundary glyphs\n\nConditional MI (bits) given the last sign "
      "of the first word and the first sign of the second, minus a permutation baseline.\n\n")
md += table(rows, ["text", "pairs"] + [f"{f} -> {f}" for f in FEATS] + ["sum of all 16"])
write_md(HERE, "beyond_boundary", md)
print(md)
