.. _path:

Exploration & Path Diversity
============================

Statement of Problem
--------------------

The movements of mice are theorized to be correlated with physical, neural,
and environmental attributes associated with mice such as strain, health,
time-of-day, and day-of-week. The aim of this subproject was to discover
whether or not mouse locomotion patterns are unique to each strain. To achieve
this objective, we studied the paths the mice took throughout the days of the
experiment. This involved engineering path features such as length, speed,
acceleration, and angle, followed by incorporating visualization techniques to
discover previously hidden patterns.

.. plot:: plots/heat_map_0_0_0.py

   A heatmap of a mouse movement.

Statement of Statistical Problems
---------------------------------

As stated previously, this subproject attempted to discover differences in
path patterns that were unique to each mouse strain and each mouse within a
strain. The major statistical problem associated with this project was to
collapse the data in such a way as to increase our understanding of physical
and psychological behavior through visualization of mouse paths. With the
Tecott lab's visualization graphics as a launching point, we continued on to
create features that could be adapted to their plots and also generated new
plotting methods to find the optimal method of expression. These features
might prove useful in the classification subproject and potentially help us
understand the relationship between behavior and genetics in mice and humans.

Exploratory Analysis
--------------------

The initial exploratory data analysis focused on how to define a path, how to
generate metrics from the data, and how to visualize paths at different points
in the day. Based on advice from the Tecott lab and our initial data
exploration, we separated paths by interruptions in movement that were more
than one second long. The path metrics we chose to include were length, speed,
acceleration, angles, radius, center angles, area covered, area of the
rectangle that contains the path, and absolute distance between the first and
last points of a path. With the results of these features, we hoped to gain a
better understanding of the more granular differences in paths between strains
than with just visualization alone. Having considered these questions, we also
realized the need for data cleaning functions to filter out any noise from the
data.

.. plot:: report/plots/plot_path.py

   Example of path plot.


Data Requirements
-----------------

The data required to perform our analysis included the ``<x, y, t>``
coordinates for the mice as well as a boolean indicating whether the mouse
was situated in its home base. Additionally, we required the daily coordinates
of the home base for each mouse.

.. figure:: figure/mice_path.png
   :alt: alt tag

   Path (image courtesy of Tecott Lab)

Methodology/Approach Description
--------------------------------

**Step 1** : Define “Path”

We define a path based on a specific time threshold between movements. In more
detail, we created a function that considers that time difference. If the time
between movements exceeded the threshold, we considered a new path to have
begun. That path was considered to have ended once the threshold had been
exceeded again. Based on the advice of the Tecott lab, the default threshold
was one second.

**Step 2**: Clean Data

Based on our definition of a path, we realized that we needed to clean the
data to remove obvious outliers and noise. For instance, we found that the
sensor platform generated extreme outliers such as an acceleration of -4000
centimeters per second. In order to remove this noise, we created two
functions: one to filter the paths and one to remove duplicate rows. The
filter paths function uses a minimum number of points in a path to filter out
paths that create noise. For example, a path that is only three points could
simply be a mouse shifting weight from one foot to the other and back again.
Since this is not the type of path we are interested in analyzing, it makes
sense to filter them out. The remove duplicates function deals with an issue
in the data where the same x and y coordinates appear in adjacent rows but
with different timestamps. This caused a problem when computing the angles of
the paths so, while it is a trivial removal, it is necessary.

**Step 3**: Choose Key Features

The path features we wrapped up into functions are as follows:
    - Path Length: Total distance covered
    - Path Speed: Average speed
    - Acceleration: Ratio of speed to the time difference at each point
    - Angles: Angle between adjacent vectors
    - Radius of Path: Distance between the center point and every other point
    - Center Angles: Angle created by two adjacent radius vectors
    - Area Covered: Area covered by the path, computed with center angle and
      radii
    - Area of Rectangle: Area of rectangle that contains the entire path
    - Absolute Distance: Distance between the first and last points

**Step 4**:  Interpretation

Below are the plots generated based on the features we calculated above, per
strain, mouse, and day. With these plots, we can draw some initial conclusions
about differences between strains in the results section.

Results
-------------------------

.. figure:: figure/dist_path.png
   :alt: alt tag

.. figure:: figure/dist_speed.png
   :alt: alt tag

.. figure:: figure/dist_acceleration.png
   :alt: alt tag

.. figure:: figure/dist_angle.png
   :alt: alt tag

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
