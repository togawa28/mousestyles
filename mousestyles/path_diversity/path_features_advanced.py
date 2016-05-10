from __future__ import print_function, absolute_import, division
import numpy as np
import pandas as pd
# from mousestyles.path_features import path_features
from path_features import angle_between


def find_edge_points(path_obj):
    r"""
    Returns a dictionary of the edge points of the path object.

    The dictionary containts min and max of each of the x, y coordinates in the path.

    Parameters
    ----------
    path_obj : pandas.DataFrame
        CX and CY must be contained.
        The length must be greater than 2.

    Returns
    -------
    edge points : dictionary
        contains edge points the path which are
        'xmin', 'xmax', 'ymin', and 'ymax'

    Examples
    --------
    >>> movement = data.load_movement(1,2,1)
    >>> sep = path_index(movement, 1, 1)
    >>> path = movement[sep[2][0]:sep[2][1]+1]
    >>> edges = find_edge_points(path)
    """
    if not isinstance(path_obj, pd.core.frame.DataFrame):
        raise TypeError("path_obj must be pandas DataFrame")

    if not set(path_obj.keys()).issuperset(['x', 'y']):
        raise ValueError("the keys of path_obj must contain 'x', 'y'")

    if len(path_obj) <= 1:
        raise ValueError("path_obj must contain at least 2 rows")

    return( {'xmin' : np.min(path_obj.x) , 'xmax' : np.max(path_obj.x) , \
             'ymin' : np.min(path_obj.y) , 'ymax' : np.max(path_obj.y)} )

def compute_area_rectangle(edge_points):
    r"""
    Returns the area of the rectangle spanned by the path.

    The rectangle, constructed by edge_points which is supposed
    to have xmin, xmax, ymin, and ymax, has 4 edges which are
    1) (xmin, ymin)
    2) (xmin, ymax)
    3) (xmax, ymin)
    4) (xmax, ymax)

    The path which has such edge points is by design completely
    covered by such rectangle.

    Parameters
    ----------
    edge_points : dictionary
        key must be xmin, xmax, ymin, ymax.
        Expecting the output of find_edge_points.

    Returns
    -------
    area : numpy float object
        area of the rectangle spanned by the path.

    Examples
    --------
    >>> movement = data.load_movement(1,2,1)
    >>> sep = path_index(movement, 1, 1)
    >>> path = movement[sep[2][0]:sep[2][1]+1]
    >>> edges = find_edge_points(path)
    >>> area_rec = compute_area_rectangle(edges)
    """
    if not isinstance(edge_points, dict):
        raise TypeError("edge_points must be a dictionary")

    if set(edge_points.keys()) != {'xmax', 'xmin', 'ymax', 'ymin'}:
        raise ValueError("the keys of edge_points must be 'xmax', 'xmin', 'ymax', and 'ymin'")

    return( (edge_points['xmax']-edge_points['xmin']) * \
           (edge_points['ymax']-edge_points['ymin']) )

def find_center(edge_points):
    r"""
    Returns the center point of the path.

    The center point is defined by the intersection point of
    2 diagonal lines of the rectangle which is constructed by
    edge_points. That is, for the elements of edge_points,
    xmin, xmax, ymin, and ymax, the center point is expressed by

    x_center = (xmin + xmax)/2,
    y_center = (ymin + ymax)/2.

    Parameters
    ----------
    edge_points : dictionary
        its key must be 'xmin', 'xmax', 'ymin', 'ymax'.
        Expecting the output of find_edge_points.

    Returns
    -------
    center point of the path : dictinoary
        defined by the intersection point of 2 diagonal lines of the
        rectangle spanned by the path.

    Examples
    --------
    >>> movement = data.load_movement(1,2,1)
    >>> sep = path_index(movement, 1, 1)
    >>> path = movement[sep[2][0]:sep[2][1]+1]
    >>> edges = find_edge_points(path)
    >>> cent = find_center(edges)
    """
    if not isinstance(edge_points, dict):
        raise TypeError("edge_points must be a dictionary")

    if set(edge_points.keys()) != {'xmax', 'xmin', 'ymax', 'ymin'}:
        raise ValueError("the keys of edge_points must be \
           'xmax', 'xmin', 'ymax', and 'ymin'")

    return( { 'x' : (edge_points['xmin'] + edge_points['xmax'])/2 , \
             'y' : (edge_points['ymin'] + edge_points['ymax'])/2 } )


