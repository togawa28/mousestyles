import matplotlib.pyplot as plt
import numpy as np
from mousestyles.distribution import (powerlaw_pdf, exp_pdf,
                                      powerlaw_inverse_cdf, exp_inverse_cdf)
from mousestyles.est_power_param import (fit_powerlaw, fit_exponential,
                                         getdistance)
from mousestyles.kde import kde


def plot_kernel(strain, mouse, day):
    """
    Return the histogram and kernel density of one single mouse day

    Parameters
    ----------
    strain : int
        the strain number of the mouse
    mouse  : int
        the mouse number in its strain
    day :  int
        the day number

    Returns
    -------
    plot : 1 histogram (blue) 1 density (cyan)
        """
    fig, ax = plt.subplots(1, 1)
    x = np.arange(1, 2.7, 0.01)
    cut_dist = getdistance(strain, mouse, day)
    alpha = fit_powerlaw(strain, mouse, day)
    weights = np.ones_like(cut_dist) / len(cut_dist) * 10
    ax.hist(cut_dist, weights=weights, bins=np.arange(1, 2.6, 0.1))
    np.random.seed(0)
    sample_cut_dist = np.random.choice(cut_dist, 1000, replace=False)
    pdf = kde(sample_cut_dist, x_grid=x, symmetric_correction=True,
              cutoff=1)
    ax.plot(x, pdf, 'c', lw=2, alpha=2,
            label='kernel pdf')

plot_kernel(0, 2, 5)
