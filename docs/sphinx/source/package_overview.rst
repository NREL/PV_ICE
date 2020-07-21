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
