import numpy as np
import pandas as pd
from mousestyles.visualization import plot_classification


# load data
GB_result = pd.DataFrame(np.load('GB_result.npy'))
# plot
plot_classification.plot_performance(GB_result)
