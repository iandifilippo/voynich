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
import math
import random
import re
from collections import Counter, defaultdict

UNIT = re.compile(r"c[tkpf]h|ch|sh|eee|ee|iii|ii|.")
POSITIONS = ("para_first", "line_first", "line_last", "middle")
GALLOWS = ("t", "k", "p", "f", "cth", "ckh", "cph", "cfh")


def signs(word):
    return UNIT.findall(word)


def position(i, n, para_start):
    if i == 0:
        return "para_first" if para_start else "line_first"
    if i == n - 1:
        return "line_last"
    return "middle"


class Assembler:
    def __init__(self, order=2, link=True, min_count=3, recall_p=0.0, edit_p=0.0, window=20,
                 sheet_sigma=0.0, hold=1.0, follow_p=0.0, link_signs=1):
        self.follow_p = follow_p
        self.link_signs = link_signs
        self.sheet_sigma = sheet_sigma
        self.hold = hold
        self.weights = None
        self.line_gallows = None
        self.recall_p = recall_p
        self.edit_p = edit_p
        self.window = window
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
                prev = "".join(seq[:-1][-self.link_signs:])
        self.first = Counter()
        self.pooled = defaultdict(Counter)
        self.short = defaultdict(Counter)
        for p in POSITIONS:
            for ctx, c in self.tab[p].items():
                self.pooled[ctx].update(c)
                self.short[ctx[-1]].update(c)
                if ctx[-1].startswith("^"):
                    self.first.update({k: v for k, v in c.items() if k != "$"})
        return self

    def _draw(self, rng, pos, ctx, start=False):
        c = self.tab[pos].get(ctx)
        if not c or sum(c.values()) < self.min_count:
            c = self.pooled.get(ctx)
        if not c:
            c = self.short.get(ctx[-1])
        if not c and ctx[-1].startswith("^"):
            c = self.first
        if not c:
            return "$"
        w = self.weights
        if w is not None or self.line_gallows is not None:
            items = []
            for s, n in c.items():
                f = 1.0
                if w is not None:
                    if start:
                        f *= w["start"].get(s, 1.0)
                    if s in GALLOWS:
                        f *= w["gallows"].get(s, 1.0)
                    if s == "$":
                        f *= w["end"].get(ctx[-1], 1.0)
                if self.line_gallows is not None and s in GALLOWS:
                    f *= self.hold if s == self.line_gallows else 1.0
                items.append((s, n * f))
        else:
            items = list(c.items())
        r = rng.random() * sum(n for _, n in items)
        for s, n in items:
            r -= n
            if r <= 0:
                return s
        return s

    def word(self, rng, pos, prev_last):
        hist = []
        while True:
            s = self._draw(rng, pos, self._ctx(prev_last, hist), start=not hist)
            if s == "$":
                if hist:
                    return "".join(hist)
                continue
            hist.append(s)
            if len(hist) > 15:
                return "".join(hist)

    def edit(self, rng, pos, word):
        """Redraw one sign of a word from the chain, keeping the rest."""
        seq = signs(word)
        j = rng.randrange(len(seq))
        for _ in range(10):
            s = self._draw(rng, pos, self._ctx("#", seq[:j]))
            if s != "$" and s != seq[j]:
                return "".join(seq[:j] + [s] + seq[j + 1:])
        return word

    def new_setting(self, rng):
        """A sheet's setting: every start sign, gallows and word ending gets a
        random weight exp(N(0, sheet_sigma)), held until the next call."""
        if not self.sheet_sigma:
            self.weights = None
            return
        signs_ = {s for c in self.pooled.values() for s in c if s != "$"}
        draw = lambda: math.exp(rng.gauss(0, self.sheet_sigma))  # noqa: E731
        self.weights = {"start": {s: draw() for s in signs_}, "gallows": {g: draw() for g in GALLOWS},
                        "end": {s: draw() for s in signs_}}

    def fill_sheet(self, shape, seed=0):
        """Like fill, for a whole sheet: one setting for the sheet, and with
        hold > 1 one favoured gallows per line (weight `hold`)."""
        rng = random.Random(seed)
        self.new_setting(rng)
        out = []
        history = []
        for n, para_start in shape:
            self.line_gallows = rng.choice(GALLOWS[:4]) if self.hold != 1.0 else None
            out += self.fill([(n, para_start)], seed=rng.randrange(10 ** 9), history=history)
        self.weights = None
        self.line_gallows = None
        return out

    def fill(self, shape, seed=0, history=None):
        """shape is one page. With recall_p > 0 a word is, with that
        probability, a repeat of one of the last `window` words on the page,
        and with probability edit_p such a word with one sign redrawn (only
        for words inside a line). With follow_p > 0, if the previous word
        already occurred on the page, the word that followed it there is
        written again (possibly with a sign redrawn, edit_p), i.e. a short
        run is copied. `history` carries the page's words across calls."""
        rng = random.Random(seed)
        out = []
        recent = history if history is not None else []
        for n, para_start in shape:
            prev = "#"
            line = []
            for i in range(n):
                pos = position(i, n, para_start)
                r = rng.random()
                follow = None
                if self.follow_p and line and rng.random() < self.follow_p:
                    starts = [k for k in range(len(recent) - 1) if recent[k] == line[-1]]
                    if starts:
                        follow = recent[rng.choice(starts) + 1]
                if follow is not None:
                    w = follow if rng.random() >= self.edit_p else self.edit(rng, pos, follow)
                elif pos == "middle" and recent and r < self.recall_p:
                    w = rng.choice(recent[-self.window:])
                elif pos == "middle" and recent and r < self.recall_p + self.edit_p:
                    w = self.edit(rng, pos, rng.choice(recent[-self.window:]))
                else:
                    w = self.word(rng, pos, prev)
                recent.append(w)
                line.append(w)
                prev = "".join(signs(w)[-self.link_signs:])
            out.append(line)
        return out
