"""
In this file we will define a class of sandpile for trianglular lattices.

"""
from copy import deepcopy

import numpy as np

from nisip.sandpiles.sandpile import Sandpile


def drop_sand(sandpile: Sandpile, x: int, y: int, z: int) -> Sandpile:
    """
    Add z grains of sand to the pile at (x, y).
    """
    sandpile = deepcopy(sandpile)
    sandpile.add_history(x, y, z)
    sandpile.add(x, y, z)
    assert sandpile.tiling in ["triangular"]
    if sandpile.tiling == "square":
        while np.max(sandpile.graph) >= 4:
            indexes = np.argwhere(sandpile.graph > 3)
            # TODO delete invalid indexes
            for x, y in indexes:
                grains = sandpile.get(x, y)
                sandpile.set(x, y, grains % 4)
                grains = grains // 4
                sandpile.add(x + 1, y, grains)
                sandpile.add(x - 1, y, grains)
                sandpile.add(x, y + 1, grains)
                sandpile.add(x, y - 1, grains)
    elif sandpile.tiling == "triangular":
        while np.max(sandpile.graph) >= 6:
            indexes = np.argwhere(sandpile.graph > 5)
            # TODO delete invalid indexes
            for x, y in indexes:
                grains = sandpile.get(x, y)
                sandpile.set(x, y, grains % 6)
                grains = grains // 6
                sandpile.add(x + 1, y, grains)
                sandpile.add(x - 1, y, grains)
                sandpile.add(x, y + 1, grains)
                sandpile.add(x, y - 1, grains)
                sandpile.add(x - 1, y - 1, grains)
                sandpile.add(x + 1, y + 1, grains)
    return sandpile
