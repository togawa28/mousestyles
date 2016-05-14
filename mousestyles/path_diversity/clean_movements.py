from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pandas as pd


def clean_movements(movements, keep_index=False):
    r"""
    Returns a list of cleaned movement objects.

    For each element of the input `movements` object, detects the existence of
    adjacent rows which have i) same x,y-coordinates, or ii) same timestamps.
    For case i), and removes the duplicated rows except for the first.
    For case ii), raises value error.

    Parameters
    ----------
    movements : list
        each element is pandas.DataFrame containing
        CT, CX, CY coordinates.
        Should have length greater than 1.

    keep_index : boolean
        whether or not keep the original index.
        Deafalt is False.
        If false, cleaned movement object is re-indexed.

    Returns
    -------
    cleaned-movements : list
        each element is cleaned movement object.

    Examples
    --------
    >>> strain_nums = [0,0,1,1,2,2]
    >>> mouse_nums = [0,0,1,1,2,2]
    >>> day_nums = [0,11,0,11,0,11]
    >>> movements = [data.load_movement(strain_num, mouse_num, day_num)
                     for strain_num, mouse_num, day_num in
                     zip(strain_nums, mouse_nums, day_nums)]
    >>> cleaned_movements = clean_movements(movements)
    """
    if not isinstance(movements, list):
        raise TypeError("movements must be a list")

    if len(movements) == 0:
        raise ValueError("movements must contain at least 1 movement object")

    if not isinstance(keep_index, bool):
        raise TypeError("keep_index must be bool")

    def testing_input_movement(one_movement):
        # test for each element of `movements`
        # 1) must be pandas DataFrame
        if not isinstance(one_movement, pd.core.frame.DataFrame):
            out = 1
        # 2) must have columns named `x`, `y`, `t`
        elif not set(one_movement.keys()).issuperset(['x', 'y', 't']):
            out = 2
        # 3) must have length greater than 1
        elif len(one_movement) <= 1:
            out = 3
        else:
            out = 0
        return(out)

    def detect_same_loc(one_movement):
        # returns indices which have same x,y-coordinates as the previous
        x_bool = one_movement['x'][:-1] == one_movement['x'][1:]
        y_bool = one_movement['y'][:-1] == one_movement['y'][1:]
        same_loc_bool = x_bool & y_bool
        same_loc = [i + 1 for i in range(len(same_loc_bool))
                    if same_loc_bool[i]]
        return(same_loc)

    def detect_same_time(one_movement):
        # returns indices which have same timestamp as the previous
        time_bool = one_movement['t'][:-1] == one_movement['t'][1:]
        same_time = [i + 1 for i in range(len(time_bool))
                     if time_bool[i]]
        return(same_time)

    def drop_same_loc(one_movement, same_loc):
        # based on `same_loc` drops the duplicated rows
        new_one_movement = one_movement.drop(same_loc)
        if not keep_index:
            new_one_movement.index = range(len(new_one_movement))
        return(new_one_movement)

    # testing each element of `movements` obj.
    test_outs = [testing_input_movement(one_movement)
                 for one_movement in movements]

    if any([True for test in test_outs if test == 1]):
        raise TypeError("each movement object must be pandas DataFrame")

    if any([True for test in test_outs if test == 2]):
        raise ValueError(
            "the keys of each movement object must contain 'x', 'y', 't")

    if any([True for test in test_outs if test == 3]):
        raise ValueError("each movement object must contain at least 2 rows")

    same_locs = [detect_same_loc(one_movement) for one_movement in movements]
    same_times = [detect_same_time(one_movement) for one_movement in movements]

    # if any of one movement contains same timestamps in adjacent rows, raise
    # error.
    if any([len(same_time) != 0 for same_time in same_times]):
        raise ValueError(
            "some movement contains same timestamps in adjacent rows")

    cleaned_movements = [drop_same_loc(movement, same_loc)
                         for movement, same_loc in zip(movements, same_locs)]
    return(cleaned_movements)
