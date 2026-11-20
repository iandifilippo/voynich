"""How often does the habits generator reach the manuscript's value by chance?

Eight generator runs (different seeds) per text, fitted settings from run.py,
words of 3+ signs: the spread of 'beyond the boundary' and of the
off-diagonal sum, against the text's value.
"""
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "50_settings_generator"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402

import importlib.util  # noqa: E402

HERE = pathlib.Path(__file__).parent
src = (HERE / "run.py").read_text()
head = src[:src.index("rng = random.Random(0)\nrows = []")]
ns = {"__file__": str(HERE / "run.py")}
exec(compile(head, "r51", "exec"), ns)
prev = {r["text"]: r for r in json.loads((HERE / "results" / "replication.json").read_text())}
rng = random.Random(5)
rows = []
for trans, lang in (("ZL", "B"), ("ZL", "A")):
    key = f"{trans} Currier {lang}"
    S = ns["load"](trans, lang)
    sigma, hold = map(float, prev[key]["fitted sigma, hold"].split(", "))
    bb, od = [], []
    for seed in range(11, 19):
        g = ns["long_words"](ns["generator"](S, sigma, hold, seed))
        bb.append(ns["r50"].beyond_boundary(g, rng))
        r = ns["residual"].analyse(g, rng)
        od.append(sum(x["off-diagonal CMI"] for x in r.values()))
    rows.append({"text": key, "text: beyond boundary": prev[key]["beyond boundary: text"],
                 "generator runs: beyond boundary (min-max)": f"{min(bb):.3f} - {max(bb):.3f}",
                 "text: off-diagonal": prev[key]["off-diag sum: text"],
                 "generator runs: off-diagonal (min-max)": f"{min(od):.3f} - {max(od):.3f}"})
    print(rows[-1], flush=True)
save(HERE, "seeds", rows)
write_md(HERE, "seeds", "# 51 eight generator runs against the text\n\n" + table(
    rows, ["text", "text: beyond boundary", "generator runs: beyond boundary (min-max)", "text: off-diagonal",
           "generator runs: off-diagonal (min-max)"]))
