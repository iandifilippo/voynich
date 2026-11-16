"""Stephen Bax (2014), "A proposed partial decoding of the Voynich script".

Bax read about ten words as proper names (kydainy f2r = 'kantairon', centaury;
koaiin f3v = 'kaur', hellebore; the f68r label = 'taurn', Taurus; oror =
'arar', juniper; ...) and from them proposed sound values for 14 EVA signs and
clusters (his Appendix 1, figures 36-37):

  k /k/   y /n/   d /t,d,θ,ð/   r /r/   m /r/ (final)   n /r/   sh /kʰ,x,tʃ/   s /s/
  o /a/   a /ə,u,wa/   in /ir/   iin /ur/   e /o/   ee /oo/

He suggested the language behind it may be Near Eastern / Indo-Iranian.

A sound-value key that is right should keep working on words it wasn't built
from. Test: transliterate every VMS word that uses only these signs, reduce it
to a consonant skeleton (vowels are the least certain part of his key), and
count how many skeletons are real words in each of ~30 candidate languages.
Then do the same with keys that use exactly Bax's sound values but assigned to
the signs at random. If his assignment is right, it should beat its own
shuffles; if the names were coincidences, it shouldn't.
"""
import pathlib
import random
import re
import sys
import unicodedata
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import _path  # noqa: F401
from _common import save, table, write_md
from voynich import Voynich
from voynich.corpus import wikipedia, historical

HERE = pathlib.Path(__file__).parent
UNITS = ["iin", "in", "sh", "ee", "k", "y", "d", "r", "m", "n", "s", "o", "a", "e"]
CONS_UNITS = ["k", "y", "d", "r", "m", "n", "sh", "s", "in", "iin"]
BAX = {"k": "K", "y": "N", "d": "T", "r": "R", "m": "R", "n": "R", "sh": "X", "s": "S", "in": "R", "iin": "R"}
N_SHUFFLES = 1000

# ---- consonant skeletons for each script ------------------------------------
LATIN_DIGRAPHS = [("sch", "X"), ("tsh", "X"), ("sh", "Š"), ("ch", "X"), ("kh", "X"), ("th", "T"),
                  ("dh", "T"), ("gh", "G"), ("ph", "F"), ("ck", "K"), ("qu", "K")]
LATIN = {"k": "K", "c": "K", "q": "K", "t": "T", "d": "T", "r": "R", "n": "N", "s": "S", "x": "X",
         "ç": "X", "č": "X", "ş": "Š", "š": "Š", "ñ": "N", "ŧ": "T", "ţ": "T", "ț": "T", "ș": "S",
         "đ": "T", "ð": "T", "þ": "T", "ř": "R", "ň": "N", "ď": "T", "ť": "T", "ķ": "K", "ņ": "N",
         "ŗ": "R", "ś": "S", "ń": "N", "ċ": "X", "ḥ": "X", "ḫ": "X"}
LATIN_VOWELS = set("aeiouyáàâäãåāăąéèêëēėęěíìîïīįıóòôöõøōőúùûüūůűųýÿæœəɛɔ'ʼʻ")
ARABIC = {"ك": "K", "ق": "K", "ک": "K", "ت": "T", "د": "T", "ط": "T", "ض": "T", "ث": "T", "ذ": "T",
          "ر": "R", "ن": "N", "س": "S", "ص": "S", "خ": "X", "ج": "X", "چ": "X", "ح": "X", "ش": "Š",
          "ۆ": "", "ێ": ""}
ARABIC_DROP = set("اوىيیةهءأإآؤئٱے") | {chr(c) for c in range(0x064B, 0x0660)}
HEBREW = {"כ": "K", "ך": "K", "ק": "K", "ת": "T", "ד": "T", "ט": "T", "ר": "R", "נ": "N", "ן": "N",
          "ס": "S", "ח": "X", "ש": "Š"}
