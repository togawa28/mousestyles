import numpy as np
import matplotlib.pyplot as plt

from mousestyles.data.utils import day_to_mouse_average, mouse_to_strain_average, total_time_rectangle_bins, pull_locom_tseries_subset, split_data_in_half_randomly

# Make position density first mouse first day
# from mousestyles.data import load_movement
# #maybe M = load_movement(0, 0, 0)
CT = np.load('../../../../mousestyles/data/txy_coords/CT/CT_strain0_mouse0_day0.npy')
CX = np.load('../../../../mousestyles/data/txy_coords/CX/CX_strain0_mouse0_day0.npy')
CY = np.load('../../../../mousestyles/data/txy_coords/CY/CY_strain0_mouse0_day0.npy')

# mask for HB Move Events
CT_NHB = np.load('../../../../mousestyles/data/txy_coords/C_idx_HB/C_idx_HB_strain0_mouse0_day0.npy')
CT_HB = ~ CT_NHB

start_time, stop_time = np.load('../../../../mousestyles/data/txy_coords/recordingStartTimeEndTime/recordingStartTimeEndTime_strain0_mouse0_day0.npy')

# Cage boundaries
YLower = 1.0; YUpper = 43.0; XUpper = 3.75; XLower = -16.25
xbins = 12; ybins = 24
M = np.vstack([CT, CX, CY])
pos_subset = pull_locom_tseries_subset(M, start_time, stop_time)
bin_times = total_time_rectangle_bins(pos_subset, xlims=(XLower, XUpper), ylims=(YLower, YUpper), xbins=xbins, ybins=ybins)
position_pdf = bin_times / bin_times.sum()

plt.matshow(position_pdf)
plt.title('Cage PDF: 1st Strain, 1st Mouse, 1st Day (12 x 24)')
plt.xlabel('Cage X discretized coordinate')
plt.ylabel('Cage Y discretized coordinate')
