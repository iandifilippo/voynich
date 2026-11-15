"""Do the headline statistics depend on who transcribed the text and which alphabet they used?

EVA-style files (ZL, IT, RF, VT) split glyphs into strokes; CD, FG and GC
use bigger units. If a number moves a lot between them, it is a property
of the alphabet, not of the manuscript.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich, metrics
from voynich.corpus import TRANSCRIPTIONS

HERE = pathlib.Path(__file__).parent
N = 8000

rows = []
for name in TRANSCRIPTIONS:
    v = Voynich(name)
    lines = v.text_lines(unit="P")
    p = metrics.profile(lines, N)
    rows.append({"transcription": name, "all_tokens": len(v.words()), **p})

cols = ["transcription", "all_tokens", "alphabet", "word_len", "h1", "h2", "hapax_ratio",
        "edge_coupling", "word_mi", "line_first_jsd", "line_last_jsd", "line_cohesion"]

# spread of each metric across the EVA-family files vs all files
eva = [r for r in rows if r["transcription"] in ("ZL", "IT", "RF", "VT")]
spread = {}
for k in cols[2:]:
    a = [r[k] for r in rows]
    e = [r[k] for r in eva]
    spread[k] = {"eva_min": min(e), "eva_max": max(e), "all_min": min(a), "all_max": max(a)}

save(HERE, "transcriptions", {"rows": rows, "spread": spread})
md = f"# 01 transcriptions\n\nFirst {N} paragraph tokens of each file.\n\n" + table(rows, cols)
md += "\n## spread\n\n" + table([{"metric": k, **v} for k, v in spread.items()],
                                  ["metric", "eva_min", "eva_max", "all_min", "all_max"])
write_md(HERE, "transcriptions", md)
print(md)
