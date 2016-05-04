from __future__ import print_function, absolute_import, division

import pandas as pd
import numpy as np
from mousestyles import data


def create_time_matrix(combined_gap=4, time_gap=1, days_index=137):
    r"""
    Return a time matrix for estimate the MLE parobability.
    The rows are 137 mousedays. The columns are time series
    in a day. The data are the mouse activity at that time.
    0 represents IS, 1 represents eating, 2 represents
    drinking, 3 represents others activity in AS.

    Parameters
    ----------
    combined_gap: nonnegative float or int
        The threshold for combining small intervals. If next start time
        minus last stop time is smaller than combined_gap than combined
        these two intervals.
    time_gap: positive float or int
        The time gap for create the columns time series
    days_index: nonnegative int
        The number of days to process, from day 0 to day days_index.

    Returns
    -------
    time: Pandas.DataFrame
        a matrix represents the activity for a certain
        mouse day and a certain time.

    Examples
    --------
    >>> time = create_time_matrix(combined_gap=4, time_gap=1).iloc[0, 0:10]
    >>> strain    0
        mouse     0
        day       0
        48007     0
        48008     0
        48009     0
        48010     0
        48011     0
        48012     0
        48013     0
        Name: 0, dtype: float64
    """
    # check all the inputs
    condition_combined_gap = ((type(combined_gap) == int or
                              type(combined_gap) == float) and
                              combined_gap >= 0)
    condition_time_gap = ((type(time_gap) == int or type(time_gap) ==
                           float) and time_gap > 0)
    condition_days_index = (type(days_index) == int and days_index >= 0)
    if not condition_time_gap:
        raise ValueError("time_gap should be nonnegative int or float")
    if not condition_combined_gap:
        raise ValueError("combined_gap should be nonnegative int or float")
    if not condition_days_index:
        raise ValueError("days_index should be nonnegative int")

    intervals_AS = data.load_intervals('AS')
    intervals_F = data.load_intervals('F')
    intervals_W = data.load_intervals('W')
    intervals_IS = data.load_intervals('IS')
    # 137 days totally
    days = np.array(intervals_AS.iloc[:, 0:3].drop_duplicates().
                    reset_index(drop=True))
    # set time range for columns
    initial = int(min(intervals_IS['stop']))
    end = int(max(intervals_IS['stop'])) + 1
    columns = np.arange(initial, end + 1, time_gap)
    # result matrix
    matrix = np.zeros((days.shape[0], len(columns)))
    # we set 0 as IS, 1 as F, 2 as W, 3 as Others
    for i in range(days.shape[0]):
        W = np.array(intervals_W[(intervals_W['strain'] == days[i, 0]) &
                                 (intervals_W['mouse'] == days[i, 1]) &
                                 (intervals_W['day'] == days[i, 2])].
                     iloc[:, 3:5])
        F = np.array(intervals_F[(intervals_F['strain'] == days[i, 0]) &
                                 (intervals_F['mouse'] == days[i, 1]) &
                                 (intervals_F['day'] == days[i, 2])].
                     iloc[:, 3:5])
        AS = np.array(intervals_AS[(intervals_AS['strain'] == days[i, 0]) &
                                   (intervals_AS['mouse'] == days[i, 1]) &
                                   (intervals_AS['day'] == days[i, 2])].
                      iloc[:, 3:5])
        n = W.shape[0]
        index = (np.array(np.where(W[1:, 0]-W[0:n - 1, 1] >
                                   combined_gap))).ravel()
        stop_W = W[np.append(index, n - 1), 1]
        start_W = W[np.append(0, index + 1), 0]
        n = F.shape[0]
        index = (np.array(np.where(F[1:, 0]-F[0:n-1, 1] >
                                   combined_gap))).ravel()
        stop_F = F[np.append(index, n - 1), 1]
        start_F = F[np.append(0, index + 1), 0]
        n = AS.shape[0]
        index = (np.array(np.where(AS[1:, 0]-AS[0:n - 1, 1] >
                                   combined_gap))).ravel()
        stop_AS = AS[np.append(index, n - 1), 1]
        start_AS = AS[np.append(0, index + 1), 0]
        for j in range(len(columns)):
            if sum(np.logical_and(columns[j] > start_AS, columns[j] <
                                  stop_AS)) != 0:
                if sum(np.logical_and(columns[j] > start_F, columns[j] <
                                      stop_F)) != 0:
                    matrix[i, j] = 1  # food
                elif sum(np.logical_and(columns[j] > start_W, columns[j] <
                                        stop_W)) != 0:
                    matrix[i, j] = 2  # water
                else:
                    matrix[i, j] = 3  # others
        # give you the precent of matrix has been processed
        print(i / days.shape[0], 'has been processed')
        if i > days_index:
            break
    # format data frame
    matrix = pd.DataFrame(matrix, columns=columns)
    title = pd.DataFrame(days, columns=['strain', 'mouse', 'day'])
    time_matrix = pd.concat([title, matrix], axis=1)
    return(time_matrix)
