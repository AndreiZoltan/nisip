from copy import deepcopy

from nisip.sandpiles.basesandpile import BaseSandpile
from nisip.core.addition import drop_sand

class Sandpile(BaseSandpile):
    """
    A class of sandpile for triangular lattices.
    """
    def __init__(self, size: int, tiling: str = 'square') -> None:
        super().__init__(size, tiling)

    def drop_sand(self, x: int, y: int, z: int) -> BaseSandpile:
        return drop_sand(deepcopy(self), x, y, z)