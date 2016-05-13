from mousestyles.visualization.plot_ultradian import compare_strain
import matplotlib.pyplot as plt
plt.style.use('ggplot')

LS_plot = compare_strain(feature='AS', bin_width=30)
