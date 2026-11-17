"""Words assembled fresh, sign by sign, with a short memory.

The alternative to copying that exp. 34 points at. Each word is drawn from a
sign-level Markov chain that looks back `order` signs, with separate tables
for the first word of a paragraph, the first word of a line, the last word of
a line and every other word (falling back on the general table when a
position table hasn't seen a context). The only link between words: the
first sign of a word is drawn given the last sign of the word before
(`link=True`). No word is ever copied, so there is no lexicon beyond what the
sign chain implies.

    m = Assembler(order=2).fit(lines, para_starts)
    out = m.fill(shape, seed=1)   # shape: list of (n_words, para_start) per line
"""
import random
import re
from collections import Counter, defaultdict

UNIT = re.compile(r"c[tkpf]h|ch|sh|eee|ee|iii|ii|.")
POSITIONS = ("para_first", "line_first", "line_last", "middle")


def signs(word):
    return UNIT.findall(word)


def position(i, n, para_start):
    if i == 0:
        return "para_first" if para_start else "line_first"
    if i == n - 1:
        return "line_last"
    return "middle"


class Assembler:
    def __init__(self, order=2, link=True, min_count=3):
        self.order = order
        self.link = link
        self.min_count = min_count
        self.tab = {p: defaultdict(Counter) for p in POSITIONS}

    def _ctx(self, prev_last, history):
        h = tuple(history[-self.order:])
        if len(history) < self.order:
            pad = ("^" + (prev_last if self.link else ""),)
            h = pad * (self.order - len(history)) + h
        return h

    def fit(self, lines, para_starts=()):
        para_starts = set(para_starts)
        for k, line in enumerate(lines):
            prev = "#"
            for i, w in enumerate(line):
                pos = position(i, len(line), k in para_starts)
                seq = signs(w) + ["$"]
                hist = []
                for s in seq:
                    ctx = self._ctx(prev, hist)
                    self.tab[pos][ctx][s] += 1
                    hist.append(s)
                prev = seq[-2]
        self.pooled = defaultdict(Counter)
        self.short = defaultdict(Counter)
        for p in POSITIONS:
            for ctx, c in self.tab[p].items():
                self.pooled[ctx].update(c)
                self.short[ctx[-1]].update(c)
        return self

    def _draw(self, rng, pos, ctx):
        c = self.tab[pos].get(ctx)
        if not c or sum(c.values()) < self.min_count:
            c = self.pooled.get(ctx)
        if not c:
            c = self.short.get(ctx[-1])
        if not c:
            return "$"
        r = rng.random() * sum(c.values())
        for s, n in c.items():
            r -= n
            if r <= 0:
                return s
        return s

    def word(self, rng, pos, prev_last):
        hist = []
        while True:
            s = self._draw(rng, pos, self._ctx(prev_last, hist))
            if s == "$":
                if hist:
                    return "".join(hist)
                continue
            hist.append(s)
            if len(hist) > 15:
                return "".join(hist)

    def fill(self, shape, seed=0):
        rng = random.Random(seed)
        out = []
        for n, para_start in shape:
            prev = "#"
            line = []
            for i in range(n):
                w = self.word(rng, position(i, n, para_start), prev)
                line.append(w)
                prev = signs(w)[-1]
            out.append(line)
        return out
