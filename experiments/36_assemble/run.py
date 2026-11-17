"""Assembled words against copied words, on held-out text.

Exp. 34 suggested that Voynich words are not copied from a stock of words but
built fresh by a short-sighted rule, with a little influence from the word
before. voynich/assemble.py is that idea as a generator. Here it is fitted on
half of Currier B (every other page) and asked to fill the other half: the
same pages, same number of lines, same words per line, same paragraph starts.
Everything is measured against the held-out half, which the generator never
saw.

Competitors, all filling the same shape:
  assemble k      sign chain looking back k signs (1, 2, 3), linked to the previous word
  assemble 2, no link
  lexicon         words drawn from the training half's word frequencies (pure vocabulary, no rule)
  copying model   exp. 22's best (not fitted to text at all; its own line shapes)

Run with VMS_LANG=A and/or VMS_TRANS=IT (etc.) for the robustness checks;
the recall knobs stay as fitted on ZL Currier B.

Measures: vocabulary size and novelty (share of tokens never seen in the
training half), frequency profile, the exp. 34 lexicon gain, adjacent
repeats, word shape at line and paragraph edges, and rare-word locality (both
occurrences of a doubleton on the same page).
"""
import json
import math
import os
import pathlib
import random
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, benchmark
from voynich.assemble import Assembler, signs
from voynich.autocopy import AutoCopy

HERE = pathlib.Path(__file__).parent
TRANS = os.environ.get("VMS_TRANS", "ZL")
LANG = os.environ.get("VMS_LANG", "B")
TAG = "" if (TRANS, LANG) == ("ZL", "B") else f"_{TRANS}_{LANG}"
SEEDS = [1, 2, 3]
chart = {k: set(x) for k, x in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}


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


def edit1(a, b):
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


def measure(pages, train_vocab):
    """pages: list of pages, each a list of (words, para_start)."""
    lines = [(l, ps) for p in pages for l, ps in p]
    words = [w for l, _ in lines for w in l]
    c = Counter(words)
    n = len(words)
    adj = [(a, b) for l, _ in lines for a, b in zip(l, l[1:])]
    first = [l[0] for l, ps in lines if l and not ps]
    pfirst = [l[0] for l, ps in lines if l and ps]
    last = [l[-1] for l, _ in lines if len(l) > 1]
    where = defaultdict(list)
    for k, p in enumerate(pages):
        for l, _ in p:
            for w in l:
                where[w].append(k)
    dbl = [x for w, x in where.items() if len(x) == 2]
    return {
        "words": n,
        "distinct per 1000 words": 1000 * len(c) / n,
        "hapax share of types": sum(1 for x in c.values() if x == 1) / len(c),
        "tokens unseen in training half": sum(1 for w in words if w not in train_vocab) / n,
        "top word share": c.most_common(1)[0][1] / n,
        "top 20 share": sum(x for _, x in c.most_common(20)) / n,
        "lexicon gain (bits)": lexicon_gain(words, random.Random(0)),
        "adjacent exact repeats per 1000": 1000 * sum(a == b for a, b in adj) / len(adj),
        "adjacent near repeats per 1000": 1000 * sum(edit1(a, b) for a, b in adj) / len(adj),
        "mean word length": sum(map(len, words)) / n,
        "words starting q": sum(w.startswith("q") for w in words) / n,
        "line-first starting q": sum(w.startswith("q") for w in first) / len(first),
        "para-first starting p/t/k/f": sum(w[0] in "ptkf" for w in pfirst) / max(1, len(pfirst)),
        "line-last ending m": sum(w.endswith("m") for w in last) / len(last),
        "doubletons on one page": sum(x[0] == x[1] for x in dbl) / max(1, len(dbl)),
    }


v = Voynich(TRANS)
pages = defaultdict(list)
for l in v.lines:
    if l.unit == "P" and l.meta.get("L") == LANG:
        words = [w for w in l.words if "?" not in w and "'" not in w]
        if words:
            pages[l.page].append((words, l.para_start))
