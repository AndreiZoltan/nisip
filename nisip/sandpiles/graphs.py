import numpy as np


def degrees2nodes(degrees: np.ndarray) -> np.ndarray:
    return np.vectorize(lambda x: np.unpackbits(np.array([x], dtype="uint8")).sum())(
        degrees
    )


def charge_graph(x: int, y: int, shape: tuple) -> np.ndarray:
    """
    Get charge-like boundary.
    """
    graph = np.zeros(shape, dtype=np.int64)
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


def regular_graph(directions: tuple, shape: tuple) -> np.ndarray:
    assert len(directions) == 3
    assert set(directions) <= {-1, 1}
    directs = np.array(directions)
    dir_bits = np.array([0, 2, 4])
    dir_bits[directs < 0] += 1
    dir_bits = (2**dir_bits).sum()
    graph = np.full(shape, dir_bits)

    graph[0] &= 0b010111
    graph[-1] &= 0b101011
    graph[:, 0] &= 0b011101
    graph[:, -1] &= 0b101110
    return graph


def random_graph(shape):
    return np.random.choice(1 << 6 - 1, size=shape)
