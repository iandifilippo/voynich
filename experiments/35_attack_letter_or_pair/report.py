"""Tables from results/partial.jsonl."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md

HERE = pathlib.Path(__file__).parent
rows = [json.loads(l) for l in open(HERE / "results" / "partial.jsonl")]
by = {(r["text"], r["order"], r["k"], r["language"]): r for r in rows}
out = []
for (text, order, k, lang), r in sorted(by.items()):
    if order != "as written":
        continue
    s = by.get((text, "shuffled", k, lang))
    out.append({"text": text, "language": lang, "k": k, "pieces": r["pieces"], "covered": r["covered"],
                "score": r["score"], "real text": r["real"],
                "words shuffled": s["score"] if s else "",
                "lost by shuffling": r["score"] - s["score"] if s else "",
                "similarity to plaintext": r.get("similarity to plaintext", ""), "sample": r["sample"][:70]})
save(HERE, "attack", out)
md = "# 35 letter or pair, full text\n\nScores are log10 probability per symbol under the language's letter model.\n\n"
md += table(out, ["text", "language", "k", "pieces", "covered", "score", "real text", "words shuffled",
                  "lost by shuffling", "similarity to plaintext"])
md += "\n## Samples\n\n" + table(out, ["text", "language", "k", "sample"])
write_md(HERE, "attack", md)
print(md)
