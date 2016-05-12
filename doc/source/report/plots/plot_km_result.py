from mousestyles import data
from mousestyles.classification import clustering
from mousestyles.visualization import plot_clustering

# load data
mouse_data = data.load_all_features()

# mouse inidividual
mouse_dayavgstd_rsl = clustering.prep_data(
                        mouse_data, melted=False, std = True, rescale = True)

# kmeans
sils_km, labels_km = clustering.get_optimal_fit_kmeans(
                        mouse_X = mouse_dayavgstd_rsl[:,2:],
                        num_clusters = range(2,17))
# result
result = clustering.cluster_in_strain(mouse_dayavgstd_rsl[:, 0], labels_km[2])

# plot
plot_clustering.plot_strain_cluster(count_data=result, groupby_cluster=True)
