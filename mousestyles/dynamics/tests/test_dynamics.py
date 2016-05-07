from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest
import numpy as np
import pandas as pd

from mousestyles.dynamics import create_time_matrix
from mousestyles.dynamics import get_prob_matrix_list
from mousestyles.dynamics import get_prob_matrix_small_interval


def test_creat_time_matrix_input():
    # checking functions raise the correct errors for wrong input
    # time_gap is zeros
    err_string = "time_gap should be nonnegative int or float"
    with pytest.raises(ValueError) as excinfo:
        create_time_matrix(combined_gap=4, time_gap=0, days_index=137)
    assert excinfo.value.args[0] == err_string
    # time_gap is negative
    with pytest.raises(ValueError) as excinfo:
        create_time_matrix(combined_gap=4, time_gap=-1, days_index=137)
    assert excinfo.value.args[0] == err_string
    # combined_ap is negative value
    err_string = "combined_gap should be nonnegative int or float"
    with pytest.raises(ValueError) as excinfo:
        create_time_matrix(combined_gap=-1, time_gap=1, days_index=137)
    assert excinfo.value.args[0] == err_string
    # min_path_length cannot be floating number
    # days_index is negative value
    with pytest.raises(ValueError) as excinfo:
        create_time_matrix(combined_gap=4, time_gap=1, days_index=-1)
    assert excinfo.value.args[0] == "days_index should be nonnegative int"
    # days_index is float value
    with pytest.raises(ValueError) as excinfo:
        create_time_matrix(combined_gap=4, time_gap=1, days_index=0.1)
    assert excinfo.value.args[0] == "days_index should be nonnegative int"


def test_creat_time_matrix():
    # Checking functions output the correct time matrix
    matrix = create_time_matrix(combined_gap=4, time_gap=1, days_index=0)
    assert matrix.iloc[0, 2181] == 1.0


def test_get_prob_matrix_list_input():
    # checking functions raise the correct errors for wrong input
    # time_df is not DataFrame
    with pytest.raises(ValueError) as excinfo:
        get_prob_matrix_list(time_df=5, interval_length=1000)
    assert excinfo.value.args[0] == "time_df should be pandas DataFrame"
    # interval_length is 0
    row_i = np.hstack((np.zeros(13), np.ones(10),
                      np.ones(10)*2, np.ones(10)*3))
    time_df_eg = np.vstack((row_i, row_i, row_i))
    time_df_eg = pd.DataFrame(time_df_eg)
    with pytest.raises(ValueError) as excinfo:
        get_prob_matrix_list(time_df=time_df_eg, interval_length=0)
    assert excinfo.value.args[0] == "interval_length should be positive int"
    # interval_length is not int
    with pytest.raises(ValueError) as excinfo:
        get_prob_matrix_list(time_df=time_df_eg, interval_length=0.5)
    assert excinfo.value.args[0] == "interval_length should be positive int"


def test_get_prob_matrix_list():
    # Checking functions output the correct matrix list
    row_i = np.hstack((np.zeros(13), np.ones(10),
                      np.ones(10)*2, np.ones(10)*3))
    time_df_eg = np.vstack((row_i, row_i, row_i))
    time_df_eg = pd.DataFrame(time_df_eg)
    mat_list = get_prob_matrix_list(time_df_eg,
                                    interval_length=10)
    assert mat_list[0][0, 0] == 1.
    assert sum(sum(mat_list[0])) == 1.


def test_get_prob_matrix_small_interval_input():
    # checking functions raise the correct errors for wrong input
    # string_list is not list
    with pytest.raises(ValueError) as excinfo:
        get_prob_matrix_small_interval(string_list=np.array([1, 2]))
    assert excinfo.value.args[0] == "string_list should be a list"
    # items in string_list is not string
    time_list = [0, 1, 2]
    with pytest.raises(ValueError) as excinfo:
        get_prob_matrix_small_interval(string_list=time_list)
    assert excinfo.value.args[0] == "items in string_list should be str"


def test_get_prob_matrix_small_interval():
    # Checking functions output the correct matrix
    time_list = [str('002'), '001', '012']
    example = get_prob_matrix_small_interval(time_list)
    assert example[0, 0] == 0.4
    assert example[0, 1] == 0.4
    assert example[0, 2] == 0.2
    assert example[1, 2] == 1.
    assert sum(example[0, :]) == 1.
