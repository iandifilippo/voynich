"""Self-citation text generator after Timm & Schinner.

Independent reimplementation of the procedure in Timm (2014, arXiv:1407.6639),
Timm & Schinner (2020, Cryptologia 44:1) and the VoynichTextGenerator app
(github.com/TorstenTimm/VoynichTextGenerator). Rule tables and probabilities
follow the app; control flow is simplified where the app's choices are UI
details. The text is built line by line, every new word being a modified copy
of a word already on the page.

    gen = AutoCopy(seed=1, currier="B")
    lines = gen.run(n_lines=1200)        # list of word lists
    gen.paragraph_starts                 # indices of paragraph-initial lines
"""
import random

GALLOWS = ["k", "t", "p", "f"]
FIRST_LINE_GALLOWS = {"p", "f"}
LINE_INITIAL = ["o", "y", "d", "s"]
LINE_FINAL = ["m", "g"]
OL = {"ol", "al", "or", "ar"}

# token -> [(replacement tokens, cumulative probability out of 100)]
SIMILAR = {
    "k": [(["t"], 77), (["p"], 94), (["f"], 100)],
    "t": [(["k"], 84), (["p"], 96), (["f"], 100)],
    "p": [(["k"], 59), (["t"], 97), (["f"], 100)],
    "f": [(["k"], 56), (["t"], 92), (["p"], 100)],
    "in": [(["n"], 8), (["iin"], 84), (["iiin"], 87), (["ir"], 97), (["iir"], 99), (["il"], 100)],
    "iin": [(["n"], 13), (["in"], 70), (["iiin"], 74), (["ir"], 94), (["iir"], 99), (["il"], 100)],
    "iiin": [(["n"], 6), (["in"], 31), (["iin"], 90), (["ir"], 98), (["iir"], 100)],
    "ir": [(["r"], 6), (["in"], 33), (["iin"], 95), (["iiin"], 97), (["iir"], 99), (["iiir"], 100)],
    "iir": [(["r"], 6), (["in"], 30), (["iin"], 89), (["iiin"], 91), (["ir"], 99), (["iiir"], 100)],
    "iiir": [(["ir"], 90), (["iir"], 100)],
    "is": [(["in"], 50), (["iis"], 100)],
    "iis": [(["iin"], 50), (["is"], 100)],
    "il": [(["in"], 50), (["iil"], 100)],
    "iil": [(["iin"], 50), (["il"], 99), (["iiil"], 100)],
    "iiil": [(["il"], 66), (["iil"], 100)],
    "im": [(["in"], 30), (["iin"], 100)],
    "iim": [(["in"], 30), (["iin"], 100)],
    "iiim": [(["in"], 30), (["iin"], 100)],
    "om": [(["ol"], 45), (["or"], 94), (["og"], 98), (["omg"], 100)],
    "am": [(["al"], 45), (["ar"], 94), (["ag"], 98), (["amg"], 100)],
    "og": [(["or"], 30), (["al"], 63), (["ar"], 100)],
    "ag": [(["ol"], 48), (["or"], 72), (["ar"], 100)],
    "ol": [(["or"], 30), (["al"], 63), (["ar"], 100)],
    "or": [(["ol"], 47), (["al"], 73), (["ar"], 100)],
    "al": [(["ol"], 48), (["or"], 72), (["ar"], 100)],
    "ar": [(["ol"], 49), (["or"], 73), (["al"], 100)],
    "e": [(["e"], 50), (["ee"], 99), (["eee"], 100)],
    "ee": [(["ch"], 40), (["ch", "e"], 50), (["e"], 98), (["eee"], 100)],
    "eee": [(["ch"], 10), (["ch", "e"], 20), (["ee"], 65), (["e"], 100)],
    "ch": [(["ee"], 10), (["sh"], 90), (["ckh"], 97), (["cth"], 100)],
    "sh": [(["ee"], 10), (["ch"], 90), (["ckh"], 97), (["cth"], 100)],
    "ckh": [(["cth"], 30), (["k", "ch"], 50), (["t", "ch"], 70), (["eke"], 72), (["ete"], 74), (["cph"], 78), (["ch"], 100)],
    "cth": [(["ckh"], 30), (["k", "ch"], 50), (["t", "ch"], 70), (["eke"], 72), (["ete"], 74), (["cph"], 78), (["cfh"], 80), (["ch"], 100)],
    "eke": [(["ckh"], 30), (["cth"], 50), (["k", "ee"], 56), (["t", "ee"], 60), (["ete"], 65), (["ee"], 100)],
    "ete": [(["ckh"], 30), (["cth"], 50), (["k", "ee"], 56), (["t", "ee"], 60), (["eke"], 65), (["ee"], 100)],
    "cph": [(["ckh"], 40), (["cth"], 75), (["cfh"], 80), (["ch"], 100)],
    "cfh": [(["ckh"], 40), (["cth"], 75), (["cph"], 80), (["ch"], 100)],
    "ikh": [(["ckh"], 100)], "ith": [(["cth"], 100)], "iph": [(["cph"], 100)], "ifh": [(["cfh"], 100)],
    "y": [(["o"], 100)], "o": [(["y"], 100)],
    "n": [(["r"], 50), (["in"], 63), (["iin"], 100)],
    "l": [(["r"], 100)],
    "r": [(["r"], 50), (["s"], 100)],
    "g": [(["m"], 100)],
    "s": [(["r"], 75), (["d"], 100)],
    "d": [(["d"], 50), (["s"], 100)],
    "a": [(["d", "a"], 98), (["d", "o"], 100)],
    "qo": [(["o"], 100)],
}

