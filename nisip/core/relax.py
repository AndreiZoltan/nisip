import os
from copy import deepcopy

import numpy as np
import taichi as ti

import nisip as ns

device = 3
os.environ["CUDA_VISIBLE_DEVICES"] = str(device)
ti.init(arch=ti.cuda, advanced_optimization=True)

from nisip.sandpiles import Sandpile
import cnisip as cns

arr_type = ti.types.ndarray(dtype=ti.i32, ndim=2)
@ti.kernel
def has_all_non_boundary_values_less_than_4(arr: ti.i32) -> ti.i32: # type: ignore
    result = 1
    for I in ti.grouped(arr):
        if 0 < I[0] < arr.shape[0] - 1 and 0 < I[1] < arr.shape[1] - 1:
            if arr[I] >= 4:
                result = 0
    return result

@ti.kernel
def tairelax_directed(configuration: ti.i32, nodes_degrees: ti.i32, boundary: ti.i32, graph: ti.i32):
    for i, j in configuration:
        if boundary[i, j] == 0 and nodes_degrees[i, j] != 0 and configuration[i, j] >= nodes_degrees[i, j]:
            pile = configuration[i, j] // nodes_degrees[i, j]
            configuration[i, j] %= nodes_degrees[i, j]
            if graph[i, j] & (1 << 0):
                configuration[i, j + 1] += pile
            if graph[i, j] & (1 << 1):
                configuration[i, j - 1] += pile
            if graph[i, j] & (1 << 2):
                configuration[i + 1, j] += pile
            if graph[i, j] & (1 << 3):
                configuration[i - 1, j] += pile
            if graph[i, j] & (1 << 4):
                configuration[i + 1, j + 1] += pile
            if graph[i, j] & (1 << 5):
                configuration[i - 1, j - 1] += pile
            # Can simplify with something like this:
            # directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]
            # for k, dx, dy in enumerate(directions):
            #     if graph[i, j] & (1 << k):
            #         configuration[i + dx, j + dy] += pile


def tairelax(sandpile: Sandpile, device: int = 0) -> Sandpile:
    sandpile = deepcopy(sandpile)
    os.environ["CUDA_VISIBLE_DEVICES"] = str(device)
    ti.init(arch=ti.cuda, advanced_optimization=True)
    configuration = ti.field(dtype=ti.int32, shape=sandpile.shape)
    nodes_degrees = ti.field(dtype=ti.int32, shape=sandpile.shape)
    boundary = ti.field(dtype=ti.int32, shape=sandpile.shape)
    graph = ti.field(dtype=ti.int32, shape=sandpile.shape)
    configuration.from_numpy(sandpile.configuration.astype(np.int32))
    nodes_degrees.from_numpy(sandpile.nodes_degrees.astype(np.int32))
    boundary.from_numpy(sandpile.boundary.astype(np.int32))
    graph.from_numpy(sandpile.graph.astype(np.int32))
    tairelax_directed(configuration, nodes_degrees, boundary, graph)
    sandpile.set_configuration(configuration.to_numpy())
    return sandpile


@ti.kernel
def tai_sym_square(configuration: ti.template(), n: int, m: int) -> ti.i32: # type: ignore
# def tai_sym_square(configuration: arr_type, n: int, m: int) -> ti.i32: # type: ignore
    k: ti.i32 = 0
    for i, j in configuration:  # Parallelized over all pixels
        if configuration[i, j] >= 4 and 0 < i < n - 1 and 0 < j < m - 1:
            k = 1
            pile = configuration[i, j] // 4
            configuration[i, j] -= pile * 4
            configuration[i+1, j] += pile
            configuration[i-1, j] += pile
            configuration[i, j+1] += pile
            configuration[i, j-1] += pile
    return k

def calc_identity(shape: tuple, tiling: int = ns.SQUARE, device: int = 0) -> np.ndarray:
    if tiling == ns.SQUARE:
        new_shape = shape
        height, width = new_shape
        configuration = ti.field(dtype=ti.i32, shape=new_shape)
        configuration.fill(6)
        while tai_sym_square(configuration, height, width):
            pass
        boundary = np.ones(shape, dtype=np.int32)
        boundary[::shape[0]-1] = 0
        boundary[:, ::shape[1]-1] = 0
        configuration.from_numpy(configuration.to_numpy()*boundary)
        sixies = np.full(shape, 6, dtype=np.int32)*boundary
        id_configuration = ti.field(dtype=ti.i32, shape=shape)
        id_configuration.from_numpy(sixies - configuration.to_numpy())
        while tai_sym_square(id_configuration, height, width):
            pass
        return id_configuration.to_numpy()
    else:
        raise NotImplementedError


def relax_directed(
    configuration: np.ndarray,
    _nodes_degrees: np.ndarray,
    boundary: np.ndarray,
    graph: np.ndarray,
) -> np.ndarray:
    nodes_degrees = np.where(_nodes_degrees != 0, _nodes_degrees, 6)
    boundary = np.where(boundary, 0, 1)
    configuration = configuration * boundary
    shift_masks = np.zeros((6, *configuration.shape), dtype=np.bool_)
    for i in range(6):
        shift_masks[i] = (graph & (1 << i)) != 0
    while (mask := configuration >= nodes_degrees).any():
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
        configuration = configuration * boundary
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
            sandpile.set_configuration(
                cns.relax_triangular_directed_irregular_non_trivial_boundary(
                    sandpile.configuration,
                    sandpile.graph,
                    sandpile.nodes_degrees,
                    sandpile.boundary,
                )
            )
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
