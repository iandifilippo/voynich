"""Cipher solving: language models, a compiled annealer, and helpers to
turn a text into a symbol stream under a given hypothesis."""
import ctypes
import pathlib
import re
import subprocess
from collections import Counter

import numpy as np

HERE = pathlib.Path(__file__).parent
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def _lib():
    so = HERE / "_solver.so"
    src = HERE / "solver.c"
    if not so.exists() or so.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["gcc", "-O3", "-march=native", "-shared", "-fPIC", "-o", str(so), str(src), "-lm"], check=True)
    lib = ctypes.CDLL(str(so))
    ip = np.ctypeslib.ndpointer(np.int32, flags="C")
    bp = np.ctypeslib.ndpointer(np.int8, flags="C")
    fp = np.ctypeslib.ndpointer(np.float32, flags="C")
    dp = np.ctypeslib.ndpointer(np.float64, flags="C")
    lib.anneal.restype = ctypes.c_double
    lib.anneal.argtypes = [ip, ctypes.c_int, ctypes.c_int, ip, bp, bp, ctypes.c_int, fp, ctypes.c_int, ctypes.c_int,
                           ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_uint64, dp, dp, ctypes.c_double]
    lib.score_key.restype = ctypes.c_double
    lib.score_key.argtypes = [ip, ctypes.c_int, ip, bp, bp, fp, ctypes.c_int, ctypes.c_int]
    return lib


class LM:
    """Letter 4-gram model. Alphabet: a-z, optional space, then the boundary mark '#'."""

    def __init__(self, text, spaces=True, k=0.05):
        self.spaces = spaces
        self.alphabet = LETTERS + (" " if spaces else "") + "#"
        self.A = len(self.alphabet)
        self.idx = {c: i for i, c in enumerate(self.alphabet)}
        codes = self.encode(text)
        A = self.A
        c = np.array(codes, dtype=np.int64)
        c4 = np.zeros((A, A, A, A))
        np.add.at(c4, (c[:-3], c[1:-2], c[2:-1], c[3:]), 1)
        c3, c2, c1 = c4.sum(axis=0), c4.sum(axis=(0, 1)), c4.sum(axis=(0, 1, 2))

        def cond(x):
            tot = x.sum(axis=-1, keepdims=True)
            return np.divide(x, tot, out=np.zeros_like(x), where=tot > 0)
        # interpolated: a context never seen falls back on shorter ones, down to letter frequency
        p1 = (c1 + k) / (c1 + k).sum()
        probs = 0.60 * cond(c4) + 0.25 * cond(c3)[None] + 0.10 * cond(c2)[None, None] + 0.05 * p1
        self.table = np.ascontiguousarray(np.log10(probs).astype(np.float32).ravel())
        # letter frequencies (letters only), for the solver's frequency term
        n_letters = 26
        lf = c1[:n_letters] + k
        self.letter_logp = np.full(64, -99.0)
        self.letter_logp[:n_letters] = np.log10(lf / lf.sum())

    def encode(self, text):
        """lines of plain text -> codes, '#' at line ends"""
        if isinstance(text, str):
            text = text.split("\n")
        out = [self.A - 1] * 3
        for line in text:
            line = re.sub(r"[^a-z ]+", "", line.lower())
            line = re.sub(r" +", " " if self.spaces else "", line).strip()
            if line:
                out.extend(self.idx[ch] for ch in line)
                out.append(self.A - 1)
        return out

    def per_letter(self, text):
        """mean log10 probability per letter of real text under the model"""
        c = np.array(self.encode(text), dtype=np.int64)
        A = self.A
        ix = ((c[:-3] * A + c[1:-2]) * A + c[2:-1]) * A + c[3:]
        return float(self.table[ix].mean())


