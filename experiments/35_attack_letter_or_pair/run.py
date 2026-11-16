"""Attack 4: a word is one letter or two (the Naibbe family), full text.

Exp. 33 could not read this family. Two things were wrong and neither was
the annealer. The text was too short, and the words were cut in the wrong
places: with one cut in five misplaced, letters are inserted and dropped all
along the stream and no key can score.

The fix for the cuts is one assumption about the cipher. A word that stands
for a single letter is far more frequent than one that stands for a pair, so
the k most frequent words are taken whole and every other word is cut where
both halves are commonest (segment.fit_ranked). k is not known: three values
are tried and the score decides.

Entry test: the Naibbe cipher of Pliny, from the ciphertext alone. Then the
manuscript (Currier A and B separately) and the copying model, in Latin,
and Italian. And every text again with its words in random order: a
real message is a sequence, so shuffling must cost it; if a text scores the
same shuffled, the solver found letter statistics, not a message. The Naibbe
text is also attacked in German, to see what the wrong language looks like.

One annealing run finds the Naibbe plaintext about two times in three, and a
run that misses scores visibly lower, so each job is the best of four.
"""
import csv
import difflib
import json
import multiprocessing
import pathlib
import random
import re
import sys
import unicodedata
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _common  # noqa: F401
from voynich import Voynich
from voynich.autocopy import AutoCopy
from voynich.corpus import DATA, historical, wikipedia
from voynich.crack import LM, Problem, segment

HERE = pathlib.Path(__file__).parent
PARTIAL = HERE / "results" / "partial.jsonl"
NB = DATA / "external" / "naibbe-cipher"
LANGS = ["Latin", "Italian"]
KS = [60, 110, 200]
TOP = 500


def plain(words):
    out = []
    for w in words:
        w = unicodedata.normalize("NFD", w.lower())
        w = re.sub(r"[^a-z]", "", "".join(c for c in w if not unicodedata.combining(c)))
        if w:
            out.append(w)
    return out


def corpus(lang):
    if lang == "Latin":
        ws = []
        for n in ["Latin_Aix", "Latin_Adso", "Secreta_Secretorum_LAT", "Agrippa_Book1", "BrunoDeMagia",
                  "Steganographia", "Picatrix"]:
            ws += historical(n, 400000)
        return plain(ws)
    if lang == "Italian":
        return plain(historical("Rettorica", 400000) + wikipedia("Italian", 400000))
    return plain(wikipedia(lang, 500000))


def naibbe_plain(words):
    uni, pre, suf = {}, {}, {}
    for code, g in list(csv.reader(open(NB / "references" / "naibbe_tables.csv", encoding="utf-8-sig")))[1:]:
        kind, _, let = code.split("_")
        {"unigram": uni, "prefix": pre, "suffix": suf}[kind].setdefault(g, let)
    out = []
    for w in words:
        if w in uni:
            out.append(uni[w])
            continue
        for i in range(1, len(w)):
            if w[:i] in pre and w[i:] in suf:
                out.append(pre[w[:i]] + suf[w[i:]])
                break
    return "".join(out)


def texts():
    chart = {k: set(x) for k, x in json.loads(
        (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
    v = Voynich("ZL")
    body = [l for l in v.lines if l.unit == "P"]
    t = {"Naibbe cipher of Pliny": open(NB / "encrypted" / "nathist_output_ciphertext.txt",
                                        encoding="utf-8-sig").read().split(),
         "VMS, Currier A": [w for l in body if l.meta.get("L") == "A" for w in l.words],
         "VMS, Currier B": [w for l in body if l.meta.get("L") == "B" for w in l.words],
         "copying model": [w for l in AutoCopy(seed=1, boundary=chart, boundary_p=0.65, line_end_p=0.5,
                                               common_p=0.5).run(3000) for w in l]}
    return {k: [w for w in ws if w and "?" not in w] for k, ws in t.items()}


_lm = {}


def model(lang):
    if lang not in _lm:
        ws = corpus(lang)
        cut = int(len(ws) * 0.85)
        lm = LM(" ".join(ws[:cut]), spaces=False)
        _lm[lang] = (lm, lm.per_letter(" ".join(ws[cut:])))
    return _lm[lang]


def job(args):
    name, order, k, lang = args
    words = TEXTS[name]
    if order == "shuffled":
        words = words[:]
        random.Random(1).shuffle(words)
    seg = segment.fit_ranked(Counter(words), k)
    tokens, vocab = segment.stream([words], seg, top=TOP)
    lm, real = model(lang)
    p = Problem(tokens, len(vocab), list("abcdefghijklmnopqrstuvwxyz"), lm)
    key, _ = p.solve(iters=min(8000 * len(vocab), 4000000), restarts=4, seed=k)
    dec = p.decode(key, limit=10 ** 9).replace("#", "")
    row = {"text": name, "order": order, "k": k, "language": lang, "symbols": len(vocab), "letters": len(dec),
           "pieces": len({x for w in set(words) for x in zip("FS" if len(seg[w]) == 2 else "W", seg[w])}),
           "covered": sum(t >= 0 for t in tokens) / (len(tokens) - 1),
           "score": p.score(key) / len(tokens), "real": real, "sample": dec[:160]}
    row["gap"] = row["real"] - row["score"]
    if name.startswith("Naibbe") and order == "as written":
        row["similarity to plaintext"] = difflib.SequenceMatcher(
            None, dec[:3000], naibbe_plain(words)[:3000], autojunk=False).ratio()
    return row


TEXTS = texts()

if __name__ == "__main__":
    done = set()
    if PARTIAL.exists():
        done = {(r["text"], r["order"], r["k"], r["language"]) for r in map(json.loads, open(PARTIAL))}
    jobs = [(n, o, k, l) for n in TEXTS for l in LANGS for k in KS for o in ("as written", "shuffled")]
    jobs += [("Naibbe cipher of Pliny", "as written", k, "German") for k in KS]
    jobs = [j for j in jobs if j not in done]
    with multiprocessing.Pool(2) as pool:
        for row in pool.imap_unordered(job, jobs):
            with open(PARTIAL, "a") as f:
                f.write(json.dumps(row) + "\n")
            print({k: v for k, v in row.items() if k != "sample"}, flush=True)
