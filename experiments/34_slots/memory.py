"""How far back does a word remember? No slot grammar needed.

Cost of a held-out word under a model that sees only the previous sign,
against one that sees the last two, three, four. In a language the longer
view pays: a word is a lexical item, and its ending depends on its whole
stem. If the words come out of a walk through a table or a state machine,
the previous sign is nearly all there is to know.

Every text is cut to the same number of words. Models are interpolated
(Witten-Bell), trained on four fifths of the tokens and scored on the rest.
"""
import json
import math
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA, historical

HERE = pathlib.Path(__file__).parent
N_WORDS = 11000
UNIT = re.compile(r"c[tkpf]h|ch|sh|eee|ee|iii|ii|.")


def bits(words, split, order, rng, folds=5):
    seqs = [tuple(split(w)) + ("$",) for w in words]
    idx = list(range(len(seqs)))
    rng.shuffle(idx)
    alphabet = len({s for q in seqs for s in q})
    cost = signs = 0
    for f in range(folds):
        tabs = [defaultdict(Counter) for _ in range(order + 1)]
        for k, i in enumerate(idx):
            if k % folds == f:
                continue
            q = ("^",) * order + seqs[i]
            for j in range(order, len(q)):
                for o in range(order + 1):
                    tabs[o][q[j - o:j]][q[j]] += 1
        for i in idx[f::folds]:
            q = ("^",) * order + seqs[i]
            for j in range(order, len(q)):
                c0 = tabs[0][()]
                p = (c0[q[j]] + 0.5) / (sum(c0.values()) + 0.5 * alphabet)
                for o in range(1, order + 1):
                    c = tabs[o].get(q[j - o:j])
                    if not c:
                        continue
                    n, t = sum(c.values()), len(c)
                    p = (c[q[j]] + t * p) / (n + t)
                cost -= math.log2(p)
                signs += 1
    return cost / len(seqs), signs / len(seqs)


def eva(w):
    return UNIT.findall(w)


chart = {k: set(x) for k, x in json.loads(
    (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
v = Voynich("ZL")
body = [l for l in v.lines if l.unit == "P"]
texts = [("VMS, Currier A", [w for l in body if l.meta.get("L") == "A" for w in l.words], eva),
         ("VMS, Currier B", [w for l in body if l.meta.get("L") == "B" for w in l.words], eva),
         ("copying model", [w for l in AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5,
                                                common_p=0.5).run(4500) for w in l], eva)]
src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
if src.exists():
    texts.append(("Naibbe cipher of Pliny", open(src, encoding="utf-8-sig").read().split(), eva))
for name in ("Secreta_Secretorum_LAT", "Latin_Adso", "Picatrix", "Rettorica", "Cirurgie", "Agrippa_Book1",
             "Steganographia", "Sindbad", "Hebrew_Mishneh", "Amirandar", "Codex_Wormianus_dip"):
    try:
        texts.append((name, historical(name), list))
    except Exception as e:
        print("skip", name, e)

rows = []
for name, words, split in texts:
    words = [w for w in words if w and "?" not in w][:N_WORDS]
    if len(words) < N_WORDS:
        print("short", name, len(words))
        continue
    r = {"text": name, "distinct words": len(set(words))}
    for o in (1, 2, 3, 4):
        b, s = bits(words, split, o, random.Random(0))
        r[f"sees {o}"] = b
    r["signs per word"] = s - 1
    r["gain from seeing 4 instead of 1"] = r["sees 1"] - r["sees 4"]
    r["gain, share"] = r["gain from seeing 4 instead of 1"] / r["sees 1"]
    r["gain from 2 to 4"] = r["sees 2"] - r["sees 4"]
    rows.append(r)
    print(r, flush=True)

save(HERE, "memory", rows)
md = "# 34 how far back a word remembers\n\nHeld-out bits per word.\n\n" + table(
    rows, ["text", "distinct words", "signs per word", "sees 1", "sees 2", "sees 3", "sees 4",
           "gain from seeing 4 instead of 1", "gain, share", "gain from 2 to 4"])
write_md(HERE, "memory", md)
print(md)

# same thing with every EVA character as its own sign, so the result does not
# rest on which strokes were grouped into units
plain = []
for name, words, split in texts[:4]:
    words = [w for w in words if w and "?" not in w][:N_WORDS]
    r = {"text": name}
    for o in (1, 2, 3, 4, 6):
        r[f"sees {o}"] = bits(words, list, o, random.Random(0))[0]
    r["best"] = min((1, 2, 3, 4, 6), key=lambda o: r[f"sees {o}"])
    r["gain from 3 to 6"] = r["sees 3"] - r["sees 6"]
    plain.append(r)
    print(r, flush=True)
save(HERE, "memory_plain", plain)
md2 = "\n## Every EVA character a sign\n\n" + table(plain, ["text", "sees 1", "sees 2", "sees 3", "sees 4", "sees 6", "best", "gain from 3 to 6"])
write_md(HERE, "memory", md + md2)
print(md2)


# Is there a lexicon on top of the sign statistics? Cost of a held-out word
# when the model may also remember whole words (falling back on the two-sign
# model for words it has not seen), against the two-sign model alone.
def lexicon_gain(words, split, rng, folds=5, order=2):
    seqs = [tuple(split(w)) + ("$",) for w in words]
    idx = list(range(len(seqs)))
    rng.shuffle(idx)
    alphabet = len({s for q in seqs for s in q})
    a = b = 0.0
    for f in range(folds):
        tabs = [defaultdict(Counter) for _ in range(order + 1)]
        lex = Counter()
        for k, i in enumerate(idx):
            if k % folds == f:
                continue
            lex[seqs[i]] += 1
            q = ("^",) * order + seqs[i]
            for j in range(order, len(q)):
                for o in range(order + 1):
                    tabs[o][q[j - o:j]][q[j]] += 1
        n, t = sum(lex.values()), len(lex)
        for i in idx[f::folds]:
            q = ("^",) * order + seqs[i]
            lp = 0.0
            for j in range(order, len(q)):
                c0 = tabs[0][()]
                p = (c0[q[j]] + 0.5) / (sum(c0.values()) + 0.5 * alphabet)
                for o in range(1, order + 1):
                    c = tabs[o].get(q[j - o:j])
                    if c:
                        p = (c[q[j]] + len(c) * p) / (sum(c.values()) + len(c))
                lp += math.log2(p)
            a -= lp
            b -= math.log2((lex[seqs[i]] + t * 2 ** lp) / (n + t))
    return a / len(seqs), b / len(seqs)


lexrows = []
for name, words, split in texts:
    words = [w for w in words if w and "?" not in w][:N_WORDS]
    if len(words) < N_WORDS:
        continue
    a, b = lexicon_gain(words, split, random.Random(0))
    lexrows.append({"text": name, "two signs": a, "two signs + remembered words": b, "what the lexicon saves": a - b,
                    "share": (a - b) / a})
    print(lexrows[-1], flush=True)
save(HERE, "memory_lexicon", lexrows)
md3 = "\n## Does remembering whole words help?\n\n" + table(
    lexrows, ["text", "two signs", "two signs + remembered words", "what the lexicon saves", "share"])
write_md(HERE, "memory", md + md2 + md3)
print(md3)
