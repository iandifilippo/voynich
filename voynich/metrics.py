"""Text statistics. Everything takes a list of lines (each a list of words)
so the same code runs on Voynichese, plaintext and cipher output."""
import math
import random
from collections import Counter


def flatten(lines):
    return [w for l in lines for w in l]


def entropy(counter):
    n = sum(counter.values())
    return -sum(c / n * math.log2(c / n) for c in counter.values() if c)


def char_entropies(words):
    """h1 and conditional h2 over the glyph stream, space included."""
    s = " ".join(words)
    uni = Counter(s)
    bi = Counter(s[i - 1:i + 1] for i in range(1, len(s)))
    h1 = entropy(uni)
    return math.log2(len(uni)), h1, entropy(bi) - h1


def mutual_info(pairs):
    pairs = list(pairs)
    if not pairs:
        return 0.0
    a = Counter(x for x, _ in pairs)
    b = Counter(y for _, y in pairs)
    ab = Counter(pairs)
    n = len(pairs)
    return sum(c / n * math.log2((c / n) / ((a[x] / n) * (b[y] / n))) for (x, y), c in ab.items())


def edge_coupling(lines, seed=0):
    """MI between the last glyph of a word and the first glyph of the next one,
    minus the same measure after shuffling words (removes the frequency effect)."""
    obs = mutual_info((l[i][-1], l[i + 1][0]) for l in lines for i in range(len(l) - 1))
    rng = random.Random(seed)
    words = flatten(lines)
    rng.shuffle(words)
    shuf = mutual_info((words[i][-1], words[i + 1][0]) for i in range(len(words) - 1))
    return obs - shuf


def word_mi(lines, seed=0):
    """MI between consecutive words relative to word entropy, shuffle-corrected."""
    words = flatten(lines)
    obs = mutual_info((l[i], l[i + 1]) for l in lines for i in range(len(l) - 1))
    rng = random.Random(seed)
    sw = words[:]
    rng.shuffle(sw)
    base = mutual_info((sw[i], sw[i + 1]) for i in range(len(sw) - 1))
    h = entropy(Counter(words))
    return (obs - base) / h if h else 0.0


def zipf_slope(words, top=1000):
    freqs = sorted(Counter(words).values(), reverse=True)[:top]
    xs = [math.log(i + 1) for i in range(len(freqs))]
    ys = [math.log(f) for f in freqs]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den else 0.0


def mattr(words, window=500):
    if len(words) < window:
        return len(set(words)) / max(len(words), 1)
    c = Counter(words[:window])
    total = len(c)
    for i in range(window, len(words)):
        c[words[i]] += 1
        old = words[i - window]
        c[old] -= 1
        if c[old] == 0:
            del c[old]
        total += len(c)
    return total / (len(words) - window + 1) / window


def jsd(p, q):
    keys = set(p) | set(q)
    sp, sq = sum(p.values()), sum(q.values())
    out = 0.0
    for k in keys:
        a, b = p.get(k, 0) / sp, q.get(k, 0) / sq
        m = (a + b) / 2
        if a:
            out += 0.5 * a * math.log2(a / m)
        if b:
            out += 0.5 * b * math.log2(b / m)
    return out


def line_effects(lines):
    """How different line-initial and line-final words are from line-internal ones."""
    first, mid_f, last, mid_l = Counter(), Counter(), Counter(), Counter()
    for l in lines:
        if len(l) < 3:
            continue
        for i, w in enumerate(l):
            (first if i == 0 else mid_f)[w[0]] += 1
            (last if i == len(l) - 1 else mid_l)[w[-1]] += 1
    if not first or not last:
        return 0.0, 0.0
    return jsd(first, mid_f), jsd(last, mid_l)


def line_cohesion(lines, rounds=5, seed=0):
    """Repeated word types inside the same line, observed / expected
    when tokens are dealt back into lines of the same lengths at random."""
    def repeats(ls):
        return sum(len(l) - len(set(l)) for l in ls)
    obs = repeats(lines)
    rng = random.Random(seed)
    words = flatten(lines)
    exp = 0
    for _ in range(rounds):
        rng.shuffle(words)
        out, i = [], 0
        for l in lines:
            out.append(words[i:i + len(l)])
            i += len(l)
        exp += repeats(out)
    exp /= rounds
    return obs / exp if exp else 0.0


def profile(lines, n_words=None):
    """Full feature vector for a text. n_words truncates for fair comparison."""
    if n_words:
        out, k = [], 0
        for l in lines:
            if k >= n_words:
                break
            out.append(l[: n_words - k])
            k += len(out[-1])
        lines = out
    words = flatten(lines)
    freq = Counter(words)
    h0, h1, h2 = char_entropies(words)
    lf, ll = line_effects(lines)
    lens = [len(w) for w in words]
    ml = sum(lens) / len(lens)
    return {
        "tokens": len(words),
        "types": len(freq),
        "hapax_ratio": sum(1 for c in freq.values() if c == 1) / len(freq),
        "mattr500": mattr(words),
        "word_len": ml,
        "word_len_sd": (sum((x - ml) ** 2 for x in lens) / len(lens)) ** 0.5,
        "alphabet": 2 ** h0,
        "h1": h1,
        "h2": h2,
        "zipf": zipf_slope(words),
        "edge_coupling": edge_coupling(lines),
        "word_mi": word_mi(lines),
        "repeat_rate": 1000 * sum(l[i] == l[i - 1] for l in lines for i in range(1, len(l))) / len(words),
        "line_first_jsd": lf,
        "line_last_jsd": ll,
        "line_cohesion": line_cohesion(lines),
    }
