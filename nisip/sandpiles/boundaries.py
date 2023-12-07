import numpy as np


def hexagon_boundary(x: int, y: int, diameter: int, shape: tuple) -> np.ndarray:
    """
    Get charge-like boundary.
    """
    assert len(shape) == 2
    boundary = np.zeros(shape, dtype=np.int64)
    grid = np.indices(shape)
    boundary[: x - diameter] = 1
    boundary[x + diameter + 1 :] = 1
    boundary[:, : y - diameter] = 1
    boundary[:, y + diameter + 1 :] = 1
    boundary[grid[0] - grid[1] < x - y - diameter] = 1
    boundary[grid[0] - grid[1] > x - y + diameter] = 1
    return boundary
