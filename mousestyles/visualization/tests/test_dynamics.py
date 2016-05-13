from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest
import numpy as np
import pandas as pd

from mousestyles.dynamics import plot_dynamics


def test_plot_dynamics_input():
    # checking functions raise the correct errors for wrong input
    # time_df is not DataFrame
    with pytest.raises(ValueError) as excinfo:
        plot_dynamics(df=5, strain_num=2)
    assert excinfo.value.args[0] == "df should be pandas DataFrame"
    # strain_num is not integer in 0,1,2
    row_i = np.hstack((np.zeros(13), np.ones(10),
                       np.ones(10) * 2, np.ones(10) * 3))
    time_df_eg = np.vstack((row_i, row_i, row_i))
    time_df_eg = pd.DataFrame(time_df_eg)
    time_df_eg.rename(columns={0: 'strain'}, inplace=True)
    with pytest.raises(ValueError) as excinfo:
        plot_dynamics(df=time_df_eg, strain_num=3)
    assert excinfo.value.args[0] == "strain_num can only be 0, 1, 2"
    # interval_length_initial is a numpy array with positive integers
    with pytest.raises(ValueError) as excinfo:
        plot_dynamics(df=time_df_eg, strain_num=0,
                      interval_length_initial=3)
    assert excinfo.value.args[0] == "interval_length_initial positive np.array"
    with pytest.raises(ValueError) as excinfo:
        plot_dynamics(df=time_df_eg, strain_num=0,
                      interval_length_initial=np.array([1, 2, -1]))
    assert excinfo.value.args[0] == "interval_length_initial positive np.array"
    with pytest.raises(ValueError) as excinfo:
        plot_dynamics(df=time_df_eg, strain_num=0,
                      interval_length_initial=np.array([1, 2, 3.1]))
    assert excinfo.value.args[0] == "interval_length_initial positive np.array"
    # plot_time_range is a numpy array with positive integers
    with pytest.raises(ValueError) as excinfo:
        plot_dynamics(df=time_df_eg, strain_num=0,
                      plot_time_range=3)
    assert excinfo.value.args[0] == "plot_time_range positive np.array"
    with pytest.raises(ValueError) as excinfo:
        plot_dynamics(df=time_df_eg, strain_num=0,
                      plot_time_range=np.array([1, 2, -1]))
    assert excinfo.value.args[0] == "plot_time_range positive np.array"
    with pytest.raises(ValueError) as excinfo:
        plot_dynamics(df=time_df_eg, strain_num=0,
                      plot_time_range=np.array([1, 2, 3.1]))
    assert excinfo.value.args[0] == "plot_time_range positive np.array"
