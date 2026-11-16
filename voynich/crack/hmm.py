"""Homophonic decipherment by EM: letters are hidden states with the
transition table of a known language, symbols are what they emit, and only
the emission table is learned (Knight et al. 2006)."""
import ctypes
import pathlib
import subprocess

import numpy as np

HERE = pathlib.Path(__file__).parent
_cache = []


def _lib():
    if _cache:
        return _cache[0]
    so, src = HERE / "_hmm.so", HERE / "hmm.c"
    if not so.exists() or so.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["gcc", "-O3", "-march=native", "-shared", "-fPIC", "-o", str(so), str(src), "-lm"], check=True)
    lib = ctypes.CDLL(str(so))
    ip = np.ctypeslib.ndpointer(np.int32, flags="C")
    dp = np.ctypeslib.ndpointer(np.float64, flags="C")
    lib.em.restype = ctypes.c_double
    lib.em.argtypes = [ip, ctypes.c_int, ctypes.c_int, ctypes.c_int, dp, dp, dp, ctypes.c_int, ctypes.c_int,
                       ctypes.c_double]
    lib.loglik.restype = ctypes.c_double
    lib.loglik.argtypes = [ip, ctypes.c_int, ctypes.c_int, ctypes.c_int, dp, dp, dp]
    _cache.append(lib)
    return lib


def bigram_table(text, letters, k=0.5):
    """Transition table and letter frequencies of a text, spaces ignored."""
    ix = {c: i for i, c in enumerate(letters)}
    seq = [ix[c] for c in text if c in ix]
    K = len(letters)
    A = np.full((K, K), k)
    for a, b in zip(seq, seq[1:]):
        A[a, b] += 1
    pi = A.sum(1) / A.sum()
    return A / A.sum(1, keepdims=True), pi


def fit(obs, V, A, pi, iters=150, restarts=10, learn_A=False, seed=0, smooth=0.01, sharp=1.0):
    """Best of several random starts. Returns (loglik, B, A)."""
    lib = _lib()
    obs = np.ascontiguousarray(obs, dtype=np.int32)
    K = len(pi)
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(restarts):
        B = rng.gamma(sharp, size=(K, V)) + 1e-6
        B /= B.sum(1, keepdims=True)
        A2 = np.ascontiguousarray(A, dtype=np.float64).copy()
        if learn_A:
            A2 = rng.gamma(1.0, size=(K, K)) + 0.1
            A2 /= A2.sum(1, keepdims=True)
        B = np.ascontiguousarray(B)
        pi2 = np.ascontiguousarray(pi, dtype=np.float64)
        ll = lib.em(obs, len(obs), V, K, A2, pi2, B, iters, int(learn_A), smooth)
        if best is None or ll > best[0]:
            best = (ll, B.copy(), A2.copy())
    return best


def loglik(obs, V, A, pi, B):
    obs = np.ascontiguousarray(obs, dtype=np.int32)
    return _lib().loglik(obs, len(obs), V, len(pi), np.ascontiguousarray(A, dtype=np.float64),
                         np.ascontiguousarray(pi, dtype=np.float64), np.ascontiguousarray(B, dtype=np.float64))


def read(B, pi):
    """Most likely letter for each symbol."""
    return (B * np.asarray(pi)[:, None]).argmax(0)
