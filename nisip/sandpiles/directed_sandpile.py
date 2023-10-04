import numpy as np
import networkx as nx

from .sandpile import Sandpile

import cnisip as cns


class DirectedSandpile(Sandpile):
    def __init__(self, rows: int, cols: int, tiling: str="square", directions=(1, 1, -1),
                 directed_graph: np.ndarray=np.empty(0)) -> None:
        super().__init__(rows, cols, tiling=tiling)
        self.is_directed = True
        self.directions = np.array(directions)
        if np.size(directed_graph) == 0:
            self.is_regular = True
        else:
            self.is_regular = False
            self.directed_graph = directed_graph

    def set_random_graph(self):
        self.is_regular = False
        if self.tiling == "triangular":
            random_triangular_graph = cns.random_triangular_graph(self.rows, self.cols)
            self.directed_graph = random_triangular_graph[:self.rows]
            self.nodes_degrees = random_triangular_graph[self.rows:]