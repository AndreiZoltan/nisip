from copy import deepcopy
import numpy as np


class Sandpile:
    def __init__(self, shape, tiling="triangular") -> None:
        assert tiling in ("triangular", "square", "hexagonal")
        self.configuration = np.zeros(shape, dtype=np.int64)
        self.untoppled = np.zeros(shape, dtype=np.int64)
        self.tiling = tiling

        boundary = np.zeros(shape, dtype=np.int64)
        self.set_boundary(boundary)

        self.set_undirected_graph()

        self.directions = None

    def __repr__(self) -> str:
        return f"Meta: {self.meta}"

    def __eq__(self, other):
        assert isinstance(other, Sandpile)
        assert self.shape == other.shape, f"{self.shape} != {other.shape}"
        assert self.tiling == other.tiling, f"{self.tiling} != {other.tiling}"
        assert (self.graph == other.graph).all(), f"{self.graph} != {other.graph}"
        assert (
            self.boundary == other.boundary
        ).all(), f"{self.boundary} != {other.boundary}"
        return (self.configuration == other.configuration).all()

    def __add__(self, other):
        assert isinstance(other, Sandpile)
        assert self.shape == other.shape
        assert self.tiling == other.tiling
        assert (self.graph == other.graph).all()
        assert (self.boundary == other.boundary).all()
        self.add_configuration(other.configuration)
        return self

    def __mul__(self, multiplier):
        assert isinstance(multiplier, int)
        assert multiplier >= 0
        new_instance = deepcopy(self)
        new_instance.set_configuration(self.configuration * multiplier)
        return new_instance

    def add(self, x: int, y: int, z: int) -> None:
        """
        Add z grains of sand to the pile at (x, y).
        """
        if self.boundary[x, y] == 0:
            self.untoppled[x, y] += z
            self.configuration[x, y] += z

    def add_everywhere(self, z: int) -> None:
        """
        Add z grains of sand everywhere.
        """
        self.untoppled[self.boundary == 0] += z
        self.configuration[self.boundary == 0] += z

    def get(self, x: int, y: int) -> int:
        """
        Return the number of grains at (x, y).
        """
        return self.configuration[x, y]

    def add_configuration(self, configuration: np.ndarray) -> None:
        """
        Add configuration to the sandpile.
        """
        assert configuration.shape == self.configuration.shape
        self.untoppled += configuration
        self.configuration += configuration

    def set_configuration(self, configuration: np.ndarray) -> None:
        """
        Set the configuration of the sandpile.
        """
        assert configuration.shape == self.configuration.shape
        self.untoppled = configuration  # TODO add boundary condition
        self.configuration = configuration

    def get_configuration(self):
        return self.configuration.astype(np.int64)

    def degrees2nodes(self, degrees: np.ndarray) -> np.ndarray:
        return np.vectorize(
            lambda x: np.unpackbits(np.array([x], dtype="uint8")).sum()
        )(degrees).astype(np.int64)

    def set_graph(self, graph: np.ndarray) -> None:
        """
        Set the directed graph of the sandpile.
        """
        assert graph.shape == self.shape
        self.graph = graph
        self.nodes_degrees = self.degrees2nodes(graph)
        self.untoppled[:] = self.configuration

    def undirected_graph(self):
        graph = np.full(self.shape, 0b111111)
        graph[0] &= 0b010111
        graph[-1] &= 0b101011
        graph[:, 0] &= 0b011101
        graph[:, -1] &= 0b101110
        return graph

    def set_undirected_graph(self) -> None:
        self.set_graph(self.undirected_graph())

    def set_boundary(self, boundary: np.ndarray) -> None:
        """
        Set the boundary of the sandpile.
        """
        assert boundary.shape == self.shape
        assert set(np.unique(boundary)) <= {0, 1}
        boundary[0 :: self.rows - 1] = 1
        boundary[:, 0 :: self.cols - 1] = 1
        self.boundary = boundary

    @property
    def max_recurrent(self):
        max_recurent = self.nodes_degrees - 1
        max_recurent[self.boundary == 1] = 0
        return max_recurent

    @property
    def degree(self) -> int:
        """
        Return the total number of grains in the sandpile.
        """
        return int(np.sum(self.configuration))

    @property
    def meta(self):  # TODO get rid of auxilary methods
        """
        Return the metadata of the sandpile.
        """
        return {
            "shape": self.shape,
            "tiling": self.tiling,
            "is_directed": self.is_directed,
            "degree": self.degree,
            "is_trivial_boundary": self.is_trivial_boundary,
        }

    @property
    def is_trivial_boundary(self) -> bool:
        """
        Return True if the boundary is trivial.
        """
        if (
            (self.boundary[:: self.rows - 1] == 1).all()
            and (self.boundary[:, :: self.cols - 1] == 1).all()
            and (self.boundary[1 : self.rows - 1, 1 : self.cols - 1] == 0).all()
        ):
            return True
        return False

    @property
    def shape(self):
        return self.configuration.shape

    @property
    def rows(self):
        return self.shape[0]

    @property
    def cols(self):
        return self.shape[1]

    @property
    def is_directed(self):
        return not (self.graph == self.undirected_graph()).all()

    @property
    def is_regular(self):
        return self.directions is not None
