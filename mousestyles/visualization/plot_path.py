from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import matplotlib.pyplot as plt
import pandas as pd


def plot_path(movement, paths, title='example plot of path', alpha=.1,
              linewidth=1., xlim=[-16.24, 3.76], ylim=[0.9, 43.5]):
    r"""
    Plot the lines along paths.

    Parameters
    ----------
    movement : pandas.DataFrame
        CX, CY coordinates. Must have length greater than 1.

    paths: list
        a list containing the indices for all paths.

    title : str
        the title of the plot. Default is 'example plot of path'

    alpha : numeric
        graphical parameter which determines strongness of each
        line. Default is .1.

    linewidth : numeric
        graphical parameter which determines the width of each
        line. Default is 1.

    xlim, ylim : list
        list of length 2 indicating the end points of the plot.

    Returns
    -------
    Drawing the plot of the path.

    Examples
    --------
    >>> movement = data.load_movement(1,2,1)
    >>> sep = path_index(movement, 1, 1)
    >>> plot_path(movement, sep)
    """

    if not isinstance(movement, pd.core.frame.DataFrame):
        raise TypeError("movement must be pandas DataFrame")

    if not set(movement.keys()).issuperset(['x', 'y']):
        raise ValueError("the keys of movement must contain 'x', 'y'")

    if len(movement) <= 1:
        raise ValueError("movement must contain at least 2 rows")

    if not isinstance(paths, list):
        raise TypeError("paths must be a list")

    if len(paths) == 0:
        raise ValueError("length of paths is 0")

    if not isinstance(title, str):
        raise TypeError("title must be a string")

    if not isinstance(alpha, float):
        raise TypeError("alpha must be float")

    if not isinstance(linewidth, float):
        raise TypeError("linewidth must be float")

    for sep in paths:
        path = movement[sep[0]:sep[1] + 1]
        plt.plot(path['x'], path['y'], 'b',
                 linewidth=linewidth, alpha=alpha)
        plt.xlabel('x-coordinate')
        plt.xlim(xlim[0], xlim[1])
        plt.ylabel('y-coordinate')
        plt.ylim(ylim[0], ylim[1])
        plt.title(title)
