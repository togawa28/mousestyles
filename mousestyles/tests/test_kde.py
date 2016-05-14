import numpy as np
from scipy.stats.distributions import norm
from mousestyles.kde import kde


def test_kde():
    pdf = kde(x=np.array([2, 3, 1, 0]), x_grid=np.linspace(0, 5, 10))
    assert (type(pdf) == np.ndarray)
    assert all([item >= 0 for item in pdf])
    assert (len(pdf) == 10)
    x1 = np.concatenate([norm(-1, 1.).rvs(400),
                        norm(1, 0.3).rvs(100)])
    pdf = kde(x=x1)
    assert (type(pdf) == np.ndarray)
    assert all([item >= 0 for item in pdf])
    assert (len(pdf) == 300)