HEBREW_DROP = set("אהויע")
GREEK = {"κ": "K", "τ": "T", "δ": "T", "θ": "T", "ρ": "R", "ν": "N", "σ": "S", "ς": "S", "χ": "X"}
GREEK_DROP = set("αεηιουωάέήίόύώϊϋΐΰ")
CYRILLIC = {"к": "K", "қ": "K", "т": "T", "д": "T", "р": "R", "н": "N", "ң": "N", "с": "S", "х": "X",
            "ҳ": "X", "ч": "X", "ҷ": "X", "ш": "Š", "щ": "Š", "һ": "X"}
CYR_DROP = set("аеёиоуыэюяәөүіїєйъьӣӯ")


def skeleton(word):
    w = word.lower()
    if re.search(r"[؀-ۿ]", w):
        return "".join(ARABIC.get(c, "" if c in ARABIC_DROP else c) for c in w)
    if re.search(r"[֐-׿]", w):
        return "".join(HEBREW.get(c, "" if c in HEBREW_DROP else c) for c in w)
    if re.search(r"[Ͱ-Ͽἀ-῿]", w):
        w = "".join(c for c in unicodedata.normalize("NFD", w) if not unicodedata.combining(c))
        return "".join(GREEK.get(c, "" if c in GREEK_DROP else c) for c in w)
    if re.search(r"[Ѐ-ӿ]", w):
        return "".join(CYRILLIC.get(c, "" if c in CYR_DROP else c) for c in w)
    for a, b in LATIN_DIGRAPHS:
        w = w.replace(a, b)
    out = []
    for c in w:
        if c in LATIN:
            out.append(LATIN[c])
        elif c in LATIN_VOWELS or c in "hw":
            continue
        else:
            out.append(c)
    return "".join(out)


LANGS = ["Arabic", "Egyptian Arabic", "Persian", "Urdu", "Pashto", "Kurdish", "Tajik", "Turkish",
         "Azerbaijani", "Uzbek", "Turkmen", "Kazakh", "Tatar", "Crimean Tatar", "Chechen", "Ossetian",
         "Hebrew", "Greek", "Latin", "Italian", "Spanish", "German", "English", "Czech", "Croatian",
         "Albanian", "Romanian", "Romani", "Hungarian"]
lex = {}
for lang in LANGS:
    words = wikipedia(lang, 300000)
    c = Counter(skeleton(w) for w in words)
    lex[lang] = {s for s, n in c.items() if n >= 2 and s}
lex["Latin (Aix, medieval)"] = {s for s, n in Counter(skeleton(w) for w in historical("Latin_Aix")).items() if n >= 2 and s}


# ---- VMS words under a key --------------------------------------------------
def units(word):
    out, i = [], 0
    while i < len(word):
        for u in UNITS:
            if word.startswith(u, i):
                out.append(u)
                i += len(u)
                break
        else:
            return None
    return out


v = Voynich("ZL")
tokens = [w for l in v.lines for w in l.words]
keyed = [(w, units(w)) for w in tokens]
keyed = [(w, u) for w, u in keyed if u]
coverage = len(keyed) / len(tokens)


def skel_of(u, key):
    return "".join(key[x] for x in u if x in key)


def keyed_units(words):
    out = [units(w) for w in words]
    return [u for u in out if u]


def score(ks, key, min_len, types=False):
    sk = [skel_of(u, key) for u in ks]
    sk = [s for s in sk if len(s) >= min_len]
    if types:
        sk = list(set(sk))
    res = {lang: sum(s in L for s in sk) / len(sk) for lang, L in lex.items()}
    return res, len(sk)


def test(ks, min_len, types, shuffles=N_SHUFFLES, seed=0):
    rng = random.Random(seed)
    values = [BAX[u] for u in CONS_UNITS]
    bax, n = score(ks, BAX, min_len, types)
    null = {lang: [] for lang in lex}
    best_null = []
    for _ in range(shuffles):
        vals = values[:]
        rng.shuffle(vals)
        r, _ = score(ks, dict(zip(CONS_UNITS, vals)), min_len, types)
        for lang in lex:
            null[lang].append(r[lang])
        best_null.append(max(r.values()))
    rows = []
    for lang in lex:
        nl = null[lang]
        rows.append({"language": lang, "lexicon": len(lex[lang]), "bax": bax[lang],
                     "shuffled_mean": sum(nl) / len(nl),
                     "p": (1 + sum(x >= bax[lang] for x in nl)) / (1 + len(nl)),
                     "rank_of_bax": 1 + sum(x > bax[lang] for x in nl)})
    rows.sort(key=lambda r: r["p"])
    best = max(bax.values())
    n_sig = sum(r["p"] <= 0.05 for r in rows)
    return {"items": n, "rows": rows, "best_bax": best, "n_langs_p05": n_sig,
            "p_best": (1 + sum(x >= best for x in best_null)) / (1 + shuffles)}


