from mousestyles.visualization.plot_ultradian import plot_strain_seasonal
import matplotlib.pyplot as plt

plt.style.use('ggplot')


fig_W = plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                             feature="W", bin_width=30,
                             period_length=24)
fig_F = plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                             feature="F", bin_width=30,
                             period_length=24)
fig_MIS = plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                               feature="M_IS", bin_width=30,
                               period_length=24)
