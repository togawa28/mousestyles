from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import pairwise_distances, silhouette_samples, silhouette_score
from sklearn import metrics
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from mousestyles import data
from mousestyles.data_utils import day_to_mouse_average

##### prep data functions
def prep_data(mouse_data, std = True, rescale = True):
    """
    Returns a ndarray data to be used in clustering algorithms:
        column 0 : strain,
        column 1: mouse,
        other columns corresponding to feature avg/std of a mouse over 16 days
            that may or may not be rescaled to the same unit as specified
        
    Parameters
    ----------
    mouse_data: a 21131 * 13 pandas DataFrame, 
        column 0 : strain,
        column 1: mouse,
        column 2: day,
        column 3: hour,
        other columns corresponding to features
    std: bool,
        whether the standard deviation of each feature is returned
    rescale: bool,
        whether each column is rescaled or not (rescale is performed by the 
        column's maximum)

    Returns
    ----------
    The ndarray as specified
    """
    mouse_X = np.array(mouse_data.iloc[:,4:], dtype=float) # no hour attribute
    mouse_labels = np.array(mouse_data.iloc[:,0:3])
    mouse_dayavg, mouse_daystd = day_to_mouse_average(mouse_X, mouse_labels,\
    num_strains=16, stdev=True, stderr=False) # 11 cols
    mouse_dayavgstd = np.hstack([mouse_dayavg, mouse_daystd[:, 2:]]) # 20 cols
    mouse_dayavgstd_X = mouse_dayavgstd[:, 2:]
    mouse_dayavgstd_X_scl = mouse_dayavgstd_X / np.max(mouse_dayavgstd_X, \
    axis = 0)
    mouse_dayavgstd_scl = np.hstack([mouse_dayavgstd[:, 0:2],\
    mouse_dayavgstd_X_scl])
    if (std == False and rescale == False):
        return(mouse_dayavg)
    elif (std == True and rescale == True):
        return(mouse_dayavgstd)
    elif (std == False and rescale == True):
        return(mouse_dayavgstd_scl[:, 0:(mouse_dayavg.shape[1])])
    else:
        return(mouse_dayavgstd_scl)

##### model fitting functions
def get_optimal_hc_params(mouse_day):
    """
    Returns a list of 2: [method, dist]
        method: {'ward', 'average', 'complete'}
        dist: {'cityblock', 'euclidean', 'chebychev'}

    Parameters
    ----------
    mouse_day: a 170 * M numpy array, 
        column 0 : strain,
        column 1: mouse,
        other columns corresponding to feature avg/std of a mouse over 16 days

    Returns
    -------
    method_distance: list
        [method, dist]
    """
    methods = ['ward', 'average', 'complete']
    dists = ['cityblock', 'euclidean', 'chebychev']
    
    method_dists = [(methods[i], dists[j]) for i in range(len(methods)) \
    for j in range(len(dists))]
    method_dists = [(method, dist) for method, dist in method_dists \
    if method != 'ward' or dist == 'euclidean']
    
    cs = []
    for method, dist in method_dists:
        Z = linkage(mouse_day[:, 2:], method=method, metric=dist)
        c, coph_dists = cophenet(Z, pdist(mouse_day[:, 2:]))
        cs.append(c)
        
    # determine the distance method
    method, dist = method_dists[np.argmax(cs)]
    return([method, dist])
    

def fit_hc(mouse_day_X, method, dist, num_clusters = range(2,17)):
    """
    Returns a list of 2: [silhouettes, cluster_labels]
        silhouettes: list of float,
        cluster_labels: list of list, 
            each sublist is the labels corresponding to the silhouette

    Parameters
    ----------
    mouse_day_X: a 170 * M numpy array, 
        all columns corresponding to feature avg/std of a mouse over 16 days
    method: str,
        method of calculating distance between clusters
    dist: str,
        distance metric
    num_clusters: range
        range of number of clusters

    Returns
    -------
    A list of 2: [silhouettes, cluster_labels]
    """
    if (dist == "chebychev"):
        dist = "chebyshev"
    cluster_labels=[]
    silhouettes = []
    for n_clusters in num_clusters:
        clustering = AgglomerativeClustering(linkage=method, \
        n_clusters=n_clusters) # use the optimal method determined above
        clustering.fit(mouse_day_X)
        labels = clustering.labels_
        silhouettes.append(metrics.silhouette_score(mouse_day_X, labels, \
        metric=dist)) # ward use euclidean distance
        cluster_labels.append(list(labels))
    
    return([silhouettes, cluster_labels])  

        
