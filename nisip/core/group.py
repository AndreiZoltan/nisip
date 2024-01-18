from copy import deepcopy

import numpy as np

import nisip as ns


def identity(sandpile: ns.Sandpile, check: bool = True) -> np.ndarray:
    sandpile = deepcopy(sandpile)
    max_recurent = sandpile.max_recurrent
    sandpile.set_configuration(2 * max_recurent)
    sandpile = ns.relax(sandpile)
    sandpile.set_configuration(2 * max_recurent - sandpile.configuration)
    zero_sandpile = ns.relax(sandpile)
    if check:
        assert zero_sandpile == ns.relax(zero_sandpile * 2)
    return zero_sandpile.configuration
