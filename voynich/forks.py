"""A page's fork choices: how its words start, which gallows they carry, how
they end (exps. 39-40)."""
from collections import Counter

import numpy as np

STARTS = ("qo", "q", "ch", "sh", "o", "d", "y", "s", "a")
ENDS = ("edy", "eedy", "dy", "ey", "y", "aiin", "ain", "iin", "in", "al", "ol", "ar", "or", "l", "r", "m", "s", "o")
FEATS = [("start", s) for s in STARTS + ("other",)] + \
        [("gallows", g) for g in ("t", "k", "p", "f", "none")] + \
        [("end", e) for e in ENDS + ("other",)]


def start(w):
    return next((p for p in STARTS if w.startswith(p)), "other")


def end(w):
    return next((e for e in ENDS if w.endswith(e)), "other")


def profile(words):
    c = Counter()
    for w in words:
        c[("start", start(w))] += 1
        c[("gallows", next((x for x in w if x in "tkpf"), "none"))] += 1
        c[("end", end(w))] += 1
    n = max(len(words), 1)
    return np.array([c[f] / n for f in FEATS])
