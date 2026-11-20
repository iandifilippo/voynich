"""Where in a word is the part that depends on the previous word?

Exp. 44: Currier B words carry sequence information (0.09 bits), much less
than any letter or syllable cipher of Latin would (0.28-0.69), and about as
much as a word-for-word codebook (0.13), which B can't be because its words
have no lexicon (exp. 34). One reading is left: each word carries a small
unit of information in one part of it, and the rest is filler made by the
slot machine. Then the sequence should live in that part.

For each word feature (first sign, first two signs, last sign, last two signs,
the gallows, the length in signs, the middle without first and last sign),
the mutual information between that feature in one word and each feature in
the next word of the same line, minus the same with words shuffled among words
at the same place in their line (first, inside, last), which keeps feature
frequencies and line-edge habits and removes order. Plug-in MI with
the shuffled baseline also removing most of the small-sample bias.

Run on Currier B and A, the Naibbe cipher (whose information sits in the
whole word, prefix and suffix), and the synthetic "one word per letter, 5
homophones" cipher from exp. 44.
"""
import math
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "44_word_classes"))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
SHUF = 10
FEATS = {
    "first sign": lambda s: s[0],
    "first 2": lambda s: tuple(s[:2]),
    "last sign": lambda s: s[-1],
    "last 2": lambda s: tuple(s[-2:]),
    "gallows": lambda s: next((x for x in s if x in ("t", "k", "p", "f", "cth", "ckh", "cph", "cfh")), "-"),
    "length": lambda s: min(len(s), 7),
    "middle": lambda s: tuple(s[1:-1]) if len(s) > 2 else ("-",),
}


def mi(pairs):
    N = Counter(pairs)
    tot = sum(N.values())
    L, R = Counter(), Counter()
    for (a, b), c in N.items():
        L[a] += c
        R[b] += c
    return sum(c / tot * math.log2(c * tot / (L[a] * R[b])) for (a, b), c in N.items())


def latin_free(w):
    """EVA words are split into signs; plain-language words into letters."""
    return EVA


EVA = True


def pos(i, n):
    return 0 if i == 0 else 2 if i == n - 1 else 1


def shuffle_by_position(seqs, rng):
    """Words shuffled among words at the same position class in their line
    (first, inside, last), so line-edge habits stay in the baseline."""
    groups = defaultdict(list)
    for li, l in enumerate(seqs):
        for i, w in enumerate(l):
            groups[pos(i, len(l))].append((li, i))
    out = [list(l) for l in seqs]
    for where in groups.values():
        ws = [seqs[a][b] for a, b in where]
        rng.shuffle(ws)
        for (a, b), w in zip(where, ws):
            out[a][b] = w
    return out


def table_for(lines, rng):
    seqs = [[signs(w) if latin_free(w) else list(w) for w in l] for l in lines]
    out = {}
    for fa, ga in FEATS.items():
        for fb, gb in FEATS.items():
            obs = mi([(ga(a), gb(b)) for l in seqs for a, b in zip(l, l[1:])])
            base = 0
            for _ in range(SHUF):
                ss = shuffle_by_position(seqs, rng)
                base += mi([(ga(a), gb(b)) for l in ss for a, b in zip(l, l[1:])])
            out[fa, fb] = obs - base / SHUF
    return out


def vms(lang):
    v = Voynich("ZL")
    return [[w for w in l.words if "?" not in w and "'" not in w] for l in v.lines
            if l.unit == "P" and l.meta.get("L") == lang]


import run as r44  # noqa: E402
import synthetic  # noqa: E402

nb = open(r44.DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt",
          encoding="utf-8-sig").read().split()[:23000]
syn = synthetic.homophone_cipher(list("".join(synthetic.latin))[:23000], random.Random(2),
                                 lambda c: round(5 * 23 * c / 100000) or 1)
texts = {"Currier B": vms("B"), "Currier A": vms("A"), "Naibbe cipher": r44.lines_of(nb),
         "one word per letter, 5 homophones": r44.lines_of(syn),
         "Latin (letters as signs)": r44.lines_of(synthetic.latin[:23000]),
         "Italian (letters as signs)": r44.lines_of(r44.plain(r44.historical("Rettorica"))[:23000])}
rng = random.Random(0)
rows, full = [], {}
for name, lines in texts.items():
    EVA = "letters as signs" not in name
    t = table_for(lines, rng)
    full[name] = {f"{a} -> {b}": x for (a, b), x in t.items()}
    row = {"text": name}
    for f in FEATS:
        row[f"{f} -> same"] = t[f, f]
    row["last sign -> first sign"] = t["last sign", "first sign"]
    row["last 2 -> first 2"] = t["last 2", "first 2"]
    best = max(t.items(), key=lambda kv: kv[1])
    row["strongest pair"] = f"{best[0][0]} -> {best[0][1]} ({best[1]:.3f})"
    rows.append(row)
    print(row, flush=True)
save(HERE, "where", {"rows": rows, "full": full})
cols = ["text"] + [f"{f} -> same" for f in FEATS] + ["last sign -> first sign", "last 2 -> first 2", "strongest pair"]
md = "# 46 where in the word the sequence lives\n\nMI (bits) between a feature of one word and a feature of the next, minus words shuffled within their line position class.\n\n"
md += table(rows, cols)
write_md(HERE, "where", md)
print(md)
