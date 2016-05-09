from __future__ import print_function, absolute_import, division

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import chi2
import statsmodels
import mousestyles.ultradian as ultradian
import pytest
import mousestyles.data as data

# aggregate_interval test


def test_aggregate_interval():
    with pytest.raises(ValueError) as msg1:
        ultradian.aggregate_interval(-1, 1, "M_IS", 30)
    assert msg1.value.args[0] == 'Strain must be a non-negative integer'

    with pytest.raises(ValueError) as msg2:
        ultradian.aggregate_interval(1, -1, "M_IS", 30)
    assert msg2.value.args[0] == 'Mouse value must be a non-negative integer'

    with pytest.raises(ValueError) as msg3:
        ultradian.aggregate_interval(1, 1, "A", 30)
    right_msg_1 = 'Input value must in {"AS", "F", M_AS", "M_IS", "W"}'
    assert msg3.value.args[0] == right_msg_1

    with pytest.raises(ValueError) as msg4:
        ultradian.aggregate_interval(1, 1, "M_IS", -30)
    right_msg = 'Bin width (minutes) must be a non-negative integer below 1440'
    assert msg4.value.args[0] == right_msg
    result = ultradian.aggregate_interval(0, 1, "AS", 30)
    assert type(result) is pd.core.series.Series
    assert all(result >= 0) is True


# Testforaggregate_movement
def test_aggregate_movement():
    with pytest.raises(ValueError) as msg1:
        ultradian.aggregate_movement(-1, 1, 30)
    assert msg1.value.args[0] == 'Strain must be a non-negative integer'

    with pytest.raises(ValueError) as msg2:
        ultradian.aggregate_movement(1, -1, 30)
    assert msg2.value.args[0] == 'Mouse value must be a non-negative integer'

    with pytest.raises(ValueError) as msg3:
        ultradian.aggregate_movement(1, 1, -30)
    assert msg3.value.args[
        0] == 'Bin width (minutes) must be a non-negative integer below 1440'
# Check the outcome data type of function aggregate_movement()
    result = ultradian.aggregate_movement(0, 1, 30)
    assert type(result) is pd.core.series.Series


# Test for aggregate_data
def test_aggregate_data(feature="AS", bin_width=30):
    result = ultradian.aggregate_data(feature, bin_width)
    assert type(result) is pd.core.frame.DataFrame
# Check the columns
    n = len(result.columns)
    assert n == 4
# Check the hours
    test_1 = np.array(result['hour'])
    assert test_1.max() < 24
# Check the strain
    test_2 = np.array(result['strain'])
    assert len(np.unique(test_2)) == 3


# Test for seasonal decomposition
def test_seasonal_decomposition(strain=0, mouse=1, feature='AS',
                                bin_width=30, period_length=10):
    result = ultradian.seasonal_decomposition(strain,
                                    mouse, feature, bin_width, period_length)
    assert type(result) == statsmodels.tsa.seasonal.DecomposeResult


# Test for strai_seasonal
def test_strain_seasonal():
    res = ultradian.strain_seasonal(strain=0, mouse={0, 1, 2}, feature="W",
                          bin_width=30, period_length=24)
    assert type(res) == tuple
    assert len(res) == 2


# check the outcome range of mix_strain, the result is a p-value, so it's
# between 0 and 1

def test_mix_strain(data):
    data = ultradian.aggregate_data("AS", 30)
    result = ultradian.mix_strain(data, "AS")
    assert result > 0
    assert result < 1

