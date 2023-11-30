from copy import deepcopy

import numpy as np
from numba import jit

from nisip.sandpiles import Sandpile
import cnisip as cns


def relax_directed(sandpile: Sandpile) -> np.ndarray:
    sandpile.graph = sandpile.graph.astype(np.int32)
    nodes_degrees = np.where(
        sandpile.nodes_degrees != 0, sandpile.nodes_degrees, 6
    ).astype(np.int32)
    sandpile.graph[sandpile.boundary != 0] = 0
    shift_masks = np.zeros((6, *sandpile.graph.shape), dtype=np.bool_)
    for i in range(6):
        shift_masks[i] = (sandpile.directed_graph & (1 << i)) != 0
    while (sandpile.graph >= nodes_degrees).any():
        mask = sandpile.graph >= nodes_degrees
        pile = np.where(mask, sandpile.graph, 0)
        sandpile.graph[mask] = pile[mask] % nodes_degrees[mask]
        pile = pile // nodes_degrees
        shifts = mask & shift_masks
        sandpile.graph[:, 1:][shifts[0, :, :-1]] += pile[shifts[0]]
        sandpile.graph[:, :-1][shifts[1, :, 1:]] += pile[shifts[1]]
        sandpile.graph[1:, :][shifts[2, :-1, :]] += pile[shifts[2]]
        sandpile.graph[:-1, :][shifts[3, 1:, :]] += pile[shifts[3]]
        sandpile.graph[1:, 1:][shifts[4, :-1, :-1]] += pile[shifts[4]]
        sandpile.graph[:-1, :-1][shifts[5, 1:, 1:]] += pile[shifts[5]]
        sandpile.graph[sandpile.boundary != 0] = 0
    sandpile.graph[sandpile.nodes_degrees == 0] = 0
    return sandpile.graph


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
        sandpile.set_graph(relax_directed(sandpile))
    return sandpile


def _relax(sandpile: Sandpile) -> Sandpile:
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
                # sandpile.set_graph(relax_directed(sandpile))
                sandpile.set_graph(
                    cns.relax_triangular_directed_irregular(
                        sandpile.graph,
                        sandpile.directed_graph,
                        sandpile.nodes_degrees,
                    )
                )
            else:
                # sandpile.set_graph(relax_directed(sandpile))
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
                # sandpile.set_graph(relax_directed(sandpile))
                sandpile.set_graph(cns.relax_triangular(sandpile.graph))
            else:
                # sandpile.set_graph(relax_directed(sandpile))
                sandpile.set_graph(
                    cns.relax_triangular_non_trivial_boundary(
                        sandpile.graph, sandpile.boundary
                    )
                )
    return sandpile
