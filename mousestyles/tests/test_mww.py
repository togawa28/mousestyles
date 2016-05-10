# coding: utf-8
import numpy as np

from mousestyles.mww import get_pvalues


def test_pvalues_type():
    poisson = np.random.poisson(2, size=100)
    normal = np.random.normal(loc=10, scale=2, size=50)
    cor = get_pvalues([poisson, normal])
    assert (type(cor) == np.ndarray)


def test_pvalues_size():
    poisson = np.random.poisson(2, size=100)
    normal = np.random.normal(loc=10, scale=2, size=50)
    cor = get_pvalues([poisson, normal])
    assert (cor.size == 4)


def test_pvalues_similarity():
    # test p values for close distributions
    poisson = np.random.poisson(2, size=100)
    normal = np.random.normal(loc=10, scale=2, size=50)
    cor = get_pvalues([poisson, normal])
    assert (cor[0, 0] > 0.95 and cor[1, 1] > 0.95)


def test_pvalues_difference():
    # test p values for very different distributions
    poisson = np.random.poisson(2, size=100)
    normal = np.random.normal(loc=10, scale=2, size=50)
    cor = get_pvalues([poisson, normal])
    assert (cor[0, 1] < 0.05)
