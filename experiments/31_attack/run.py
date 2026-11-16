"""Attack 1: is the manuscript a substitution of letters, however dressed up?

Hypothesis family: every cipher symbol stands for one plaintext letter. What a
"symbol" is, is the open part:

  glyphs         EVA glyphs, bench glyphs as units (about 25 symbols)
  groups         glyph groups from the copying model's tokeniser (ol, dy, qo, iin, ...)
  merged 60/150  frequent glyph pairs merged until 60 / 150 extra units exist
  pieces         every word cut into at most two pieces, each piece a symbol
                 (the shape of a Naibbe-type cipher), 400 commonest pieces

each with word spaces kept as spaces, or ignored. Several letters may share a
symbol set (homophones), so this covers simple, homophonic and verbose
substitution. Exp. 30: on real enciphered Latin the solver gets 99% of letters
with up to 400 symbols, and on texts with no Latin in them it stays 0.2-0.4
below real Latin per letter and finds no Latin words.

Targets: nine languages. Texts: Currier A and B (3000 words of paragraph
text each). Controls run through the identical pipeline:
  copying model     generator output, no content by construction
  shuffled glyphs   Currier B with the glyphs of each word in random order

A reading counts only if it beats the controls by a margin like the one in
exp. 30: score within ~0.05 of real text of that language and real words at
something like the real rate.
"""
import json
import pathlib
import random
import re
import sys
import unicodedata
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich
from voynich.autocopy import AutoCopy, tokens as groups
from voynich.corpus import DATA, historical, wikipedia
from voynich.crack import LM, LETTERS, Problem, dictionary, glyph_stream, word_hits
from voynich.crack import segment, units

HERE = pathlib.Path(__file__).parent
N_WORDS = 3000
PARTIAL = HERE / "results" / "partial.jsonl"
LANGS = ["Latin", "Italian", "Spanish", "French", "German", "English (Middle)", "Czech", "Hungarian", "Turkish"]
GREEK = dict(zip("αβγδεζηθικλμνξοπρστυφχψως", "abgdezhqiklmnxoprstufcyws"))


def plain(words):
    out = []
    for w in words:
        w = unicodedata.normalize("NFD", w.lower())
        w = "".join(GREEK.get(c, c) for c in w if not unicodedata.combining(c))
        w = re.sub(r"[^a-z]", "", w)
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
        dc = open(DATA / "external" / "naibbe-cipher" / "input" / "examples" / "divina_commedia.txt",
                  encoding="utf-8").read().split()
        return plain(historical("Rettorica", 400000) + dc + wikipedia("Italian", 300000))
    if lang == "English (Middle)":
        return plain(historical("AlphabetOfTales", 400000) + historical("Cirurgie", 400000))
    return plain(wikipedia(lang, 500000))


def texts():
    chart = {k: set(v) for k, v in json.loads(
        (HERE.parent / "18_autocopy_boundary" / "results" / "boundary.json").read_text())["chart"].items()}
    v = Voynich("ZL")

    def take(lines):
        out, k = [], 0
        for l in lines:
            if k >= N_WORDS:
                break
            l = [w for w in l if "?" not in w]
            if l:
                out.append(l)
                k += len(l)
        return out
    b = take(v.text_lines(unit="P", language="B"))
    rng = random.Random(4)
    return {"VMS Currier A": take(v.text_lines(unit="P", language="A")),
            "VMS Currier B": b,
            "control: copying model": take(AutoCopy(seed=1, currier="B", boundary=chart, boundary_p=0.65,
                                                    line_end_p=0.5, common_p=0.5).run(900)),
            "control: shuffled glyphs": [["".join(rng.sample(units.eva(w), len(units.eva(w)))) for w in l] for l in b]}


def symbolise(lines, scheme):
    words = [w for l in lines for w in l]
    if scheme == "glyphs":
        return glyph_stream(lines, units.eva)
    if scheme == "groups":
        return glyph_stream(lines, groups)
    if scheme.startswith("merged"):
        return glyph_stream(lines, units.bpe(words, int(scheme.split()[1])))
    seg = segment.fit(Counter(words), two_piece_cost=-2, discount=2)
    return segment.stream(lines, seg, top=400)


def job(args):
    text_name, scheme, spaces, lang = args
    lines = texts()[text_name]
    tok, vocab = symbolise(lines, scheme)
    if scheme == "pieces":
        # one word = one or two letters: there are no plaintext spaces to keep
        spaces = False
    elif not spaces:
        tok = [t for t in tok if t != -2]
    words = corpus(lang)
    lm = LM([" ".join(words[i:i + 12]) for i in range(0, len(words), 12)], spaces=spaces)
    held = words[-3000:]
    real = lm.per_letter("\n".join(" ".join(held[i:i + 9]) for i in range(0, len(held), 9)))
    prob = Problem(tok, len(vocab), list(LETTERS), lm)
    key, val = prob.solve(iters=6000 * max(len(vocab), 26), restarts=2, t0=5.0, t1=0.02, seed=1)
    decoded = prob.decode(key, limit=len(tok))
    vocab_words = dictionary(words[:-3000])
    r = {"text": text_name, "symbols as": scheme, "spaces": "kept" if spaces else "ignored", "language": lang,
         "n symbols": len(vocab), "score": val / prob.letters(key), "real text": real,
         "gap": val / prob.letters(key) - real, "in real words": word_hits(decoded, vocab_words, spaces),
         "real text in words": word_hits("\n".join(" ".join(held[i:i + 9]) for i in range(0, len(held), 9)),
                                         vocab_words, spaces),
         "sample": decoded[:90]}
    with open(PARTIAL, "a") as f:
        f.write(json.dumps(r) + "\n")
    return r


if __name__ == "__main__":
    PARTIAL.parent.mkdir(exist_ok=True)
    done = set()
    if PARTIAL.exists():
        for line in open(PARTIAL):
            r = json.loads(line)
            done.add((r["text"], r["symbols as"], r["spaces"], r["language"]))
    jobs = []
    for scheme in ["glyphs", "groups", "merged 60", "merged 150", "pieces"]:
        for spaces in ([False] if scheme == "pieces" else [True, False]):
            for lang in LANGS:
                for text_name in ["VMS Currier B", "VMS Currier A", "control: copying model", "control: shuffled glyphs"]:
                    if (text_name, scheme, "kept" if spaces else "ignored", lang) not in done:
                        jobs.append((text_name, scheme, spaces, lang))
    print(len(jobs), "jobs", flush=True)
    with ProcessPoolExecutor(2) as ex:
        for r in ex.map(job, jobs):
            print(r["text"], r["symbols as"], r["spaces"], r["language"], round(r["gap"], 3), round(r["in real words"], 3), flush=True)
