"""
In this file we will define a class of sandpile for trianglular lattices.

"""

import numpy as np

from nisip.sandpile import Sandpile

def add_grain(sandpile: Sandpile, x: int, y: int, z: int) -> None:
    """
    Add z grains of sand to the pile at (x, y).
    """
    if sandpile.tiling == 'square':
        while np.max(sandpile.grid) >= 4:
            ...
            
    if sandpile.tiling == 'triangle':
        while np.max(sandpile.grid) >= 6:
            ...