order = list(pages)
train = [pages[p] for p in order[0::2]]
test = [pages[p] for p in order[1::2]]
tr_lines = [l for p in train for l, _ in p]
tr_starts = [k for k, (l, ps) in enumerate([x for p in train for x in p]) if ps]
vocab = Counter(w for l in tr_lines for w in l)
shape = [[(len(l), ps) for l, ps in p] for p in test]


def fill_assemble(seed, k, link=True):
    m = Assembler(order=k, link=link).fit(tr_lines, tr_starts)
    out = []
    for p in shape:
        filled = m.fill(p, seed=seed * 1000 + len(out))
        out.append(list(zip(filled, [ps for _, ps in p])))
    return out


def fill_lexicon(seed):
    rng = random.Random(seed)
    ws, cs = zip(*vocab.items())
    return [[(rng.choices(ws, cs, k=n), ps) for n, ps in p] for p in shape]


def fill_copy(seed):
    n_lines = sum(len(p) for p in shape)
    g = AutoCopy(seed=seed, currier=LANG, boundary=chart, boundary_p=0.65, line_end_p=0.5, common_p=0.5)
    lines = g.run(n_lines)
    starts = set(g.paragraph_starts)
    rows = [(l, k in starts) for k, l in enumerate(lines) if l]
    return [rows[i:i + 29] for i in range(0, len(rows), 29)]


def fill_recall(seed, p, e, window):
    m = Assembler(order=2, recall_p=p, edit_p=e, window=window).fit(tr_lines, tr_starts)
    return [list(zip(m.fill(pg, seed=seed * 1000 + i), [ps for _, ps in pg])) for i, pg in enumerate(shape)]


if __name__ == "__main__":
    TUNED = json.loads((HERE / "results" / "tune.json").read_text())["best"] if (HERE / "results" / "tune.json").exists() else None
    models = {"held-out VMS (target)": lambda s: test,
              "assemble 1": lambda s: fill_assemble(s, 1),
              "assemble 2": lambda s: fill_assemble(s, 2),
              "assemble 3": lambda s: fill_assemble(s, 3),
              "assemble 2, no link": lambda s: fill_assemble(s, 2, link=False),
              "lexicon": fill_lexicon,
              **({f"assemble 2 + recall (exact {TUNED['p']}, edited {TUNED['edit']}, last {TUNED['window']})":
                  (lambda s: fill_recall(s, TUNED["p"], TUNED["edit"], TUNED["window"]))} if TUNED else {}),
              "copying model": fill_copy}
    rows = []
    for name, make in models.items():
        runs = [measure(make(s), vocab) for s in (SEEDS[:1] if name.startswith("held") else SEEDS)]
        row = {"model": name}
        for k in runs[0]:
            row[k] = statistics.mean(r[k] for r in runs)
        pg = make(SEEDS[0])
        row["benchmark distance"] = benchmark.score([l for p in pg for l, _ in p])[0]
        rows.append(row)
        print(name, {k: round(x, 3) for k, x in row.items() if k != "model"}, flush=True)

    target = rows[0]
    keys = [k for k in rows[0] if k not in ("model", "words")]
    off = []
    for r in rows[1:]:
        rel = {}
        for k in keys:
            t = target[k]
            rel[k] = r[k] / t if t else float("nan")
        r["measures within 0.8-1.25x"] = sum(1 for k in keys if k != "benchmark distance" and 0.8 <= rel[k] <= 1.25)
    save(HERE, "assemble" + TAG, rows)
    cols = ["model", "distinct per 1000 words", "hapax share of types", "tokens unseen in training half",
            "top word share", "top 20 share", "lexicon gain (bits)"]
    cols2 = ["model", "adjacent exact repeats per 1000", "adjacent near repeats per 1000", "mean word length",
             "words starting q", "line-first starting q", "para-first starting p/t/k/f", "line-last ending m",
             "doubletons on one page", "benchmark distance", "measures within 0.8-1.25x"]
    md = f"# 36 assembled vs copied words, on held-out Currier {LANG} ({TRANS})\n\nFitted on even pages, measured on odd pages (3 seeds). Recall knobs as fitted on ZL Currier B.\n\n"
    md += "## Vocabulary\n\n" + table(rows, cols) + "\n## Sequence and edges\n\n" + table(rows, cols2)
    write_md(HERE, "assemble" + TAG, md)
    print(md)
