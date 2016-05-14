#!/usr/bin/python

import mousestyles.behavior as bh
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# get a tree for each day for two different mice
mouse1_trees = [bh.compute_tree('F', 0, 0, d) for d in range(11)]
mouse2_trees = [bh.compute_tree('F', 0, 1, d) for d in range(11)]
print(mouse1_trees[0])
print(mouse2_trees[0])

# merge each of the trees for the two mice
mouse1_merged = bh.BehaviorTree.merge(*mouse1_trees)
mouse2_merged = bh.BehaviorTree.merge(*mouse2_trees)
print(mouse1_merged)
print(mouse2_merged)

# get the means for the two mice
print(mouse1_merged.summarize(np.mean))
print(mouse2_merged.summarize(np.mean))

# turn the tree into pandas DataFrame
mouse1_df = pd.DataFrame.from_dict(mouse1_merged.contents)
# this gives us another way to compute summary statistics
print(mouse1_df.describe())


# plot the AS Probability over time
plt.plot(range(11),
         mouse1_merged['AS Prob'], 'r',
         mouse2_merged['AS Prob'], 'g')
plt.title('Mouse 1 and 2 AS prob. over time')
plt.show()

# plot consumption vs. AS prob
plt.plot(mouse2_merged['AS Prob'],
         mouse2_merged['Consumption Rate'], 'go')
plt.title('Mouse 2 consumption rate vs. AS prob.')
plt.show()
