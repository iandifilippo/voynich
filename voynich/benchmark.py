"""How Voynich-like is a text?

score() compares a text's profile with the manuscript's on every metric.
Distances are scaled by how much that metric varies across ordinary
historical texts (median absolute deviation), so a metric that is
naturally noisy counts for less.
"""
import json
import pathlib

from . import metrics
from .corpus import Voynich, historical, list_historical, chunk_lines

N_WORDS = 10000
KEYS = ["hapax_ratio", "mattr500", "word_len", "word_len_sd", "h1", "h2", "zipf",
        "edge_coupling", "word_mi", "repeat_rate", "line_first_jsd", "line_last_jsd",
        "line_cohesion"]

CACHE = pathlib.Path(__file__).resolve().parent.parent / "data" / "benchmark_reference.json"


def reference(rebuild=False):
    if CACHE.exists() and not rebuild:
        return json.loads(CACHE.read_text())
    vms = Voynich("ZL")
    target = metrics.profile(vms.text_lines(unit="P"), N_WORDS)
    natural = {}
    for name in list_historical():
        words = historical(name)
        if len(words) >= N_WORDS:
            natural[name] = metrics.profile(chunk_lines(words), N_WORDS)
    scale = {}
    for k in KEYS:
        vals = sorted(p[k] for p in natural.values())
        med = vals[len(vals) // 2]
        mad = sorted(abs(v - med) for v in vals)[len(vals) // 2] * 1.4826
        # floor at 10% of the VMS value so a metric where natural texts all
        # sit near zero can't swamp the others
        scale[k] = max(mad, 0.1 * abs(target[k]), 1e-3)
    ref = {"voynich": target, "natural": natural, "scale": scale}
    CACHE.write_text(json.dumps(ref, indent=1))
    return ref


def score(lines, ref=None):
    """Returns (distance, per-metric z-scores). 0 = indistinguishable from the VMS
    on these metrics. Lines should hold at least N_WORDS words."""
    ref = ref or reference()
    p = metrics.profile(lines, N_WORDS)
    z = {k: (p[k] - ref["voynich"][k]) / ref["scale"][k] for k in KEYS}
    dist = (sum(v * v for v in z.values()) / len(z)) ** 0.5
    return dist, z, p
