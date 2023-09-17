from argparse import ArgumentParser

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
import matplotlib.cm as cm

def build_argparser():
    parser = ArgumentParser()
    parser.prog = "hex heatmap vector (slow)"
    parser.add_argument(
        "--data", type=str, help="path to the pickle file with data", required=True
    )
    parser.add_argument(
        "--output", type=str, help="path to the output svg file", required=True
    )
    return parser

def hexagon(x, y, unitcell=1, col="white"):
    """Draw a hexagon at coordinates (x, y) with the given color."""
    h = np.sqrt(3) / 2 * unitcell
    hex_coords = [
        (x, y - h/2),
        (x + unitcell/2, y - h),
        (x + unitcell, y - h/2),
        (x + unitcell, y + h/2),
        (x + unitcell/2, y + h),
        (x, y + h/2)
    ]
    hexagon = Polygon(hex_coords, closed=True, edgecolor='none', facecolor=col) # type: ignore
    plt.gca().add_patch(hexagon)

def hex_heatmap_vec(graph_path, output_path) -> None:
    heatmap_matrix = np.loadtxt(graph_path, delimiter=",")
    heatmap_data = np.array(heatmap_matrix).flatten()

    SOM_Rows = heatmap_matrix.shape[0]
    SOM_Columns = heatmap_matrix.shape[1]

    plt.figure(figsize=(8, 8))
    plt.xlim(0, SOM_Columns)
    plt.ylim(0, SOM_Rows)
    plt.axis('off')

    col_ramp = cm.get_cmap('magma', 50)(np.linspace(0, 1, 50))

    bins = np.linspace(np.nanmin(heatmap_data), np.nanmax(heatmap_data), num=len(col_ramp))
    color_code = [col_ramp[np.argmin(np.abs(bins - value))] if not np.isnan(value) else 'white' for value in heatmap_data]

    offset = 0.5
    for row in range(SOM_Rows):
        for column in range(SOM_Columns):
            hexagon(column + offset, row - 1, col=color_code[row + SOM_Rows * column])
        offset = 0 if offset else 0.5

    plt.savefig(output_path, format="svg", bbox_inches='tight', pad_inches=0)