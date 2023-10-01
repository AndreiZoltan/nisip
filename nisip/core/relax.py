from copy import deepcopy

import numpy as np

from nisip.sandpiles.sandpile import Sandpile
import cnisip as cns


def relax(sandpile: Sandpile) -> Sandpile:
    """
    Relax the sandpile until it is stable.

    Parameters
    ----------
    sandpile : Sandpile
        The sandpile to relax.

    Returns
    -------
    Sandpile
        The relaxed sandpile.
    """
    sandpile = deepcopy(sandpile)
    if sandpile.tiling == "square":
        if sandpile.is_trivial_boundary:
            sandpile.set_graph(cns.relax_square(sandpile.graph))
    if sandpile.tiling == "triangular":
        if sandpile.is_trivial_boundary:
            sandpile.set_graph(cns.relax_triangular(sandpile.graph))
    return sandpile
