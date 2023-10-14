import numpy as np
import networkx as nx

from .sandpile import Sandpile

import cnisip as cns


def degrees2nodes(degrees: np.ndarray) -> np.ndarray:
    return np.vectorize(lambda x: np.unpackbits(np.array([x], dtype="uint8")).sum())(
        degrees
    )


class DirectedSandpile(Sandpile):
    def __init__(
        self,
        rows: int,
        cols: int,
        tiling: str = "square",
        directions=(1, 1, -1),
        directed_graph: np.ndarray = np.empty(0),
    ) -> None:
        super().__init__(rows, cols, tiling=tiling)
        self.is_directed = True
        self.directions = np.array(directions)
        if np.size(directed_graph):
            self.directed_graph = directed_graph
            self.nodes_degrees = degrees2nodes(directed_graph)
        else:
            self.directed_graph = np.empty(0, dtype=np.int64)

    def set_random_graph(self):
        if self.tiling == "triangular":
            random_triangular_graph = cns.random_triangular_graph(self.rows, self.cols)
            self.directed_graph = random_triangular_graph[: self.rows]
            self.nodes_degrees = random_triangular_graph[self.rows :]

    def set_directed_graph(self, directed_graph: np.ndarray) -> None:
        """
        Set the directed graph of the sandpile.
        """
        assert directed_graph.shape == (self.rows, self.cols)
        self.directed_graph = directed_graph
        self.nodes_degrees = degrees2nodes(directed_graph)

    @property
    def meta(self):
        return super().meta | {
            "is_regular": self.is_regular,
            "directions": self.directions.tolist(),
        }

    @property
    def is_regular(self):
        if np.size(self.directed_graph):
            return False
        else:
            return True
