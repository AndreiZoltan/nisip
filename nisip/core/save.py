import sqlite3
import datetime
import json
import os
from pathlib import Path

nisip_path = Path(__file__).parent.parent.parent

import pickle
import numpy as np

from nisip import Sandpile
from nisip.visualization.hex_heatmap_vector import hex_heatmap_vec


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


def save(sandpile: Sandpile) -> None:
    """
    Write a sandpile to a png file.
    """
    # if directory nisip_path/dunes does not exist, create it
    dunes_path = f"{nisip_path}/dunes"
    os.makedirs(dunes_path, exist_ok=True)
    db_path = f"{dunes_path}/dunes.sqlite"
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    if not res.fetchall():
        cur.execute(
            "CREATE TABLE dunes (id INTEGER PRIMARY KEY,\
                    folder TEXT, grains INTEGER, width INTEGER, height INTEGER, tiling TEXT,\
                    is_directed BOOLEAN)"
        )
    check_integrity()
    current_time = datetime.datetime.now()
    # create folder
    folder = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    os.makedirs(f"{dunes_path}/{folder}", exist_ok=False)
    # save graph matrix
    graph_path = f"{dunes_path}/{folder}/graph.csv"
    np.savetxt(graph_path, sandpile.get_graph(), delimiter=",", fmt="%i")
    # save image
    assert ncolors(sandpile.tiling) == 6
    hex_heatmap_vec(
        graph_path, f"{dunes_path}/{folder}/graph.svg", ncolors(sandpile.tiling)
    )
    # save history as csv
    np.savetxt(f"{dunes_path}/{folder}/history.csv", sandpile.history, delimiter=",")
    with open(f"{dunes_path}/{folder}/meta.json", "w") as f:
        json.dump(sandpile.meta, f)
    cur.execute(
        """INSERT INTO dunes (folder, grains, width, height, tiling, is_directed)
               VALUES (?, ?, ?, ?, ?, ?)""",
        (
            folder,
            sandpile.grains,
            sandpile.width,
            sandpile.height,
            sandpile.tiling,
            sandpile.is_directed,
        ),
    )

    con.commit()

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
