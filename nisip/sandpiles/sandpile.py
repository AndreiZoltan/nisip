from nisip.sandpiles.basesandpile import BaseSandpile


class Sandpile(BaseSandpile):
    """
    A class of sandpile for triangular lattices.
    """

    def __init__(self, width: int, height: int, tiling: str = "square") -> None:
        super().__init__(width, height, tiling)
