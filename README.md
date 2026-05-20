# nisip

`nisip` is a high-performance Python package for simulating Abelian Sandpile Models on various grid structures (square, triangular, and hexagonal). It features a C extension (`cnisip`) to efficiently compute sandpile relaxations and topplings.

## Features

- **Multiple Tilings:** Support for square, triangular, and hexagonal grid topologies.
- **Fast C Backend:** Sandpile relaxation (toppling) is implemented as a C extension for maximum performance.
- **Custom Boundaries & Graphs:** Support for directed/undirected graphs and custom boundary conditions.
- **Group Operations:** Built-in operations corresponding to the Abelian Sandpile Group (addition, multiplication).
- **Visualization:** Tools for plotting and visualizing the configurations in regular and hexagonal grids, both as rasters and vectors.

## Installation

You can install `nisip` from source. It requires a C compiler and NumPy to build the extension.

```bash
git clone https://github.com/AndreiZoltan/sandpile.git
cd sandpile
pip install .
```

To install the requirements for documentation and testing:
```bash
pip install -r requirements.txt
pip install -r docs/requirements.txt
```

## Quick Start

```python
import numpy as np
from nisip.sandpiles.sandpile import Sandpile

# Create a 20x20 sandpile on a square grid
pile = Sandpile(shape=(20, 20), tiling="square")

# Add 100 grains of sand to the center
pile.add(10, 10, 100)

# The sandpile can be relaxed using the core tools (internally calls the C extension bindings)
from nisip.core.relax import relax
relax(pile)

# Get the current configuration
config = pile.get_configuration()
print(config)
```

## Testing

Tests are written using `pytest`. You can run them simply via:

```bash
pytest tests/
```

This will run all functional and true-data validation tests.

## License

This project is licensed under the GPLv2 License. See the `LICENSE` file for details.
