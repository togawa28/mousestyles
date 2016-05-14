from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
from scipy import stats
from mousestyles.distributions.kolmogorov_test import perform_kstest
from mousestyles.distributions.kolmogorov_test import get_travel_distances


def test_get_travel_distances():
    # testing the function that gets the distances travelled by a mouse within
    # 20 millisecond, truncated to >= 1cm
    res = get_travel_distances(strain=0, mouse=0, day=0)
    assert type(res) is np.ndarray
    # check that all the distances are actually >= 1
    assert np.all(res >= 1)


def test_perform_kstest1():
    # check the kolgomorov test for the pareto distribution
    x = get_travel_distances(0, 0, 0)
    res = perform_kstest(x, distribution=stats.pareto, verbose=False)
    assert type(res) is np.ndarray
    assert res.shape == (3,)
    # Since our mouse distances data is truncated at 1, the sum of loc and
    # scale parameter in pareto distribution should be close to 1
    assert np.abs(res[1] + res[2] - 1) <= .1


def test_perform_kstest2():
    # check the kolgomorov test for the exponential distribution
    x = get_travel_distances(1, 1, 1)
    res = perform_kstest(x, distribution=stats.expon, verbose=True)
    assert type(res) is np.ndarray
    assert res.shape == (2,)
    # Since our mouse distances data is truncated at 1, the loc parameter in
    # exponential distribution should be close to 1
    assert np.abs(res[0] - 1) <= .1
