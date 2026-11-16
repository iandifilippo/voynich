"""What can the solver crack, and when does it start seeing things?

Before pointing a cipher solver at the manuscript it has to pass two tests.

  Power: given a real text enciphered with a known scheme, does it get the
  plaintext back?
  Honesty: given a text that does NOT contain the target language, how good
  a "solution" does it produce anyway?

The second matters as much as the first. A key with hundreds of free symbols
can bend almost anything towards the letter statistics of Latin.

Solver: simulated annealing over keys (symbol -> letter), scored by a letter
4-gram model of the target language plus a letter-frequency term
(voynich/crack). Target Latin; plaintext is Latin held out from the model.

Ciphers, on 4000 words of plaintext:
  substitution            26 symbols, spaces kept
  homophonic, n symbols   each letter gets homophones in proportion to its
                          frequency (n = 50, 100, 200, 400), with and without spaces
Controls, same ciphers applied to text with no Latin in it:
  Hungarian               a real language, the wrong one
  scrambled Latin         the same Latin words with their letters shuffled

Reported: letters right (where there is a truth), model score per letter
against real Latin, and the share of letters inside real Latin words.
"""
import pathlib
import random
import re
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich.corpus import historical, wikipedia, chunk_lines
from voynich.crack import LM, LETTERS, Problem, dictionary, glyph_stream, word_hits

HERE = pathlib.Path(__file__).parent
N_WORDS = 4000


def clean(words):
    out = [re.sub(r"[^a-z]", "", w.lower()) for w in words]
    return [w for w in out if w]


def latin_training():
    words = []
    for name in ["Latin_Adso", "Secreta_Secretorum_LAT", "Agrippa_Book1", "BrunoDeMagia", "Steganographia", "Picatrix"]:
        words += clean(historical(name, 400000))
    return words


def homophonic(lines, n_symbols, seed):
    """letter -> one of its homophones at random; homophones allotted by frequency"""
    rng = random.Random(seed)
    freq = Counter(c for l in lines for w in l for c in w)
    total = sum(freq.values())
    alloc = {c: 1 for c in freq}
    while sum(alloc.values()) < n_symbols:
        c = max(freq, key=lambda x: freq[x] / total / alloc[x])
        alloc[c] += 1
    table, k = {}, 0
    for c, n in alloc.items():
        table[c] = list(range(k, k + n))
        k += n
    truth = {s: c for c, ss in table.items() for s in ss}
    return [[[rng.choice(table[c]) for c in w] for w in l] for l in lines], truth


def run(job):
    name, source, n_symbols, spaces, seed = job
    train = latin_training()
    lm = LM([" ".join(train[i:i + 12]) for i in range(0, len(train), 12)], spaces=spaces)
    vocab_words = dictionary(train)
    if source == "Latin":
        words = clean(historical("Latin_Aix", 60000))[:N_WORDS]
    elif source == "Hungarian":
        words = [w for w in clean(wikipedia("Hungarian", 40000)) if len(w) > 1][:N_WORDS]
    else:
        rng = random.Random(7)
        words = ["".join(rng.sample(w, len(w))) for w in clean(historical("Latin_Aix", 60000))[:N_WORDS]]
    lines = chunk_lines(words)
    enc, truth = homophonic(lines, n_symbols, seed)
    tokens = []
    for l in enc:
        for k, w in enumerate(l):
            if k and spaces:
                tokens.append(-2)
            tokens.extend(w)
        tokens.append(-1)
    units = [c for c in LETTERS]
    prob = Problem(tokens, n_symbols, units, lm)
    iters = 8000 * n_symbols          # cost per step falls as symbols get rarer, so this is constant work
    key, val = prob.solve(iters=iters, restarts=2, t0=5.0, t1=0.02, seed=seed)
    freq = Counter(t for t in tokens if t >= 0)
    acc = sum(freq[s] for s in range(n_symbols) if units[key[s]] == truth.get(s)) / sum(freq.values())
    decoded = prob.decode(key, limit=len(tokens))
    plain = "\n".join(" ".join(l) for l in lines)
    real = lm.per_letter("\n".join(" ".join(l) for l in chunk_lines(clean(historical("Latin_Aix", 60000))[:N_WORDS])))
    return {"cipher": name, "plaintext": source, "symbols": n_symbols, "spaces": "kept" if spaces else "removed",
            "letters right": acc if source == "Latin" else None,
            "score per letter": val / prob.letters(key), "real Latin": real,
            "in Latin words": word_hits(decoded, vocab_words, spaces),
            "real Latin in words": word_hits(plain, vocab_words, spaces) if source == "Latin" else None,
            "sample": decoded[:70]}


if __name__ == "__main__":
    jobs = []
    for source in ("Latin", "Hungarian", "scrambled Latin"):
        jobs.append(("substitution", source, 26, True, 1))
        for n in (50, 100, 200, 400):
            jobs.append((f"homophonic {n}", source, n, True, 1))
        for n in (50, 200, 400):
            jobs.append((f"homophonic {n}", source, n, False, 1))
    with ProcessPoolExecutor(2) as ex:
        rows = list(ex.map(run, jobs))
    for r in rows:
        print({k: round(v, 3) if isinstance(v, float) else v for k, v in r.items()})
    save(HERE, "calibration", rows)
    md = "# 30 solver calibration (target: Latin)\n\n"
    for source in ("Latin", "Hungarian", "scrambled Latin"):
        md += f"\n## plaintext: {source}\n\n" + table(
            [r for r in rows if r["plaintext"] == source],
            ["cipher", "spaces", "symbols", "letters right", "score per letter", "real Latin", "in Latin words",
             "real Latin in words", "sample"])
    write_md(HERE, "calibration", md)
    print(md)
