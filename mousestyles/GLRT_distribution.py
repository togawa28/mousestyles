from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


import numpy as np
from mousestyles import data


def random_powerlaw(n, a, seed=-1):
    """
    Random generate points of truncated power law.

    The method we generate is to inverse Cumulative Density Function
    of truncated powerlaw function, and put random number draw from
    Unif[0,1]. The theory behind it is $F^{-1}(U) \sim F$.

    Parameters
    ----------
    n : int
        number of points
    a : int>1
        power law parameter alpha

    Returns
    -------
    points : a vector of float number
        n points have the target distribution.

    Examples
    --------
    >>> random_powerlaw(4,2)
    array([  1.18097435,   1.04584078,   1.4650779 ,  36.03967524])
    """
    if seed != -1:
        np.random.seed(seed)
    y = np.random.sample(n)
    return (1 - y)**(-1 / (a - 1))


def random_exp(n, l, seed=-1):
    """
    Random generate points of truncated exponential.

    The method we generate is to use the memorylessness property
    of exponential distribution. As the survival function of
    exponential distribution is always the same, for truncated
    exponential distribution, it is just the same to draw from
    regular exponential distribtion and shift the truncated
    value.

    Parameters
    ----------
    n : int
        number of points
    l : int
        exponential parameter lambda

    Returns
    -------
    points : a vector of float number
        n points have the target distribution.

    Examples
    --------
    >>> random_exp(4,2)
    array([ 1.07592496,  1.19789646,  1.19759663,  1.03993227])
    """
    if seed != -1:
        np.random.seed(seed)
    y = np.random.exponential(1.0 / l, n)
    return y + 1


def hypo_powerLaw_null(strain, mouse, day, law_est=0, seed=-1):
    """
    Return the outcome from GLRT with null hypothesis law distribution.

    This function used the Generalized Likelihood Ratio Test to test the
    goodness of fit: in other words, which distribution is more likely.

    In this function, we choose the powerLaw distributin to be the null
    and exponential distribution to be the alternative. We derived the
    test statistics by theory and pluged in MLE as our estimation of
    best parameters.

    After we calculated the paramters, we need to find the rejection
    region, critical value or pvalue. To get a more general test, we
    want to use pvalue, instead of critical value under certain
    significance level.

    To find the p-value, we use simulation methods, and all random
    numbers are drawn from previous functions. Therefore, although
    p value should be a constant given data, it is not a constant in
    our function, if we did not set the seed.

    In general, in this function, if the p value is too small, then we
    will reject the null, and we say powerlaw is not a better fit
    compared to exponential distribution.

    Parameters
    ----------
    strain : int
        the strain number of the mouse
    mouse : int
        the mouse number in its strain
    day :  int
        the day number
    law_est: double (optional)
        the estimated parameter in law distribution

    Returns
    -------
    p_value:
        the probablity under null reject.

    Examples
    --------
    >>> hypo_law_null (0, 0, 0)
    0.0070000000000000001
    """
    if seed != -1:
        np.random.seed(seed)
    df = data.load_movement(strain, mouse, day)
    xcood = df["x"]
    ycood = df["y"]
    distance_vector = np.sqrt(np.diff(xcood)**2 + np.diff(ycood)**2)
    msk = distance_vector > 1
    cut_dist = distance_vector[msk]
    if law_est == 0:
        law_est = 1 + len(cut_dist) * 1 / \
            (np.sum(np.log(cut_dist / np.min(cut_dist))))
    n = len(cut_dist)
    log_cut = np.log(cut_dist)
    sum_cut = np.sum(log_cut)
    test_stat = n * (np.log(sum_cut - n) - np.log(sum_cut)) - law_est * sum_cut
    sample_stat = []
    for i in range(1000):
        sample = random_powerlaw(len(cut_dist), law_est)
        sum_sam = np.sum(sample)
        log_sam = np.log(sample)
        sum_log_sam = np.log(np.sum(log_sam))
        tmp = n * (np.log(sum_sam - n) - sum_log_sam) - \
            law_est * np.sum(log_sam)
        sample_stat.append(tmp)
    # critical_value = ss.mstats.mquantiles(sample_stat, prob = 0.05)[0]
    p_value = np.sum(sample_stat > test_stat) / len(sample_stat)
    return p_value


def hypo_exp_null(strain, mouse, day, law_est=0, exp_est=0, seed=-1):
    """
    Return the outcome from GLRT with null hypothesis law distribution.

    Description
    -----------
    This function also used the Generalized Likelihood Ratio Test to test
    goodness of fit: in other words, which distribution is more likely.

    In this function, we choose the exponential distributin to be the null
    and powerlaw distribution to be the alternative. We derived the
    test statistics by theory and pluged in MLE as our estimation of
    best parameters.

    After we calculated the paramters, we need to find the rejection
    region, critical value or pvalue. To get a more general test, we
    want to use pvalue, instead of critical value under certain
    significance level.

    To find the p-value, we use simulation methods, and all random
    numbers are drawn from previous functions. Therefore, although
    p value should be a constant given data, it is not a constant in
    our function, if we did not set the seed.

    In general, in this function, if the p value is too small, then we
    will reject the null, and we say exponential is not a better fit
    compared to exponential distribution.

    Parameters
    ----------
    strain : int
        the strain number of the mouse
    mouse  : int
        the mouse number in its strain
    day       :  int
        the day number
    law_est: double (optional)
        the estimated parameter in law distribution
    exp_est: double (optional)
        the estimated parameter in exponential distribution

    Returns
    -------
    p_value:
        the probablity under null reject.

    Examples
    --------
    >>> hypo_exp_null (0, 0, 0)
    1.0
    """
    if seed != -1:
        np.random.seed(seed)
    df = data.load_movement(strain, mouse, day)
    xcood = df["x"]
    ycood = df["y"]
    distance_vector = np.sqrt(np.diff(xcood)**2 + np.diff(ycood)**2)
    msk = distance_vector > 1
    cut_dist = distance_vector[msk]
    if law_est == 0:
        law_est = 1 + len(cut_dist) * 1 / \
            (np.sum(np.log(cut_dist / np.min(cut_dist))))
    if exp_est == 0:
        exp_est = len(cut_dist) / (np.sum(cut_dist) - len(cut_dist))
    n = len(cut_dist)
    sum_cut = np.sum(cut_dist)
    log_cut = np.log(cut_dist)
    sum_log_cut = np.sum(log_cut)
    test_stat = n * (np.log(sum_cut - n) - np.log(sum_log_cut)) - \
        law_est * sum_log_cut
    sample_stat = []
    for i in range(1000):
        sample = random_exp(len(cut_dist), exp_est)
        sum_sam = np.sum(sample)
        log_sam = np.log(sample)
        sum_log_sam = np.sum(log_sam)
        tmp = n * (np.log(sum_sam - n) - np.log(sum_log_sam)) - \
            law_est * sum_log_sam
        sample_stat.append(tmp)
    # critical_value = ss.mstats.mquantiles(sample_stat, prob = 0.95)[0]
    p_value = np.sum(sample_stat <= test_stat) / len(sample_stat)
    return p_value
