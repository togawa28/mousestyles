from __future__ import print_function, absolute_import

import pytest
import pandas as pd
import numpy as np


from mousestyles.path_diversity.path_features_advanced import compute_advanced


def test_compute_advanced_input():
    # Check if function raises the correct type of errors.
    # not pandas DataFrame
    like_path = [1, 2, 3]
    # not having keys 'x', 'y'
    like_path2 = pd.DataFrame({'x': [5, -2, 1],
                               't': [-2, 3, 1],
                               'isHB': [True, True, False]})
    # length is less than 2
    like_path3 = pd.DataFrame({'t': [2], 'x': [5], 'y': [3], 'isHB': [True]})

    with pytest.raises(TypeError) as info:
        compute_advanced(like_path)
    assert info.value.args[0] == "path_obj must be pandas DataFrame"

    with pytest.raises(ValueError) as info:
        compute_advanced(like_path2)
    assert info.value.args[0] == "the keys of path_obj must contain 'x', 'y'"

    with pytest.raises(ValueError) as info:
        compute_advanced(like_path3)
    assert info.value.args[0] == "path_obj must contain at least 3 rows"


def test_compute_advanced():
    '''path = pd.DataFrame({'t': [2, 4.5, 10.5],
                         'x': [0, 1, 1],
                         'y': [0, 0, 1],
                         'isHB': [True, True, False]})
    adv_feats = compute_advanced(path)
    assert adv_feats['area_rec'] == 1
    assert adv_feats['abs_distance'] == np.sqrt(2)
    assert len(adv_feats['radius']) == len(path)
    assert len(adv_feats['center_angles']) == len(path) - 1
    assert adv_feats['center_angles'] == [np.pi / 2] * 2
    assert adv_feats['radius'] == [np.sqrt(2) / 2] * 3

    # in area covered some error was produced
    # so it's not exactly but approximately equal to 1/2
    expected = 1 / 2
    assert np.abs(adv_feats['area_cov'] - expected) < 0.00001
    '''
    path = pd.DataFrame({'x': [0, 3, 3, 0],
                         'y': [0, 0, 4, 4]})
    adv_feats = compute_advanced(path)
    assert adv_feats['area_rec'] == 3 * 4
    assert adv_feats['abs_distance'] == 4
    assert len(adv_feats['center_angles']) == len(path) - 1
    assert len(adv_feats['radius']) == len(path)
    assert adv_feats['radius'] == [np.sqrt(3 ** 2 + 4 ** 2) / 2] * 4

    # in area covered some error was produced
    # so it's not exactly but approximately equal to
    # the theoretical value
    expected = 3 * 4 - 3 / 2 * 4 / 2
    assert np.abs(adv_feats['area_cov'] - expected) < 0.0000001

    # in center_angles some errors were produced
    # so it's not exactly but approximately equal to
    # the theoretical values
    # By law of cosines
    expected1 = (2 * 2.5 ** 2 - 3 ** 2) / (2 * 2.5 ** 2)
    expected2 = (2 * 2.5 ** 2 - 4 ** 2) / (2 * 2.5 ** 2)

    assert np.abs(np.cos(adv_feats['center_angles'][0]) -
                  expected1) < 0.0000001
    assert np.abs(np.cos(adv_feats['center_angles'][2]) -
                  expected1) < 0.0000001
    assert np.abs(np.cos(adv_feats['center_angles'][1]) -
                  expected2) < 0.0000001
