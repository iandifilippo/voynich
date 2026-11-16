"""Can a hand-executable rule give the Naibbe cipher the cross-word coupling it lacks?

community/c01: Greshko's Naibbe output matches the VMS on word-internal
statistics but has zero edge coupling (0.002 vs 0.17 in the VMS), because each
word's table comes from an independent card draw.

Idea: an autokey. Instead of always drawing a card, the scribe reads the table
for the next word off the last glyph of the word just written (a small fixed
chart), with probability p. Autokey ciphers are a 15th-16th c. idea (Belaso
1553 and earlier progressive systems), and this needs no extra equipment.

Parts
1. our Naibbe implementation vs Greshko's own ciphertext (validation)
2. autokey p sweep with an arbitrary chart: does coupling appear, does anything else move?
3. shape: which (last glyph, next initial) pairs are over-represented, VMS vs cipher.
   Search for the chart that best matches the VMS pattern on half the lines, evaluate on the other half.
4. is the VMS coupling real? coupling across certain spaces only
5. full benchmark, with lines/paragraphs cut like the VMS and Smith's line-start transformation
Plaintexts: Pliny (Greshko's nathist units) and Dante (his divcom units).
"""
import math
import pathlib
import random
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, benchmark, chunk_lines, metrics, naibbe
from voynich.corpus import DATA
from voynich.metrics import mutual_info

HERE = pathlib.Path(__file__).parent
LAST = ["y", "n", "l", "r", "s", "m", "o", "d"]
PROFILE_KEYS = ["h2", "hapax_ratio", "edge_coupling", "word_len", "zipf", "mattr500"]


def first_cls(w):
    return w[:2] if w[:2] in ("ch", "sh", "qo") else w[0]


def last_cls(w):
    return w[-1] if w[-1] in LAST else "other"


def pmi(pairs, mincount=30):
    a = Counter(x for x, _ in pairs)
    b = Counter(y for _, y in pairs)
    ab = Counter(pairs)
    n = len(pairs)
    return {k: math.log2((c / n) / ((a[k[0]] / n) * (b[k[1]] / n))) for k, c in ab.items() if c >= mincount}


def corr(p, q):
    ks = [k for k in p if k in q]
    xs, ys = [p[k] for k in ks], [q[k] for k in ks]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def pairs_of(lines):
    return [(last_cls(l[i]), first_cls(l[i + 1])) for l in lines for i in range(len(l) - 1)]


def flat(lines):
    return [w for l in lines for w in l]


v = Voynich("ZL")
vl = v.text_lines(unit="P")
vms_half_a, vms_half_b = pmi(pairs_of(vl[::2])), pmi(pairs_of(vl[1::2]))
res = {}

# ---- 1. validation
units = {"pliny": naibbe.load_units("nathist"), "dante": naibbe.load_units("divcom")[:1100]}
greshko = [l.split() for l in open(DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt",
                                    encoding="utf-8-sig") if l.split()]
val = []
for name, ls in (("Greshko's file (Pliny)", greshko), ("ours, same units", naibbe.Naibbe(seed=1).encrypt(units["pliny"]))):
    p = metrics.profile(chunk_lines(flat(ls)), 10000)
    val.append({"text": name, **{k: p[k] for k in PROFILE_KEYS}})
res["validation"] = val

# ---- 2. p sweep
sweep = []
for src in units:
    for pa in (0.0, 0.25, 0.5, 0.65, 0.8, 1.0):
        rule = "autokey" if pa else "deck"
        c = naibbe.Naibbe(seed=2, table_rule=rule, autokey_p=pa).encrypt(units[src])
        p = metrics.profile(chunk_lines(flat(c)), 10000)
        sweep.append({"plaintext": src, "autokey_p": pa, **{k: p[k] for k in PROFILE_KEYS}})
vp = metrics.profile(vl, 10000)
res["sweep"] = sweep

# ---- 3. shape: chart search on half A, evaluate on half B
rng = random.Random(0)
base_words = flat(naibbe.Naibbe(seed=3).encrypt(units["pliny"]))
Fd = Counter(first_cls(w) for w in base_words)
Lc = Counter(last_cls(w) for w in base_words)


class Const(dict):
    def __init__(self, t):
        super().__init__()
        self.t = t

    def get(self, k, d=None):
        return self.t


