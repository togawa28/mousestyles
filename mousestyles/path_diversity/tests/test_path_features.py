from __future__ import (absolute_imoport, division, print_function, unicode_literals)


import pytest


from mousestyles import data
from mousestyles.path_features import compute_distances, take_time_diffs,\
 compute_speeds, compute_accelerations, angle_between, compute_angles

def test_compute_distances_input():
    # Check if function raises the correct type of errors.
    
    # not pandas DataFrame
    like_path = [1,2,3]
    # not having keys 't', 'x', 'y', and 'isHB'
    like_path2 = pd.DataFrame({'x':[5,-2],'y':[-2,3],'isHB':[True,True]})
    # length is less than 2
    like_path3 = pd.DataFrame({'t':[2], 'x':[5],'y':[3],'isHB':[True]})
    
    with pytest.raises(TypeError) as excinfo:
        compute_distances(like_path)
    assert excinfo.value.args[0] == "path_obj must be pandas DataFrame"

    with pytest.raises(ValueError) as excinfo:
        compute_distances(like_path2)
    assert excinfo.value.args[0] == "the keys of path_obj must be 't', 'x', 'y', and 'isHB'"

    with pytest.raises(ValueError) as excinfo:
        compute_distances(like_path3)
    assert excinfo.value.args[0] == "path_obj must contain at least 2 rows"

def test_compute_distances():
    path = pd.DataFrame({'t':[2,3,4], 'x':[0,1,4],'y':[0,1,5],'isHB':[True,True,False]})
    assert compute_distances(path) == [np.sqrt(2),5.0] 


# similar test function for input as compute_distances
def test_take_time_diffs_input():
    # Check if function raises the correct type of errors.
    
    # not pandas DataFrame
    like_path = [1,2,3]
    # not having keys 't', 'x', 'y', and 'isHB'
    like_path2 = pd.DataFrame({'x':[5,-2],'y':[-2,3],'isHB':[True,True]})
    # length is less than 2
    like_path3 = pd.DataFrame({'t':[2], 'x':[5],'y':[3],'isHB':[True]})
    
    with pytest.raises(TypeError) as excinfo:
        take_time_diffs(like_path)
    assert excinfo.value.args[0] == "path_obj must be pandas DataFrame"

    with pytest.raises(ValueError) as excinfo:
        take_time_diffs(like_path2)
    assert excinfo.value.args[0] == "the keys of path_obj must be 't', 'x', 'y', and 'isHB'"

    with pytest.raises(ValueError) as excinfo:
        take_time_diffs(like_path3)
    assert excinfo.value.args[0] == "path_obj must contain at least 2 rows"


def test_take_time_diffs():
    path = pd.DataFrame({'t':[2,4.5,10.5], 'x':[0,1,4],'y':[0,1,5],'isHB':[True,True,False]})
    assert take_time_diffs(path) == [2.5, 6]
    

def test_compute_speeds_input():
    # Check if function raises the correct type of errors.
    
    with pytest.raises(TypeError) as excinfo:
        compute_speeds(0, 1)
    assert excinfo.value.args[0] == 'distances and time_diffs must be lists'
    
    with pytest.raises(TypeError) as excinfo:
        compute_speeds([0], 1)
    assert excinfo.value.args[0] == 'distances and time_diffs must be lists'

    with pytest.raises(ValueError) as excinfo:
        compute_speeds([0], [1,2])
    assert excinfo.value.args[0] == 'lengths of distances and time_diffs must be same'

    with pytest.raises(ValueError) as excinfo:
        compute_speeds([0, 1], [1, 0])
    assert excinfo.value.args[0] == 'time_diffs should not contain 0'


def test_compute_speeds():
    assert compute_speeds([0,3],[1,2]) == [0.0, 1.5]


def test_compute_accelerations_input():
    # Check if function raises the correct type of errors.
 
    with pytest.raises(TypeError) as excinfo:
        compute_accelerations(0, 1)
    assert excinfo.value.args[0] == 'speeds and timestamps must be lists'
    
    with pytest.raises(TypeError) as excinfo:
        compute_accelerations([0], 1)
    assert excinfo.value.args[0] == 'speeds and timestamps must be lists'

    with pytest.raises(ValueError) as excinfo:
        compute_accelerations([0,1], [1,2])
    assert excinfo.value.args[0] == \
    'lengths of speeds must be the length of timestamps minus 1'

    with pytest.raises(ValueError) as excinfo:
        compute_accelerations([1,3], [4,4,4])
    assert excinfo.value.args[0] == \
     'timestamps should not contain same times in i th and i+2 th rows.'


def test_compute_accelerations():
    assert compute_accelerations([1, 2, 0], [3,4,5,6]) == [0.5, -1.0]


def test_angle_between_input():
    # Check if function raises the correct type of errors.

    with pytest.raises(TypeError) as excinfo:
        angle_between([0], 1)
    assert excinfo.value.args[0] == 'v1 and v2 must be lists'
    
    with pytest.raises(ValueError) as excinfo:
        angle_between([0], [1,2])
    assert excinfo.value.args[0] == 'both vectors must have same lengths'

    with pytest.raises(ValueError) as excinfo:
        angle_between([0,0], [1,0])
    assert excinfo.value.args[0] == 'both vectors must have norms greater than 0'


def test_angle_between():
    assert angle_between([0,1], [0,1]) == 0.0
    assert angle_between([1,0], [0,1]) == np.pi/2
    assert angle_between([0,1], [0,-1]) == np.pi


# similar test function for input as compute_distances and take_time_diffs
def test_compute_angles_input():
    # Check if function raises the correct type of errors.
    
    path = pd.DataFrame({'t':[2, 1, -1], 'x':[5, 3, 8], \
                         'y':[-3, 0, 0], 'isHB':[True, False, False]})
    # not pandas DataFrame
    like_path = [1,2,3]
    # not having keys 't', 'x', 'y', and 'isHB'
    like_path2 = pd.DataFrame({'x':[5,-2],'y':[-2,3],'isHB':[True,True]})
    # length is less than 2
    like_path3 = pd.DataFrame({'t':[2], 'x':[5],'y':[3],'isHB':[True]})
    
    with pytest.raises(TypeError) as excinfo:
        compute_angles(path, 1)
    assert excinfo.value.args[0] == 'radian must be bool'
    
    with pytest.raises(TypeError) as excinfo:
        compute_angles(like_path, True)
    assert excinfo.value.args[0] == "path_obj must be pandas DataFrame"

    with pytest.raises(ValueError) as excinfo:
        compute_angles(like_path2, True)
    assert excinfo.value.args[0] == "the keys of path_obj must be 't', 'x', 'y', and 'isHB'"

    with pytest.raises(ValueError) as excinfo:
        compute_angles(like_path3, True)
    assert excinfo.value.args[0] == "path_obj must contain at least 3 rows"


def test_compute_angles():
    path = pd.DataFrame({'t':[2,4.5,10.5], 'x':[0,1,1],'y':[0,0,1],'isHB':[True,True,False]})
    assert compute_angles(path) == [None, 90.0, None]
    assert compute_angles(path, True) == [None, np.pi/2, None]