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


FAMILIES = ("q", "c", "o", "x")


def family(word):
    """qo-, ch/sh- (and the bench gallows), o-, anything else."""
    if word.startswith("q"):
        return "q"
    if word[:2] in ("ch", "sh") or word[:3] in ("cth", "ckh", "cph", "cfh"):
        return "c"
    if word.startswith("o"):
        return "o"
    return "x"


def position(i, n, para_start):
    if i == 0:
        return "para_first" if para_start else "line_first"
    if i == n - 1:
        return "line_last"
    return "middle"


class Assembler:
    def __init__(self, order=2, link=True, min_count=3, recall_p=0.0, edit_p=0.0, window=20,
                 sheet_sigma=0.0, hold=1.0, follow_p=0.0, link_signs=1, link_by="last",
                 line_sigma=0.0, echo_fits=False, line_drift=0.0):
        self.line_drift = line_drift
        self.echo_fits = echo_fits
        self.link_by = link_by
        self.line_sigma = line_sigma
        self.line_family = None
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

    def key(self, word):
        """What the next word's start is drawn given: the previous word's last
        `link_signs` signs, or (link_by="family") its family and last sign."""
        seq = signs(word)
        if self.link_by == "family":
            return family(word) + ":" + seq[-1]
        return "".join(seq[-self.link_signs:])

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
                prev = self.key(w)
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
        if w is not None or self.line_gallows is not None or (start and self.line_family is not None):
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
                if self.line_family is not None:
                    if start and s != "$":
                        f *= self.line_family["start"][family(s)]
                    if s == "$":
                        f *= self.line_family["end"].get(ctx[-1], 1.0)
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

    def line_setting(self, rng, before=None):
        """A line's own setting, on top of the sheet's: a weight for each
        family of word starts and for ending a word after each sign. With
        line_drift = rho > 0 the log weights follow the line before,
        rho * previous + sqrt(1 - rho^2) * N(0, line_sigma), so the setting
        wanders down the sheet instead of being drawn afresh."""
        rho = self.line_drift if before else 0.0
        keep = math.sqrt(1 - rho * rho)
        ends = {s for c in self.pooled.values() for s in c if s != "$"}
        out = {}
        for part, keys in (("start", FAMILIES), ("end", ends)):
            out[part] = {}
            for k in keys:
                old = math.log(before[part][k]) if before else 0.0
                out[part][k] = math.exp(rho * old + keep * rng.gauss(0, self.line_sigma))
        return out

    def pick_recent(self, rng, pos, prev, words):
        """A recent word to repeat. With echo_fits, words whose first sign is
        likely after `prev` are picked more often (weight: how often that
        first sign follows `prev` in the fitted tables, plus one)."""
        if not self.echo_fits:
            return rng.choice(words)
        c = self.tab[pos].get(self._ctx(prev, [])) or self.pooled.get(self._ctx(prev, [])) or Counter()
        ws = [c.get(signs(w)[0], 0) + 1 for w in words]
        r = rng.random() * sum(ws)
        for w, x in zip(words, ws):
            r -= x
            if r <= 0:
                return w
        return words[-1]

    def fill_sheet(self, shape, seed=0):
        """Like fill, for a whole sheet: one setting for the sheet, and with
        hold > 1 one favoured gallows per line (weight `hold`)."""
        rng = random.Random(seed)
        self.new_setting(rng)
        self.line_family = None
        out = []
        history = []
        for n, para_start in shape:
            self.line_gallows = rng.choice(GALLOWS[:4]) if self.hold != 1.0 else None
            self.line_family = self.line_setting(rng, self.line_family) if self.line_sigma else None
            out += self.fill([(n, para_start)], seed=rng.randrange(10 ** 9), history=history)
        self.weights = None
        self.line_gallows = None
        self.line_family = None
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
                    w = self.pick_recent(rng, pos, prev, recent[-self.window:])
                elif pos == "middle" and recent and r < self.recall_p + self.edit_p:
                    w = self.edit(rng, pos, self.pick_recent(rng, pos, prev, recent[-self.window:]))
                else:
                    w = self.word(rng, pos, prev)
                recent.append(w)
                line.append(w)
                prev = self.key(w)
            out.append(line)
        return out
