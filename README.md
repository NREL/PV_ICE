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
    <a href="https://github.com/NREL/CircularEconomy-MassFlowCalculator/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/pvlib.svg" alt="license" />
    </a>
</td>
</tr>
<tr>
  <td>Build Status</td>
  <td>
    <a href="http://circulareconomy-massflowcalculator.readthedocs.org/en/latest/">
    <img src="https://readthedocs.org/projects/circulareconomy-massflowcalculator/badge/?version=latest" alt="documentation build status" />
    </a>
  </td>
</tr>
<tr>
  <td>Publications</td>
  <td>
    <!--- <a href="https://doi.org/10.5281/zenodo.3762635">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3762635.svg" alt="zenodo reference">
     ---> Connected to Zenodo, awaiting first release
    </a>
  </td>
</tr>
</table>


# PV_ICE: PV in the Circular Economy, Dynamic Energy and Materials TOOL

This open-source tool implements Circular Economy metrics for photovoltaic (PV) materials. It can be used to quantify and assign a value framework to efforts on re-design, reduction, replacement, reuse, recycling, and lifetime and reliability increases in the PV value chain.

The PV_ICE is leveraging published data from different sources on PV manufacturing and predicted technological changes. Input data is being compiled [here](https://docs.google.com/spreadsheets/d/1WV54lNAdA2uP6a0g5wMOOE9bu8nbwvnQDgLj3GuGojE/edit?usp=sharing)

This tool will help implement circularity metrics, quantify and assign a value framework to efforts on re-design, reduction, replacement, reusage, recycling, and lifetime and reliability increases on PV.


Documentation
=============

The calculator follows the following diagram for calculating Mass Flow. Baseline inputs are available in the PV_ICE \ baselines folder for US and World past and projected values. Full documentation can be found at [readthedocs](http://CircularEconomy-MassFlowCalculator.readthedocs.io/en/latest/).

<img src="docs/images_wiki/MFC-Diagram.PNG" width="550">

[Input data](https://docs.google.com/spreadsheets/d/1WV54lNAdA2uP6a0g5wMOOE9bu8nbwvnQDgLj3GuGojE/edit?usp=sharing) references include:

Real world installation data from IEA-PVPS reports for 1995 - 2010 (K. Bolcar and K. Ardani, “National Survey Report of PV Power Applications in the United States 2010,” IEA-PVPS, National Survey T1-19:2010, 2010. [Online]. Available: https://iea-pvps.org/national-survey-reports/.)

Projection installation data 2010-2019 from Q4 2019 Wood Mackenzie Power & Renewables/SEIA U.S. Solar Market Insight (A. Perea et al., “U.S. Solar Market Insight: Q4 2019,” SEIA, Wood Mackenzie Power & Renewables, Dec. 2019.)

Installations projected to increase 8.9% compound annual growth rate through 2050 (IRENA, “Future of Solar PV 2019,” IRENA, 2019. Accessed: Apr. 02, 2020. [Online]. Available: https://irena.org/-/media/Files/IRENA/Agency/Publication/2019/Nov/IRENA_Future_of_Solar_PV_2019.pdf.)

Degradation rate (in percentage power loss per year) (D. C. Jordan, S. R. Kurtz, K. VanSant, and J. Newmiller, “Compendium of photovoltaic degradation rates,” Progress in Photovoltaics: Research and Applications, vol. 24, no. 7, pp. 978–989, 2016, doi: 10.1002/pip.2744.)

Glass thickness data (ITRPV, “International Technology Roadmap for Photovoltaic (ITRPV) 2019,” ITRPV, 10th, Oct. 2019.)

Reliability data, i.e. T50 and T90 lifetime in years (D. C. Jordan, B. Marion, C. Deline, T. Barnes, and M. Bolinger, “PV field reliability status—Analysis of 100 000 solar systems,” Progress in Photovoltaics: Research and Applications, vol. n/a, no. n/a, Feb. 2020, doi: 10.1002/pip.3262.)

All manufacturing, recyling, collection efficiencies currently estimates with real world data pending.


Installation
============

CircularEconomy-MassFlowCalculator releases may be installed using the ``pip`` and ``conda`` tools.
Please see the [Installation page](http://PV_ICE.readthedocs.io/en/latest/installation.html) of the documentation for complete instructions.

CircularEconomy-MassFlowCalculator is compatible with Python 3.5 and above.

Install with:

    pip install PV_ICE

For developer installation, download the repository, navigate to the folder location and install as:

    pip install -e .


Contributing
============

We need your help to make PV_ICE a great tool!
Please see the [Contributing page](http://PV_ICE.readthedocs.io/en/stable/contributing.html) for more on how you can contribute.
The long-term success of CircularEconomy-MassFlowCalculator requires substantial community support.


License
=======

BSD 3-clause


Getting support
===============

If you suspect that you may have discovered a bug or if you'd like to
change something about CF-MFA, then please make an issue on our
[GitHub issues page](https://github.com/NREL/CircularEconomy-MassFlowCalculator/issues).


Citing
======

If you use PV_ICE in a published work, please cite:

	Ayala Pelaez, Silvana; Mirletz, Heather; Silverman, Timothy; 
	Carpenter, Alberta; Barnes, Teresa. “De-fluffing Circular 
	Economy Metrics with Open-Source Calculator for PV” 
	2020 PV Reliability Workshop, Denver CO.

Please also cite the DOI corresponding to the specific version of
PV_ICE that you used. PV_ICE DOIs are listed at
[Zenodo.org](https://zenodo.org/)
