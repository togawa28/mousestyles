from __future__ import print_function, absolute_import, division

import numpy as np
import pandas as pd
import statsmodels
import mousestyles.ultradian as ultradian
import pytest


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
    right_msg_1 = 'Input value must in {"AS", "F", "M_AS", "M_IS", "W"}'
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
def test_aggregate_data():
    result = ultradian.aggregate_data(feature='AS', bin_width=30)
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
    # check input error
    with pytest.raises(ValueError) as msg1:
        ultradian.aggregate_data(feature='hehe', bin_width=30)
    assert msg1.value.args[0] == \
        'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}'
    # check input error
    with pytest.raises(ValueError) as msg2:
        ultradian.aggregate_data(feature='F', bin_width=-30)
    assert msg2.value.args[
        0] == 'Bin width (minutes) must be a non-negative integer below 1440'


# Test for seasonal decomposition
def test_seasonal_decomposition():
    result = ultradian.seasonal_decomposition(strain=0, mouse=1, feature='AS',
                                              bin_width=30, period_length=10)
    assert type(result) == statsmodels.tsa.seasonal.DecomposeResult
    # check input error
    with pytest.raises(ValueError) as msg1:
        ultradian.seasonal_decomposition(strain=-5, mouse=1, feature='AS',
                                         bin_width=30, period_length=10)
    assert msg1.value.args[0] == 'Strain must be a non-negative integer'
    # check input error
    with pytest.raises(ValueError) as msg2:
        ultradian.seasonal_decomposition(strain=0, mouse=-1, feature='AS',
                                         bin_width=30, period_length=10)
    assert msg2.value.args[0] == 'Mouse value must be a non-negative integer'
    # check input error
    with pytest.raises(ValueError) as msg3:
        ultradian.seasonal_decomposition(strain=0, mouse=1, feature='hehe',
                                         bin_width=30, period_length=10)
    assert msg3.value.args[0] == \
        'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}'
    # check input error
    with pytest.raises(ValueError) as msg4:
        ultradian.seasonal_decomposition(strain=0, mouse=1, feature='AS',
                                         bin_width=-30, period_length=10)
    assert msg4.value.args[
        0] == 'Bin width (minutes) must be a non-negative integer below 1440'
    # check input error
    with pytest.raises(ValueError) as msg5:
        ultradian.seasonal_decomposition(strain=0, mouse=1, feature='AS',
                                         bin_width=30, period_length=-10)
    assert msg5.value.args[
        0] == 'Peoriod length must be a non-negative integer or float'


# Test for strai_seasonal
def test_strain_seasonal():
    res = ultradian.strain_seasonal(strain=0, mouse={0, 1, 2}, feature="W",
                                    bin_width=30, period_length=24)
    assert len(res) == 3
    # check input error
    with pytest.raises(ValueError) as msg1:
        ultradian.strain_seasonal(strain=-5, mouse={0, 1}, feature='AS',
                                  bin_width=30, period_length=10)
    assert msg1.value.args[0] == 'Strain must be a non-negative integer'
    # check input error
    with pytest.raises(ValueError) as msg2:
        ultradian.strain_seasonal(strain=0, mouse={1, -1}, feature='AS',
                                  bin_width=30, period_length=10)
    assert msg2.value.args[0] == 'Mouse value must be a non-negative integer'
    # check input error
    with pytest.raises(ValueError) as msg3:
        ultradian.strain_seasonal(strain=0, mouse={0, 1}, feature='hehe',
                                  bin_width=30, period_length=10)
    assert msg3.value.args[0] == \
        'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}'
    # check input error
    with pytest.raises(ValueError) as msg4:
        ultradian.strain_seasonal(strain=0, mouse={0, 1}, feature='AS',
                                  bin_width=-30, period_length=10)
    assert msg4.value.args[
        0] == 'Bin width (minutes) must be a non-negative integer below 1440'
    # check input error
    with pytest.raises(ValueError) as msg5:
        ultradian.strain_seasonal(strain=0, mouse={0, 1}, feature='AS',
                                  bin_width=30, period_length=-10)
    assert msg5.value.args[
        0] == 'Peoriod length must be a non-negative integer or float'


# check the outcome range of mix_strain, the result is a p-value, so it's
# between 0 and 1
def test_mix_strain():
    data = ultradian.aggregate_data("AS", 30)
    result = ultradian.mix_strain(data, "AS")
    assert result > 0
    assert result < 1
    # check input error
    with pytest.raises(ValueError) as msg1:
        ultradian.mix_strain([0, 1], 'W')
    assert msg1.value.args[0] == 'Data must be a pandas data frame'
    # check input error
    with pytest.raises(ValueError) as msg2:
        ultradian.mix_strain(data, 'hehe')
    assert msg2.value.args[0] == \
        'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}'


# Test for find_cycle
def test_find_cycle():
    # check the length of returned values
    result = ultradian.find_cycle(feature='Distance', strain=0, mouse=0,
                                  methods='LombScargleFast',
                                  plot=False, gen_doc=False)
    assert len(result) == 3
    assert len(result[0]) == 10
    # check the gen_doc option, which prepares data for plotting
    r2 = ultradian.find_cycle(feature='Distance', strain=0, mouse=0,
                              methods='LombScargleFast',
                              plot=False, gen_doc=True)
    assert len(r2) == 7
    assert type(r2[3]) == int
    assert all(r2[6] <= 1) & all(r2[4] > 0)
    # check search_range_fit option
    r3 = ultradian.find_cycle(feature='Distance', strain=0, mouse=0,
                              methods='LombScargleFast',
                              plot=False,
                              search_range_fit=np.arange(3, 15, 0.1))
    assert len(r3) == 3
    assert len(r3[0]) == 10
    assert all(r3[1] >= 0)
    assert all(r3[2] <= 1)
    # check methods LombScargle and disturb_t option
    r4 = ultradian.find_cycle(feature='Distance', strain=0, mouse=0,
                              methods='LombScargle', disturb_t=True,
                              plot=False)
    assert len(r4) == 3
    assert all(r4[2] <= 1) & all(r4[1] >= 0)
    assert len(r4[0]) == 10
    # check mouse==None option
    r5 = ultradian.find_cycle(feature='AS', strain=0,
                              methods='LombScargleFast',
                              plot=False, search_range_find=[3, 10])
    assert len(r5) == 3
    assert all(r5[0] >= 0) & all(r5[0] <= 48)
    assert all(r5[1] >= 0) & all(r5[2] <= 1)
    # check bin_width option
    r6 = ultradian.find_cycle(feature='AS', strain=0, bin_width=45,
                              methods='LombScargleFast',
                              plot=False, gen_doc=True)
    assert len(r6) == 7
    assert type(r6[3]) == int
    assert all(r6[6] <= 1) & all(r6[4] > 0)
    # check input error
    with pytest.raises(ValueError) as msg1:
        ultradian.find_cycle(feature='hehe', strain=0, mouse=0,
                             methods='LombScargleFast',
                             plot=False)
    assert msg1.value.args[0] == \
        'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}'
    # check input error
    with pytest.raises(ValueError) as msg2:
        ultradian.find_cycle(feature='F', strain=0, mouse=0,
                             methods='hehe',
                             plot=False)
    assert msg2.value.args[
        0] == 'Input value must in {"LombScargleFast","LombScargle"}'
