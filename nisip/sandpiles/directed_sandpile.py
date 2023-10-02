import numpy as np

from .sandpile import Sandpile


class DirectedSandpile(Sandpile):
    def __init__(self, rows, cols, tiling="square", directions=(1, 1, -1)) -> None:
        super().__init__(rows, cols, tiling)
        self.is_directed = True
        self.directions = np.array(directions)
