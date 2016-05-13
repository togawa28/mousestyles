from __future__ import print_function, absolute_import, division

from gatspy.periodic import LombScargleFast
from gatspy.periodic import LombScargle
import matplotlib.pyplot as plt
import mousestyles.data as data
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import chi2
plt.style.use('ggplot')


INTERVAL_FEATURES = ["AS", "F", "M_AS", "M_IS", "W"]
ALL_FEATURES = ["AS", "F", "M_AS", "M_IS", "W", "Distance"]


def aggregate_interval(strain, mouse, feature, bin_width):
    """
    Aggregate the interval data based on n-minute time
    intervals, return a time series.

    Parameters
    ----------
    strain: int
        nonnegative integer indicating the strain number
    mouse: int
        nonnegative integer indicating the mouse number
    feature: {"AS", "F", "M_AS", "M_IS", "W"}
        "AS": Active state probalibity
        "F": Food consumed (g)
        "M_AS": Movement outside homebase
        "M_IS": Movement inside homebase
        "W": Water consumed (g)
    bin_width: number of minutes of time interval for data aggregation

    Returns
    -------
    ts: pandas.tseries
        a pandas time series of length 12(day)*24(hour)*60(minute)/n
    """
    # Input Check

    if (not isinstance(strain, int)) or (strain < 0):
        raise ValueError(
            'Strain must be a non-negative integer')
    if (not isinstance(mouse, int)) or (mouse < 0):
        raise ValueError(
            'Mouse value must be a non-negative integer')
    if feature not in INTERVAL_FEATURES:
        raise ValueError(
            'Input value must in {"AS", "F", "M_AS", "M_IS", "W"}')
    if (not isinstance(bin_width, int)) or bin_width < 0 or bin_width > 1440:
        raise ValueError(
            'Bin width (minutes) must be a non-negative integer below 1440')

    # load data
    intervals = data.load_intervals(feature)
    mouse_data = intervals.loc[
        (intervals['strain'] == strain) & (intervals['mouse'] == mouse)]

    # build data frame
    days = sorted(np.unique(mouse_data['day']))
    bin_count = int(24 * 60 / bin_width)
    time_behaviour = np.repeat(0.0, bin_count * len(days))
    bin_length = bin_width * 60

    for j in days:
        df = mouse_data.loc[mouse_data['day'] == j]
        start_end = data.load_start_time_end_time(strain, mouse, j)
        start = np.asarray(df['start']) - start_end[0]
        end = np.asarray(df['stop']) - start_end[0]

        for i in range(len(start)):
            start_time = start[i]
            end_time = end[i]
            start_index = int(start_time / (bin_width * 60))
            end_index = int(end_time / (bin_width * 60))
            if start_index == end_index:
                time_behaviour[start_index + j *
                               bin_count] += end_time - start_time
            elif end_index - start_index == 1:
                time_behaviour[
                    start_index + j *
                    bin_count] += bin_length * end_index - start_time
                time_behaviour[end_index + j *
                               bin_count] += end_time % bin_length
            else:
                time_behaviour[
                    start_index + j *
                    bin_count] += bin_length * (start_index + 1) - start_time
                time_behaviour[end_index + j *
                               bin_count] += end_time % bin_length
                time_behaviour[start_index + j * bin_count +
                               1:end_index + j * bin_count] += bin_length

    if feature == 'F' or feature == 'W':
        all_feature = data.load_all_features()
        group = all_feature[
            ["strain", "mouse", "day", "hour", "Food", "Water"]].groupby(
            ["strain", "mouse", "day"]).sum()
        group = group.reset_index()
        mouse_data = group.loc[(group['strain'] == strain) &
                               (group['mouse'] == mouse)].copy()
        mouse_data.loc[:, 'day'] = np.arange(len(mouse_data))
        for i in mouse_data['day'].astype('int'):
            if feature == 'F':
                food_amount = float(mouse_data['Food'][mouse_data['day'] == i])
                time_behaviour[
                    (bin_count * i):(bin_count * (i + 1))] /= sum(
                    time_behaviour[(bin_count * i):(bin_count * (i + 1))])
                time_behaviour[(bin_count * i):(bin_count *
                                                (i + 1))] *= food_amount
            else:
                food_amount = float(mouse_data['Water'][
                                    mouse_data['day'] == i])
                time_behaviour[
                    (bin_count * i):(bin_count * (i + 1))] /= sum(
                    time_behaviour[(bin_count * i):(bin_count * (i + 1))])
                time_behaviour[(bin_count * i):(bin_count *
                                                (i + 1))] *= food_amount
    if feature == 'AS':
        time_behaviour /= (bin_width * 60)

    ts = pd.Series(time_behaviour, index=pd.date_range(
        '01/01/2014', periods=len(time_behaviour),
        freq=str(bin_width) + 'min'))
    return(ts)


