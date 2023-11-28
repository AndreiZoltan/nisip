from copy import deepcopy

import numpy as np

from nisip.sandpiles import Sandpile
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
    elif sandpile.tiling == "triangular":
        if sandpile.is_directed:
            if sandpile.is_trivial_boundary:
                sandpile.set_graph(
                    cns.relax_triangular_directed_irregular(
                        sandpile.graph,
                        sandpile.directed_graph,
                        sandpile.nodes_degrees,
                    )
                )
            else:
                sandpile.set_graph(
                    cns.relax_triangular_directed_irregular_non_trivial_boundary(
                        sandpile.graph,
                        sandpile.directed_graph,
                        sandpile.nodes_degrees,
                        sandpile.boundary,
                    )
                )
        else:
            if sandpile.is_trivial_boundary:
                sandpile.set_graph(cns.relax_triangular(sandpile.graph))
            else:
                sandpile.set_graph(
                    cns.relax_triangular_non_trivial_boundary(
                        sandpile.graph, sandpile.boundary
                    )
                )
    return sandpile
