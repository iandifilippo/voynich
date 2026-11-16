"""How much does a letter-perfect anagram prove?

A 2026 Zenodo preprint ("Voynich f99r Deciphered: Italian Anagrams of a Spagyric
Recipe", record 20109175) maps Voynich labels to letters and then anagrams each
string into Italian words. Before looking at any specific mapping, the question
is how often *any* string of that length can be anagrammed into Italian.

We build an Italian word list from the Lindemann & Bowern corpora (Italian
Wikipedia + Brunetto Latini's Rettorica) and count, for strings of 4-9 letters:
  - one-word anagram exists
  - two-word anagram exists (split the letters into two Italian words)
for (a) scrambled real Italian words (control, should be 100%), (b) random
strings with Italian letter frequencies, (c) Voynich words pushed through a
frequency-matched glyph->letter key (most common glyph -> most common letter...).
If (b) and (c) succeed about as often as (a), a successful anagram is not evidence.
"""
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich import Voynich, historical, wikipedia

HERE = pathlib.Path(__file__).parent
rng = random.Random(0)

it_words = wikipedia("Italian", 400000) + historical("Rettorica")
freq = Counter(w for w in it_words if w.isalpha() and all(c in "abcdefghilmnopqrstuvz" for c in w))
VOCAB_SIZE = 30000
vocab = [w for w, _ in freq.most_common(VOCAB_SIZE) if len(w) >= 2]
by_key = defaultdict(set)
for w in vocab:
    by_key["".join(sorted(w))].add(w)
keys_by_len = defaultdict(list)
for k in by_key:
    keys_by_len[len(k)].append(Counter(k))

letters = Counter(c for w, n in freq.items() for c in w for _ in range(n))
alpha, weights = zip(*letters.most_common())


def one_word(s):
    return "".join(sorted(s)) in by_key


def two_words(s):
    c = Counter(s)
    n = len(s)
    for L in range(2, n - 1):
        for kc in keys_by_len[L]:
            if all(c[x] >= m for x, m in kc.items()):
                rest = "".join(sorted((c - kc).elements()))
                if rest in by_key:
                    return True
    return False


v = Voynich("ZL")
vwords = [w for w in v.words(unit="P")]
glyph_rank = [g for g, _ in Counter(c for w in vwords for c in w).most_common()]
key = {g: alpha[i % len(alpha)] for i, g in enumerate(glyph_rank)}

rows = []
N = 300
for L in range(4, 10):
    real = [w for w in vocab if len(w) == L]
    samples = {
        "scrambled Italian words": ["".join(rng.sample(w, len(w))) for w in rng.sample(real, min(N, len(real)))],
        "random, Italian letter frequencies": ["".join(rng.choices(alpha, weights, k=L)) for _ in range(N)],
        "Voynich words, frequency key": ["".join(key[c] for c in w) for w in rng.sample([w for w in vwords if len(w) == L], N)],
    }
    for name, ss in samples.items():
        rows.append({"length": L, "strings": name, "n": len(ss),
                     "one_word": sum(map(one_word, ss)) / len(ss),
                     "two_words": sum(one_word(s) or two_words(s) for s in ss) / len(ss)})

save(HERE, "anagrams", {"vocab_size": len(vocab), "rows": rows})
md = "# c03 anagram freedom\n\n"
md += f"Italian vocabulary: {len(vocab)} most frequent word forms. Share of strings that can be rearranged into one Italian word, or into one or two.\n\n"
md += table(rows, ["length", "strings", "n", "one_word", "two_words"])
write_md(HERE, "anagrams", md)
print(md)