class Problem:
    """A symbol stream plus the units a symbol may stand for."""

    def __init__(self, tokens, n_symbols, units, lm):
        self.lm = lm
        self.tokens = np.ascontiguousarray(np.array(tokens, dtype=np.int32))
        self.n_symbols = n_symbols
        self.unit_strings = list(units)
        self.units = np.zeros((len(units), 4), dtype=np.int8)
        self.ulen = np.zeros(len(units), dtype=np.int8)
        for i, u in enumerate(units):
            self.ulen[i] = len(u)
            for j, ch in enumerate(u):
                self.units[i, j] = lm.idx[ch]
        self.units = np.ascontiguousarray(self.units.ravel())
        freq = Counter(t for t in tokens if t >= 0)
        self.weights = np.array([freq.get(s, 0) ** 0.5 + 0.5 for s in range(n_symbols)], dtype=np.float64)
        self.space = lm.idx.get(" ", lm.A - 1)
        self._lib = _lib()

    def solve(self, iters=300000, restarts=4, t0=12.0, t1=0.4, seed=0, freq_weight=1.0):
        rng = np.random.default_rng(seed)
        best_key, best = None, -1e300
        for r in range(restarts):
            key = np.ascontiguousarray(rng.integers(0, len(self.unit_strings), self.n_symbols).astype(np.int32))
            val = self._lib.anneal(self.tokens, len(self.tokens), self.n_symbols, key, self.units, self.ulen,
                                   len(self.unit_strings), self.lm.table, self.lm.A, self.space,
                                   iters, t0, t1, seed * 1000 + r + 1, self.weights,
                                   np.ascontiguousarray(self.lm.letter_logp), freq_weight)
            if val > best:
                best, best_key = val, key.copy()
        return best_key, best

    def score(self, key, tokens=None):
        tok = self.tokens if tokens is None else np.ascontiguousarray(np.array(tokens, dtype=np.int32))
        return self._lib.score_key(tok, len(tok), np.ascontiguousarray(key.astype(np.int32)), self.units, self.ulen,
                                   self.lm.table, self.lm.A, self.space)

    def decode(self, key, tokens=None, limit=400):
        tok = self.tokens if tokens is None else tokens
        out = []
        for t in tok[:limit]:
            out.append(self.unit_strings[key[t]] if t >= 0 else (" " if t == -2 else "#"))
        return "".join(out)

    def letters(self, key, tokens=None):
        tok = self.tokens if tokens is None else np.array(tokens)
        n = sum(int(self.ulen[key[t]]) if t >= 0 else 1 for t in tok)
        return max(n, 1)


def word_stream(lines, top=600, vocab=None):
    """Each word is a symbol (the `top` most frequent types); other words and
    line ends are boundaries. Returns tokens, vocab list."""
    if vocab is None:
        freq = Counter(w for l in lines for w in l)
        vocab = [w for w, _ in freq.most_common(top)]
    ix = {w: i for i, w in enumerate(vocab)}
    tokens = []
    for l in lines:
        tokens.extend(ix.get(w, -1) for w in l)
        tokens.append(-1)
    return tokens, vocab


def glyph_stream(lines, split, vocab=None, spaces=True):
    """Each glyph unit (as cut by `split(word)`) is a symbol; spaces kept or dropped."""
    seq = [[split(w) for w in l] for l in lines]
    if vocab is None:
        freq = Counter(g for l in seq for w in l for g in w)
        vocab = [g for g, _ in freq.most_common()]
    ix = {g: i for i, g in enumerate(vocab)}
    tokens = []
    for l in seq:
        for k, w in enumerate(l):
            if k and spaces:
                tokens.append(-2)
            tokens.extend(ix.get(g, -1) for g in w)
        tokens.append(-1)
    return tokens, vocab


def dictionary(words, min_len=5, min_count=2):
    freq = Counter(words)
    return {w for w, c in freq.items() if c >= min_count and len(w) >= min_len}


def word_hits(text, vocab, spaces=True):
    """share of letters that sit in dictionary words. With spaces: whole words.
    Without: greedy longest match, words of 6+ letters only."""
    text = text.replace("#", " ").replace("\n", " ")
    if spaces:
        ws = text.split()
        n = sum(map(len, ws))
        return sum(len(w) for w in ws if w in vocab) / n if n else 0.0
    s = text.replace(" ", "")
    long_words = {w for w in vocab if len(w) >= 6}
    longest = max(map(len, long_words), default=0)
    i = covered = 0
    while i < len(s):
        for k in range(min(longest, len(s) - i), 5, -1):
            if s[i:i + k] in long_words:
                covered += k
                i += k
                break
        else:
            i += 1
    return covered / len(s) if s else 0.0
