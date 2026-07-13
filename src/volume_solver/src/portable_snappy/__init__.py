import sys
import os

dirnow = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirnow) # to import: decorator and networkx

from . import snappy
__all__ = [
    "snappy",
]

if sys.path[-1] == dirnow:
    sys.path.pop(-1) # delete last term: dirnow
