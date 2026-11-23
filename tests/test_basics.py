import pytest
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from voynich import ciphers, metrics
from voynich.cisiojanus import months, DAYS, syllabify
from voynich.ivtff import clean


def test_clean_alternatives_and_ligatures():
    words, unc, start, end = clean("<%>fachys.ykal.[cth:oto]res.{ckh}y,dan<!@254;>")
    assert words == ["fachys", "ykal", "cthres", "ckhy", "dan"]
    assert start and not end


def test_clean_drops_uncertain():
    words, unc, _, _ = clean("dain.oto@192;aiin.ch*y.ol")
    assert words == ["dain", "ol"]
    assert unc == 2


def test_clean_commas():
    text = "qo,kedy.ch,ol,dy"
    assert clean(text)[0] == ["qo", "kedy", "ch", "ol", "dy"]
    assert clean(text, commas="join")[0] == ["qokedy", "choldy"]
    vocab = {"qokedy": 5, "chol": 3}
    assert clean(text, commas="smart", vocab=vocab)[0] == ["qokedy", "chol", "dy"]


def test_cisiojanus_has_one_syllable_per_day():
    m = months()
    assert [len(m[i]) for i in range(1, 13)] == DAYS


def test_syllabify():
    assert syllabify("cisio") == ["ci", "si", "o"]
    assert syllabify("quin") == ["quin"]


def test_entropy_of_repeated_text_is_low():
    _, h1, h2 = metrics.char_entropies(["ab"] * 200)
    assert h2 < 0.1


def test_ciphers_run():
    pt = "in principio erat verbum et verbum erat apud deum".split() * 50
    for f in ciphers.METHODS.values():
        out = f(pt, seed=1)
        assert out and all(isinstance(w, str) and w for w in out)
    assert len(ciphers.self_citation(500)) > 10


def test_profile_keys():
    lines = [["daiin", "ol", "chedy"], ["qokedy", "shedy", "ol", "dar"]] * 50
    p = metrics.profile(lines)
    for k in ("h2", "edge_coupling", "line_first_jsd", "line_cohesion", "hapax_ratio"):
        assert k in p


def test_naibbe_autokey_adds_coupling():
    import pytest
    from voynich import naibbe
    if not (naibbe.ROOT / "references" / "naibbe_tables.csv").exists():
        pytest.skip("naibbe-cipher repo not downloaded")
    units = naibbe.load_units("nathist")[:300]
    plain = [w for l in naibbe.Naibbe(seed=1).encrypt(units) for w in l]
    auto = [w for l in naibbe.Naibbe(seed=1, table_rule="autokey", autokey_p=1.0).encrypt(units) for w in l]
    lines = lambda ws: [ws[i:i + 9] for i in range(0, len(ws), 9)]
    assert metrics.edge_coupling(lines(auto)) > metrics.edge_coupling(lines(plain)) + 0.1


def test_autocopy_runs_and_is_deterministic():
    from voynich.autocopy import AutoCopy, tokens
    assert tokens("qokeedy") == ["qo", "k", "ee", "dy"]
    a = AutoCopy(seed=3).run(60)
    b = AutoCopy(seed=3).run(60)
    assert a == b and len(a) == 60 and all(l for l in a)


def test_autocopy_options_run():
    from voynich.autocopy import AutoCopy
    lines = AutoCopy(seed=2, boundary={"y": {"qo", "o"}}, boundary_p=0.5, line_end_p=0.5,
                     common_p=0.5, global_p=0.1, exact_p=0.1, extra_change=0.1).run(80)
    assert len(lines) == 80 and all(lines)


def test_solver_reads_a_substitution():
    import random
    import shutil
    import pytest
    pytest.importorskip("numpy")
    if not shutil.which("gcc"):
        pytest.skip("no compiler")
    from voynich.crack import LM, LETTERS, Problem, glyph_stream
    rng = random.Random(0)
    words = ["arma", "virumque", "cano", "troiae", "qui", "primus", "ab", "oris", "italiam", "fato", "profugus",
             "laviniaque", "venit", "litora", "multum", "ille", "et", "terris", "iactatus", "alto"]
    text = [[rng.choice(words) for _ in range(9)] for _ in range(250)]
    lm = LM([" ".join(l) for l in text[:150]])
    perm = list(LETTERS)
    rng.shuffle(perm)
    enc = [["".join(perm[LETTERS.index(c)] for c in w) for w in l] for l in text[150:]]
    tok, vocab = glyph_stream(enc, list)
    prob = Problem(tok, len(vocab), list(LETTERS), lm)
    key, _ = prob.solve(iters=40000, restarts=2)
    assert prob.decode(key, limit=20).split()[0] in words


