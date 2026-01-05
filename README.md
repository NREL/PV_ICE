<img src="docs/images_wiki/CE-MFC.png" width="400">

<table>
<tr>
  <td>Version</td>
  <td>
  <a href="https://zenodo.org/badge/latestdoi/248347431"><img src="https://zenodo.org/badge/248347431.svg" alt="DOI"></a>
</td>
</tr>

<tr>
  <td>License</td>
  <td>
    <a href="https://github.com/NREL/PV_ICE/blob/master/LICENSE.md">
    <img src="https://img.shields.io/pypi/l/pvlib.svg" alt="license" />
    </a>
</td>
</tr>
<tr>
  <td>Documentation</td>
  <td>
	<a href='https://pv-ice.readthedocs.io/en/latest/?badge=latest'>
	    <img src='https://readthedocs.org/projects/pv-ice/badge/?version=latest' alt='Documentation Status' />
	</a>
  </td>
</tr>
</table>


# PV ICE: A Dynamic Framework for Photovoltaic Material, Energy, and Lifetime Analysis

PV ICE is an open-source modeling framework for quantifying photovoltaic (PV) material flows, energy flows, and lifetime behavior across deployment, operation, reuse, and end-of-life scenarios.

The framework supports scenario-based analysis of evolving PV technologies by combining deployment schedules, module and material properties, and reliability and degradation parameters. PV ICE enables transparent accounting of capacity evolution, material demand, waste generation, and energy balance over time, supporting comparative analysis across technology designs and lifecycle pathways.

PV ICE was originally developed to explore circular material pathways in PV systems and has since evolved into a general modeling framework for lifecycle and reliability-aware analysis.

