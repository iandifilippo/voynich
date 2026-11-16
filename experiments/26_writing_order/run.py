"""Leaf by leaf, or sheet by sheet?

(Layfield & Davis 2026 argue from page similarity, drawings that run across
conjoint pages and scribal hands that many bifolia were written as separate
units, "singulions". Written that way, the verso of a sheet's first leaf is
followed by the recto of its second leaf. This is a direct test of that
sequence, using carry-over instead of whole-page similarity.)


Exp. 25: in herbal A the end of a page carries over into the start of the next.
That gives a way to ask how the quires were written. A quire is a stack of
folded sheets (bifolia). Each sheet carries two leaves that are far apart in
the bound book. A scribe can either

  write the book in reading order, leaf after leaf (the quire already nested), or
  write one sheet at a time: both leaves of a bifolium, then the next sheet.

After the verso of the first leaf of a sheet, the next text written is then
either the recto of the next folio in the book, or the recto of the conjugate
leaf (the other half of the same sheet). Wherever those two differ, compare
the carry-over: last 5 lines of the verso against the first 5 lines of each
candidate, and against every other recto of the block as a baseline.

Also: the same recto -> verso and verso -> next recto carry-over split by
whether the page break falls inside a quire or between two quires.
"""
import pathlib
import random
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _common import save, table, write_md
from voynich import Voynich

HERE = pathlib.Path(__file__).parent
BOOT = 2000
v = Voynich("ZL")
order = list(v.pages)
BLOCKS = [("herbal A, hand 1", dict(language="A", hand="1", section="H")),
          ("herbal B, hand 2", dict(language="B", hand="2", section="H")),
          ("stars B, hand 3", dict(language="B", hand="3", section="S")),
          ("balneo B, hand 2", dict(language="B", hand="2", section="B")),
          ("pharma A, hand 1", dict(language="A", hand="1", section="P"))]


def folio(p):
    m = re.match(r"f(\d+)([rv])", p)
    return (int(m.group(1)), m.group(2)) if m else None


def analyse(name, sel):
    pages = {}
    for l in v.select(unit="P", **sel):
        if len(l.words) >= 3:
            pages.setdefault(l.page, []).append(set(l.words))
    fl, n = Counter(), 0
    for ls in pages.values():
        for s in ls:
            fl.update(s)
            n += 1
    exp = sum(c * (c - 1) for c in fl.values()) / (n * (n - 1))

    def shared(a, b):
        A, B = pages[a][-5:], pages[b][:5]
        return sum(len(x & y) for x in A for y in B), len(A) * len(B)

    # simple pages only (f12r, f12v; skip foldouts like f67r1)
    simple = {p: folio(p) for p in pages if re.fullmatch(r"f\d+[rv]", p)}
    by_folio = {}
    for p, (num, s) in simple.items():
        by_folio.setdefault(num, {})[s] = p
    sheet = {}
    for num, d in by_folio.items():
        meta = v.pages[next(iter(d.values()))]
        sheet.setdefault((meta.get("Q"), meta.get("B")), []).append(num)
    rectos = [d["r"] for d in by_folio.values() if "r" in d]

    cases = []
    for (q, b), nums in sheet.items():
        nums = sorted(nums)
        if len(nums) != 2:
            continue
        first, second = nums
        if "v" not in by_folio[first] or "r" not in by_folio[second]:
            continue
        nxt = first + 1
        if nxt == second or nxt not in by_folio or "r" not in by_folio[nxt]:
            continue
        if v.pages[by_folio[nxt]["r"]].get("Q") != q:
            continue
        src = by_folio[first]["v"]
        bound, conj = by_folio[nxt]["r"], by_folio[second]["r"]
        others = [r for r in rectos if r not in (bound, conj) and folio(r)[0] != first]
        cases.append({"verso": src, "next in book": bound, "conjugate": conj,
                      "bound": shared(src, bound), "conj": shared(src, conj),
                      "other": tuple(map(sum, zip(*[shared(src, o) for o in others])))})

    rng = random.Random(0)

    def lift(cs, key):
        s = sum(c[key][0] for c in cs)
        m = sum(c[key][1] for c in cs)
        return s / (m * exp) if m else float("nan")

    res = None
    for c in cases:
        c["exp"] = exp
        c["block"] = name
    all_cases.extend(cases)
    if len(cases) >= 6:
        boots = [[rng.choice(cases) for _ in cases] for _ in range(BOOT)]
        diff = sorted(lift(b, "bound") - lift(b, "conj") for b in boots)
        res = {"block": name, "sheets": len(cases), "next folio in the book": lift(cases, "bound"),
               "conjugate leaf": lift(cases, "conj"), "any other recto": lift(cases, "other"),
               "book - conjugate": lift(cases, "bound") - lift(cases, "conj"),
               "ci": f"{diff[int(.025 * BOOT)]:.2f} to {diff[int(.975 * BOOT)]:.2f}",
               "p(book <= conjugate)": sum(d <= 0 for d in diff) / BOOT,
               "p(conjugate > other)": sum(lift(b, "conj") <= lift(b, "other") for b in boots) / BOOT,
               "p(book > other)": sum(lift(b, "bound") <= lift(b, "other") for b in boots) / BOOT}

    # page breaks inside a quire vs between quires
    brk = {"inside a quire": [], "between quires": []}
    for num in sorted(by_folio):
        if "v" in by_folio[num] and num + 1 in by_folio and "r" in by_folio[num + 1]:
            a, b = by_folio[num]["v"], by_folio[num + 1]["r"]
            same_q = v.pages[a].get("Q") == v.pages[b].get("Q")
            brk["inside a quire" if same_q else "between quires"].append(shared(a, b))
    quire = []
    for k, xs in brk.items():
        if xs:
            s, m = map(sum, zip(*xs))
            bs = sorted(sum(x[0] for x in smp) / (sum(x[1] for x in smp) * exp)
                        for smp in ([rng.choice(xs) for _ in xs] for _ in range(BOOT)))
            quire.append({"block": name, "verso -> next recto": k, "breaks": len(xs), "lift": s / (m * exp),
                          "ci": f"{bs[int(.025 * BOOT)]:.2f}-{bs[int(.975 * BOOT)]:.2f}"})
    listing = [{"block": name, "verso": c["verso"], "next in book": c["next in book"], "conjugate": c["conjugate"],
                "shared with next": c["bound"][0], "shared with conjugate": c["conj"][0]} for c in cases]
    return res, quire, listing


