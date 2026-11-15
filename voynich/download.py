"""python -m voynich.download

Fetches the transliterations from voynich.nu and the comparison corpora
from Lindemann & Bowern's repository. Nothing third-party is stored in git.
"""
import pathlib
import shutil
import subprocess
import tempfile
import urllib.request

from .corpus import DATA, TRANSCRIPTIONS

BASE = "https://www.voynich.nu/data/"
CORPORA_REPO = "https://github.com/chirila/Voynich-public"


def transcriptions():
    DATA.mkdir(exist_ok=True)
    for name, fn in TRANSCRIPTIONS.items():
        dest = DATA / fn
        if dest.exists():
            continue
        print("get", fn)
        urllib.request.urlretrieve(BASE + fn, dest)


def corpora():
    hist = DATA / "corpora" / "historical"
    wiki = DATA / "corpora" / "wikipedia"
    if hist.exists() and wiki.exists():
        return
    with tempfile.TemporaryDirectory() as tmp:
        print("clone", CORPORA_REPO)
        subprocess.run(["git", "clone", "--depth", "1", CORPORA_REPO, tmp], check=True)
        src = pathlib.Path(tmp) / "Corpora"
        hist.mkdir(parents=True, exist_ok=True)
        wiki.mkdir(parents=True, exist_ok=True)
        for p in (src / "Historical_texts").iterdir():
            if p.is_file() and not p.name.startswith("."):
                shutil.copy(p, hist / p.name)
        for p in (src / "Wikipedia_texts" / "full").iterdir():
            if p.is_file() and not p.name.startswith("."):
                shutil.copy(p, wiki / p.name)


if __name__ == "__main__":
    transcriptions()
    corpora()
    print("done:", DATA)
