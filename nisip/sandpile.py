import numpy as np

class Sandpile:
    def __init__(self, size, tiling='triangle') -> None:
        self.size = size
        self.grid = np.zeros((size, size), dtype=np.int32)
        if tiling not in ['triangle', 'square']:
            raise ValueError("Tiling must be either 'triangle'\
                              or 'square'.")
        self.tiling = tiling

    def __repr__(self) -> str:
        return f"Sandpile(size={self.size}, tiling='{self.tiling}')"
    
    def set(self, x: int, y: int, z: int) -> None:
        """
        Set the number of grains at (x, y) to z.
        """
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            raise IndexError("Invalid coordinates.")
        if z < 0:
            raise ValueError("Cannot set negative number of grains.")
        self.grid[x, y] = z

    def get(self, x: int, y: int) -> int:
        """
        Return the number of grains at (x, y).
        """
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            raise IndexError("Invalid coordinates.")
        return self.grid[x, y]