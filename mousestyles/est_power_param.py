from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import pandas as pd
from mousestyles import data


def getdistance(strain, mouse, day):
    """
    Return the distance of each two consecutive points among coordinates
    which is bigger than 1cm(truncated).

    Parameters
    ----------
    strain : int
    the strain number of the mouse
    mouse  : int
    the mouse number in its strain
    day    :  int
    the day number

    Returns
    -------
    cut_dist : an array of number
    The vector of truncated distance.

    Examples
    --------
    >>> getdistance (0, 0, 0)
    array([ 1.00648944,  1.02094319,  1.0178885 , ...,  1.00099351,
    1.01191156,  1.00423354])
    """
    df = data.load_movement(strain, mouse, day)
    xcood = df["x"]
    ycood = df["y"]
    distance_vector = np.sqrt(np.diff(xcood)**2 + np.diff(ycood)**2)
    msk = distance_vector > 1
    cut_dist = distance_vector[msk]
    return(cut_dist)


def fit_powerlaw(strain, mouse, day):
    """
    Return the estimator of truncated power law.

    Parameters
    ----------
    strain : int
        the strain number of the mouse
    mouse  : int
        the mouse number in its strain
    day    :  int
        the day number

    Returns
    -------
    estimator : a float number
        The estimator of truncated power law.

    Examples
    --------
    >>> fit_powerlaw (0, 0, 0)
    9.4748705008269827
    """
    cut_dist = getdistance(strain, mouse, day)
    ret_mle = 1 + len(cut_dist) * 1 / \
        (np.sum(np.log(cut_dist / np.min(cut_dist))))
    return ret_mle


def fit_exponential(strain, mouse, day):
    """
    Return the estimator of truncated exponential.

    Parameters
    ----------
    strain : int
        the strain number of the mouse
    mouse  : int
        the mouse number in its strain
    day :  int
        the day number

    Returns
    -------
    estimator : a float number
        The estimator of truncated exponential distribution.

    Examples
    --------
    >>> fit_exponential (0, 0, 0)
    7.385844980814098
    """
    cut_dist = getdistance(strain, mouse, day)
    ret_mle = len(cut_dist) / (np.sum(cut_dist) - len(cut_dist))
    return ret_mle


def fit_dist_all():
    """
    Return the estimators of truncated power law and exponential for each
    mouse day.

    Parameters
    ----------

    Returns
    -------
    estimator : a float number
        The estimator of truncated exponential distribution.

    Examples
    --------
    >>> fit()
    7.385844980814098
    """
    esti_df = {"strain": [], "mouse": [], "day": [], "power": [], "exp": []}
    for i in range(3):
        for j in range(4):
            for k in range(12):
                try:
                    temp1 = fit_powerlaw(i, j, k)
                    temp2 = fit_exponential(i, j, k)
                    esti_df["strain"].append(i)
                    esti_df["mouse"].append(j)
                    esti_df["day"] .append(k)
                    esti_df["power"] .append(temp1)
                    esti_df["exp"] .append(temp2)
                except:
                    next
    estimation = pd.DataFrame(
        esti_df, columns=["strain", "mouse", "day", "power", "exp"])
    return estimation
