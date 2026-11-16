"""Is EVA cutting the script into the wrong pieces?

Two recent arguments: Rozanova & Temerev (arXiv:2608.17096) say EVA glyphs act
like pieces of recurring multi-glyph units; a Reddit thread ("Is it too late to
rethink EVA?", Nov 2026) proposes reading the script as stroke "particles".
Either way the question is the same: is there a way of grouping EVA glyphs into
bigger units that makes the text look like a normal alphabetic language?

Byte-pair merging is the neutral way to try every grouping the data itself
suggests: repeatedly fuse the most frequent adjacent pair inside words into one
symbol. We track the alphabet size and the conditional entropy h2 as merges
pile up, for the VMS and for Latin, Italian and English run through the same
procedure. If some merge depth puts the VMS on the natural-language curve, a
better transliteration could exist; if the gap stays, re-cutting EVA doesn't fix it.
"""
import math
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich import Voynich, historical
from voynich.metrics import entropy

HERE = pathlib.Path(__file__).parent
N = 10000
CHECK = [0, 5, 10, 20, 40, 80, 120]


def h_stats(seqs):
    stream = []
    for s in seqs:
        stream += s + [" "]
    uni = Counter(stream)
    bi = Counter(zip(stream, stream[1:]))
    h1 = entropy(uni)
    return len(uni), h1, entropy(bi) - h1


def bpe_curve(words):
    seqs = [list(w) for w in words[:N]]
    out = []
    for step in range(max(CHECK) + 1):
        if step in CHECK:
            a, h1, h2 = h_stats(seqs)
            out.append({"merges": step, "alphabet": a, "h1": h1, "h2": h2,
                        "h2_over_log2_alphabet": h2 / math.log2(a), "mean_units_per_word": sum(map(len, seqs)) / len(seqs)})
        pairs = Counter((s[i], s[i + 1]) for s in seqs for i in range(len(s) - 1))
        if not pairs:
            break
        (a, b), _ = pairs.most_common(1)[0]
        new = []
        for s in seqs:
            t, i = [], 0
            while i < len(s):
                if i + 1 < len(s) and s[i] == a and s[i + 1] == b:
                    t.append(a + b)
                    i += 2
                else:
                    t.append(s[i])
                    i += 1
            new.append(t)
        seqs = new
    return out


texts = {"VMS (ZL)": Voynich("ZL").words(unit="P"), "VMS Currier B": Voynich("ZL").words(language="B"),
         "Latin": historical("Latin_Aix"), "Latin (med.)": historical("Secreta_Secretorum_LAT"),
         "Italian": historical("Rettorica"), "English": historical("Agrippa_Book1")}
rows = []
for name, ws in texts.items():
    for r in bpe_curve(ws):
        rows.append({"text": name, **r})

save(HERE, "glyph_units", rows)
md = "# c05 re-cutting EVA into bigger units\n\n"
md += "h2 = conditional entropy of the next unit given the previous one. `h2_over_log2_alphabet` normalises for alphabet size so different cuts can be compared.\n\n"
md += table(rows, ["text", "merges", "alphabet", "h1", "h2", "h2_over_log2_alphabet", "mean_units_per_word"])
write_md(HERE, "glyph_units", md)
print(md)
