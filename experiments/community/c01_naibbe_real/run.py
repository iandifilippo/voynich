"""Greshko's actual Naibbe ciphertext through the benchmark.

Input: data/external/naibbe-cipher/encrypted/nathist_output_ciphertext.txt
(Pliny's Natural History enciphered with the published tables), fetched by
python -m voynich.download. Greshko, Cryptologia 2025, doi:10.1080/01611194.2025.2566408.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich import Voynich, benchmark, ciphers, historical, chunk_lines, metrics
from voynich.corpus import DATA

HERE = pathlib.Path(__file__).parent
ref = benchmark.reference()
LINE = {"line_first_jsd", "line_last_jsd", "line_cohesion", "repeat_rate"}
CORE = [k for k in benchmark.KEYS if k not in LINE]

src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
raw_lines = [l.split() for l in open(src, encoding="utf-8-sig") if l.split()]
words = [w for l in raw_lines for w in l]

v = Voynich("ZL")
b_profile = metrics.profile(v.text_lines(unit="P", language="B"), benchmark.N_WORDS)

rows = []


def run(name, lines):
    d, z, p = benchmark.score(lines, ref)
    core = (sum(z[k] ** 2 for k in CORE) / len(CORE)) ** .5
    zb = {k: (p[k] - b_profile[k]) / ref["scale"][k] for k in benchmark.KEYS}
    core_b = (sum(zb[k] ** 2 for k in CORE) / len(CORE)) ** .5
    rows.append({"text": name, "distance": d, "core": core, "core_vs_B": core_b,
                 "h2": p["h2"], "hapax": p["hapax_ratio"], "edge": p["edge_coupling"],
                 "word_mi": p["word_mi"], "word_len": p["word_len"], "zipf": p["zipf"],
                 "line_first": p["line_first_jsd"],
                 "worst_core": ", ".join(f"{k} {z[k]:+.1f}" for k in sorted(CORE, key=lambda k: -abs(z[k]))[:3])})


run("Naibbe (Greshko), his line breaks", raw_lines)
run("Naibbe (Greshko), 9-word lines", chunk_lines(words))
run("naibbe_like (ours), Latin", chunk_lines(ciphers.naibbe_like(historical("Latin_Aix", 40000), seed=7)))
run("VMS Currier B", v.text_lines(unit="P", language="B"))
run("VMS later pages", v.text_lines(unit="P")[600:])

save(HERE, "naibbe_real", rows)
md = "# c01 Greshko's Naibbe ciphertext\n\n"
md += "`core` = distance on the 9 glyph/word metrics (no line metrics). `core_vs_B` = same, against the Currier B profile.\n\n"
md += table(rows, ["text", "distance", "core", "core_vs_B", "h2", "hapax", "edge", "word_mi", "word_len", "zipf", "worst_core"])
write_md(HERE, "naibbe_real", md)
print(md)
