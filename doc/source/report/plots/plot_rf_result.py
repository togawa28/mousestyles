import numpy as np
import pandas as pd
from mousestyles.visualization import plot_classification


# load data
RF_result = pd.DataFrame(np.load('RF_result.npy'))
# plot
plot_classification.plot_performance(RF_result)
