from __future__ import print_function, absolute_import, division

import pytest
import pandas as pd

from mousestyles import path_diversity


def test_clean_movements_input():
    # Check if function raises the correct type of errors.
    with pytest.raises(TypeError) as excinfo:
        path_diversity.clean_movements(1)
    assert excinfo.value.args[0] == 'movements must be a list'

    with pytest.raises(ValueError) as excinfo:
        path_diversity.clean_movements([])
    assert excinfo.value.args[
        0] == "movements must contain at least 1 movement object"

    # good objects
    m_obj1 = pd.DataFrame({'t': [2, 4.5, 10.5],
                           'x': [0, 1, 1],
                           'y': [0, 0, 1],
                           'isHB': [True, True, False]})
    # not a pandas DataFrame
    m_obj11 = {'t': [2, 4.5, 10.5],
               'x': [0, 1, 1],
               'y': [0, 0, 1],
               'isHB': [True, True, False]}
    # no cloumn for `x`
    m_obj12 = pd.DataFrame({'t': [2, 4.5, 10.5],
                            'y': [0, 0, 1],
                            'isHB': [True, True, False]})

    # good object
    m_obj2 = pd.DataFrame({'t': [2, 4.5, 10.5],
                           'x': [0, 1, 1],
                           'y': [0, 0, 1],
                           'isHB': [True, True, False]})
    # length is only 1
    m_obj21 = pd.DataFrame({'t': [2],
                            'x': [0],
                            'y': [0]})
    # having same timestamps
    m_obj22 = pd.DataFrame({'t': [2, 2, 10.5],
                            'x': [0, 1, 1],
                            'y': [0, 0, 1],
                            'isHB': [True, True, False]})

    test_obj = [m_obj1, m_obj2]
    test_obj11 = [m_obj11, m_obj2]
    test_obj12 = [m_obj12, m_obj2]
    test_obj21 = [m_obj1, m_obj21]
    test_obj22 = [m_obj1, m_obj22]

    with pytest.raises(TypeError) as excinfo:
        path_diversity.clean_movements(test_obj, 1)
    assert excinfo.value.args[0] == "keep_index must be bool"

    with pytest.raises(TypeError) as excinfo:
        path_diversity.clean_movements(test_obj11)
    assert excinfo.value.args[
        0] == "each movement object must be pandas DataFrame"

    with pytest.raises(ValueError) as excinfo:
        path_diversity.clean_movements(test_obj12)
    assert excinfo.value.args[
        0] == "the keys of each movement object must contain 'x', 'y', 't"

    with pytest.raises(ValueError) as excinfo:
        path_diversity.clean_movements(test_obj21)
    assert excinfo.value.args[
        0] == "each movement object must contain at least 2 rows"

    with pytest.raises(ValueError) as excinfo:
        path_diversity.clean_movements(test_obj22)
    assert excinfo.value.args[
        0] == "some movement contains same timestamps in adjacent rows"


def test_clean_movements():
    # 4th and 5th rows must be dropeed
    m_obj1 = pd.DataFrame({'t': [1, 1.4, 2, 3, 4, 4.3, 5, 5.1],
                           'x': [0, 1, 1, 1, 1, 2, 2, 2],
                           'y': [0, 0, 1, 1, 1, -1, 0, -1],
                           'isHB': [True, True, False, True, True, True,
                                    True, True]})
    # 2 length object. 2nd row must be dropeed
    m_obj2 = pd.DataFrame({'t': [2, 4],
                           'x': [10, 10],
                           'y': [10, 10]})
    test_obj = [m_obj1, m_obj2]

    output = path_diversity.clean_movements(test_obj)
    output_same_ind = path_diversity.clean_movements(test_obj, True)

    # desired outputs
    comp1 = pd.DataFrame({'t': [1, 1.4, 2, 4.3, 5, 5.1],
                          'x': [0, 1, 1, 2, 2, 2],
                          'y': [0, 0, 1, -1, 0, -1],
                          'isHB': [True, True, False, True, True, True]})
    comp2 = pd.DataFrame({'t': [2],
                          'x': [10],
                          'y': [10]})

    assert (output[0] == comp1).all().all()
    assert (output[1] == comp2).all().all()

    # see index-match
    comp1.index = [0, 1, 2, 5, 6, 7]
    assert (output_same_ind[0] == comp1).all().all()