all_cases = []
results, quires, listings = [], [], []
for name, sel in BLOCKS:
    r, q, l = analyse(name, sel)
    if r:
        results.append(r)
    quires += q
    listings += l
    print(r)

# all blocks together: each sheet compared within its own block's rates
rng = random.Random(5)


def pooled(cs, key):
    return sum(c[key][0] for c in cs) / sum(c[key][1] * c["exp"] for c in cs)


boots = [[rng.choice(all_cases) for _ in all_cases] for _ in range(BOOT)]
diff = sorted(pooled(b, "bound") - pooled(b, "conj") for b in boots)
wins = sum(c["bound"][0] / c["bound"][1] > c["conj"][0] / c["conj"][1] for c in all_cases)
ties = sum(c["bound"][0] / c["bound"][1] == c["conj"][0] / c["conj"][1] for c in all_cases)
from math import comb
n_eff = len(all_cases) - ties
sign_p = sum(comb(n_eff, k) for k in range(max(wins, n_eff - wins), n_eff + 1)) / 2 ** n_eff * 2 if n_eff else 1.0
pool = {"sheets": len(all_cases), "next folio in the book": pooled(all_cases, "bound"),
        "conjugate leaf": pooled(all_cases, "conj"), "any other recto": pooled(all_cases, "other"),
        "book - conjugate": pooled(all_cases, "bound") - pooled(all_cases, "conj"),
        "ci": f"{diff[int(.025 * BOOT)]:.2f} to {diff[int(.975 * BOOT)]:.2f}",
        "p(book <= conjugate)": sum(d <= 0 for d in diff) / BOOT,
        "sheets where book order wins": f"{wins} of {n_eff}", "sign test p": min(1.0, sign_p)}
print(pool)


def side_of(c):
    a, b = c["bound"][0] / c["bound"][1], c["conj"][0] / c["conj"][1]
    return "book" if a > b else "conjugate" if b > a else "tie"


split = []
tab = {}
for label, test in [("scribe 1 (Currier A)", lambda b: "hand 1" in b), ("scribes 2 and 3 (Currier B)", lambda b: "hand 1" not in b)]:
    cs = [c for c in all_cases if test(c["block"])]
    k = Counter(side_of(c) for c in cs)
    tab[label] = (k["book"], k["conjugate"])
    bs = [[rng.choice(cs) for _ in cs] for _ in range(BOOT)]
    d = sorted(pooled(b, "bound") - pooled(b, "conj") for b in bs)
    split.append({"scribe": label, "sheets": len(cs), "next folio in the book": pooled(cs, "bound"),
                  "conjugate leaf": pooled(cs, "conj"), "any other recto": pooled(cs, "other"),
                  "book wins": k["book"], "conjugate wins": k["conjugate"], "ties": k["tie"],
                  "book - conjugate": pooled(cs, "bound") - pooled(cs, "conj"),
                  "ci": f"{d[int(.025 * BOOT)]:.2f} to {d[int(.975 * BOOT)]:.2f}"})
(a, b), (c, d) = tab.values()
tot = comb(a + b + c + d, a + c)
p_obs = comb(a + b, a) * comb(c + d, c) / tot
fisher = sum(comb(a + b, x) * comb(c + d, a + c - x) / tot for x in range(0, a + b + 1)
             if 0 <= a + c - x <= c + d and comb(a + b, x) * comb(c + d, a + c - x) / tot <= p_obs + 1e-12)
print(split, fisher)

save(HERE, "writing_order", {"pooled": pool, "by_scribe": split, "fisher_p": fisher, "sheet_test": results, "quire_breaks": quires, "cases": listings})
md = "# 26 leaf by leaf or sheet by sheet\n\nLift of shared word types: last 5 lines of the verso of a sheet's first leaf against the first 5 lines of a candidate recto.\n\n"
md += table(results, ["block", "sheets", "next folio in the book", "conjugate leaf", "any other recto",
                      "book - conjugate", "ci", "p(book <= conjugate)", "p(book > other)", "p(conjugate > other)"])
md += "\n## all blocks together (" + ", ".join(sorted({l["block"] for l in listings})) + ")\n\n" + table(
    [pool], ["sheets", "next folio in the book", "conjugate leaf", "any other recto", "book - conjugate", "ci",
             "p(book <= conjugate)", "sheets where book order wins", "sign test p"])
md += "\n## by scribe\n\n" + table(split, ["scribe", "sheets", "next folio in the book", "conjugate leaf", "any other recto",
                                            "book wins", "conjugate wins", "ties", "book - conjugate", "ci"])
md += f"\nFisher exact test on wins (book / conjugate) between the two groups: p = {fisher:.3f}\n"
md += "\n## page breaks inside and between quires\n\n" + table(quires, ["block", "verso -> next recto", "breaks", "lift", "ci"])
md += "\n## the sheets used\n\n" + table(
    listings,
    ["block", "verso", "next in book", "conjugate", "shared with next", "shared with conjugate"])
write_md(HERE, "writing_order", md)
print(md)
