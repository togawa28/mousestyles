import matplotlib.pyplot as plt
import numpy as np


def lombscargle_visualize(periods, power, sig, N, cycle,
                          cycle_power, cycle_pvalue):
    """
    Use Lomb-Scargel method on different strain and mouse's data to find the
    best possible periods with highest p-values, and plot the Lomb Scargle
    power versus periods plot. use the periods as time sequence to predict
    the corresponding LS power, draw the plot.

    There will also be stars and horizontal lines indicating the p-value of
    significance. Three stars will be p-value in [0,0.001], two stars will be
    p-value in [0.001,0.01], one star will be p-value in [0.01,0.05]. The
    horizontal line is the LS power that has p-value of 0.05.

    Parameters
    ----------
    periods: numpy array of the same length with 'power'
        use as time sequence in LS model to make predictions
    power: numpy array of the same length with 'periods'
        the corresponding predicted power of periods
    sig: list, tuple or numpy array, default is [0.05].
        significance level to be used for plot horizontal line.
    N: int
        the length of time sequence in the fit model
    cycle: numpy array
        periods
    cycle_power: numpy array
        LS power corrsponding to the periods in 'cycle'
    cycle_pvalue: numpy array
        p-values corresponding to the periods in 'cycle'

    Returns
    -------
    Lomb Scargle Power versus Periods (hours) plot with significant levels.

    Examples
    --------

    """
    fig, ax = plt.subplots()
    ax.plot(periods, power, color='steelblue')
    ax.set(xlim=(0, 26), ylim=(0, max(cycle_power)),
           xlabel='Period (hours)',
           ylabel='Lomb-Scargle Power')

    for i in sig:
        power_sig = -2 / (N - 1) * np.log(
            1 - (1 - np.asarray(i)) ** (1 / 2 / N))
        plt.axhline(y=power_sig, color='green', ls='dashed', lw=1)
        ax.text(x=24, y=power_sig, s='P-value:' +
                str(float(i)), ha='right', va='bottom')
        idx = [i for i, x in enumerate(cycle_pvalue) if x < 0.001]
        for j in idx:
            if cycle[j] > min(periods) and cycle[j] < max(periods):
                ax.text(x=cycle[j],
                        y=cycle_power[j], s=r'$\bigstar\bigstar\bigstar$',
                        ha='right', va='top')
        idx = [i for i, x in enumerate(cycle_pvalue) if x > 0.001 and x < 0.01]
        for j in idx:
            if cycle[j] > min(periods) and cycle[j] < max(periods):
                ax.text(x=cycle[j], y=cycle_power[j],
                        s=r'$\bigstar\bigstar$', ha='right', va='top')
        idx = [i for i, x in enumerate(cycle_pvalue) if x > 0.01 and x < 0.05]
        for j in idx:
            if cycle[j] > min(periods) and cycle[j] < max(periods):
                ax.text(x=cycle[j], y=cycle_power[j],
                        s=r'$\bigstar$', ha='right', va='top')
