"""Labels that appear more than once.

Labels sit next to drawings (plants, jars, nymphs, stars). If a label names the
thing drawn, a repeated label should come back next to a similar drawing, and
repeated labels should mostly stay inside one section. Here we only have the
text side: which labels repeat, where, and whether repeats stay within a
section more than chance. The list is meant for checking against the scans.
"""
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
v = Voynich("ZL")

labels = []
for l in v.select(unit="L"):
    if len(l.words) == 1 and len(l.words[0]) >= 4:
        labels.append((l.words[0], l.locus, l.page, v.section_name(l.section)))

where = defaultdict(list)
for w, loc, page, sec in labels:
    where[w].append((loc, page, sec))
repeated = {w: locs for w, locs in where.items() if len({p for _, p, _ in locs}) >= 2}

text_freq = Counter(v.words(unit="P"))


def same_section_share(assign):
    same = tot = 0
    groups = defaultdict(list)
    for w, sec in assign:
        groups[w].append(sec)
    for w, secs in groups.items():
        for i in range(len(secs)):
            for j in range(i + 1, len(secs)):
                tot += 1
                same += secs[i] == secs[j]
    return same / tot if tot else 0.0, tot


assign = [(w, sec) for w, _, _, sec in labels]
obs, pairs = same_section_share([a for a in assign if a[0] in repeated])
rng = random.Random(0)
words = [w for w, _ in assign]
secs = [s for _, s in assign]
null = []
for _ in range(2000):
    rng.shuffle(secs)
    sh = list(zip(words, secs))
    null.append(same_section_share([a for a in sh if a[0] in repeated])[0])
p = sum(x >= obs for x in null) / len(null)

rows = []
for w, locs in sorted(repeated.items(), key=lambda kv: -len(kv[1])):
    rows.append({"label": w, "times": len(locs), "pages": len({p for _, p, _ in locs}),
                 "sections": ", ".join(sorted({s for _, _, s in locs})),
                 "in_running_text": text_freq.get(w, 0),
                 "where": " ".join(loc for loc, _, _ in locs[:8])})

cross = [r for r in rows if "," in r["sections"]]
res = {"labels": len(labels), "distinct": len(where), "repeated": len(repeated),
       "same_section_share": obs, "pairs": pairs, "null_mean": sum(null) / len(null), "p": p,
       "rows": rows}
save(HERE, "label_reuse", res)
md = "# 11 label reuse\n\n"
md += f"{len(labels)} single-word labels (4+ glyphs), {len(where)} distinct, {len(repeated)} occur on 2+ pages.\n\n"
md += f"Pairs of occurrences of the same label that fall in the same section: **{obs:.1%}** of {pairs} pairs; with sections shuffled: {res['null_mean']:.1%} (p = {p:.4f}).\n\n"
md += f"Labels repeated across different sections ({len(cross)}): worth checking the drawings side by side.\n\n"
md += table(cross, ["label", "times", "pages", "sections", "in_running_text", "where"])
md += "\n## all repeated labels\n\n" + table(rows, ["label", "times", "pages", "sections", "in_running_text", "where"])
write_md(HERE, "label_reuse", md)
print(md[:3500])
