from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
from mousestyles.distribution import (powerlaw_pdf, exp_pdf,
                                      powerlaw_inverse_cdf, exp_inverse_cdf)


def test_powerlaw_pdf():
    assert (powerlaw_pdf(2, 2) == 0.25)


def test_exp_pdf():
    assert (exp_pdf(2, 1) == 0.36787944117144233)


def test_powerlaw_inverse_cdf():
    y = np.arange(0, 1, 0.01)
    x = powerlaw_inverse_cdf(y, 2)
    assert (type(x) == np.ndarray)
    assert (all([item >= 1 for item in x]))
    assert (x[0] == 1)


def test_exp_inverse_cdf():
    y = np.arange(0, 1, 0.01)
    x = exp_inverse_cdf(y, 2)
    assert (type(x) == np.ndarray)
    assert (all([item >= 1 for item in x]))
    assert (x[0] == 1)
