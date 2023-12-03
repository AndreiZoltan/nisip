import os
import json
import sys
from pathlib import Path

import pytest
import numpy as np
import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(r"{}".format(parent_dir))
sys.path.append(r"{}/{}".format(parent_dir, "nisip"))


test_path = Path(__file__).parent
from sandpiles import Sandpile  # type: ignore
from core import relax, create_from_meta  # type: ignore

true_data = "true_data/"
# true_data = "isolate/"


def get_test_list():
    files = os.listdir(f"{test_path}/{true_data}/")
    relaxed = sorted([graph for graph in files if graph.startswith("relaxed_")])
    untoppled = sorted(
        [
            configuration
            for configuration in files
            if configuration.startswith("untoppled_")
        ]
    )
    graphs = sorted([graph for graph in files if graph.startswith("graph_")])
    boundary = sorted(
        [boundary for boundary in files if boundary.startswith("boundary_")]
    )
    metas = sorted([meta for meta in files if meta.startswith("meta_")])
    relaxed_id = [graph.replace("relaxed_", "") for graph in relaxed]
    relaxed_id = [graph.replace(".csv", "") for graph in relaxed_id]
    metas_id = [meta.replace("meta_", "") for meta in metas]
    metas_id = [meta.replace(".json", "") for meta in metas_id]
    assert set(relaxed_id) == set(metas_id)
    graphs = [
        graph.replace("relaxed", "graph")
        if graph.replace("relaxed", "graph") in files
        else None
        for graph in relaxed
    ]
    boundary = [
        boundary.replace("relaxed", "boundary")
        if boundary.replace("relaxed", "boundary") in files
        else None
        for boundary in relaxed
    ]
    return list(zip(relaxed, untoppled, metas, graphs, boundary))


@pytest.mark.parametrize("relaxed, untoppled, meta, graph, boundary", get_test_list())
def relax_test(relaxed, untoppled, meta, graph, boundary):
    with open(f"{test_path}/{true_data}/{meta}") as f:
        meta = json.load(f)
    if graph is not None:
        graph = np.loadtxt(
            f"{test_path}/{true_data}/{graph}",
            delimiter=",",
            dtype=np.int64,
        )
    if boundary is not None:
        boundary = np.loadtxt(
            f"{test_path}/{true_data}/{boundary}", delimiter=",", dtype=np.int64
        )
    untoppled = np.loadtxt(
        f"{test_path}/{true_data}/{untoppled}", delimiter=",", dtype=np.int64
    )
    sandpile = create_from_meta(
        meta, untoppled=untoppled, directed_graph=graph, boundary=boundary
    )
    relaxed = np.loadtxt(
        f"{test_path}/{true_data}/{relaxed}", delimiter=",", dtype=np.int64
    )
    sandpile = relax(sandpile)
    assert np.array_equal(sandpile.get_configuration(), relaxed)