def compute_radius_and_center_angle(path_obj, center):
    r"""
    Returns radius and center angles of the path.

    Radius of a path are defined by the length of each vector which
    connects the center point and each point in the path. The number
    of radius in a path is by design equal to the number of points in
    the path.

    For vectors connecting the center and each point in a path,
    center angles of the path are the angles between the 2 adjacent vectors.
    The number of the center angles in the path is by design equal to
    the number of points in the path minus 1.

    Parameters
    ----------
    path_obj : pandas.DataFrame
        CX and CY must be contained.
        The length must be greater than 2.

    center : dictionary
        its key must be 'x' and 'y'.
        Expecting the output of find_center.

    Returns
    -------
    dictionary having the following elements.
    radius : list
        each element is the distance between center point and
        each point in the path. The length equals to the length
        of the path_obj.

    center_anlges : list
        each element is the center angle generated by 2 adjacent
        radius. The length equals to the length of the radius minus 1.

    Examples
    --------
    >>> movement = data.load_movement(1,2,1)
    >>> sep = path_index(movement, 1, 1)
    >>> path = movement[sep[2][0]:sep[2][1]+1]
    >>> edges = find_edge_points(path)
    >>> cent = find_center(edges)
    >>> r_and_ca = compute_radius_and_center_angle(path, cent)
    """
    if not isinstance(path_obj, pd.core.frame.DataFrame):
        raise TypeError("path_obj must be pandas DataFrame")

    if not set(path_obj.keys()).issuperset(['x', 'y']):
        raise ValueError("the keys of path_obj must contain 'x', 'y'")

    if len(path_obj) <= 1:
        raise ValueError("path_obj must contain at least 2 rows")

    if not isinstance(center, dict):
        raise TypeError("center must be a dictionary")

    if set(center.keys()) != {'x', 'y'}:
        raise ValueError("the keys of center must be 'x', and 'y'")

    indices = path_obj.index[:-1]
    vectors = [ path_obj.loc[i,'x':'y'] - [center['x'],center['y']] for i in indices]
    # center_angles = [oath_features.angle_between(v1,v2) for v1,v2 in zip(vectors[1:], vectors[:len(vectors)])]
    center_angles = [angle_between(list(v1),list(v2)) for v1,v2 in zip(vectors[1:], vectors[:-1])]
    radius = [np.linalg.norm(v) for v in vectors]
    return({'radius': radius, 'center_angles': center_angles})

def compute_area_covered(r_and_theta):
    r"""
    Returns the area spanned by the path.

    For 2 adjacent points in a path and its center, the area of the triangle
    constructed by such 3 points can be calculated by the 2 radius and the center
    angle: let r1 and r2 be 2 adjacent radius, and theta be the angle between such 2 vectors.
    The area of the triangle is then calculated by
    r1 * r2 * sin(theta) / 2.

    This function sums up such areas of the triangles over all pairs of 2 adjacent points
    in the path.

    Parameters
    ----------
    r_and_theta : dictionary
        its key must be radius and center_angles.
        Expecting the output of compute_area_radius_and_center_angle.

    Returns
    -------
    area : numpy float
        area computed by radius and center angles in the path.

    Examples
    --------
    >>> movement = data.load_movement(1,2,1)
    >>> sep = path_index(movement, 1, 1)
    >>> path = movement[sep[2][0]:sep[2][1]+1]
    >>> edges = find_edge_points(path)
    >>> cent = find_center(edges)
    >>> r_and_ca = compute_radius_and_center_angle(path, cent)
    >>> area = compute_area_covered(r_and_ca)
    """

    if not isinstance(r_and_theta, dict):
        raise TypeError("r_and_theta must be a dictionary")

    if set(r_and_theta.keys()) != {'radius', 'center_angles'}:
        raise ValueError("the keys of r_and_theta must be 'radius' and 'center_angles'")

    if not isinstance(r_and_theta['radius'], list):
        raise TypeError("r_and_theta['radius'] must be a list")

    if not isinstance(r_and_theta['center_angles'], list):
        raise TypeError("r_and_theta['center_angles'] must be a list")

    if len(r_and_theta['radius']) != len(r_and_theta['center_angles']) + 1:
        raise ValueError("length of r_and_theta['radius'] must be \
            the length of r_and_theta['center_angles'] plus 1")

    zipped = zip(r_and_theta['radius'][1:], r_and_theta['radius'][:-1], \
                 r_and_theta['center_angles'])
    areas = [ v1 * v2 * np.sin(theta) / 2 for v1,v2,theta in zipped]
    return(sum(areas))

def compute_start_end_distance(path_obj):
    r'''
    Returns the distance between the start and end in a path.

    Parameters
    ----------
    path_obj : pandas.DataFrame
        CX and CY must be contained.
        The length must be greater than 2.

    Returns
    -------
    start-end distance : numpy float
        the distance between the start and end points in a path.

    Examples
    --------
    >>> movement = data.load_movement(1,2,1)
    >>> sep = path_index(movement, 1, 1)
    >>> path = movement[sep[2][0]:sep[2][1]+1]
    >>> p_dist = compute_start_end_distance(path)
    '''
    if not isinstance(path_obj, pd.core.frame.DataFrame):
        raise TypeError("path_obj must be pandas DataFrame")

    if not set(path_obj.keys()).issuperset(['x', 'y']):
        raise ValueError("the keys of path_obj must contain 'x', 'y'")

    if len(path_obj) <= 1:
        raise ValueError("path_obj must contain at least 2 rows")

    initial = path_obj.loc[path_obj.index[0], 'x':'y']
    end = path_obj.loc[path_obj.index[-1], 'x':'y']
    return(np.sqrt( (end['x'] - initial['x'])**2 + (end['y'] - initial['y'])**2 ))