def aggregate_movement(strain, mouse, bin_width):
    """
    Aggregate the movement data based on n-minute
    time intervals, return a time series.

    Parameters
    ----------
    strain: int
        nonnegative integer indicating the strain number
    mouse: int
        nonnegative integer indicating the mouse number
    bin_width: number of minutes of time interval for data aggregation

    Returns
    -------
    ts: pandas.tseries
        a pandas time series of length (#day)*24(hour)*60(minute)/n
    """
    # Input Check
    if (not isinstance(strain, int)) or (strain < 0):
        raise ValueError(
            'Strain must be a non-negative integer')
    if (not isinstance(mouse, int)) or (mouse < 0):
        raise ValueError(
            'Mouse value must be a non-negative integer')
    if (not isinstance(bin_width, int)) or bin_width < 0 or bin_width > 1440:
        raise ValueError(
            'Bin width (minutes) must be a non-negative integer below 1440')

    # determine number of days
    intervals = data.load_intervals('IS')
    mouse_data = intervals.loc[
        (intervals['strain'] == strain) & (intervals['mouse'] == mouse)]
    days = sorted(np.unique(mouse_data['day']))

    # build data frame
    bin_count = int(24 * 60 / bin_width)
    time_movements = np.repeat(0.0, bin_count * len(days))
    bin_length = bin_width * 60
    for j in days:
        M = data.load_movement(strain, mouse, day=int(j))
        distance_df = pd.DataFrame({"start": M["t"].values[0:-1],
                                    "end": M["t"].values[1:],
                                    "distance":
                                    np.linalg.norm(M[["x", "y"]].values[1:] -
                                                   M[["x", "y"]].values[0:-1],
                                                   axis=1)})
        start_end = data.load_start_time_end_time(strain, mouse, j)
        start = np.asarray(distance_df['start']) - start_end[0]
        end = np.asarray(distance_df['end']) - start_end[0]
        dist = distance_df['distance']
        for i in range(len(start)):
            start_time = start[i]
            end_time = end[i]
            start_index = int(start_time / (bin_width * 60))
            end_index = int(end_time / (bin_width * 60))
            if start_index == end_index:
                time_movements[start_index + j *
                               bin_count] += dist[i]
            else:
                time_movements[
                    end_index + j * bin_count] += end_time % \
                    bin_length / (end_time - start_time) * dist[i]
                time_movements[
                    start_index + j * bin_count] += dist[i] - \
                    end_time % bin_length / (end_time - start_time) * dist[i]
    ts = pd.Series(time_movements, index=pd.date_range(
        '01/01/2014', periods=len(time_movements),
        freq=str(bin_width) + 'min'))
    return(ts)


def aggregate_data(feature, bin_width, nmouse=4, nstrain=3):
    r"""
    Aggregate all the strains and mouses with any feature together
    in one dataframe. It combines the results you got from
    aggregate_movements and aggregate_interval. It will return
    a dataframe with three variables: mouse, strain, feature and hour.

    Parameters
    ----------
    feature :
        {"AS", "F", "IS", "M_AS", "M_IS", "W", "Distance"}
    bin_width : int
        Number of minutes, the time interval for data aggregation.

    Returns
    -------
    pandas.dataframe
    describe :
        Column 0: the mouse number (number depends on strain)(0-3)
        Column 1: the strain of the mouse (0-2)
        Column 2: hour(numeric values below 24 accourding to bin_width)
        Column 3: feature values

    Examples
    --------
    >>> test = aggregate_data("Distance",20)
    >>> print(np.mean(test["Distance"]))
    531.4500177747973
    """
    if feature not in ALL_FEATURES:
        raise ValueError(
            'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}')
    if (not isinstance(bin_width, int)) or bin_width < 0 or bin_width > 1440:
        raise ValueError(
            'Bin width (minutes) must be a non-negative integer below 1440')

    init = pd.DataFrame(columns=["mouse", "strain", "hour", feature])
    for i in range(nstrain):
        for j in range(nmouse):
            if feature == "Distance":
                tmp = aggregate_movement(strain=i, mouse=j,
                                         bin_width=bin_width)
            else:
                tmp = aggregate_interval(strain=i, mouse=j,
                                         feature=feature,
                                         bin_width=bin_width)
            tmp = pd.DataFrame(list(tmp.values), index=tmp.index)
            tmp.columns = [feature]
            tmp["strain"] = i
            tmp["mouse"] = j
            tmp["hour"] = tmp.index.hour + tmp.index.minute / 60
            init = init.append(tmp)
    return(init)


