.. _package_overview:

Package Overview
================

The PV ICE tool explores the effects of Circular Economy (CE) pathways for photovoltaic (PV) materials. It can be used to quantify and assign a value framework to CE efforts including re-design, lightweighting, replacement, reuse, recycling, and lifetime and reliability improvements across the PV value chain. PV ICE enables tradeoff analysis through scenario comparisons, and is highly customizable through user inputs such as deployment schedules, module properties and component materials, and CE pathways. The PV ICE tool considers the following material flows and their associated energies:

.. image:: ../../images_wiki/PV_ICE_diagram-simpleAltUpdate.PNG
  :width: 450
  :alt: Simplified diagram of mass flows captured in the PV ICE tool.

PV ICE system boundaries include “Virgin Extraction & Refinement,” “PV Manufacturing,”  “Use Phase,” and “End-of-Life,”. Mass flows (arrows) are affected by process efficiencies (circles) and decision points (hexagons). Mass flows are split into module and material properties. All materials are tracked on a mass-per-module-area basis, allowing conversion between module and material. The module and its materials can follow a linear flow from extraction to EoL in the landfill, or follow circular pathways (teal arrows). Process efficiencies or yields (circles) dictate extra material demands and wastes generated in a process step (ex: kerf loss of silicon). Decision points (hexagons) are influenced by stakeholders or policy decisions and regulations, dictating the fraction of modules or materials which follow a specific pathway (ex: fraction of modules recycled at EoL).

Calculations of mass and energy are driven by annual installed capacity. The input deployment schedule and module efficiency are used to calculate the area of new deployed capacity. The material demand is determined from this deployed area because materials are tracked on a per module area basis. Cohorts of intalled modules (and their associated materials) are installed and are tracked annually for power degradation (ex: 0.5%/year), probability of failure (Weibull), and their economic lifetime (ex: 25 year warranty).  As modules enter end of life (EOL) through any of the 3 EOL criteria, a collection rate is applied, and they are first evaluated for "good status" or "bad status". Based on their good/bad status, different EOL pathways are available, including landfill, reuse, remanufacture and recycling. Inputs determine the fraction of modules entering circular EOL pathways, which can be used to offset virgin material demand for the upcoming cohort of deployment. All properties/inputs are dynamic with time to account for PV module technology evolution and changing business practice and policy landscape.

Inputs to the calculator are csvs with the columns corresponding to mass and energy quantities and pathway determinations. In addition to the PV ICE framework, we provide module and material baselines of the average crystalline silicon PV module over time, accounting for technology evolution.  Baseline input files of module and materials for 1995-2050 are available in the ``PV_ICE/baselines`` folder.


Framework and Definitions
----------------------------

The following flow chart details the mass and energy path structure of the PV ICE framework.

.. image:: ../../images_wiki/MassEnergyFlowChart.PNG
  :width: 900
  :alt: Full logic flow chart of mass and energy quantities as captured and structured in the PV ICE tool. Begin at the "Mine" in the bottom right corner.

Material Extraction, PV Manufacturing & Use Phase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mining/extraction and refinement/processing of the virgin materials are represented as a single efficiency for each material ("Virgin Material Efficiency") capturing the order of magnitude of material extraction yield. Next, "Manufacturing" converts a mass of processed materials into an area of module. Yields for both material use and module manufacturing are considered. Recycling pathways are available for manufacturing scrap and mimic the EOL recycling pathways described below. "Lifetime/UsePhase" installs the module and generates electricity over it's lifetime, accounting for expected power degradation. 

EOL
~~~~~
Modules reach End of Life in one of three forms: economic/warranty lifetime, power degradation, or probabilistic failure. All functions are applied to each annual cohort of modules. 

Economic/Warranty Lifetime
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This annual module property reflects the market trends of PV system lifetime. The PV module is the longest lived component of a PV system. Typically, the PV system has an economic pay back period, loan term, or PPA, while the PV module has a warranty period (ex: 25 years). This input allows for a PV system to reach EOL throuh non-technical determination. The economic EOL mode has the potential for the Merchant Tail EOL pathway.

