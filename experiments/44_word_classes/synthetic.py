"""What would a word cipher of Latin score on the same test?

run.py measures B at 0.09 bits. To know what that number allows, the same
test on ciphers of Latin whose output words are Voynich words, so that the
only thing that differs from the manuscript is what the words stand for:

  one word per letter: each Latin letter gets its own set of Voynich words
    (homophones), more for frequent letters, chosen with the manuscript's
    word frequencies;
  one word per syllable: Latin cut into syllable-like chunks (consonants +
    vowels), each chunk type mapped to Voynich words the same way;
  one word per word (a codebook): each Latin word type gets one Voynich word.

Text size and the rare-word merging are the same as run.py's.
"""
import pathlib
import random
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import run  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich.corpus import historical  # noqa: E402
from voynich.crack.classes import class_mi, fit  # noqa: E402

HERE = pathlib.Path(__file__).parent
K = 16

tr, te = run.vms("B")
vms_freq = Counter(w for l in tr + te for w in l)
pool = [w for w, _ in vms_freq.most_common()]
latin = run.plain(historical("Secreta_Secretorum_LAT"))


def homophone_cipher(units, rng, homophones_per_unit):
    """units: plaintext token sequence. Each unit type gets a set of Voynich
    words (disjoint between units); each token picks one by the manuscript's
    frequencies."""
    freq = Counter(units)
    words = pool[:]
    rng.shuffle(words)
    it = iter(words)
    table_ = {}
    for u, _ in freq.most_common():
        n = max(1, homophones_per_unit(freq[u]))
        try:
            table_[u] = [next(it) for _ in range(n)]
        except StopIteration:
            table_[u] = [rng.choice(pool)]
    return [rng.choices(table_[u], [vms_freq[w] for w in table_[u]])[0] for u in units]


def syllables(words):
    out = []
    for w in words:
        out += re.findall(r"[^aeiouy]*[aeiouy]+|[^aeiouy]+$", w)
    return out


def score(tokens):
    lines = run.lines_of(tokens[:2 * run.N_WORDS])
    a, b = lines[0::2], lines[1::2]
    a, b = run.cap(a, run.N_WORDS), run.cap(b, run.N_WORDS)
    f = Counter(w for l in a for w in l)
    keep = {w for w, c in f.items() if c >= run.MIN_COUNT}
    a, b = run.merge_rare(a, keep), run.merge_rare(b, keep)
    _, assign = fit(a, K)
    sh = [w for l in a for w in l]
    random.Random(0).shuffle(sh)
    it = iter(sh)
    _, a0 = fit([[next(it) for _ in l] for l in a], K)
    return class_mi(b, assign, unknown=K) - class_mi(b, a0, unknown=K), len(keep)


rng = random.Random(1)
letters = list("".join(latin))
syl = syllables(latin)
rows = []
for label, units, per in [
        ("one word per letter, ~5 homophones each", letters, lambda c: round(5 * 23 * c / len(letters))),
        ("one word per letter, ~40 homophones each", letters, lambda c: round(40 * 23 * c / len(letters))),
        ("one word per syllable, 1 homophone", syl, lambda c: 1),
        ("one word per syllable, ~3 homophones", syl, lambda c: 3 if c > 20 else 1),
        ("one word per Latin word (codebook)", latin, lambda c: 1)]:
    toks = homophone_cipher(units, rng, per)
    mi, types = score(toks)
    rows.append({"cipher of Latin": label, "frequent types": types, f"held-out MI, K={K}": mi})
    print(rows[-1], flush=True)
b = __import__("json").loads((HERE / "results" / "classes.json").read_text())
for r in b:
    if r["text"] in ("VMS Currier B", "VMS Currier A"):
        rows.append({"cipher of Latin": r["text"] + " (run.py)", "frequent types": "", f"held-out MI, K={K}": r[f"K={K}"]})
save(HERE, "synthetic", rows)
md = "# 44 word ciphers of Latin with Voynich words, same test\n\n" + table(
    rows, ["cipher of Latin", "frequent types", f"held-out MI, K={K}"])
write_md(HERE, "synthetic", md)
print(md)
