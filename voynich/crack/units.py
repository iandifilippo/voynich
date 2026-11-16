"""Ways of cutting Voynich words into cipher symbols."""
from collections import Counter

BENCH = ["cth", "ckh", "cph", "cfh", "ch", "sh"]


def eva(word):
    """EVA glyphs, with the bench glyphs as single symbols"""
    out, i = [], 0
    while i < len(word):
        for b in BENCH:
            if word.startswith(b, i):
                out.append(b)
                i += len(b)
                break
        else:
            out.append(word[i])
            i += 1
    return out


def bpe(words, merges):
    """Learn `merges` pair merges on top of eva(); returns a split(word) function."""
    types = Counter(words)
    seqs = {w: eva(w) for w in types}
    rules = []
    for _ in range(merges):
        pairs = Counter()
        for w, s in seqs.items():
            for i in range(len(s) - 1):
                pairs[s[i], s[i + 1]] += types[w]
        if not pairs:
            break
        (a, b), _ = pairs.most_common(1)[0]
        rules.append((a, b))
        for w, s in seqs.items():
            t, i = [], 0
            while i < len(s):
                if i + 1 < len(s) and s[i] == a and s[i + 1] == b:
                    t.append(a + b)
                    i += 2
                else:
                    t.append(s[i])
                    i += 1
            seqs[w] = t

    def split(word):
        if word in seqs:
            return seqs[word]
        s = eva(word)
        for a, b in rules:
            t, i = [], 0
            while i < len(s):
                if i + 1 < len(s) and s[i] == a and s[i + 1] == b:
                    t.append(a + b)
                    i += 2
                else:
                    t.append(s[i])
                    i += 1
            s = t
        return s
    return split