The provided PV ICE module and material baselines leverage published data from many sources on PV manufacturing and predicted technological changes. Input data are being compiled [here](https://docs.google.com/spreadsheets/d/1WV54lNAdA2uP6a0g5wMOOE9bu8nbwvnQDgLj3GuGojE/edit?usp=sharing) and the baselines are available here for use in other projects as well as for the PV ICE tool.


## Scope and Intended Use

PV ICE provides core calculations for photovoltaic material flows, energy flows, and lifetime behavior.  
The framework is designed to support comparative scenario analysis and does not prescribe policy, investment, or operational decisions.

Downstream applications—such as techno-economic assessments, repowering decision tools, or site-specific case studies—may use PV ICE outputs but are maintained in separate repositories to preserve modularity and reproducibility.

How it Works
=============

This section provides a brief description of how the PV ICE tool works. FULL DOCUMENTATION CAN BE FOUND AT [readthedocs](https://pv-ice.readthedocs.io/en/latest/?badge=latest).


Mass
-----

PV ICE is a dynamic mass flow based tool. It takes in any deployment forecast of any evolving module design along with it's component materials and uses user-defined lifetime, degradation, and reliability parameters to calculate effective capacity, virgin material demand, and life cycle wastes. The calculator captures all the mass flows shown in the simplified diagram below for all years studied in a simulation (ex: 2020-2050). 

<img src="docs/images_wiki/PV_ICE_diagram-simpleAltUpdate.png" width="550">

Annually deployed cohorts of modules are tracked through the simulation, subjected to lifetime, degradation, and reliability parameters, and guided along user-defined lifecycle pathways (e.g., continued operation, reuse, recycling). The PV ICE framework is designed for scenario comparisons (ex: different deployment schedules, module designs, or circular pathways) and is capable of both geospatial and temporal analysis (i.e. when and where materials will be demanded or are available).

Module and material properties are known to be variable with time, and PV ICE can capture this dynamic evolution of PV technology. Dynamic baseline inputs for crystalline silicon and cadmium-telluride PV modules and their component materials are provided in the PV_ICE \ baselines folder. These baselines are derived from [literature and report data](https://docs.google.com/spreadsheets/d/1Ec5JRBSN2NFXjEABgUp1ch-EG6uQao8j5Rk1MLuZZYI/edit?usp=sharing). Module baselines capture the annual average module (i.e. a market share weighted average of PV technologies deployed). Each material similarly is a market share weighted average compiled from multiple sources, most notably consistent with ITRPV data. Please see the Jupyter Journals (tutorials \ baseline development documentation) for the derivations and sources (baselines \ SupportingMaterials) of the provided c-Si and CdTe baselines. Simplified baselines for perovskites are also included, as well as of business as usual and ideal modules evolutions as described in [Mirletz et al., 2024]: https://doi.org/10.1051/epjpv/2024015. Alternate module and material files can be created by the user.


Energy
-------

Energy accounting is a critical complement to material flow analysis when evaluating the lifecycle performance of energy technologies. Additionally, few studies of Circular Economy (CE) pathways consider the energy return on investment of a particular pathway. PV ICE energy flows fill this analysis gap, and provide useful insights into the potential tradeoffs between mass and energy of CE pathways.

The energy flows of PV ICE are based on the mass flows. These energy flows, like the mass flows, are dynamic with time and are seperated into module and material energies. For each supply chain process step captured in the mass flows, an energy per module area or energy per material mass is captured as an input (ex: module manufacturing energy, energy to manufacture rolled glass from silica sand, energy to crush a module for recycling ). The energy demanded for each step is the sum of all electrical energy demands and all fuel/heating energy demands. 

We provide an energy baseline for crystalline silicon modules and cadmium telluride modules including their component materials. Data for these baselines is being compiled from [literature and report data](https://docs.google.com/spreadsheets/d/1Ec5JRBSN2NFXjEABgUp1ch-EG6uQao8j5Rk1MLuZZYI/edit?usp=sharing). For the complete derivation of the energy demands, please see the Jupyter Journals (tutorials \ baseline development documentation) and (baselines \ SupportingMaterials). Simplified baselines for perovskites are also included, as well as of business as usual and ideal modules evolutions as described in [Mirletz et al., 2024]: https://doi.org/10.1051/epjpv/2024015. Alternate module and material files can be created by the user.

After running a mass flow simulation, an energy flow calculation can be run which will multiply the energy demands by the mass flows and calculate annual generation from the deployed modules. Results of this calculation provide annual, cumulative, and lifetime energy demands and energy generated. These values can be used to calculate energy balance metrics such as energy return on investment (EROI), net energy, and energy payback time (EPBT). 


Installation for PV ICE
=======================

PV ICE releases may be installed using the ``pip`` and ``conda`` tools.
Please see the [Installation page](http://PV_ICE.readthedocs.io/en/latest/installation.html) of the documentation for complete instructions.

PV ICE is compatible with Python 3.5 and above.

Install with:

    pip install PV_ICE

For developer installation, download the repository, navigate to the folder location and install as:

    pip install -e .


How to Get Started
===================

After you have installed PV ICE, we recommend heading over to our tutorials jupyter journals (PV ICE \ docs \ tutorials). There you will find journals ["0 - quick start Example"](https://github.com/NREL/PV_ICE/blob/development/docs/tutorials/0%20-%20quickStart%20Example.ipynb) and ["1 - Beginner Example"](https://github.com/NREL/PV_ICE/blob/development/docs/tutorials/1%20-%20Beginner%20Example.ipynb) which can help guide you through your first simulation using the PV ICE provided crystalline silicon PV baselines. In journals 2-4 we walk you through modifications to the basic simulation, including modifying parameters with PV ICE functions to suit your analysis needs.


Some Analyses Featuring/Leveraging PV ICE
==========================================

PV ICE has been used in a variety of published analyses, including:

**The Solar Futures Report and Circular Economy Technical Report**

    Ardani, Kristen, Paul Denholm, Trieu Mai, Robert Margolis, 
    Eric O’Shaughnessy, Timothy Silverman, and Jarett Zuboy. 2021. 
    “Solar Futures Study.” EERE DOE. 
    https://www.energy.gov/eere/solar/solar-futures-study.

    Heath, Garvin, Dwarakanath Ravikumar, Silvana Ovaitt, 
    Leroy Walston, Taylor Curtis, Dev Millstein, Heather Mirletz, 
    Heidi Hartman, and James McCall. 2022. 
    “Environmental and Circular Economy Implications of Solar Energy
     in a Decarbonized U.S. Grid.” NREL/TP-6A20-80818. NREL.

**ISCIENCE**

    S. Ovaitt & H. Mirletz, S. Seetharaman, and T. Barnes, 
    “PV in the Circular Economy, A Dynamic Framework Analyzing 
    Technology Evolution and Reliability Impacts,” 
    ISCIENCE, Jan. 2022, doi: https://doi.org/10.1016/j.isci.2021.103488.

**EPJ**

    Mirletz, H., Ovaitt, S., Sridhar, S., & Barnes, T. M. (2024). 
    "Prioritizing circular economy strategies for sustainable PV deployment at the terawatt scale."
    EPJ Photovoltaics*, 15, 18.  
    https://doi.org/10.1051/epjpv/2024015

Other

**PVSC**

    H. M. Mirletz, S. Ovaitt, A. Gaulding, S. Sridhar, and T. Barnes,
     “Quantifying Energy flows in PV Circularity Processes,” 
     Philidelphia PA, Jun. 2022, p. 3.


**PVRW**

    H. Mirletz, S. Ovaitt, and T. M. Barnes, 
    “Short-Lived Modules Need to be Efficient, Lightweight,
     and Circular for the Energy Transition,” online, Feb. 2022.



Contributing
============

We need your help to make PV ICE a great tool!
Please see the [Contributing page](http://PV_ICE.readthedocs.io/en/stable/contributing.html) for more on how you can contribute.
The long-term success of PV ICE requires substantial community support.


License
=======

BSD 3-clause


Getting support
===============

If you suspect that you may have discovered a bug or if you'd like to
change something about CF-MFA, then please make an issue on our
[GitHub issues page](https://github.com/NREL/PV_ICe/issues).


Citing
======

If you use PV_ICE in a published work, please cite:

    S. Ovaitt & H. Mirletz, S. Seetharaman, and T. Barnes, 
    “PV in the Circular Economy, A Dynamic Framework Analyzing 
    Technology Evolution and Reliability Impacts,” 
    ISCIENCE, Jan. 2022, doi: https://doi.org/10.1016/j.isci.2021.103488.


and also please also cite the DOI corresponding to the specific version of
PV_ICE that you used. PV_ICE DOIs are listed at
[Zenodo.org](https://zenodo.org/badge/latestdoi/248347431). For example for version 0.2.1:

	S. Ovaitt, H. Mirletz, A. Hegedus. (2022). 
	NREL/PV_ICE: v0.3.0 Release. Zenodo. 
	https://doi.org/10.5281/zenodo.7065727
