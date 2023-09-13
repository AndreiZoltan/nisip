import numpy as np
import networkx as nx


class BaseSandpile:
    def __init__(self, size, tiling= 'square') -> None:
        if tiling not in ['triangular', 'square', 'hexagonal']:
            raise ValueError("Tiling must be either 'triangle',\
                             'square' or 'hexagonal'.")
        self.graph = np.zeros((size, size), dtype=np.int64)
        # else:
        #     if tiling == 'triangular':
        #         self.graph = nx.triangular_lattice_graph(size, size)
        #     elif tiling == 'square':
        #         self.graph = nx.grid_2d_graph(size, size)
        #     elif tiling == 'hexagonal':
        #         self.graph = nx.hexagonal_lattice_graph(size, size)
        self.tiling = tiling
        self.size = size

    def __repr__(self) -> str:
        return f"Sandpile(size={self.size}, tiling='{self.tiling}')"
    
    def add(self, x: int, y: int, z: int) -> None:
        """
        Add z grains of sand to the pile at (x, y).
        """
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
        self.graph[x, y] = z
    
    @property
    def grains(self) -> int:
        """
        Return the total number of grains in the sandpile.
        """
        return int(np.sum(self.graph))