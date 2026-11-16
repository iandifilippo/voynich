"""How much do our conclusions depend on what ',' means?

ZL marks uncertain spaces with ','. Everything so far treats them as spaces.
c02 says roughly a third of them are probably not. Three readings:

  split  ',' is a space (what everything else uses)
  smart  join across ',' only when the glued form occurs 2+ times elsewhere
  join   ',' is never a space

For each: the full profile (all / A / B), where the VMS sits among the 18
historical texts on each metric, and how far the published Naibbe output is
from the VMS under each reading.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, benchmark, metrics
from voynich.corpus import DATA

HERE = pathlib.Path(__file__).parent
ref = benchmark.reference()
KEYS = benchmark.KEYS
LINE = {"line_first_jsd", "line_last_jsd", "line_cohesion", "repeat_rate"}
CORE = [k for k in KEYS if k not in LINE]
N = benchmark.N_WORDS
MODES = ["split", "smart", "join"]
natural = ref["natural"]

prof, counts = {}, []
for mode in MODES:
    v = Voynich("ZL", commas=mode)
    for lang in (None, "A", "B"):
        lines = v.text_lines(unit="P", language=lang)
        words = [w for l in lines for w in l]
        prof[mode, lang] = metrics.profile(lines, N)
        counts.append({"reading": mode, "subset": lang or "all", "words": len(words),
                       "types": len(set(words)), "mean_len": sum(map(len, words)) / len(words)})


def rank(k, val):
    """How many of the 18 historical texts are below this value."""
    return sum(p[k] < val for p in natural.values())


rows = []
for k in KEYS:
    r = {"metric": k}
    for mode in MODES:
        val = prof[mode, None][k]
        r[mode] = val
        r[mode + "_rank"] = f"{rank(k, val)}/{len(natural)}"
    r["z_smart"] = (prof["smart", None][k] - prof["split", None][k]) / ref["scale"][k]
    r["z_join"] = (prof["join", None][k] - prof["split", None][k]) / ref["scale"][k]
    rows.append(r)


def dist(p, q, keys):
    return (sum(((p[k] - q[k]) / ref["scale"][k]) ** 2 for k in keys) / len(keys)) ** .5


# distances between readings, against the A-B gap as a yardstick
gaps = []
for mode in ("smart", "join"):
    gaps.append({"pair": f"split vs {mode} (all)", "distance": dist(prof["split", None], prof[mode, None], KEYS),
                 "core": dist(prof["split", None], prof[mode, None], CORE)})
for mode in MODES:
    gaps.append({"pair": f"A vs B ({mode})", "distance": dist(prof[mode, "A"], prof[mode, "B"], KEYS),
                 "core": dist(prof[mode, "A"], prof[mode, "B"], CORE)})

# published Naibbe ciphertext vs each reading
src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
naib = []
if src.exists():
    nl = [l.split() for l in open(src, encoding="utf-8-sig") if l.split()]
    pn = metrics.profile(nl, N)
    for mode in MODES:
        naib.append({"reading": mode, "distance": dist(pn, prof[mode, None], KEYS),
                     "core": dist(pn, prof[mode, None], CORE),
                     "worst": ", ".join(f"{k} {(pn[k] - prof[mode, None][k]) / ref['scale'][k]:+.1f}"
                                        for k in sorted(CORE, key=lambda k: -abs(pn[k] - prof[mode, None][k]) / ref["scale"][k])[:3])})

save(HERE, "commas", {"counts": counts, "metrics": rows, "gaps": gaps, "naibbe": naib,
                      "profiles": {f"{m}/{l or 'all'}": p for (m, l), p in prof.items()}})
md = "# 16 what ',' means\n\n## size\n\n" + table(counts, ["reading", "subset", "words", "types", "mean_len"])
md += "\n## metrics (all paragraph text), with rank among 18 historical texts\n\n"
md += table(rows, ["metric", "split", "split_rank", "smart", "smart_rank", "join", "join_rank", "z_smart", "z_join"])
md += "\n`z_*` = shift from the split reading in benchmark units (MAD of the historical texts).\n"
md += "\n## how big is that shift\n\n" + table(gaps, ["pair", "distance", "core"])
if naib:
    md += "\n## Greshko's Naibbe ciphertext against each reading\n\n" + table(naib, ["reading", "distance", "core", "worst"])
write_md(HERE, "commas", md)
print(md)
