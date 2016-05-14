from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pytest
import pandas as pd

from mousestyles import data
from mousestyles import path_diversity


def test_path_input():
    movement = data.load_movement(0, 0, 0)
    # checking functions raise the correct errors
    # input negative number
    with pytest.raises(ValueError) as excinfo:
        path_diversity.path_index(movement, -1, -1)
    assert excinfo.value.args[0] == "Input values need to be positive"
    # input zeros
    with pytest.raises(ValueError) as excinfo:
        path_diversity.path_index(movement, 0, 0)
    assert excinfo.value.args[0] == "Input values need to be positive"
    # min_path_length cannot be floating number
    with pytest.raises(TypeError) as excinfo:
        path_diversity.path_index(movement, 1, 1.5)
    assert excinfo.value.args[0] == "min_path_length needs to be integer"


def test_path():
    movement = {
        't': pd.Series([0.5, 0.6, 1.0, 2.5, 2.6, 2.7,
                        4.0, 4.5, 5.0, 6.0, 8.0, 8.5, 10.0]),
        'x': pd.Series([1.42, 1.96, 1.79, 1.85, 1.80, 1.98,
                        1.19, 1.30, 1.85, 1.86, 1.90, 1.76, 1.65]),
        'y': pd.Series([1.67, 1.60, 1.13, 1.95, 1.65, 1.11,
                        1.71, 1.37, 1.88, 1.97, 1.11, 1.15, 1.38])
    }

    movement = pd.DataFrame(movement)
    # Checking functions output the correct path
    paths = path_diversity.path_index(movement, 1, 1)
    assert paths == [[0, 2], [3, 5], [6, 8]]
