import numpy as np


from nisip.sandpiles.sandpile import Sandpile


def imshow(sandpile: Sandpile) -> None:
    """
    Display the sandpile.
    """
    import matplotlib.pyplot as plt  # TODO : move this import to the top of the file

    if sandpile.tiling == "square":
        plt.imshow(sandpile.configuration, cmap="hot", interpolation="nearest")
        plt.show()