F = {}
for t in naibbe.TABLES:
    ws = flat(naibbe.Naibbe(seed=3, table_rule="autokey", autokey_p=1.0, chart=Const(t)).encrypt(units["pliny"]))
    F[t] = Counter(first_cls(w) for w in ws)


def predicted(chart, p):
    keys = set(Fd).union(*[set(F[t]) for t in F])
    counts = {}
    for L, nl in Lc.items():
        ft = F[chart.get(L, "alpha")]
        for f in keys:
            counts[(L, f)] = nl * (p * ft[f] / sum(ft.values()) + (1 - p) * Fd[f] / sum(Fd.values()))
    a, b = Counter(), Counter()
    for (L, f), c in counts.items():
        a[L] += c
        b[f] += c
    n = sum(counts.values())
    return {k: math.log2((c / n) / ((a[k[0]] / n) * (b[k[1]] / n))) for k, c in counts.items() if c >= 30}


P_SHAPE = 0.65
best = None
for _ in range(30):
    chart = {L: rng.choice(naibbe.TABLES) for L in LAST + ["other"]}
    cur = corr(predicted(chart, P_SHAPE), vms_half_a)
    improved = True
    while improved:
        improved = False
        for L in LAST + ["other"]:
            for t in naibbe.TABLES:
                if t == chart[L]:
                    continue
                old = chart[L]
                chart[L] = t
                c = corr(predicted(chart, P_SHAPE), vms_half_a)
                if c > cur + 1e-9:
                    cur, improved = c, True
                else:
                    chart[L] = old
    if best is None or cur > best[0]:
        best = (cur, dict(chart))
best_chart = best[1]
sim_best = naibbe.Naibbe(seed=11, table_rule="autokey", autokey_p=P_SHAPE, chart=best_chart).encrypt(units["pliny"])
sim_dante = naibbe.Naibbe(seed=11, table_rule="autokey", autokey_p=P_SHAPE, chart=best_chart).encrypt(units["dante"])
random_charts = []
for k in range(20):
    ch = {L: rng.choice(naibbe.TABLES) for L in LAST + ["other"]}
    s = naibbe.Naibbe(seed=20 + k, table_rule="autokey", autokey_p=P_SHAPE, chart=ch).encrypt(units["pliny"])
    random_charts.append(corr(pmi(pairs_of(chunk_lines(flat(s)))), vms_half_b))
shape = {
    "vms_half_vs_half": corr(vms_half_a, vms_half_b),
    "best_chart": best_chart,
    "fit_on_half_a": best[0],
    "simulated_vs_half_b_pliny": corr(pmi(pairs_of(chunk_lines(flat(sim_best)))), vms_half_b),
    "simulated_vs_half_b_dante": corr(pmi(pairs_of(chunk_lines(flat(sim_dante)))), vms_half_b),
    "random_charts_mean": sum(random_charts) / len(random_charts),
    "random_charts_max": max(random_charts),
    "vms_top_pairs": sorted(((f"{a}|{b}", x) for (a, b), x in pmi(pairs_of(vl)).items()), key=lambda t: -t[1])[:10],
}
res["shape"] = shape

# ---- 4. is the VMS coupling real?
dot, com = [], []
for raw in open(DATA / "ZL3b-n.txt", encoding="latin-1"):
    m = re.match(r"^<(f\d+[rv]\d?)\.(\d+),[+@=&~*]?P\w*>\s*(.*)$", raw.rstrip("\n"))
    if not m:
        continue
    t = m.group(3)
    t = re.sub(r"<![^>]*>", "", t)
    t = re.sub(r"\[([^:\]]*)[^\]]*\]", r"\1", t)
    t = re.sub(r"\{([^}]*)\}", r"\1", t)
    t = re.sub(r"<[^>]*>", ".", t).replace("'", "")
    toks = re.split(r"([.,])", t)
    pieces = [x for x in toks if x not in ".,"]
    seps = [x for x in toks if x in ".,"]
    for a, s, b in zip(pieces, seps, pieces[1:]):
        if a and b and not re.search(r"[?*@!]", a + b):
            (dot if s == "." else com).append((a[-1], b[0]))
