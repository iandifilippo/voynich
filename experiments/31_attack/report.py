"""Tables from the partial results of run.py."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md

HERE = pathlib.Path(__file__).parent
rows = [json.loads(l) for l in open(HERE / "results" / "partial.jsonl")]
key = lambda r: (r["symbols as"], r["spaces"], r["language"])
groups = {}
for r in rows:
    groups.setdefault(key(r), {})[r["text"]] = r

summary = []
for (scheme, spaces, lang), g in groups.items():
    if len(g) < 4:
        continue
    b, a = g["VMS Currier B"], g["VMS Currier A"]
    c, s = g["control: copying model"], g["control: shuffled glyphs"]
    summary.append({"symbols as": scheme, "spaces": spaces, "language": lang, "n symbols": b["n symbols"],
                    "gap B": b["gap"], "gap A": a["gap"], "gap copying model": c["gap"], "gap shuffled": s["gap"],
                    "words B": b["in real words"], "words A": a["in real words"],
                    "words copying model": c["in real words"], "words real": b["real text in words"],
                    "B minus control": b["gap"] - c["gap"], "A minus control": a["gap"] - c["gap"]})

best = sorted(summary, key=lambda r: -max(r["gap B"], r["gap A"]))[:12]
wins = sorted(summary, key=lambda r: -max(r["B minus control"], r["A minus control"]))[:12]
n = len(summary)
stats = {
    "combinations": n,
    "best gap, VMS": max(max(r["gap B"], r["gap A"]) for r in summary),
    "best gap, copying model": max(r["gap copying model"] for r in summary),
    "VMS B better than copying model": sum(r["B minus control"] > 0 for r in summary),
    "VMS A better than copying model": sum(r["A minus control"] > 0 for r in summary),
    "mean B minus control": sum(r["B minus control"] for r in summary) / n,
    "mean A minus control": sum(r["A minus control"] for r in summary) / n,
    "best words share, VMS": max(max(r["words B"], r["words A"]) for r in summary),
    "best words share, copying model": max(r["words copying model"] for r in summary),
    "within 0.05 of real text": sum(max(r["gap B"], r["gap A"]) > -0.05 for r in summary),
}
samples = []
for r in sorted(rows, key=lambda r: -r["gap"]):
    if r["text"].startswith("VMS") and len(samples) < 6:
        samples.append({"text": r["text"], "symbols as": r["symbols as"], "spaces": r["spaces"], "language": r["language"],
                        "gap": r["gap"], "decoded": r["sample"]})
ctrl = [{"text": r["text"], "symbols as": r["symbols as"], "spaces": r["spaces"], "language": r["language"],
         "gap": r["gap"], "decoded": r["sample"]}
        for r in sorted(rows, key=lambda r: -r["gap"]) if r["text"] == "control: copying model"][:3]

save(HERE, "attack", {"stats": stats, "summary": summary, "samples": samples, "control_samples": ctrl})
md = "# 31 attack: one symbol, one letter\n\n"
md += "gap = score per letter of the best key minus real text in that language. 0 means it reads like the language; exp. 30 put texts with no such language in them at −0.19 to −0.47.\n\n"
md += table([{"": k, "value": v} for k, v in stats.items()], ["", "value"])
md += "\n## the twelve best readings of the manuscript\n\n" + table(
    best, ["symbols as", "spaces", "language", "n symbols", "gap B", "gap A", "gap copying model", "gap shuffled",
           "words B", "words A", "words copying model", "words real"])
md += "\n## where the manuscript beats the content-free control by most\n\n" + table(
    wins, ["symbols as", "spaces", "language", "gap B", "gap A", "gap copying model", "B minus control", "A minus control"])
md += "\n## what the best readings look like\n\n" + table(samples, ["text", "symbols as", "spaces", "language", "gap", "decoded"])
md += "\n## and the best readings of the control\n\n" + table(ctrl, ["text", "symbols as", "spaces", "language", "gap", "decoded"])
md += "\n## every combination\n\n" + table(
    sorted(summary, key=lambda r: (r["symbols as"], r["spaces"], r["language"])),
    ["symbols as", "spaces", "language", "n symbols", "gap B", "gap A", "gap copying model", "gap shuffled",
     "words B", "words A", "words copying model", "words real"])
write_md(HERE, "attack", md)
print(md)
