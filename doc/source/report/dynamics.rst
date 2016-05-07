.. _dynamics:

Dynamics of AS Patterns
=======================

Statement of Problem
--------------------

The objective of Dynamics Analysis is to analyze and characterize the behaviors of different strains of mice using Markov Chain model. We could use the MC models to further explore the discrepancy between different strains and even simulate a particular mouse day for a particular strain.

Statement of Statistical Problems
---------------------------------

The statistical problems in this project are mainly naturally divided into two parts, the modeling part and the simluation of the model part. The modelling part consists of estimating the probability of events transition using the raw data of mouse's spatial and temporal data, and once we've got the model, we could use this model to do predictions and simulate a fake mouse day.

For the estimation, the statistical problems include:

    - Define the states of interest.
    - Estimate the transition probability matrix given the data we have
    - Expand the capacity of our model to take into account the effect of time in our estimation. We want our model to be time-dependent (non-homogeneous) and could also model some of the time series structure of the behaviors of the mice during one typical mouse day

Data Requirements Description
-----------------------------

-  We need labels of states of interest with respect to the time intervals in a specific mouse day to extract the structure of the Markov Chain.

Methodology/ Approach Description
---------------------------------

1. Defining states of interest: which behaviors of the mouse are we interested in? 

   - Feeding: labeled by event F
   - Drinking: labeled by event W
   - Other active state behaviors: This could possibly include all other movements in the AS state of a mouse besides drinking and eating.
   - Inactive State: labeled by event I.


2. Data Preprocessing: convert the data we had into strings of the events chosen. This could be done by checking out the states of a typical mouse day at a lot of equally spaced time points and store the states and the time points in the same order. In order to perform this task, we need basically do the following two steps:

   -  Data cleaning: Clean the raw intervals given by the measurements in the experiment into interval data that makes more sense and consistent. Also need to check if any of our states overlapped.
   -  Data reformating: Convert the cleaned interval data into strings of events or matrices containing both information from timestamps and the events at those timepoints.

3. Estimating Transition Probability: Estimate the transition probability matrix of the Markov Chain using the data given. One of the key challenges to estimate the transition matrix is that our model is actually time continuous non-homogeneous Markov Chain, and the parameters are too difficult to estimate given the data we have. Instead, we figured out a way to make our model a composite of small homogeneous discrete time Markov Chains, so that we could perform a rough estimation of the original time continuous non-homogeneous Markov Chain. We followed the following steps to achieve our goal:

   - Divide each mouse day into small time intervals, say 5 minutes
   - For each of the small time intervals, aggregate the data from all mouses in the same strain for all mouse days and estimate the transition probability matrix of a discrete homogeneous Markov Chain model just for this small time interval.
     - each of these transition probability matrices is estimated by MLE method, where e.g.: 
     .. math:: P(F_{t+1} | W_{t}) = \frac{N_{WF}}{N_{W.}}
     where ..math::N_{WF} indicates the counts of transitions from W to F and ..math::N_{W.} indicates the counts of transitions starting from W, no matter where it ends.
   - Build the whole model by compositing the models for each small time intervals.

4. Simluation: Use previous estimated model to simluate a typical mouse day for a typical strain. This part could also be used to evaluate the length of the time interval chosen in the previous step.

Remarks:
--------
Testing for each function should be done by the person who wrote the function.

References:
-----------

http://scikit-learn.sourceforge.net/stable/modules/hmm.html

https://github.com/hmmlearn/hmmlearn

https://en.wikipedia.org/wiki/Hidden\_Markov\_model


Project Details:
----------------

- Data Preprocessing: Hongfei
- Modeling: Jianglong
- Simlation: Chenyu
- Evaluation of length of small time interval chosen: Weiyan, Lynn, Mingyung
- Final Report writeup: Weiyan, Lynn, Mingyung
