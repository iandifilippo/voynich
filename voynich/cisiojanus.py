"""Cisiojanus: one syllable per day of the year."""
import pathlib
import re
import unicodedata
from collections import defaultdict

PATH = pathlib.Path(__file__).resolve().parent.parent / "corpora" / "cisiojanus_latin.txt"
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
VOWELS = "aeiouy"
DIPHTHONGS = ("ae", "au", "oe", "eu")


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def syllabify(word):
    """Rough Latin syllabification: one syllable per vowel nucleus, diphthongs count once,
    'qu' and 'gu' before a vowel keep the u as a consonant."""
    w = strip_accents(word.lower())
    w = re.sub(r"(q|g)u(?=[aeiouy])", r"\1w", w)
    nuclei = []
    i = 0
    while i < len(w):
        if w[i] in VOWELS:
            j = i + 2 if w[i:i + 2] in DIPHTHONGS else i + 1
            nuclei.append((i, j))
            i = j
        else:
            i += 1
    if not nuclei:
        return [w]
    sylls, start = [], 0
    for k, (a, b) in enumerate(nuclei):
        if k + 1 < len(nuclei):
            nxt = nuclei[k + 1][0]
            cons = w[b:nxt]
            cut = b + (len(cons) - 1 if len(cons) > 1 else 0) if cons else b
            sylls.append(w[start:cut])
            start = cut
        else:
            sylls.append(w[start:])
    return [s.replace("w", "u") for s in sylls]


def months():
    out = defaultdict(list)
    for line in PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        m, text = line.split(" ", 1)
        for word in text.replace("|", " ").split():
            out[int(m)].extend(syllabify(word))
    return dict(out)
