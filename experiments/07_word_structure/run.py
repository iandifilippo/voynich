"""How rigid is glyph order inside a word, compared with real languages?

- bigram fill: share of possible glyph pairs that ever occur inside words
- positional entropy: for each glyph, how spread out its position in the word is
  (0 = always in the same relative slot), averaged by frequency
- predictability of the next glyph from the previous one *inside words only*
"""
import math
import pathlib
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, historical
from voynich.metrics import entropy

HERE = pathlib.Path(__file__).parent
N = 10000
BINS = 4


def stats(words):
    words = [w for w in words if w][:N]
    glyphs = Counter(c for w in words for c in w)
    bi = Counter(w[i:i + 2] for w in words for i in range(len(w) - 1))
    fill = len(bi) / (len(glyphs) ** 2)
    pos = defaultdict(Counter)
    for w in words:
        L = len(w)
        for i, c in enumerate(w):
            b = 0 if L == 1 else min(BINS - 1, int(BINS * i / L))
            pos[c][b] += 1
    tot = sum(glyphs.values())
    pent = sum(glyphs[c] / tot * entropy(pos[c]) for c in glyphs) / math.log2(BINS)
    # within-word conditional entropy
    prev = Counter(w[i] for w in words for i in range(len(w) - 1))
    h_cond = entropy(bi) - entropy(prev)
    start = Counter(w[0] for w in words)
    end = Counter(w[-1] for w in words)
    return {"alphabet": len(glyphs), "bigram_fill": fill, "positional_entropy": pent,
            "h_within_word": h_cond, "start_entropy": entropy(start), "end_entropy": entropy(end)}


rows = []
v = Voynich("ZL")
for name, ws in [("VMS ZL", v.words(unit="P")), ("VMS Currier A", v.words(language="A")),
                 ("VMS Currier B", v.words(language="B")), ("VMS GC alphabet", Voynich("GC").words(unit="P"))]:
    rows.append({"text": name, **stats(ws)})
for t in ["Latin_Aix", "Secreta_Secretorum_LAT", "Steganographia", "Rettorica", "Picatrix",
          "Agrippa_Book1", "Cirurgie", "Codex_Wormianus_dip", "Hebrew_Mishneh", "Amirandar"]:
    rows.append({"text": t, **stats(historical(t, N))})

# glyph slot profile for the VMS: where in the word each glyph lives
ws = [w for w in v.words(unit="P")][:N]
prof = defaultdict(Counter)
for w in ws:
    for i, c in enumerate(w):
        b = 0 if len(w) == 1 else min(BINS - 1, int(BINS * i / len(w)))
        prof[c][b] += 1
slots = []
for c, cnt in sorted(prof.items(), key=lambda kv: -sum(kv[1].values())):
    n = sum(cnt.values())
    if n < 50:
        continue
    slots.append({"glyph": c, "n": n, **{f"q{b + 1}": cnt[b] / n for b in range(BINS)}})

save(HERE, "word_structure", {"rows": rows, "slots": slots})
cols = ["text", "alphabet", "bigram_fill", "positional_entropy", "h_within_word", "start_entropy", "end_entropy"]
md = "# 07 word structure\n\nFirst 10k words of each text.\n\n" + table(rows, cols)
md += "\n## where each VMS glyph sits in the word (quarters of word length)\n\n"
md += table(slots, ["glyph", "n", "q1", "q2", "q3", "q4"], {f"q{i}": ".2f" for i in range(1, 5)})
write_md(HERE, "word_structure", md)
print(md)
