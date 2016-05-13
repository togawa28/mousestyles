from mousestyles.visualization.plot_ultradian import compare_strain
from mousestyles.visualization.plot_ultradian import plot_strain_seasonal
import matplotlib.pyplot as plt
plt.style.use('ggplot')

LS_plot = compare_strain(feature='AS', bin_width=30)


fig_AS = plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                              feature="AS", bin_width=30,
                              period_length=12)


LS_plot = compare_strain(feature='M_IS', bin_width=30)


fig_AS = plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                              feature="M_IS", bin_width=30,
                              period_length=8)
