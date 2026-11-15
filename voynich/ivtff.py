"""IVTFF transliteration files (voynich.nu format)."""
import re
from dataclasses import dataclass, field

LINE_RE = re.compile(r"^<([^>]+)>\s*(.*)$")
META_RE = re.compile(r"\$(\w)=(\w+)")

SECTIONS = {
    "H": "herbal", "A": "astronomical", "B": "biological", "C": "cosmological",
    "P": "pharmaceutical", "S": "stars", "Z": "zodiac", "T": "text",
}


@dataclass
class Line:
    page: str
    locus: str
    unit: str            # P paragraph, L label, C circular, R radial
    words: list
    uncertain: int       # words dropped because they had ? or unreadable glyphs
    para_start: bool
    para_end: bool
    meta: dict = field(default_factory=dict)

    @property
    def section(self):
        return self.meta.get("I")

    @property
    def language(self):
        return self.meta.get("L")

    @property
    def hand(self):
        return self.meta.get("H")

    @property
    def quire(self):
        return self.meta.get("Q")


def clean(text, keep_uncertain=False):
    start = "<%>" in text
    end = "<$>" in text
    s = re.sub(r"<![^>]*>", "", text)               # comments
    s = re.sub(r"\[([^:\]]*)[^\]]*\]", r"\1", s)    # [a:b] -> a
    s = re.sub(r"\{([^}]*)\}", r"\1", s)            # {ckh} ligatures -> plain glyphs
    s = re.sub(r"@\d+;?", "?", s)                   # rare glyphs
    s = re.sub(r"<[^>]*>", ".", s)                  # <%> <$> <-> etc
    s = s.replace(",", ".").replace("*", "?").replace("'", "")
    s = re.sub(r"[!%$\"+]", "", s)
    raw = [w for w in re.split(r"\.+", s) if w.strip()]
    words = [w for w in raw if keep_uncertain or "?" not in w]
    return words, len(raw) - len(words), start, end


def parse(path, keep_uncertain=False):
    pages, lines = {}, []
    with open(path, encoding="latin-1") as f:
        for raw in f:
            raw = raw.rstrip("\n")
            if not raw.strip() or raw.startswith("#"):
                continue
            m = LINE_RE.match(raw)
            if not m:
                continue
            loc, rest = m.groups()
            if "." not in loc:
                pages[loc] = dict(META_RE.findall(rest))
                continue
            parts = loc.split(",")
            locus = parts[0]
            unit = re.sub(r"^[+@=&~*]", "", parts[1])[:1] if len(parts) > 1 else ""
            page = locus.split(".")[0]
            words, unc, start, end = clean(rest, keep_uncertain)
            lines.append(Line(page, locus, unit, words, unc, start, end, pages.get(page, {})))
    return lines, pages
