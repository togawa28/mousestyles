from __future__ import print_function, absolute_import, division

import os as _os

import numpy as np
import pandas as pd

from mousestyles import data_dir
from mousestyles.intervals import Intervals
import collections

from matplotlib.externals import six

INTERVAL_FEATURES = ["AS", "F", "IS", "M_AS", "M_IS", "W"]


def load_all_features():
    """
    Returns a (21131, 13) size pandas.DataFrame object corresponding to
    9 features over each mouse's 2-hour time bin. The first four columns
    index each mouses's 2-hour bin:

    Column 0: the strain of the mouse (0-15)
    Column 1: the mouse number (number depends on strain)
    Column 2: the day number (5-16)
    Column 3: the 2-hour time bin (e.g., value 4 corresponds to hours 4 to 6)

    The remaining 9 columns are the computed features.

    Returns
    -------
    features_data_frame : pandas.DataFrame
        A dataframe of computed features.
    """
    features = [
        'ASProbability',
        'ASNumbers',
        'ASDurations',
        'Food',
        'Water',
        'Distance',
        'ASFoodIntensity',
        'ASWaterIntensity',
        'MoveASIntensity']

    # 9 x 1921 x (3 labels + 11 feature time bins)
    all_features = np.load(
        _os.path.join(
            data_dir,
            'all_features_mousedays_11bins.npy'))

    # Here we begin reshaping the 3-d numpy array into a pandas 2-d dataframe
    columns = ['strain', 'mouse', 'day']
    # Append 2-hour time bin values
    columns += list(range(0, 22, 2))

    # For each feature, unpivot its dataframe so that the 2-hour
    # time bins become a value column, rather than a dimension
    data_frames = []
    for (i, feature) in enumerate(features):
        df = pd.DataFrame(data=all_features[i, :, :], columns=columns)
        melted_df = pd.melt(df, id_vars=columns[:3], value_vars=columns[3:],
                            var_name='hour', value_name=feature)
        data_frames.append(melted_df)

    # Connect each of the feature dataframes to make one dataframe
    all_features_df = data_frames.pop(0)
    other_features = [x.iloc[:, -1] for x in data_frames]
    other_features.insert(0, all_features_df)
    return pd.concat(other_features, axis=1)


def load_mouseday_features(features=None):
    """
    Returns a (1921, 3+11*n) size pandas.DataFrame object corresponding to
    each 2-hour time bin of the n inputted features over each mouse.
    The first three columns index each mouse:

    Column 0: the strain of the mouse (0-15)
    Column 1: the mouse number (number depends on strain)
    Column 2: the day number (5-16)

    The remaining 3*n columns are the values for each 2-hour time bin
    of the n inputted features.

    Parameters
    ----------
    features: list, optional
        A list of one or more features chosen from
        {"ASProbability", "ASNumbers", "ASDurations",
        "Food", "Water", "Distance",
        "ASFoodIntensity", "ASWaterIntensity", "MoveASIntensity"}
        Default all features when optional

    Returns
    -------
    features_data_frame : pandas.DataFrame
        A dataframe of computed features.

    Examples
    --------
    >>> mouseday = load_mouseday_features()
    >>> mouseday = load_mouseday_features(["Food"])
    >>> mouseday = load_mouseday_features(["Food", "Water", "Distance"])
    """
    features_list = [
        "ASProbability",
        "ASNumbers",
        "ASDurations",
        "Food",
        "Water",
        "Distance",
        "ASFoodIntensity",
        "ASWaterIntensity",
        "MoveASIntensity"]

    if features is None:
        features = features_list

    if type(features) is str:
        features = [features]

    fea_str = "{"
    for item in features_list:
        fea_str += '"' + item + '", '
    fea_str = fea_str[:-2] + "}"

    # Check if input is a list
    if type(features) is not list:
        raise TypeError(
            "Input value must be a list."
        )

    # Check if input values are expected features
    for feature in features:
        if feature not in features_list:
            raise ValueError(
                "Input value must be chosen from " + fea_str + "."
            )

    # 9 x 1921 x (3 labels + 11 feature time bins)
    all_features = np.load(
        _os.path.join(
            data_dir,
            "all_features_mousedays_11bins.npy"))

    # Locate each feature and aggregate numpy arrays
    dic = {}
    for (i, feature) in enumerate(features_list):
        dic[feature] = i
    all_data_orig = np.hstack(
        [all_features[0, :, 0:3]] +
        [all_features[dic[feature], :, 3:] for feature in features])

    # Prepare column names
    columns = ["strain", "mouse", "day"]
    for feature in features:
        columns += [feature + "_" + str(x) for x in range(0, 22, 2)]
    # Transform into data frame
    data_all = pd.DataFrame(all_data_orig, columns=columns)

    return data_all


