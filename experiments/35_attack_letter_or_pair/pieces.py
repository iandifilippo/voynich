"""Is there a closed table of halves?

A Naibbe-type cipher builds its two-letter words from a fixed table of first
halves and second halves, a few hundred in all. However much text is
enciphered, no new halves appear. This counts the distinct pieces the
segmenter finds as the text grows, in the Naibbe cipher, the manuscript and
the copying model, all cut the same way (k = 110).
"""
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich.crack import segment

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from run import TEXTS  # noqa: E402

HERE = pathlib.Path(__file__).parent
rows = []
for name, words in TEXTS.items():
    for n in (2500, 5000, 10000, 20000):
        if n > len(words):
            continue
        ws = words[:n]
        seg = segment.fit_ranked(Counter(ws), 110)
        c = Counter()
        for w in ws:
            s = seg[w]
            c.update([("W", s[0])] if len(s) == 1 else [("F", s[0]), ("S", s[1])])
        tot = sum(c.values())
        top = c.most_common()
        rows.append({"text": name, "words": n, "distinct words": len(set(ws)),
                     "first halves": sum(1 for k in c if k[0] == "F"),
                     "second halves": sum(1 for k in c if k[0] == "S"),
                     "pieces": len(c), "pieces seen once": sum(1 for x in c.values() if x == 1) / len(c),
                     "text covered by 400 commonest pieces": sum(x for _, x in top[:400]) / tot})
save(HERE, "pieces", rows)
md = "# 35 inventory of halves\n\n" + table(rows, ["text", "words", "distinct words", "first halves", "second halves",
                                                    "pieces", "pieces seen once", "text covered by 400 commonest pieces"])
write_md(HERE, "pieces", md)
print(md)
