import numpy as np
import pandas as pd
import os.path as _osp
from mousestyles import pkg_dir
from mousestyles.visualization import plot_classification


# load data
RF_result = pd.DataFrame(np.load(
                            _osp.join(
                                pkg_dir, '..', 'doc', 'source', 'report', 
                                'plots', 'RF_result.npy')))
# plot
plot_classification.plot_performance(RF_result)
