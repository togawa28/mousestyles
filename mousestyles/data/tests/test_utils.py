from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np

from mousestyles.data.utils import (pull_locom_tseries_subset,
                                    total_time_rectangle_bins)


def test_pull_locom():
    M = np.array([[1, 2, 3, 4, 5, 6], [8, 7, 6, 5, 5, 4], [-1, 3, 4, 1, 1, 4]])

    M_ = np.array([[1, 2, 3, 4], [8, 7, 6, 5], [-1, 3, 4, 1]])
    Mnew = pull_locom_tseries_subset(M, start_time=1, stop_time=4)
    np.testing.assert_allclose(Mnew, M_)

    M_ = np.array([[1, 2, 3, 3.4], [8, 7, 6, 6], [-1, 3, 4, 4]])
    Mnew = pull_locom_tseries_subset(M, start_time=1, stop_time=3.4)
    np.testing.assert_allclose(Mnew, M_)

    M_ = np.array([[1.2, 2, 3, 3.4], [8, 7, 6, 6], [-1, 3, 4, 4]])
    Mnew = pull_locom_tseries_subset(M, start_time=1.2, stop_time=3.4)
    np.testing.assert_allclose(Mnew, M_)

    M_ = np.array([[1, 2, 3, 4, 5], [8, 7, 6, 5, 5], [-1, 3, 4, 1, 1]])
    Mnew = pull_locom_tseries_subset(M, start_time=0, stop_time=5)
    np.testing.assert_allclose(Mnew, M_)

    M_ = np.array([[1.2, 1.5], [8, 8], [-1, -1]])
    Mnew = pull_locom_tseries_subset(M, start_time=1.2, stop_time=1.5)
    np.testing.assert_allclose(Mnew, M_)

    Mnew = pull_locom_tseries_subset(M, start_time=1, stop_time=7)
    np.testing.assert_allclose(Mnew, M)


def test_total_time():
    M = np.array([[1, 2, 3], [.5, .1, .1], [.3, .4, .6]])
    TT = total_time_rectangle_bins(M, xbins=2, ybins=2)
    np.testing.assert_allclose(TT, [[0., 0.], [1., 1.]])

    M = np.array([[1, 2, 3], [.5, .6, .1], [.3, .4, .6]])
    TT = total_time_rectangle_bins(M, xbins=3, ybins=5)
    np.testing.assert_allclose(TT, [[0., 0., 0.], [0., 0., 0.],
                                    [0., 1., 0.], [0., 1., 0.], [0., 0., 0.]])

    M = np.array([[1, 2, 3, 4, 5, 6],
                  [.51, .61, .11, .81, .21, .3],
                  [.3, .41, .6, .1, .1, .1]])
    TT = total_time_rectangle_bins(M, xbins=3, ybins=5)
    np.testing.assert_allclose(TT, [[0., 0., 0.], [1., 0., 0.], [
                               0., 1., 0.], [0., 1., 0.], [1., 0., 1.]])

    M = np.array([[1, 2], [.5, .5], [.3, .3]])
    TT = total_time_rectangle_bins(M, xbins=3, ybins=5)
    np.testing.assert_allclose(TT, [[0., 0., 0.], [0., 0., 0.],
                                    [0., 0., 0.], [0., 1., 0.], [0., 0., 0.]])
