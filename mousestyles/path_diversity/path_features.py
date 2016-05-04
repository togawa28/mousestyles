from __future__ import print_function, absolute_import, division
import numpy as np
import pandas as pd
import math


def compute_distances(path_obj):
    r"""
    Returns a list of the traveled distances along the path.
    Each element of the list is the Euclidean distance between the adjacent points in the path.
    The length of the list is equal to the length of the path minus 1.

    Parameters
    ----------
    path_obj : pandas.DataFrame
        CT, CX, CY coordinates and homebase status. 
        Must have the length greater than 1.

    Returns
    -------
    distances : list
        contains the traveled distances along the path.

    Examples
    --------
    >>> path = pd.DataFrame({'t':[2, 4.5], 'x':[0, 3],'y':[0, 4],'isHB':[True,False]})
    >>> compute_distances(path)
    [5.0]
    """

    if type(path_obj) is not pd.core.frame.DataFrame:
        raise TypeError("path_obj must be pandas DataFrame")
    
    if set(path_obj.keys()) != {'isHB', 't', 'x', 'y'}:
        raise ValueError("the keys of path_obj must be 't', 'x', 'y', and 'isHB'")
    
    if len(path_obj) <= 1:
        raise ValueError("path_obj must contain at least 2 rows")
    
    indices = path_obj.index[:len(path_obj)-1]
    distances = [np.linalg.norm(path_obj.loc[i,'x':'y'] - path_obj.loc[i+1,'x':'y']) for i in indices]
    return(distances)


def take_time_diffs(path_obj):
    r"""
    Returns a list of the time differences along the path.
    Each element of the list is the difference of timestamp between the adjacent points in the path.
    The length of the list is equal to the length of the path minus 1.

    Parameters
    ----------
    path_obj : pandas.DataFrame
        CT, CX, CY coordinates and homebase status.
        Must have the length greater than 1.

    Returns
    -------
    time differences : list
        contains the time differences along the path.

    Examples
    --------
    >>> path = pd.DataFrame({'t':[2, 4.5], 'x':[0, 3],'y':[0, 4],'isHB':[True,False]})
    >>> take_time_diffs(path)
    [2.5]
    """

    if type(path_obj) is not pd.core.frame.DataFrame:
        raise TypeError("path_obj must be pandas DataFrame")
    
    if set(path_obj.keys()) != {'isHB', 't', 'x', 'y'}:
        raise ValueError("the keys of path_obj must be 't', 'x', 'y', and 'isHB'")
    
    if len(path_obj) <= 1:
        raise ValueError("path_obj must contain at least 2 rows")

    indices = path_obj.index[:len(path_obj)-1]
    time_diffs = [path_obj.loc[i+1, 't'] - path_obj.loc[i, 't'] for i in indices]
    return(time_diffs)


def compute_speeds(distances, time_diffs):
    r"""
    Returns a list of the speeds along the path.
    Each element of the list is the ratio of the traveled distance to the time difference.
    The length of the list is equal to the length of distances or time_diffs.

    Parameters
    ----------
    distances : list
        the traveled distances along the path. Expecting the output of compute_distances.

    time_diffs : list
        the time difference within the path. Expecting the output of take_time_diffs. 
        Must have the same length as distances. Should not contain 0; otherwise output would 
        contain inf.

    Returns
    -------
    speeds : list
        contains the speeds along the path.

    Examples
    --------
    >>> compute_speeds([0,2,9], [1,2,5])
    [0.0, 1.0, 1.8]
    """

    if type(distances) is not list or type(time_diffs) is not list:
        raise TypeError("distances and time_diffs must be lists")

    if len(distances) is not len(time_diffs):
        raise ValueError("lengths of distances and time_diffs must be same")
    
    if np.count_nonzero(time_diffs) is not len(time_diffs):
        raise ValueError("time_diffs should not contain 0")    
    
    speeds = [d/t for d,t in zip(distances, time_diffs)]
    return(speeds)


