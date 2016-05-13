from mousestyles import data
from mousestyles.classification import clustering
from mousestyles.visualization import plot_clustering


# load data
mouse_data = data.load_all_features()

# mouse inidividual
mouse_dayavgstd_rsl = clustering.prep_data(mouse_data, melted=False, std = True, rescale = True)

# optimal parameters
method, dist = clustering.get_optimal_hc_params(mouse_day=mouse_dayavgstd_rsl)

# fit hc
sils_hc, labels_hc = clustering.fit_hc(
    mouse_day_X=mouse_dayavgstd_rsl[:,2:],
    method=method, dist=dist, num_clusters=range(2,17))

# plot and get the distance matrxix
Z = plot_clustering.plot_dendrogram(
        mouse_day=mouse_dayavgstd_rsl, method=method, dist=dist)
