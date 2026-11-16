"""Is there a line-end transformation too?

08 showed words ending in -m are ~17x commoner at line end. If line ends work
like line starts (10), some ordinary ending is being rewritten as -m (or -g)
when a word lands at the end of a line. For each candidate rewrite
"ending e -> m", every word type x ending in e gets a partner x' = x[:-len(e)] + "m".
deficit(x)  = how much rarer x is at line end than expected
surplus(x') = how much commoner x' is at line end than expected
If the rewrite is real, the two correlate across word types (permutation test).
Same for -g, and a control rewrite that shouldn't do anything (e -> "l").
"""
import math
import pathlib
import random
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
ENDINGS = ["in", "iin", "aiin", "ain", "n", "y", "dy", "r", "l", "s", "o", "e"]
TARGETS = ["m", "g"]


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def analyse(lines, label, rng, targets=TARGETS):
    lines = [l for l in lines if len(l) >= 3]
    last = Counter(l[-1] for l in lines)
    rest = Counter(w for l in lines for w in l[:-1])
    n_last, n_rest = sum(last.values()), sum(rest.values())
    rows = []
    for tgt in targets:
        for e in ENDINGS:
            defs, surs, xs = [], [], []
            for x, cx in rest.items():
                if cx < 5 or not x.endswith(e) or len(x) <= len(e):
                    continue
                x2 = x[:-len(e)] + tgt
                exp_x = cx / n_rest * n_last
                exp_x2 = rest.get(x2, 0) / n_rest * n_last
                defs.append((exp_x - last.get(x, 0)) / math.sqrt(exp_x))
                surs.append((last.get(x2, 0) - exp_x2) / math.sqrt(exp_x))
                xs.append((x, x2, last.get(x2, 0)))
            if len(xs) < 10:
                continue
            r = pearson(defs, surs)
            perm, hits = surs[:], 0
            for _ in range(2000):
                rng.shuffle(perm)
                if pearson(defs, perm) >= r:
                    hits += 1
            top = sorted(zip(xs, surs), key=lambda t: -t[1])[:5]
            rows.append({"set": label, "rewrite": f"-{e} -> -{tgt}", "types": len(xs), "r": r, "p": hits / 2000,
                         "line_end_tokens_explained": sum(n for (_, _, n) in xs),
                         "examples": ", ".join(f"{a}->{b} ({n})" for (a, b, n), _ in top)})
    return rows


rng = random.Random(0)
v = Voynich("ZL")
lines = v.text_lines(unit="P")
last_all = Counter(l[-1] for l in lines if len(l) >= 3)
m_final = sum(c for w, c in last_all.items() if w.endswith("m"))
g_final = sum(c for w, c in last_all.items() if w.endswith("g"))

rows = analyse(lines, "all", rng, TARGETS + ["l"])
rows += analyse(v.text_lines(unit="P", language="A"), "Currier A", rng)
rows += analyse(v.text_lines(unit="P", language="B"), "Currier B", rng)
rows += analyse(Voynich("IT").text_lines(unit="P"), "Takahashi", rng)
n_tests = len(rows)

# is line end about selection (short words) rather than rewriting?
ls3 = [l for l in lines if len(l) >= 3]
mean_len = lambda ws: sum(map(len, ws)) / len(ws)
lengths = {"line_first": mean_len([l[0] for l in ls3]), "line_internal": mean_len([w for l in ls3 for w in l[1:-1]]),
           "line_final": mean_len([l[-1] for l in ls3])}
internal = Counter(w for l in ls3 for w in l[1:-1])
n_int = sum(internal.values())
fam = {}
for stem in ("a", "da", "ota", "ra", "o", "do", "sa"):
    for e in ("l", "m", "r", "s", "in", "iin"):
        w = stem + e
        exp = internal.get(w, 0) / n_int * len(ls3)
        if exp >= 2:
            fam[w] = {"line_final": last_all.get(w, 0), "expected": exp, "ratio": last_all.get(w, 0) / exp}
# stem-level: does the whole family stem+{r,l,s,n,in,iin,y,dy} lose at line end what stem+m gains?
FAMILY = ["r", "l", "s", "n", "in", "iin", "y", "dy"]


def stem_test(ls, rng):
    ls = [l for l in ls if len(l) >= 3]
    lastc = Counter(l[-1] for l in ls)
    restc = Counter(w for l in ls for w in l[:-1])
    nl, nr = sum(lastc.values()), sum(restc.values())
    stems = {w[:-1] for w in set(lastc) | set(restc) if w.endswith("m") and len(w) >= 2}
    defs, surs, used = [], [], []
    for st in stems:
        fam_rest = sum(restc.get(st + e, 0) for e in FAMILY)
        if fam_rest < 10:
            continue
        exp_f = fam_rest / nr * nl
        obs_f = sum(lastc.get(st + e, 0) for e in FAMILY)
        exp_m = restc.get(st + "m", 0) / nr * nl
        defs.append((exp_f - obs_f) / math.sqrt(exp_f))
        surs.append((lastc.get(st + "m", 0) - exp_m) / math.sqrt(exp_f))
        used.append(st)
    r = pearson(defs, surs)
    perm, hits = surs[:], 0
    for _ in range(5000):
        rng.shuffle(perm)
        if pearson(defs, perm) >= r:
            hits += 1
    return {"stems": len(used), "r": r, "p": hits / 5000}


stem_rows = []
for label, ls in (("all", lines), ("Currier A", v.text_lines(unit="P", language="A")),
                  ("Currier B", v.text_lines(unit="P", language="B")), ("Takahashi", Voynich("IT").text_lines(unit="P"))):
    stem_rows.append({"set": label, **stem_test(ls, rng)})

save(HERE, "lineend_model", {"stem_level": stem_rows, "lengths": lengths, "families": fam, "rows": rows, "m_final_tokens": m_final, "g_final_tokens": g_final, "tests": n_tests})

md = "# 14 line-end transformation\n\n"
md += f"Line-final tokens ending in -m: {m_final}; in -g: {g_final}. {n_tests} tests, so Bonferroni threshold p < {0.05 / n_tests:.4f}.\n\n"
md += "## stem level: family deficit vs stem+m surplus\n\n" + table(stem_rows, ["set", "stems", "r", "p"]) + "\n"
md += f"Mean word length: line-first {lengths['line_first']:.2f}, internal {lengths['line_internal']:.2f}, line-final {lengths['line_final']:.2f}.\n\n"
md += "Line-final vs expected for some word families (ratio > 1 = favoured at line end):\n\n"
md += table([{"word": w, **x} for w, x in fam.items()], ["word", "line_final", "expected", "ratio"]) + "\n"
md += "`-e -> -l` rows are a control: no reason to expect it.\n\n"
md += table(rows, ["set", "rewrite", "types", "r", "p", "line_end_tokens_explained", "examples"])
write_md(HERE, "lineend_model", md)
print(md)
