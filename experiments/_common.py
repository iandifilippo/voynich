import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def save(exp_dir, name, obj):
    out = pathlib.Path(exp_dir) / "results"
    out.mkdir(exist_ok=True)
    (out / f"{name}.json").write_text(json.dumps(obj, indent=1, ensure_ascii=False))


def table(rows, cols, fmt=None):
    fmt = fmt or {}
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    body = ""
    for r in rows:
        cells = []
        for c in cols:
            v = r.get(c, "")
            if isinstance(v, float):
                v = format(v, fmt.get(c, ".3f"))
            cells.append(str(v))
        body += "| " + " | ".join(cells) + " |\n"
    return head + body


def write_md(exp_dir, name, text):
    out = pathlib.Path(exp_dir) / "results"
    out.mkdir(exist_ok=True)
    (out / f"{name}.md").write_text(text)
