
from mousestyles import data
from mousestyles.classification import clustering


def test_prep_data():
    # Check prep_data return the correct dimension
    mouse_data = data.load_all_features()
    preped_data = clustering.prep_data(mouse_data)
    assert preped_data.shape == (170, 20)


def test_hc_param():
    # Check get_optimal_hc_params returns appropriate parameters
    mouse_data = data.load_all_features()
    preped_data = clustering.prep_data(mouse_data)
    method, dist = clustering.get_optimal_hc_params(preped_data)
    assert method in ['ward', 'average', 'complete']
    assert dist in ['cityblock', 'euclidean', 'chebychev']


def test_fit_hc():
    # Check fit_hc returns appropriate result
    mouse_data = data.load_all_features()
    preped_data = clustering.prep_data(mouse_data)
    mouse_day_X = preped_data[:, 2:]
    res = clustering.fit_hc(mouse_day_X, "average", "chebychev",
                            num_clusters=range(2, 17))
    assert len(res) == 2
    assert len(res[0]) == 15
    assert len(res[1][0]) == 170
    assert len(set(res[1][14])) <= 16
    # silhouette score should be between -1 and 1
    assert all(value < 1 for value in res[0])
    assert all(value > -1 for value in res[0])


def test_fit_kmeans():
    # Check get_optimal_fit_kmeans returns expected result
    mouse_data = data.load_all_features()
    preped_data = clustering.prep_data(mouse_data)
    mouse_day_X = preped_data[:, 2:]
    res = clustering.get_optimal_fit_kmeans(
        mouse_day_X, num_clusters=range(2, 17), raw=False)
    assert len(res) == 2
    assert len(res[0]) == 15
    assert len(res[1][0]) == 170
    assert len(set(res[1][14])) <= 16
    # silhouette score should be between -1 and 1
    assert all(value < 1 for value in res[0])
    assert all(value > -1 for value in res[0])


def test_cluster_in_strain():
    # Check cluster_in_strain calculate correct strain counts
    res = clustering.cluster_in_strain([1, 2, 1, 0, 0], [0, 1, 1, 2, 1])
    assert res == {0: [0, 1, 0], 1: [1, 1, 1], 2: [1, 0, 0]}
