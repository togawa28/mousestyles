.. _classification:

Classification and Clustering of Mice
=====================================

Statement of overall problem
----------------------------

The mouse style research investigates mouse behaviors of different
genes. The researchers hope to gain insight to human behaviors using
mouse data, since experimenting directly on human is difficult.

The important concern is whether we can classify different strains of
mice based on mouse behaviors through machine learning algorithms.
Important features in classification models will be extracted for future
study. The fundamental hypothesis is that different mouse
strains have different behaviors, and we are able to use these behaviors
as features to classify mice successfully. On the other hand, we are also 
trying to use unsupervised clustering algorithms to cluster mice, and 
ideally different strains should have different clustering distributions.


Statement of statistical problems
---------------------------------

The researchers design the experiment as follow: they have 16 different
strains of mice, and each strain has 9 to 12 almost identical male mice
in terms of gene.

We need to firstly verify the assumption that mouse of different strains
do exhibit different behaviors. One way to do this is to perform
hypothesis testing based on the joint distribution of all the features.
A simpler alternative is to perform EDA on each of the features. If we
observe that each mouse behaves very similarly to its twins, but
differently from other strains of mice, we can conclude that genetic
differences affect mouse behaviors and that behavioral features might be
important for classification. Notice that here we can evaluate the
difference by assessing the classification performance of models based
on behavioral features.

**Classification**
Based on the assumption, the problem is inherently a multiclass
classification problem based on behavioral features either directly
obtained during the experiment or artificially constructed. Here we have
to determine the feature space both from the exploratory analysis and
biological knowledge. If the classification models performed well, we
may conclude that behavioral differences indeed reveal genetic
differences, and dig into the most important features needed seeking the
biological explanations. Otherwise, say if the model fails to
distinguish two different strains of mice, we may study that whether
those strains of mice are genetically similar or the behavior features
we selected are actually homogeneous through different strains of mice.

**Clustering**
To extend the scope of the analysis, the clustering analysis may also be used 
to analyze mouse behaviors. Though these mice had inherent strain labels,
the clusters may not follow the strain labels because genetical differences are not
fully capturing the behavioral differences. Moreover, determining the best number
of clusters is the key assessing the performance of a clustering model. Notice that
the best number of clusters are neither necessarily equaling to 16 nor the same 
across different clustering methods. Criterion like silhouette scores would be
evaluated to choose the best number of clusters. 



Exploratory Analysis & Classification Models
--------------------------------------------

In 1D, box plots of each feature, say food consumption or sleeping time,
of each strain can be plotted. In 2D, PCA can be preformed on the
feature data set and the data are then plotted along the first and the
second principal axes colored in different strains. These plots are
useful in verifying assumptions. For instance, we could box-plot
different strains of mice against food consumption to see whether
different strains of mice eat distinctly. If the number of variables
needed to be evaluated is large, we might also use five number summaries
to study the distributions.

Example boxplots: 

.. figure:: figure/features_boxplot_by_strain.png 
   :align:   center

   Example boxplots

Since each strain (each class) only has 9 to 12 mice, inputting too many
features to the classification model is unwise. The exploratory data
analysis will be an important step for hypothesis testing and feature
selection. The process will also help us to find outliers and missing
values in each behavioral variable, and we will decide how to handle
those values after encountering that.

Data Requirements Description
-----------------------------

We dispose of a labeled data set of 16 different strains of mice.
Behavioral features are recorded for each mouse and each day. One
example can be the time spent eating or drinking, and the amount
ingested.

The researchers record the daily activities of each mouse, for example
the time it spends eating, drinking, sleeping, and wondering around its
habitats. Therefore, every behavioral features should be averaged to the
same time period (one mouse day) for each mouse. For example, the food
consumed variable at each timestamp will be aggregated to the average
food consumption.

Notice that the final dataset should be a clean and well formatted
dataframe (in numpy array or pandas dataframe) aggregating the features
of mice so that it can be directly used to train classification models.

Besides, the detailed explanation for each variable and strain type
might be needed for further interpretations of models.

Methodology/ Approach Description
---------------------------------

1.Supervised Classification: Supervised classification algorithms
(logistic regression, random forest, KNN) will be used to detect the
relationship between strain of mice and behavioral features. If we gain
good model performance, we can conclude different mouse behaviors
actually indicate different genetic differences. K-fold cross-validation
might be used to tune model parameters, and a proportion of data would
be used as test data to evaluate the model performance. Notice that we
may manually manipulate so that the both the training data and the test
data cover all strains of mice.

The step after model fitting is to assess the important behavioral
features in the classification and clustering models. A smaller set of
feature space containing only top features might be used to gain better
interpretations of the model.

**Unsupervised learning**

Unsupervised learning algorithms, K-means and hierarchical clustering, are included in the subpackage `classification`. Unlike other clustering problems where no ground truth is available, the biological information of the mice allows us to group the 16 strains into 6 larger mouse families, although the ‘distances’ among the families are unknown and may not be comparable at all. Hence, cluster numbers from 2 to 16 should all be tried out to find the optimal. Here, we briefly describe the two algorithms and the usage of the related functions.

Above all, note that unlike the supervised classification problem where we have 11 levels for one feature (so we have up to 99 features in the classification problem), the unsupervised clustering methods could suffer from curse of high dimensionality when we input a large amount of features. In high dimension, every data point is far away from each other, and the useful feature may fail to stand out. Thus we decided to use the average amount of features over a day and the standard deviation of those features for the individual mouse (170 data points) case. 

