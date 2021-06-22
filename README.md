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
  <td>Documentation</td>
  <td>
	<a href='https://pv-ice.readthedocs.io/en/latest/?badge=latest'>
	    <img src='https://readthedocs.org/projects/pv-ice/badge/?version=latest' alt='Documentation Status' />
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

<img src="docs/images_wiki/PV_ICE_Diagram-AltLegend.png" width="550">

[Input data](https://docs.google.com/spreadsheets/d/1WV54lNAdA2uP6a0g5wMOOE9bu8nbwvnQDgLj3GuGojE/edit?usp=sharing) references include:

Real world installation data from IEA-PVPS reports for 1995 - 2010 (K. Bolcar and K. Ardani, “National Survey Report of PV Power Applications in the United States 2010,” IEA-PVPS, National Survey T1-19:2010, 2010. [Online]. Available: https://iea-pvps.org/national-survey-reports/.) Installation data 2010-2020 from U.S. Solar Market Insight 2020-yir from SEIA & Wood Mackenzie (M. Davis et al., “U.S. Solar Market Insight: 2020 Year in review,” Wood Mackenzie Power & Renewables, Mar. 2021.) All installation data is weighted by the marketshare of silicon PV, as derived from a combination of:
[1]G. Barbose and N. Darghouth, “Tracking the Sun 2019,” LBNL, Oct. 2019. Accessed: Aug. 13, 2020. [Online]. Available: https://emp.lbl.gov/sites/default/files/tracking_the_sun_2019_report.pdf
[2]M. Bolinger, J. Seel, and D. Robson, “Utility-Scale Solar 2019,” LBNL, Dec. 2019. Accessed: Aug. 13, 2020. [Online]. Available: https://emp.lbl.gov/sites/default/files/lbnl_utility_scale_solar_2019_edition_final.pdf 

Installation projections either increase by 8.9% compound annual growth rate through 2050 (IRENA, “Future of Solar PV 2019,” IRENA, 2019. Accessed: Apr. 02, 2020. [Online]. Available: https://irena.org/-/media/Files/IRENA/Agency/Publication/2019/Nov/IRENA_Future_of_Solar_PV_2019.pdf.) or are drawn from NREL's Electrification Futures Studies (https://cambium.nrel.gov/?project=fc00a185-f280-47d5-a610-2f892c296e51).

Degradation rates (in percentage power loss per year) (D. C. Jordan, S. R. Kurtz, K. VanSant, and J. Newmiller, “Compendium of photovoltaic degradation rates,” Progress in Photovoltaics: Research and Applications, vol. 24, no. 7, pp. 978–989, 2016, doi: 10.1002/pip.2744.)

Reliability data, i.e. T50 and T90 lifetime in years (D. C. Jordan, B. Marion, C. Deline, T. Barnes, and M. Bolinger, “PV field reliability status—Analysis of 100 000 solar systems,” Progress in Photovoltaics: Research and Applications, vol. n/a, no. n/a, Feb. 2020, doi: 10.1002/pip.3262.)

Project Lifetime data in years from (R. Wiser, M. Bolinger, and J. Seel, “Benchmarking Utility-Scale PV Operational Expenses and Project Lifetimes: Results from a Survey of U.S. Solar Industry Professionals,” None, 1631678, ark:/13030/qt2pd8608q, Jun. 2020. doi: 10.2172/1631678.)

Each material is a compilation of multiple sources, most notably consistent with ITRPV data. Please see the Jupyter Journals for the derivations and sources of material baseline inputs.


Installation for PV ICE
=======================

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
[GitHub issues page](https://github.com/NREL/PV_ICe/issues).


Citing
======

If you use PV_ICE in a published work, please cite:

	Ayala Pelaez, Silvana; Mirletz, Heather; Silverman, Timothy; 
	Carpenter, Alberta; Barnes, Teresa. “De-fluffing Circular 
	Economy Metrics with Open-Source Calculator for PV” 
	2020 PV Reliability Workshop, Denver CO.

and also please also cite the DOI corresponding to the specific version of
PV_ICE that you used. PV_ICE DOIs are listed at
[Zenodo.org](https://zenodo.org/). For example for version 0.1.0:

	Silvana Ayala Pelaez, Heather Mirletz, & Tim Silverman. 
	(2020, December 16). NREL/PV_ICE: First Release v0.1.0 
	(Version v0.1.0). Zenodo. http://doi.org/10.5281/zenodo.4324011
