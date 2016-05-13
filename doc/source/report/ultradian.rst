.. _ultradian:

Ultradian and Circadian Analysis
================================

Statement of problem
--------------------

Ultradian and circadian rhythm are widely observed in mammalian
behavioral patterns. The ultradian analysis aims to
find the time-specific patterns in behavioral
records, without specifying the length of the cycle in advance (but need to be
within 1 hour to 1 day). The typical ultradian period includes 8 and 12 hours.
The circadian rhythm refers to a roughly 24-hour cycle.
For example, we expect the rats to be inactive in the nighttime.
And ingestions and movements mostly happened in the daytime.

The variables of interests are the summary statistics of mouse activity
including food (F) and water (W) ingestion, distance traveled (D), Active
State probability (AS), movement inside the home base (M_IS) and
movement outside the home base (M_AS). We may also consider spatial variables,
for example, to spatially discrete the data to cells each with its primary
functions such as food cell, water cell, and examine
ultradian cycle of the spatial probability densities
of the occupancy time in each cell.

In this report, we assume strain to be the primary influence on the variation of
ultradian rhythms across individual mouse and examine the
difference in rhythms across strains. Currently, we lack
basic information such as weight, age, and gender. With more data available
in the future, we may look into the cycle for each mouse and detect the most
important factors influencing the ultradian rhythms.

The ultradian and circadian analysis is closely related to other subprojects.
Ultradian rhythms could be treated as one feature for clustering the 16
strains. We may also subset the data using the results of the cluster and
analysis the rhythm similarities and differences across clusters.

Statement of statistical problem
--------------------------------

Our statistical problems are three parts: data preparation, choice of
the frequency or period, and modeling of rhythm patterns.

- Data preparation: mouse behaviour are recorded based on time intervals
  or time points. For example, the beginning and ending time
  stamp of one food ingestion, or the coordinates of mouse
  position at a specific time point. We aggregate the
  data based on given time bins and thus convert the raw data to time series.
  Then how to determine the optimal bin intervals for
  constructing the time series? Bin interval examples includes
  5 min, 30 min, 1 hour etc.

- Choice of the frequency or period: For ultradian rhythms,
  significant period length may vary according to the
  variables of interests. The Lomb-Scargle (LS) periodogram spectral
  analysis technique, a widely used tool in
  period detection and frequency analysis, is applied.

- Modeling of rhythm patterns:

Data Requirements
-----------------

Input: records for each strains (total of 16), each feature of interest (food,
water, distance, active\_state probability, ...), in a duration of 12 days
(excluding 4 acclimation days).

Processed: using one-minute time bins of movement records to binary score the
activity into 0 (IS: inactive state) and 1 (AS: active state); using
thirty-minute bins of food records to calculate the amount of chows consumed by
mice; using LS periodogram technique to select the appropriate time bins for
above.

Output: different patterned visualization for each feature, with the
appropriate time bins that presents the most significant ultradian pattern.

Exploratory Analysis
--------------------

Methodology/Approach Description
--------------------------------
**********************
Seasonal decomposition
**********************


Seasonal decomposition is a very common method used in
time series analysis. One of the main objectives for a decomposition is to
estimate seasonal effects that can be used to create and present seasonally
adjusted values.

Two basic structures are commonly used::

    1. Additive:  x_t = Trend + Seasonal + Random

    2. Multiplicative:  x_t= Trend * Seasonal * Random

The "Random" term is often called "Irregular" in software for decompositions.

Basic steps::

    1. Estimate the trend

    2. "De-trend" the data

    3. Estimate seasonal factors by using the "de-trended" series

    4. Determine the "random" term

.. plot:: report/plots/plot_24H_seasonal_AS.py

   Seasonal variation of AS probability (circadian).

**************************
Longitudinal data analysis
**************************

Description
^^^^^^^^^^^
-  Attempts for mixed models

   The mixed model is frequently used for longitudinal analysis. We should specify the random effects and fixed effects first. Since it is ultradian analysis so we only need to focus on the hour factor and their cycle which we can get from the previous LS test. The random effect is the mouse id. Basically we have 4 different mouses in one strain and we only want to compare the different pattern among these three strains. So if we set the random effect to be mouse id, the effects from different mouses will be cancelled off and we can also test the significance of these effects. The response variable will be one of the six features listed before. After that we can use the mixed model to get the pattern of the movements in different time period.

- Build the model

  Take `Food` feature as an example, and here strain0 means a dummy variable indicates whether the mouse belongs to strain 0 or not. Also  strain1 means a dummy variable indicates whether the mouse belongs to strain 1 or not. The interaction terms means strain0*hour, strain1*hour. We add this because we want to figure out whether the strain and hour have some interaction effect in Food feature. (`i denote ith strain, j denote the jth mouse`)

.. math::

  Food_{ij} = f(strain0_{ij} , strain1_{ij} , hour_{ij} , cycle_{ij}) + interactions + \beta_j mouse

- Perform significance test

  Here we have two purposes, firstly we want to figure out if the effects from different mouses are significant. Secondly we want to figure out if the patterns for different strains are significantly different. To test the first one, we just need to use the t test and get the p value from the result by using the `statsmodels.formula.api` package. For the second one, we can perform the likelihood ratio test on the interaction terms.

Result
^^^^^^
Firstly the summary of the full model result is below:(also take the Food feature as an example)


============  =================  ===========  ========  ======
factors       Coef.              Std.Err.       z       P>|z|
============  =================  ===========  ========  ======
Intercept     -1311245600.366    2868292.58   -457.152  0.000
hour                   -0.005    0.000        -11.649   0.000
strain0           5990116.561    3103.119     457.152   0.000
strain1           3491829.461    7638.225     457.152   0.000
cycle           109224897.792    238924.702   457.152   0.000
strain0:hour            0.002    0.001        4.294     0.000
strain1:hour           -0.003    0.001        -4.526    0.000
RE                      0.016
============  =================  ===========  ========  ======

We can see that the effects of the mouse from the same strain is not significant. Also we did likelihood ratio test and found that the p values for 6 features below:

=======  ========  ========  =======  ========  ========
Water    Food      AS        M_AS     M_IS      Distance
=======  ========  ========  =======  ========  ========
3.08e-9  1.40e-12  9.39e-12  5.11e-5  0.002     1.53e-8
=======  ========  ========  =======  ========  ========

We can see that the Water, Food, AS, M_AS, Distance have significantly different patterns for different strains.

Testing Framework Outline
-------------------------

Step 1: Generating random samples for testing:

- Split the data based on the Mouse Day Cycle
- Number the splits and use numpy.random to subset from these splits

Step 2: Conduct Lomb-Scargle (LS) test to detect the period. Implement the
three different models onto the certain period and get the patterns/ estimated
coefficients for the model.

Step 3: Compare the result with our hypothesis.

Reference
---------

-  Lloyd, David, and Ernest L. Rossi, eds. Ultradian rhythms in life
   processes: An inquiry into fundamental principles of chronobiology
   and psychobiology. Springer Science & Business Media, 2012.
-  Stephenson, Richard, et al. "Sleep-Wake Behavior in the Rat Ultradian
   Rhythms in a Light-Dark Cycle and Continuous Bright Light." Journal
   of biological rhythms 27.6 (2012): 490-501.

Appendix
--------

.. plot:: report/plots/plot_24H_seasonal_features.py

   Seasonal variation of other features (circadian).

.. plot:: report/plots/plot_LS.py

   LS plot.
