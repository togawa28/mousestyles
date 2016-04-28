import numpy as np
import pandas as pd
import math

from mousestyles import data
from mousestyles.path_index import path_index

def compute_distances(path_obj):
	r"""
	Returns a list of the traveled distances along the path.
	Each element of the list is the Euclidean distance between the adjacent points in the path.
	The length of the list is equal to the length of the path minus 1.

	Parameters
    ----------
    path_obj : pandas.DataFrame
        CT, CX, CY coordinates and homebase status.

	Returns
    -------
    distances : list
    	contains the traveled distances along the path.

    Examples
    --------
    >>> movement = data.load_movement(1,2,1)
    >>> sep = path_index(movement, 1, 1)
    >>> path = movement[sep[2][0]:sep[2][1]+1]
    >>> dist = compute_distances(path)
	"""

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

	Returns
    -------
    time differences : list
    	contains the time differences along the path.

	"""

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

	"""

    if len(distances) is not len(time_diffs):
        raise ValueError("lengths of distances and time_diffs must be same")
    
    ## caution: time_diff should not contain 0.
    
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
    	the time difference within the path. Expecting the output of take_time_diffs. 
    	Must have the same length as distances. Should not contain 0; otherwise output would 
    	contain inf.

	Returns
    -------
    speeds : list
    	contains the speeds along the path.

	"""

    if len(speeds) is not len(timestamps)-1:
        raise ValueError("lengths of speeds must be the length of timestamps minus 1")
        
    ## caution: timestamps shoud not contain same time at adjacet rows
    
    speeds_diff = [ x - y for x,y in zip(speeds[:len(speeds)], speeds[1:])] 
    time_diffs = [ x - y for x,y in zip(timestamps[:len(timestamps)-1], timestamps[2:])]
    out = [v/t for v,t in zip(speeds_diff, time_diffs)]
    return(out)

def unit_vector(vector):
    r""" Returns the unit vector of the vector.  """
    return(vector / np.linalg.norm(vector))

def angle_between(v1, v2):
    r"""
    Returns the angle in radians between vectors 'v1' and 'v2'::

    Examples
    --------
    >>> angle_between((1, 0, 0), (0, 1, 0))
    1.5707963267948966
    >>> angle_between((1, 0, 0), (1, 0, 0))
    0.0
    >>> angle_between((1, 0, 0), (-1, 0, 0))
    3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    
def compute_angles(path_obj, radian):
	r"""
	Returns a list of the angles in the path.
	Each element of the list is the angle between the adjacent vectors in the path.
	The length of the list is equal to the length of speeds minus 2.

	Parameters
    ----------
    path_obj : pandas.DataFrame
        CT, CX, CY coordinates and homebase status.
	radian : boolean
    	True for the output in radians. False for in turns (i.e. 360 for a full turn).

	Returns
    -------
    angles : list
    	contains the angles in the path.
	"""

    if type(radian) != bool:
        raise TypeError("radian must be bool")
    indices = path_obj.index[:len(path_obj)-1]
    vectors = [path_obj.loc[i + 1,'x':'y'] - path_obj.loc[i,'x':'y'] for i in indices]
    angles = [angle_between(v1,v2) for v1,v2 in zip(vectors[1:], vectors[:len(vectors)])]
    if not radian:
        angles = [theta * 180 / math.pi for theta in out]
    return(angles)
