"""Attack 7: a few bits per word, hidden in the forks.

The last cipher family the series hasn't calibrated: the message is not in
which word is written but in a few choices inside it (how it starts, how it
ends), and one letter of plaintext is spread over several words. Everything
else in the word is filler from the slot machine. Such a text would have
the manuscript's word shapes, no lexicon, and weak links between
neighbours, exactly what exps. 34-53 found.

What it can't hide: the sequence of fork choices carries the plaintext, so
it is predictable from several words back, not just one. Test:
  fork symbol of a word = (start class: qo / o / ch-sh / other) x (end class:
  y / n / l-r / other), 16 values;
  stream of fork symbols in reading order through each sheet;
  held-out bits per symbol under an n-gram model looking back k = 0..4
  symbols, trained on half the sheets, tested on the other half.
The quantity that matters is how much looking 2-4 words back adds over
looking 1 back: a code that spreads a letter over several words makes it
large; a writer's habit between neighbours doesn't.

Calibration: ciphers of Latin built from the manuscript's own word machine
(exp. 36 generator, B tables): plaintext letters -> 5-bit codes -> a bit
stream, each word made to carry 2 bits (its start class) or 4 bits (start
and end class), the rest of the word filled in freely by the machine.
Controls: the habits generator (exp. 50). Then Currier A and B.
"""
import math
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "51_residual_replication"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "50_settings_generator"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md  # noqa: E402
from voynich.assemble import Assembler, signs  # noqa: E402
from voynich.corpus import historical  # noqa: E402

HERE = pathlib.Path(__file__).parent
src = (HERE.parent / "51_residual_replication" / "run.py").read_text()
ns = {"__file__": str(HERE.parent / "51_residual_replication" / "run.py")}
exec(compile(src[:src.index("rng = random.Random(0)\nrows = []")], "r51", "exec"), ns)
KMAX = 8
SYMBOLS = {"start (4)": lambda w: start_cls(w), "end (4)": lambda w: end_cls(w),
           "start and end (16)": lambda w: fork(w)}


def start_cls(w):
    return 0 if w.startswith("qo") else 1 if w.startswith("o") else 2 if w[:2] in ("ch", "sh") else 3


def end_cls(w):
    return 0 if w.endswith("y") else 1 if w.endswith("n") else 2 if w[-1:] in ("l", "r") else 3


def fork(w):
    return start_cls(w) * 4 + end_cls(w)


def bits_per_symbol(train, test, k, V):
    """Interpolated (Witten-Bell) n-gram over symbol streams; held-out bits."""
    tabs = [defaultdict(Counter) for _ in range(k + 1)]
    for s in train:
        q = [-1] * k + s
        for j in range(k, len(q)):
            for o in range(k + 1):
                tabs[o][tuple(q[j - o:j])][q[j]] += 1
    cost = n = 0
    for s in test:
        q = [-1] * k + s
        for j in range(k, len(q)):
            c0 = tabs[0][()]
            p = (c0[q[j]] + 0.5) / (sum(c0.values()) + 0.5 * V)
            for o in range(1, k + 1):
                c = tabs[o].get(tuple(q[j - o:j]))
                if c:
                    p = (c[q[j]] + len(c) * p) / (sum(c.values()) + len(c))
            cost -= math.log2(p)
            n += 1
    return cost / n


def streams(sheets, f):
    return [[f(w) for l in s for w in l] for s in sheets]


def evaluate(sheets, f, V, kmax):
    st = streams(sheets, f)
    a, b = st[0::2], st[1::2]
    return {k: (bits_per_symbol(a, b, k, V) + bits_per_symbol(b, a, k, V)) / 2 for k in range(kmax + 1)}


LATIN = re.sub(r"[^a-z]", "", " ".join(historical("Secreta_Secretorum_LAT")).lower())
ALPHA = sorted(set(LATIN))
CODE = {c: format(i, "05b") for i, c in enumerate(ALPHA)}


def cipher(template_sheets, bits_per_word, rng, machine):
    """Fill the template's sheets and lines with words whose fork classes
    spell out the bit stream of the Latin text."""
    stream = "".join(CODE[c] for c in LATIN)
    pos = 0
    pools = defaultdict(list)
    for _ in range(60000):
        w = machine.word(rng, "middle", "#")
        pools[(start_cls(w), end_cls(w))].append(w)
    out = []
    for s in template_sheets:
        lines = []
        for l in s:
            line = []
            for _ in l:
                chunk = stream[pos:pos + bits_per_word]
                pos += bits_per_word
                if bits_per_word == 2:
                    sc = int(chunk, 2)
                    ec = rng.choices(range(4), [len(pools[(sc, e)]) for e in range(4)])[0]
                else:
                    sc, ec = int(chunk[:2], 2), int(chunk[2:], 2)
                line.append(rng.choice(pools[(sc, ec)]))
            lines.append(line)
        out.append(lines)
    return out


rng = random.Random(0)
SB, SA = ns["load"]("ZL", "B"), ns["load"]("ZL", "A")
B = [[w for w, _ in s] for s in SB]
A = [[w for w, _ in s] for s in SA]
machine = Assembler(order=2).fit([l for s in B for l in s])
texts = {"cipher of Latin, 2 bits per word (start)": cipher(B, 2, rng, machine),
         "cipher of Latin, 4 bits per word (start + end)": cipher(B, 4, rng, machine),
         "habits generator (B)": ns["generator"](SB, 0.9, 2.5, 7),
         "Currier B": B, "Currier A": A}
rows = []
for sym, f in SYMBOLS.items():
    V = 16 if "16" in sym else 4
    kmax = 4 if V == 16 else KMAX
    for name, sheets in texts.items():
        r = evaluate(sheets, f, V, kmax)
        rows.append({"symbol": sym, "text": name, **{f"k={k}": r[k] for k in r}, "gain k=1 over k=0": r[0] - r[1],
                     "gain from looking further than 1 back": r[1] - min(r[k] for k in range(1, kmax + 1)),
                     "best k": min(r, key=r.get)})
        print({k: (round(x, 4) if isinstance(x, float) else x) for k, x in rows[-1].items()}, flush=True)
save(HERE, "fork_bits", rows)
md = ("# 54 bits hidden in the forks\n\nHeld-out bits per symbol, n-gram looking k symbols back, "
      "trained on half the sheets, tested on the other half.\n\n") + table(
    rows, ["symbol", "text"] + [f"k={k}" for k in (0, 1, 2, 3, 4, 6, 8)] +
    ["gain k=1 over k=0", "gain from looking further than 1 back", "best k"])
write_md(HERE, "fork_bits", md)
print(md)
