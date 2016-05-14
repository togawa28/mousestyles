from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from mousestyles.GLRT_distribution import (random_powerlaw, random_exp,
                                           hypo_powerLaw_null, hypo_exp_null)


def test_random_powerlaw():
    assert (abs(random_powerlaw(1, 3, 0)[0] - 1.48875061) <= 1e-7)


def test_random_exp():
    assert (abs(random_exp(1, 2, 0)[0] - 1.39793725) <= 1e-7)


def test_hypo_powerLaw_null():
    assert abs(hypo_powerLaw_null(0, 0, 0, 0) - 0) <= 1e-7


def test_hypo_exp_null():
    assert abs(hypo_exp_null(0, 0, 0, seed=0) - 1.0) <= 1e-7
