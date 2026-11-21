"""Spaces measured on the page instead of read by a transcriber.

Every result so far uses the transliteration's spaces, and exps. 46 and 53
found that some of the strongest effects sit at doubtful spaces ('or aiin'
is probably one word). Rozanova and Temerev's reproduction archive
(github.com/lrozanova/voynich-units, arXiv:2608.17096) includes per-word
bounding boxes for 223 folios, drawn on the page images (from
voynichese.com), with which they showed that ZL's uncertain spaces are
physically narrower.

Here the boxes are used to redraw word boundaries from the page itself and
re-ask two of the central questions:
  1. Is there still no lexicon (exp. 34) when words are defined by physical
     gaps? Boundaries whose boxes touch or nearly touch are closed, at
     several thresholds, and the lexicon gain is measured on the result,
     against the same number of boundaries closed at random.
  2. Does the coupling across the space (exp. 46: last sign of a word ->
     first sign of the next) live at narrow gaps (false spaces) or also at
     wide ones? MI by gap tertile, each with its own shuffle baseline.
Currier A and B apart (folio language from the ZL file).
"""
import glob
import json
import math
import pathlib
import random
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
BOXES = pathlib.Path("/home/claude/lrozanova/voynich-units/data/voynich-units/morphometry_voynichese/voynichese_boxes")
if not BOXES.exists():
    BOXES = HERE.parent.parent / "data" / "external" / "voynich-units-boxes"


def load_lines():
    """{folio: [[(word, gap_to_next or None), ...], ...]} in reading order."""
    out = {}
    for f in sorted(BOXES.glob("*.js")):
        d = json.loads(f.read_text())
        voc = [x[0] for x in d[0]]
        toks = d[1]
        mh = statistics.median([t[4] for t in toks]) or 1
        lines, cur, prev = [], [], None
        for t in toks:
            new_line = prev is None or t[1] < prev[1] - 3 or abs(t[2] - prev[2]) >= 0.8 * mh
            if new_line and cur:
                lines.append(cur)
                cur = []
            if cur:
                cur[-1] = (cur[-1][0], (t[1] - (prev[1] + prev[3])) / mh)
            cur.append((voc[t[0]], None))
            prev = t
        if cur:
            lines.append(cur)
        out[f.stem] = lines
    return out


def merged(lines, close):
    """close(gap) -> True joins the word to the next one."""
    out = []
    for l in lines:
        words, cur = [], ""
        for w, g in l:
            cur += w
            if g is None or not close(g):
                words.append(cur)
                cur = ""
        if cur:
            words.append(cur)
        out.append(words)
    return out


def lexicon_gain(words, rng, folds=5, order=2):
    seqs = [tuple(signs(w)) + ("$",) for w in words]
    idx = list(range(len(seqs)))
    rng.shuffle(idx)
    alphabet = len({s for q in seqs for s in q})
    a = b = 0.0
    for f in range(folds):
        tabs = [defaultdict(Counter) for _ in range(order + 1)]
        lex = Counter()
        for k, i in enumerate(idx):
            if k % folds == f:
                continue
            lex[seqs[i]] += 1
            q = ("^",) * order + seqs[i]
            for j in range(order, len(q)):
                for o in range(order + 1):
                    tabs[o][q[j - o:j]][q[j]] += 1
        n, t = sum(lex.values()), len(lex)
        for i in idx[f::folds]:
            q = ("^",) * order + seqs[i]
            lp = 0.0
            for j in range(order, len(q)):
                c0 = tabs[0][()]
                p = (c0[q[j]] + 0.5) / (sum(c0.values()) + 0.5 * alphabet)
                for o in range(1, order + 1):
                    c = tabs[o].get(q[j - o:j])
                    if c:
                        p = (c[q[j]] + len(c) * p) / (sum(c.values()) + len(c))
                lp += math.log2(p)
            a -= lp
            b -= math.log2((lex[seqs[i]] + t * 2 ** lp) / (n + t))
    return (a - b) / len(seqs)


def mi(pairs):
    N = Counter(pairs)
    tot = sum(N.values())
    L, R = Counter(), Counter()
    for (a, b), c in N.items():
        L[a] += c
        R[b] += c
    return sum(c / tot * math.log2(c * tot / (L[a] * R[b])) for (a, b), c in N.items())


def coupling(pairs, rng, shuffles=20):
    obs = mi(pairs)
    right = [b for _, b in pairs]
    base = 0
    for _ in range(shuffles):
        rng.shuffle(right)
        base += mi([(a, b) for (a, _), b in zip(pairs, right)])
    return obs - base / shuffles


if __name__ == "__main__":
    v = Voynich("ZL")
    lang = {p: v.pages[p].get("L") for p in v.pages}
    all_lines = load_lines()
    rng = random.Random(0)
    rows, crows = [], []
    for L in ("B", "A"):
        lines = [l for f, ls in all_lines.items() if lang.get(f) == L for l in ls]
        gaps = sorted(g for l in lines for _, g in l if g is not None)
        n_bound = len(gaps)
        for label, thr in (("as boxed", None), ("touching boxes joined (gap <= 0)", 0.0),
                           ("gap <= 0.125 joined", 0.125), ("gap <= 0.143 joined", 0.143)):
            if thr is None:
                text = merged(lines, lambda g: False)
                k = 0
            else:
                text = merged(lines, lambda g, t=thr: g <= t)
                k = sum(1 for g in gaps if g <= thr)
            words = [w for l in text for w in l]
            row = {"Currier": L, "spacing": label, "boundaries closed": k / n_bound, "words": len(words),
                   "distinct per 1000": 1000 * len(set(words)) / len(words),
                   "lexicon gain": lexicon_gain(words, random.Random(0))}
            if thr is not None:
                p = k / n_bound
                rand = merged(lines, lambda g: rng.random() < p)
                rw = [w for l in rand for w in l]
                row["lexicon gain, same number closed at random"] = lexicon_gain(rw, random.Random(0))
            rows.append(row)
            print({a: (round(b, 3) if isinstance(b, float) else b) for a, b in row.items()}, flush=True)
        # coupling by gap tertile
        bpairs = [(signs(w)[-1], signs(l[i + 1][0])[0], g) for l in lines for i, (w, g) in enumerate(l) if g is not None]
        t1, t2 = gaps[len(gaps) // 3], gaps[2 * len(gaps) // 3]
        for name, sel in (("narrowest third", lambda g: g <= t1), ("middle third", lambda g: t1 < g <= t2),
                          ("widest third", lambda g: g > t2)):
            ps = [(a, b) for a, b, g in bpairs if sel(g)]
            crows.append({"Currier": L, "gaps": name, "pairs": len(ps), "last sign -> next first sign (bits)": coupling(ps, rng)})
            print(crows[-1], flush=True)
    save(HERE, "spaces", {"lexicon": rows, "coupling": crows})
    md = "# 55 spaces from the page (word boxes from the Rozanova & Temerev archive)\n\n## Lexicon gain with physically defined words\n\n"
    md += table(rows, ["Currier", "spacing", "boundaries closed", "words", "distinct per 1000", "lexicon gain",
                       "lexicon gain, same number closed at random"])
    md += "\n## Coupling across the space, by physical gap\n\n" + table(
        crows, ["Currier", "gaps", "pairs", "last sign -> next first sign (bits)"])
    write_md(HERE, "spaces", md)
    print(md)