def seasonal_decomposition(strain, mouse, feature, bin_width, period_length):
    """
    Apply seasonal decomposition model on the time series
    of specified strain, mouse, feature and bin_width.

    Parameters
    ----------
    strain: int
        nonnegative integer indicating the strain number
    mouse: int
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
    period_length: int
        number of hours, usually the significant period
        length indicated by Lomb-scargle model

    Returns
    -------
    res: statsmodel seasonal decomposition object
        seasonal decomposition result for the mouse.
        Check the seasonal decomposition plot by res.plot(),
        seasonl term and trend term by res.seasonal and
        res.trend separately.

    Examples
    --------
    >>> res = seasonal_decomposition(strain=0, mouse=0, feature="W",
                                     bin_width=30, period_length = 24)
    """

    if (not isinstance(strain, int)) or (strain < 0):
        raise ValueError(
            'Strain must be a non-negative integer')
    if (not isinstance(mouse, int)) or (mouse < 0):
        raise ValueError(
            'Mouse value must be a non-negative integer')
    if feature not in ALL_FEATURES:
        raise ValueError(
            'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}')
    if (not isinstance(bin_width, int)) or bin_width < 0 or bin_width > 1440:
        raise ValueError(
            'Bin width (minutes) must be a non-negative integer below 1440')
    if (not isinstance(period_length, int)) or period_length < 0:
        raise ValueError(
            'Peoriod length must be a non-negative integer')

    freq = int(period_length * 60 / bin_width)
    if feature == "Distance":
        ts = aggregate_movement(strain=strain, mouse=mouse,
                                bin_width=bin_width)
    else:
        ts = aggregate_interval(strain=strain, mouse=mouse,
                                feature=feature, bin_width=bin_width)
    res = sm.tsa.seasonal_decompose(ts.values, freq=freq, model="additive")
    return(res)


def strain_seasonal(strain, mouse, feature, bin_width, period_length):
    """
    Use seansonal decomposition model on the time series
    of specified strain, mouse, feature and bin_width.
    return the seasonal term and the plot of seasonal term
    by mouse of a set of mouses in a strain

    Parameters
    ----------
    strain: int
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
    period_length: int
        number of hours, usually the significant period
        length indicated by Lomb-scargle model

    Returns
    -------
    seasonal_all: numpy array containing the seasonal term for every
        mouse indicated by the input parameter

    Examples
    --------
    >>> res = strain_seasonal(strain=0, mouse={0, 1, 2, 3}, feature="W",
                              bin_width=30, period_length = 24)
    """

    if (not isinstance(strain, int)) or (strain < 0):
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
    if (not isinstance(period_length, int)) or period_length < 0:
        raise ValueError(
            'Peoriod length must be a non-negative integer')
    # seasonal decomposition
    seasonal_all = np.array([])
    freq = int(period_length * 60 / bin_width)
    for m in mouse:
        res = seasonal_decomposition(
            strain, m, feature, bin_width, period_length)
        seasonal_all = np.append(seasonal_all, res.seasonal[0:freq])
    seasonal_all = seasonal_all.reshape([len(mouse), -1])
    return(seasonal_all)


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
    period_length: int
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
    if (not isinstance(period_length, int)) or period_length < 0:
        raise ValueError(
            'Peoriod length must be a non-negative integer')
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


