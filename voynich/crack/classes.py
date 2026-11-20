"""Word classes that make neighbouring words most predictable of each other.

If every word of a cipher stands for a letter (or a letter in context), the
words that stand for the same letter behave alike towards their neighbours,
and grouping them recovers the alphabet: classes whose sequence has the
letter statistics of the plaintext. Exchange clustering finds the K classes
that maximise the mutual information between adjacent words' classes.
"""
import ctypes
import math
import pathlib
import subprocess
from collections import Counter

import numpy as np

HERE = pathlib.Path(__file__).parent
_cache = []


def _lib():
    if _cache:
        return _cache[0]
    so, src = HERE / "_classes.so", HERE / "classes.c"
    if not so.exists() or so.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["gcc", "-O3", "-shared", "-fPIC", "-o", str(so), str(src), "-lm"], check=True)
    lib = ctypes.CDLL(str(so))
    ip = np.ctypeslib.ndpointer(np.int32, flags="C")
    lib.exchange.restype = ctypes.c_double
    lib.exchange.argtypes = [ip, ctypes.c_int, ctypes.c_int, ctypes.c_int, ip, ctypes.c_int]
    _cache.append(lib)
    return lib


def encode(lines, vocab=None):
    """lines of tokens -> id stream with -1 between lines, and the vocabulary."""
    if vocab is None:
        vocab = {w: i for i, w in enumerate(sorted({w for l in lines for w in l}))}
    seq = []
    for l in lines:
        seq += [vocab.get(w, -1) for w in l] + [-1]
    return np.array(seq, dtype=np.int32), vocab


def fit(lines, K, passes=50, starts=3, seed=0):
    """Returns (mi in bits per bigram, {word: class})."""
    seq, vocab = encode(lines)
    V = len(vocab)
    freq = Counter(w for l in lines for w in l)
    rng = np.random.default_rng(seed)
    best = None
    for s in range(starts):
        cls = np.ascontiguousarray(rng.integers(0, K, V), dtype=np.int32)
        if s == 0:
            ranked = sorted(vocab, key=lambda w: -freq[w])
            for r, w in enumerate(ranked):
                cls[vocab[w]] = r % K
        mi = _lib().exchange(seq, len(seq), V, K, cls, passes)
        if best is None or mi > best[0]:
            best = (mi, cls.copy())
    inv = {i: w for w, i in vocab.items()}
    return best[0] / math.log(2), {inv[i]: int(c) for i, c in enumerate(best[1])}


def class_mi(lines, assign, unknown=None):
    """MI (bits) between classes of adjacent tokens in other text, under a
    fixed assignment; tokens without a class break the chain unless
    `unknown` gives them a class of their own."""
    N = Counter()
    for l in lines:
        cs = [assign.get(w, unknown) for w in l]
        for a, b in zip(cs, cs[1:]):
            if a is not None and b is not None:
                N[a, b] += 1
    tot = sum(N.values())
    if not tot:
        return 0.0
    L, R = Counter(), Counter()
    for (a, b), c in N.items():
        L[a] += c
        R[b] += c
    return sum(c / tot * math.log2(c * tot / (L[a] * R[b])) for (a, b), c in N.items())
