"""What kind of plaintext could still hide in the forks?

Exp. 54 found no message carried in the fork choices, with ciphers of full
Latin text as calibration. Its power comes from the plaintext's redundancy.
A writer abbreviating heavily, or enciphering numbers, would leave less to
find. How much less?

Same channel and test as exp. 54 (2 bits per word in the start class, held-
out gain from looking further than one word back), with plaintexts:
  Latin, full letters;
  Latin without vowels (a consonant skeleton);
  Latin cut to the first three letters of each word;
  Latin word initials only;
  numbers: the digits of the word lengths of the Latin text (a table of
    small numbers, real but low in redundancy);
  random digits.
Each plaintext alphabet is coded in the fewest bits that hold it.
"""
import math
import pathlib
import random
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "54_fork_bits"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import run as r54  # noqa: E402
from _common import save, table, write_md  # noqa: E402
from voynich.corpus import historical  # noqa: E402

HERE = pathlib.Path(__file__).parent
words = [w for w in (r54.re.sub(r"[^a-z]", "", x.lower()) for x in historical("Secreta_Secretorum_LAT")) if w]
rng = random.Random(0)
PLAINS = {
    "Latin, full letters": "".join(words),
    "Latin, no vowels": "".join(c for c in "".join(words) if c not in "aeiouy"),
    "Latin, first 3 letters of each word": "".join(w[:3] for w in words),
    "Latin, word initials": "".join(w[0] for w in words),
    "numbers: word lengths of the Latin": "".join(str(min(len(w), 9)) for w in words),
    "random digits": "".join(str(rng.randrange(10)) for _ in range(60000)),
}


def cipher_of(text, template, rng, machine):
    alpha = sorted(set(text))
    nb = max(1, math.ceil(math.log2(len(alpha))))
    code = {c: format(i, f"0{nb}b") for i, c in enumerate(alpha)}
    stream = "".join(code[c] for c in text)
    pools = defaultdict(list)
    for _ in range(60000):
        w = machine.word(rng, "middle", "#")
        pools[(r54.start_cls(w), r54.end_cls(w))].append(w)
    pos, out = 0, []
    for s in template:
        out.append([])
        for l in s:
            line = []
            for _ in l:
                sc = int(stream[pos:pos + 2], 2)
                pos += 2
                ec = rng.choices(range(4), [len(pools[(sc, e)]) for e in range(4)])[0]
                line.append(rng.choice(pools[(sc, ec)]))
            out[-1].append(line)
    return out, nb


rows = []
for name, text in PLAINS.items():
    sheets, nb = cipher_of(text, r54.B, rng, r54.machine)
    r = r54.evaluate(sheets, lambda w: r54.start_cls(w), 4, 10)
    gain = r[1] - min(r[k] for k in range(1, 11))
    rows.append({"plaintext": name, "bits per plaintext symbol": nb,
                 "gain from looking further than 1 back": gain, "best k": min(r, key=r.get)})
    print(rows[-1], flush=True)
rows.append({"plaintext": "Currier B (exp. 54)", "bits per plaintext symbol": "",
             "gain from looking further than 1 back": 0.003, "best k": ""})
save(HERE, "limits", rows)
write_md(HERE, "limits", "# 59 what plaintext could hide in the forks\n\nStart channel, 2 bits per word.\n\n" + table(
    rows, ["plaintext", "bits per plaintext symbol", "gain from looking further than 1 back", "best k"]))
