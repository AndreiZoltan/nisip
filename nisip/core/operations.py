from copy import deepcopy
from typing import Union

import numpy as np

from nisip.sandpiles import Sandpile, DirectedSandpile
from nisip.core.relax import relax


def add(
    sandpile: Union[Sandpile, DirectedSandpile], x: int, y: int, z: int
) -> Union[Sandpile, DirectedSandpile]:
    sandpile = deepcopy(sandpile)
    sandpile.add(x, y, z)
    return sandpile
