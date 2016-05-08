from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pytest
import pandas as pd

from mousestyles import data
from mousestyles.path_diversity import detect_noise
from mousestyles.path_diversity import smooth_noise
from mousestyles.path_diversity import path_index


def test_smooth_noise_input():
    movement = data.load_movement(0, 0, 0)
    paths = path_index(movement, 1, 1)
    # Check if function raises the correct type of errors.
    # Input negative angle_threshold
    with pytest.raises(ValueError) as excinfo:
        smooth_noise(movement, paths, -1, 1)
    assert excinfo.value.args[0] == "Input values need to be positive"
    # Input negative delta_t
    with pytest.raises(TypeError) as excinfo:
        smooth_noise(movement, paths, 1, -1)
    assert excinfo.value.args[0] == "Input values need to be positive"
    # Input zero angle_threshold
    with pytest.raises(ValueError) as excinfo:
        smooth_noise(movement, paths, 0, 1)
    assert excinfo.value.args[0] == "Input values need to be positive"
    # Input zero delta_t
    with pytest.raises(ValueError) as excinfo:
        smooth_noise(movement, paths, 1, 0)
    assert excinfo.value.args[0] == "Input values need to be positive"


def test_smooth_noise():
    movement = {'t': pd.Series([0., 0.02, 0.04, 0.06], index=[0, 1, 2, 3]),
                'x': pd.Series([0., 0., 0.1, 0.2], index=[0, 1, 2, 3]),
                'y': pd.Series([0., 1., 0., 1.], index=[0, 1, 2, 3]),
                'isHB': pd.Series(['No', 'No', 'No', 'No'],
                                  index=[0, 1, 2, 3])}
    movement = pd.DataFrame(movement)
    paths = path_index(movement, 1, 1)

    # Check if function produces the correct outputs.
    smoothed = smooth_noise(movement, paths, 120, 1)
    assert len(smoothed) == 3

    movement = {'t': pd.Series([0., 0.02, 0.04, 0.06], index=[0, 1, 2, 3]),
                'x': pd.Series([0., 0., 0.1, 0.2], index=[0, 1, 2, 3]),
                'y': pd.Series([0., 1., 0., 1.], index=[0, 1, 2, 3]),
                'isHB': pd.Series(['No', 'No', 'No', 'No'],
                                  index=[0, 1, 2, 3])}
    movement = pd.DataFrame(movement)
    paths = path_index(movement, 1, 1)
    # Check if function produces the correct outputs.
    smoothed = smooth_noise(movement, paths, 120, 1)
    assert smoothed['y'][1] == 0.5

    movement = {'t': pd.Series([0., 0.02, 0.04, 0.06], index=[0, 1, 2, 3]),
                'x': pd.Series([0., 0., 0.1, 0.2], index=[0, 1, 2, 3]),
                'y': pd.Series([0., 1., 0., 1.], index=[0, 1, 2, 3]),
                'isHB': pd.Series(['No', 'No', 'No', 'No'],
                                  index=[0, 1, 2, 3])}
    movement = pd.DataFrame(movement)
    paths = path_index(movement, 1, 1)
    # Check if function produces the correct outputs.
    smoothed = smooth_noise(movement, paths, 120, 1)
    assert smoothed['x'][1] == 0.05

    movement = {'t': pd.Series([0., 0.02, 0.04, 0.06], index=[0, 1, 2, 3]),
                'x': pd.Series([0., 0., 0.1, 0.2], index=[0, 1, 2, 3]),
                'y': pd.Series([0., 1., 0., 1.], index=[0, 1, 2, 3]),
                'isHB': pd.Series(['No', 'No', 'No', 'No'],
                                  index=[0, 1, 2, 3])}
    movement = pd.DataFrame(movement)
    paths = path_index(movement, 1, 1)
    # Check if function produces the correct outputs.
    smoothed = smooth_noise(movement, paths, 120, 1)
    assert smoothed['t'][1] == 0.03
