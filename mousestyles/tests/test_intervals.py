from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import mousestyles.data as data
from mousestyles.intervals import Intervals


def test_intervals():
    # This is a place holder.  Not sure this is correct.
    all_features = data.load_all_features()
    assert Intervals(all_features).measure() == 11.0
