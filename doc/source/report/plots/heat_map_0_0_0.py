import numpy as np
import matplotlib.pyplot as plt

from mousestyles.data import load_movement, load_start_time_end_time
from mousestyles.data.utils import (total_time_rectangle_bins,
                                    pull_locom_tseries_subset)

# Make position density first mouse first day
# Make position density first mouse first day
# from mousestyles.data import load_movement
M = load_movement(0, 0, 0)
CT = M['t']
CX = M['x']
CY = M['y']

# mask for HB Move Events
CT_NHB = M['isHB']
CT_HB = ~ CT_NHB

start_time, stop_time = load_start_time_end_time(0, 0, 0)

# Cage boundaries
YLower = 1.0
YUpper = 43.0
XUpper = 3.75
XLower = -16.25
xbins = 12
ybins = 24
M = np.vstack([CT, CX, CY])
pos_subset = pull_locom_tseries_subset(M, start_time, stop_time)
bin_times = total_time_rectangle_bins(pos_subset, xlims=(
    XLower, XUpper), ylims=(YLower, YUpper), xbins=xbins, ybins=ybins)
position_pdf = bin_times / bin_times.sum()

plt.matshow(position_pdf)
