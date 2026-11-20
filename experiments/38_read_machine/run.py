"""Read the machine.

Exp. 37 found that a machine with a few dozen states writes Voynich words as
well as a two-sign chain does. A small one is easier to read: here a 12-state
machine is fitted to all of Currier B (best of 6 starts), and for each state
it lists what it writes and where it goes next, and draws it.

Then a check against what the machine is supposed to be. If a state is a
"position" in the word, its signs should come from one or two of Zattera's
slots (exp. 34) and it should rarely loop back to itself. For each state:
the share of its emissions that fall in its most common slot, and its
self-transition.
"""
import json
import pathlib
import subprocess
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "34_slots"))
from _common import save, table, write_md
from voynich import Voynich
from voynich.assemble import signs
from voynich.crack import hmm

HERE = pathlib.Path(__file__).parent
K = 12
LANG = sys.argv[1] if len(sys.argv) > 1 else "B"

v = Voynich("ZL")
lines = [[signs(w) for w in l.words if "?" not in w and "'" not in w]
         for l in v.lines if l.unit == "P" and l.meta.get("L") == LANG]
symbols = sorted({s for l in lines for w in l for s in w}) + ["$"]
index = {s: i for i, s in enumerate(symbols)}
obs = []
for l in lines:
    for w in l:
        obs += [index[s] for s in w] + [index["$"]]
    obs.append(-1)
obs = np.array(obs, dtype=np.int32)
A0 = np.full((K, K), 1.0 / K)
pi = np.full(K, 1.0 / K)
ll, B, A = hmm.fit(obs, len(symbols), A0, pi, iters=400, restarts=6, learn_A=True, seed=7)

# state occupancy from the emission-weighted stationary distribution
w, vecs = np.linalg.eig(A.T)
stat = np.real(vecs[:, np.argmin(abs(w - 1))])
stat = stat / stat.sum()

# Zattera's slots, as reconstructed in exp. 34, by sign
SLOTS = [("q", "s", "d"), ("y", "o"), ("l", "r"), ("t", "k", "p", "f"), ("ch", "sh"),
         ("cth", "ckh", "cph", "cfh"), ("eee", "ee", "e"), ("s", "d"), ("o", "a"),
         ("iii", "ii", "i"), ("d", "l", "r", "m", "n"), ("y",)]
slot_of = defaultdict(set)
for k, g in enumerate(SLOTS):
    for s in g:
        slot_of[s].add(k)

order = list(np.argsort(-stat))
name = {int(s): f"S{n + 1}" for n, s in enumerate(order)}
rows = []
for s in order:
    em = sorted(((B[s, i], symbols[i]) for i in range(len(symbols))), reverse=True)
    top = [(p, x) for p, x in em if p >= 0.05][:6]
    slots = Counter()
    for p, x in em:
        for k in slot_of.get(x, ()):
            slots[k] += p / len(slot_of[x])
    best_slot, share = slots.most_common(1)[0] if slots else (None, 0)
    nxt = sorted(((A[s, j], name[int(j)]) for j in range(K)), reverse=True)
    rows.append({"state": name[int(s)], "time spent": float(stat[s]),
                 "writes": ", ".join(f"{x} {p:.2f}" for p, x in top),
                 "next": ", ".join(f"{n} {p:.2f}" for p, n in nxt if p >= 0.1),
                 "stays": float(A[s, s]),
                 "main slot": f"{best_slot + 1}: {'/'.join(SLOTS[best_slot])}" if best_slot is not None else "-",
                 "share in main slot": float(share),
                 "writes the space": float(B[s, index['$']])})

dot = ["digraph M {", "rankdir=LR; node [shape=box, fontname=monospace, fontsize=10];"]
for r in rows:
    label = r["state"] + "\\n" + "\\n".join(x for x in r["writes"].split(", ")[:4])
    dot.append(f'{r["state"]} [label="{label}"];')
for s in order:
    for j in range(K):
        if A[s, j] >= 0.15:
            dot.append(f'{name[int(s)]} -> {name[int(j)]} [label="{A[s, j]:.2f}", penwidth={1 + 4 * A[s, j]:.1f}];')
dot.append("}")
(HERE / "results").mkdir(exist_ok=True)
(HERE / "results" / f"machine_{LANG}.dot").write_text("\n".join(dot))
subprocess.run(["dot", "-Tsvg", str(HERE / "results" / f"machine_{LANG}.dot"), "-o",
                str(HERE / "results" / f"machine_{LANG}.svg")], check=True)
save(HERE, f"machine_{LANG}", {"loglik": ll, "symbols": symbols, "rows": rows, "A": A.tolist(), "B": B.tolist()})
md = f"# 38 a {K}-state machine for Currier {LANG}\n\n![machine](machine_{LANG}.svg)\n\n" + table(
    rows, ["state", "time spent", "writes", "next", "stays", "writes the space", "main slot", "share in main slot"])
write_md(HERE, f"machine_{LANG}", md)
print(md)
