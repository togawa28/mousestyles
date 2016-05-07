Overview
========

1. Statement of Problem
-----------------------

For this project, our primary data source is mouse behavioral data from the
Tecott Lab at UCSF. [#f1]_ The lab has recently developed a method for
continuous high-resolution behavioral data collection and analysis, which
enables them to observe and study the structure of spontaneous patterns of
behavior ("Lifestyles") in the mouse
:cite:`tecott2003genes,tecott2004neurobehavioral,goulding2008robust,anderson2014toward`.
They have found that using this method: 1) reveals a set of fundamental
principles of behavioral organization that have not been previously reported,
2) permits classification by genotype with unprecedented accuracy, and 3)
enables fine dissection of behavioral patterns.

1.1 Project Goal
~~~~~~~~~~~~~~~~

The goal of this project is to explore the effects of genetics on
behavior in mice and extrapolate these findings to improve treatment of
psychiatric diseases in humans.

1.2 Computational Ethology
~~~~~~~~~~~~~~~~~~~~~~~~~~

`Ethology` is the study of animal behavior, and it
generally follows one of two approaches. The first approach was
developed by B.F. Skinner and relies heavily on laboratory experiments.
Skinner postulated that since behavior is predictable, it should be
controllable. His most prominent experiment involved training pigeons
through `operant conditioning`. He found that
the pigeons had the ability to learn new behaviors under a reward
system. However, the setting of the experiment was incredibly artificial
and controlled. In contrast, Konrad Lorenz believed that the only way to
truly understand animal behavior is to observe them in their natural
context as behavior induced by an artificial environment may not reflect
animal behavior in their natural environment. Lorenz's most prominent
experiment discovered that a young goose will instinctively bond with
the first moving object that it perceives in order to better recognize
its own species. This experiment was conducted in a more natural setting
to minimize human manipulation.

This project adopts Lorenz's approach---observing the whole spectrum of
animal behavior in their natural state. Previous approaches relied on
human observation to score animal behavior. However, slow data
collection, low dimensional data, imprecise and subjective measurements,
and human visual and language limitations impeded data collection and
analysis. Using modern quantitative tools for measurement, description,
and analysis, the field of `computational
ethology` has emerged to solve these
issues. Together, modern mathematics, engineering, and computer science
have the potential to establish a causal relationship between genetics
and behavior.

1.3 Why Mice?
~~~~~~~~~~~~~

Although the human genome was first sequenced over a decade ago, the
relationship between genetics and behavior is still not well understood.
For ethical reasons, genes cannot be systematically manipulated in
humans. Therefore, the familiar scientific testing approach must be
edited---enter mice. There are several reasons the mouse has become the
mammal of choice in human behavioral studies. Chief among them is the
fact that "approximately 99% of mouse genes have human
counterparts---conversely, mouse versions (orthologs) can be identified
for 99% of human genes." Additionally, the brain organization and
behavioral responses of humans and mice display many similarities. For
example, both mammals display complex processes like hunger and fear.
This allows scientists to more easily identify and track these
behaviors. In addition, the extreme similarities of intra-strain mice,
the space efficiency of maintaining their caged environments, and the
speed of reproduction make mice a logical alternative to testing on
humans.

2. Methodology Description
--------------------------

The traditional technology to analyze behavior is time-intensive and
labor-intensive. For example, recording data requires researchers to
track behavior uninterruptedly. This experiment utilized a method for
continuous high-resolution behavioral data collection and analysis. The
`home cage monitoring (HCM) system` utilized is a
network of photobeam feeding detection, drinking detection, and activity
platform sensors that records mouse `active states`
and `inactive states` automatically and incessantly
over 24-hour periods where 1 hour per day was reserved for HCM
maintenance. This facilitates objective, multi-dimensional computer
tracking, providing a higher degree of accuracy compared to human
observation.

