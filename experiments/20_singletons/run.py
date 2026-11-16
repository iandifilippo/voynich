"""What are the one-off words?

Exp. 19: the copying model can't make enough words that occur once (hapax
ratio 0.55 vs 0.69) even when it is more varied locally than the VMS. So what
are the VMS singletons, and what would a process need to do to make them?

For each text (first 10 000 words, whole lines):
  - share of types that are singletons
  - of the singletons: how many are one edit away from a word that occurs 2+
    times (a "copy with one change"), how many are two known words written
    together, how many are neither
  - length of singletons vs other words
  - where singletons sit in the line
For the VMS also: paragraph-opening words and labels.
"""
import pathlib
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, historical, chunk_lines
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA

HERE = pathlib.Path(__file__).parent
N = 10000


def edit1(a, b):
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


def take(lines, n=N):
    out, k = [], 0
    for l in lines:
        if k >= n:
            break
        if l:
            out.append(list(l))
            k += len(l)
    return out


def anatomy(lines):
    words = [w for l in lines for w in l]
    freq = Counter(words)
    single = [w for w, c in freq.items() if c == 1]
    known = {w for w, c in freq.items() if c >= 2}
    index = defaultdict(set)
    for w in known:
        index[w].add(w)
        for i in range(len(w)):
            index[w[:i] + w[i + 1:]].add(w)
    near = joined = neither = 0
    for w in single:
        cands = set(index.get(w, ()))
        for i in range(len(w)):
            cands |= index.get(w[:i] + w[i + 1:], set())
        is_near = any(edit1(w, c) for c in cands)
        is_join = any(w[:i] in known and w[i:] in known for i in range(2, len(w) - 1))
        near += is_near
        joined += (not is_near) and is_join
        neither += not (is_near or is_join)
    pos = {"first": [0, 0], "middle": [0, 0], "last": [0, 0]}
    for l in lines:
        if len(l) < 3:
            continue
        for i, w in enumerate(l):
            k = "first" if i == 0 else "last" if i == len(l) - 1 else "middle"
            pos[k][0] += freq[w] == 1
            pos[k][1] += 1
    ns = len(single)
    return {"words": len(words), "types": len(freq), "singleton_share_of_types": ns / len(freq),
            "singleton_share_of_tokens": ns / len(words),
            "one_edit_from_known": near / ns, "two_known_joined": joined / ns, "neither": neither / ns,
            "neither_per_1000_tokens": 1000 * neither / len(words),
            "len_singleton": statistics.mean(map(len, single)),
            "len_other": statistics.mean(len(w) for w in words if freq[w] > 1),
            "rate_first": pos["first"][0] / pos["first"][1], "rate_middle": pos["middle"][0] / pos["middle"][1],
            "rate_last": pos["last"][0] / pos["last"][1]}


v = Voynich("ZL")
texts = {
    "VMS Currier A": take(v.text_lines(unit="P", language="A")),
    "VMS Currier B": take(v.text_lines(unit="P", language="B")),
    "VMS B, smart commas": take(Voynich("ZL", commas="smart").text_lines(unit="P", language="B")),
    "copying model (B)": take(AutoCopy(seed=1, currier="B").run(1500)),
    "copying model (A)": take(AutoCopy(seed=1, currier="A").run(1500)),
    "Latin (Aix)": take(chunk_lines(historical("Latin_Aix", 12000))),
    "Italian (Rettorica)": take(chunk_lines(historical("Rettorica", 12000))),
}
src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
if src.exists():
    texts["Naibbe (Pliny)"] = take([l.split() for l in open(src, encoding="utf-8-sig") if l.split()])

rows = []
for name, lines in texts.items():
    r = anatomy(lines)
    r["text"] = name
    rows.append(r)
    print(name, {k: round(x, 3) if isinstance(x, float) else x for k, x in r.items()})

# VMS only: paragraph openers and labels, whole manuscript
allw = Counter(w for l in v.lines for w in l.words)
para = [l for l in v.lines if l.unit == "P" and l.words]
opener = [l.words[0] for l in para if l.para_start]
line_first = [l.words[0] for l in para if not l.para_start]
other = [w for l in para for w in l.words[1:]]
labels = [w for l in v.lines if l.unit == "L" for w in l.words]
where = [{"position": k, "words": len(ws), "singleton_rate": sum(allw[w] == 1 for w in ws) / len(ws),
          "mean_len": statistics.mean(map(len, ws))}
         for k, ws in [("paragraph-opening word", opener), ("other line-first words", line_first),
                       ("rest of paragraph text", other), ("labels", labels)]]
