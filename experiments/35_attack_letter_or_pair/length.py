"""Would the attack have read a Naibbe cipher the size of the manuscript's
two languages? Same job as run.py on the first 11 231 and 23 084 words."""
import json
import multiprocessing
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import run  # noqa: E402
from _common import save, table, write_md  # noqa: E402

HERE = pathlib.Path(__file__).parent
FULL = run.TEXTS["Naibbe cipher of Pliny"]


def one(n):
    run.TEXTS["Naibbe cipher of Pliny"] = FULL[:n]
    r = run.job(("Naibbe cipher of Pliny", "as written", 110, "Latin"))
    r["words"] = n
    return r


if __name__ == "__main__":
    with multiprocessing.Pool(2) as pool:
        rows = pool.map(one, [5000, 11231, 23084])
    save(HERE, "length", rows)
    md = "# 35 Naibbe cipher cut to the manuscript's sizes (Latin, k = 110)\n\n" + table(
        rows, ["words", "pieces", "score", "real", "gap", "similarity to plaintext"])
    write_md(HERE, "length", md)
    print(md)
