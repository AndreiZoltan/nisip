from pathlib import Path

NISIP_DIR = Path(__file__).parent
PROJECT_DIR = NISIP_DIR.parent
TESTS_DIR = PROJECT_DIR / "tests"

SQUARE = 4
TRIANGULAR = 3
HEXAGONAL = 6
TILINGS = [SQUARE, TRIANGULAR, HEXAGONAL]

__all__ = [
    "Sandpile",
    "relax",
    "save",
    "add",
    "create_from_meta",
    "degrees2nodes",
    "charge_graph",
    "charge_graph_with_corridors",
    "regular_graph",
    "random_graph",
    "identity",
    "hexagon_boundary",
    "adjacency_matrix",
    "undirected_graph",
    "pyrelax",
    "tairelax",
]
from .sandpiles import (
    Sandpile,
    degrees2nodes,
    charge_graph,
    charge_graph_with_corridors,
    regular_graph,
    random_graph,
    hexagon_boundary,
    undirected_graph,
)
from .core import (
    relax,
    save,
    add,
    create_from_meta,
    identity,
    adjacency_matrix,
    pyrelax,
    tairelax,
    calc_identity,
)
