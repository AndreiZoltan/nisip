import numpy as np

from nisip.sandpiles import Sandpile


def create_from_meta(
    meta: dict,
    untoppled: np.ndarray,
    directed_graph: np.ndarray | None = None,
    boundary: np.ndarray | None = None,
) -> Sandpile:
    """
    Create a sandpile from a metadata dictionary.
    """
    sandpile = Sandpile(meta["shape"], meta["tiling"])
    if directed_graph is not None:
        sandpile.set_graph(directed_graph)
    if boundary is not None:
        sandpile.set_boundary(boundary)
    sandpile.set_configuration(untoppled)
    return sandpile