def compute_accelerations(speeds, timestamps):
    r"""
    Returns a list of the accelerations along the path.
    Each element of the list is the ratio of the speed to the time difference.
    The length of the list is equal to the length of speeds minus 1.

    Parameters
    ----------
    speeds : list
        the traveled distances along the path. Expecting the output of compute_distances.

    timestamps : list
        the time difference within the path.
        Its length must be equal to the length of speeds plus 1.
        Should not contain same time in adjacent rows;
        otherwise output would contain inf.

    Returns
    -------
    accel : list
        contains the speeds along the path.

    Examples
    --------
    >>> compute_accelerations([1, 2, 0], [3,4,5,6])
    [0.5, -1.0]
    """

    if type(speeds) is not list or type(timestamps) is not list:
        raise TypeError("speeds and timestamps must be lists")

    if len(speeds) is not len(timestamps)-1:
        raise ValueError("lengths of speeds must be the length of timestamps minus 1")
    
    speeds_diff = [ x - y for x,y in zip(speeds[:len(speeds)], speeds[1:])] 
    time_diffs = [ x - y for x,y in zip(timestamps[:len(timestamps)-1], timestamps[2:])]

    if np.count_nonzero(time_diffs) is not len(time_diffs):
        raise ValueError("timestamps should not contain same times in i th and i+2 th rows.")

    accel = [v/t for v,t in zip(speeds_diff, time_diffs)]
    return(accel)


def angle_between(v1, v2):
    r"""
    Returns the angle in radians between vectors `v1` and `v2`.
    Both vectors must have same length.
    
    Parameters
    ----------
    v1, v2 : lists
        Vectors whose angle would be calculated.
        Should have same lengths.
        Should not be zero vector.

    Returns
    -------
    angle : numpy float object
        nan if either of `v1` or `v2` is zero vector, 


    Examples
    --------
    >>> angle_between([1, 0],[1, 0])
    0.0
    >>> angle_between([1, 0],[0, 1])
    1.5707963267948966
    >>> angle_between([1, 0],[-1, 0])
    3.1415926535897931
    """

    if type(v1) is not list or type(v2) is not list:
        raise TypeError("v1 and v2 must be lists")

    if len(v1) is not len(v2):
        raise ValueError("both vectors must have same lengths")   

    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    if np.count_nonzero([norm_v1, norm_v2]) is not 2:
        raise ValueError('both vectors must have norms greater than 0')
    
    v1_u = v1 / norm_v1
    v2_u = v2 / norm_v2
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    

def compute_angles(path_obj, radian=None):
    r"""
    Returns a list of the angles in the path.
    Each element of the list is the angle between the adjacent vectors in the path.
    The length of the list is equal to the length of speeds minus 2.

    Parameters
    ----------
    path_obj : pandas.DataFrame
        CT, CX, CY coordinates and homebase status.
        Must have length greater than 3.

    radian : boolean
        True for the output in radians. False for in turns (i.e. 360 for a full turn).
        Default is False.

    Returns
    -------
    angles : list
        contains the angles in the path. The first and last elements are None.

    Examples
    --------
    >>> path = pd.DataFrame({'t':[2,4.5,10.5], 'x':[0,1,1],\ 
    'y':[0,0,1], 'isHB':[True,True,False]})
    >>> compute_angles(path)
    [None, 90.0, None]
    """
    if radian == None:
        radian = False
    
    if type(path_obj) is not pd.core.frame.DataFrame:
        raise TypeError("path_obj must be pandas DataFrame")
    
    if set(path_obj.keys()) != {'isHB', 't', 'x', 'y'}:
        raise ValueError("the keys of path_obj must be 't', 'x', 'y', and 'isHB'")
    
    if len(path_obj) <= 2:
        raise ValueError("path_obj must contain at least 3 rows")

    if type(radian) != bool:
        raise TypeError("radian must be bool")

    indices = path_obj.index[:len(path_obj)-1]
    vectors = [path_obj.loc[i + 1,'x':'y'] - path_obj.loc[i,'x':'y'] for i in indices]
    angles = [angle_between(list(v1),list(v2)) for v1,v2 in zip(vectors[1:], vectors[:len(vectors)])]

    if not radian:
        angles = [theta * 180 / math.pi for theta in angles]

    # the first and last elements should be None
    angles.insert(len(angles), None)
    angles.insert(0, None)
    return(angles)
