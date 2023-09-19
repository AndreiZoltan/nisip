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
            print(np.max(sandpile.graph))
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


def drop_sand_cache(sandpile: Sandpile, x: int, y: int, z: int) -> Sandpile:
    """
    Add z grains of sand to the pile at (x, y).
    """
    sandpile = deepcopy(sandpile)
    sandpile.add_history(x, y, z)
    sandpile.add(x, y, z)
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
        cache = np.empty((0, 2), dtype=np.int32)
        cache = np.append(cache, [[x, y]], axis=0)
        while np.max(sandpile.graph) >= 6:
            print(np.max(sandpile.graph), "all caches are zero")
            while cache.shape[0] > 0:
                print(np.max(sandpile.graph), "cache is not zero")
                new_cache = np.empty((0, 2), dtype=np.int32)
                for x, y in cache:
                    grains = sandpile.get(x, y)
                    sandpile.set(x, y, grains % 6)
                    grains = grains // 6
                    sandpile.add(x + 1, y, grains)
                    sandpile.add(x - 1, y, grains)
                    sandpile.add(x, y + 1, grains)
                    sandpile.add(x, y - 1, grains)
                    sandpile.add(x - 1, y - 1, grains)
                    sandpile.add(x + 1, y + 1, grains)
                    if grains > 5:
                        new_cache = np.append(new_cache, [[x + 1, y]], axis=0)
                        new_cache = np.append(new_cache, [[x - 1, y]], axis=0)
                        new_cache = np.append(new_cache, [[x, y + 1]], axis=0)
                        new_cache = np.append(new_cache, [[x, y - 1]], axis=0)
                        new_cache = np.append(new_cache, [[x - 1, y - 1]], axis=0)
                        new_cache = np.append(new_cache, [[x + 1, y + 1]], axis=0)
                cache = new_cache

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
