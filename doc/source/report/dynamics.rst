.. _dynamics:

Dynamics of AS Patterns
=======================

Introduction
------------

The objective of Dynamics Analysis is to analyze and characterize the state transforming behaviors of different strains of mice. The analysis is mainly focused on the three strains of mice included in the interval dataset. Using Markov Chain Model, a sequence of state transition probability matrix is retrieved for each strain depends on the time intervals and a simulation mouse is generated based on the model. A evaluation system is created for comparing the behaviors of two certain mice, and based on which the optimal time interval is choosen so as to have the most realistic simulation mice.Further visualizatoin on those fake mice is done to explore the discrepancy between different strains's behaviors. 

Data Source
-----------


Methodology
-----------

1. Defining states of interest:

   - Feeding: labeled by event F
   - Drinking: labeled by event W
   - Other active state behaviors: This could possibly include all other movements in the AS state of a mouse besides drinking and eating.
   - Inactive State: labeled by event I.


2. Data Preprocessing: 

convert the data we had into strings of the events chosen. This could be done by checking out the states of a typical mouse day at a lot of equally spaced time points and store the states and the time points in the same order. In order to perform this task, we need basically do the following two steps:

   -  Data cleaning: Clean the raw intervals given by the measurements in the experiment into interval data that makes more sense and consistent. Also need to check if any of our states overlapped.
   -  Data reformating: Convert the cleaned interval data into strings of events or matrices containing both information from timestamps and the events at those timepoints.

3. Estimating Transition Probability: 

Estimate the transition probability matrix of the Markov Chain using the data given. One of the key challenges to estimate the transition matrix is that the model used is actually time continuous non-homogeneous Markov Chain, and the parameters are too difficult to estimate given the current data. Therefore, a new way is discovered to make the model a composite of small homogeneous discrete time Markov Chains, so that performing a rough estimation of the original time continuous non-homogeneous Markov Chain is possible. The following steps are followed to get the transistion probability matrix: 

   - Divide each mouse day into small time intervals, say 5 minutes. (The time interval is optimized in the future analysis)
   - For each of the small time intervals, aggregate the data from all mouses in the same strain for all mouse days and estimate the transition probability matrix of a discrete homogeneous Markov Chain model just for this small time interval.
     - each of these transition probability matrices is estimated by MLE method, where e.g.: 
     .. math:: P(F_{t+1} | W_{t}) = \frac{N_{WF}}{N_{W.}}
     where ..math::N_{WF} indicates the counts of transitions from W to F and ..math::N_{W.} indicates the counts of transitions starting from W, no matter where it ends.
   - Build the whole model by compositing the models for each small time intervals. 

```python
strain_df = data_df[data_df.strain == 2]
get_prob_matrix_list(time_df=strain_df,interval_length=1000)
# [array([[ 1.,  0.,  0.,  0.],
        [ 0.,  0.,  0.,  0.],
        [ 0.,  0.,  0.,  0.],
        [ 0.,  0.,  0.,  0.]]),
# array([[  9.99854291e-01,   0.00000000e+00,   4.85696246e-05,
           9.71392491e-05],
        [  0.00000000e+00,   9.10714286e-01,   0.00000000e+00,
           8.92857143e-02],
        [  0.00000000e+00,   0.00000000e+00,   5.00000000e-01,
           5.00000000e-01],
        [  0.00000000e+00,   1.64835165e-02,   0.00000000e+00,
           9.83516484e-01]]),
  ...
  ...

```

4. Simluation: 

Use the Transition Model generated to simluate a typical mouse day for a typical strain. The simulation is time sensitive which means the simulation mouse is generated depend on the time interval chosen in the transition model. The time interval length is optimized in the future analysis so as the generate the best fake mouse for each strain. 

```python
trans_matrix = get_prob_matrix_list(time_df=strain_df,interval_length=1000)
mcmc_simulation(trans_matrix, n_per_int=1000)
# array([0, 0, 0, ..., 0, 0, 0])
```

5. Evaluation System:


Result
------

The problem we are insteresting in here is whether the three strains of mice are indeed acting differently in a time series manner. The behaviors are compared using the three simulation mice, each for one strain. Therefore, as the first step, the optimal time interval is selected so as to have the most-real simulation mouse that behaves the most similarly to its strain, which is evaluated using the score system we created. As a result, the best time interval length is selected for each strain as well as the corresponding simulation mice behavior and the comparison score.

```python
# data_df: 
find_best_interval(data_df,strain=0)
# (600, array([0, 0, 0, ..., 0, 0, 0]), 0.70509736459572225)
find_best_interval(data_df,strain=1)
# (600, array([0, 0, 0, ..., 0, 0, 0]), 0.91423472578532516)
find_best_interval(data_df,strain=2)
# (1800, array([0, 0, 0, ..., 0, 0, 0]), 0.83975976073161329)
```

As the scipt suggested, the best time interval selected is 600 seconds for the first strain which generates the simultation mouse that has 71% similarity compared to the real mice in that strain, and the simulation behavior is quoted in the numpy array format. Similarly, it shows the 600s optimal time interval with 91% similarity for the second strain and the 1800s optimal time interval with 84% similarity for the third strain. 

With the resulting best simulation mice, we move forward to compare the between-strain behaviors using visulization.

Discussion
-----------


References Reading
-------------------

http://scikit-learn.sourceforge.net/stable/modules/hmm.html

https://github.com/hmmlearn/hmmlearn

https://en.wikipedia.org/wiki/Hidden\_Markov\_model


Contribution
------------

- Data Preprocessing: Hongfei
- Modeling: Jianglong
- Simlation: Chenyu
- Score: Weiyan
- Evaluation: Luyun Zhao
- Comparison: Mingyung
