from __future__ import (absolute_imoport, division, print_function, unicode_literals)

import pytest

from mousestyles import data
from detect_noise import detect_noise
from path_index import path_index


def test_detect_noise_input():
    movement = data.load_movement(0, 0, 0)
    paths = path_index(movement, 1, 1)
    # Check if function raises the correct type of errors.
    # Input negative angle_threshold
    with pytest.raises(ValueError) as excinfo:
        detect_noise(movement, paths, -1, 1)
    assert excinfo.value.args[0] == "Input values need to be positive"
    # Input negative delta_t
    with pytest.raises(TypeError) as excinfo:
        detect_noise(movement, paths, 1, -1)
    assert excinfo.value.args[0] == "Input values need to be positive"
    # Input zero angle_threshold
    with pytest.raises(ValueError) as excinfo:
        detect_noise(movement, paths, 0, 1)
    assert excinfo.value.args[0] == "Input values need to be positive"
    # Input zero delta_t
    with pytest.raises(ValueError) as excinfo:
        detect_noise(movement, paths, 1, 0)
    assert excinfo.value.args[0] == "Input values need to be positive"


def test_detect_noise():
    movement = data.load_movement(1, 2, 1)
    paths = path_index(movement, 1, 1)
    # Check if function produces the correct outputs.
    noise = detect_noise(movement, paths, 135, 0.08)
    assert noise[0:9] == [0, 0, 0, 0, 0, 0, 0,  1,  1]
    
