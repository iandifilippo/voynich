"""Loading the manuscript and comparison texts."""
import pathlib
import re

from .ivtff import parse, SECTIONS

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

TRANSCRIPTIONS = {
    "ZL": "ZL3b-n.txt",    # Zandbergen-Landini, EVA (reference)
    "IT": "IT2a-n.txt",    # Takahashi, EVA
    "RF": "RF1b-e.txt",    # Reference transliteration, extended EVA
    "VT": "VT0e-n.txt",    # see voynich.nu/transcr.html
    "GC": "GC2a-n.txt",    # Glen Claston v101 alphabet
    "CD": "CD2a-n.txt",    # Currier / D'Imperio alphabet
    "FG": "FG2a-n.txt",    # Friedman group (FSG) alphabet
}


class Voynich:
    def __init__(self, name="ZL", keep_uncertain=False, commas="split"):
        self.name = name
        self.lines, self.pages = parse(DATA / TRANSCRIPTIONS[name], keep_uncertain, commas)

    def select(self, section=None, language=None, hand=None, unit=None, pages=None):
        out = []
        for l in self.lines:
            if section and l.section not in section:
                continue
            if language and l.language != language:
                continue
            if hand and l.hand != hand:
                continue
            if unit and l.unit not in unit:
                continue
            if pages and l.page not in pages:
                continue
            out.append(l)
        return out

    def words(self, **kw):
        return [w for l in self.select(**kw) for w in l.words]

    def text_lines(self, **kw):
        return [l.words for l in self.select(**kw) if l.words]

    @staticmethod
    def section_name(code):
        return SECTIONS.get(code, code)


def plain_text(path, max_words=None):
    """Normalize a plain text: lowercase letters only, single spaces."""
    with open(path, encoding="utf-8", errors="ignore") as f:
        t = f.read(max_words * 15 if max_words else -1).lower()
    t = re.sub(r"[^\w\s]|[\d_]", " ", t)
    words = t.split()
    if max_words:
        words = words[:max_words]
    return words


def historical(name, max_words=None):
    return plain_text(DATA / "corpora" / "historical" / name, max_words)


def wikipedia(lang, max_words=None):
    return plain_text(DATA / "corpora" / "wikipedia" / lang, max_words)


def list_historical():
    d = DATA / "corpora" / "historical"
    return sorted(p.name for p in d.iterdir() if p.is_file()) if d.exists() else []


def list_wikipedia():
    d = DATA / "corpora" / "wikipedia"
    return sorted(p.name for p in d.iterdir() if p.is_file()) if d.exists() else []


def chunk_lines(words, per_line=9):
    """Split a flat word list into pseudo-lines (Voynich paragraph lines average ~9 words)."""
    return [words[i:i + per_line] for i in range(0, len(words), per_line)]
