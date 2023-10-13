import sqlite3
import datetime
import json
import os
import subprocess
from pathlib import Path
from copy import deepcopy

nisip_path = Path(__file__).parent.parent.parent
dunes_path = f"{nisip_path}/dunes/"

import numpy as np

from nisip.sandpiles import Sandpile, DirectedSandpile
from nisip.visualization.hex_heatmap_vector import hex_heatmap_vec
from nisip.visualization.hex_heatmap_raster import hex_heatmap_raster


def check_integrity() -> None:
    """
    Check if the database is consistent with the files in nisip_path/dunes.
    """
    pass


def ncolors(tiling: str) -> int:
    """
    Return the number of colors for a given tiling.
    """
    if tiling == "square":
        return 4
    elif tiling == "triangular":
        return 6
    elif tiling == "hexagonal":
        return 3
    else:
        raise ValueError(f"Invalid tiling: {tiling}")


def init_sqlite() -> tuple:
    os.makedirs(dunes_path, exist_ok=True)
    db_path = f"{dunes_path}/dunes.sqlite"
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    if not res.fetchall():
        cur.execute(
            "CREATE TABLE dunes (id INTEGER PRIMARY KEY,\
                    folder TEXT, grains INTEGER, rows INTEGER, cols INTEGER, tiling TEXT,\
                    is_directed BOOLEAN)"
        )
    check_integrity()
    return con, cur


def save_data(sandpile: Sandpile, folder: str = "") -> tuple:
    current_time = datetime.datetime.now()
    current = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    if not folder:
        folder = current
    os.makedirs(f"{dunes_path}/{folder}", exist_ok=True)
    graph_path = f"{dunes_path}/{folder}/graph_{current}.csv"
    np.savetxt(graph_path, sandpile.graph, delimiter=",", fmt="%i")
    if sandpile.is_directed:
        assert isinstance(sandpile, DirectedSandpile)
        if not sandpile.is_regular:
            np.savetxt(
                f"{dunes_path}/{folder}/directed_graph_{current}.csv",
                sandpile.directed_graph,
                delimiter=",",
                fmt="%i",
            )
            np.savetxt(
                f"{dunes_path}/{folder}/nodes_degrees_{current}.csv",
                sandpile.nodes_degrees,
                delimiter=",",
                fmt="%i",
            )
    if not sandpile.is_trivial_boundary:
        np.savetxt(
            f"{dunes_path}/{folder}/boundary_{current}.csv",
            sandpile.boundary,
            delimiter=",",
            fmt="%i",
        )

    np.savetxt(
        f"{dunes_path}/{folder}/history_{current}.csv",
        sandpile.history,
        delimiter=",",
        fmt="%i",
    )
    with open(f"{dunes_path}/{folder}/meta_{current}.json", "w") as f:
        json.dump(sandpile.meta, f)
    return graph_path, folder, current


def save_image(graph_path: str, folder: str = "", current: str = ""):
    # if imsave:
    #     hex_heatmap_raster(
    #         graph_path, f"{dunes_path}/{folder}/graph.png", ncolors(sandpile.tiling)
    #     )
    subprocess.run(
        [
            "Rscript",
            f"{nisip_path}/nisip/visualization/hex_heatmap_raster.R",
            graph_path,
            f"{dunes_path}/{folder}/graph_{current}.png",
        ]
    )
    # hex_heatmap_vec(
    #     graph_path, f"{dunes_path}/{folder}/graph.svg", ncolors(sandpile.tiling)
    # )
    # subprocess.run(["Rscript", f"{nisip_path}/nisip/visualization/hex_heatmap_raster.R",
    #                 graph_path, f"{dunes_path}/{folder}/graph.png"])
    # save history as csv


def update_sqlite(
    sandpile: Sandpile, folder: str, con: sqlite3.Connection, cur: sqlite3.Cursor
):
    cur.execute(
        """INSERT INTO dunes (folder, grains, rows, cols, tiling, is_directed)
               VALUES (?, ?, ?, ?, ?, ?)""",
        (
            folder,
            sandpile.grains,
            sandpile.rows,
            sandpile.cols,
            sandpile.tiling,
            sandpile.is_directed,
        ),
    )
    con.commit()


def save(sandpile: Sandpile, folder: str = "", imsave=True) -> None:
    """
    Write a sandpile to a png file.
    """
    # if directory nisip_path/dunes does not exist, create it
    assert ncolors(sandpile.tiling) == 6
    con, cur = init_sqlite()
    graph_path, folder, current = save_data(sandpile, folder)
    if imsave:
        save_image(graph_path, folder, current)
    update_sqlite(sandpile, folder, con, cur)

    # print("The image and history were saved in the directory nisip/dunes.")
    # TODO database of experiments
    # in exp folder save json with history of sand drop
    # add animation
    # write history in BaseSandpile
    # check if db exists
    # check_integrity
    # create image
    # create json and write in meta about image (when was done)
    # ns.avalanches if no: you haven't done avalanches yet
