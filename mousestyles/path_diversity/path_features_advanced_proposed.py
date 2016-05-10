from future import print_function, absolute_import, division
import numpy as np
import pandas as pd
from mousestyles.path_diversity.path_features import angle_between
from mousestyles.path_diversity import path_index

def compute_advanced(path_obj):
    r"""
    Return dictionary containing the radius, area of the rectangle 
    spanned by the path, and absolute distance between start and end
    points of each path.

    Parameters
    ----------
    path_obj : pandas.DataFrame
        CX and CY must be contained.
        The length must be greater than 2.

    Returns
    -------
    radius : numpy float object
        each element is the distance between center point and
        each point in the path. The length equals to the length
        of the path_obj.

    area : numpy float object
        area of the rectangle spanned by the path.

    abs_distance : numpy float
        the distance between the start and end points in a path.

    Examples
    --------
    >>> movement = data.load_movement(1,2,1)
    >>> compute_advanced(movement)
    """
    if not isinstance(path_obj, pd.core.frame.DataFrame):
        raise TypeError("path_obj must be pandas DataFrame")

    if not set(path_obj.keys()).issuperset(['x', 'y']):
        raise ValueError("the keys of path_obj must contain 'x', 'y'")

    if len(path_obj) <= 1:
        raise ValueError("path_obj must contain at least 2 rows")

    # Computes edge points like find_edge_points originally did compute_area_rectangle did
    edge_points = {'xmin': np.min(path_obj.x), 'xmax': np.max(path_obj.x),
                   'ymin': np.min(path_obj.y), 'ymax': np.max(path_obj.y)}

    # Computes area of rectangle
    area = (edge_points['xmax']-edge_points['xmin']) * (edge_points['ymax']-edge_points['ymin'])

    # Computes center like find_center originally did
    center = {'x': (edge_points['xmin'] + edge_points['xmax'])/2,
              'y': (edge_points['ymin'] + edge_points['ymax'])/2}

    # Computes average radius
    indices = path_obj.index[:-1]
    vectors = [path_obj.loc[i, 'x':'y'] -
               [center['x'], center['y']] for i in indices]
    radius = [np.linalg.norm(v) for v in vectors]
    # but maybe we just want a single number for this? We could do average or sum?
    avg_radius = sum(radius)/len(radius)

    # Computes distance between start and end points of each path
    initial = path_obj.loc[path_obj.index[0], 'x':'y']
    end = path_obj.loc[path_obj.index[-1], 'x':'y']
    abs_distance = np.sqrt((end['x'] - initial['x'])**2 +
                           (end['y'] - initial['y'])**2)

    return({'radius': avg_radius, 'area': area, 'abs_distance': abs_distance})`