allw = flat(vl)
sh = allw[:]
random.Random(0).shuffle(sh)
base_mi = mutual_info((sh[i][-1], sh[i + 1][0]) for i in range(len(sh) - 1))
res["vms_coupling"] = {"certain_spaces_only": mutual_info(dot) - base_mi, "n_certain": len(dot),
                       "uncertain_spaces_only": mutual_info(com) - base_mi, "n_uncertain": len(com)}

# ---- 5. full benchmark with VMS-like lineation and Smith's line-start transformation
ref = benchmark.reference()
LINE = {"line_first_jsd", "line_last_jsd", "line_cohesion", "repeat_rate"}
CORE = [k for k in benchmark.KEYS if k not in LINE]
line_lengths = [len(l) for l in vl if l]
paras, cur_len = [], 0
for l in v.select(unit="P"):
    if l.para_start and cur_len:
        paras.append(cur_len)
        cur_len = 0
    cur_len += 1
paras.append(cur_len)

bench = []


def score(name, src, lines):
    d, z, p = benchmark.score(lines, ref)
    core = (sum(z[k] ** 2 for k in CORE) / len(CORE)) ** .5
    bench.append({"variant": name, "plaintext": src, "distance": d, "core": core,
                  "edge": p["edge_coupling"], "line_first": p["line_first_jsd"], "line_last": p["line_last_jsd"],
                  "hapax": p["hapax_ratio"], "h2": p["h2"],
                  "worst": ", ".join(f"{k} {z[k]:+.1f}" for k in sorted(z, key=lambda k: -abs(z[k]))[:3])})


for src in units:
    for label, kw in (("Naibbe (deck)", {}),
                      ("+ autokey p=.65, arbitrary chart", {"table_rule": "autokey", "autokey_p": .65}),
                      ("+ autokey p=.65, fitted chart", {"table_rule": "autokey", "autokey_p": .65, "chart": best_chart})):
        words = flat(naibbe.Naibbe(seed=5, **kw).encrypt(units[src]))
        r = random.Random(7)
        ps = naibbe.relineate(words, line_lengths, paras, r)
        plain_lines = [l for para in ps for l in para if l]
        score(label, src, plain_lines)
        for q in (0.3, 0.5):
            score(label + f" + line-start q={q}", src, naibbe.linestart(ps, q=q, seed=8))
score("VMS later pages", "-", vl[600:])
score("VMS Currier B", "-", v.text_lines(unit="P", language="B"))
bench.sort(key=lambda r: r["distance"])
res["benchmark"] = bench
save(HERE, "autokey_naibbe", res)

# ---- report
md = "# 13 autokey Naibbe\n\n## 1. validation\n\n" + table(val, ["text"] + PROFILE_KEYS)
md += f"\n## 2. autokey strength (arbitrary chart)\n\nVMS: edge {vp['edge_coupling']:.3f}, h2 {vp['h2']:.2f}, hapax {vp['hapax_ratio']:.2f}\n\n"
md += table(sweep, ["plaintext", "autokey_p"] + PROFILE_KEYS)
md += "\n## 3. shape of the coupling\n\n"
md += f"Correlation of PMI(last glyph, next initial) between patterns:\n\n"
md += f"- VMS odd lines vs even lines: {shape['vms_half_vs_half']:.2f}\n"
md += f"- 20 random charts vs VMS (held-out half): mean {shape['random_charts_mean']:.2f}, best {shape['random_charts_max']:.2f}\n"
md += f"- chart fitted on odd lines ({shape['fit_on_half_a']:.2f} there), simulated cipher vs even lines: Pliny {shape['simulated_vs_half_b_pliny']:.2f}, Dante {shape['simulated_vs_half_b_dante']:.2f}\n"
md += f"- fitted chart: {shape['best_chart']}\n"
md += "- strongest VMS pairs: " + ", ".join(f"{k} {x:.2f}" for k, x in shape["vms_top_pairs"]) + "\n"
c4 = res["vms_coupling"]
md += f"\n## 4. VMS coupling by space type\n\ncertain spaces only: {c4['certain_spaces_only']:.3f} bits ({c4['n_certain']} boundaries); uncertain only: {c4['uncertain_spaces_only']:.3f} ({c4['n_uncertain']}).\n"
md += "\n## 5. benchmark\n\n" + table(bench, ["variant", "plaintext", "distance", "core", "edge", "line_first", "line_last", "hapax", "h2", "worst"])
write_md(HERE, "autokey_naibbe", md)
print(md)
