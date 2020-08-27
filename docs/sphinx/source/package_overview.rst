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
PV Life Stages/Phases:
We are setting the boundaries of the PV Life stages at mining/extraction and processing of the virgin materials, which are all represented as a single stage ("Extraction and Material Prep"). Subsequent stages are 
"Manufacturing", where the processed materials are made into a module; 
"Lifetime/UsePhase"; where the module is installed and used to generate electricity; and 
"End of Life" (EOL), where the module has either failed or degraded beyond use. The "R's" modify the linear life stages of a PV module.

EOL
~~~~~
Modules reach End of Life in one of two forms: Failure and Degradation. Both functions are applied to each annual cohort of modules such that each year in the model produces modules that enter the End of Life Pathway Options.

Failure
^^^^^^^^^
Failure is a random occurrence where the module stops working on site at any point after installation. It follows a probabilistic distribution (usually Weibull in reliability, as defined by T50 and T90 values in years). Early loss of modules are due to manufacturing defects, low quality components, or installation errors and usually represent a higher amount of failures in the first 4 years of deployment. Failure probability also increases as the modules get near their end of lifetime. Failure has the potential for "Repair".

Degradation
^^^^^^^^^^^^^
The other mechanism of reaching EOL is Degradation. Modules are expected to last on the field for their working lifetime/warranty, and they degrade from their nameplate capacity each year, producing less power. Once the nameplate capacity is reduced below the warranty and/or the project lifetime is complete (whichever comes first) then modules are deemed to be at EOL. Owners might choose to keep the plant going for the merchant tail benefits, or to resell or use the modules in other capacity. These options are captured through the "Reuse" circular economy pathway.

Weibull CDF / PDF -
Weibull distributions are often used in product reliability to capture lifetime and failure occurrences. We are controlling our weibull curve parameters by using the T50 and T90 values, which represent the time at which 50% and 90% of the cohort has failed, respectively. For PV panels that are expected to last past their 30 year warranty, T50 and T90 must be bigger than 30, for example T50=35 years and T90=40 years. See the Weibull section for more details.

Weibull CDF / PDF
~~~~~~~~~~~~~~~~~~~
Weibull distributions are often used in product reliability to capture lifetime and failure occurrences. We are controlling our weibull curve parameters by using the T50 and T90 values, which represent the time at which 50% and 90% of the cohort has failed, respectively. For PV panels that are expected to last past their 30 year warranty, T50 and T90 must be bigger than 30, for example T50=35 years and T90=40 years. See the Weibull section for more details.


EOL Pathway Options
~~~~~~~~~~~~~~~~~~~~~
Landfill
^^^^^^^^^^
Module or material is waste and gets landfilled. 

Repair
^^^^^^^
A module is at EOL (through failure) and an onsite fix to the module defect or problem is possible such that the module is not demounted. If the module is not repaired, it is assumed to be at End of Life.

Refurbish
^^^^^^^^^^
Module is at EOL (through failure or degradation), and the module is demounted and taken offsite to resolve defects or problems.

Reuse
^^^^^^^
Module is at EOL (through degradation) and is demounted and removed from the field. Offsite, the module is assessed/tested/recertified and found to be in sufficient working condition to be reinstalled at the same site or on a new site. Could be as a result of a solar PV farm "Repowering".

Recycle
^^^^^^^^
We are considering Recycle as a Circularity Pathway at two stages in the PV lifetime: during Manufacturing ("pre-consumer"), to salvage material losses due to the manufacturing inefficiencies, and EOL. When a module is at EOL and is not reused, repaired, refurbished, or sent directly to landfill it can be recycled into its constituent materials. These materials can be used to displace virgin materials for the manufacture of new modules or other products. Different quality products are considered from recycling; high quality is used for new modules (same-cycling) or for other products ("o-cycling"); low quality is considered down-cycled into products with less stringent material quality requirements.

"The R's" - different pathways for circular economy. The idea for the calculator is to capture the material and energy benefits of each of these pathways to help inform of their impact, as they might have different requirements and efficacy. This pathways can be improved through science (for example, improving recycling efficiency of a material), as well as with policy (for example, choosing to support refurbishment research).

