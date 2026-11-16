"""Attack 2: letters, but not written the plain way.

Exp. 31 assumed each symbol is a letter of ordinary text. Three old ideas about
the manuscript keep that and change the text instead:

  no vowels        the plaintext is written without vowels (an abjad habit,
                   or deliberate abbreviation)
  letters sorted   every word has its letters put in a fixed order (the usual
                   explanation offered for the rigid word structure)
  backwards        every word is written back to front

and three Semitic/Iranian targets written consonantally anyway: Hebrew,
Arabic, Persian (transliterated to 26 letters, some emphatics merged).

The solver doesn't care: train the language model on the transformed text and
search as before. Each variant gets its own power check (Latin held-out text,
transformed, enciphered with 100 homophones: can the solver read it?) and its
own content-free control (copying model).
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
HEBREW = dict(zip("אבגדהוזחטיכלמנסעפצקרשתךםןףץ", "abgdhvzxtyklmnsopcqrwjkmnpc"))
ARABIC = dict(zip("ابتثجحخدذرزسشصضطظعغفقكلمنهويىةءأإآؤئپچژگک",
                  "abtsjhxddrzswcdtzogfqklmnhuyyhaaaauypjzgk"))
TRANSFORMS = {
    "plain": lambda w: w,
    "no vowels": lambda w: re.sub(r"[aeiouy]", "", w),
    "letters sorted": lambda w: "".join(sorted(w)),
    "backwards": lambda w: w[::-1],
}
TARGETS = [("Latin", "no vowels"), ("Latin", "letters sorted"), ("Latin", "backwards"),
           ("Italian", "no vowels"), ("Italian", "letters sorted"), ("Italian", "backwards"),
           ("German", "no vowels"), ("German", "letters sorted"),
           ("Hebrew", "plain"), ("Arabic", "plain"), ("Persian", "plain")]


def plain(words, table=None):
    out = []
    for w in words:
        if table:
            w = "".join(table.get(c, "") for c in w)
        else:
            w = unicodedata.normalize("NFD", w.lower())
            w = "".join(c for c in w if not unicodedata.combining(c))
        w = re.sub(r"[^a-z]", "", w)
        if w:
            out.append(w)
    return out


def corpus(lang, transform):
    if lang == "Latin":
        ws = []
        for n in ["Latin_Adso", "Secreta_Secretorum_LAT", "Agrippa_Book1", "BrunoDeMagia", "Steganographia", "Picatrix"]:
            ws += historical(n, 400000)
        ws = plain(ws)
    elif lang == "Italian":
        dc = open(DATA / "external" / "naibbe-cipher" / "input" / "examples" / "divina_commedia.txt",
                  encoding="utf-8").read().split()
        ws = plain(historical("Rettorica", 400000) + dc + wikipedia("Italian", 300000))
    elif lang == "Hebrew":
        ws = plain(historical("Hebrew_Bereshit", 400000) + historical("Hebrew_Mishneh", 400000)
                   + wikipedia("Hebrew", 400000), HEBREW)
    elif lang in ("Arabic", "Persian"):
        ws = plain(wikipedia(lang, 500000), ARABIC)
    else:
        ws = plain(wikipedia(lang, 500000))
    f = TRANSFORMS[transform]
    return [x for x in (f(w) for w in ws) if x]


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
    text_name, scheme, lang, transform = args
    words = corpus(lang, transform)
    lm = LM([" ".join(words[i:i + 12]) for i in range(0, len(words), 12)], spaces=True)
    held = words[-N_WORDS:] if lang != "Latin" else [
        x for x in (TRANSFORMS[transform](w) for w in plain(historical("Latin_Aix", 60000))[:N_WORDS]) if x]
    held_lines = [held[i:i + 9] for i in range(0, len(held), 9)]
    real_text = "\n".join(" ".join(l) for l in held_lines)
    vocab_words = dictionary(words[:-N_WORDS], min_len=4 if transform == "no vowels" or lang in ("Hebrew", "Arabic", "Persian") else 5)
    truth = None
    if text_name == "power check":
        # the held-out text of this very language and transform, behind 100 homophones
        rng = random.Random(3)
        freq = Counter(c for w in held for c in w)
        alloc = {c: 1 for c in freq}
        while sum(alloc.values()) < 100:
            c = max(freq, key=lambda x: freq[x] / alloc[x])
            alloc[c] += 1
        tab, k = {}, 0
        for c, n in alloc.items():
            tab[c] = list(range(k, k + n))
            k += n
        truth = {s: c for c, ss in tab.items() for s in ss}
        tok = []
        for l in held_lines:
            for i, w in enumerate(l):
                if i:
                    tok.append(-2)
                tok.extend(rng.choice(tab[c]) for c in w)
            tok.append(-1)
        vocab = list(range(100))
        scheme = "100 homophones"
    else:
        lines = vms_texts()[text_name]
        split = {"glyphs": units.eva, "groups": groups}.get(scheme) or units.bpe([w for l in lines for w in l], 60)
        tok, vocab = glyph_stream(lines, split)
    prob = Problem(tok, len(vocab), list(LETTERS), lm)
    key, val = prob.solve(iters=6000 * max(len(vocab), 26), restarts=2, t0=5.0, t1=0.02, seed=1)
    decoded = prob.decode(key, limit=len(tok))
    real = lm.per_letter(real_text)
    r = {"text": text_name, "symbols as": scheme, "language": lang, "written": transform, "n symbols": len(vocab),
         "score": val / prob.letters(key), "real text": real, "gap": val / prob.letters(key) - real,
         "in real words": word_hits(decoded, vocab_words), "real text in words": word_hits(real_text, vocab_words),
         "sample": decoded[:80]}
    if truth:
        freq = Counter(t for t in tok if t >= 0)
        r["letters right"] = sum(freq[s] for s in range(100) if LETTERS[key[s]] == truth[s]) / sum(freq.values())
    with open(PARTIAL, "a") as f:
        f.write(json.dumps(r) + "\n")
    return r


def report():
    rows = [json.loads(l) for l in open(PARTIAL)]
    power = [r for r in rows if r["text"] == "power check"]
    md = "# 32 attack: transformed plaintext\n\n## can the solver read each variant? (held-out text, 100 homophones)\n\n"
    md += table(power, ["language", "written", "letters right", "gap", "in real words", "real text in words", "sample"])
    md += "\n## the manuscript and the control\n\ngap = best key's score per letter minus real text of that kind (0 = reads like the real thing).\n\n"
    out = []
    for lang, tr in TARGETS:
        for scheme in ("glyphs", "groups", "merged 60"):
            sel = {r["text"]: r for r in rows if r["language"] == lang and r["written"] == tr and r["symbols as"] == scheme}
            if len(sel) < 3:
                continue
            real_hits = next(iter(sel.values()))["real text in words"]
            out.append({"language": lang, "written": tr, "symbols as": scheme,
                        "gap B": sel["VMS Currier B"]["gap"], "gap A": sel["VMS Currier A"]["gap"],
                        "gap control": sel["control: copying model"]["gap"],
                        "words B": sel["VMS Currier B"]["in real words"], "words A": sel["VMS Currier A"]["in real words"],
                        "words control": sel["control: copying model"]["in real words"], "words real": real_hits})
    md += table(out, ["language", "written", "symbols as", "gap B", "gap A", "gap control", "words B", "words A",
                      "words control", "words real"])
    save(HERE, "transforms", {"power": power, "summary": out})
    write_md(HERE, "transforms", md)
    print(md)


if __name__ == "__main__":
    PARTIAL.parent.mkdir(exist_ok=True)
    done = set()
    if PARTIAL.exists():
        for line in open(PARTIAL):
            r = json.loads(line)
            done.add((r["text"], r["symbols as"], r["language"], r["written"]))
    jobs = [("power check", "100 homophones", lang, tr) for lang, tr in TARGETS
            if ("power check", "100 homophones", lang, tr) not in done]
    for lang, tr in TARGETS:
        for scheme in ("glyphs", "groups", "merged 60"):
            for text_name in ("VMS Currier B", "VMS Currier A", "control: copying model"):
                if (text_name, scheme, lang, tr) not in done:
                    jobs.append((text_name, scheme, lang, tr))
    print(len(jobs), "jobs", flush=True)
    with ProcessPoolExecutor(2) as ex:
        for r in ex.map(job, jobs):
            print(r["text"], r["symbols as"], r["language"], r["written"], round(r["gap"], 3),
                  round(r["in real words"], 3), r.get("letters right"), flush=True)
    report()
