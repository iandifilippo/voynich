"""Hand-executable text transformations a 15th c. scribe could have used,
plus generators for the main "meaningless text" hypotheses.

Each function takes plaintext words and returns cipher words. None of these
is claimed to be *the* Voynich method; they exist to be scored by benchmark.py.
"""
import random
import re
import string

EVA_GLYPHS = list("acdefhiklmnopqrsty")

PREFIX = ["", "", "q", "o", "qo", "ch", "sh", "d", "s", "y", "ol"]
GALLOWS = ["", "", "k", "t", "ke", "te", "ckh", "cth", "p", "f"]
BODY = ["", "e", "ee", "o", "a", "ch", "sh"]
SUFFIX = ["dy", "y", "in", "iin", "r", "l", "ol", "al", "ar", "or", "aiin", "ain", "am", "s", "edy", "ey"]


def _letters(words):
    return [re.sub(r"[^a-z]", "", w) for w in words if re.sub(r"[^a-z]", "", w)]


def plain(words, seed=0):
    return _letters(words)


def substitution(words, seed=0):
    rng = random.Random(seed)
    src = list(string.ascii_lowercase)
    dst = src[:]
    rng.shuffle(dst)
    key = dict(zip(src, dst))
    return ["".join(key[c] for c in w) for w in _letters(words)]


def homophonic(words, seed=0, homophones=3):
    rng = random.Random(seed)
    symbols = [a + b for a in EVA_GLYPHS for b in EVA_GLYPHS]
    rng.shuffle(symbols)
    key, i = {}, 0
    for c in string.ascii_lowercase:
        key[c] = symbols[i:i + homophones]
        i += homophones
    return ["".join(rng.choice(key[c]) for c in w) for w in _letters(words)]


def verbose(words, seed=0):
    """Each letter becomes a fixed short glyph group (letters -> 'syllables' of glyphs)."""
    rng = random.Random(seed)
    pieces = list({g + b for g in GALLOWS for b in BODY if g + b} | set(SUFFIX))
    rng.shuffle(pieces)
    key = dict(zip(string.ascii_lowercase, pieces))
    return ["".join(key[c] for c in w) for w in _letters(words)]


def _syllables(w):
    return re.findall(r"[^aeiouy]*[aeiouy]+(?:[^aeiouy]*$)?", w) or [w]


def _codeword(rng):
    return rng.choice(PREFIX) + rng.choice(GALLOWS) + rng.choice(BODY) + rng.choice(SUFFIX)


def syllable_code(words, seed=0):
    """Nomenclator-style: every plaintext syllable becomes one code word."""
    rng = random.Random(seed)
    book, out = {}, []
    for w in _letters(words):
        for s in _syllables(w):
            if s not in book:
                cw = _codeword(rng)
                while not cw:
                    cw = _codeword(rng)
                book[s] = cw
            out.append(book[s])
    return out


def naibbe_like(words, seed=0, tables=6):
    """Verbose homophonic cipher in the spirit of Greshko (2025): plaintext is cut
    into unigrams and bigrams at random, and each chunk is enciphered with one of
    several tables chosen at random (dice/cards). Tables map chunks to slot-built
    words, so every chunk becomes one cipher word. Not his actual tables."""
    rng = random.Random(seed)
    keys = [dict() for _ in range(tables)]
    out = []
    for w in _letters(words):
        i = 0
        while i < len(w):
            n = 2 if (i + 1 < len(w) and rng.random() < 0.5) else 1
            chunk = w[i:i + n]
            t = keys[rng.randrange(tables)]
            if chunk not in t:
                t[chunk] = _codeword(rng) or "o"
            out.append(t[chunk])
            i += n
    return out


MUTATIONS = [("e", "ee"), ("ee", "e"), ("k", "t"), ("t", "k"), ("o", "a"), ("a", "o"),
             ("y", "dy"), ("dy", "y"), ("ch", "sh"), ("sh", "ch"), ("in", "iin"), ("iin", "in"),
             ("r", "l"), ("l", "r"), ("qo", "o"), ("o", "qo"), ("d", "s"), ("s", "d")]


def self_citation(n_words, seed=0, line_len=9, memory=60):
    """Timm & Schinner style: each new word copies a recent word and maybe mutates it."""
    rng = random.Random(seed)
    lines = [[_codeword(rng) for _ in range(line_len)] for _ in range(3)]
    total = 3 * line_len
    while total < n_words:
        line = []
        recent = [w for l in lines[-6:] for w in l][-memory:]
        for j in range(line_len):
            src = lines[-1][j] if (j < len(lines[-1]) and rng.random() < 0.35) else rng.choice(recent)
            w = src
            for _ in range(rng.choice([0, 1, 1, 2])):
                a, b = rng.choice(MUTATIONS)
                if a in w:
                    w = w.replace(a, b, 1)
            line.append(w or src)
        lines.append(line)
        total += line_len
    return lines


def shuffle_glyphs(words, seed=0):
    """Control: keep word lengths, scramble glyphs across the whole text."""
    rng = random.Random(seed)
    glyphs = [c for w in words for c in w]
    rng.shuffle(glyphs)
    out, i = [], 0
    for w in words:
        out.append("".join(glyphs[i:i + len(w)]))
        i += len(w)
    return out


METHODS = {
    "plain": plain,
    "substitution": substitution,
    "homophonic": homophonic,
    "verbose": verbose,
    "syllable_code": syllable_code,
    "naibbe_like": naibbe_like,
}