##### plotting functions
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
    plt.ylabel('{} distance'.format(dist) + '\n{} linkage method'.format(method))
    dendrogram(
        Z,
        truncate_mode='lastp',  # show only the last p merged clusters
        p=10,  # show only the last p merged clusters
        leaf_rotation=90., # rotates the x axis labels
        leaf_font_size=12.,  # font size for the x axis labels
        show_contracted=True,
    )
    plt.show()
    return(Z)


def plot_lastp_dist(Z, method, dist, p = 10):
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
    plt.ylabel('{} distance'.format(dist) + '\n({} linkage method)'.format(method))
    line1, = plt.plot(idxs, last_rev, label = '{} distance'.format(dist))
    
    # plot the 2nd derivative of the distances
    acceleration = np.diff(last, 2)
    acceleration_rev = acceleration[::-1]
    line2, = plt.plot(idxs[:-2] + 2, acceleration_rev, \
    label = '2nd derivative of {} distance'.format(dist))
    plt.legend(handles = [line1, line2])
    plt.show()

def get_optimal_fit_kmeans(mouse_X,num_clusters,raw=False):
    """
    Returns a list of 2: [silhouettes, cluster_labels]
        silhouettes: list of float,
        cluster_labels: list of list, 
            each sublist is the labels corresponding to the silhouette

    Parameters
    ----------
    mouse_X: a 170 * M numpy array or 21131 * M numpy array, 
        all columns corresponding to feature avg/std of a mouse over 16 days
        or the raw data without averaging over days
    num_clusters: range or a list or a numpy array
        range of number of clusters
    raw: a boolean with default is False
       False if using the 170 * M array
    Returns
    -------
    A list of 2: [silhouettes, cluster_labels]
    """

    if raw=True:
        sample_amount=1000
    else: sample_amount=mouse_X.shape[0]
    cluster_labels=[]
    silhouettes = []
    for n_clusters in num_clusters:
        clustering = KMeans(n_clusters=n_clusters)
        clustering.fit(mouse_X)
        labels = clustering.labels_
        silhouettes.append(metrics.silhouette_score(mouse_X, labels,\
        metric="euclidean",sample_size=sample_amount))
        cluster_labels.append(list(labels))
    return([silhouettes,cluster_labels])

def cluster_in_strain(labels_first,labels_second):
    """
    Returns a dictionary object indicating the count of different
    clusters in each different strain (when put cluster labels as first) 
    or the count of different strain in each clusters (when put strain
    labels as first).

    Parameters
    ----------
    labels_first: numpy arrary or list
        A numpy arrary or list of integers representing which cluster 
        the mice in, or representing which strain mice in.
    labels_second: numpy arrary or list
        A numpy array or list of integers (0-15) representing which strain 
        the mice in, or representing which cluster the mice in  

    Returns
    -------
    count_data : dictionary
        A dictioanry object with key is the strain number and value is a list 
        indicating the distribution of clusters, or the key is the cluster 
        number and the value is a list indicating the distribution of each
        strain.

    Examples
    --------
    >>> count_1=cluster_in_strain([1,2,1,0,0],[0,1,1,2,1])
    """
    count_data={}
    labels_first=np.asarray(labels_first)
    labels_second=np.asarray(labels_second)
    for label_2 in np.unique(labels_second):
        label_2_index=labels_second==label_2
        label_1_sub=labels_first[label_2_index]
        count_list=[]
        for label_1 in np.unique(labels_first):
            count_list.append(sum(label_1_sub==label_1))
        count_data[label_2]=count_list
    return(count_data)

