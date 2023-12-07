import numpy as np

import nisip as ns
from nisip.core.graph_theory import adjacency_matrix


def adjacency_matrix(graph: np.ndarray, tiling: int) -> np.ndarray:
    """Return the adjacency matrix of a graph.

    Args:
        graph (np.ndarray): Graph to be converted.
        tiling (int): Tiling of the graph.

    Returns:
        np.ndarray: Adjacency matrix of the graph.
    """
    assert tiling in ns.TILINGS, f"Invalid tiling: {tiling}"
    rows, cols = graph.shape
    nodes = rows * cols

    adjacency_matrix = np.zeros((nodes, nodes), dtype=np.int64)
    grid = np.indices(adjacency_matrix.shape)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]

    for shift, direction in enumerate(directions):
        mask = (grid[1] - grid[0]) % nodes == (
            cols * direction[0] + direction[1]
        ) % nodes
        values = (graph & 1 << shift).flatten()
        values[values != 0] = 1
        adjacency_matrix[mask] = values

    return adjacency_matrix


def laplacian(graph: np.ndarray, tiling: int) -> np.ndarray:
    """Return the Laplacian of a graph.

    Args:
        graph (np.ndarray): Graph to be converted.
        tiling (int): Tiling of the graph.

    Returns:
        np.ndarray: Laplacian of the graph.
    """
    assert tiling in ns.TILINGS, f"Invalid tiling: {tiling}"
    adj_matrix = adjacency_matrix(graph, tiling)
    return np.diag(np.sum(adj_matrix, axis=1)) - adj_matrix
