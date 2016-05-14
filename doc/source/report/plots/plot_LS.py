from mousestyles.visualization.plot_ultradian import compare_strain
import matplotlib.pyplot as plt
plt.style.use('ggplot')

LS_plot = compare_strain(feature='Distance', bin_width=30)

LS_plot = compare_strain(feature='F', bin_width=30)

LS_plot = compare_strain(feature='W', bin_width=30)

LS_plot = compare_strain(feature='M_AS', bin_width=30)
