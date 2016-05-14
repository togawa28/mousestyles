import numpy as np
from scipy.stats.distributions import norm
from mousestyles.kde import kde


def test_kde():
    pdf = kde(x=np.array([2, 3, 1, 0]), x_grid=np.linspace(0, 5, 10))
    # check function kde returns an np.ndarray
    assert (type(pdf) == np.ndarray)
    # check function kde returns array with all nonnegative numbers
    assert all([item >= 0 for item in pdf])
    # check function kde returns array with length the same as length of x_grid
    assert (len(pdf) == 10)

    x1 = np.concatenate([norm(-1, 1.).rvs(400),
                        norm(1, 0.3).rvs(100)])
    
    # check kde works fine for a more complicated input, and the default value
    # of x_grid works fine
    pdf = kde(x=x1, x_grid=np.linspace(0, 5, 10))
    # check function kde returns an np.ndarray
    assert (type(pdf) == np.ndarray)
    # check function kde returns array with all nonnegative numbers
    assert all([item >= 0 for item in pdf])
    # check function kde returns array with length the same as length of x_grid
    assert (len(pdf) == 10)
    
    pdf = kde(x=x1, x_grid=np.linspace(0, 5, 100), symmetric_correction
              =True, cutoff=1)
    # check function kde returns an np.ndarray
    assert (type(pdf) == np.ndarray)
    # check function kde returns array with all nonnegative numbers
    assert all([item >= 0 for item in pdf])
    # check function kde returns array with length the same as length of x_grid
    assert (len(pdf) == 100)