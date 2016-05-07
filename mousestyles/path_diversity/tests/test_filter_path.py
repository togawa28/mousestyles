from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

from mousestyles import data
from mousestyles.path_diversity import path_index
from mousestyles.path_diversity import filter_path


def test_filter_path_input():
    movement = data.load_movement(0, 0, 0)
    paths = path_index(movement, 1, 1)
    # checking functions raise the correct errors
    # input negative number
    with pytest.raises(ValueError) as excinfo:
        filter_path.filter_paths(movement, paths, -1)
    assert excinfo.value.args[0] == "Input values need to be positive"
    # input zeros
    with pytest.raises(ValueError) as excinfo:
        filter_path.filter_paths(movement, paths, 0)
    assert excinfo.value.args[0] == "Input values need to be positive"


def test_filter_path():
    movement = data.load_movement(0, 0, 0)
    paths = path_index(movement, 1, 1)
    # Checking functions output the correct path
    pass_paths = filter_path.filter_paths(movement, paths, 20)
    assert pass_paths == [[3082, 3181], [30835, 30970], [31346, 31557]]
