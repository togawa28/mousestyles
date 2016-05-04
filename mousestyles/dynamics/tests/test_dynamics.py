from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest

from mousestyles.dynamics import create_time_matrix


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