***K-means***

To begin with, *K-means* minimizes the within-cluster sum of squares to search for the best clusters set. Then the best number of clusters was determined by a compromise between the silhouette score and the interpretability. K-means is computationally inexpensive so we can either do the individual mouse options (170 data points) or use the raw data with 21192 data points where we regard different data points to be different mice.
However, the nature of K-means makes it perform poorly when we have imbalanced clusters. 

***Hierarchical Clustering***

Given the above, the potentially uneven cluster sizes lead us to consider an additional clustering algorithm, *hierarchical clustering*, the functionality of which is included in the subpackage. Generally, hierarchical clustering seeks to build a hierarchy of clusters and falls into two types: agglomerative and divisive. The agglomerative approach has a “richer get richer” behavior and hence is adopted, which works in a bottom-up manner such that each observation starts in its own cluster, and pairs of clusters are merged as one moves up the hierarchy. The merges are determined in a greedy manner in the sense that the merge resulting in the greatest reduction in the total distances is chosen at each step. The results of hierarchical clustering are usually presented in a dendrogram, and thereby one may choose the cutoff to decide the optimal number of clusters.
Below is a demo to fit the clustering algorithm. The loaded data is firstly standardized, and then the optimal distance measure and the optimal linkage method are determined. We have restricted the distance measure to be l1-norm (Manhattan distance), l2-norm (Euclidean distance) and infinity-norm (maximum distance), and the linkage method to be ward linkage, maximum linkage and average linkage. The maximum linkage assigns the maximum distance between any pair of points from two clusters to be the distance between the clusters, while the average linkage assigns the average. The ward linkage uses the Ward variance minimization criterion. Then, the optimal linkage method and distance measure are input to the model fitting function, and the resulting clusters and corresponding silhouette scores are recorded for cluster number determination. A plotting function from the subpackage is also called to output a plot. The output plot is included in the result section of the report.

```python
from mousestyles import data
from mousestyles.classification import clustering
from mousestyles.visualization import plot_clustering

# load data
mouse_data = data.load_all_features()

# rescaled mouse data
mouse_dayavgstd_rsl = clustering.prep_data(
mouse_data, melted=False, std=True, rescale=True)

# get optimal parameters
method, dist = clustering.get_optimal_hc_params(mouse_day=mouse_dayavgstd_rsl)

# fit hc
sils_hc, labels_hc = clustering.fit_hc(
    mouse_day_X=mouse_dayavgstd_rsl[:,2:],
    method=method, dist=dist, num_clusters=range(2,17))

# plot 
plot_clustering.plot_dendrogram(
    mouse_day=mouse_dayavgstd_rsl, method=method, dist=dist)
```

Testing Framework outline
-------------------------

-  The first step to test the reproducibility is to test the stability
   of classification models. Since we randomly split the dataset to be
   the test set and the training set, we can train and test the model
   over different seeds and plot the accuracy against different
   trials. We should also see if the important features are stable over
   different trials.

-  From our limited understanding, the results of this research might
   have a meaningful implication on the way we treat psychological
   disorders. If it turns out that nature does influence these
   disorders, we can probably conclude that psychological disorders is
   not much different than physical disabilities. Otherwise, if nature
   has little influence over these disorders, we can try to find way to
   prevent these disorders from happening.

Result
-------------
**Classification**

**Clustering**
***K-means***

***Hierarchical clustering***

The optimal distance measure is l1-norm and the optimal linkage method is average linkage method. The silhouette scores corresponding to the number of clusters ranging from 2 to 16 are:  0.8525, 0.7548, 0.7503, 0.6695, 0.6796, 0.4536, 0.4557, 0.4574, 0.3997, 0.4057, 0.3893, 0.3959, 0.4075, 0.4088, 0.4179. It seems 6 clusters is a good choice from the silhouette scores. 
However, the clustering dendrogram tells a different story. Below shows the last 10 merges of the hierarchical clustering algorithm. The black dots indicate the earlier merges. The leaf texts are either the mouse id (ranges from 0 to 169) or the number of mice in that leaf. Clearly, we see that almost all the mice are clustered in 2 clusters, very far from the rest individuals. Thus, the hierarchical clustering fails to correctly cluster the mice in the case. 
.. plot:: report/plots/plot_hc_dendrogram.py

   Dendrogram of the hierarchical clustering
The failure of the the algorithm might be due to the different importance levels of the features in determining which cluster a mouse belongs to. One improvement could be that using only the important features determined in the classification algorithms to cluster the mice, but given the unsupervised learning nature of the algorithm, not using the results from the classification is fair for clustering tasks.
The distribution of strains in each cluster in the case of using 6 clusters are shown below. Obviously, the mice almost fall into the same cluster.
.. plot:: report/plots/plot_hc_result.py

   Distribution of strains in clusters by agglomerative hierarchical clustering

Future work
----------------
The future research should focus more on feature engineering, including the questions 
that whether more features could be added to the model. Moreover, an economized subset 
of features should be evaluated to see whether we can reduce the model complexity
without losing too much model accuracy. 
To understand more about the nature of the strain difference, it would be better to 
have a sense of relationships between different strains of mice. For instance, we have 
explored that these 16 strains of mice belong to 7 different groups, which implied that 
some strains were genetically similar. Considering the time limit, we have put it to 
the future work. 

References
----------

