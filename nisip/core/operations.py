from copy import deepcopy

import numpy as np

from nisip.sandpiles import Sandpile
from nisip.core.relax import relax


def add(sandpile: Sandpile, x: int, y: int, z: int) -> Sandpile:
    sandpile = deepcopy(sandpile)
    sandpile.add(x, y, z)
    return sandpile
