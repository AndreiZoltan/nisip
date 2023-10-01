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
    if sandpile.tiling == "square":
        if sandpile.is_trivial_boundary:
            return cns.relax_square(sandpile.graph)
    return sandpile