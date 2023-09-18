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
# sys.path.append('***REMOVED***')
# sys.path.append('***REMOVED***/tests')
# sys.path.append('***REMOVED***/nisip')
# sys.path.append('***REMOVED***/nisip/sandpiles')
# from nisip import Sandpile, drop_sand
from sandpiles import Sandpile # type: ignore
from core import drop_sand # type: ignore
# from nisip import save
files = os.listdir(f"{test_path}/true_data")
graphs = sorted([graph for graph in files if graph.startswith("graph_")])
metas = sorted([meta for meta in files if meta.startswith("meta_")])
graphs_id = [graph.replace("graph_", "") for graph in graphs]
graphs_id = [graph.replace(".csv", "") for graph in graphs_id]
metas_id = [meta.replace("meta_", "") for meta in metas]
metas_id = [meta.replace(".json", "") for meta in metas_id]
assert set(graphs_id) == set(metas_id)
test_list = list(zip(graphs, metas))


def create_from_meta(meta: dict) -> Sandpile:
    """
    Create a sandpile from a metadata dictionary.
    """
    sandpile = Sandpile(int(meta["width"]), 
                        int(meta["height"]), meta["tiling"])
    for x, y, z in np.array(meta["history"], dtype=np.int64):
        sandpile = drop_sand(sandpile, x, y, z)
    return sandpile


@pytest.mark.parametrize(
    "graph, meta", test_list
)
def drop_sand_test(graph, meta):
    graph = np.loadtxt(f"{test_path}/true_data/{graph}", delimiter=",")
    with open(f"{test_path}/true_data/{meta}") as f:
        meta = json.load(f)
    sandpile = create_from_meta(meta)
    assert np.array_equal(sandpile.graph, graph)

@pytest.mark.parametrize(
    "width, height, tiling, x, y, z",
    [
        [3, 3, "square", 1, 1, 10],
    ],
)
def drop_sand_boundary_test(width, height, tiling, x, y, z):
    if tiling == "square":
        max_grain = 3
    elif tiling == "triangular":
        max_grain = 5
    else:
        max_grain = 2
    sand = Sandpile(width, height, tiling)
    sand = drop_sand(sand, x, y, z)
    assert np.max(sand.graph) <= max_grain
    assert np.max(sand.graph[0]) == 0
    assert np.max(sand.graph[-1]) == 0
    assert np.max(sand.graph[:, 0]) == 0
    assert np.max(sand.graph[:, -1]) == 0
