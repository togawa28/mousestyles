# coding: utf-8
import numpy as np

from mousestyles.mww import (get_pvalues, MWW_mice, MWW_allmice,
                             MWW_strains)


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


def test_MWW_mice_type():
    cor = MWW_mice(0)
    assert(type(cor) == np.ndarray)


def test_MWW_mice_similarity():
    # Similarity when comparing with the same mouse
    cor = MWW_mice(0)
    assert(cor[0, 0] > 0.95)


def test_MWW_allmice_type():
    mww_values = MWW_allmice()
    assert(type(mww_values) == list)


def test_MWW_allmice_first():
    # See whether the first element matches
    cor = MWW_mice(0)
    mww_values = MWW_allmice()
    assert(np.all(mww_values[0] == cor))


def test_MWW_strains_type():
    cor = MWW_strains()
    assert(type(cor) == np.ndarray)


def test_MWW_strains_similarity():
    # Similarity when comparing with the same strain
    cor = MWW_strains()
    assert(cor[0, 0] > 0.95)
