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


def plot_strain_cluster(count_data, groupby_cluster=True):
    """
    Plot the side by side bar chart showing the strain distribution
    of mice in different clusters or the cluster distribution in different
    strains 

    Parameters
    ----------
    count_data: Dictionary
        A dictionary object with the keys are the cluster numbers and the
        values are lists containing strain counts
    groupbu_cluster: Boolean
        If True, then the barchart is group by cluster otherwise by strain
    """
    fig,ax = plt.subplots()
    n_groups = len(count_data)
    index = np.arange(n_groups)
    LABEL_COLOR_MAP = {0 : 'r', 1 : 'b', 2 : 'y',
                   3 : 'g', 4 : 'chocolate', 5 : 'm',
                   6 : 'k', 7 : 'gray', 8 : 'maroon',
                   9 : 'coral', 10 : 'lime', 11 : 'blueviolet',
                   12 : 'deeppink', 13 : 'steelblue', 14 : 'tan',
                   15 : 'orange' }
    strain_names = {0: 'C57BL6J', 1: 'BALB', 2: 'A', 3: '129S1', 4: 'DBA', 
            5: 'C3H',
            6: 'AKR', 7: 'SWR', 8: 'SJL', 9: 'FVB', 10: 'WSB', 11: 'CZECH',
            12: 'CAST', 13: 'JF1', 14: 'MOLF', 15: 'SPRET'}
    bar_width = 1 / len(count_data[0])
    opacity = 0.4
    for i in range(len(count_data[0])):
        sub_count_data = [t[i] for t in count_data.values()]
        plt.bar(
        index + i * bar_width, sub_count_data, bar_width,
        alpha=opacity,
        color=LABEL_COLOR_MAP[i],
        label=strain_names[i])
    if groupby_cluster == True:
        plt.xlabel('Clusters')
        plt.title('Counts by cluster and strain')
    else:
        plt.xlabel('Strains')
        lt.title('Counts by strain and cluster')
    plt.ylabel('Counts')
    plt.xticks(
        (index + 1) * len(count_data[0]) * bar_width - 0.5, 
        ['Cluster' + str(t) for t in range(1,n_groups + 1)])
    for x in range(1, n_groups + 1):
        plt.axvline(x=x, linestyle='--')
    ax.set_xlim([0.0, n_groups + 1])
    plt.legend(loc='right')
    plt.tight_layout()
    plt.show()