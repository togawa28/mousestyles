from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np


def powerlaw_pdf(x, a):
    """
    The probability density function of truncated power law.

    Parameters
    ----------
    x : float > 0, or a np.dnarray
        x in formula p(x)=(alpha-1)*x^(-alpha).
    a : float > 1
        alpha in formula p(x)=(alpha-1)*x^(-alpha).

    Returns
    -------
    probability density : float
        The probability density of power law at x.

    Examples
    --------
    >>> powerlaw_pdf (2, 2)
    0.25
    """
    return (a - 1) * x ** (-a)


def exp_pdf(x, l):
    """
    The probability density function of truncated exponential.

    Parameters
    ----------
    x : float, or a np.dnarray
        x in formula p(x)=lambda*exp(-lambda*x).
    l : float
        lambda in formula p(x)=lambda*exp(-lambda*x).

    Returns
    -------
    probability density : float
        The probability density of power law at x.

    Examples
    --------
    >>> exp_pdf(1, 1)
    0.36787944117144233
    """
    return l * np.exp(-l * (x - 1))


def powerlaw_inverse_cdf(y, a):
    """
    The inverse CDF function of power law distribution

    Parameters
    ----------
    y : float in [0, 1], or a np.dnarray
        y in formula F^(-1)(y) = (1 - y)^(1/(1-a))
    a : float > 1
        a in formula F^(-1)(y) = (1 - y)^(1/(1-a))

    Returns
    -------
    x : float
        The inverse CDF function of power law distribution with
        parameter a at point y

    Examples
    --------
    >>> powerlaw_inverse_cdf(0.5, 5)
    1.189207115002721
    """
    return (1 - y)**(1/(1-a))


def exp_inverse_cdf(y, l):
    """
    The inverse CDF function of truncated (at 1) exponential distribution

    Parameters
    ----------
    y : float in [0, 1], or a np.dnarray
        y in formula F^(-1)(y) = 1 - log(1 - y) / l
    l : float > 0
        a in formula F^(-1)(y) = 1 - log(1 - y) / l

    Returns
    -------
    x : float
        The inverse CDF function of truncated (at 1) exponential distribution
        distribution with parameter l at point y

    Examples
    --------
    >>> exp_inverse_cdf(0.6,2)
    1.4581453659370776
    """
    return 1 - np.log(1 - y) / l
