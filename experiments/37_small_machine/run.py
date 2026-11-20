"""How small can the word rule be?

Exp. 36 matched the manuscript with a sign chain looking two signs back:
thousands of parameters, no procedure anyone would have used. A scribe with a
table, a volvelle or a habit would be following a machine with a handful of
states: in state s, write one of a few signs, then move to the next state.

Here that machine is fitted directly. A hidden Markov model whose hidden
states are the machine's states, whose emissions are EVA signs plus the word
space "$", trained by EM on the training half of Currier B (even pages),
K = 2 ... 20 states. For each K:
  - held-out bits per sign on the odd pages (does a bigger table keep helping?)
  - generate as many words as the held-out half and measure them the way
    exp. 36 did: vocabulary size, one-off words, share of words never seen in
    the training half, top words, lexicon gain, word length, q- words.

The same is done on a Latin and an Italian text, and on the two content-free
controls (the Naibbe cipher of Pliny and the copying model). If a small machine is enough
for Voynich words but not for words of a language, that is the difference
between a rule and a vocabulary, measured in states.
"""
import math
import pathlib
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.assemble import signs
from voynich.corpus import historical
from voynich.crack import hmm

HERE = pathlib.Path(__file__).parent
KS = [2, 4, 6, 8, 12, 16, 24, 32, 48]
RESTARTS, ITERS = 3, 250


def lexicon_gain(seqs, rng, folds=5, order=2):
    seqs = [tuple(s) + ("$",) for s in seqs]
    idx = list(range(len(seqs)))
    rng.shuffle(idx)
    alphabet = len({x for q in seqs for x in q})
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


def describe(words, train_vocab):
    w = ["".join(x) for x in words]
    c = Counter(w)
    n = len(w)
    return {"distinct per 1000": 1000 * len(c) / n,
            "hapax share": sum(1 for x in c.values() if x == 1) / len(c),
            "unseen in training": sum(1 for x in w if x not in train_vocab) / n,
            "top 20 share": sum(x for _, x in c.most_common(20)) / n,
            "lexicon gain": lexicon_gain(words, random.Random(0)),
            "mean length (signs)": sum(map(len, words)) / n}


def chain_bits(train, test, order):
    """Held-out bits per symbol of an interpolated sign chain over the same
    stream the machine sees (signs and word spaces, lines independent)."""
    def seqs(lines):
        for l in lines:
            yield [x for w in l for x in list(w) + ["$"]]
    tabs = [defaultdict(Counter) for _ in range(order + 1)]
    V = len({x for q in seqs(train + test) for x in q})
    for q in seqs(train):
        q = ["^"] * order + q
        for j in range(order, len(q)):
            for o in range(order + 1):
                tabs[o][tuple(q[j - o:j])][q[j]] += 1
    cost = n = 0
    for q in seqs(test):
        q = ["^"] * order + q
        for j in range(order, len(q)):
            c0 = tabs[0][()]
            p = (c0[q[j]] + 0.5) / (sum(c0.values()) + 0.5 * V)
            for o in range(1, order + 1):
                c = tabs[o].get(tuple(q[j - o:j]))
                if c:
                    p = (c[q[j]] + len(c) * p) / (sum(c.values()) + len(c))
            cost -= math.log2(p)
            n += 1
    return cost / n


def stream(lines, index):
    out = []
    for l in lines:
        for w in l:
            out += [index[s] for s in w] + [index["$"]]
        out.append(-1)
    return np.array(out, dtype=np.int32)


def plain_lines(name, n_words=24000, per_line=8):
    ws = []
    for w in historical(name):
        w = unicodedata.normalize("NFD", w.lower())
        w = re.sub(r"[^a-z]", "", "".join(ch for ch in w if not unicodedata.combining(ch)))
        if w:
            ws.append(list(w))
    ws = ws[:n_words]
    return [ws[i:i + per_line] for i in range(0, len(ws), per_line)]


def split_vms(lang):
    v = Voynich("ZL")
    pages = defaultdict(list)
    for l in v.lines:
        if l.unit == "P" and l.meta.get("L") == lang:
            ws = [signs(w) for w in l.words if "?" not in w and "'" not in w]
            if ws:
                pages[l.page].append(ws)
    order = list(pages)
    return ([l for p in order[0::2] for l in pages[p]], [l for p in order[1::2] for l in pages[p]])


def naibbe_lines(n_words=24000, per_line=8):
    from voynich.corpus import DATA
    ws = open(DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt",
              encoding="utf-8-sig").read().split()[:n_words]
    ws = [signs(w) for w in ws]
    return [ws[i:i + per_line] for i in range(0, len(ws), per_line)]


def copy_lines(n_lines=2700):
    import json
    from voynich.autocopy import AutoCopy
    chart = {k: set(x) for k, x in json.loads(
        (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
    lines = AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5, common_p=0.5).run(n_lines)
    return [[signs(w) for w in l] for l in lines if l]


def split_text(lines):
    return lines[0::2], lines[1::2]


def run(name, train, test):
    symbols = sorted({s for l in train + test for w in l for s in w}) + ["$"]
    index = {s: i for i, s in enumerate(symbols)}
    tr, te = stream(train, index), stream(test, index)
    vocab = {"".join(w) for l in train for w in l}
    test_words = [w for l in test for w in l]
    target = describe(test_words, vocab)
    rows = [{"text": name, "states": "held-out text", **target}]
    for o in (1, 2, 3):
        rows.append({"text": name, "states": f"sign chain, {o} back", "held-out bits per sign": chain_bits(train, test, o)})
    rng = np.random.default_rng(0)
    for K in KS:
        A = np.full((K, K), 1.0 / K)
        pi = np.full(K, 1.0 / K)
        ll, B, A = hmm.fit(tr, len(symbols), A, pi, iters=ITERS, restarts=RESTARTS, learn_A=True, seed=K)
        held = hmm.loglik(te, len(symbols), A, pi, B)
        n_signs = int((te >= 0).sum())
        gen = hmm.sample_words(A, pi, B, symbols, len(test_words), rng)
        row = {"text": name, "states": K, "held-out bits per sign": -held / n_signs / math.log(2),
               **describe(gen, vocab)}
        rows.append(row)
        print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
    return rows


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    jobs = {"VMS Currier B": lambda: split_vms("B"), "VMS Currier A": lambda: split_vms("A"),
            "Latin (Secreta secretorum)": lambda: split_text(plain_lines("Secreta_Secretorum_LAT")),
            "Italian (Rettorica)": lambda: split_text(plain_lines("Rettorica")),
            "Naibbe cipher of Pliny": lambda: split_text(naibbe_lines()),
            "copying model": lambda: split_text(copy_lines())}
    for name, make in jobs.items():
        if which != "all" and which not in name:
            continue
        rows = run(name, *make())
        tag = re.sub(r"[^a-z]+", "_", name.lower()).strip("_")
        save(HERE, "machine_" + tag, rows)
        write_md(HERE, "machine_" + tag, f"# 37 small machine: {name}\n\n" + table(
            rows, ["states", "held-out bits per sign", "distinct per 1000", "hapax share", "unseen in training",
                   "top 20 share", "lexicon gain", "mean length (signs)"]))
