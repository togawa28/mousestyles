import numpy as np
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV

def kde(x, x_grid=np.linspace(0, 3, 300)):
    """
    Return a numpy.ndarray object of estimated density
    
    Parameters
    ----------
    x      : numpy.ndarray
        observations of variable x
    x_grid : numpy.ndarray
        the grid points for the estimated density
    
    Returns
    -------
    pdf : numpy.ndarray
        estimated density at the specified grid points
        
    Examples
    --------
    >>> kde(x = np.array([2,3,1,0]), x_grid=np.linspace(0, 5, 10))
    array([ 0.17483395,  0.21599529,  0.23685855,  0.24007961,  0.22670763,
        0.19365019,  0.14228937,  0.08552725,  0.04043597,  0.01463953])
    """
    # use GridSearchCV to search for the best bandwidth by 10 fold cross-validation max loglikelihood
    grid = GridSearchCV(KernelDensity(),
                    {'bandwidth': np.linspace(0.1, 1.0, 10)},
                    cv=min(5, len(x)))
    grid.fit(x[:, None])
    bandwidth = grid.best_params_['bandwidth']
    # setup and do desity estimation
    kde_skl = KernelDensity(bandwidth=bandwidth)
    kde_skl.fit(x[:, np.newaxis])
    log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
    # transform the fuction score function to density
    pdf = np.exp(log_pdf)
    return(pdf)