In this project, the HCM system tracked 170 mice, representing 16
`strains` or approximately 94% of the genome, logging
500,000 behavioral events per mouse per day over 12 days of data
collection after 5 days of acclimation. The scope of the study was
limited to male mice as females tended to display cyclical changes in
behavior. Mice within each strain display strong homogeneity and low
variability in genetic composition. This is in part due to high levels
of inbreeding which decreases the randomness between individual mouse
samples. By studying the behaviors of theses 16 different strains --
each strain with their own unique genetic makeup -- we can begin to
understand the importance of genetic makeup on mice behavior. We can
then extrapolate to humans thanks to the remarkable genetic similarity
between the two species.

3. Statement of Statistical Problems
------------------------------------

This project utilized sophisticated statistical methods to process data,
including machine learning algorithms and statistical inference. The
whole project can be divided into 6 sub-projects:

-  :ref:`behavior`
-  :ref:`path`
-  :ref:`dynamics`
-  :ref:`ultradian`
-  :ref:`classification`
-  :ref:`distribution`

4. Glossary
-----------

-  **Active State (AS):** The active state in this model is when the
   mouse is using energy, such as foraging, patrolling, eating, or
   drinking. Active states are energetically costly and can be dangerous
   in a natural environment.
-  **Computational Ethology:** The use of mathematics, engineering, and
   computer science to overcome the difficulties that come from using
   humans to score animal behavior.
-  **Ethology:** The study of animal behavior, including the
   phenomenological, causal, genetic, and evolutionary aspects.
-  **HCM System:** The system used in this experiment to track variables
   of interest. The HCM System included photobeam sensors at the feeding
   stations, capacity based sensors at the drinking station, and an
   activity platform for position detection using an (x,y) system.
-  **Home Environment:** The home environment is the cage of each mouse
   containing a home base, a food station, and a water station.
-  **Inactive State (IS):** The inactive state in this model is when the
   mouse is in a state of energy conservation, such as sleeping or
   resting at the home base.
-  **Operant Conditioning:** Altering of behavior through the use of
   positive reinforcement which is given to the subject after eliciting
   a desired response.
-  **Phenotype:** The set of observable characteristics of an individual
   resulting from the interaction of its genotype with the home
   environment.
-  **Strain:** A strain here is a genetic variant or sub-type of of the
   more general mouse population.

5. Data 
-------

The data includes two directories, intervals and txy_coords, and a npy file named all_features_mousedays_11bins. The all_features_mousedays_11bins.npy
contains a 9*1921*11 matrix, which represents 9 features among 1921 mouse days in 11 2 hour bins for a day, the 9 features are:

-  **Food (F):** records the food consumption (g) for a certain mouse day and a certain time bin.
-  **Water (W):** records the water consumption (g) for a certain mouse day and a certain time bin.
-  **Distance (D):** records the movement distance for a certain mouse day and a certain time bin.
-  **ASProbability (ASP):** records the AS time proportion in the certain time bin.
-  **ASNumbers (ASN):** records the numbers of AS in the certain time bin. 
-  **ASDurations (ASD):** records the total duration of AS in a certain bin.
-  **ASFoodIntensity (ASFI):** equals F/ASP.
-  **ASWaterIntensity (ASWI):** equals W/ASP. 
-  **MoveASIntensity (ASMI):** equals D/ASP.

The intervals directory has 6 sub-directories, all sub-directories have about 33 files for 3 strains, and for each strain there are 11 days data:

-  **F:** records start and stop time of eating behaviors for a certain strain and a certain day. 
-  **W:** records start and stop time of drinking behaviors for a certain strain and a certain day.
-  **AS:** records start and stop time of AS for a certain strain and a certain day.
-  **M_AS:** records start and stop time of movements in AS for a certain strain and a certain day.
-  **IS:** records start and stop time of IS for a certain strain and a certain day.
-  **M_IS:** records start and stop time of movements in IS for a certain strain and a certain day.

The txy_coords directory has 5 sub-directories,all sub-directories have about 33 files for 3 strains, and for each strain there are 11 days data:

-  **CY,CX,CY:** records the position (x,y) in time t for a certain strain and a certain day.
-  **C_idx_HB:** indicates whether the mouse is in HB or not at time t.
-  **recordingStartTimeEndTime:** records the start and stop time of tracking (x,y,t) for a certain strain and a certain day.

.. rubric:: Footnotes

.. [#f1] http://www.neuroscience.ucsf.edu/neurograd/faculty/tecott.html