LIGATURES = sorted(
    "ol or al ar dy qo ch sh eee ee cth ckh cph cfh ith ikh iph ifh eke ete in iin iiin "
    "ir iir iiir is iis iiis il iil iiil im iim iiim om am og ag".split(), key=len, reverse=True)
DELETABLE = set("eoadyl")
PREFIXES = {"l": ["k", "t", "p", "f", "d", "ch", "o", "a", "e", "i"],
            "o": ["k", "t", "p", "f", "d", "ch"],
            "ch": ["k", "t", "p", "f", "d", "ol", "or", "al", "ar"],
            "q": [], "d": ["a"], "x": ["ol", "or", "al", "ar"]}
DROP_BEFORE = {"ol": ["l", "r", "s"], "al": ["l", "r", "s"], "or": ["l", "r", "s"], "ar": ["l", "r", "s"]}

FOLLOWERS = {
    "k": ["a", "o", "y", "e", "ch", "sh"], "t": ["a", "o", "y", "e", "ch", "sh"],
    "p": ["a", "o", "y", "ch", "sh"], "f": ["a", "o", "y", "ch", "sh"],
    "ol": ["", "a", "o", "y", "ch", "sh", "al", "ar", "ol", "t", "k", "p", "f", "d", "dy"],
    "or": ["", "a", "o", "y", "ch", "al", "ar", "ol"],
    "al": ["", "a", "o", "y", "ch", "sh", "al", "ar", "ol", "t", "k", "p", "f", "dy"],
    "ar": ["", "a", "o", "y", "ch", "al", "ar", "ol"],
    "r": ["", "a", "o", "y", "ch"], "s": ["", "a", "o", "y", "e", "ee", "ch"],
    "d": ["", "a", "o", "l", "e", "ee", "ch", "sh"], "m": [""],
    "e": ["d", "o", "y", "a", "s", "k", "t", "p", "f", "ch", "ckh", "cth", "cph", "cfh", ""],
}
FOLLOWERS["ee"] = FOLLOWERS["eee"] = FOLLOWERS["e"]
INITIAL_FOLLOWERS = {"s": ["a", "o", "y", "e", "ch", "sh"], "d": ["a", "o", "y", "ch"],
                     "y": ["d", "s", "ch", "sh", "k", "t", "p", "f"],
                     "o": ["d", "s", "ch", "sh", "k", "t", "p", "f"]}
_g = ["", "o", "qo", "y", "l", "e", "ch", "sh", "ol", "al"]
_d = ["", "o", "qo", "y", "l", "e", "ch", "ckh", "cth", "cph", "cfh", "sh", "ol", "al"]
_c = ["", "o", "y", "e", "ch", "sh"]
_e = ["", "t", "k", "ch", "sh", "ckh", "cth", "cph", "cfh", "q", "o", "l", "s", "d"]
PRECURSORS = {"k": _g, "t": _g, "p": _g, "f": _g, "dy": _d, "d": _d,
              "sh": ["", "l", "ol", "al", "d", "t", "k", "p", "f", "o", "y", "s", "e", "ee", "eee"],
              "ckh": _c, "cth": _c, "cph": _c, "cfh": _c, "e": _e, "ee": _e, "eee": _e}
