"""python -m voynich.download

Fetches the transliterations from voynich.nu, the comparison corpora from
Lindemann & Bowern's repository, and other people's published code/output we
test in experiments/community. Nothing third-party is stored in git.
"""
import pathlib
import shutil
import subprocess
import tempfile
import urllib.request

from .corpus import DATA, TRANSCRIPTIONS

BASE = "https://www.voynich.nu/data/"
CORPORA_REPO = "https://github.com/chirila/Voynich-public"
EXTERNAL = {
    # Greshko (2025), Cryptologia, doi:10.1080/01611194.2025.2566408 (modified MIT, cite when used)
    "naibbe-cipher": "https://github.com/greshko/naibbe-cipher",
}


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


def external():
    root = DATA / "external"
    root.mkdir(parents=True, exist_ok=True)
    for name, url in EXTERNAL.items():
        if (root / name).exists():
            continue
        print("clone", url)
        subprocess.run(["git", "clone", "--depth", "1", url, str(root / name)], check=True)


if __name__ == "__main__":
    transcriptions()
    corpora()
    external()
    print("done:", DATA)
