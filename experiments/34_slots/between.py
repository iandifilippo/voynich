"""If words carry no lexicon, where is the message? Maybe between them.

In a cipher that writes one or two letters per word (the Naibbe family) the
words themselves are near-arbitrary, but the next word depends on the last
the way the next letter of a language depends on the last. So: what does
knowing the previous word save on a held-out word? Against the same text with
words shuffled (should save nothing), a Naibbe cipher of Latin, and real
languages read word by word and letter by letter.

Words are also reduced to their last sign and their first sign, since rare
words make the whole-word table sparse: does the end of one word predict the
start of the next?

The whole-word table is sparse at this size and the smoothing charges for it
(shuffled text comes out below zero), so the number to read is the
difference from the shuffled text.
"""
import json
import math
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA, historical

HERE = pathlib.Path(__file__).parent
N = 11000
UNIT = re.compile(r"c[tkpf]h|ch|sh|eee|ee|iii|ii|.")


def gain(lines, key_prev=lambda w: w, key_next=lambda w: w, folds=5):
    """Held-out bits saved on key_next(word) by knowing key_prev(previous word)."""
    saved = n = 0
    for f in range(folds):
        uni, bi = Counter(), defaultdict(Counter)
        test = []
        for k, l in enumerate(lines):
            if k % folds == f:
                test.append(l)
                continue
            for a, b in zip(l, l[1:]):
                uni[key_next(b)] += 1
                bi[key_prev(a)][key_next(b)] += 1
        tot, types = sum(uni.values()), len(uni)
        for l in test:
            for a, b in zip(l, l[1:]):
                x = key_next(b)
                p1 = (uni[x] + 0.5) / (tot + 0.5 * (types + 1))
                c = bi.get(key_prev(a))
                p2 = (c[x] + len(c) * p1) / (sum(c.values()) + len(c)) if c else p1
                saved += math.log2(p2 / p1)
                n += 1
    return saved / n


def chunks(words, size=8):
    return [words[i:i + size] for i in range(0, len(words), size)]


def cap(lines):
    out, n = [], 0
    for l in lines:
        if n >= N:
            break
        out.append(l)
        n += len(l)
    return out


chart = {k: set(x) for k, x in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
v = Voynich("ZL")
body = [l for l in v.lines if l.unit == "P"]
first, last = (lambda w: UNIT.findall(w)[0]), (lambda w: UNIT.findall(w)[-1])
texts = [("VMS, Currier A", [l.words for l in body if l.meta.get("L") == "A"], first, last),
         ("VMS, Currier B", [l.words for l in body if l.meta.get("L") == "B"], first, last),
         ("copying model", AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5, common_p=0.5).run(4500),
          first, last)]
src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
if src.exists():
    texts.append(("Naibbe cipher of Pliny", chunks(open(src, encoding="utf-8-sig").read().split()), first, last))
for name in ("Secreta_Secretorum_LAT", "Rettorica", "Cirurgie", "Hebrew_Mishneh"):
    w = historical(name)
    texts.append((name + ", words", chunks(w), lambda x: x[0], lambda x: x[-1]))
    texts.append((name + ", letters as words", chunks(list("".join(w))), lambda x: x, lambda x: x))

rng = random.Random(0)
rows = []
for name, lines, fst, lst in texts:
    lines = cap([[w for w in l if w and "?" not in w] for l in lines])
    lines = [l for l in lines if len(l) > 1]
    flat = [w for l in lines for w in l]
    rng.shuffle(flat)
    it = iter(flat)
    shuf = [[next(it) for _ in l] for l in lines]
    g, g0 = gain(lines), gain(shuf)
    rows.append({"text": name, "previous word -> word": g, "same, words shuffled": g0, "above shuffled": g - g0,
                 "last sign -> first sign of next": gain(lines, lst, fst),
                 "same, shuffled": gain(shuf, lst, fst),
                 "previous word -> first sign of next": gain(lines, lambda w: w, fst)})
    print(rows[-1], flush=True)

save(HERE, "between", rows)
md = "# 34 between words\n\nHeld-out bits saved per word.\n\n" + table(
    rows, ["text", "previous word -> word", "same, words shuffled", "above shuffled", "last sign -> first sign of next", "same, shuffled",
           "previous word -> first sign of next"])
write_md(HERE, "between", md)
print(md)
