"""voynich.ninja, Antonio Garcia Jimenez: "The Voynich is an astronomical-astrological code".

No language: each glyph is a sign. o = the degree of the sphere where the star
is; q (always before o) = the star rising; c, cc, ccc, cccc (EVA e, ee, eee,
eeee) = days of the Moon; gallows = coordinates, "always at first of the
paragraphs"; repeated words = stars almost in the same place.

A reading like this can't be checked against a language, but it makes
statements about where signs occur, and those can be counted.
"""
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
v = Voynich("ZL")
para = [l for l in v.lines if l.unit == "P" and l.words]
words = [w for l in para for w in l.words]
GALLOWS = "ktpf"

# gallows and paragraph starts
first_words = [l.words[0] for l in para if l.para_start]
starts_with_gallows = sum(w[0] in GALLOWS for w in first_words) / len(first_words)
g_tokens = sum(sum(c in GALLOWS for c in w) for w in words)
g_at_para_start = sum(1 for w in first_words if w[0] in GALLOWS)
by_gallows = []
for g in GALLOWS:
    tot = sum(w.count(g) for w in words)
    first_line = sum(w.count(g) for l in para if l.para_start for w in l.words)
    by_gallows.append({"gallows": g, "occurrences": tot, "in a paragraph's first line": first_line / tot,
                       "as the paragraph's first glyph": sum(1 for w in first_words if w[0] == g) / tot})
first_line_share = sum(len(l.words) for l in para if l.para_start) / len(words)

# q and o
q_total = sum(w.count("q") for w in words)
q_before_o = sum(len(re.findall("qo", w)) for w in words)
o_total = sum(w.count("o") for w in words)
o_after_q = q_before_o / o_total

# runs of e
runs = Counter()
for w in words:
    for m in re.finditer(r"e+", w):
        runs[len(m.group())] += 1
run_rows = [{"run": "e" * k, "count": runs[k], "share": runs[k] / sum(runs.values())} for k in sorted(runs)]

# immediate repeats by section: more where the stars are?
rep = []
for sec in sorted({l.section for l in para if l.section}):
    ls = [l.words for l in para if l.section == sec]
    pairs = sum(len(l) - 1 for l in ls)
    if pairs < 300:
        continue
    r = sum(a == b for l in ls for a, b in zip(l, l[1:]))
    rep.append({"section": sec, "adjacent pairs": pairs, "same word twice per 1000": 1000 * r / pairs})

facts = [
    {"claim": "gallows are always at the start of paragraphs",
     "count": f"{starts_with_gallows:.0%} of paragraphs open with a gallows, but only {g_at_para_start / g_tokens:.1%} of gallows are a paragraph's first glyph"},
    {"claim": "q goes before o like a prefix", "count": f"{q_before_o / q_total:.1%} of q are followed by o; {o_after_q:.0%} of o follow a q"},
    {"claim": "c, cc, ccc, cccc are days of the Moon (28 mansions)",
     "count": "runs of e: " + ", ".join(f"{'e' * k} {runs[k]}" for k in sorted(runs)) + "; nothing longer"},
]
save(HERE, "star_code", {"facts": facts, "gallows": by_gallows, "first_line_share_of_text": first_line_share,
                         "e_runs": run_rows, "repeats": rep})
md = "# c10 the star-code reading\n\n" + table(facts, ["claim", "count"])
md += f"\n## gallows\n\nFirst lines of paragraphs hold {first_line_share:.1%} of the text.\n\n" + table(
    by_gallows, ["gallows", "occurrences", "in a paragraph's first line", "as the paragraph's first glyph"])
md += "\n## runs of e\n\n" + table(run_rows, ["run", "count", "share"])
md += "\n## the same word twice in a row, by section\n\n" + table(rep, ["section", "adjacent pairs", "same word twice per 1000"])
write_md(HERE, "star_code", md)
print(md)
