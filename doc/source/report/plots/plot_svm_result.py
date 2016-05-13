import numpy as np
import pandas as pd
from mousestyles.visualization import plot_classification


# load data
SVM_result = pd.DataFrame(np.load('SVM_result.npy'))
# plot
plot_classification.plot_performance(SVM_result)
