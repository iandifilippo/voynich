"""r/voynich, u/Worldmaster777 (2025): "The word 'tolor' means 'fertilization'".

Claims, as stated in the post:
 1. 'tolor' occurs only 3 times: tolor (f38r) and otolor (f67r2, f77v).
 2. A word with 2-5 occurrences sitting on three "fertilization" pictures is
    unlikely to be chance.
 3. Grammar: o- works like an article ('the'); gallows mark part of speech
    (t- noun, k- verb); final -l / -r mark feminine / masculine.

Checks
 A. the occurrences and where they sit (paragraph text or label)
 B. look-elsewhere: how many other pairs X / oX have the same layout
    (X opening a paragraph, oX as a label, 2-5 occurrences in all)
 C. gender: if -l/-r were gender endings, neighbouring words would agree
    (Russian adjective + noun, Italian -a/-o). Test agreement against words
    shuffled within their line; calibrate on Italian and Latin.
 D. o- as an article and t-/k- as noun/verb: compare the contexts of
    minimal pairs X/oX and tX/kX with frequency-matched random pairs.
"""
import math
import random
import re
import statistics
from collections import Counter, defaultdict
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401

from _common import save, table, write_md
from voynich import Voynich, historical, chunk_lines

HERE = pathlib.Path(__file__).parent
v = Voynich("ZL")
para = [l for l in v.lines if l.unit == "P"]
labels = [l for l in v.lines if l.unit == "L"]
allw = [w for l in v.lines for w in l.words]
freq = Counter(allw)

# A ---------------------------------------------------------------------
occ = [{"page": l.page, "locus": l.locus, "unit": l.unit, "position": i,
        "word": w, "line": " ".join(l.words)}
       for l in v.lines for i, w in enumerate(l.words) if "tolor" in w]

# B ---------------------------------------------------------------------
para_first = Counter(l.words[0] for l in para if l.para_start and l.words)
label_words = Counter(w for l in labels for w in l.words)
sub_count = lambda s: sum(c for w, c in freq.items() if s in w)
same_layout = []
for x in para_first:
    if len(x) < 4:
        continue
    ox = "o" + x
    if label_words.get(ox) and 2 <= sub_count(x) <= 5:
        same_layout.append({"opening word": x, "label": ox, "substring count": sub_count(x)})
# looser: any word X opening a paragraph with o+X anywhere, no count limit
loose = sum(1 for x in para_first if len(x) >= 4 and freq.get("o" + x))
n_rare = sum(1 for w, c in freq.items() if 2 <= c <= 5)
first_unique = sum(1 for x in para_first if freq[x] == 1) / len(para_first)


# C ---------------------------------------------------------------------
def agreement(lines, a, b, reps=300, seed=0):
    """log odds ratio of (prev ends a/b, next ends a/b) for adjacent words,
    against words shuffled inside their line."""
    def lor(ls):
        c = Counter()
        for l in ls:
            for x, y in zip(l, l[1:]):
                ex = a if x.endswith(a) else b if x.endswith(b) else None
                ey = a if y.endswith(a) else b if y.endswith(b) else None
                if ex and ey:
                    c[ex, ey] += 1
        n = [c[a, a], c[a, b], c[b, a], c[b, b]]
        n = [k + 0.5 for k in n]
        return math.log(n[0] * n[3] / (n[1] * n[2])), sum(c.values())
    obs, n = lor(lines)
    rng = random.Random(seed)
    null = [lor([rng.sample(l, len(l)) for l in lines])[0] for _ in range(reps)]
    mu, sd = statistics.mean(null), statistics.pstdev(null)
    p = (1 + sum(x >= obs for x in null)) / (reps + 1)
    return {"pairs": n, "log_odds": obs, "null": mu, "z": (obs - mu) / sd if sd else 0, "p_agree": p}


gender = []
for name, lines, a, b in [
    ("VMS paragraphs, -l vs -r", v.text_lines(unit="P"), "l", "r"),
    ("VMS Currier A, -l vs -r", v.text_lines(unit="P", language="A"), "l", "r"),
    ("VMS Currier B, -l vs -r", v.text_lines(unit="P", language="B"), "l", "r"),
    ("VMS paragraphs, -y vs -n (control)", v.text_lines(unit="P"), "y", "n"),
    ("Italian (Rettorica), -a vs -o", chunk_lines(historical("Rettorica", 40000)), "a", "o"),
    ("Latin (Aix), -a vs -us", chunk_lines(historical("Latin_Aix", 40000)), "a", "us"),
    ("Latin (Aix), -am vs -um", chunk_lines(historical("Latin_Aix", 40000)), "am", "um"),
]:
    r = agreement(lines, a, b)
    r["text"] = name
    gender.append(r)
    print(r)


