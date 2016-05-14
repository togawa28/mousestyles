import matplotlib.pyplot as plt
import numpy as np
from mousestyles.distribution import (powerlaw_pdf, exp_pdf,
                                      powerlaw_inverse_cdf, exp_inverse_cdf)
from mousestyles.est_power_param import (fit_powerlaw, fit_exponential,
                                         getdistance)
from mousestyles.kde import kde


def plot_powerlaw(estimation):
    """
    Return the histogram of all estimators of power law
    to check the distribution.

    Parameters
    ----------
    estimation: dataframe
        dataframe of strain, mouse, day and the estimator

    Returns
    -------
    plot : histogram
        The histogram of all estimators of power law
    """
    plt.hist(list(estimation.ix[estimation["strain"] == 0, 3]))
    plt.hist(list(estimation.ix[estimation["strain"] == 1, 3]))
    plt.hist(list(estimation.ix[estimation["strain"] == 2, 3]))
    plt.title("Histogram: Power Law parameters distribution by strain")


def plot_exponential(estimation):
    """
    Return the histogram of all estimators of exponential
    to check the distribution.

    Parameters
    ----------
    estimation: dataframe
        dataframe of strain, mouse, day and the estimator

    Returns
    -------
    plot : histogram
        The histogram of all estimators of exponential.
    """
    plt.hist(list(estimation.ix[estimation["strain"] == 0, 4]))
    plt.hist(list(estimation.ix[estimation["strain"] == 1, 4]))
    plt.hist(list(estimation.ix[estimation["strain"] == 2, 4]))
    plt.title("Histogram: Exponential parameters distribution by strain")


def plot_fitted(strain, mouse, day, hist=True, density=False):
    """
    Return the plot of one single mouse day
    -fitted power law
    -fitted exponential
    -histogram of distance
    -kernel density curve

    Parameters
    ----------
    strain : int
        the strain number of the mouse
    mouse  : int
        the mouse number in its strain
    day :  int
        the day number
    hist : boolean
        Plot histogram if True
    density : boolean
        plot density if True

    Returns
    -------
    plot : 1 histogram (blue) + 2 fitted curve + 1 density (cyan)
    """
    fig, ax = plt.subplots(1, 1)
    x = np.arange(1, 2.7, 0.01)
    alpha = fit_powerlaw(strain, mouse, day)
    lamb = fit_exponential(strain, mouse, day)
    cut_dist = getdistance(strain, mouse, day)
    ax.plot(x, powerlaw_pdf(x, alpha), 'r-', lw=2, alpha=2,
            label='powerlaw pdf')
    ax.plot(x, exp_pdf(x, lamb), 'y-', lw=2, alpha=2,
            label='exp pdf')
    if hist:
        weights = np.ones_like(cut_dist) / len(cut_dist) * (alpha - 1)
        ax.hist(cut_dist, weights=weights, bins=np.arange(1, 2.6, 0.1))
    if density:
        np.random.seed(0)
        sample_cut_dist = np.random.choice(cut_dist, 1000, replace=False)
        pdf = kde(sample_cut_dist, x_grid=x, symmetric_correction=True,
                  cutoff=1)
        ax.plot(x, pdf, 'c', lw=2, alpha=2,
                label='powerlaw pdf')


def plot_relative_dist(strain, mouse, day):
    """
    Return the relative distribution of distance of a single mouse day
    The relative distribution of a comparison distribution with density g
    vs a reference distribution with density f is g(F^(-1)(x))/f(F^(-1)(x))
    It's a prob distribution on [0, 1].

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
    pdf_rel_power : numpy.ndarray
        the relative distribution, referencing the best fit powerlaw
        distribution, at grid points np.arange(0, 1.0, 0.02)
    pdf_rel_exp : numpy.ndarray
        the relative distribution, referencing the best fit exponential
        distribution, at grid points np.arange(0, 1.0, 0.02)
    """
    # calculate the best fit parameters for powerlaw and exponential
    alpha = fit_powerlaw(strain, mouse, day)
    lamb = fit_exponential(strain, mouse, day)
    # set up the grid points on [0, 1]
    x = np.arange(0, 1.0, 0.02)
    # transform x to F^(-1)(x) = y
    y_grid_power = powerlaw_inverse_cdf(x, alpha)
    y_grid_exp = exp_inverse_cdf(x, lamb)
    cut_dist = getdistance(strain, mouse, day)
    # to save computation, we do random sampling
    np.random.seed(0)
    sample_cut_dist = np.random.choice(cut_dist, 1000, replace=False)
    # get the corresponding density at points y
    pdf_grid_power = kde(sample_cut_dist, x_grid=y_grid_power,
                         symmetric_correction=True, cutoff=1)
    pdf_grid_exp = kde(sample_cut_dist, x_grid=y_grid_exp,
                       symmetric_correction=True, cutoff=1)
    # calculate the ratio as relative distribution
    pdf_rel_power = pdf_grid_power / powerlaw_pdf(y_grid_power, alpha)
    pdf_rel_exp = pdf_grid_exp / exp_pdf(y_grid_exp, lamb)
    # plot the relative distribution
    fig, ax = plt.subplots(1, 2)
    ax[0].plot(x, pdf_rel_power, lw=2, alpha=2, c='b',
               label='Relative distribution, powerlaw')
    ax[0].axhline(y=1, c='r')
    ax[1].plot(x, pdf_rel_exp, lw=2, alpha=2, c='b',
               label='Relative distribution, exponential')
    ax[1].axhline(y=1, c='r')
