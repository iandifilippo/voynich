"""Score cipher and generator hypotheses against the manuscript.

Every candidate produces >= 10k words, gets cut into 9-word lines, and is
compared with the VMS on 13 metrics (voynich/benchmark.py). Distance 0 means
"looks like the VMS on these metrics". The VMS itself (a different stretch of
text) is included to show what a realistic floor looks like.
"""
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, benchmark, ciphers, historical, chunk_lines

HERE = pathlib.Path(__file__).parent
ref = benchmark.reference()
PLAIN = {"latin": "Latin_Aix", "latin_med": "Secreta_Secretorum_LAT",
         "italian": "Rettorica", "english": "Agrippa_Book1", "spanish": "Picatrix"}

rows = []
LINE = {"line_first_jsd", "line_last_jsd", "line_cohesion", "repeat_rate"}
CORE = [k for k in benchmark.KEYS if k not in LINE]


def run(name, plaintext, lines):
    d, z, p = benchmark.score(lines, ref)
    worst = sorted(z.items(), key=lambda kv: -abs(kv[1]))[:3]
    core = [z[k] for k in CORE]
    d_core = (sum(x * x for x in core) / len(core)) ** 0.5
    rows.append({"candidate": name, "plaintext": plaintext, "distance": d, "core": d_core,
                 "h2": p["h2"], "hapax": p["hapax_ratio"], "edge": p["edge_coupling"],
                 "line_first": p["line_first_jsd"], "cohesion": p["line_cohesion"],
                 "worst": ", ".join(f"{k} {v:+.1f}" for k, v in worst), "z": z})


v = Voynich("ZL")
vl = v.text_lines(unit="P")
k, start = 0, 0
for i, l in enumerate(vl):
    k += len(l)
    if k > 12000:
        start = i
        break
run("VMS (later pages)", "-", vl[start:])
run("VMS Currier A", "-", v.text_lines(unit="P", language="A"))
run("VMS Currier B", "-", v.text_lines(unit="P", language="B"))

words = [w for l in vl for w in l]
rng = random.Random(1)
sw = words[:]
rng.shuffle(sw)
run("control: VMS words shuffled", "-", chunk_lines(sw))
run("control: VMS glyphs shuffled", "-", chunk_lines(ciphers.shuffle_glyphs(words)))

for lang, src in PLAIN.items():
    pt = historical(src, 40000)
    for m, f in ciphers.METHODS.items():
        out = f(pt, seed=7)
        run(m, lang, chunk_lines(out))

for seed in range(3):
    run(f"self_citation (seed {seed})", "-", ciphers.self_citation(12000, seed=seed))

rows.sort(key=lambda r: r["distance"])
save(HERE, "ciphers", rows)
cols = ["candidate", "plaintext", "distance", "core", "h2", "hapax", "edge", "line_first", "cohesion", "worst"]
md = "# 05 cipher and generator benchmark\n\n"
md += "Lower distance = more VMS-like. Distance is the RMS of 13 z-scores (scale = spread among 18 historical texts).\n\n"
md += f"VMS reference: h2 {ref['voynich']['h2']:.2f}, hapax {ref['voynich']['hapax_ratio']:.2f}, edge {ref['voynich']['edge_coupling']:.3f}, line_first {ref['voynich']['line_first_jsd']:.3f}, cohesion {ref['voynich']['line_cohesion']:.2f}\n\n"
md += "`core` drops the four line-level metrics (line_first, line_last, cohesion, repeat_rate), so it only looks at glyphs and words.\n\n"
md += "## sorted by full distance\n\n" + table(rows, cols)
md += "\n## sorted by core distance\n\n" + table(sorted(rows, key=lambda r: r["core"]), cols)
write_md(HERE, "ciphers", md)
print(md)
