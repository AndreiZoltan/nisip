from nisip.sandpiles.basesandpile import BaseSandpile


class Sandpile(BaseSandpile):
    """
    A class of sandpile for triangular lattices.
    """

    def __init__(self, height: int, width: int, tiling: str = "square") -> None:
        super().__init__(height, width, tiling)
