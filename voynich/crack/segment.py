"""Cut words into at most two pieces without knowing the cipher.

A verbose cipher that writes one or two plaintext letters per word builds its
two-letter words from a "first half" and a "second half". The halves come
from small inventories, so the right cut is the one that makes both halves
frequent. Hard EM over three inventories: whole words, first halves, second
halves.
"""
import math
from collections import Counter


def fit(types, rounds=12, two_piece_cost=0.0, discount=1.0):
    """types: {word: count}. Returns {word: (piece,) or (first, second)}."""
    whole, first, second = Counter(), Counter(), Counter()
    for w, c in types.items():
        whole[w] += c
        for i in range(1, len(w)):
            first[w[:i]] += c / (len(w) - 1)
            second[w[i:]] += c / (len(w) - 1)
    seg = {}
    for _ in range(rounds):
        tw, tf, ts = sum(whole.values()), sum(first.values()), sum(second.values())
        tot = tw + tf  # tokens: either whole or split
        # every count is discounted, so a form seen once explains nothing by being listed
        d = discount
        lw = lambda w: math.log((max(whole[w] - d, 0) + 0.01) / (tw + 1)) + math.log(tw / tot + 1e-9)
        lf = lambda p: math.log((max(first[p] - d, 0) + 0.01) / (tf + 1))
        ls = lambda p: math.log((max(second[p] - d, 0) + 0.01) / (ts + 1))
        split_prior = math.log(tf / tot + 1e-9) - two_piece_cost
        nw, nf, ns = Counter(), Counter(), Counter()
        for w, c in types.items():
            best, cut = lw(w), None
            for i in range(1, len(w)):
                v = split_prior + lf(w[:i]) + ls(w[i:])
                if v > best:
                    best, cut = v, i
            if cut is None:
                seg[w] = (w,)
                nw[w] += c
            else:
                seg[w] = (w[:cut], w[cut:])
                nf[w[:cut]] += c
                ns[w[cut:]] += c
        whole, first, second = nw, nf, ns
    return seg


def stream(lines, seg, top=None):
    """Symbol stream: one symbol per piece, tagged by role so that the same
    glyph string as a whole word, a first half and a second half are three
    different symbols. Returns tokens, vocab."""
    seq = []
    for l in lines:
        row = []
        for w in l:
            s = seg.get(w)
            if s is None:
                row.append(None)
            elif len(s) == 1:
                row.append(("W:" + s[0],))
            else:
                row.append(("F:" + s[0], "S:" + s[1]))
        seq.append(row)
    freq = Counter(p for r in seq for w in r if w for p in w)
    vocab = [p for p, _ in freq.most_common(top)]
    ix = {p: i for i, p in enumerate(vocab)}
    tokens = []
    for r in seq:
        for w in r:
            if w is None:
                tokens.append(-1)
            else:
                tokens.extend(ix.get(p, -1) for p in w)
        tokens.append(-1)
    return tokens, vocab