LINE_END = {"ol": "om", "or": "om", "al": "am", "ar": "am", "iin": "im", "in": "n",
            "iiin": "im", "om": "og", "am": "ag", "im": "mg"}
SELF_IN = {"y": "o", "m": "r", "g": "r", "n": "r", "in": "ir", "iin": "iir", "dy": "da"}
SELF_END = {"o": "y", "a": "y", "k": "t", "t": "k", "p": "f", "f": "p"}


def tokens(word):
    out, i = [], 0
    while i < len(word):
        for lig in LIGATURES:
            if word.startswith(lig, i):
                out.append(lig)
                i += len(lig)
                break
        else:
            out.append(word[i])
            i += 1
    return out


def before_ok(tok, rest):
    """Can `tok` stand in front of the string `rest`?"""
    allowed = FOLLOWERS.get(tok)
    if allowed is not None:
        return any((a == "" and rest == "") or (a and rest.startswith(a)) for a in allowed)
    return not rest.startswith("q") and not (rest and rest.startswith(tok))


def after_ok(prev, tok):
    """Can `tok` follow the string `prev`?"""
    allowed = PRECURSORS.get(tok)
    if allowed is not None:
        return any((a == "" and prev == "") or (a and prev.endswith(a)) for a in allowed)
    return not tok.startswith("q") and not (prev and prev.endswith(tok))


def valid(toks):
    return all(after_ok(a, b) and before_ok(a, b) for a, b in zip(toks, toks[1:]))


class Word:
    __slots__ = ("toks", "kind")

    def __init__(self, toks, kind="copy"):
        self.toks = [t for t in toks if t]
        self.kind = kind

    @property
    def s(self):
        return "".join(self.toks)

    def __len__(self):
        return len(self.s)


