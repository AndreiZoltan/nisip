from typing import Union

import numpy as np

from nisip.sandpiles import Sandpile, DirectedSandpile
from nisip.core.relax import relax


def degrees2nodes(degrees: np.ndarray) -> np.ndarray:
    return np.vectorize(lambda x: np.unpackbits(np.array([x], dtype="uint8")).sum())(
        degrees
    )


def create_from_meta(
    meta: dict,
    untoppled: np.ndarray = np.empty(0),
    directed_graph: np.ndarray = np.empty(0),
    boundary: np.ndarray = np.empty(0),
) -> Union[Sandpile, DirectedSandpile]:
    """
    Create a sandpile from a metadata dictionary.
    """
    if meta["is_directed"] == True:
        sandpile = DirectedSandpile(meta["shape"], meta["tiling"], meta["directions"])
        if not meta["is_regular"]:
            sandpile.set_directed_graph(directed_graph)
    else:
        sandpile = Sandpile(meta["shape"], meta["tiling"])
    if not meta["is_trivial_boundary"]:
        sandpile.set_boundary(boundary)
    sandpile.set_graph(untoppled)
    sandpile = relax(sandpile)
    return sandpile


def charge_graph(x: int, y: int, shape: tuple) -> np.ndarray:
    """
    Get charge-like boundary.
    """
    graph = np.zeros(shape, dtype=np.int64)
    # graph[x, y+1] = 240
    grid = np.indices(shape)
    graph[: x + 1, y:-1] |= 1 << 0
    graph[1 : x + 1, y:] |= 1 << 3
    graph[:x, y + 1 : -1] |= np.where(grid[0] + grid[1] >= x + y, 1 << 4, 0)[
        :x, y + 1 : -1
    ]
    graph[1:x, y + 1 :] |= np.where(grid[0] + grid[1] <= x + y, 1 << 5, 0)[1:x, y + 1 :]

    graph[x:, 1 : y + 1] |= 1 << 1
    graph[x:-1, : y + 1] |= 1 << 2
    graph[x + 1 : -1, :y] |= np.where(grid[0] + grid[1] >= x + y, 1 << 4, 0)[
        x + 1 : -1, :y
    ]
    graph[x + 1 :, 1:y] |= np.where(grid[0] + grid[1] <= x + y, 1 << 5, 0)[x + 1 :, 1:y]

    graph[: x + 1, 1 : y + 1] |= np.where(grid[1] <= grid[0] + y - x, 1 << 1, 0)[
        : x + 1, 1 : y + 1
    ]
    graph[1 : x + 1, 1 : y + 1] |= np.where(grid[1] <= grid[0] + y - x, 1 << 5, 0)[
        1 : x + 1, 1 : y + 1
    ]
    graph[1:x, :y] |= np.where(
        (grid[1] >= 2 * grid[0] - 2 * x + y) & (grid[1] < grid[0] + y - x), 1 << 3, 0
    )[1:x, :y]
    graph[:x, :y] |= np.where(grid[1] <= 2 * grid[0] - 2 * x + y, 1 << 2, 0)[:x, :y]

    graph[1 : x + 1, : y + 1] |= np.where(grid[1] >= grid[0] + y - x, 1 << 3, 0)[
        1 : x + 1, : y + 1
    ]
    graph[1 : x + 1, 1 : y + 1] |= np.where(grid[1] >= grid[0] + y - x, 1 << 5, 0)[
        1 : x + 1, 1 : y + 1
    ]
    graph[:x, :y] |= np.where(grid[1] >= grid[0] / 2 - x / 2 + y, 1 << 0, 0)[:x, :y]
    graph[:x, 1:y] |= np.where(
        (grid[1] <= grid[0] / 2 - x / 2 + y) & (grid[1] > grid[0] + y - x), 1 << 1, 0
    )[:x, 1:y]

    graph[x:, y:-1] |= np.where(grid[1] >= grid[0] + y - x, 1 << 0, 0)[x:, y:-1]
    graph[x:-1, y:-1] |= np.where(grid[1] >= grid[0] + y - x, 1 << 4, 0)[x:-1, y:-1]
    graph[x + 1 :, y + 1 :] |= np.where(grid[1] >= 2 * grid[0] - 2 * x + y, 1 << 3, 0)[
        x + 1 :, y + 1 :
    ]
    graph[x + 1 : -1, y + 1 :] |= np.where(
        (grid[1] <= 2 * grid[0] - 2 * x + y) & (grid[1] > grid[0] + y - x), 1 << 2, 0
    )[x + 1 : -1, y + 1 :]

    graph[x:-1, y:] |= np.where(grid[1] <= grid[0] + y - x, 1 << 2, 0)[x:-1, y:]
    graph[x:-1, y:-1] |= np.where(grid[1] <= grid[0] + y - x, 1 << 4, 0)[x:-1, y:-1]
    graph[x + 1 :, y + 1 :] |= np.where(grid[1] <= grid[0] / 2 - x / 2 + y, 1 << 1, 0)[
        x + 1 :, y + 1 :
    ]
    graph[x + 1 :, y + 1 : -1] |= np.where(
        (grid[1] >= grid[0] / 2 - x / 2 + y) & (grid[1] < grid[0] + y - x), 1 << 0, 0
    )[x + 1 :, y + 1 : -1]
    return graph


def charge_graph_with_corridors(
    x: int, y: int, stride: int, shape: tuple
) -> np.ndarray:
    grid = np.indices(shape)
    graph = charge_graph(x, y, shape)
    for i in range(x % stride, shape[0], stride):
        graph[i] |= 0b111111
    for i in range(y % stride, shape[1], stride):
        graph[:, i] |= 0b111111
    for i in range(-shape[0] + ((shape[0] + y - x) % stride), np.sum(shape), stride):
        graph |= np.where(grid[1] == grid[0] + y - x + i, 0b111111, 0)
    return graph
