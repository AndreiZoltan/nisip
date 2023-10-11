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
    directed_graph: np.ndarray = np.empty(0),
    boundary: np.ndarray = np.empty(0),
) -> Union[Sandpile, DirectedSandpile]:
    """
    Create a sandpile from a metadata dictionary.
    """
    if meta["is_directed"] == True:
        sandpile = DirectedSandpile(
            int(meta["rows"]), int(meta["cols"]), meta["tiling"], meta["directions"]
        )
        if not meta["is_regular"]:
            sandpile.set_directed_graph(directed_graph)
    else:
        sandpile = Sandpile(int(meta["rows"]), int(meta["cols"]), meta["tiling"])
    if not meta["is_trivial_boundary"]:
        sandpile.set_boundary(boundary)
    for x, y, z in np.array(meta["history"], dtype=np.int64):
        sandpile.add(x, y, z)
        sandpile = relax(sandpile)
    return sandpile
