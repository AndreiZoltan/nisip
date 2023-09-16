import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import pickle

# Load your heatmap data
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
    hexagon = Polygon(hex_coords, closed=True, edgecolor='none', facecolor=col)
    plt.gca().add_patch(hexagon)

heatmap_data = np.array(heatmap_matrix).flatten()

SOM_Rows = heatmap_matrix.shape[0]
SOM_Columns = heatmap_matrix.shape[1]

# Set the output file path
output_path = "heatmap_py_vec.svg"

# Create a figure and axis for the plot
plt.figure(figsize=(8, 8))
plt.xlim(0, SOM_Columns)
plt.ylim(0, SOM_Rows)
plt.axis('off')  # Turn off axis labels and ticks

# Create a colormap similar to viridis
col_ramp = cm.get_cmap('magma', 50)(np.linspace(0, 1, 50))

# Create color mapping based on data values
bins = np.linspace(np.nanmin(heatmap_data), np.nanmax(heatmap_data), num=len(col_ramp))
color_code = [col_ramp[np.argmin(np.abs(bins - value))] if not np.isnan(value) else 'white' for value in heatmap_data]

offset = 0.5
for row in range(SOM_Rows):
    for column in range(SOM_Columns):
        hexagon(column + offset, row - 1, col=color_code[row + SOM_Rows * column])
    offset = 0 if offset else 0.5

# Save the plot as an SVG file
plt.savefig(output_path, format="svg", bbox_inches='tight', pad_inches=0)

# Display the saved plot (optional)
# plt.show()