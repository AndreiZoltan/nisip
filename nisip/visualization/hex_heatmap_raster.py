import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import pickle


def hexagon(x, y, unitcell=1, col="white"):
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
    hexagon = Polygon(hex_coords, closed=True, edgecolor="g", facecolor=col)  # type: ignore
    plt.gca().add_patch(hexagon)


def matrix2color(matrix: np.array, colormap: str = "viridis") -> np.array:
    col_ramp = cm.get_cmap("viridis")
    matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))
    return col_ramp(matrix)


def hex_heatmap_raster(graph_path, output_path, ncolors=6) -> None:
    heatmap = np.loadtxt(graph_path, delimiter=",", dtype=int)
    height, width = heatmap.shape

    plt.figure(figsize=(15, 15))
    plt.xlim(-0.2, width * 1.5)
    plt.ylim(-1.5 * height, height + 0.2)
    plt.axis("off")

    # col_ramp = cm.get_cmap("magma", 50)(np.linspace(0, 1, 50))
    # norm = plt.Normalize(vmin=np.nanmin(heatmap), vmax=np.nanmax(heatmap))  # type: ignore
    # color_mapper = cm.ScalarMappable(norm=norm, cmap="Oranges")
    heatmap = matrix2color(heatmap)

    offset = 0
    for row in reversed(range(height)):
        for column in range(width):
            color = heatmap[row, column]
            x, y = column + offset, row
            hexagon(x, -y, col=color)
        offset += 0.5

    plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0)
