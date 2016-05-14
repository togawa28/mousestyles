from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import itertools

import numpy as np
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt

from mousestyles.data import distances_bymouse, distances_bystrain


def get_pvalues(m):
    """
    This function takes a bunch of sampled distributions and compute the
    p-values of the two sided Mann Whitney U test for each couple of samples.

    The Mann-Whitney U test is a test for assessing whether two independent
    samples come from the same distribution. The null hypothesis for this test
    is that the two groups have the same distribution, while the alternative
    hypothesis is that one group has larger (or smaller) values than the other.

    Null hypothesis $H_0$: $P(X>Y)=P(Y>X)$.
    Alternative $H_1: not $H_0$.

    The Mann-Whitney U test is similar to the Wilcoxon test, but can be used to
    compare multiple samples that aren't necessarily paired.

    Parameters
    ----------
    m: list of numpy arrays
        Sampled distributions.

    Returns
    -------
    cor: 2 dimensional array of pvalues.
        cor[i,j] is the p-value of the MWW test between the samples i and j.

    Notes:
    ------
    A p-value < 0.05 means that there is strong evidence to reject the null
    hypothesis.

    References:
    -----------
        1. Mann-Whitney U test:
            http://tqmp.org/RegularArticles/vol04-1/p013/p013.pdf
        2. Non parametric tests
            http://www.mit.edu/~6.s085/notes/lecture5.pdf

    Examples:
    ---------
    >>> cor = get_pvalues([np.array([1, 2, 3]), np.array([1, 1, 2])])
    """
    n = len(m)
    indices = list(itertools.product(*[range(n), range(n)]))
    cor = np.empty([n, n])
    for (a, b) in indices:
        cor[a, b] = 2 * mannwhitneyu(m[a], m[b])[1]
    return cor


def MWW_mice(strain, step=50, verbose=False):
    """
    Compare distributions of distances among mice of the same strain.
    Use p-values of the Mann-Whitney U test.

    Parameters
    ----------
    strain: integer
        Number of the strain.
    step: floeat
        Time interval length used to compute distances. Default is 1s.
        See data.distances_bymouse for more information.
    verbose: boolean

    Returns
    -------
    cor: pvalues of the Mann-Whitney U test for each couple of distances
        samples among mice of the corresponding strain.

    Examples:
    ---------
    >>> cor = MWW_mice(0)
    """
    mouse = 0
    res = []
    dist = np.array([0])
    while dist.size > 0:
        dist = distances_bymouse(strain, mouse,
                                 step=step)
        res.append(dist)
        mouse += 1
        if verbose:
            print('mouse %s done.' % mouse)
    cor = get_pvalues(res[:-1])
    return cor


def MWW_allmice(step=50, verbose=False):
    """ Aggregates MWW_mice data for all available strains of mice.

    Parameters
    ----------
    step: time interval length used to compute distances. Default is 1s.
        See data.distances_bymouse for more information.
    verbose: boolean

    Returns
    -------
    mww_values: MWW_mice outputs for each strain.
        mww_values[i] corresponds to the ith strain.

    Examples:
    ---------
    >>> mww_values = MWW_allmice()
    """
    strain = 0
    mww = np.array([0])
    mww_values = []
    while mww.size > 0:
        mww = MWW_mice(strain, verbose=False)
        mww_values.append(mww)
        if verbose:
            print('strain %s done.' % strain)
        strain += 1
    mww_values = mww_values[:-1]
    return mww_values


def MWW_strains(step=50, verbose=False):
    """
    Compare distributions of distances among strains. Proceed as if
    the mice in each strain are i.i.d. samples, and compare the p-values
    of the Mann-Whitney U test.

    Parameters
    ----------
    step: time interval length used to compute distances. Default is 1s.
        See data.distances_bymouse for more information.
    verbose: boolean

    Returns
    -------
    cor: pvalues of the Mann-Whitney U test for each couple of distances
        samples among strains of mice.

    Examples:
    ---------
    >>> cor = MWW_strains()
    """
    strain = 0
    res = []
    dist = np.array([0])
    while dist.size > 0:
        dist = distances_bystrain(strain,
                                  step=step)
        res.append(dist)
        if verbose:
            print('strain %s done.' % strain)
        strain += 1
    cor = get_pvalues(res[:-1])
    return cor


def plot_cor(data):
    """
    Plot the p-values outputed by the Mann-Whitney U test using
    a correlation matrix representation.

    Parameters
    ----------
    data: MWW_allmice output

    Returns
    -------
    plot: correlation matrix

    Examples:
    --------
    >>> strains = MWW_strains()
    >>> plot_cor(strains)
    """
    plt.style.use('seaborn-notebook')

    n = len(data)
    column_labels = range(n)
    row_labels = range(n)
    fig, ax = plt.subplots()
    ax.pcolor(data, cmap=plt.cm.Blues)

    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    ax.set_xticklabels(row_labels, minor=False)
    ax.set_yticklabels(column_labels, minor=False)
    plt.ylabel('Strains')
    plt.xlabel('Strains')
    plt.show()


def plot_cor_multi(mww_values):
    """
    Vectorized version of plot_cor. Plot several correlation
    matrices side by side using plot_cor.

    Parameters
    ----------
    data: MWW_allmice output

    Returns
    -------
    plot: correlation matrix
    Examples:
    --------
    >>> allmice = MWW_allmice()
    >>> plot_cor_multi(allmice)
    """
    plt.style.use('seaborn-notebook')

    nb_plots = len(mww_values)
    fig, ax = plt.subplots(nb_plots, sharex=True)
    fig.subplots_adjust(hspace=.4)
    for i, mww in enumerate(mww_values):
        ax[i].pcolor(mww, cmap=plt.cm.Blues)
        labels = range(len(mww))

        ax[i].set_xticklabels(labels, minor=False)
        ax[i].set_yticklabels(labels, minor=False)
        ax[i].set_xticks(np.arange(mww.shape[0]) + 0.5, minor=False)
        ax[i].set_yticks(np.arange(mww.shape[1]) + 0.5, minor=False)
        ax[i].set_ylabel('Mouse')
        ax[i].set_title('strain %s' % i)

    plt.xlabel('Mouse')
    plt.show()