# D ---------------------------------------------------------------------
def contexts(lines):
    ctx = defaultdict(Counter)
    for l in lines:
        for i, w in enumerate(l):
            if i:
                ctx[w]["L:" + l[i - 1]] += 1
            if i < len(l) - 1:
                ctx[w]["R:" + l[i + 1]] += 1
    return ctx


def cos(p, q):
    num = sum(p[k] * q[k] for k in p if k in q)
    den = math.sqrt(sum(x * x for x in p.values()) * sum(x * x for x in q.values()))
    return num / den if den else 0.0


pl = v.text_lines(unit="P")
ctx = contexts(pl)
tf = Counter(w for l in pl for w in l)
common = [w for w, c in tf.items() if c >= 8]
cs = set(common)


def pairs_where(rule):
    return [(x, y) for x in common for y in [rule(x)] if y and y in cs and y != x]


def swap_gallows(x):
    if "t" in x and "k" not in x and x.count("t") == 1:
        return x.replace("t", "k")
    return None


def lr(x):
    return x[:-1] + "r" if x.endswith("l") else None


rng = random.Random(1)
by_freq = sorted(common, key=lambda w: tf[w])
rank = {w: i for i, w in enumerate(by_freq)}


def matched_random(pairs, k=20):
    out = []
    for x, y in pairs:
        for _ in range(k):
            j = min(len(by_freq) - 1, max(0, rank[y] + rng.randint(-15, 15)))
            z = by_freq[j]
            if z not in (x, y):
                out.append(cos(ctx[x], ctx[z]))
    return out


sims = []
for name, rule in [("X / oX (o- as article)", lambda x: "o" + x),
                   ("tX / kX (t noun, k verb)", swap_gallows),
                   ("Xl / Xr (feminine / masculine)", lr),
                   ("X / qX (control prefix)", lambda x: "q" + x if x.startswith("o") else None),
                   ("X / yX (control prefix)", lambda x: "y" + x)]:
    ps = pairs_where(rule)
    if not ps:
        continue
    s = [cos(ctx[x], ctx[y]) for x, y in ps]
    rnd = matched_random(ps)
    sims.append({"pairs": name, "n": len(ps), "context_cosine": statistics.mean(s),
                 "random_matched": statistics.mean(rnd), "ratio": statistics.mean(s) / statistics.mean(rnd),
                 "examples": ", ".join(f"{x}/{y}" for x, y in sorted(ps, key=lambda p: -tf[p[0]])[:5])})
    print(sims[-1])

save(HERE, "tolor", {"occurrences": occ, "same_layout": same_layout, "loose_layout": loose,
                     "word_types_2_to_5": n_rare, "paragraph_first_unique_share": first_unique,
                     "gender": gender, "contexts": sims})
md = "# c06 'tolor' = fertilization\n\n## A. the occurrences\n\n" + table(occ, ["page", "locus", "unit", "position", "word", "line"])
md += "\n`unit` P = paragraph text, L = label.\n"
md += f"\n## B. look-elsewhere\n\n{n_rare} word types occur 2-5 times. {first_unique:.0%} of paragraph-opening words occur nowhere else. "
md += f"Paragraph-opening words X (4+ glyphs) for which oX also exists somewhere: {loose}. Same layout as tolor/otolor (X opens a paragraph, oX is a label, 2-5 occurrences in all):\n\n"
md += table(same_layout, ["opening word", "label", "substring count"]) if same_layout else "(none besides)\n"
md += "\n## C. do -l / -r endings agree like gender?\n\n" + table(gender, ["text", "pairs", "log_odds", "null", "z", "p_agree"])
md += "\nPositive log odds above the within-line null = neighbours tend to share the ending.\n"
md += "\n## D. contexts of minimal pairs\n\n" + table(sims, ["pairs", "n", "context_cosine", "random_matched", "ratio", "examples"])
md += "\nCosine of left/right neighbour counts (paragraph text, words with 8+ occurrences). `random_matched`: the first word against random words of similar frequency.\n"
write_md(HERE, "tolor", md)
print(md)
