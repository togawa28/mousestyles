from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np


def path_index(movement, stop_threshold, min_path_length):
    r"""
    Return a list object containing start and end indices
    for a specific movement. Each element in the list is
    a list containing two indices: the first element is
    the start index and the second element is the end index.

    Parameters
    ----------
    movement : pandas.DataFrame
        CT, CX, CY coordinates and homebase status
        for the unique combination of strain, mouse and day
    stop_threshold : float
        positive number indicating the path cutoff criteria
        if the time difference between two observations is
        less than this threhold, they will be in the same path

    min_path_length : int
        positive integer indicating how many observations in
        a path

    Returns
    -------
    paths index : a list containing the indices for all paths

    Examples
    --------
    >>> movement = data.load_movement(1, 2, 1)
    >>> paths = path_index(movement, 1, 1)[:5]
    >>> paths
    [[0, 2], [6, 8], [107, 113], [129, 131], [144, 152]]
    """
    # check if all inputs are positive integers
    conditions_value = [stop_threshold <= 0, min_path_length <= 0]
    conditions_type = type(min_path_length) != int
    if any(conditions_value):
        raise ValueError("Input values need to be positive")
    if conditions_type:
        raise TypeError("min_path_length needs to be integer")

    # Pull out time variable
    T = movement['t'].ravel()
    # Calculate time differences
    TD = np.diff(T)
    path = []

    # index
    i = 0
    while i < len(TD):
        start_index = i
        # If time difference is less than stop_threshold
        # start to track the index in this path
        while TD[i] < stop_threshold:
            i += 1
            if i == len(TD):
                break
        end_index = i

        # Check whether start index is equal to end index
        # If they are equal jump to next index
        if start_index == end_index:
            next
        else:
            path.append([start_index, end_index])

        i += 1
    path = [p for p in path if (p[1] - p[0]) > min_path_length]

    return(path)
