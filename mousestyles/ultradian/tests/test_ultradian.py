from __future__ import print_function, absolute_import, division

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import chi2

import mousestyles.data as data

#Check the outcome data type of function aggregate_interval()
def aggregate_interval_test(strain=0, mouse=1, feature="AS", bin_width=30):
    result = aggregate_interval(strain, mouse, feature, bin_width)
        assert type(result) is pd.core.series.Series
#Check the length of the outcome, should be 17280/bin_width
def aggregate_interval_test_length(strain=0, mouse=1, feature="AS", bin_width=30):
    result = aggregate_interval(strain, mouse, feature, bin_width)
        assert len(result) == 17280/bin_width

#Check the outcome data type of function aggregate_movement()
def aggregate_movement_test(strain=0, mouse=1, bin_width=30):
    result = aggregate_movement(strain,mouse, bin_width)
        assert type(result) is pd.core.series.Series
#Check the outcome data type of function aggregate_movement()
def aggregate_movement_test_length(strain=0, mouse=1, bin_width=30):
    result = aggregate_movement(strain,mouse, bin_width)
        assert len(result) == 17280/bin_width

#Check the outcome data type of function aggregate_data()
#First to check to data type
def aggregate_data_test(feature="AS", bin_width=30):
    result = aggregate_data(feature, binwith)
        assert type(result) is pd.core.frame.DataFrame
#Then to check the number of columns
def aggregate_data_test_columns(feature="AS", bin_width=30):
    result = aggregate_data(feature, binwith)
        n = len(result.columns)
        assert n == 4
#Check the range for hour, should be within 24 hours
def aggregate_data_test_hour(feature="AS", bin_width=30):
    result = aggregate_data(feature,bin_width)
    test = np.array(result['hour'])
    assert test.max() < 24
#Check the range of strain, should only have 0,1,2. There the lenght of the unique values should be 3
def aggregate_data_test_strain(feature="AS", bin_width=30):
    result = aggregate_data(feature,bin_width)
    test = np.array(result['strain'])
    assert len(np.unique(test)) == 3
#Check the values in feature columns, all the values should be greater than 0
def aggregate_data_test_feature(feature="AS", bin_width=30):
    result = aggregate_data(feature,bin_width)
    test = np.array(result[feature])
    assert test.min() >= 0

#Test for seasonal decomposition
def seasonal_decomposition_test(strain=0, mouse=1, feature='AS', bin_width=30, period_length=10):
    resul = seasonal_decomposition(strain, mouse, feature, bin_width, period_length)
        assert tyep(result) == statsmodels.tsa.seasonal.DecomposeResult

#strain_seasonal is to produce a plot, so I think we can check the plot directly istead of writing a test function

#check the outcome range of mix_strain, the result is a p-value, so it's between 0 and 1
def mix_strain_test(data, feature):
    result = mix_strain(data, feature)
        assert  0 < result < 1