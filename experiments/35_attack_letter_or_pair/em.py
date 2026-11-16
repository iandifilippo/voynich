"""The textbook method for homophonic ciphers, tried first: EM over an HMM
whose hidden states are letters with Latin's transition table (Knight et al.
2006). Given the true cuts of the Naibbe text it still fails, and the reason
is visible: the true key has a lower likelihood than what EM finds. With 400
symbols and only letter pairs to go on, the model is free to use the letters
as arbitrary clusters. The annealer with four-letter context does not have
that freedom."""
import csv
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import run  # noqa: E402
from _common import save  # noqa: E402
from voynich.crack import hmm  # noqa: E402

HERE = pathlib.Path(__file__).parent
L = "abcdefghilmnopqrstuvxyz"
uni, pre, suf = {}, {}, {}
for code, g in list(csv.reader(open(run.NB / "references" / "naibbe_tables.csv", encoding="utf-8-sig")))[1:]:
    kind, _, let = code.split("_")
    {"unigram": uni, "prefix": pre, "suffix": suf}[kind].setdefault(g, let)
seq = []
for w in run.TEXTS["Naibbe cipher of Pliny"]:
    if w in uni:
        seq.append(("W:" + w, uni[w]))
        continue
    for i in range(1, len(w)):
        if w[:i] in pre and w[i:] in suf:
            seq += [("F:" + w[:i], pre[w[:i]]), ("S:" + w[i:], suf[w[i:]])]
            break
vocab = {s: i for i, s in enumerate(sorted({s for s, _ in seq}))}
obs = np.array([vocab[s] for s, _ in seq], dtype=np.int32)
true = np.array([L.index(l) for _, l in seq])
latin = "".join(run.corpus("Latin")).replace("j", "i").replace("k", "c").replace("w", "uu")
A, pi = hmm.bigram_table(latin, L)
V = len(vocab)
ll, B, _ = hmm.fit(obs, V, A, pi, iters=150, restarts=5)
Bt = np.full((len(L), V), 0.01)
np.add.at(Bt, (true, obs), 1)
Bt /= Bt.sum(1, keepdims=True)
out = {"symbols": V, "letters right": float((hmm.read(B, pi)[obs] == true).mean()),
       "log-likelihood per symbol, EM": ll / len(obs),
       "log-likelihood per symbol, true key": hmm.loglik(obs, V, A, pi, Bt) / len(obs)}
save(HERE, "em", out)
print(out)
