from __future__ import print_function, absolute_import, division

import numpy as np


def get_dist_speed(movement, start, end, return_array=True):
    r"""
    Return a list containing distance(s) covered in a path and
    average speed(s) within a path.

    Parameters
    ----------
    movement : pandas.DataFrame
        CT, CX, CY coordinates and homebase status for the unique
        combination of strain, mouse, and day

    start : int
        positive integer indicating the starting index of a path

    end : int
        positive integer indicating the end index of a path

    return_array : bool
        boolean indicating whether an array of distances and
        average speeds are returned or the summation of those
        distances and speeds

    Returns
    -------
    dist : distance(s) travelled along a path

    speed : average speed(s) along a path

    Examples
    --------
    >>> movement = data.load_movement(1, 2, 1)
    >>> dist, speed = get_dist_speed(movement, 0, 3)
    >>> print(dist)
    [0.0, 0.17999999999999972, 0.19446593532030554]
    >>> print(speed)
    [0.0, 0.9999999999983815, 0.055246004352409776]
    >>> dist, speed = get_dist_speed(movement, 0, 3, return_array=False)
    >>> print(dist)
    0.37446593532030525
    >>> print(speed)
    0.096661315260887087
    """

    # Check whether inputs are valid.
    if (start < 0) or (end < 0):
        raise ValueError("Start and end indices must be positive")
    if (type(start) != int) or (type(end) != int):
        raise TypeError("Start and end indices must be integers")
    if start > end:
        raise ValueError("Start index must be smaller than end index")
    if end - start > len(movement) - 1:
        raise ValueError("Number of observations must be less than \
        or equal to total observations")

    if start == end:
        return(0, 0)

    x = movement['x'][start:(end + 1)].ravel()
    y = movement['y'][start:(end + 1)].ravel()

    if return_array:
        t = movement['t'][start:(end + 1)].ravel()
        time = np.diff(t)
        dist = np.sqrt((x[1:] - x[:-1])**2 + (y[1:] - y[:-1])**2).tolist()
        speed = (dist / time).tolist()
    else:
        t = movement['t']
        time = t[end] - t[start]
        dist = sum(np.sqrt((x[1:] - x[:-1])**2 + (y[1:] - y[:-1])**2))
        speed = dist / time

    return([dist, speed])
