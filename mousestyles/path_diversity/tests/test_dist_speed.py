from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pandas as pd
import pytest


from mousestyles import data
from mousestyles.path_diversity import get_dist_speed


def test_dist_speed_input():
    movement = data.load_movement(0, 0, 0)
    # Check if function raises the correct type of errors.
    # Input negative numbers
    with pytest.raises(ValueError) as excinfo:
        get_dist_speed.get_dist_speed(movement, -1, -1)
    assert excinfo.value.args[0] == "Start and end indices must be positive"
    # Input non-integers
    with pytest.raises(TypeError) as excinfo:
        get_dist_speed.get_dist_speed(movement, 0.1, 0.1)
    assert excinfo.value.args[0] == "Start and end indices must be integers"
    # Input start index greater than end index
    with pytest.raises(ValueError) as excinfo:
        get_dist_speed.get_dist_speed(movement, 500, 2)
    assert excinfo.value.args[
        0] == "Start index must be smaller than end index"
    # Input indices that encompass data outside of true data length
    with pytest.raises(ValueError) as excinfo:
        get_dist_speed.get_dist_speed(movement, 0, len(movement))
    assert excinfo.value.args[0] == "Number of observations must be less than \
        or equal to total observations"


def test_dist_speed():
    movement = pd.DataFrame([[1, 1, 1], [2, 2, 1], [3, 2, 3]])
    movement.columns = ['t', 'x', 'y']
    # Check if function produces the correct outputs.
    dist, speed = get_dist_speed.get_dist_speed(movement, 0, 2)
    assert dist[0] == 1.0 and dist[1] == 2.0 and speed[0] == 1.0 and\
        speed[1] == 2.0
