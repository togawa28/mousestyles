from __future__ import print_function, absolute_import, division

import pandas as pd
import numpy as np
from math import ceil
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


def get_prob_matrix_list(time_df, interval_length=1000):
    r"""
    returns a list of probability transition matrices
    that will be later used to characterize and simu-
    late the behavior dynamics of different strains of
    mice. The data used as input is the pandas DataFrame
    generated by function create_time_matrix with de-
    fault parameters. The output is a list of numpy
    arrays, each being a transition matrix characterizing
    one small time interval. The interval length could
    be chosen.

    Parameters
    ----------
    time_df: Pandas.DataFrame
        a huge data frame containing info on strain, mouse
        no., mouse day, and different states at chosen time
        points.
    interval_length: int
        an integer specifying the desired length of each
        small time interval.

    Returns
    -------
    matrix_list: list
        a list of the mle estimations of the probability tran-
        sition matrices for each small time interval stored in
        the format of numpy array. Each element of this list
        is a numpy array matrix.

    Examples
    --------
    >>> row_i = np.hstack((np.zeros(13), np.ones(10),
                            np.ones(10)*2, np.ones(10)*3))
    >>> time_df_eg = np.vstack((row_i, row_i,row_i))
    >>> time_df_eg = pd.DataFrame(time_df_eg)
    >>> mat_list = get_prob_matrix_list(time_df_eg,
                                        interval_length=10)
    >>> mat_list[0]
    >>> array([[ 1.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.]])
    >>> mat_list[1]
    >>> array([[ 0.,  0.,  0.,  0.],
               [ 0.,  1.,  0.,  0.],
               [ 0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.]])
    >>> mat_list[2]
    >>> array([[ 0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.],
               [ 0.,  0.,  1.,  0.],
               [ 0.,  0.,  0.,  0.]])
    >>> mat_list[3]
    >>> array([[ 0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  1.]])

    """
    # check all the inputs
    condition_time_df = (type(time_df) == pd.core.frame.DataFrame)
    condition_interval_length = (type(interval_length) == int and
                                 interval_length > 0)
    if not condition_time_df:
        raise ValueError("time_df should be pandas DataFrame")
    if not condition_interval_length:
        raise ValueError("interval_length should be positive int")

    time_array = np.array(time_df)[:, 3:]
    n = ceil(time_array.shape[1]/interval_length)
    matrix_list = [None] * int(n)
    for i in np.arange(n):
        i = int(i)
        ind = [(i * interval_length), ((i+1) * interval_length)]
        small_time_array = time_array[:, ind[0]:ind[1]]
        small_time_list = list(small_time_array)
        small_time_str_list = ["".join(np.char.mod('%i', a))
                               for a in small_time_list]
        matrix_list[i] = get_prob_matrix_small_interval(small_time_str_list)
    return matrix_list


def get_prob_matrix_small_interval(string_list):
    r"""
    return the MLE estimate of the probability matrix
    of the markov chain model. The data used as input
    is a list of strings that contains the information
    regarding the transition of states of the mouse be-
    havior. The output is a matrix stored in the format
    of numpy array, where the i,j th term indicates the
    probability of transiting from state i to state j.

    Parameters
    ----------
    string_list: list
        a list of strings of the states in the given
        time slot.

    Returns
    -------
    M: numpy.ndarray
        the MLE estimation of the probability tran-
        sition matrix. Each entry M_ij represents the
        probability of transiting from state i to state
        j.

    Examples
    --------
    >>> time_list = ['002', '001', '012']
    >>> get_prob_matrix_small_interval(time_list)
    >>> array([[ 0.4,  0.4,  0.2,  0. ],
               [ 0. ,  0. ,  1. ,  0. ],
               [ 0. ,  0. ,  0. ,  0. ],
               [ 0. ,  0. ,  0. ,  0. ]])

    """
    # check all the inputs
    condition_string_list = (type(string_list) == list)
    condition_list_item = (type(string_list[0]) == str)
    print(string_list[0])
    if not condition_string_list:
        raise ValueError("string_list should be a list")
    if not condition_list_item:
        raise ValueError("items in string_list should be str")

    Mat_prob = np.zeros(4*4).reshape(4, 4)
    for i in np.arange(4):
        i = int(i)
        for j in np.arange(4):
            j = int(j)
            ijth = str(i) + str(j)
            Mat_prob[i, j] = sum([string.count(ijth) for string
                                 in string_list])
    for k in np.arange(4):
        k = int(k)
        if sum(Mat_prob[k, :]) != 0:
            Mat_prob[k, :] = Mat_prob[k, :]/sum(Mat_prob[k, :])
    return Mat_prob
