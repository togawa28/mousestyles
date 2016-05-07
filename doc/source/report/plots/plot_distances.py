import matplotlib.pyplot as plt

from mousestyles.data import distances_bystrain


threshold = 0.1
numbins = 30
xlim = [0, 40]
col = 'blue'
verbose = False
step = 50

plt.style.use('ggplot')
plt.style.use('seaborn-notebook')

# Extract strain data
dist_strain = []
strain = 0
dist = distances_bystrain(strain, step=step)
while dist.size > 0:
    dist_strain.append(dist[dist >= threshold])
    if verbose:
        print('strain %s loaded.' % strain)
    strain += 1
    dist = distances_bystrain(strain, step=step)

# Plot
fig = plt.figure(1)
fig.subplots_adjust(hspace=.6)
nb_plots = strain
for i, s in enumerate(dist_strain):
    index_plot = nb_plots * 100 + 10 + i + 1
    plt.subplot(index_plot)
    plt.hist(s, numbins, normed=1, facecolor=col, alpha=0.5, range=xlim)
    plt.ylabel('Density')
    plt.title('strain %s' % i)
plt.xlabel('Distance (cm)')
plt.show()
