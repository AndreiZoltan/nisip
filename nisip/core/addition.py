"""
In this file we will define a class of sandpile for trianglular lattices.

"""

import numpy as np

from nisip.sandpiles.basesandpile import BaseSandpile
# drop_sand
def drop_sand(sandpile: BaseSandpile, x: int, y: int, z: int) -> BaseSandpile:
    """
    Add z grains of sand to the pile at (x, y).
    """
    sandpile.add(x, y, z)
    if sandpile.tiling == 'square':
        while np.max(sandpile.graph) >= 4:
            # print(np.max(sandpile.graph), "max")
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
    elif sandpile.tiling == 'triangular':
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
