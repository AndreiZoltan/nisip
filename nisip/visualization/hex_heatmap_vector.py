from argparse import ArgumentParser

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
import matplotlib.cm as cm


def build_argparser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.prog = "hex heatmap vector (slow)"
    parser.add_argument(
        "--data", type=str, help="path to the pickle file with data", required=True
    )
    parser.add_argument(
        "--output", type=str, help="path to the output svg file", required=True
    )
    return parser


def hexagon(x: float, y: float, color: list, unitcell=1):
    """Draw a hexagon at coordinates (x, y) with the given color."""
    h = np.sqrt(3) / 2 * unitcell
    hex_coords = [
        (x, y - h / 2),
        (x + unitcell / 2, y - h),
        (x + unitcell, y - h / 2),
        (x + unitcell, y + h / 2),
        (x + unitcell / 2, y + h),
        (x, y + h / 2),
    ]
    hexagon_ = Polygon(hex_coords, closed=True, edgecolor="g", facecolor=color)  # type: ignore
    plt.gca().add_patch(hexagon_)


def matrix2color(matrix: npt.NDArray, colormap: str = "viridis") -> npt.NDArray:
    col_ramp = cm.get_cmap("viridis")
    matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))
    return col_ramp(matrix) # type: ignore


def hex_heatmap_vec(graph_path: str, output_path: str, ncolors=6) -> None:
    heatmap = np.loadtxt(graph_path, delimiter=",", dtype=int)

    height, width = heatmap.shape

    plt.figure(figsize=(20, 20))
    plt.xlim(0, height)
    plt.ylim(0, width)
    plt.axis("off")

    heatmap = matrix2color(heatmap)
    # offset = 0.5*height
    offset = 0
    for row in range(width):
        for column in range(height):
            hexagon(column + offset, row, heatmap[row, column])
        # offset -= 0.5
        offset += 0.5

    plt.savefig(output_path, format="svg", bbox_inches="tight", pad_inches=0)
