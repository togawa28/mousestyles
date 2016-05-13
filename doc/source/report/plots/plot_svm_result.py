import numpy as np
import pandas as pd
import os.path as _osp
from mousestyles import pkg_dir
from mousestyles.visualization import plot_classification


# load data
SVM_result = pd.DataFrame(np.load(
                            _osp.join(
                                pkg_dir, '..', 'doc', 'source', 'report', 'plots',
                                'SVM_result.npy')))
# plot
plot_classification.plot_performance(SVM_result)
