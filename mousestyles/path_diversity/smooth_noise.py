from __future__ import print_function, absolute_import, division

import pandas as pd
import numpy as np
from mousestyles.path_diversity import detect_noise


def smooth_noise(movement, paths, angle_threshold, delta_t):
    r"""
    Return a new smoothed movement pandas DataFrame object containing
    CT, CX, CY coordinates.

    The inputted movement DataFrame is passed through a noise detection
    function. At points where noise is detected, as defined by the
    input parameters (i.e., angle_threshold and delta_t), this function
    returns a new movement DataFrame by averaging points where noise
    is detected.

    Parameters
    ----------
    movement : pandas.DataFrame
        CT, CX, CY coordinates and homebase status
        for the unique combination of strain, mouse and day

    paths index : a list containing the indices for all paths

    angle_threshold : float
        positive number indicating the minimum turning angle to flag as noise

    delta_t : float
        positive number indicating the delta_time interval

    Returns
    -------
    smoothed movement : pandas.DataFrame
        CT, CX, CY coordinates and homebase status
        for the unique combination of strain, mouse and day

    Examples
    --------
    >>> movement = data.load_movement(1, 2, 1)
    >>> paths = path_index(movement, 1, 1)
    >>> smoothed_movement = smooth_noise(movement, paths, 135, .1)
    """

    # check if all inputs are positive
    if not isinstance(movement, pd.core.frame.DataFrame):
        raise TypeError("Movement must be pandas DataFrame")

    if set(movement.keys()).issuperset(['x', 'y', 't']) is False:
        raise ValueError(
            "The keys of movement must be 't', 'x', and 'y'")

    if len(movement) <= 1:
        raise ValueError("Movement must contain at least 2 rows")

    noise = detect_noise.detect_noise(
        movement, paths, angle_threshold, delta_t)

    max_noise = max(noise)

    drop_ind = np.array([])

    for i in range(1, max_noise + 1):
        noise_chunk = noise[noise == i]
        movement_chunk = movement.loc[noise_chunk.index]

        x_avg = np.mean(movement_chunk['x'])
        y_avg = np.mean(movement_chunk['y'])
        t_avg = np.mean(movement_chunk['t'])

        movement['x'][noise_chunk.index[0]] = x_avg
        movement['y'][noise_chunk.index[0]] = y_avg
        movement['t'][noise_chunk.index[0]] = t_avg

        # Note: The above DataFrame manipulations result in a
        # SettingWithCopyWarning. The warning persists even after
        # attempting the following format:
        # .loc[row_indexer,col_indexer] = value. Despite this,
        # the output of the function is working as intended.

        drop_ind = np.append(drop_ind, noise_chunk.index[1:])

    new_movement = movement.drop(drop_ind)
    new_movement.index = range(len(new_movement))

    return(new_movement)
