import numpy as np
import pandas as pd
from mousestyles.visualization import plot_classification


# load data
RF_result = pd.DataFrame(np.load('RF_result.npy'))
GB_result = pd.DataFrame(np.load('GB_result.npy'))
SVM_result = pd.DataFrame(np.load('SVM_result.npy'))
total = pd.concat([RF_result.iloc[:, 2], GB_result.iloc[:, 2],
                   SVM_result.iloc[:, 2]], axis=1)
# plot
plot_classification.plot_comparison(total)
