import random
import json

import numpy as np


class Sandpile:
    def __init__(self, rows, cols, tiling="square") -> None:
        assert tiling in ("triangular", "square", "hexagonal")
        self.graph = np.zeros((rows, cols), dtype=np.int64)
        self.id = random.getrandbits(128)
        self.tiling = tiling
        self.rows = rows
        self.cols = cols
        self.is_directed = False
        self.history = np.empty((0, 3))

        self.boundary = np.zeros((rows, cols), dtype=np.int64)
        self.boundary[:, 0::cols] = 1
        self.boundary[0::rows, :] = 1
        self.is_trivial_boundary = True

    def __repr__(self) -> str:
        return f"Sandpile(rows={self.rows}, cols={self.cols}, tiling={self.tiling})"

    def add(self, x: int, y: int, z: int) -> None:
        """
        Add z grains of sand to the pile at (x, y).
        """
        if 0 < x < self.rows - 1 and 0 < y < self.cols - 1:
            self.add_history(x, y, z)
            self.graph[x, y] += z

    def get(self, x: int, y: int) -> int:
        """
        Return the number of grains at (x, y).
        """
        return self.graph[x, y]

    def set(self, x: int, y: int, z: int) -> None:
        """
        Set the number of grains at (x, y) to z.
        """
        if 0 < x < self.rows - 1 and 0 < y < self.cols - 1:
            self.graph[x, y] = z

    def set_graph(self, graph: np.ndarray) -> None:
        """
        Set the graph of the sandpile.
        """
        assert graph.shape == self.graph.shape
        self.graph = graph

    def get_graph(self):
        return self.graph.astype(np.int64)

    def set_boundary(self, boundary: np.ndarray) -> None:
        """
        Set the boundary of the sandpile.
        """
        assert boundary.shape == self.boundary.shape
        self.boundary = boundary
        self.is_trivial_boundary = False

    def add_history(self, x: int, y: int, z: int) -> None:
        """
        Add a step to the history of the sandpile.
        """
        self.history = np.append(self.history, np.array([[x, y, z]]), axis=0)

    @property
    def grains(self) -> int:
        """
        Return the total number of grains in the sandpile.
        """
        return int(np.sum(self.graph))

    @property
    def meta(self):
        """
        Return the metadata of the sandpile.
        """
        return {
            "id": self.id,
            "rows": self.rows,
            "cols": self.cols,
            "tiling": self.tiling,
            "is_directed": self.is_directed,
            "grains": self.grains,
            "history": self.history.tolist(),
        }