def load_intervals(feature):
    """
    Return a pandas.DataFrame object of project interval data
    for the specified feature.

    There are 5 columns in the dataframe:
    strain: the strain number of the mouse
    mouse: the mouse number in its strain
    day: the day number
    start: the start time
    stop: the stop time

    Parameters
    ----------
    feature: {"AS", "F", "IS", "M_AS", "M_IS", "W"}

    Returns
    -------
    intervals : pandas.DataFrame
        All data of the specified feature as a dataframe

    Examples
    --------
    >>> AS = load_intervals('AS')
    >>> IS = load_intervals('IS')
    """
    # check input is one of the provided choices
    if feature not in INTERVAL_FEATURES:
        raise ValueError(
            'Input value must be one of {"AS", "F", "IS", "M_AS", "M_IS", "W"}'
        )
    # get all file names
    file_names = _os.listdir(_os.path.join(data_dir, "intervals", feature))
    # check if directory is empty
    if len(file_names) == 0:
        raise ValueError('Directory is empty; no file found.')
    # initialized data frame
    # use for loop to load every file and concat to overall data frame
    dt = pd.DataFrame()
    for item in file_names:
        strain = int(item.split("strain")[1].split("_mouse")[0])
        mouse = int(item.split("mouse")[1].split("_day")[0])
        day = int(item.split("day")[1].split(".npy")[0])
        path = _os.path.join(data_dir, "intervals", feature, item)
        sub = np.load(path)
        dt_sub = pd.DataFrame()
        dt_sub["strain"] = [strain] * sub.shape[0]
        dt_sub["mouse"] = [mouse] * sub.shape[0]
        dt_sub["day"] = [day] * sub.shape[0]
        dt_sub["start"] = sub[:, 0]
        dt_sub["stop"] = sub[:, 1]
        dt = pd.concat([dt, dt_sub])
    # sort based on strain, mouse and day
    dt = dt.sort(["strain", "mouse", "day"])
    dt.index = range(dt.shape[0])
    return dt


def load_movement(strain, mouse, day):
    """
    Return a pandas.DataFrame object of project movement data
    for the specified combination of strain, mouse and day.

    There are 4 columns in the dataframe:
    t: Time coordinates (in seconds)
    x: X coordinates indicating the left-right position of the cage
    y: Y coordinates indicating the front-back position of the cage
    isHB: Boolean indicating whether the point is in the home base or not

    Parameters
    ----------
    strain: int
        nonnegative integer indicating the strain number
    mouse: int
        nonnegative integer indicating the mouse number
    day: int
        nonnegative integer indicating the day number

    Returns
    -------
    movement : pandas.DataFrame
        CT, CX, CY coordinates and home base status
        of the combination of strain, mouse and day

    Examples
    --------
    >>> movement = load_movement(0, 0, 0)
    >>> movement = load_movement(1, 2, 1)
    """
    # check if all inputs are nonnegative integers
    conditions_value = [strain < 0, mouse < 0, day < 0]
    conditions_type = [type(strain) != int, type(mouse) != int,
                       type(day) != int]
    if any(conditions_value):
        raise ValueError("Input values need to be nonnegative")
    if any(conditions_type):
        raise TypeError("Input values need to be integer")
    # load all four files of HB, CT, CX and CY data
    NHB_path = "txy_coords/C_idx_HB/C_idx_HB_strain{}_mouse{}_day{}.npy".\
        format(strain, mouse, day)
    CT_path = "txy_coords/CT/CT_strain{}_mouse{}_day{}.npy".\
        format(strain, mouse, day)
    CX_path = "txy_coords/CX/CX_strain{}_mouse{}_day{}.npy".\
        format(strain, mouse, day)
    CY_path = "txy_coords/CY/CY_strain{}_mouse{}_day{}.npy".\
        format(strain, mouse, day)
    try:
        HB = ~ np.load(_os.path.join(data_dir, NHB_path))
        CT = np.load(_os.path.join(data_dir, CT_path))
        CX = np.load(_os.path.join(data_dir, CX_path))
        CY = np.load(_os.path.join(data_dir, CY_path))
    except IOError:
        raise ValueError("No data exists for strain {}, mouse {}, day {}".
                         format(strain, mouse, day))
    # make data frame
    dt = pd.DataFrame()
    dt["t"] = CT
    dt["x"] = CX
    dt["y"] = CY
    dt["isHB"] = HB
    return dt


