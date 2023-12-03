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
    configuration: np.ndarray,
    _nodes_degrees: np.ndarray,
    boundary: np.ndarray,
    directed_graph: np.ndarray,
) -> np.ndarray:
    nodes_degrees = np.where(_nodes_degrees != 0, _nodes_degrees, 6)
    configuration[boundary != 0] = 0
    shift_masks = np.zeros((6, *configuration.shape), dtype=np.bool_)
    for i in range(6):
        shift_masks[i] = (directed_graph & (1 << i)) != 0
    while (configuration >= nodes_degrees).any():
        mask = configuration >= nodes_degrees
        pile = np.where(mask, configuration, 0)
        configuration[mask] = pile[mask] % nodes_degrees[mask]
        pile = pile // nodes_degrees
        shifts = mask & shift_masks
        configuration[:, 1:][shifts[0, :, :-1]] += pile[shifts[0]]
        configuration[:, :-1][shifts[1, :, 1:]] += pile[shifts[1]]
        configuration[1:, :][shifts[2, :-1, :]] += pile[shifts[2]]
        configuration[:-1, :][shifts[3, 1:, :]] += pile[shifts[3]]
        configuration[1:, 1:][shifts[4, :-1, :-1]] += pile[shifts[4]]
        configuration[:-1, :-1][shifts[5, 1:, 1:]] += pile[shifts[5]]
        configuration[boundary != 0] = 0
    configuration[_nodes_degrees == 0] = 0  # TODO: remove this line
    return configuration


def pyrelax(sandpile: Sandpile) -> Sandpile:
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
            sandpile.set_configuration(cns.relax_square(sandpile.configuration))
    elif sandpile.tiling == "triangular":
        assert sandpile.configuration.dtype == np.int64
        assert sandpile.nodes_degrees.dtype == np.int64
        assert sandpile.boundary.dtype == np.int64
        assert sandpile.graph.dtype == np.int64
        sandpile.set_configuration(
            relax_directed(
                sandpile.configuration,
                sandpile.nodes_degrees,
                sandpile.boundary,
                sandpile.graph,
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
            sandpile.set_configuration(cns.relax_square(sandpile.configuration))
    elif sandpile.tiling == "triangular":
        if sandpile.is_directed:
            if sandpile.is_trivial_boundary:
                sandpile.set_configuration(
                    cns.relax_triangular_directed_irregular(
                        sandpile.configuration,
                        sandpile.graph,
                        sandpile.nodes_degrees,
                    )
                )
            else:
                sandpile.set_configuration(
                    cns.relax_triangular_directed_irregular_non_trivial_boundary(
                        sandpile.configuration,
                        sandpile.graph,
                        sandpile.nodes_degrees,
                        sandpile.boundary,
                    )
                )
        else:
            if sandpile.is_trivial_boundary:
                sandpile.set_configuration(cns.relax_triangular(sandpile.configuration))
            else:
                sandpile.set_configuration(
                    cns.relax_triangular_non_trivial_boundary(
                        sandpile.configuration, sandpile.boundary
                    )
                )
    return sandpile
