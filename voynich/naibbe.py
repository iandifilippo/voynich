"""Naibbe cipher using Greshko's published tables, plus variants.

Tables and respaced plaintexts come from github.com/greshko/naibbe-cipher
(fetched into data/external/ by python -m voynich.download).
Greshko, M. A. (2025). The Naibbe cipher: a substitution cipher that encrypts
Latin and Italian as Voynich Manuscript-like ciphertext. Cryptologia.
doi:10.1080/01611194.2025.2566408

The encryption below follows his naibbe_v2.py (weighted 78-card deck, one
card per unigram / per half of a bigram, ambiguity-safe bigrams). Variants:

- table_rule="autokey": the table for the next word's first half is read off
  the last glyph of the word just written (a fixed glyph -> table chart), with
  probability `autokey_p`; otherwise a card is drawn as usual.
- linestart(): Smith's line-start transformation applied after the fact: at
  the start of a line a glyph is prefixed with probability q, and paragraphs
  open with a gallows.
"""
import csv
import random
from collections import defaultdict

from .corpus import DATA

ROOT = DATA / "external" / "naibbe-cipher"
TABLES = ["alpha", "beta1", "beta2", "beta3", "gamma1", "gamma2"]
WEIGHTS = {"alpha": 28, "beta1": 14, "beta2": 11, "beta3": 11, "gamma1": 7, "gamma2": 7}

DEFAULT_CHART = {"y": "alpha", "n": "beta1", "l": "beta2", "r": "beta3",
                 "s": "gamma1", "m": "gamma1", "o": "gamma2"}


def load_tables():
    glyph = {}
    with open(ROOT / "references" / "naibbe_tables.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            glyph[row["code"]] = row["glyphs"]
    return glyph


def load_units(name="nathist"):
    path = ROOT / "respaced_plaintext" / f"{name}_pre_encryption_respaced_plaintext.txt"
    return [line.split() for line in open(path, encoding="utf-8") if line.split()]


class Deck:
    def __init__(self, rng):
        self.rng = rng
        self.cards = []

    def draw(self):
        if not self.cards:
            self.cards = [t for t, n in WEIGHTS.items() for _ in range(n)]
            self.rng.shuffle(self.cards)
        return self.cards.pop()


class Naibbe:
    def __init__(self, seed=0, table_rule="deck", autokey_p=1.0, chart=None):
        self.g = load_tables()
        self.rng = random.Random(seed)
        self.deck = Deck(self.rng)
        self.rule = table_rule
        self.p = autokey_p
        self.chart = DEFAULT_CHART if chart is None else chart
        self.unigrams = {v for k, v in self.g.items() if k.startswith("unigram_")}
        self.catalog = defaultdict(set)
        letters = sorted({k.split("_")[2] for k in self.g})
        for t1 in TABLES:
            for a in letters:
                pc = f"prefix_{t1}_{a}"
                for t2 in TABLES:
                    for b in letters:
                        sc = f"suffix_{t2}_{b}"
                        if pc in self.g and sc in self.g:
                            self.catalog[self.g[pc] + self.g[sc]].add((pc, sc))

    def first_table(self, prev):
        if self.rule == "autokey" and prev and self.rng.random() < self.p:
            return self.chart.get(prev[-1], "alpha")
        return self.deck.draw()

    def word(self, unit, prev):
        if len(unit) == 1:
            return self.g[f"unigram_{self.first_table(prev)}_{unit}"]
        last = None
        for _ in range(10000):
            t1 = self.first_table(prev)
            t2 = self.deck.draw()
            pc, sc = f"prefix_{t1}_{unit[0]}", f"suffix_{t2}_{unit[1]}"
            w = self.g[pc] + self.g[sc]
            last = w
            if w in self.unigrams:
                continue
            if any(pair != (pc, sc) for pair in self.catalog.get(w, ())):
                continue
            return w
        return last

    def encrypt(self, unit_lines):
        out = []
        for units in unit_lines:
            prev, line = None, []
            for u in units:
                if not all(f"unigram_alpha_{c}" in self.g for c in u):
                    continue
                w = self.word(u, prev)
                line.append(w)
                prev = w
            out.append(line)
        return out


def relineate(words, line_lengths, para_lengths, rng):
    """Cut a word stream into lines and paragraphs with given length distributions."""
    lines, paras, i = [], [], 0
    while i < len(words):
        n_lines = rng.choice(para_lengths)
        para = []
        for _ in range(n_lines):
            if i >= len(words):
                break
            k = rng.choice(line_lengths)
            para.append(words[i:i + k])
            i += k
        paras.append(para)
    return paras


def linestart(paras, q=0.3, gallows_p=0.85, seed=0):
    """Smith's transformation: prefix s/d/t to line-initial words with probability q,
    and a gallows to paragraph-initial words with probability gallows_p."""
    rng = random.Random(seed)
    out = []
    for para in paras:
        for j, line in enumerate(para):
            if not line:
                continue
            line = line[:]
            if j == 0:
                if rng.random() < gallows_p:
                    line[0] = rng.choice(["p", "t", "k", "f"]) + line[0]
            elif rng.random() < q:
                w = line[0]
                g = "d" if w.startswith(("ch", "sh")) else rng.choice(["s", "s", "d", "t"])
                line[0] = g + w
            out.append(line)
    return out