total_single = sum(1 for w, c in allw.items() if c == 1)
share_opener = sum(allw[w] == 1 for w in opener) / total_single
share_label = sum(allw[w] == 1 for w in labels) / total_single

# which single change links a singleton to a known word, by line position (VMS only)
def links(w, known, by_len):
    out = set()
    for i in range(len(w)):
        if w[:i] + w[i + 1:] in known:
            out.add(("added", "start" if i == 0 else "end" if i == len(w) - 1 else "inside", w[i]))
    for k in by_len.get(len(w), ()):
        d = [i for i in range(len(w)) if w[i] != k[i]]
        if len(d) == 1:
            out.add(("changed", "start" if d[0] == 0 else "end" if d[0] == len(w) - 1 else "inside", w[d[0]]))
    for k in by_len.get(len(w) + 1, ()):
        for i in range(len(k)):
            if k[:i] + k[i + 1:] == w:
                out.add(("dropped", "start" if i == 0 else "end" if i == len(k) - 1 else "inside", k[i]))
                break
    return out


edges, glyphs = [], {}
for lang in ("A", "B"):
    ls = [l for l in v.text_lines(unit="P", language=lang) if len(l) >= 3]
    f = Counter(w for l in ls for w in l)
    known = {w for w, c in f.items() if c >= 2}
    by_len = defaultdict(list)
    for k in known:
        by_len[len(k)].append(k)
    for name, sel in [("first", lambda l: l[:1]), ("middle", lambda l: l[1:-1]), ("last", lambda l: l[-1:])]:
        single = [w for l in ls for w in sel(l) if f[w] == 1]
        c, g = Counter(), Counter()
        for w in single:
            lk = links(w, known, by_len)
            for kind in {(a, b) for a, b, _ in lk}:
                c[kind] += 1
            for a, b, ch in lk:
                if a == "added" and b in ("start", "end"):
                    g[b, ch] += 1
        r = {"language": lang, "position": name, "singletons": len(single)}
        for a in ("added", "changed", "dropped"):
            for b in ("start", "inside", "end"):
                r[f"{a}_{b}"] = c[a, b] / len(single)
        edges.append(r)
        glyphs[lang, name] = g
top_added = []
for lang in ("A", "B"):
    for name, side in [("first", "start"), ("last", "end"), ("middle", "start"), ("middle", "end")]:
        g = glyphs[lang, name]
        tot = sum(c for (b, _), c in g.items() if b == side)
        top_added.append({"language": lang, "position": name, "side": side, "n": tot,
                          "glyphs": ", ".join(f"{ch} {c / tot:.0%}" for (b, ch), c in
                                              sorted(g.items(), key=lambda x: -x[1]) if b == side)[:80]})

save(HERE, "singletons", {"texts": rows, "vms_positions": where, "edges": edges, "added_glyphs": top_added,
                          "share_of_all_singletons_in_openers": share_opener,
                          "share_of_all_singletons_in_labels": share_label})
md = "# 20 singletons\n\n## how many, and what they look like (first 10 000 words)\n\n"
md += table(rows, ["text", "types", "singleton_share_of_types", "one_edit_from_known", "two_known_joined",
                   "neither", "neither_per_1000_tokens", "len_singleton", "len_other"])
md += "\n`one_edit_from_known`: one glyph added, dropped or changed from a word that occurs 2+ times in the same sample. `two_known_joined`: not that, but splits into two such words. \n"
md += "\n## where they sit in the line (share of words in that position that are singletons)\n\n"
md += table(rows, ["text", "rate_first", "rate_middle", "rate_last"])
md += "\n## VMS, whole manuscript\n\n" + table(where, ["position", "words", "singleton_rate", "mean_len"])
md += f"\nParagraph openers hold {share_opener:.1%} of all singletons, labels {share_label:.1%}.\n"
md += "\n## how VMS singletons differ from the nearest known word, by line position\n\n"
md += table(edges, ["language", "position", "singletons", "added_start", "added_inside", "added_end",
                    "changed_start", "changed_inside", "changed_end", "dropped_start", "dropped_inside", "dropped_end"])
md += "\nShare of singletons in that position that are a known word with one glyph added / changed / dropped at the start, inside or at the end (a singleton can count in several columns).\n"
md += "\n## which glyph is added at the edge\n\n" + table(top_added, ["language", "position", "side", "n", "glyphs"])
write_md(HERE, "singletons", md)
print(md)
