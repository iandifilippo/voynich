"""Attack 3: a sign is a letter or a pair of letters.

A syllabary, or a cipher that writes common letter pairs with one sign (as the
Naibbe cipher does at the level of words), makes each sign worth one or two
letters. With about two to three sign-like units per Voynich word (c05), that
would give words of three to five letters, which is the right size.

The key now maps each symbol to a letter or to one of the language's 150
commonest letter pairs. That is a much bigger search than exp. 31, so it gets
its own calibration first:

  power    held-out Latin / Italian written with a sign for each of the
           N commonest pairs plus a sign per letter (N = 60, 150), greedy
           longest match; spaces kept. Can the solver read it?
  honesty  Hungarian written the same way, solved towards Latin.

Then the manuscript: symbols = glyph groups (about 50) and merged units
(60 and 150 merges), spaces kept; Currier A and B, and the copying model.
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
from voynich.crack import units

HERE = pathlib.Path(__file__).parent
N_WORDS = 3000
PARTIAL = HERE / "results" / "partial.jsonl"
LANGS = ["Latin", "Italian", "Spanish", "French", "German", "Czech", "Hungarian", "Turkish"]


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
        for n in ["Latin_Adso", "Secreta_Secretorum_LAT", "Agrippa_Book1", "BrunoDeMagia", "Steganographia", "Picatrix"]:
            ws += historical(n, 400000)
        return plain(ws)
    if lang == "Italian":
        dc = open(DATA / "external" / "naibbe-cipher" / "input" / "examples" / "divina_commedia.txt",
                  encoding="utf-8").read().split()
        return plain(historical("Rettorica", 400000) + dc + wikipedia("Italian", 300000))
    return plain(wikipedia(lang, 500000))


def held_out(lang, words):
    if lang == "Latin":
        return plain(historical("Latin_Aix", 60000))[:N_WORDS]
    return words[-N_WORDS:]


def top_pairs(words, n):
    c = Counter(w[i:i + 2] for w in words for i in range(len(w) - 1))
    return [p for p, _ in c.most_common(n)]


def pair_cipher(lines, pairs):
    """greedy: a sign for the pair if it is in the list, else a sign for the letter"""
    pairs = set(pairs)
    out = []
    for l in lines:
        row = []
        for w in l:
            s, i = [], 0
            while i < len(w):
                if w[i:i + 2] in pairs:
                    s.append(w[i:i + 2])
                    i += 2
                else:
                    s.append(w[i])
                    i += 1
            row.append(s)
        out.append(row)
    return out


def vms_texts():
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
    return {"VMS Currier B": take(v.text_lines(unit="P", language="B")),
            "VMS Currier A": take(v.text_lines(unit="P", language="A")),
            "control: copying model": take(AutoCopy(seed=1, currier="B", boundary=chart, boundary_p=0.65,
                                                    line_end_p=0.5, common_p=0.5).run(900))}


def job(args):
    kind, text_name, scheme, lang = args
    words = corpus(lang)
    lm = LM([" ".join(words[i:i + 12]) for i in range(0, len(words), 12)], spaces=True)
    train = words[:-N_WORDS]
    key_units = list(LETTERS) + top_pairs(train, 150)
    vocab_words = dictionary(train)
    held = held_out(lang, words)
    real_text = "\n".join(" ".join(held[i:i + 9]) for i in range(0, len(held), 9))
    truth = None
    if kind == "calibration":
        src_lang, n_pairs = text_name.split("|")
        src_words = corpus(src_lang)
        src = held_out(src_lang, src_words)
        lines = [src[i:i + 9] for i in range(0, len(src), 9)]
        enc = pair_cipher(lines, top_pairs(src_words[:-N_WORDS], int(n_pairs)))
        tok, vocab = glyph_stream([["\x00".join(w) for w in l] for l in enc], lambda w: w.split("\x00"))
        truth = vocab
    else:
        lines = vms_texts()[text_name]
        split = groups if scheme == "groups" else units.bpe([w for l in lines for w in l], int(scheme.split()[1]))
        tok, vocab = glyph_stream(lines, split)
    prob = Problem(tok, len(vocab), key_units, lm)
    key, val = prob.solve(iters=40000 * max(len(vocab), 26), restarts=2, t0=5.0, t1=0.02, seed=1)
    decoded = prob.decode(key, limit=len(tok))
    real = lm.per_letter(real_text)
    r = {"kind": kind, "text": text_name, "symbols as": scheme, "language": lang, "n symbols": len(vocab),
         "score": val / prob.letters(key), "real text": real, "gap": val / prob.letters(key) - real,
         "in real words": word_hits(decoded, vocab_words), "real text in words": word_hits(real_text, vocab_words),
         "letters per symbol": prob.letters(key) / max(1, sum(t >= 0 for t in tok)), "sample": decoded[:80]}
    if truth and text_name.split("|")[0] == lang:
        freq = Counter(t for t in tok if t >= 0)
        r["signs right"] = sum(freq[s] for s in range(len(vocab)) if key_units[key[s]] == truth[s]) / sum(freq.values())
    with open(PARTIAL, "a") as f:
        f.write(json.dumps(r) + "\n")
    return r


def report():
    rows = [json.loads(l) for l in open(PARTIAL)]
    cal = [r for r in rows if r["kind"] == "calibration"]
    for r in cal:
        r["plaintext"], r["pair signs"] = r["text"].split("|")
    md = "# 33 attack: a sign is a letter or a pair\n\n## calibration\n\n" + table(
        cal, ["plaintext", "pair signs", "language", "n symbols", "signs right", "gap", "in real words",
              "real text in words", "sample"])
    out = []
    for lang in LANGS:
        for scheme in ("groups", "merged 60", "merged 150"):
            sel = {r["text"]: r for r in rows if r["kind"] == "attack" and r["language"] == lang and r["symbols as"] == scheme}
            if len(sel) == 3:
                out.append({"language": lang, "symbols as": scheme, "n symbols": sel["VMS Currier B"]["n symbols"],
                            "gap B": sel["VMS Currier B"]["gap"], "gap A": sel["VMS Currier A"]["gap"],
                            "gap control": sel["control: copying model"]["gap"],
                            "words B": sel["VMS Currier B"]["in real words"], "words A": sel["VMS Currier A"]["in real words"],
                            "words control": sel["control: copying model"]["in real words"],
                            "words real": sel["VMS Currier B"]["real text in words"],
                            "sample B": sel["VMS Currier B"]["sample"][:60]})
    md += "\n## the manuscript and the control\n\n" + table(
        out, ["language", "symbols as", "n symbols", "gap B", "gap A", "gap control", "words B", "words A",
              "words control", "words real", "sample B"])
    save(HERE, "pairs", {"calibration": cal, "attack": out})
    write_md(HERE, "pairs", md)
    print(md)


if __name__ == "__main__":
    PARTIAL.parent.mkdir(exist_ok=True)
    done = set()
    if PARTIAL.exists():
        for line in open(PARTIAL):
            r = json.loads(line)
            done.add((r["kind"], r["text"], r["symbols as"], r["language"]))
    jobs = [("calibration", f"{src}|{n}", "pair cipher", tgt)
            for src, tgt in [("Latin", "Latin"), ("Italian", "Italian"), ("Hungarian", "Latin"), ("Hungarian", "Italian")]
            for n in (60, 150)]
    if "--calibrate" not in sys.argv:
        for lang in LANGS:
            for scheme in ("groups", "merged 60", "merged 150"):
                for text_name in ("VMS Currier B", "VMS Currier A", "control: copying model"):
                    jobs.append(("attack", text_name, scheme, lang))
    jobs = [j for j in jobs if j not in done]
    print(len(jobs), "jobs", flush=True)
    with ProcessPoolExecutor(2) as ex:
        for r in ex.map(job, jobs):
            print(r["kind"], r["text"], r["symbols as"], r["language"], r["n symbols"], round(r["gap"], 3),
                  round(r["in real words"], 3), r.get("signs right"), flush=True)
    report()
