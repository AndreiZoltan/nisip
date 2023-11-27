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
    graphs = sorted([graph for graph in files if graph.startswith("graph_")])
    untoppled_graphs = sorted(
        [graph for graph in files if graph.startswith("untoppled_")]
    )
    directed_graphs = sorted(
        [graph for graph in files if graph.startswith("directed_graph_")]
    )
    boundary = sorted(
        [boundary for boundary in files if boundary.startswith("boundary_")]
    )
    metas = sorted([meta for meta in files if meta.startswith("meta_")])
    graphs_id = [graph.replace("graph_", "") for graph in graphs]
    graphs_id = [graph.replace(".csv", "") for graph in graphs_id]
    metas_id = [meta.replace("meta_", "") for meta in metas]
    metas_id = [meta.replace(".json", "") for meta in metas_id]
    assert set(graphs_id) == set(metas_id)
    directed_graphs = [
        f"directed_{graph}" if f"directed_{graph}" in files else "" for graph in graphs
    ]
    boundary = [
        f"boundary_{'_'.join(graph.split('_')[1:])}"
        if f"boundary_{'_'.join(graph.split('_')[1:])}" in files
        else ""
        for graph in graphs
    ]
    return list(zip(graphs, untoppled_graphs, metas, directed_graphs, boundary))


@pytest.mark.parametrize(
    "graph, untoppled, meta, directed_graph, boundary", get_test_list()
)
def relax_test(graph, untoppled, meta, directed_graph, boundary):
    with open(f"{test_path}/{true_data}/{meta}") as f:
        meta = json.load(f)
    if meta["is_directed"]:
        if not meta["is_regular"]:
            directed_graph = np.loadtxt(
                f"{test_path}/{true_data}/{directed_graph}",
                delimiter=",",
                dtype=np.int64,
            )
    if not meta["is_trivial_boundary"]:
        boundary = np.loadtxt(
            f"{test_path}/{true_data}/{boundary}", delimiter=",", dtype=np.int64
        )
    untoppled = np.loadtxt(
        f"{test_path}/{true_data}/{untoppled}", delimiter=",", dtype=np.int64
    )
    sandpile = create_from_meta(
        meta, untoppled=untoppled, directed_graph=directed_graph, boundary=boundary
    )
    graph = np.loadtxt(
        f"{test_path}/{true_data}/{graph}", delimiter=",", dtype=np.int64
    )
    assert np.array_equal(sandpile.graph, graph)
