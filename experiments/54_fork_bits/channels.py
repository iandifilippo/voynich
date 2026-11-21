"""The channels run.py left uncalibrated: the gallows, the length, the e-run.

Same test as run.py, with ciphers of Latin that put their bits in
  the gallows (2 bits: t / k / p-f / none),
  the length (1 bit: even or odd number of signs),
  the e-run (1 bit: the word has e, ee or eee, or it hasn't),
built from the same word machine, laid out in B's sheets. Each is measured
on its own channel, and the manuscript on the same channels.
"""
import pathlib
import random
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
CHANNELS = {
    "gallows (4)": (run.gal_cls, 4, 2),
    "length parity (2)": (lambda w: len(signs(w)) % 2, 2, 1),
    "has e-run (2)": (lambda w: int(any(x in ("e", "ee", "eee") for x in signs(w))), 2, 1),
}


def channel_cipher(template, f, V, bits, rng):
    stream = "".join(run.CODE[c] for c in run.LATIN)
    pos = 0
    pools = defaultdict(list)
    for _ in range(60000):
        w = run.machine.word(rng, "middle", "#")
        pools[f(w)].append(w)
    out = []
    for s in template:
        out.append([])
        for l in s:
            line = []
            for _ in l:
                v = int(stream[pos:pos + bits], 2)
                pos += bits
                line.append(rng.choice(pools[v]))
            out[-1].append(line)
    return out


rng = random.Random(3)
rows = []
for name, (f, V, bits) in CHANNELS.items():
    kmax = 12 if V == 2 else 8
    texts = {f"cipher of Latin in this channel ({bits} bit/word)": channel_cipher(run.B, f, V, bits, rng),
             "habits generator (B)": run.texts["habits generator (B)"],
             "Currier B": run.B, "Currier A": run.A}
    for t, sheets in texts.items():
        r = run.evaluate(sheets, f, V, kmax)
        rows.append({"channel": name, "text": t, "k=0": r[0],
                     "gain from looking further than 1 back": r[1] - min(r[k] for k in range(1, kmax + 1)),
                     "best k": min(r, key=r.get)})
        print(rows[-1], flush=True)
save(HERE, "channels", rows)
write_md(HERE, "channels", "# 54 the remaining channels\n\n" + table(
    rows, ["channel", "text", "k=0", "gain from looking further than 1 back", "best k"]))


# Currier A's e-run channel came out above the generator: check it in the other
# transcription and against A's own sheets shuffled line by line (a line-level
# habit survives that; a sequence running across lines doesn't).
f, V, _ = CHANNELS["has e-run (2)"]
ita = [[w for w, _ in s] for s in run.ns["load"]("IT", "A")]
check = []
for label, sheets in (("Currier A (ZL)", run.A), ("Currier A (IT)", ita)):
    r = run.evaluate(sheets, f, V, 12)
    shuffled = []
    for s in sheets:
        s2 = s[:]
        rng.shuffle(s2)
        shuffled.append(s2)
    r2 = run.evaluate(shuffled, f, V, 12)
    check.append({"text": label, "gain": r[1] - min(r[k] for k in range(1, 13)), "best k": min(r, key=r.get),
                  "gain, lines in random order": r2[1] - min(r2[k] for k in range(1, 13))})
    print(check[-1], flush=True)
save(HERE, "channels_check", check)
md = (HERE / "results" / "channels.md").read_text()
write_md(HERE, "channels", md + "\n## Currier A, e-run channel, checks\n\n" + table(
    check, ["text", "gain", "best k", "gain, lines in random order"]))
