"""Which page follows which, sheet by sheet.

Exp. 26 compared two candidates for what was written after the verso of a
sheet's first leaf. A sheet has four pages (leaf a: recto, verso; leaf b:
recto, verso, with b later in the book) and there are three ways to write it:

  book order (quire nested first)   a_r a_v | next folio ... | b_r b_v
  folded singly                     a_r a_v b_r b_v
  laid flat, a side at a time       a_v b_r (inside)  then  b_v a_r (outside), or the reverse

They predict different carry-overs:

  transition               book   folded   flat
  recto -> own verso        yes    yes      no
  a_v -> b_r (conjoint)     no     yes      yes
  b_v -> a_r (outside)      no     no       yes
  a_v -> next folio recto   yes    no       no
  previous verso -> b_r     yes    no       no

Carry-over = shared word types between the last K lines of one page and the
first K lines of the other, over the number expected in that scribe's block.
Sheets where the conjoint leaf *is* the next folio (the middle of a quire) are
kept apart: there every hypothesis says yes. Robustness: K = 4, 6, 8, and
with the 60 commonest words left out. Intervals by resampling sheets.
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
BLOCKS = [("scribe 1", "herbal A", dict(language="A", hand="1", section="H")),
          ("scribe 1", "pharma A", dict(language="A", hand="1", section="P")),
          ("scribes 2, 3", "herbal B", dict(language="B", hand="2", section="H")),
          ("scribes 2, 3", "balneo B", dict(language="B", hand="2", section="B")),
          ("scribes 2, 3", "stars B", dict(language="B", hand="3", section="S"))]
KINDS = ["recto -> own verso", "a_v -> b_r (conjoint)", "b_v -> a_r (outside of sheet)",
         "a_v -> next folio recto", "previous verso -> b_r", "middle of quire: a_v -> b_r",
         "unrelated verso -> recto"]


def collect(K, rare):
    """per sheet: {kind: [shared, expected]}"""
    sheets = []
    for group, block, sel in BLOCKS:
        pages = {}
        for l in v.select(unit="P", **sel):
            if len(l.words) >= 3:
                pages.setdefault(l.page, []).append(set(l.words))
        pages = {p: ls for p, ls in pages.items() if re.fullmatch(r"f\d+[rv]", p)}
        fl, n = Counter(), 0
        for ls in pages.values():
            for s in ls:
                fl.update(s)
                n += 1
        if rare:
            common = {w for w, _ in fl.most_common(60)}
            pages = {p: [s - common for s in ls] for p, ls in pages.items()}
            for w in common:
                del fl[w]
        exp = sum(c * (c - 1) for c in fl.values()) / (n * (n - 1))

        def pair(a, b):
            if a not in pages or b not in pages:
                return None
            A, B = pages[a][-K:], pages[b][:K]
            return [sum(len(x & y) for x in A for y in B), len(A) * len(B) * exp]

        folios = sorted({int(p[1:-1]) for p in pages})
        by_sheet = {}
        for f in folios:
            m = v.pages.get(f"f{f}r") or v.pages.get(f"f{f}v")
            by_sheet.setdefault((m.get("Q"), m.get("B")), []).append(f)
        rectos = [p for p in pages if p.endswith("r")]
        rng = random.Random(len(sheets) + K)
        for (q, bnum), fs in by_sheet.items():
            if len(fs) != 2:
                continue
            a, b = sorted(fs)
            rec = {"group": group, "block": block, "sheet": f"f{a}|f{b}"}
            t = {}
            own = [pair(f"f{x}r", f"f{x}v") for x in (a, b)]
            own = [o for o in own if o]
            if own:
                t["recto -> own verso"] = [sum(o[0] for o in own), sum(o[1] for o in own)]
            middle = b == a + 1
            c = pair(f"f{a}v", f"f{b}r")
            if c:
                t["middle of quire: a_v -> b_r" if middle else "a_v -> b_r (conjoint)"] = c
            o = pair(f"f{b}v", f"f{a}r")
            if o:
                t["b_v -> a_r (outside of sheet)"] = o
            if not middle:
                same_q = lambda f: (v.pages.get(f"f{f}r") or v.pages.get(f"f{f}v") or {}).get("Q") == q
                if same_q(a + 1):
                    x = pair(f"f{a}v", f"f{a + 1}r")
                    if x:
                        t["a_v -> next folio recto"] = x
                if same_q(b - 1):
                    x = pair(f"f{b - 1}v", f"f{b}r")
                    if x:
                        t["previous verso -> b_r"] = x
            # baseline: this sheet's versos against rectos far away in the block
            base = [0, 0.0]
            for src in (f"f{a}v", f"f{b}v"):
                far = [r for r in rectos if abs(int(r[1:-1]) - int(src[1:-1])) > 2 and int(r[1:-1]) not in (a, b)]
                for r in rng.sample(far, min(12, len(far))):
                    x = pair(src, r)
                    if x:
                        base[0] += x[0]
                        base[1] += x[1]
            if base[1]:
                t["unrelated verso -> recto"] = base
            rec["t"] = t
            sheets.append(rec)
    return sheets


def summarise(sheets, group):
    cs = [s for s in sheets if s["group"] == group]
    rng = random.Random(1)
    rows = []
    for kind in KINDS:
        have = [s for s in cs if kind in s["t"]]
        if not have:
            continue
        lift = lambda xs: sum(s["t"][kind][0] for s in xs) / sum(s["t"][kind][1] for s in xs)
        bs = sorted(lift([rng.choice(have) for _ in have]) for _ in range(BOOT))
        rows.append({"scribe": group, "transition": kind, "sheets": len(have), "lift": lift(have),
                     "ci": f"{bs[int(.025 * BOOT)]:.2f}-{bs[int(.975 * BOOT)]:.2f}"})
    # paired contrasts on sheets that have both
    def contrast(k1, k2):
        have = [s for s in cs if k1 in s["t"] and k2 in s["t"]]
        if len(have) < 4:
            return None
        d = lambda xs: (sum(s["t"][k1][0] for s in xs) / sum(s["t"][k1][1] for s in xs)
                        - sum(s["t"][k2][0] for s in xs) / sum(s["t"][k2][1] for s in xs))
        bs = sorted(d([rng.choice(have) for _ in have]) for _ in range(BOOT))
        return {"scribe": group, "contrast": f"{k1}  minus  {k2}", "sheets": len(have), "difference": d(have),
                "ci": f"{bs[int(.025 * BOOT)]:.2f} to {bs[int(.975 * BOOT)]:.2f}",
                "p(diff <= 0)": sum(x <= 0 for x in bs) / BOOT}
    cons = [contrast("a_v -> b_r (conjoint)", "a_v -> next folio recto"),
            contrast("a_v -> b_r (conjoint)", "previous verso -> b_r"),
            contrast("a_v -> b_r (conjoint)", "unrelated verso -> recto"),
            contrast("a_v -> next folio recto", "unrelated verso -> recto"),
            contrast("b_v -> a_r (outside of sheet)", "unrelated verso -> recto"),
            contrast("recto -> own verso", "unrelated verso -> recto")]
    return rows, [c for c in cons if c]


ASYM = []


def matrix(K=6):
    """every ordered pair among the four pages of a sheet, by block"""
    labels = ["a_r", "a_v", "b_r", "b_v"]
    rows = []
    for group, block, sel in BLOCKS:
        pages = {}
        for l in v.select(unit="P", **sel):
            if len(l.words) >= 3:
                pages.setdefault(l.page, []).append(set(l.words))
        pages = {p: ls for p, ls in pages.items() if re.fullmatch(r"f\d+[rv]", p)}
        fl, n = Counter(), 0
        for ls in pages.values():
            for x in ls:
                fl.update(x)
                n += 1
        exp = sum(c * (c - 1) for c in fl.values()) / (n * (n - 1))
        by_sheet = {}
        for f in sorted({int(p[1:-1]) for p in pages}):
            m = v.pages.get(f"f{f}r") or v.pages.get(f"f{f}v")
            by_sheet.setdefault((m.get("Q"), m.get("B")), []).append(f)
        tot, per_sheet = {}, []
        for fs in by_sheet.values():
            if len(fs) != 2 or fs[1] == fs[0] + 1:
                continue
            a, b = sorted(fs)
            pg = [f"f{a}r", f"f{a}v", f"f{b}r", f"f{b}v"]
            mine = {}
            for i in range(4):
                for j in range(4):
                    if i != j and pg[i] in pages and pg[j] in pages:
                        A, B = pages[pg[i]][-K:], pages[pg[j]][:K]
                        sh, ex = sum(len(x & y) for x in A for y in B), len(A) * len(B) * exp
                        t = tot.setdefault((i, j), [0, 0.0, 0])
                        t[0] += sh
                        t[1] += ex
                        t[2] += 1
                        mine[i, j] = (sh, ex)
            per_sheet.append(mine)
        # across the two leaves: leaf a -> leaf b against leaf b -> leaf a
        fwd, back = [(0, 2), (0, 3), (1, 2), (1, 3)], [(2, 0), (2, 1), (3, 0), (3, 1)]
        full = [m for m in per_sheet if all(k in m for k in fwd + back)]
        if len(full) >= 4:
            def lifts(ms):
                f = sum(m[k][0] for m in ms for k in fwd) / sum(m[k][1] for m in ms for k in fwd)
                bk = sum(m[k][0] for m in ms for k in back) / sum(m[k][1] for m in ms for k in back)
                return f, bk
            rng = random.Random(2)
            f, bk = lifts(full)
            bs = sorted(x - y for x, y in (lifts([rng.choice(full) for _ in full]) for _ in range(BOOT)))
            ASYM.append({"block": block, "sheets": len(full), "leaf a -> leaf b": f, "leaf b -> leaf a": bk,
                         "difference": f - bk, "ci": f"{bs[int(.025 * BOOT)]:.2f} to {bs[int(.975 * BOOT)]:.2f}",
                         "p(diff <= 0)": sum(x <= 0 for x in bs) / BOOT,
                         "sheets with a->b higher": sum(lifts([m])[0] > lifts([m])[1] for m in full)})
        if not tot or max(t[2] for t in tot.values()) < 4:
            continue
        for i in range(4):
            r = {"block": block, "sheets": max(t[2] for t in tot.values()), "end of": labels[i]}
            for j in range(4):
                r["start of " + labels[j]] = tot[i, j][0] / tot[i, j][1] if (i, j) in tot else None
            rows.append(r)
    return rows


out = {}
md = "# 29 sheet geometry\n\nLift of shared word types, end of one page against start of another.\n"
main_rows, main_cons = [], []
for K, rare in [(5, False), (4, False), (6, False), (8, False), (5, True), (8, True)]:
    sheets = collect(K, rare)
    label = f"K = {K}, {'without the 60 commonest words' if rare else 'all words'}"
    rows, cons = [], []
    for g in ("scribe 1", "scribes 2, 3"):
        r, c = summarise(sheets, g)
        rows += r
        cons += c
    out[label] = {"transitions": rows, "contrasts": cons}
    if K == 5 and not rare:
        md += f"\n## {label}\n\n" + table(rows, ["scribe", "transition", "sheets", "lift", "ci"])
        md += "\n" + table(cons, ["scribe", "contrast", "sheets", "difference", "ci", "p(diff <= 0)"])
        listing = [{"scribe": s["group"], "block": s["block"], "sheet": s["sheet"],
                    **{k: (f"{s['t'][k][0]}" if k in s["t"] else "") for k in KINDS[:6]}} for s in sheets]
    for c in cons:
        main_cons.append({"setting": label, **c})
key = [c for c in main_cons if c["contrast"].startswith("a_v -> b_r (conjoint)  minus  a_v -> next") or
       c["contrast"].startswith("a_v -> b_r (conjoint)  minus  previous")]
md += "\n## the two deciding contrasts under every setting\n\n" + table(
    key, ["setting", "scribe", "contrast", "sheets", "difference", "ci", "p(diff <= 0)"])
mat = matrix()
out["matrix"] = mat

# the same two tests on other people's transliterations
replication = []
zl_asym = list(ASYM)
for name, label in [("IT", "Takahashi"), ("GC", "Glen Claston (v101)"), ("FG", "First Study Group (Friedman)")]:
    v = Voynich(name)
    del ASYM[:]
    matrix()
    sheets = collect(5, False)
    _, cons = summarise(sheets, "scribes 2, 3")
    c = next((x for x in cons if x["contrast"].startswith("a_v -> b_r (conjoint)  minus  a_v -> next")), None)
    d = {a["block"]: a for a in ASYM}
    replication.append({"transliteration": label,
                        "conjoint - next folio (scribes 2, 3)": c["difference"] if c else None,
                        "ci": c["ci"] if c else None, "p": c["p(diff <= 0)"] if c else None,
                        "stars: a->b": d.get("stars B", {}).get("leaf a -> leaf b"),
                        "stars: b->a": d.get("stars B", {}).get("leaf b -> leaf a"),
                        "stars p": d.get("stars B", {}).get("p(diff <= 0)"),
                        "herbal A: a->b": d.get("herbal A", {}).get("leaf a -> leaf b"),
                        "herbal A: b->a": d.get("herbal A", {}).get("leaf b -> leaf a")})
    print(replication[-1])
v = Voynich("ZL")
ASYM[:] = zl_asym
out["replication"] = replication
md += "\n## every pair of pages within a sheet, by block (K = 6, sheets not in the middle of a quire)\n\nLeaf a comes before leaf b in the book. Rows: where the text stops; columns: where it starts.\n\n"
md += table(mat, ["block", "sheets", "end of", "start of a_r", "start of a_v", "start of b_r", "start of b_v"])
out["direction"] = ASYM
md += "\n## direction across the two leaves of a sheet\n\nEnd of a page on the earlier leaf against start of a page on the later leaf (4 pairs), and the reverse. A sheet written as a unit, first leaf first, gives a -> b higher; leaves written many folios apart give no difference.\n\n"
md += table(ASYM, ["block", "sheets", "leaf a -> leaf b", "leaf b -> leaf a", "difference", "ci", "p(diff <= 0)", "sheets with a->b higher"])
md += "\n## other transliterations\n\n" + table(
    replication, ["transliteration", "conjoint - next folio (scribes 2, 3)", "ci", "p", "stars: a->b", "stars: b->a",
                  "stars p", "herbal A: a->b", "herbal A: b->a"])
md += "\n## shared word types per sheet (K = 5, all words)\n\n" + table(listing, ["scribe", "block", "sheet"] + KINDS[:6])
save(HERE, "sheet_geometry", out)
write_md(HERE, "sheet_geometry", md)
print(md)
