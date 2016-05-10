from future import (absolute_import, division, print_function,
unicode_literals)

import pytest

from mousestyles import data
from mousestyles.path_diversity import path_index
from mousestyles.path_diversity import filter_path

def test_compute_advanced_input():
    # Check if function raises the correct type of errors.
    path = pd.DataFrame({'t': [2, 1, -1], 'x': [5, 3, 8],
    'y': [-3, 0, 0], 'isHB': [True, False, False]})
    # not pandas DataFrame
    like_path = [1, 2, 3]
    # not having keys 'x', 'y'
    like_path2 = pd.DataFrame(
    {'x': [5, -2, 1], 't': [-2, 3, 1], 'isHB': [True, True, False]})
    # length is less than 2
    like_path3 = pd.DataFrame({'t': [2], 'x': [5], 'y': [3], 'isHB': [True]})

    with pytest.raises(TypeError) as excinfo:
        path_features.compute_angles(like_path, True)
    assert excinfo.value.args[0] == "path_obj must be pandas DataFrame"

    with pytest.raises(ValueError) as excinfo:
        path_features.compute_angles(like_path2, True)
    assert excinfo.value.args[
        0] == "the keys of path_obj must contain 'x', 'y'"

    with pytest.raises(ValueError) as excinfo:
        path_features.compute_angles(like_path3, True)
    assert excinfo.value.args[0] == "path_obj must contain at least 2 rows"
    def test_compute_advanced():
    path = pd.DataFrame({'t': [2, 4.5, 10.5], 'x': [0, 1, 1], 'y': [
    0, 0, 1], 'isHB': [True, True, False]})
    assert path_features.compute_advanced(path['area']) == 1
    assert path_features.compute_advanced(path['abs_distance']) == 1.4142135623730951
    assert path_features.compute_advanced(path['radius']) == 0.70710678118654757