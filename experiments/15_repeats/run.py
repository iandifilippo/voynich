"""Why do Voynich words repeat right next to each other?

Immediate repeats (qokedy qokedy) and near-repeats (qokedy qokeedy, one glyph
apart) are a known oddity, and nothing benchmarked so far (ciphers, autokey,
line-start rule) produces them. Questions:

1. How far above chance are they? Two baselines: words shuffled within each
   line (keeps line composition) and shuffled across the whole text.
2. Where do they sit in the line? Across line breaks?
3. Which words repeat, and is it just the frequent ones?
4. Same measures for natural texts (pseudo-lines of 9 words) and for cipher output.
"""
import pathlib
import random
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, historical, chunk_lines, naibbe

HERE = pathlib.Path(__file__).parent


def edit1(a, b):
    """True if a and b differ by exactly one substitution, insertion or deletion."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    for i in range(len(b)):
        if b[:i] + b[i + 1:] == a:
            return True
    return False


def rates(lines):
    n = sum(max(len(l) - 1, 0) for l in lines)
    exact = sum(l[i] == l[i - 1] for l in lines for i in range(1, len(l)))
    near = sum(edit1(l[i], l[i - 1]) for l in lines for i in range(1, len(l)))
    return 1000 * exact / n, 1000 * near / n


def shuffled_within(lines, rng):
    out = []
    for l in lines:
        l = l[:]
        rng.shuffle(l)
        out.append(l)
    return out


def shuffled_across(lines, rng):
    words = [w for l in lines for w in l]
    rng.shuffle(words)
    out, i = [], 0
    for l in lines:
        out.append(words[i:i + len(l)])
        i += len(l)
    return out


def baseline(lines, fn, rng, k=20):
    e = n = 0
    for _ in range(k):
        a, b = rates(fn(lines, rng))
        e += a
        n += b
    return e / k, n / k


rng = random.Random(0)
v = Voynich("ZL")
texts = {
    "VMS all": v.text_lines(unit="P"),
    "VMS Currier A": v.text_lines(unit="P", language="A"),
    "VMS Currier B": v.text_lines(unit="P", language="B"),
    "VMS Takahashi": Voynich("IT").text_lines(unit="P"),
}
for name in ["Latin_Aix", "Rettorica", "Agrippa_Book1", "Secreta_Secretorum_LAT"]:
    texts[name] = chunk_lines(historical(name, 30000))
units = naibbe.load_units("nathist")
texts["Naibbe"] = chunk_lines([w for l in naibbe.Naibbe(seed=4).encrypt(units) for w in l])
texts["Naibbe + autokey"] = chunk_lines([w for l in naibbe.Naibbe(seed=4, table_rule="autokey", autokey_p=.65).encrypt(units) for w in l])

rows = []
for name, ls in texts.items():
    ex, nr = rates(ls)
    wex, wnr = baseline(ls, shuffled_within, rng)
    aex, anr = baseline(ls, shuffled_across, rng)
    rows.append({"text": name, "exact_per_1000": ex, "exact_shuffled_in_line": wex, "exact_shuffled_all": aex,
                 "exact_ratio": ex / aex if aex else None,
                 "near_per_1000": nr, "near_shuffled_in_line": wnr, "near_shuffled_all": anr,
                 "near_ratio": nr / anr if anr else None})

# --- detail for the VMS
vl = texts["VMS all"]
pos = Counter()
for l in vl:
    for i in range(1, len(l)):
        if l[i] == l[i - 1]:
            pos["first pair" if i == 1 else "last pair" if i == len(l) - 1 else "middle"] += 1
slots = Counter()
for l in vl:
    for i in range(1, len(l)):
        slots["first pair" if i == 1 else "last pair" if i == len(l) - 1 else "middle"] += 1
position = [{"position": k, "repeats": pos[k], "pairs": slots[k], "per_1000": 1000 * pos[k] / slots[k]} for k in slots]

# across line breaks (within a paragraph, consecutive lines)
cross = same = 0
plines = v.select(unit="P")
for a, b in zip(plines, plines[1:]):
    if a.words and b.words and a.page == b.page and not b.para_start:
        cross += 1
        same += a.words[-1] == b.words[0]
freq = Counter(w for l in vl for w in l)
N = sum(freq.values())
exp_cross = sum((c / N) ** 2 for c in freq.values()) * cross

# which words repeat, against expectation from their frequency
rep = Counter(l[i] for l in vl for i in range(1, len(l)) if l[i] == l[i - 1])
pairs_total = sum(max(len(l) - 1, 0) for l in vl)
word_rows = []
for w, c in rep.most_common(25):
    exp = pairs_total * (freq[w] / N) ** 2
    word_rows.append({"word": w, "repeats": c, "expected": exp, "ratio": c / exp, "frequency": freq[w]})
near_pairs = Counter()
for l in vl:
    for i in range(1, len(l)):
        if edit1(l[i - 1], l[i]):
            near_pairs[(l[i - 1], l[i])] += 1
near_rows = [{"pair": f"{a} {b}", "count": c} for (a, b), c in near_pairs.most_common(20)]

# do near-repeats change in a consistent direction? (glyph added vs removed, which glyph)
changes = Counter()
for (a, b), c in near_pairs.items():
    if len(a) == len(b):
        i = next(k for k in range(len(a)) if a[k] != b[k])
        changes[f"{a[i]}->{b[i]}"] += c
    elif len(b) > len(a):
        changes["insert"] += c
    else:
        changes["delete"] += c
# adjacency beyond line composition: observed vs the within-line shuffle distribution
adj = {}
for name in ["VMS all", "VMS Currier A", "VMS Currier B"]:
    ls = texts[name]
    ex, nr = rates(ls)
    null = [rates(shuffled_within(ls, rng)) for _ in range(300)]
    adj[name] = {"exact": ex, "exact_null_mean": sum(a for a, _ in null) / len(null),
                 "exact_p_higher": sum(a >= ex for a, _ in null) / len(null),
                 "near": nr, "near_null_mean": sum(b for _, b in null) / len(null),
                 "near_p_higher": sum(b >= nr for _, b in null) / len(null)}

res = {"adjacency_vs_line_composition": adj, "rates": rows, "position": position, "across_line_break": {"pairs": cross, "same": same, "expected": exp_cross},
       "top_words": word_rows, "top_near_pairs": near_rows, "near_changes": changes.most_common(20)}
save(HERE, "repeats", res)

md = "# 15 repeats\n\nRates per 1000 adjacent word pairs. `ratio` = observed / whole-text shuffle.\n\n"
md += table(rows, ["text", "exact_per_1000", "exact_shuffled_in_line", "exact_shuffled_all", "exact_ratio",
                   "near_per_1000", "near_shuffled_in_line", "near_shuffled_all", "near_ratio"])
md += "\n## adjacency beyond line composition (300 within-line shuffles)\n\n"
md += table([{"text": k, **v} for k, v in adj.items()], ["text", "exact", "exact_null_mean", "exact_p_higher", "near", "near_null_mean", "near_p_higher"])
md += "\n## position of exact repeats in the line (VMS)\n\n" + table(position, ["position", "repeats", "pairs", "per_1000"])
md += f"\n## across line breaks\n\nLast word of a line = first word of the next line: {same} of {cross} (expected by frequency {exp_cross:.1f}).\n"
md += "\n## words that repeat most\n\n" + table(word_rows, ["word", "repeats", "expected", "ratio", "frequency"])
md += "\n## commonest near-repeats\n\n" + table(near_rows, ["pair", "count"])
md += "\n## what changes between near-repeats\n\n" + ", ".join(f"{k} {c}" for k, c in changes.most_common(20)) + "\n"
write_md(HERE, "repeats", md)
print(md)