class AutoCopy:
    PARA_GALLOW = 94

    def __init__(self, seed=0, currier="B", line_chars=55, page_lines=29, seed_text=None,
                 boundary=None, boundary_p=0.0):
        """boundary: optional {last glyph: set of word starts} the writer prefers
        after a word ending in that glyph; with probability boundary_p a new word
        that doesn't fit is thrown away and another one is copied instead."""
        self.boundary, self.boundary_p = boundary or {}, boundary_p
        self.rng = random.Random(seed)
        self.currier = currier
        self.line_chars = line_chars
        self.page_lines = page_lines
        self.same_pos_start, self.same_pos = 23, 75
        self.lines, self.para_lines, self.paragraph_starts = [], [], []
        self.pool, self._in_pool = [], set()
        self.n_tokens = self.n_i = 0
        self.streak = {"i": 0, "dy": 0, "ol": 0, "other": 0}
        if seed_text is None:
            seed_text = ("fachys ykal ar ataiin shol shory cthres y kor sholdy" if currier == "A" else
                         "polchedy qokeol okain checthy oteey lshedy okain qokain qokalshedy oteys")
        first = [Word(tokens(w), "seed") for w in seed_text.split()]
        for w in first:
            self.remember(w)
        for w in ("daiin", "ol", "cheody" if currier == "A" else "chedy"):
            self.remember(Word(tokens(w), "seed"))
        self.lines.append(first)
        self.para_lines.append(first)
        self.paragraph_starts.append(0)

    def r(self, n):
        return self.rng.randrange(n) if n > 0 else 0

    # bookkeeping -------------------------------------------------------
    def kind_of(self, w):
        s = w.s
        if "i" in s:
            return "i"
        if "dy" in w.toks or s.endswith(("y", "d")):
            return "dy"
        if OL & set(w.toks):
            return "ol"
        return "other"

    def remember(self, w):
        s = w.s
        if (w.kind == "seed" or valid(w.toks)) and len(w.toks) < 8 and not s.startswith(tuple(GALLOWS)) \
                and not s.endswith(tuple(LINE_FINAL)) and w.kind != "combine" and s not in self._in_pool:
            self.pool.append(w)
            self._in_pool.add(s)
        self.n_tokens += 1
        k = self.kind_of(w)
        self.n_i += k == "i"
        for key in self.streak:
            self.streak[key] = self.streak[key] + 1 if key == k else 0

    # choosing a source -------------------------------------------------
    def neighbours(self, line, i):
        a = line[i]
        b = line[i - 1] if i > 0 else line[i + 1] if i < len(line) - 1 else line[i]
        return [a, b]

    def position(self, current, source):
        x = sum(len(w) + 1 for w in current)
        pos = 0
        for i, w in enumerate(source):
            if pos < x < pos + len(w) + 1:
                return i
            pos += len(w) + 1
        return len(current)

    def source(self, current, para_initial, line_initial, in_page):
        roll = self.r(100)
        if para_initial and roll < 70 and len(self.para_lines) > 1:
            roll = self.r(100)
            if not line_initial and roll <= 20:
                roll = 21
            if len(current) <= 3 and roll <= 20:
                if len(current) < 2 or self.r(100) < (60 if len(current) == 2 else 40):
                    roll = 21
            if roll <= 5:
                out = [current[-1], current[-2] if len(current) > 1 else current[-1]]
            elif roll <= 20:
                out = self.neighbours(current, self.r(len(current)))
            else:
                src = self.para_lines[self.r(len(self.para_lines))]
                pos = self.r(3) if line_initial else self.r(len(src))
                if pos >= len(src):
                    pos = self.r(len(src))
                out = self.neighbours(src, pos)
        else:
            roll = self.r(100)
            if len(current) <= 3 and roll <= 10:
                if len(current) < 2 or self.r(100) < (60 if len(current) == 2 else 40):
                    roll = 11
            if roll <= 2:
                out = [current[-1], current[-2] if len(current) > 1 else current[-1]]
            elif roll <= 10:
                out = self.neighbours(current, self.r(len(current)))
            elif roll <= 75:
                n = len(self.lines)
                pick = self.r(min(10, n))
                back = {4: 4, 3: 3, 2: 2}.get(pick, 1) if pick < 5 else 1 + self.r(max(2, in_page) - 2)
                idx = max(0, n - back) if n - back >= 0 else n - 1
                src = self.lines[idx]
                pos = self.position(current, src)
                roll = self.r(100)
                if roll <= self.same_pos_start or (pos > 2 and roll <= self.same_pos):
                    if not 0 <= pos < len(src):
                        pos = len(src) - 1 if idx == n - 1 else self.r(len(src))
                else:
                    pos = self.r(len(src))
                out = self.neighbours(src, pos)
            else:
                first = (Word(tokens("daiin"), "seed") if self.n_tokens and self.n_i / self.n_tokens < 0.19
                         else self.pool[self.r(len(self.pool))])
                out = [first, self.pool[self.r(len(self.pool))]]
        # copied words lose an initial gallows
        return [Word(w.toks[1:], w.kind) if w.s.startswith(tuple(GALLOWS)) and len(w.toks) > 1 else w
                for w in out]

    # modifications -----------------------------------------------------
    def pick(self, subs):
        roll = self.r(100)
        for toks, p in subs:
            if p > roll:
                return toks
        return subs[-1][0]

    def replace(self, w, para_initial):
        for _ in range(5):
            pos = self.r(len(w.toks))
            subs = SIMILAR.get(w.toks[pos])
            if not subs:
                continue
            new = self.pick(subs)
            nxt = w.toks[pos + 1] if pos + 1 < len(w.toks) else ""
            drop_next, ok = False, True
            if any(g in "".join(new) for g in GALLOWS):
                if nxt in GALLOWS:
                    drop_next = True
                elif any(g in w.s for g in GALLOWS) and self.r(100) < 90:
                    ok = False
                elif self.r(100) < (40 if para_initial else 60):
                    ok = False
            if not ok:
                continue
            prev = w.toks[pos - 1] if pos else ""
            after = w.toks[pos + 2 if drop_next else pos + 1] if pos + (2 if drop_next else 1) < len(w.toks) else ""
            if not (after_ok(prev, new[0]) and before_ok(new[-1], after)):
                continue
            if len(new) == 1 and new[0] in w.toks and self.r(100) < 50:
                continue
            toks = w.toks[:pos] + new + w.toks[pos + (2 if drop_next else 1):]
            return Word(toks, "combine" if w.kind == "combine" else "replace")
        return w

    def delete(self, w):
        if w.toks and w.toks[0] in DELETABLE and before_ok("", w.toks[1] if len(w.toks) > 1 else ""):
            toks = w.toks[1:]
            if len(w.toks) > 2 and toks[0] in GALLOWS:
                if toks[1].startswith("a"):
                    toks[0] = "d"
                elif toks[1].startswith("e"):
                    toks[0] = "ch"
            if toks:
                return Word(toks, w.kind)
        return w

    def gallow(self, first_line):
        roll = self.r(100)
        if roll < 35:
            return "k"
        if roll < 50:
            return "t"
        if roll < 90:
            return "p" if first_line else "k"
        return "f" if first_line else "t"

    def place_gallow(self, g, w, pos):
        toks = w.toks
        prev = toks[pos - 1] if pos else ""
        nxt = toks[pos] if pos < len(toks) else ""
        a, b = after_ok(prev, g), before_ok(g, nxt)
        if a and b:
            return Word(toks[:pos] + [g] + toks[pos:], w.kind)
        if a and pos < len(toks) and before_ok(g, toks[pos + 1] if pos + 1 < len(toks) else "-"):
            return Word(toks[:pos] + [g] + toks[pos + 1:], w.kind)
        if b and pos > 0 and after_ok(toks[pos - 2] if pos - 2 > 0 else "-", g):
            return Word(toks[:pos - 1] + [g] + toks[pos:], w.kind)
        return w

    def add_gallow(self, w, para_initial, line_initial):
        if para_initial and line_initial:
            g = self.gallow(True)
            new = self.place_gallow(g, w, 0)
            if new.toks[0] != g:
                new = Word([g, "o"] + new.toks[1:], new.kind)
            return new
        if len(w.toks) > 1 and not (any(c in w.s for c in GALLOWS) and self.r(100) < 90):
            n = len(w.toks)
            for _ in range(5):
                pos = self.r(n) if para_initial else 1 if n == 2 else self.r(n - 2) + 1
                new = self.place_gallow(self.gallow(para_initial), w, pos)
                if new.s != w.s:
                    return new
        return w

    def add_prefix(self, w):
        keys = list(PREFIXES)
        for _ in range(4):
            p = keys[self.r(len(keys))]
            kind = "combine" if w.kind == "combine" else "add"
            if p == "q":
                if self.currier == "A" and self.r(100) > 25:
                    continue
                if w.toks[0][:1] in ("o", "y"):
                    return Word(["qo"] + w.toks[1:], kind)
            elif p == "x":
                if self.currier != "A" and self.r(100) < 30 and w.toks[0] in PREFIXES["x"]:
                    return Word(["x"] + w.toks, kind)
            elif w.toks[0] in PREFIXES[p]:
                toks = list(w.toks)
                if len(toks) > 2 and p in ("o", "y", "l") and toks[0] in ("d", "ch") and self.r(100) < 70:
                    g = self.gallow(False)
                    if before_ok(g, toks[1]):
                        toks[0] = g
                return Word([p] + toks, kind)
        return w

    def add_glyph(self, w, para_initial, line_initial):
        if self.r(100) < (80 if para_initial else 8):
            return self.add_gallow(w, para_initial, line_initial)
        return self.add_prefix(w)

    def self_combine(self, w):
        first, last = w.toks[0], w.toks[-1]
        if not before_ok(last, first):
            return w
        a, b = list(w.toks), list(w.toks)
        if SELF_END.get(last, last) != last and self.r(100) < 80:
            b[-1] = SELF_END[last]
        if SELF_IN.get(last, last) != last:
            a[-1] = SELF_IN[last]
        if before_ok("k", first) and before_ok(last, "k") and self.r(100) < 30:
            b = [self.gallow(False)] + b
        return Word(a + b, "combine")

    def head_of(self, w):
        roll = self.r(100)
        if roll < 40:
            return w.toks[:self.r(len(w.toks) - 1) + 1] if len(w.toks) > 1 else []
        if roll >= 60 and w.toks[0] in DROP_BEFORE:
            for lig in DROP_BEFORE:
                if lig in w.toks:
                    return [lig]
        return w.toks[:-1]

    def combine(self, w1, w2):
        if (len(w1.toks) == 2 or (len(w1.toks) == 1 and w1.s in DROP_BEFORE)) and self.r(100) < 60:
            new = self.self_combine(w1)
            if new.s != w1.s:
                return new
        head = self.head_of(w2)
        if head:
            tail = list(w1.toks)
            for t in DROP_BEFORE.get(head[-1], []):
                if tail and tail[0] == t:
                    tail = tail[1:]
            if tail and len(head) + len(tail) < 9 and before_ok(head[-1], tail[0]):
                return Word(head + tail, "combine")
        return self.self_combine(w1) if len(w1.toks) <= 2 else w1

    def split(self, w):
        if w.toks[0] in DROP_BEFORE and len(w.toks) > 1:
            return [Word([w.toks[0]], "split"), Word(w.toks[1:], "split")]
        if w.toks[-1] in DROP_BEFORE and len(w.toks) > 1:
            return [Word(w.toks[:-1], "split"), Word([w.toks[-1]], "split")]
        if self.r(100) < 30 and len(w.toks) > 2:
            return [w, Word(w.toks[1:], "split")]
        return [w]

    def add_line_initial(self, w):
        if w.s.startswith(tuple(LINE_INITIAL)) or self.r(100) >= 30:
            return w
        roll = self.r(100)
        g = "o" if roll < 46 else "y" if roll < 76 else "d" if roll < 91 else "s"
        toks = list(w.toks)
        if len(toks) > 2 and g in ("o", "y") and toks[0] in ("d", "ch") and self.r(100) < 90:
            gal = self.gallow(False)
            if before_ok(gal, toks[1]):
                toks[0] = gal
        allowed = INITIAL_FOLLOWERS.get(g, [])
        if any(toks[0].startswith(a) for a in allowed):
            return Word([g] + toks, w.kind)
        return w

    def drop_line_initial(self, w):
        if not w.s.startswith(tuple(LINE_INITIAL)) or len(w.toks) <= 2:
            return w
        toks = w.toks[1:]
        if toks[0] in GALLOWS:
            if toks[1].startswith("a"):
                toks[0] = "d"
            elif toks[1].startswith("e"):
                toks[0] = "ch"
        return Word(toks, w.kind)

    def swap_gallows(self, w, first_line):
        out = []
        for t in w.toks:
            if first_line and any(g in t for g in GALLOWS):
                ng = self.gallow(True)
                for g in GALLOWS:
                    t = t.replace(g, ng)
            elif not first_line and any(g in t for g in FIRST_LINE_GALLOWS):
                ng = self.gallow(False)
                for g in FIRST_LINE_GALLOWS:
                    t = t.replace(g, ng)
            out.append(t)
        return Word(out, w.kind)

    def morph(self, src, para_initial, line_initial):
        w = src[0]
        n = len(w)
        roll = 0 if (para_initial and line_initial) else self.r(100)
        if 65 <= roll <= 81:
            r2 = self.r(100)
            grow = (n < 3 or r2 < 94) if n < 6 else not (n > 8 or r2 < 94)
            out = [self.add_glyph(w, para_initial, line_initial) if grow else self.delete(w)]
        elif roll >= 82:
            r2 = self.r(100)
            join = (n <= 2 or r2 < 96) if n < 6 else (r2 < 4 and n <= 8)
            out = [self.combine(w, src[1])] if join and w.kind != "combine" else self.split(w)
        else:
            r2 = self.r(100)
            times = 1 if r2 <= 30 else 3 if r2 <= 40 else 2
            cur = w
            for i in range(times):
                nxt = self.replace(cur, para_initial)
                if nxt.s == w.s and i == 0:
                    nxt = self.replace(cur, para_initial)
                cur = nxt if nxt.s != w.s else cur
            out = [cur]
        if line_initial:
            if para_initial and self.r(100) < self.PARA_GALLOW:
                out[0] = self.add_gallow(out[0], True, True)
            else:
                out[0] = self.add_line_initial(out[0])
        elif out[0].s.startswith(tuple(LINE_INITIAL)) and self.r(len(PREFIXES)) < 3 and len(out[0].toks) > 3:
            out[0] = self.drop_line_initial(out[0])
        if not para_initial and any(g in out[0].s for g in FIRST_LINE_GALLOWS):
            if self.r(100) < self.PARA_GALLOW:
                out[0] = self.swap_gallows(out[0], False)
        elif para_initial and any(g in out[0].s for g in GALLOWS):
            out[0] = self.swap_gallows(out[0], True)
        last = out[-1]
        ligs = [t for t in last.toks[1:] if t in DROP_BEFORE]
        if ligs and self.r(100) < 20:
            extra = Word([ligs[0]], "split")
            if self.r(100) < 50:
                extra = self.replace(extra, para_initial)
            out.append(extra)
        return [x for x in out if x.toks]

    def shorten(self, w, room):
        toks = list(w.toks)
        changed = False
        if LINE_END.get(toks[-1], toks[-1]) != toks[-1]:
            toks[-1] = LINE_END[toks[-1]]
            changed = True
        length = sum(map(len, toks))
        for i, t in enumerate(toks):
            if room < length and len(t) > 1:
                cands = [s[0] for s, _ in SIMILAR.get(t, []) if len(s) == 1 and len(s[0]) < len(t)]
                if cands:
                    best = min(cands, key=len)
                    length += len(best) - len(t)
                    toks[i] = best
                    changed = True
        while room < length and len(toks) > 2:
            length -= len(toks.pop(0))
            changed = True
        return Word(toks, "shorten") if changed else w

    def fits(self, prev, word):
        allowed = self.boundary.get(prev[-1])
        if not allowed:
            return True
        head = word[:2] if word[:2] in ("ch", "sh", "qo") else word[:1]
        return head in allowed

    # one line ------------------------------------------------------------
    def line(self, para_initial, para_final, in_page):
        limit = self.line_chars
        if para_final:
            limit = self.r(limit)
            if limit < 10:
                limit = 15
        out, used, tries = [], 0, 0
        line_initial = True
        while used + max(tries - 3, 0) < limit and tries < 60:
            room = limit - used
            src = self.source(out, para_initial, line_initial, in_page)
            n = len(src[0].toks)
            if line_initial:
                go = n > 2
            elif n > 4:
                go = n < 4 + self.r(4)
            else:
                go = True
            if go and src[0].kind == "combine":
                go = src[1].kind != "combine" and self.r(100) >= 30
            if not go:
                tries += 1
                continue
            new = self.morph(src, para_initial, line_initial)
            if not new:
                tries += 1
                continue
            if out and self.boundary and not self.fits(out[-1].s, new[0].s) \
                    and self.rng.random() < self.boundary_p:
                tries += 1
                continue
            if out and new[0].s == out[-1].s:
                if self.r(100) >= 50:
                    tries += 1
                    continue
            elif self.streak[self.kind_of(new[0])] > 3:
                tries += 1
                continue
            for i, w in enumerate(new):
                if room - len(w) <= 0:
                    w = self.shorten(w, room)
                cost = len(w) + (0 if (i == 0 and line_initial) else 1)
                if room - cost >= 0 and w.toks:
                    line_initial = False
                    out.append(w)
                    self.remember(w)
                    used += cost
                    room -= cost
                    tries = 0
                else:
                    tries += 1
        if not out:
            out = [self.pool[self.r(len(self.pool))]]
        self.lines.append(out)
        if para_initial:
            self.para_lines.append(out)
        return out

    def run(self, n_lines=1200):
        in_para = in_page = len(self.lines)
        for i in range(len(self.lines), n_lines):
            para_initial = in_para == 0
            if para_initial:
                self.paragraph_starts.append(len(self.lines))
            para_final = False
            in_para += 1
            in_page += 1
            if in_page == self.page_lines or i == n_lines - 1:
                para_final, in_para, in_page = True, 0, 0
            elif in_page < self.page_lines - 2 and in_para > 3 and i < n_lines - 2 and self.r(100) < in_para * 10:
                para_final, in_para = True, 0
            self.line(para_initial, para_final, in_page)
        return [[w.s for w in l] for l in self.lines]


def generate(n_lines=1200, seed=0, currier="B"):
    return AutoCopy(seed=seed, currier=currier).run(n_lines)
