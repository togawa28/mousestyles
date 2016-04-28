.. _path:

Exploration & Path Diversity
============================

Statement of Problem
--------------------

The background of this problem is that the movements of each mouse, defined by
"path",should be affected by some other relevant quantity including strain,
time-of-day, day-of-week, physical status, or neural psychological attributes.
These important relationships enable us to use the movement of mice to
implement statistical analysis including prediction or classification.
Generally speaking, our aim in this subproject is to use mouse locomotion
patterns to make inference about the mouse’s daily behavior. This behavior
involves how many times did the mouse eat in that day and how long did it eat.
As we think that mice locomotion patterns are fundamental aspects of behavior,
we will expect that these are good features of strains.

.. plot:: report/plots/heat_map_0_0_0.py

   A heatmap of a mouse movement.

Statement of Statistical Problems
---------------------------------

Our statistical problems are essentially classified into 2 categories;
the definition of path and statistical inference. How to define the path
should depend on what we want to do by these paths since the concept of
path could be very broad and obscure. If we employ classification in our
analysis, we need to discretize the continuous paths. Also we might be
able to quantify the paths itself by introducing some 'scores' of each
path, which is supposed to be a representative summary of the whole path
(e.g. "efficiency score" or “exploration score.” Details are in the
following sections). Classification could be certainly one of our
statistical interests. We are primarily interested in the link between
the spatial habits and strain, so for example we can use the following as
the response variable for classification:

-  Path: given the strain and certain key attributes about the mice (ex:
   time of day, time of last meal, aggregate distance traveled, etc.),
   we want to be able to predict the future movement or “path” of the
   mice. It may be possible to identify types of commonly traveled paths
   (ex: path towards food, path towards water, exploratory path, etc.)
   and use these for prediction. 
-  Strain: By using the path patterns as one of key features to predict
   strain, we can reveal the important relationship between those.

Ideally the results of those classification should be interpretable to us.
That is, for example, the results would show that mice strains which are
heavier tend to travel less frequently and less distance throughout the day.

Exploratory Analysis
--------------------

As we begin our analysis, we would like to explore the following points:

- Daily plots of densities for each strain of mice to distinguish
  locomotive patterns amongst strains and to get a sense of day-to-day
  variations in mouse locomotive behavior or possibly detect anomalies. We
  can measure the ‘distance’ between two densities by the KL divergence in
  probability.
- Summary statistics of locomotive patterns for each strain. This includes
  total distance traveled per set intervals (daily, hourly, etc.)
- How different strains allocate their time on each path.
- The impact of changing the grid size (note: the authors have used 1 cm).
- Identify paths that are structurally similar by exploiting rotational
  invariance

Data Requirements
-----------------

We would require the ``<x, y, t>`` coordinates for the mice. We require
active states ("AS") and inactive states ("IAS") to be clearly defined
and possibly flagged within the dataset. Additionally, we require
behavioral attributes about the mice to be defined and flagged (ex:
eating event, drinking event, etc.)

.. figure:: figure/mice_path.png
   :alt: alt tag

   Path (image courtesy of Tecott Lab)

As we define the path, we will also need to consider how each path will be
labeled. One possibility is to assign a number to each grid square and to
define the path as a sequence of numbers. As an alternative, we can use binary
classification to indicate if the mouse traveled on a particular grid square,
resulting in a matrix of 0s and 1s.  

Methodology/Approach Description
--------------------------------

**Step 1** : Define “Path”

Definition of path should clearly answer the following questions: -
Whether we use raw paths or chunk those into a grid. If we want treat
paths as discrete patterns, we need to set appropriate grid size so that
the paths are not too chunky or too jittery categorical variables. What
is the good measurement here? Which criteria will we follow e.g.
stability? - Functions possibly needed in this step: - Obtain\_grid:
creates grid information based on input of grid size - Chunk\_path:
chunks paths into a grid by the outputs of Obtain\_grid - Eval\_chunk:
evaluate chunked paths by certain measurement - Whether or not we use
time dimension. If yes, how to distinguish a stop or a progression in a
path? And how to consider speeds of each path? - Functions possibly
needed in this step: - Take\_timediff: takes time difference b/w
neighboring timestamps - Eval\_stops: distinguish a stop or a
progression - Obtain\_speed: calculates the speed in each path - How to
cut out paths from location data? Should it be divided by equal time
length? Or should it start from a certain point e.g. nest? - Functions
possibly needed in this step: - Cut\_paths: cuts out paths into several
smaller paths - Possibility of defining “score” of a path to summarize
it. For example, if one mouse goes to food directly and back to the nest
immediately, we can evaluate this path as “very efficient,” in a sense
that he is very efficient in getting a food. Also it is possible to
define an “exploration score” which takes a high value if a mouse goes
every part of the cage before going back to the nest. - Functions
possibly needed in this step: - Cut\_paths: cuts out paths into several
smaller paths

**Step 2**: Choose Key Features

The examples of the key features would include the following: - The
stain of the mouse - The time of day - Some pre-defined “score” of a
path e.g. efficiency - How frequently a mouse visits/stays at a location
- How long it stays at a specific location (ex: nest or food) - The last
time the mouse ate - The last time the mouse drank water - The total
distance on average a mouse travels per day - How fast on average a
mouse travels

We need to construct the functions to generate those features.

**Step 3**: Classification: Machine Learning Technique

We might be able to use several machine learning methods, including
random forest, SVM, gradient boosting. Each method should have following
steps: - Cross validation: divide the data into train, validation, and
test set - Tune the parameters: Based on the train and validation set,
tune the parameter to maximize some pre-defined measurement. - Fit on
the test set: Evaluate the performance of the classification on the test
set.

**Step 4**: Interpretation

Hopefully we might employ the different model like logistic regression
to get a sense of the effect size of each features on the response
variables.

Testing Framework Outline
-------------------------

-  Run simulations of machine learning algorithm with a set seed to
   ensure reproducibility
-  Correct warning message or error message.
-  Develop tests for python functions in methodology section above

Additional Remarks
------------------

We note that the locomotive observations of the mice are recorded at
unevenly spaced intervals (i.e., delta-t varies from point to point).
Based on exploration of the data, we assume that observations are
recorded whenever the mouse is in motion, and during large delta-t
intervals, we assume the mouse is stationary. This is an important point
we would like to confirm and understand before moving forward with the
analysis.

According to the authors, a mice 'movement event' was measured as
numbered in the tens of thousands per day. Each event was described by a
location and time stamp when the distance from the prior recorded
location exceeded 1 cm. Despite this, we note an instance in the data
where the coordinates from (t) to (t+1) did not change, but resulted in
a new observation.

Reference reading:
------------------

-  Spatial memory: the part of memory that is responsible for recording
   information about one's environment and its spatial orientation
-  `Wikipedia <https://en.wikipedia.org/wiki/Spatial_memory>`__
-  `Mouse Cognition-Related Behavior in the Open-Field: Emergence of
   Places of
   Attraction <http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000027#s1>`__