def test_ranked_cuts():
    from collections import Counter
    from voynich.crack import segment
    words = ["ol"] * 50 + ["or"] * 40 + ["shaiin", "shedy", "qoaiin", "qoedy", "ytaiin", "ytedy"] * 3
    seg = segment.fit_ranked(Counter(words), 2)
    assert seg["ol"] == ("ol",) and seg["shaiin"] == ("sh", "aiin") and seg["qoedy"] == ("qo", "edy")


def test_assembler_fills_shape():
    from voynich.assemble import Assembler, signs
    lines = [["qokedy", "chedy", "daiin"], ["shedy", "qokaiin", "ol", "chedy"]] * 20
    m = Assembler(order=2).fit(lines, para_starts=[0])
    out = m.fill([(3, True), (4, False)], seed=1)
    assert [len(l) for l in out] == [3, 4]
    assert all(w and "".join(signs(w)) == w for l in out for w in l)


def test_hmm_sample_words():
    np = pytest.importorskip("numpy")
    from voynich.crack.hmm import sample_words
    A = np.array([[0.0, 1.0], [1.0, 0.0]])
    B = np.array([[1.0, 0.0], [0.0, 1.0]])
    words = sample_words(A, np.array([1.0, 0.0]), B, ["a", "$"], 5, np.random.default_rng(0))
    assert words == [["a"]] * 5


def test_fork_profile():
    pytest.importorskip("numpy")
    from voynich.forks import FEATS, profile
    p = profile(["qokedy", "chol", "daiin"])
    assert len(p) == len(FEATS)
    assert abs(p.sum() - 3.0) < 1e-9
    assert p[FEATS.index(("start", "qo"))] == 1 / 3 and p[FEATS.index(("end", "aiin"))] == 1 / 3


def test_exchange_classes_recover_alphabet():
    pytest.importorskip("numpy")
    import random
    from voynich.crack.classes import fit
    rng = random.Random(0)
    homophones = {"a": ["x1", "x2", "x3"], "b": ["y1", "y2"]}
    plain = "ab" * 400
    lines = [[rng.choice(homophones[c]) for c in plain[i:i + 20]] for i in range(0, len(plain), 20)]
    mi, cls = fit(lines, 2)
    assert len({cls["x1"], cls["x2"], cls["x3"]}) == 1 and cls["x1"] != cls["y1"] and cls["y1"] == cls["y2"]
    assert mi > 0.9


def test_assembler_sheet_setting():
    from voynich.assemble import Assembler
    lines = [["qokedy", "chedy", "daiin", "qotedy"], ["shedy", "qokaiin", "ol", "chedy"]] * 30
    m = Assembler(order=2, sheet_sigma=0.5, hold=3.0).fit(lines)
    out = m.fill_sheet([(4, False)] * 5, seed=2)
    assert [len(l) for l in out] == [4] * 5 and m.weights is None and m.line_gallows is None


def test_assembler_follow_copies_runs():
    from voynich.assemble import Assembler
    lines = [["qokedy", "chedy", "daiin", "qotedy"], ["shedy", "qokaiin", "ol", "chedy"]] * 30
    m = Assembler(order=2, follow_p=1.0).fit(lines)
    out = m.fill_sheet([(6, False)] * 8, seed=3)
    pairs = [(a, b) for l in out for a, b in zip(l, l[1:])]
    assert len(set(pairs)) < len(pairs)


def test_assembler_link_two_signs():
    from voynich.assemble import Assembler
    lines = [["chedy", "qokedy", "chol", "daiin"]] * 40
    m = Assembler(order=2, link_signs=2).fit(lines)
    assert any(k[0] == "^dy" for k in m.pooled)
    assert len(m.fill([(4, False)], seed=1)[0]) == 4
