import pathlib
import urllib.request

URL = "https://www.voynich.nu/data/ZL3b-n.txt"
DEST = pathlib.Path(__file__).resolve().parent.parent / "data" / "ZL3b-n.txt"

DEST.parent.mkdir(exist_ok=True)
urllib.request.urlretrieve(URL, DEST)
print(DEST, DEST.stat().st_size)
