from copy import deepcopy

import numpy as np

from nisip.sandpiles import Sandpile
import cnisip as cns


def relax_directed(sandpile: Sandpile) -> Sandpile:
    max_degree = np.max(sandpile.nodes_degrees)
    _sandpile = deepcopy(sandpile)
    while (_sandpile.graph > max_degree).any():
        mask = _sandpile.graph >= _sandpile.nodes_degrees
        pile = np.where(mask, _sandpile.graph, 0)
        _sandpile.graph = pile % _sandpile.nodes_degrees
        pile = pile // _sandpile.nodes_degrees
        _sandpile.graph[:, 1:] += pile[_sandpile.directed_graph & 1 << 0][:, 1:]
        _sandpile.graph[:, :-1] += pile[_sandpile.directed_graph & 1 << 1][:, :-1]
        _sandpile.graph[1:, :] += pile[_sandpile.directed_graph & 1 << 2][1:, :]
        _sandpile.graph[:-1, :] += pile[_sandpile.directed_graph & 1 << 3][:-1, :]
        _sandpile.graph[1:, 1:] += pile[_sandpile.directed_graph & 1 << 4][1:, 1:]
        _sandpile.graph[:-1, :-1] += pile[_sandpile.directed_graph & 1 << 5][:-1, :-1]
        _sandpile.graph[_sandpile.boundary] = 0
    return _sandpile


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
