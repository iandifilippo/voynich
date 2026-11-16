import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))          # experiments/ (for _common)
sys.path.insert(0, str(HERE.parent.parent))   # repo root (for voynich)