def mix_strain(data, feature, print_opt=True, nstrain=3, range=(3, 12)):
    """
    Fit the linear mixed model onto our aggregate data. The fixed effects
    are the hour, strain, interactions between hour and strain; The random
    effect is mouse because we want to make sure that the different mouses
    will not give out any differences. We added two dummy variables:
    strain0 and strain1 to be our fixed effects.

    Parameters
    ----------
        data: data frame output from aggregate_data function
        feature: {"AS", "F", "IS", "M_AS", "M_IS", "W", "Distance"}

    Returns
    -------
    Two mixed model regression results which includes all the coefficients,
    t statistics and p values for corresponding coefficients; The first model
    includes interaction terms while the second model does not include the
    interaction terms

    Likelihood ratio test p values, if it is below our significance level,
    we can conclude that the different strains have significantly different
    time patterns

    Examples
    --------
    >>> result = mix_strain(data = aggregate_data("F",30), feature = "F",
    >>>          print_opt = False)
    >>> print(result)
    1.4047992545261542e-12

    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError(
            'Data must be a pandas data frame')
    if feature not in ALL_FEATURES:
        raise ValueError(
            'Input value must in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}')
    data["cycle"] = 0
    for i in range(nstrain):
        result = find_cycle(feature="W", strain=i, plot=False,
                            search_range_find=range)
        cycle = result[0][0]
        data.loc[data["strain"] == i, "cycle"] = cycle
    b = pd.get_dummies(data["strain"])
    data["strain0"] = b.ix[:, 0]
    data["strain1"] = b.ix[:, 1]
    data["strain2"] = b.ix[:, 2]
    data = data.drop('strain', 1)
    names = data.columns.tolist()
    names[names.index(feature)] = 'feature'
    data.columns = names
    md1 = smf.mixedlm(
        "feature ~ hour + strain0 + strain1 + cycle + \
                      strain0*hour + strain1*hour",
        data, groups=data["mouse"])
    mdf1 = md1.fit()
    like1 = mdf1.llf
    if print_opt:
        print(mdf1.summary())
    md2 = smf.mixedlm("feature ~ hour + cycle + strain0 + strain1",
                      data, groups=data["mouse"])
    mdf2 = md2.fit()
    like2 = mdf2.llf
    if print_opt:
        print(mdf2.summary())
    fstat = 2 * abs(like1 - like2)
    p_v = chi2.pdf(fstat, df=2)
    return(p_v)


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
        power_sig = -2 / (N - 1) * np.log(1 -
                                          (1 - np.asarray(i)) ** (1 / 2 / N))
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


def find_cycle(feature, strain, mouse=None, bin_width=15,
               methods='LombScargleFast', disturb_t=False, gen_doc=False,
               plot=True, search_range_fit=None, nyquist_factor=3,
               n_cycle=10, search_range_find=(2, 26), sig=np.array([0.05])):
    """
    Use Lomb-Scargel method on different strain and mouse's data to find the
    best possible periods with highest p-values. The function can be used on
    specific strains and specific mouses, as well as just specific strains
    without specifying mouse number. We use the O(NlogN) fast implementation
    of Lomb-Scargle from the gatspy package, and also provide a way to
    visualize the result.

    Note that either plotting or calculating L-S power doesn't use the same
    method in finding best cycle. The former can use user-specified
    search_range, while the latter uses default two grid search_range.

    Parameters
    ----------
    feature: string in {"AS", "F", "M_AS", "M_IS", "W", "Distance"}
        "AS": Active state probalibity
        "F": Food consumed (g)
        "M_AS": Movement outside homebase
        "M_IS": Movement inside homebase
        "W": Water consumed (g)
        "Distance": Distance traveled
    strain: int
        nonnegative integer indicating the strain number
    mouse: int, default is None
        nonnegative integer indicating the mouse number
    bin_width: int, minute unit, default is 15 minutes
        number of minutes, the time interval for data aggregation
    methods: string in {"LombScargleFast", "LombScargle"}
        indicating the method used in determining periods and best cycle.
        If choose 'LombScargle', 'disturb_t' must be True.
    disturb_t: boolean, default is False
        If True, add uniformly distributed noise to the time sequence which
        are used to fit the Lomb Scargle model. This is to avoid the singular
        matrix error that could happen sometimes.
    plot: boolean, default is True
        If True, call the visualization function to plot the Lomb Scargle
        power versus periods plot. First use the data (either strain specific
        or strain-mouse specific) to fit the LS model, then use the
        search_range_fit as time sequence to predict the corresponding LS
        power, at last draw the plot out. There will also be stars and
        horizontal lines indicating the p-value of significance. Three stars
        will be p-value in [0,0.001], two stars will be p-value in
        [0.001,0.01], one star will be p-value in [0.01,0.05]. The horizontal
        line is the LS power that has p-value of 0.05.
    search_range_fit: list, numpy array or numpy arange, hours unit,
        default is None
        list of numbers as the time sequence to predict the corrsponding
        Lomb Scargle power. If plot is 'True', these will be drawn as the
        x-axis. Note that the number of search_range_fit points can not be
        too small, or the prediction smooth line will not be accurate.
        However the plot will always give the right periods and their LS
        power with 1,2 or 3 stars. This could be a sign to check whether
        search_range_fit is not enough to draw the correct plot.
        We recommend the default None, which is easy to use.
    nyquist_factor: int
        If search_range_fit is None, the algorithm will automatically
        choose the periods sequence.
        5 * nyquist_factor * length(time sequence) / 2 gives the number of
        power and periods used to make LS prediction and plot the graph.
    n_cycle: int, default is 10
        numbers of periods to be returned by function, which have the highest
        Lomb Scargle power and p-value.
    search_range_find: list, tuple or numpy array with length of 2, default is
                       (2,26), hours unit
        Range of periods to be searched for best cycle. Note that the minimum
        should be strictly larger than 0 to avoid 1/0 issues.
    sig: list or numpy array, default is [0.05].
        significance level to be used for plot horizontal line.
    gen_doc: boolean, default is False
        If true, return the parameters needed for visualize the LS power versus
        periods

    Returns
    -------
    cycle: numpy array of length 'n_cycle'
         The best periods with highest LS power and p-values.
    cycle_power: numpy array of length 'n_cycle'
         The corrsponding LS power of 'cycle'.
    cycle_pvalue: numpy array of length 'n_cycle'
         The corrsponding p-value of 'cycle'.
    periods: numpy array of the same length with 'power'
        use as time sequence in LS model to make predictions.Only return when
        gen_doc is True.
    power: numpy array of the same length with 'periods'
        the corresponding predicted power of periods. Only return when
        gen_doc is True.
    sig: list, tuple or numpy array, default is [0.05].
        significance level to be used for plot horizontal line.
        Only return when gen_doc is True.
    N: int
        the length of time sequence in the fit model. Only return when
        gen_doc is True.

    Examples
    -------
    >>> a,b,c = find_cycle(feature='F', strain = 0,mouse = 0, plot=False,)
    >>> print(a,b,c)
    >>> [ 23.98055016   4.81080233  12.00693952   6.01216335   8.0356203
         3.4316698    2.56303353   4.9294791   21.37925713   3.5697756 ]
        [ 0.11543449  0.05138839  0.03853218  0.02982237  0.02275952
        0.0147941  0.01151601  0.00998443  0.00845883  0.0082382 ]
        [  0.00000000e+00   3.29976046e-10   5.39367189e-07   8.10528027e-05
          4.71001953e-03   3.70178834e-01   9.52707020e-01   9.99372657e-01
         9.99999981e-01   9.99999998e-01]

    """
    # get data
    if mouse is None:
        data_all = aggregate_data(feature=feature, bin_width=bin_width)
        n_mouse_in_strain = len(
            set(data_all.loc[data_all['strain'] == strain]['mouse']))
        data = [[] for i in range(n_mouse_in_strain)]
        t = [[] for i in range(n_mouse_in_strain)]
        for i in range(n_mouse_in_strain):
            data[i] = data_all.loc[(data_all['strain'] == strain) & (
                data_all['mouse'] == i)][feature]
            t[i] = np.array(np.arange(0, len(data[i]) *
                                      bin_width / 60, bin_width / 60))

        data = [val for sublist in data for val in sublist]
        N = len(data)
        t = [val for sublist in t for val in sublist]
    else:
        if feature == 'Distance':
            data = aggregate_movement(
                strain=strain, mouse=mouse, bin_width=bin_width)
            N = len(data)
            t = np.arange(0, N * bin_width / 60, bin_width / 60)
        else:
            data = aggregate_interval(
                strain=strain, mouse=mouse,
                feature=feature, bin_width=bin_width)
            N = len(data)
            t = np.arange(0, N * bin_width / 60, bin_width / 60)

    y = data

    # fit model
    if disturb_t is True:
        t = t + np.random.uniform(-bin_width / 600, bin_width / 600, N)

    if methods == 'LombScargleFast':
        model = LombScargleFast(fit_period=False).fit(t=t, y=y)
    elif methods == 'LombScargle':
        model = LombScargle(fit_period=False).fit(t=t, y=y)

    # calculate periods' LS power
    if search_range_fit is None:
        periods, power = model.periodogram_auto(nyquist_factor=nyquist_factor)
    else:
        periods = search_range_fit
        power = model.periodogram(periods=search_range_fit)

    # find best cycle
    model.optimizer.period_range = search_range_find
    cycle, cycle_power = model.find_best_periods(
        return_scores=True, n_periods=n_cycle)
    cycle_pvalue = 1 - (1 - np.exp(cycle_power / (-2) * (N - 1))) ** (2 * N)

    # visualization
    if plot is True:
        lombscargle_visualize(periods=periods, power=power, sig=sig, N=N,
                              cycle_power=cycle_power,
                              cycle_pvalue=cycle_pvalue, cycle=cycle)

    if gen_doc is True:
        return periods, power, sig, N, cycle, cycle_power, cycle_pvalue

    return cycle, cycle_power, cycle_pvalue


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
