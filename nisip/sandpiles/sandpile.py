import random

import numpy as np

import cnisip as cns


class Sandpile:
    def __init__(self, shape, tiling="square") -> None:
        assert tiling in ("triangular", "square", "hexagonal")
        rows, cols = shape
        self.graph = np.zeros(shape, dtype=np.int64)
        self.untoppled = np.zeros(shape, dtype=np.int64)
        self.id = random.getrandbits(128)
        self.tiling = tiling

        boundary = np.zeros(shape, dtype=np.int64)
        boundary[:, ::cols] = 1
        boundary[::rows, :] = 1
        self.set_boundary(boundary)

        self.set_undirected_graph()

        self.directions = None

    def __repr__(self) -> str:
        return f"Meta: {self.meta}"

    def add(self, x: int, y: int, z: int) -> None:
        """
        Add z grains of sand to the pile at (x, y).
        """
        self.untoppled[x, y] += z
        self.graph[x, y] += z

    def add_everywhere(self, z: int) -> None:
        """
        Add z grains of sand everywhere.
        """
        self.untoppled += z
        self.graph += z

    def get(self, x: int, y: int) -> int:
        """
        Return the number of grains at (x, y).
        """
        return self.graph[x, y]

    def set_graph(self, graph: np.ndarray) -> None:
        """
        Set the graph of the sandpile.
        """
        assert graph.shape == self.graph.shape
        self.untoppled = graph
        self.graph = graph

    def get_graph(self):
        return self.graph.astype(np.int64)

    def degrees2nodes(self, degrees: np.ndarray) -> np.ndarray:
        return np.vectorize(
            lambda x: np.unpackbits(np.array([x], dtype="uint8")).sum()
        )(degrees)

    def set_directed_graph(self, directed_graph: np.ndarray) -> None:
        """
        Set the directed graph of the sandpile.
        """
        assert directed_graph.shape == self.shape
        self.directed_graph = directed_graph
        self.nodes_degrees = self.degrees2nodes(directed_graph)
        self.directions = None

    def undirected_graph(self):
        directed_graph = np.full(self.shape, 0b111111)
        directed_graph[0] &= 0b010111
        directed_graph[-1] &= 0b101011
        directed_graph[:, 0] &= 0b011101
        directed_graph[:, -1] &= 0b101110
        return directed_graph

    def set_undirected_graph(self):
        self.set_directed_graph(self.undirected_graph())

    def set_regular_graph(self, directions: tuple) -> None:
        assert len(directions) == 3
        self.directions = np.array(directions)
        # TODO set directed graph normally
        self.directed_graph *= 0

    def set_random_graph(self):
        if self.tiling == "triangular":
            random_triangular_graph = cns.random_triangular_graph(self.rows, self.cols)
            self.set_directed_graph(random_triangular_graph)

    def set_boundary(self, boundary: np.ndarray) -> None:
        """
        Set the boundary of the sandpile.
        """
        assert boundary.shape == self.shape
        assert set(np.unique(boundary)) == {0, 1}
        self.boundary = boundary

    def set_trivial_boundary(self) -> None:
        """
        Set the boundary of the sandpile to trivial.
        """
        self.boundary = np.zeros(self.shape, dtype=np.int64)
        self.boundary[:, 0 :: self.cols] = 1
        self.boundary[0 :: self.rows, :] = 1

    @property
    def degree(self) -> int:
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
            "shape": self.shape,
            "tiling": self.tiling,
            "is_directed": self.is_directed,
            "degree": self.degree,
            "is_trivial_boundary": self.is_trivial_boundary,
            "is_regular": self.is_regular,
            "directions": self.directions.tolist()
            if self.directions is not None
            else None,
        }

    @property
    def is_trivial_boundary(self) -> bool:
        """
        Return True if the boundary is trivial.
        """
        if (
            (self.boundary[:, 0 :: self.cols] == 1).all()
            and (self.boundary[0 :: self.rows, :] == 1).all()
            and (self.boundary[1 : self.rows - 1, 1 : self.cols - 1] == 0).all()
        ):
            return True
        return False

    @property
    def shape(self):
        return self.graph.shape

    @property
    def rows(self):
        return self.shape[0]

    @property
    def cols(self):
        return self.shape[1]

    @property
    def is_directed(self):
        return not (self.directed_graph == self.undirected_graph()).all()

    @property
    def is_regular(self):
        return self.directions is not None
