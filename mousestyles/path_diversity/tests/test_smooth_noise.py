from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pandas as pd

from mousestyles import path_diversity


def test_smooth_noise():
    movement = {'t': pd.Series([0., 0.02, 0.04, 0.06], index=[0, 1, 2, 3]),
                'x': pd.Series([0., 0., 0.1, 0.2], index=[0, 1, 2, 3]),
                'y': pd.Series([0., 1., 0., 1.], index=[0, 1, 2, 3]),
                'isHB': pd.Series(['No', 'No', 'No', 'No'],
                                  index=[0, 1, 2, 3])}
    movement = pd.DataFrame(movement)
    paths = path_diversity.path_index(movement, 1, 1)

    # Check if function produces the correct outputs.
    smoothed = path_diversity.smooth_noise(movement, paths, 120, 1)
    assert len(smoothed) == 3

    movement = {'t': pd.Series([0., 0.02, 0.04, 0.06], index=[0, 1, 2, 3]),
                'x': pd.Series([0., 0., 0.1, 0.2], index=[0, 1, 2, 3]),
                'y': pd.Series([0., 1., 0., 1.], index=[0, 1, 2, 3]),
                'isHB': pd.Series(['No', 'No', 'No', 'No'],
                                  index=[0, 1, 2, 3])}
    movement = pd.DataFrame(movement)
    paths = path_diversity.path_index(movement, 1, 1)
    # Check if function produces the correct outputs.
    smoothed = path_diversity.smooth_noise(movement, paths, 120, 1)
    assert smoothed['y'][1] == 0.5

    movement = {'t': pd.Series([0., 0.02, 0.04, 0.06], index=[0, 1, 2, 3]),
                'x': pd.Series([0., 0., 0.1, 0.2], index=[0, 1, 2, 3]),
                'y': pd.Series([0., 1., 0., 1.], index=[0, 1, 2, 3]),
                'isHB': pd.Series(['No', 'No', 'No', 'No'],
                                  index=[0, 1, 2, 3])}
    movement = pd.DataFrame(movement)
    paths = path_diversity.path_index(movement, 1, 1)
    # Check if function produces the correct outputs.
    smoothed = path_diversity.smooth_noise(movement, paths, 120, 1)
    assert smoothed['x'][1] == 0.05

    movement = {'t': pd.Series([0., 0.02, 0.04, 0.06], index=[0, 1, 2, 3]),
                'x': pd.Series([0., 0., 0.1, 0.2], index=[0, 1, 2, 3]),
                'y': pd.Series([0., 1., 0., 1.], index=[0, 1, 2, 3]),
                'isHB': pd.Series(['No', 'No', 'No', 'No'],
                                  index=[0, 1, 2, 3])}
    movement = pd.DataFrame(movement)
    paths = path_diversity.path_index(movement, 1, 1)
    # Check if function produces the correct outputs.
    smoothed = path_diversity.smooth_noise(movement, paths, 120, 1)
    assert smoothed['t'][1] == 0.03
