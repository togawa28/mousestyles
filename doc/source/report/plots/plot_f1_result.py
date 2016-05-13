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
GB_result = pd.DataFrame(np.load(
                            _osp.join(
                                pkg_dir, '..', 'doc', 'source', 'report',
                                'plots', 'GB_result.npy')))
SVM_result = pd.DataFrame(np.load(
                            _osp.join(
                                pkg_dir, '..', 'doc', 'source', 'report',
                                'plots', 'SVM_result.npy')))
total = pd.concat([RF_result.iloc[:, 2], GB_result.iloc[:, 2],
                   SVM_result.iloc[:, 2]], axis=1)
# plot
plot_classification.plot_comparison(total)