Degradation
^^^^^^^^^^^^^
Modules have an expected degradation from their nameplate capacity each year (ex: 0.5%/year), producing less power over time. Once the nameplate capacity is reduced below a certain threshold (ex: 80% of nameplate), then modules are deemed to be at EOL. 

Failure
^^^^^^^^^
All products have a probability of failure. Failure is a random occurrence where the module stops working on site at any point after installation. Early loss of modules are due to manufacturing defects, low quality components, or installation errors and usually represent a higher amount of failures in the first 4 years of deployment. Failure probability also increases as the modules get near their end of lifetime.

Weibull distributions are commonly used in product reliability to capture lifetime and failure occurrences. We are controlling our weibull curve parameters by using the T50 and T90 values, which represent the time at which 50% and 90% of the cohort has failed, respectively. For PV panels that are expected to last past their 30 year warranty, T50 and T90 must be bigger than 30, for example T50=35 years and T90=40 years. PV ICE can calculate and print out the "alpha" and "beta" Weibull shape values corresponding to the T50 and T90 values as required.

The failure EOL mode has the potential for the "Repair" EOL pathway.


EOL Pathway Options
~~~~~~~~~~~~~~~~~~~~~
Each year in the model produces modules that enter EOL. Below is a flow chart of the EOL decision tree.

.. image:: ../../images_wiki/EOLLogic.PNG
  :width: 900
  :alt:

First, there are two pathways before demounting the module which depend on EOL mode (as described above).

Repair 
^^^^^^^^
(Failure only, before collection) A module is at EOL (through failure) and an onsite fix to the module defect or problem is possible such that the module is not demounted. If the module is not repaired, it is assumed to be at End of Life and goes through collection.

Merchant Tail
^^^^^^^^^^^^^^
(Economic only, before collection) Merchant tail is an industry practice where the system is left inplace after the loan or PPA has ended. It's called merchant tail because typically this is a bump in revenue for the system. If the module is used for merchant tail, then it is returned to use phase/generating capacity and will continue to degrade and fail at cohort determined rates.


If the module doesn't undergo repair or merchant tail, then it is demounted and an EOL module collection is considered. A collection efficiency/rate of modules is applied - any non-collected modules are landfilled (this is representative of ~2020 industry practice). 

Next, EOL modules are checked for quality, which determines available EOL paths.

* Status = Good: Module is at > 80% of nameplate power and did not reach EOL through Failure
* Status = Bad: Module is at < 80% of nameplate power and/or reached EOL through Failure

A summary of the EOL path options, requirements, and corresponding variables is found in the table below.

.. csv-table:: EOL Pathway Options
  :file: ../../images_wiki/EOLLogic.CSV
  :widths: 10,10,40,40
  :header-rows: 1

0. Resell
^^^^^^^^^^^
The module is demounted, undergoes recertification testing, and is sold on the secondary market. The module is returned to the use phase at it's cohort determined degraded power and continues generating power. It will re-enter EOL again later.

1. Landfill
^^^^^^^^^^^^
(optional) Module materials are landfilled. This variable will be adjusted to accommodate the fractions of other pathways.

2. Store
^^^^^^^^^^
(BETA) The module is demounted and warehoused.

3. Remanufacture
^^^^^^^^^^^^^^^^^
The module is demounted and sent through a dissassembly process with the goal of recovering material components intact (ex: front glass). There is a yield associated with the module dissassembly process and seperate material cleaning process. Whether or not a material is a target of remanufacture is determined in the material properties.

4. Recycle
^^^^^^^^^^^^
The module is demounted and sent through a dissassembly and/or crushing process with the goal of recovering constituent materials. These materials undergo individual recycling processes (with associated yields). The recycled materials are recovered at low purity and used in other industries ( down-cycled, open-loop), at high purity and used in other industries (HQ open-loop), or at high purity and used in the manufacture of new PV modules offsetting virgin material demand (HQ closed-loop). 