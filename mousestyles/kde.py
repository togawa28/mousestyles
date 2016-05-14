import numpy as np
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV


def kde(x, x_grid, symmetric_correction=False, cutoff=1):
    """
    Return a numpy.ndarray object of estimated density

    Parameters
    ----------
    x      : numpy.ndarray
        data, as realiztions of variable X
    x_grid : numpy.ndarray
        the grid points for the estimated density
    symmetric_correction : boolean
        a method indicator. If False, do common gaussian kernel density
        estimation (kde). If True, do common gaussian kde on data generated
        from x concatenating with its reflection around the cutoff point. Then
        transform the estimated kde back by a factor of 2. Used for e.g. kde
        for nonnegative kernel estimation
    cutoff : float
        the axis of symmetry for symmetric correction
    Returns
    -------
    pdf : numpy.ndarray
        estimated density at the specified grid points x_grid

    Examples
    --------
    >>> kde(x = np.array([2,3,1,0]), x_grid=np.linspace(0, 5, 10))
    array([ 0.17483395,  0.21599529,  0.23685855,  0.24007961,  0.22670763,
        0.19365019,  0.14228937,  0.08552725,  0.04043597,  0.01463953])
    >>> x1 = np.concatenate([norm(-1, 1.).rvs(400), norm(1, 0.3).rvs(100)])
    >>> pdf1 = kde(x=x1, x_grid=np.linspace(0, 5, 100), symmetric_correction
                   =True, cutoff=1)
    array([ 0.26625297,  0.26818492,  0.27105849,  0.27489486,  0.27968752, ...
        0.07764054,  0.07239964,  0.06736559,  0.06254175,  0.05793043])
    """
    # if we want to do a symmetric correction to do kde, we transform
    # the data to be the symmetric format by adding the counterpart
    # obtained by reflecting the data around x=cutoff
    if symmetric_correction:
        x = np.concatenate([x, 2*cutoff - x])

    # Use GridSearchCV to search for the best bandwidth by 5 fold
    # cross-validation max loglikelihood
    grid = GridSearchCV(KernelDensity(),
                        {'bandwidth': np.linspace(0.01, 0.5, 10)},
                        cv=min(5, len(x)))
    grid.fit(x[:, None])
    bandwidth = grid.best_params_['bandwidth']

    # do desity estimation
    kde_skl = KernelDensity(bandwidth=bandwidth)
    kde_skl.fit(x[:, np.newaxis])
    log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])

    # transform the fuction score function to density
    if symmetric_correction:
        # transform back to the one-sided density in symmetric correction
        pdf = 2 * np.exp(log_pdf)
    else:
        # vanilla case
        pdf = np.exp(log_pdf)
    return pdf