from voynich.autocopy import AutoCopy
from voynich.corpus import DATA
texts = {"VMS (ZL, all)": tokens,
         "self-citation generator (no meaning)": [w for l in AutoCopy(seed=1).run(4500) for w in l]}
src = DATA / "external" / "naibbe-cipher" / "encrypted" / "nathist_output_ciphertext.txt"
if src.exists():
    texts["Naibbe cipher of Pliny (Latin)"] = open(src, encoding="utf-8-sig").read().split()[:len(tokens)]

results, summary = {}, []
for name, words in texts.items():
    ks = keyed_units(words)
    for min_len in (2, 3):
        for types in (False, True):
            r = test(ks, min_len, types)
            results[f"{name} | {min_len}+ | {'types' if types else 'tokens'}"] = r
            summary.append({"text": name, "consonants": f"{min_len}+", "count": "types" if types else "tokens",
                            "items": r["items"], "langs_p<=0.05": f"{r['n_langs_p05']}/{len(lex)}",
                            "top3": ", ".join(f"{x['language']} {x['p']:.3f}" for x in r["rows"][:3]),
                            "p_best_language": r["p_best"]})
            print(summary[-1])
keyed = [(None, u) for u in keyed_units(tokens)]

# his own words under his own key
named = {"kydainy (f2r, 'kantairon')": "kydainy", "koaiin (f3v, 'kaur')": "koaiin",
         "oror (f16r, 'arar')": "oror", "dary (f68r1.6, 'taurn'; Bax saw doary)": "dary"}
own = [{"word": k, "skeleton": skel_of(units(w), BAX), "in_text": Counter(tokens)[w]} for k, w in named.items()]
top = Counter(skel_of(u, BAX) for _, u in keyed).most_common(15)

save(HERE, "bax", {"coverage": coverage, "summary": summary, "results": results, "own_words": own,
                   "top_skeletons": top, "key": BAX})
md = "# c07 Bax's sound values on the rest of the text\n\n"
md += f"Words written only with Bax's 14 signs: {len(keyed)} of {len(tokens)} tokens ({coverage:.0%}). "
md += "Each is reduced to its consonant skeleton (K N T R X S); lexicon words are reduced the same way, per script.\n\n"
md += "His own words under his key:\n\n" + table(own, ["word", "skeleton", "in_text"])
md += "\nMost common skeletons the key produces: " + ", ".join(f"{s or '∅'} ×{c}" for s, c in top) + "\n"
md += "\n## summary: does Bax's assignment beat its own shuffles?\n\n" + table(
    summary, ["text", "consonants", "count", "items", "langs_p<=0.05", "top3", "p_best_language"])
md += "\n`langs_p<=0.05`: languages (of 30) where Bax's key matches more than 95% of shuffled keys. `p_best_language`: how often a shuffled key's best language matches as well as Bax's best language.\n"
r = results["VMS (ZL, all) | 3+ | types"]
md += f"\n## VMS, distinct skeletons of 3+ consonants ({r['items']}), per language\n\n"
md += table(r["rows"], ["language", "lexicon", "bax", "shuffled_mean", "rank_of_bax", "p"])
md += f"\n`bax`: share of tokens whose skeleton is a word (2+ occurrences) in that language's Wikipedia sample. `shuffled_mean`, `rank_of_bax`, `p`: against {N_SHUFFLES} keys with Bax's sound values given to the 10 consonant signs in random order.\n"
write_md(HERE, "bax", md)
print(md)
