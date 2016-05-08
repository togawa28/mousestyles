from matplotlib import pyplot as plt


def plot_dendrogram(mouse_day, method, dist):
    """
    Returns a linkage matrix and plot the dendrogram

    Parameters
    ----------
    mouse_day: a 170 * M numpy array,
        column 0 : strain,
        column 1: mouse,
        other columns corresponding to feature avg/std of a mouse over 16 days
    method: string,
        method of calculating distance between clusters
    dist: string,
        distance metric

    Returns
    -------
    Z: ndarray
        The hierarchical clustering encoded as a linkage matrix.
    """

    # calculate full dendrogram of the optimal pair of parameters
    Z = linkage(mouse_day[:, 2:], method=method, metric=dist)
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Mouse')
    plt.ylabel(
        '{} distance'.format(dist) +
        '\n{} linkage method'.format(method))
    dendrogram(
        Z,
        truncate_mode='lastp',  # show only the last p merged clusters
        p=10,  # show only the last p merged clusters
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=12.,  # font size for the x axis labels
        show_contracted=True,
    )
    plt.show()
    return(Z)


def plot_lastp_dist(Z, method, dist, p=10):
    """
    Plot the distances between clusters of last p merges in hierarchical
    clustering

    Parameters
    ----------
    Z: ndarray
        The hierarchical clustering encoded as a linkage matrix
    p: int, optional
        number of merges to plot

    Returns
    -------
    Z: ndarray
        The hierarchical clustering encoded as a linkage matrix.
    """
    last = Z[-p:, 2]
    last_rev = last[::-1]
    idxs = np.arange(1, len(last) + 1)
    plt.figure(figsize=(10, 10))
    plt.title('Distance of last 10 cluster merges')
    plt.xlabel('Last cluster merge')
    plt.ylabel(
        '{} distance'.format(dist) +
        '\n({} linkage method)'.format(method))
    line1, = plt.plot(idxs, last_rev, label='{} distance'.format(dist))

    # plot the 2nd derivative of the distances
    acceleration = np.diff(last, 2)
    acceleration_rev = acceleration[::-1]
    line2, = plt.plot(
        idxs[:-2] + 2, acceleration_rev,
        label='2nd derivative of {} distance'.format(dist))
    plt.legend(handles=[line1, line2])
    plt.show()
