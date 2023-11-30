from copy import deepcopy

import numpy as np

# from numba import jit
# import taichi as ti
# ti.init(arch=ti.cpu)

from nisip.sandpiles import Sandpile
import cnisip as cns


# @jit(nopython=True)
# @ti.func
def relax_directed(
    graph: np.ndarray,
    _nodes_degrees: np.ndarray,
    boundary: np.ndarray,
    directed_graph: np.ndarray,
) -> np.ndarray:
    nodes_degrees = np.where(_nodes_degrees != 0, _nodes_degrees, 6)
    graph[boundary != 0] = 0
    shift_masks = np.zeros((6, *graph.shape), dtype=np.bool_)
    for i in range(6):
        shift_masks[i] = (directed_graph & (1 << i)) != 0
    while (graph >= nodes_degrees).any():
        mask = graph >= nodes_degrees
        pile = np.where(mask, graph, 0)
        graph[mask] = pile[mask] % nodes_degrees[mask]
        pile = pile // nodes_degrees
        shifts = mask & shift_masks
        graph[:, 1:][shifts[0, :, :-1]] += pile[shifts[0]]
        graph[:, :-1][shifts[1, :, 1:]] += pile[shifts[1]]
        graph[1:, :][shifts[2, :-1, :]] += pile[shifts[2]]
        graph[:-1, :][shifts[3, 1:, :]] += pile[shifts[3]]
        graph[1:, 1:][shifts[4, :-1, :-1]] += pile[shifts[4]]
        graph[:-1, :-1][shifts[5, 1:, 1:]] += pile[shifts[5]]
        graph[boundary != 0] = 0
    graph[_nodes_degrees == 0] = 0  # TODO: remove this line
    return graph


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
        assert sandpile.graph.dtype == np.int64
        assert sandpile.nodes_degrees.dtype == np.int64
        assert sandpile.boundary.dtype == np.int64
        assert sandpile.directed_graph.dtype == np.int64
        sandpile.set_graph(
            relax_directed(
                sandpile.graph,
                sandpile.nodes_degrees,
                sandpile.boundary,
                sandpile.directed_graph,
            )
        )
    return sandpile


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
