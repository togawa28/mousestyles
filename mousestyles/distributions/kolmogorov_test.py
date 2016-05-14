from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
from scipy import stats, optimize
from mousestyles.data import load_movement


def get_travel_distances(strain=0, mouse=0, day=0):
    """ Get distances travelled in 20ms for this strain, this mouse,
    on this day.

    Parameters
    ----------
    strain: int {0, 1, 2}
        The strain of mouse to test
    mouse: int {0, 1, 2, 3}
        The mouse twin id with in the strain
    day: int {0, 1, ..., 11}
        The day to calculate the distance

    Returns
    -------
    x: np.ndarray shape (n, 1)
        The distances travelled in 20ms for this mouse on this day, truncated
        at 1cm (i.e. only record mouse movement when it moves more than 1cm)

    Examples:
    >>> get_travel_distances(0, 0, 0)[:3]
    array([ 1.00648944,  1.02094319,  1.0178885 ])
    """
    df = load_movement(strain=strain, mouse=mouse, day=day)
    x = np.array(np.sqrt(df.x.diff()**2 + df.y.diff()**2))[1:]
    x = x[x >= 1]
    return x


def perform_kstest(x, distribution=stats.pareto,
                   verbose=True):
    """This function fits a distribution to data, and then test the
    fit of the distribution using Kolmogorov-Smirnov test.

    The Kolmogorov-Smirnov test constructs the test statistic, which is defined
    as $\sup |F_n(x) - F(x)|$, for $F_n$ is the sample CDF, and F is the
    theoretical CDF. This statistics can be considered as a measure of
    distance between the sample distribution and the theoretical distribution.
    The smaller it is, the more similar the two distributions.

    We first estimate the parameter using MLE, then by minimizing the KS test
    statistic.

    The Pareto distribution is sometimes known as the Power Law distribution,
    with the PDF:  $b / x**(b + 1)$ for $x >= 1, b > 0$.
    The truncated exponential distribution is the same as the rescaled
    exponential distribution.

    Parameters
    ----------
    x: np.ndarray (n,)
        The sample data to test the distribution
    distribution: A Scipy Stats Continuous Distribution
        {stats.pareto, stats.expon, stats.gamma}
        The distribution to test against. Currently support pareto, expon, and
        gamma, but any one-sided continuous distribution in Scipy.stats should
        work.
    verbose: boolean
        If True, will print out testing result

    Returns
    -------
    params: np.ndarray shape (p,)
        The optimal parameter for the distribution. Optimal in the sense of
        minimizing K-S statistics.
    The function also print out the Kolmogorov-Smirnov test result for three
    cases
    1. When comparing the empirical distribution against the distribution with
    parameters estimated with MLE
    2. When comparing the empirical distribution against the distribution with
    parameters estimated by explicitely minimizing KS statistics
    3. When comparing a resample with replacement of the empirical distribution
    against the Pareto in 2.
    A p-value > 0.05 means we fail to reject the Null hypothesis that the
    empirical distribution follow the specified distribution.

    Notes:
    ------
    The MLE often does not fit the data very well. We instead minimizing the
    K-S distance, and obtain a better fit (as seen by the PDF and CDF
    similarity between sample data and the fit)

    References:
    -----------
        1. Kolmogorov-Smirnov test:
            https://en.wikipedia.org/wiki/Kolmogorov-Smirnov_test
        2. Pareto Distribution (also known as power law distribution)
            https://en.wikipedia.org/wiki/Pareto_distribution

    Examples:
    ---------
    >>> x = get_travel_distances(0, 0, 0)
    >>> res = perform_kstest(x, verbose=False)
    >>> np.allclose(res, np.array([3.67593246, 0.62795748, 0.37224205]))
    True
    """
    dist_name = distribution.name
    # Fit the parameters by MLE
    mle_params = distribution.fit(x)

    # Fit the Parameter by explicitely minimize KS-Statistics, and perform
    # K-S test. First define helper function to minimize
    def calculate_ks_statistics(params):
        return stats.kstest(x, dist_name, args=params)[0]

    # Define good initial parameters to help optimizer find optimal values
    if dist_name == "pareto":
        init_params = [4.5, .5, .5]
    else:
        init_params = mle_params

    opt_params = optimize.fmin(calculate_ks_statistics, x0=init_params, disp=0)
    if verbose:
        print("1. Testing {} distribution with MLE parameters".format(
            dist_name))
        print(stats.kstest(x, dist_name, args=mle_params))
        print("2. Testing {} distribution with optimal parameters".
              format(dist_name))
        print(stats.kstest(x, dist_name, args=opt_params))
        # Resample x, and test again
        x_bag = np.random.choice(x, size=len(x), replace=True)
        print("3. Similar to 2., but on a resample of x")
        print(stats.kstest(x_bag, dist_name, args=opt_params))

    return opt_params
