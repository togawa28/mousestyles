from mousestyles import data
from matplotlib import pyplot as plt

plt.style.use('ggplot')

# load data
mouse_data = data.load_all_features()

fig = plt.figure(figsize = (18, 18))
for i in range(4, len(mouse_data.columns)):
    ax = fig.add_subplot(3, 3, i-3)
    feature = mouse_data[mouse_data.columns[i]]
    features = [feature.loc[mouse_data.strain == j] for j in range(16)]
    ax.boxplot(features)
    ax.set_xlabel('Strains')
    ax.set_ylabel('Value')
    ax.set_title(str(mouse_data.columns[i]))

plt.show()