def _lookup_intervals(times, intervals):
    """
    Return a boolean array where each element is True
    if the corresponding element of `times` was
    in `intervals`.

    Parameters
    ----------
    times: numpy.array of floats
        an array of timestamps
    intervals: pandas.DataFrame
        a data frame containing columns 'start' and
        'stop', represent a series of time intervals

    Returns
    -------
    numpy.array of booleans
        Array of booleans representing whether the timestamps
        in `times` fell in the intervals in `intervals`

    Examples
    --------
    >>> t = pd.Series([1.5, 2.5, 3.5])
    >>> ints = pd.DataFrame({'start': [1, 2], 'stop': [1.99, 2.99]})
    >>> in_intervals = _lookup_intervals(t, ints)
    >>> t.shape == in_intervals.shape
    True
    >>> in_intervals
    0     True
    1     True
    2    False
    dtype: bool
    """
    ints = Intervals(intervals[['start', 'stop']])
    return times.map(ints.contains)


def load_movement_and_intervals(strain, mouse, day,
                                features=INTERVAL_FEATURES):
    """
    Return a pandas.DataFrame object of project movement and interval
    data for the specified combination of strain, mouse and day.

    There are 4 + len(features) columns in the dataframe: t: Time
    coordinates (in seconds) x: X coordinates indicating the
    left-right position of the cage y: Y coordinates indicating the
    front-back position of the cage isHB: Boolean indicating whether
    the point is in the home base or not Additonal columns taking
    their names from features: Boolean indicating whether the time
    point is in an interval of behavior of the given feature.

    Parameters
    ----------
    strain: int
        nonnegative integer indicating the strain number
    mouse: int
        nonnegative integer indicating the mouse number
    day: int
        nonnegative integer indicating the day number
    features: list (or other iterable) of strings
        list of features from {"AS", "F", "IS", "M_AS", "M_IS", "W"}

    Returns
    -------
    movement : pandas.DataFrame CT, CX, CY
        coordinates, home base status, and feature interval information
        for a given srain, mouse and day

    Examples
    --------
    >>> m1 = load_movement(1, 1, 1)
    >>> m2 = load_movement_and_intervals(1, 1, 1, []) # don't add any features
    >>> np.all(m1 == m2)
    True
    >>> m3 = load_movement_and_intervals(1, 1, 1, ['AS'])
    >>> m3.shape[1] == m1.shape[1] + 1 # adds one column
    True
    >>> m3.shape[0] == m1.shape[0] # same number of rows
    True
    >>> m3[29:32]
                t      x       y   isHB     AS
    29  56448.333 -6.289  34.902  False  False
    30  56448.653 -5.509  34.173   True   True
    31  56449.273 -5.048  33.284   True   True
    """
    if isinstance(features, six.string_types):
        features = [features]
    elif not isinstance(features, collections.Iterable):
        raise ValueError('features must be a string or iterable of strings')
    movements = load_movement(strain, mouse, day)
    for f in features:
        intervals = load_intervals(feature=f)
        mouse_intervals = intervals[(intervals['strain'] == strain) &
                                    (intervals['mouse'] == mouse) &
                                    (intervals['day'] == day)]
        movements[f] = _lookup_intervals(movements['t'], mouse_intervals)

    return movements


def load_start_time_end_time(strain, mouse, day):
    """
    Returns the start and end times recorded
    for the mouse-day. The first number indicates
    the number of seconds elapsed since midnight,
    the second number indicates when the cage is
    closed for cleaning. In other words, this is
    the interval for which all sensors are active.

    Parameters
    ----------
    strain: int
        nonnegative integer indicating the strain number
    mouse: int
        nonnegative integer indicating the mouse number
    day: int
        nonnegative integer indicating the day number

    Returns
    -------
    times: a tuple of (float, float)
        the start time and end time
    """
    file_name = 'recordingStartTimeEndTime_strain{}_mouse{}_day{}.npy'.\
                format(strain, mouse, day)
    path_to_file = _os.path.join(data_dir, 'txy_coords',
                                 'recordingStartTimeEndTime',
                                 file_name)
    return tuple(np.load(path_to_file))
