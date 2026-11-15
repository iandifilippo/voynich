import math
import pathlib
from collections import Counter

from ivtff import load, SECTIONS

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "ZL3b-n.txt"


def entropy(text):
    n = len(text)
    h1 = -sum(c / n * math.log2(c / n) for c in Counter(text).values())
    pairs = Counter(text[i - 1:i + 1] for i in range(1, n))
    hj = -sum(c / (n - 1) * math.log2(c / (n - 1)) for c in pairs.values())
    return h1, hj - h1


def pct(xs, chars):
    return 100 * sum(x in chars for x in xs) / len(xs)


lines, _ = load(DATA)
tokens = [w for l in lines for w in l["words"]]
freq = Counter(tokens)

print(f"lines {len(lines)}  tokens {len(tokens)}  types {len(freq)}  "
      f"hapax {sum(c == 1 for c in freq.values())}")
print("top:", " ".join(f"{w}:{c}" for w, c in freq.most_common(30)))

sec = Counter()
for l in lines:
    sec[SECTIONS.get(l["section"], l["section"])] += len(l["words"])
print("sections:", dict(sec))

A = Counter(w for l in lines if l["language"] == "A" for w in l["words"])
B = Counter(w for l in lines if l["language"] == "B" for w in l["words"])
nA, nB = sum(A.values()), sum(B.values())
print(f"\ncurrier A {nA}  B {nB}  (per 1000)")
for w in ["daiin", "chedy", "shedy", "qokedy", "qokeedy", "chol", "chor", "cthy", "ol", "aiin"]:
    print(f"  {w:10} {1000 * A[w] / nA:5.1f} {1000 * B[w] / nB:5.1f}")

h1, h2 = entropy(" ".join(" ".join(l["words"]) for l in lines))
print(f"\nh1 {h1:.2f}  h2 {h2:.2f}")

first, mid_first, last, mid_last = [], [], [], []
for l in lines:
    ws = l["words"]
    if l["type"] != "P" or not ws:
        continue
    for i, w in enumerate(ws):
        (first if i == 0 else mid_first).append(w[0])
        (last if i == len(ws) - 1 else mid_last).append(w[-1])
print(f"gallows word-initial: line start {pct(first, 'ptkf'):.1f}%  elsewhere {pct(mid_first, 'ptkf'):.1f}%")
print(f"final m: line end {pct(last, 'm'):.1f}%  elsewhere {pct(mid_last, 'm'):.1f}%")

q = [w for w in tokens if "q" in w]
print(f"q words {len(q)}  initial {pct([w[0] for w in q], 'q'):.1f}%  "
      f"qo {100 * sum('qo' in w for w in q) / len(q):.1f}%")

reps = sum(ws[i] == ws[i - 1] for ws in (l["words"] for l in lines) for i in range(1, len(ws)))
print("repeats", reps)
