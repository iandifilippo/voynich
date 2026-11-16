"""Line and gap measurements on page scans (no transcription involved).

Pipeline: grayscale -> Sauvola binarisation -> drop small specks -> pick the
skew angle that makes the row profile sharpest -> find text lines as peaks of
the row profile -> inside each line, find runs of empty columns (gaps).
Needs numpy, scipy, scikit-image, Pillow.
"""
import numpy as np
from PIL import Image
from scipy import ndimage, signal
from skimage.filters import threshold_sauvola
from skimage.morphology import remove_small_objects


def load_gray(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im, dtype=np.float32) / 255.0
    # ink is dark and brownish; the red stars are dark in green/blue but bright in red,
    # so use the red channel to suppress them a bit
    return 0.6 * a[..., 0] + 0.4 * a[..., 1]


def binarize(gray, window=31, k=0.2, min_size=12):
    t = threshold_sauvola(gray, window_size=window, k=k)
    ink = gray < t
    return remove_small_objects(ink, max_size=min_size - 1)


def text_box(ink, frac=0.02):
    """Crop to the band of columns/rows that actually hold text (ignores dark scan borders)."""
    cols = ink.mean(axis=0)
    rows = ink.mean(axis=1)
    h, w = ink.shape
    c0, c1 = int(w * 0.08), int(w * 0.92)
    r0, r1 = int(h * 0.03), int(h * 0.97)
    return r0, r1, c0, c1


def best_skew(ink, angles=np.arange(-3, 3.01, 0.25)):
    best, best_a = -1, 0.0
    small = ink[::2, ::2].astype(np.float32)
    for a in angles:
        rot = ndimage.rotate(small, a, reshape=False, order=0)
        prof = rot.sum(axis=1)
        score = np.var(prof)
        if score > best:
            best, best_a = score, a
    return best_a


def find_lines(ink, min_gap=14, smooth=3, rel_height=0.18):
    prof = ndimage.gaussian_filter1d(ink.sum(axis=1).astype(float), smooth)
    peaks, props = signal.find_peaks(prof, distance=min_gap, height=prof.max() * rel_height, prominence=prof.max() * 0.08)
    return peaks, prof


def line_gaps(ink, center, half=9, min_ink_cols=1):
    """Widths of empty column runs inside one text line, trimmed to the inked extent."""
    band = ink[max(0, center - half): center + half + 1]
    col = band.sum(axis=0) >= min_ink_cols
    xs = np.flatnonzero(col)
    if len(xs) < 10:
        return [], (0, 0)
    col = col[xs[0]: xs[-1] + 1]
    gaps, run = [], 0
    for v in col:
        if not v:
            run += 1
        elif run:
            gaps.append(run)
            run = 0
    return gaps, (int(xs[0]), int(xs[-1]))


def analyse_page(path):
    gray = load_gray(path)
    ink = binarize(gray)
    r0, r1, c0, c1 = text_box(ink)
    ink = ink[r0:r1, c0:c1]
    angle = best_skew(ink)
    ink = ndimage.rotate(ink.astype(np.uint8), angle, reshape=False, order=0).astype(bool)
    peaks, prof = find_lines(ink)
    lines = []
    for p in peaks:
        gaps, extent = line_gaps(ink, int(p))
        lines.append({"y": int(p), "gaps": gaps, "x0": extent[0], "x1": extent[1]})
    return {"angle": float(angle), "lines": lines, "shape": ink.shape}
