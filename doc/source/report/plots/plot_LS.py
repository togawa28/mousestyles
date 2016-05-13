import mousestyles.data as data
import mousestyles.ultradian as ultradian
import matplotlib.pyplot as plt
plt.style.use('ggplot')

a = ultradian.compare_strain(feature='AS', bin_width=30)
