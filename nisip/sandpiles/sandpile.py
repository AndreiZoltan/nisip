from copy import deepcopy

from nisip.sandpiles.basesandpile import BaseSandpile
from nisip.core.addition import drop_sand

class Sandpile(BaseSandpile):
    """
    A class of sandpile for triangular lattices.
    """
    def __init__(self, width: int, height: int, tiling: str = 'square') -> None:
        super().__init__(width, height, tiling)

    def drop_sand(self, x: int, y: int, z: int) -> BaseSandpile:
        return drop_sand(self, x, y, z)