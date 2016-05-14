from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


def filter_path(movement, paths, time_threshold):
    r"""
    Return a list object containing start and end indices for
    movements lasting equal to or longer than the specified time
    threshold

    Parameters
    ----------
    movement : pandas.DataFrame
        CT, CX, CY coordinates and homebase status
        for the unique combination of strain, mouse and day
    paths: list
        a list containing the indices for all paths
    time_threshold : float
        positive number indicating the time threshold

    Returns
    -------
    paths index : a list containing the indices for all paths
    that the spending times are larger than a time threshold

    Examples
    --------
    >>> movement = data.load_movement(1, 2, 1)
    >>> paths = path_index(movement, 1, 1)
    >>> filter_path(movement, paths, 20)
    [[26754, 26897], [28538, 28627]
    """

    # check if all inputs are positive integers
    conditions_value = time_threshold <= 0
    if conditions_value:
        raise ValueError("Input values need to be positive")

    # Variable that store paths equal to or larger than time threshold
    pass_paths = []

    # Pull out time variable
    T = movement['t']

    # Run through each path and check whether the time spending
    # on the path is equal to or larger than the time threshold
    for path in paths:
        start_time, end_time = T[path].ravel()
        if (end_time - start_time) >= time_threshold:
            pass_paths.append(path)

    return(pass_paths)
