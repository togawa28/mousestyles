"""Data utilities."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np


def day_to_mouse_average(features, labels, num_strains=16,
                         stdev=False, stderr=False):
    """
    first three columns of labels are strain num, mouse number, day number
    features is an M x N matrix of mouse day x features

    Returns:
        new data matrix with a mean and stdev/stderr for each mouse over
        mouse days
    """

    data = np.hstack([labels, features])
    tot_data_avgs = np.zeros((1, data.shape[1] - 1))
    tot_data_std = np.zeros((1, data.shape[1] - 1))
    tot_data_stderr = np.zeros((1, data.shape[1] - 1))

    for strain in range(0, num_strains):
        mice = {}
        cnt = 0
        tmp_data = data[data[:, 0] == strain, :]

        for i in range(tmp_data.shape[0]):
            if tmp_data[i, 1] in mice:
                mice[tmp_data[i, 1]] += 1
            else:
                cnt += 1
                mice[tmp_data[i, 1]] = 1
        data_avgs = np.zeros((len(mice), data.shape[1] - 1))
        data_std = np.zeros((len(mice), data.shape[1] - 1))
        data_stderr = np.zeros((len(mice), data.shape[1] - 1))

        for c, num in enumerate(mice.keys()):
            mouse_arr = tmp_data[tmp_data[:, 1] == num, 0:]
            mouse_avg = mouse_arr[:, 3:].mean(axis=0)
            mouse_std = mouse_arr[:, 3:].std(axis=0)
            # standard error for plot
            mouse_stderr = mouse_arr[:, 3:].std(
                axis=0) / np.sqrt(mouse_arr.shape[0] - 1)

            data_avgs[c, 0:2] = mouse_arr[0, 0:2]
            data_avgs[c, 2:] = mouse_avg

            data_std[c, 0:2] = mouse_arr[0, 0:2]
            data_std[c, 2:] = mouse_std

            data_stderr[c, 0:2] = mouse_arr[0, 0:2]
            data_stderr[c, 2:] = mouse_stderr

        tot_data_avgs = np.vstack(
            [tot_data_avgs, data_avgs])          # not ordered
        tot_data_std = np.vstack([tot_data_std, data_std])
        tot_data_stderr = np.vstack([tot_data_stderr, data_stderr])

    if stdev:
        return tot_data_avgs[1:], tot_data_std[1:]
    elif stderr:
        return tot_data_avgs[1:], tot_data_stderr[1:]

    return tot_data_avgs[1:]


def mouse_to_strain_average(
        features, labels, num_strains=16, stdev=False, stderr=False):
    """
    first two columns of M x N data matrix are strain num (1 - num_strains),
    mouse number
    other columns are features

    Returns: new data matrix with a mean and stdev/stderr for each strain
    over mice
    """
    data = np.hstack([labels, features])
    tot_data_avgs = np.zeros((num_strains, data.shape[1] - 2))
    tot_data_std = np.zeros((num_strains, data.shape[1] - 2))
    tot_data_stderr = np.zeros((num_strains, data.shape[1] - 2))

    for strain in range(0, num_strains):
        tmp_data = data[data[:, 0] == strain, 2:]
        tot_data_avgs[strain] = tmp_data.mean(axis=0)
        tot_data_std[strain] = tmp_data.std(axis=0)
        tot_data_stderr[strain] = tmp_data.std(
            axis=0) / np.sqrt(tmp_data.shape[0] - 1)  # standard error for plot

    if stdev:
        return tot_data_avgs, tot_data_std
    elif stderr:
        return tot_data_avgs, tot_data_stderr

    return tot_data_avgs


def split_data_in_half_randomly(features, labels):
    """ given an array of the form:
            features = M x A x B x C x ...
        where M is the number of mouse days

        and an array labels for this data of the form:
            labels = M x 2
        where labels[:, 0] are strain numbers and the labels[:, 1] are
        mice numbers

        returns
            bootstrap_data_1 = a random half of the mouse days
            bootstrap_labels_1
            bootstrap_data_2 = the other half
            bootstrap_labels_2
    """
    all_perm_data = np.zeros(features.shape)
    all_perm_labels = np.zeros(labels.shape)
    strains = list(set(labels[:, 0]))
    c = 0

    for strain in strains:
        sub_data = features[labels[:, 0] == strain]
        sub_labels = labels[labels[:, 0] == strain]
        mice_nums = {}

        for i in range(len(sub_data)):
            mice_nums[sub_labels[i, 1]] = 1

        for mouse in mice_nums.keys():
            # print strain, mouse
            tmp = sub_data[sub_labels[:, 1] == mouse]
            tmp_l = sub_labels[sub_labels[:, 1] == mouse]
            # print tmp, tmp_l
            perm = np.random.permutation(len(tmp))
            all_perm_data[c:c + len(tmp)] = tmp[perm]
            all_perm_labels[c:c + len(tmp_l)] = tmp_l[perm]
            c += len(tmp)

    return all_perm_data[::2], all_perm_labels[
        ::2], all_perm_data[1::2], all_perm_labels[1::2]


def pull_locom_tseries_subset(M, start_time=0, stop_time=300):
    """
    given an (m x n) numpy array M where the 0th row is array of times
    [ASSUMED SORTED]

    returns a new array (copy) that is a subset of M corresp to
    start_time, stop_time

    returns [] if times are not in array

    (the difficulty is that if mouse does not move nothing gets registered
     so we should artificially create start_time, stop_time movement events
     at boundries)
    """
    T = M[0]
    idx_start = T.searchsorted(start_time)
    idx_stop = T.searchsorted(stop_time)
    new_M = M[:, idx_start:idx_stop].copy()
    if idx_stop != T.shape[0]:
        if (idx_start != 0) and (T[idx_start] != start_time):
            v = np.zeros(M.shape[0])
            v[1:] = M[1:, idx_start - 1].copy()
            v[0] = start_time
            v = v.reshape((M.shape[0], 1))
            new_M = np.hstack([v, new_M])
        if (T[idx_stop] != stop_time) and (idx_stop != 0):
            v = np.zeros(M.shape[0])
            v[1:] = M[1:, idx_stop - 1].copy()  # find last time registered
            v[0] = stop_time
            v = v.reshape((M.shape[0], 1))
            new_M = np.hstack([new_M, v])
        elif (T[idx_stop] == stop_time):
            v = M[:, idx_stop].copy().reshape((M.shape[0], 1))
            new_M = np.hstack([new_M, v])
    else:
        pass
    return new_M


def total_time_rectangle_bins(
        M, xlims=(0, 1), ylims=(0, 1), xbins=5, ybins=10):
    """
    given an (3 x n) numpy array M where the 0th row is array of times
    [ASSUMED SORTED]

    returns a new (xbins x ybins) array (copy) that contains PDF of location
    over time
    """
    xmin, xmax = xlims
    ymin, ymax = ylims
    meshx = xmin + (xmax - xmin) * 1. * np.array(range(1, xbins + 1)) / xbins
    meshy = ymin + (ymax - ymin) * 1. * np.array(range(1, ybins + 1)) / ybins

    Cnts = np.zeros((ybins, xbins))
    if M.shape[0] <= 1:
        return Cnts

    bin_idx = meshx.searchsorted(M[1, :], side='right')
    bin_idy = meshy.searchsorted(M[2, :], side='right')
    for k in range(M.shape[1] - 1):
        if bin_idx[k] == xbins:
            bin_idx[k] -= 1
        if bin_idy[k] == ybins:
            bin_idy[k] -= 1
        Cnts[ybins - bin_idy[k] - 1, bin_idx[k]] += M[0, k + 1] - M[0, k]
    return Cnts


def idx_restrict_to_rectangles(TXY, rects=[(0, 0)], xlims=(
        0, 1), ylims=(0, 1), xbins=2, ybins=4, eps=.01):
    """
    given (3 x T) TXY with 0th row array of times [ASSUMED SORTED] and rows
    1,2 are x,y coords

    returns new interval array which is E minus those things occuring
    outside of given rectangle
    """
    num_movements = TXY.shape[1]
    idx_F_bout = np.zeros(num_movements, dtype=bool)  # when at rectangles
    tmp_sum = 0

    for rect in rects:
        tl, tr, bl, br = map_xbins_ybins_to_cage(
            rectangle=rect, xbins=xbins, ybins=ybins)

        for t in range(num_movements):
            if ((TXY[1, t] > tl[0]) and (TXY[1, t] < tr[0]) and (
                    TXY[2, t] < tl[1]) and (TXY[2, t] > bl[1])):
                idx_F_bout[t] = True
            # print ("indexed %d move events " % (sum(idx_F_bout) - tmp_sum))
        tmp_sum += sum(idx_F_bout)

    # print ("Total move events: %d" % num_movements)
    # print ("indexing %d/%d (%1.1f percent) movements at rectangles" %
    # (sum(idx_F_bout), num_movements, 100. * sum(idx_F_bout) / num_movements))

    return idx_F_bout


def map_xbins_ybins_to_cage(rectangle=(0, 0), xbins=2, ybins=4,
                            YLower=1.0, YUpper=43.0, XUpper=3.75,
                            XLower=-16.25):
    """
    converts a rectangle in xbins x ybins to corresponding rectangle in
    Cage coordinates

    format is [[p1, p2], [p3, p4]] where
    pi = (cage_height_location, cage_length_location)

    # ??? -chris
    ### THIS GIVES WRONG CAGE LOCATIONS for top bottom left right
    # # # xbins ybins do NOT reflect cage geometry perfectly
    """
    L = XUpper - XLower
    H = YUpper - YLower

    delta_x = L / xbins
    delta_y = H / ybins

    h, l = rectangle
    coord_y = YUpper - delta_y * h
    coord_x = XLower + delta_x * l

    return ((coord_x, coord_y), (coord_x + delta_x, coord_y),
            (coord_x, coord_y - delta_y),
            (coord_x + delta_x, coord_y - delta_y))
