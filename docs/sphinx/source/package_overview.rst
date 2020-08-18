.. _package_overview:

Package Overview
================

The calculator considers the following material flow:

.. image:: ../../images_wiki/MFC-Diagram.PNG
  :width: 450

The starting point is the installed capacity. From there, the percentage of probability of each arrow determines the amount of material on each stage. For example, if 20% gets Recycled, that means the other 80% goes to landfill.

Input to the calculator is an excel file with the appropriate columns to establish all the paths in the diagram. Examples for baseline input files for the US and World past and projected values are available in the CEMFC/baselines folder.

For contrast, a completely linear economy would look like:

.. image:: ../../images_wiki/Linear-Economy.PNG
  :width: 400


Framework and Definitions
----------------------------


Weibull CDF / PDF
-------------------
Weibull distributions are often used in product reliability to capture lifetime and failure occurrences. We are controlling our weibull curve parameters by using the T50 and T90 values, which represent the time at which 50% and 90% of the cohort has failed, respectively. For PV panels that are expected to last past their 30 year warranty, T50 and T90 must be bigger than 30, for example T50=35 years and T90=40 years. See the Weibull section for more details.
