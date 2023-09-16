import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import pickle

heatmap_matrix = pickle.load(open("./random.pkl", "rb"))

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

heatmap_data = np.array(heatmap_matrix)

SOM_Rows = heatmap_matrix.shape[0]
SOM_Columns = heatmap_matrix.shape[1]

output_path = "heatmap_py.png"

plt.figure(figsize=(8, 8))
plt.xlim(0, SOM_Columns)
plt.ylim(0, SOM_Rows)
plt.axis('off')

col_ramp = cm.get_cmap('magma', 50)(np.linspace(0, 1, 50))
norm = plt.Normalize(vmin=np.nanmin(heatmap_data), vmax=np.nanmax(heatmap_data)) # type: ignore
color_mapper = cm.ScalarMappable(norm=norm, cmap='Oranges')

offset = 0.5
for row in range(SOM_Rows):
    for column in range(SOM_Columns):
        value = heatmap_data[row, column]
        if not np.isnan(value):
            color = color_mapper.to_rgba(value)
            hexagon(column + offset, row - 1, col=color) # type: ignore
    offset = 0 if offset else 0.5

plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0)
