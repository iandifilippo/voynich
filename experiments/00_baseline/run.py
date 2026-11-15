"""Baseline facts about the ZL transliteration, by section, Currier language and hand."""
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, metrics

HERE = pathlib.Path(__file__).parent

v = Voynich("ZL")
words = v.words()
freq = Counter(words)
lines = v.text_lines(unit="P")

overall = metrics.profile(lines)
groups = []
for code in "HABCPSZT":
    ls = v.text_lines(section=[code])
    if sum(map(len, ls)) < 300:
        continue
    p = metrics.profile(ls)
    groups.append({"group": "section " + v.section_name(code), **p})
for lang in "AB":
    groups.append({"group": "Currier " + lang, **metrics.profile(v.text_lines(language=lang))})
for h in "12345":
    ls = v.text_lines(hand=h)
    if sum(map(len, ls)) >= 300:
        groups.append({"group": "hand " + h, **metrics.profile(ls)})

q = [w for w in words if "q" in w]
facts = {
    "lines": len(v.lines),
    "pages": len(v.pages),
    "tokens": len(words),
    "types": len(freq),
    "top30": freq.most_common(30),
    "q_initial": sum(w[0] == "q" for w in q) / len(q),
    "q_then_o": sum("qo" in w for w in q) / len(q),
    "uncertain_words_dropped": sum(l.uncertain for l in v.lines),
}

# gallows p/f on paragraph-first lines vs the rest
pf = {"first": [0, 0], "other": [0, 0]}
for l in v.select(unit="P"):
    s = "".join(l.words)
    k = "first" if l.para_start else "other"
    pf[k][0] += s.count("p") + s.count("f")
    pf[k][1] += len(s)
facts["pf_per_1000_first_line"] = 1000 * pf["first"][0] / pf["first"][1]
facts["pf_per_1000_other_lines"] = 1000 * pf["other"][0] / pf["other"][1]

save(HERE, "baseline", {"facts": facts, "overall": overall, "groups": groups})

cols = ["group", "tokens", "types", "hapax_ratio", "word_len", "h1", "h2", "edge_coupling", "line_first_jsd", "line_cohesion"]
md = "# 00 baseline\n\n"
md += f"ZL transliteration: {facts['pages']} pages, {facts['lines']} loci, {facts['tokens']} legible tokens, {facts['types']} types ({facts['uncertain_words_dropped']} tokens with uncertain glyphs dropped).\n\n"
md += "Top words: " + ", ".join(f"{w} {c}" for w, c in facts["top30"][:15]) + "\n\n"
md += f"- q is word-initial in {facts['q_initial']:.1%} of words containing it, followed by o in {facts['q_then_o']:.1%}\n"
md += f"- p+f per 1000 glyphs: {facts['pf_per_1000_first_line']:.1f} on paragraph-first lines vs {facts['pf_per_1000_other_lines']:.1f} elsewhere\n\n"
md += "## overall (paragraph text)\n\n" + table([{"group": "all P", **overall}], cols) + "\n"
md += "## by group\n\n" + table(groups, cols)
write_md(HERE, "baseline", md)
print(md)
