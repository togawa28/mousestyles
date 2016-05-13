import mousestyles.ultradian as ultradian
import matplotlib.pyplot as plt

plt.style.use('ggplot')


fig_W = ultradian.plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                                       feature="W", bin_width=30,
                                       period_length=24)
fig_F = ultradian.plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                                       feature="F", bin_width=30,
                                       period_length=24)
fig_MIS = ultradian.plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                                         feature="M_IS", bin_width=30,
                                         period_length=24)
fig_MAS = ultradian.plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                                         feature="M_AS", bin_width=30,
                                         period_length=24)
fig_D = ultradian.plot_strain_seasonal(strains={0, 1, 2}, mouse={0, 1, 2, 3},
                                       feature="Distance", bin_width=30,
                                       period_length=24)
