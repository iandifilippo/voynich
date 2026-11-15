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
