"""Attack 6: is the code different on every sheet?

Exps. 40-43: the way words are made is set per sheet, and a fixed-table
cipher can't do that. Exp. 44: Currier B's words depend on the previous word
much less than any letter or syllable cipher of Latin would (0.09 bits
against 0.28-0.69). Both would follow if the key changed with every sheet:
pooling sheets with different keys mixes up which word stands for what and
washes the sequence out. Then inside a sheet, where the key is fixed, the
sequence should be much stronger than across the book.

Test: for links between neighbouring words that a cipher would carry (first
sign -> next first sign, last -> next last, first -> next last, and the
combined start-end "shape" of the word), the mutual information
  pooled over the whole section, and
  inside each sheet, averaged (weighted by the sheet's number of pairs).
Both corrected for small-sample bias the same way: minus the same statistic
with words shuffled among words at the same line position, inside the same
sheet (so the per-sheet setting is in both the measure and the baseline).
A fixed code gives inside ~ pooled; a key per sheet gives inside >> pooled.

Calibration: ciphers of Latin made of Voynich words (exp. 44), one word per
letter, (a) one key for the whole book, (b) a new key on every sheet, cut
into sheets of the manuscript's size. Controls: the exp. 36 generator.
"""
import math
import pathlib
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "44_word_classes"))
from _common import save, table, write_md  # noqa: E402
from voynich import Voynich  # noqa: E402
from voynich.assemble import Assembler, signs  # noqa: E402

HERE = pathlib.Path(__file__).parent
SHUF = 20
FEATS = {"first -> first": (lambda s: s[0], lambda s: s[0]),
         "last -> last": (lambda s: s[-1], lambda s: s[-1]),
         "first -> last": (lambda s: s[0], lambda s: s[-1]),
         "last -> first": (lambda s: s[-1], lambda s: s[0]),
         "shape -> shape": (lambda s: (s[0], s[-1]), lambda s: (s[0], s[-1]))}


def mi(pairs):
    N = Counter(pairs)
    tot = sum(N.values())
    if not tot:
        return 0.0
    L, R = Counter(), Counter()
    for (a, b), c in N.items():
        L[a] += c
        R[b] += c
    return sum(c / tot * math.log2(c * tot / (L[a] * R[b])) for (a, b), c in N.items())


def pos(i, n):
    return 0 if i == 0 else 2 if i == n - 1 else 1


def shuffle_in_sheet(sheets, rng):
    out = []
    for lines in sheets:
        groups = defaultdict(list)
        for li, l in enumerate(lines):
            for i in range(len(l)):
                groups[pos(i, len(l))].append((li, i))
        new = [list(l) for l in lines]
        for where in groups.values():
            ws = [lines[a][b] for a, b in where]
            rng.shuffle(ws)
            for (a, b), w in zip(where, ws):
                new[a][b] = w
        out.append(new)
    return out


def stats(sheets, fa, fb):
    pairs_by_sheet = [[(fa(a), fb(b)) for l in lines for a, b in zip(l, l[1:])] for lines in sheets]
    pooled = mi([p for ps in pairs_by_sheet for p in ps])
    n = sum(len(ps) for ps in pairs_by_sheet)
    inside = sum(mi(ps) * len(ps) for ps in pairs_by_sheet if ps) / n
    return pooled, inside


def measure(sheets, rng):
    sheets = [[[signs(w) for w in l] for l in lines] for lines in sheets]
    res = {}
    base = [shuffle_in_sheet(sheets, rng) for _ in range(SHUF)]
    for name, (fa, fb) in FEATS.items():
        p, i = stats(sheets, fa, fb)
        bp = sum(stats(b, fa, fb)[0] for b in base) / SHUF
        bi = sum(stats(b, fa, fb)[1] for b in base) / SHUF
        res[name] = (p - bp, i - bi)
    return res


v = Voynich("ZL")


def vms_sheets(lang):
    by = defaultdict(list)
    for l in v.lines:
        if l.unit == "P" and l.meta.get("L") == lang and re.fullmatch(r"f\d+[rv]\d*", l.page):
            ws = [w for w in l.words if "?" not in w and "'" not in w]
            if ws:
                m = v.pages.get(l.page) or {}
                by[(m.get("Q"), m.get("B"))].append(ws)
    return [ls for ls in by.values() if sum(map(len, ls)) >= 100]


import synthetic  # noqa: E402

latin_letters = list("".join(synthetic.latin))


def cipher_sheets(template, per_sheet_key, rng):
    """Latin letters, one Voynich word per letter (5 homophones on average),
    laid out in the template's sheets and lines."""
    out, k = [], 0
    key = None
    for lines in template:
        if key is None or per_sheet_key:
            key = synthetic.homophone_cipher(latin_letters[:1], rng, lambda c: 1)  # warm the rng
            letters = {}
        n = sum(map(len, lines))
        chunk = latin_letters[k:k + n]
        k += n
        if per_sheet_key or not out:
            words = synthetic.pool[:]
            rng.shuffle(words)
            it = iter(words)
            freq = Counter(latin_letters)
            letters = {u: [next(it) for _ in range(max(1, round(5 * 23 * c / len(latin_letters))))]
                       for u, c in freq.most_common()}
        toks = [rng.choices(letters[u], [synthetic.vms_freq[w] for w in letters[u]])[0] for u in chunk]
        it2 = iter(toks)
        out.append([[next(it2) for _ in l] for l in lines])
    return out


def generator_sheets(template, rng):
    m = Assembler(order=2, recall_p=0.01, edit_p=0.10, window=5).fit([l for s in template for l in s])
    return [m.fill([(len(l), False) for l in s], seed=rng.randrange(10 ** 6)) for s in template]


rng = random.Random(0)
B = vms_sheets("B")
A = vms_sheets("A")
if __name__ == "__main__":
    texts = {"Currier B": B, "Currier A": A,
             "cipher of Latin, one key (B's sheets)": cipher_sheets(B, False, rng),
             "cipher of Latin, new key every sheet (B's sheets)": cipher_sheets(B, True, rng),
             "generator (exp. 36), B's sheets": generator_sheets(B, rng)}
    rows = []
    for name, sheets in texts.items():
        res = measure(sheets, rng)
        row = {"text": name, "sheets": len(sheets)}
        for f, (p, i) in res.items():
            row[f"{f}: pooled"] = p
            row[f"{f}: inside sheets"] = i
        rows.append(row)
        print({k: (round(x, 3) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
    save(HERE, "sheet_keys", rows)
    md = "# 47 is the code different on every sheet?\n\nMI between neighbouring words (bits), bias-corrected, pooled over the section vs inside each sheet.\n\n"
    for f in FEATS:
        md += f"## {f}\n\n" + table(rows, ["text", "sheets", f"{f}: pooled", f"{f}: inside sheets"]) + "\n"
    write_md(HERE, "sheet_keys", md)
    print(md)
