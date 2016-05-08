from __future__ import print_function, absolute_import, division

import pandas as pd
import numpy as np
from path_features import compute_angles
from detect_noise import detect_noise


def smooth_noise(movement, paths, angle_threshold, delta_t):
    r"""
    Return a new movement pandas DataFrame object containing
    CT, CX, CY coordinates and the homebase status. The points at which
    noise, as defined by the input parameters, is detected have been
    smoothed by averaging.

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
    conditions_value = [angle_threshold < 0, delta_t < 0]
    if any(conditions_value):
        raise ValueError("Input values need to be positive")

    if not isinstance(movement, pd.core.frame.DataFrame):
        raise TypeError("Movement must be pandas DataFrame")

    if set(movement.keys()) != {'isHB', 't', 'x', 'y'}:
        raise ValueError(
            "The keys of movement must be 't', 'x', 'y', and 'isHB'")

    if len(movement) <= 1:
        raise ValueError("Movement must contain at least 2 rows")

    noise = detect_noise(movement, paths, angle_threshold, delta_t)

    max_noise = max(noise)

    drop_ind = []
    drop_ind = np.array(drop_ind)

    for i in range(1, max_noise + 1):
        noise_chunk = noise[noise == i]
        movement_chunk = movement.loc[noise_chunk.index]

        x_avg = np.mean(movement_chunk['x'])
        y_avg = np.mean(movement_chunk['y'])
        t_avg = np.mean(movement_chunk['t'])

        movement['x'][noise_chunk.index[0]] = x_avg
        movement['y'][noise_chunk.index[0]] = y_avg
        movement['t'][noise_chunk.index[0]] = t_avg

        drop_ind = np.append(drop_ind, noise_chunk.index[1:])

    new_movement = movement.drop(drop_ind)
    new_movement.index = range(len(new_movement))

    return(new_movement)
