"""Standard test data.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

import mousestyles.data as data
import numpy as np
import pandas as pd


def test_all_features_loader():
    # Checking load_all_features returns a data frame of the correct dimension
    all_features = data.load_all_features()
    assert all_features.shape == (21131, 13)


def test_mouseday_features_loader():
    # Checking load_mouseday_features returns a data frame of
    # the correct dimension
    mouseday_features1 = data.load_mouseday_features(["Food", "Water",
                                                      "Distance"])
    mouseday_features2 = data.load_mouseday_features(["Food", "Water"])
    mouseday_features3 = data.load_mouseday_features()
    assert mouseday_features1.shape == (1921, 36)
    assert mouseday_features2.shape == (1921, 25)
    assert mouseday_features3.shape == (1921, 102)


def test_intervals_loader():
    # Checking load_intervals returns a data frame of the correct dimension
    AS = data.load_intervals('AS')
    assert AS.shape == (1343, 5)


def test_movement_loader():
    # Checking load_movement returns a data frame of the correct dimension
    movement = data.load_movement(0, 0, 0)
    assert movement.shape == (39181, 4)


def test_feature_load_input():
    # checking functions raise the correct errors
    with pytest.raises(ValueError) as excinfo:
        data.load_intervals('A')
    msg = 'Input value must be one of {"AS", "F", "IS", "M_AS", "M_IS", "W"}'
    assert excinfo.value.args[0] == msg

    with pytest.raises(ValueError) as excinfo:
        data.load_movement(-1, 0, 0)
    assert excinfo.value.args[0] == "Input values need to be nonnegative"

    with pytest.raises(TypeError) as excinfo:
        data.load_movement(0.0, 0, 0)
    assert excinfo.value.args[0] == "Input values need to be integer"

    with pytest.raises(ValueError) as excinfo:
        data.load_movement(1000, 1000, 1000)
    expected = "No data exists for strain 1000, mouse 1000, day 1000"
    assert excinfo.value.args[0] == expected


def test_mouseday_load_input():
    with pytest.raises(ValueError) as excinfo:
        data.load_mouseday_features(["Food", "Water", "Distances"])
    fea_list = ["ASProbability", "ASNumbers", "ASDurations",
                "Food", "Water", "Distance",
                "ASFoodIntensity", "ASWaterIntensity", "MoveASIntensity"]
    fea_str = "{"
    for item in fea_list:
        fea_str += '"' + item + '", '
    fea_str = fea_str[:-2] + "}"
    expected1 = "Input value must be chosen from " + fea_str + "."
    assert excinfo.value.args[0] == expected1

    with pytest.raises(TypeError) as excinfo:
        data.load_mouseday_features(("Food", "Water", "Distances"))
    expected2 = "Input value must be a list."
    assert excinfo.value.args[0] == expected2


def test_lookup_intervals():
    t = pd.Series([1.5, 2.5, 3.5])
    ints = pd.DataFrame({'start': [1, 2], 'stop': [1.99, 2.99]})
    in_intervals = data._lookup_intervals(t, ints)
    assert t.shape == in_intervals.shape
    assert np.all(in_intervals == pd.Series([True, True, False]))


def test_load_movement_and_intervals():
    m1 = data.load_movement(1, 1, 1)
    m2 = data.load_movement_and_intervals(
        1, 1, 1, [])  # don't add any features
    assert np.all(m1 == m2)
    m3 = data.load_movement_and_intervals(1, 1, 1, ['AS'])
    m4 = data.load_movement_and_intervals(1, 1, 1, 'AS')
    assert m3.shape[1] == m1.shape[1] + 1  # adds one column
    assert m3.shape[0] == m1.shape[0]  # same number of rows
    assert np.all(m3 == m4)


def test_load_movement_and_intervals_error():
    with pytest.raises(ValueError) as excinfo:
        # bad value for `features`
        data.load_movement_and_intervals(1, 1, 1, 10)
    expected = "features must be a string or iterable of strings"
    assert excinfo.value.args[0] == expected


def test_start_time_end_time_loader():
    # Test for strain 0, mouse 0, day 0
    times = data.load_start_time_end_time(0, 0, 0)
    assert len(times) == 2
    assert times[1] - times[0] > 0
