import matplotlib.pyplot as plt
import numpy as np
from mousestyles.ultradian import strain_seasonal
from mousestyles.ultradian import find_cycle

ALL_FEATURES = ["AS", "F", "M_AS", "M_IS", "W", "Distance"]


def plot_strain_seasonal(strains, mouse, feature, bin_width, period_length):
    """
    Use seansonal decomposition model on the time series
    of specified strain, mouse, feature and bin_width.
    return the seasonal term and the plot of seasonal term
    by mouse of a set of mouses in a strain

    Parameters
    ----------
    strain: list, set or tuple
        nonnegative integer indicating the strain number
    mouse: list, set or tuple
        nonnegative integer indicating the mouse number
    feature: {"AS", "F", "M_AS", "M_IS", "W", "Distance"}
        "AS": Active state probalibity
        "F": Food consumed (g)
        "M_AS": Movement outside homebase
        "M_IS": Movement inside homebase
        "W": Water consumed (g)
        "Distance": Distance traveled
    bin_width: int
        number of minutes, the time interval for data aggregation
    period_length: float or int
        number of hours, usually the significant period
        length indicated by Lomb-scargle model

    Returns
    -------
    seasonal_plot: plot of seasonal term by mouse

    Examples
    --------
    >>> res = plot_strain_seasonal(strains={0, 1, 2,}, mouse={0, 1, 2, 3},
                                   feature="W",
                                   bin_width=30, period_length = 24)
    """

    if (not all([isinstance(m, int)
                 for m in mouse])) or (any([m < 0 for m in mouse])):
        raise ValueError(
            'Strain must be a non-negative integer')
    if (not all([isinstance(m, int)
                 for m in mouse])) or (any([m < 0 for m in mouse])):
        raise ValueError(
            'Mouse value must be a non-negative integer')
    if feature not in ALL_FEATURES:
        raise ValueError(
            'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}')
    if (not isinstance(bin_width, int)) or bin_width < 0 or bin_width > 1440:
        raise ValueError(
            'Bin width (minutes) must be a non-negative integer below 1440')
    if period_length < 0:
        raise ValueError(
            'Peoriod length must be a non-negative float or int')

    time = np.arange(0, period_length, bin_width / 60)
    fig = plt.figure(figsize=(8, 8))
    flag = 0

    for strain in strains:
        if flag == 0:
            ax = fig.add_subplot(3, 1, strain + 1)
            flag += 1
        else:
            ax = fig.add_subplot(3, 1, strain + 1, sharey=ax)
        seasonal_all = strain_seasonal(strain, mouse, feature,
                                       bin_width, period_length)
        for i in np.arange(len(mouse)):
            ax.plot(time, seasonal_all[i, :])
        ax.legend(['mouse' + str(i) for i in np.arange(len(mouse))],
                  loc='upper right', prop={'size': 10})
        ax.set_title('strain ' + str(strain))
        plt.xlabel('Time')
        plt.ylabel('Seasonal Variation')
    plt.suptitle(feature, fontsize=20)
    fig.show()

    return(fig)


def compare_strain(feature, n_strain=3, bin_width=15, disturb_t=False):
    """
    Use the data from function find_cycle and plotting method from function
    lombscargle_visualize to compare the Lomb-Scargle plots between different
    strains.

    Parameters
    ----------
    feature: string in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}
        "AS": Active state probalibity
        "F": Food consumed (g)
        "M_AS": Movement outside homebase
        "M_IS": Movement inside homebase
        "W": Water consumed (g)
        "Distance": Distance traveled
    n_strain: int, defalt is 3
        nonnegative integer indicating total number of strains to be compared
    bin_width: int, minute unit, default is 15 minutes
        number of minutes, the time interval for data aggregation
    disturb_t: boolean, default is False
        If True, add uniformly distributed noise to the time sequence which
        are used to fit the Lomb Scargle model. This is to avoid the singular
        matrix error that could happen sometimes.

    Returns
    -------
    Lomb Scargle Power versus Periods (hours) plot with significant levels.

    Examples
    -------

    """
    if feature not in ALL_FEATURES:
        raise ValueError(
            'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}')

    fig = plt.figure(figsize=(16, 8))

    for i in range(n_strain):
        ax = fig.add_subplot(1, n_strain, i + 1)
        periods, power, sig, N, cycle, cycle_power, cycle_pvalue = find_cycle(
            feature=feature, strain=i, bin_width=bin_width,
            methods='LombScargleFast', disturb_t=disturb_t,
            gen_doc=True, plot=False)
        ax.plot(periods, power, color='steelblue')
        ax.set(xlim=(0, 26), ylim=(0, max(cycle_power)),
               xlabel='Period (hours)',
               ylabel='Lomb-Scargle Power')
        ax.set_title('strain' + str(i))
        for i in sig:
            power_sig = -2 / (N - 1) * np.log(
                1 - (1 - np.asarray(i)) ** (1 / 2 / N))
            plt.axhline(y=power_sig, color='green', ls='dashed', lw=1)
            ax.text(x=24, y=power_sig, s='P-value:' +
                    str(float(i)), ha='right', va='bottom')
            idx = [i for i, x in enumerate(cycle_pvalue) if x < 0.001]
            for j in idx:
                if cycle[j] > min(periods) and cycle[j] < max(periods):
                    ax.text(x=cycle[j], y=cycle_power[j],
                            s=r'$\bigstar\bigstar\bigstar$',
                            ha='right', va='top')
            idx = [i for i, x in enumerate(
                cycle_pvalue) if x > 0.001 and x < 0.01]
            for j in idx:
                if cycle[j] > min(periods) and cycle[j] < max(periods):
                    ax.text(x=cycle[j], y=cycle_power[
                            j], s=r'$\bigstar\bigstar$', ha='right', va='top')
            idx = [i for i, x in enumerate(
                cycle_pvalue) if x > 0.01 and x < 0.05]
            for j in idx:
                if cycle[j] > min(periods) and cycle[j] < max(periods):
                    ax.text(x=cycle[j], y=cycle_power[j],
                            s=r'$\bigstar$', ha='right', va='top')

    plt.suptitle('Feature: ' + feature, fontsize=20)

    return fig
