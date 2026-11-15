import re

SECTIONS = {
    "H": "herbal", "A": "astronomical", "B": "biological",
    "C": "cosmological", "P": "pharmaceutical", "S": "stars_recipes",
    "Z": "zodiac", "T": "text",
}

LINE_RE = re.compile(r"^<([^>]+)>\s*(.*)$")
META_RE = re.compile(r"\$(\w)=(\w+)")


def clean(text):
    start = "<%>" in text
    end = "<$>" in text
    s = re.sub(r"\{[^}]*\}", "", text)
    s = re.sub(r"\[([^:\]]*)[^\]]*\]", r"\1", s)  # keep first alt reading
    s = re.sub(r"@\d+;?", "?", s)
    s = re.sub(r"<[^>]*>", ".", s)
    s = s.replace(",", ".").replace("*", "?")
    s = re.sub(r"[!%$\"+']", "", s)
    words = [w for w in re.split(r"\.+", s) if w and "?" not in w]
    return words, start, end


def load(path):
    pages, lines = {}, []
    with open(path, encoding="utf-8", errors="replace") as f:
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
            ltype = re.sub(r"^[+@=&~*]", "", parts[1])[:1] if len(parts) > 1 else ""
            page = locus.split(".")[0]
            meta = pages.get(page, {})
            words, start, end = clean(rest)
            lines.append({
                "page": page, "locus": locus, "type": ltype, "words": words,
                "para_start": start, "para_end": end,
                "section": meta.get("I"), "language": meta.get("L"), "hand": meta.get("H"),
            })
    return lines, pages
