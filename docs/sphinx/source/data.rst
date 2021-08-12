.. _data:

Data: Mass
===========

Input Data for Mass Flows
----------------
At least two files of baselines are needed for the simulation: 1) one file with module parameters throughout the years, for example *baseline_US*, and 2) one or more files with process parameters for each material being analyzed in the module, for example *baseline_glass*. See **baseline_module** and **baseline_material** for more details on input columns needed and their definition. 

The baselines folder in the PV_ICE tool provides baseline scenarios for modules in the US and World level, as well as baseline_materials for glass, Silver and Aluminum. For more details on the source of these values, see the documentation on baselines. 


baseline_module
~~~~~~~~~~~~~~~~
year : int
Year. 

new_Installed_Capacity_[MW]: float
New installed PV capacity in MW. Additions of PV modules in nameplate MW peak in the specified year.

module_efficiency_[%]: float 
Nameplate efficiency of the module. i.e.: 22.3 %.

module_reliability_t50_[years]: float
(optional) The number of years after the installation year at which 50% of the cohort of  modules will be removed from the field

module_reliability_t90_[years]: float
(optional) The number of years after the installation year at which 90% of the cohort of  modules will be removed from the field

module_degradation_[%]: float
Percentage annual reduction of the module's performance, relative to it’s nameplate. i.e. 0.5 %. 

module_manufacturing_efficiency_[%]: float
Efficiency of manufacturing modules (if there are losses of modules and all associated   products during production). 

module_EOL_collection_losses_[%]: float
Percentage of modules collected from the field at end of life for sorting and disposition. i.e. 30%

module_EOL_collected_recycled_[%] : float
Percentage of collected end of life modules that are sent to recycling

module_repowering_[%]: float
Percentage of modules at EOL from degradation that are repowered.

module_repairing_[%]: float
Percentage of modules at EOL from failure that are repaired and go back to functioning  in the field.


baseline_material
~~~~~~~~~~~~~~~~~~~~
material_virgin_efficiency_[%]: float
Efficiency of mining, extracting, and purifying the material up to the point of entry into the module manufacturing line. 

material_masspermodule_[g/m^2]: float
Mass of specified material in kilograms per PV module

material_manufacturing_efficiency_[%]: float
Efficiency of the manufacturing production line for the material - i.e. how much of the input material is incorporated into the module

material_manufacturing_scrap_recycled_[%]: float
The percentage of the scrap generated at the manufacturing facility that is sent to recycling (internal or external).

material_manufacturing_scrap_recycling_efficiency_[%]: float
Efficiency of the scrap recycling process

material_manufacturing_scrap_recycled_into_HighQuality_[%]: float
Percentage of manufacturing scrap which is recycled into high quality material and used for non-PV module applications externally (open loop)

material_manufacturing_scrap_recycled_into_HighQuality_reused_for_module_manufacturing_[%]: float
Percentage of manufacturing scrap material which is recycled and used in the manufacturing of a new module

material_EOL_collected_Recycled_[%]: float
Percentage of collected end of life material which is sent to recycling

material_EOL_Recycling_efficiency_[%]: float
Efficiency of the end of life recycling process, i.e. percentage of the material that is put  through the process that is successfully recycled

EOL_Recycled_Material_into_HighQuality_[%]: float
Percentage of collected end of life material recycled into high quality material and used  for non-PV modules applications externally (open loop)

EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%]: float
Percentage of end of life recycled material that is recycled into high quality material and used in the manufacture of a new module (closed loop)



Output Data for Mass flows
------------------
PV ICE calculates virgin material, landfilled and recycled materials, and the many other steps in the Mass Flow Diagram for each year dynamically. It appends these annual results to the dataframe loaded from baseline_module and baseline_materials. A description of the output columns is below.

PV ICE Outputs
~~~~~~~~~~~~~~~~
module_installedCapacity_[MW]
Summation of all cohorts of installed PV actively in the field in the specified year

material_installedMass_[kg]: float
Summation of material associated with the total installed capacity in the field in a specified year

material_EoL_[kg]: ** material_EoL_waste_[kg]:
Material in modules from all cohorts that reach that year the end-of-life stage. This value already reflects repowered, reused, or  re-manufactured modules.

material_EoL_CollectionLost: float
Summation of waste material accounting for collection efficiency on an annual basis

material_EoL_Collected_Recycled: float
Summation of waste material sent for recycling, accounting for collection efficiency  losses

material_EoL_Collected_Landfilled: float
End of life collected material that is landfilled, as opposed to recycled, on an annual basis

material_EoL_Recycled_Succesfully: float
End of life collected material that is successfully recycled, accounting for recycling process efficiencies, on an annual basis.

material_EoL_Recycled_Losses_Landfilled: float
Material waste as output by the recycling process, which is landfilled, on an annual basis.

material_EoL_Recycled_into_HQ: float
Quantity of material which is successfully recycled into high quality material, on an annual basis.

material_EoL_Recycled_into_Secondary: float
Quantity of material recycled into low quality material, i.e. downcycled, on an annual basis.

material_EoL_Recycled_HQ_into_Manufacturing: float
Quantity of material which is successfully recycled into high quality material and is used in closed loop for new PV modules, on an annual basis.

material_EoL_Recycled_HQ_into_OtherUses: float
Quantity of material which is successfully recycled into high quality material and is used in open loop in other applications, on an annual basis.

material_manufacturing_input: float
Quantity of material required to be input to the manufacturing process, accounting for inefficiencies in the production process, on an annual basis.

material_manufacturing_scrap: float
Quantity of scrap material generated during the manufacturing process, on an annual basis.

material_manufacturing_scrap_Recycled: float
Quantity of scrap material from the manufacturing process which is recycled, on an annual basis.

material_manufacturing_scrap_Landfilled: float
Quantity of scrap material generated during the manufacturing process which is not recycled, on an annual basis.

material_manufacturing_Scrap_Recycled_Succesfully: float
Quantity of scrap material generated during the manufacturing process which is successfully recycled, accounting for process efficiencies, on an annual basis.

material_manufacturing_Scrap_Recycled_Losses_Landfilled: float
Quantity of waste material generated and landfilled from the scrap recycling process, on an annual basis.

material_Manufacturing_Recycled_into_HQ: float
Quantity of manufacturing scrap material successfully recycled into high quality material, on an annual basis.

material_Manufacturing_Recycled_into_Secondary: float
Quantity of manufacturing scrap material successfully recycled into low quality material, i.e. downcycled, on an annual basis.

material_Manufacturing_Recycled_HQ_into_Manufacturing: float
Quantity of manufacturing scrap material successfully recycled into high quality material and input to the manufacturing process (closed loop), on an annual basis.

material_Manufacutring_Recycled_HQ_into_OtherUses: float
Quantity of manufacturing scrap material successfully recycled into high quality material and used in external applications (open loop), on an annual basis.

material_virgin_stock: float
Annual quantity of virgin raw material inputs to the manufacturing process to provide for the manufacturing needs. This value compensates for process and efficiency parameters such  as recycled material input.  

material_Total_EoL_Landfilled_Waste: float
Annual quantity of material sent to the landfill from the end of life, including process inefficiencies and collection losses.  

material_Total_Manufacturing_Landfilled_Waste: float
Annual quantity of material sent from the manufacturer to the landfill, including process and internal recycling process inefficiencies.  

material_Total_Landfilled_Waste: float
EoL + Manufacturing. Annual total quantity of material from all processes, manufacturing, recycling, end of life, which are sent to the landfill.  

Total_EoL_Recycled_OtherUses: float
Annual total quantity of material from all processes, manufacturing, recycling, end of life, which are recycled into external applications, open loop.  

Mass Data References
---------------------

Installed Capacity - Past
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Installation data for solar pv installed in the US and globally from several IEA-PVPS T1 reports, Wood MacKenzie Power and Renewables Reports, and LBNL Utility-Scale Solar Reports. Note that installed capacity includes on and off grid, residential, commercial, and utility scale PV. Note that IEA PVPS data (US and global) pre-2009 data is assumed to be all silicon technology.

US Installations
1995 through 2008 taken from (K. Bolcar and K. Ardani, "National Survey Report of PV Power Applications in the United States 2010," IEA-PVPS, National Survey T1-19:2010, 2010. [Online]. Available: https://iea-pvps.org/national-survey-reports/.)

2009 taken from (M. Bolinger, J. Seel, and D. Robson, "Utility-Scale Solar 2019," LBNL, Dec. 2019. Accessed: Aug. 13, 2020. [Online]. Available: https://emp.lbl.gov/sites/default/files/lbnl_utility_scale_solar_2019_edition_final.pdf.)

2010 through 2019 taken from Wood Mackenzie Power & Renewables PV Forecasts Q2 of 2020 ("US PV Forecasts Q2 2020 Report," Wood Mackenzie Power & Renewables.)

Other resources consulted include:
(F. H. Morse, "IEA PVPS Task 1 1993," IEA-PVPS, IEA PVPS T1:1993, Mar. 1995. Accessed: Aug. 13, 2020. [Online]. Available: https://iea-pvps.org/wp-content/uploads/2020/01/tr_1993.pdf.)
("IEA PVPS Task 1 1997," IEA-PVPS, IEA PVPS T1:1997, Mar. 1997. Accessed: Aug. 13, 2020. [Online]. Available: https://iea-pvps.org/wp-content/uploads/2020/01/tr_1995_01.pdf.)
("Trends in Photovoltaic Applications 2019," IEA-PVPS, IEA PVPS T1-36:2019, Aug. 2019. Accessed: Aug. 12, 2020. [Online]. Available: https://iea-pvps.org/wp-content/uploads/2020/02/5319-iea-pvps-report-2019-08-lr.pdf.)
IRENA Solar Energy Data (https://www.irena.org/solar, and https://irena.org/Statistics/Download-Data)


Installed Capacity - Projections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Projection installation data for 2019 through 2050 options include:

* Increasing deployment of 8.9% compound annual growth rate (CAGR) through 2050 (IRENA, "Future of Solar PV 2019," IRENA, 2019. Accessed: Apr. 02, 2020. [Online]. Available: https://irena.org/-/media/Files/IRENA/Agency/Publication/2019/Nov/IRENA_Future_of_Solar_PV_2019.pdf.)
* C. Murphy et al., “Electrification Futures Study: Scenarios of Power System Evolution and Infrastructure Development for the United States,” NREL, NREL/TP-6A20-72330, 1762438, MainId:6548, Jan. 2021. Accessed: Apr. 15, 2021. [Online]. Available: https://www.osti.gov/servlets/purl/1762438/
* W. J. Cole et al., “Quantifying the challenge of reaching a 100% renewable energy power system for the United States,” Joule, p. S2542435121002464, Jun. 2021, doi: 10.1016/j.joule.2021.05.011.
* Any other MW/year projection (annual not cumulative)

Module Baselines
~~~~~~~~~~~~~~~~~~
Average annual efficiency in % from:
1. G. F. Nemet, “Beyond the learning curve: factors influencing cost reductions in photovoltaics,” Energy Policy, vol. 34, no. 17, pp. 3218–3232, Nov. 2006, doi: 10.1016/j.enpol.2005.06.020.
2. M. Fischer, M. Woodhouse, S. Herritsch, and J. Trube, “International Technology Roadmap for Photovoltaic (ITRPV) 2019 Results,” ITRPV, Apr. 2020. Accessed: Aug. 25, 2020. [Online]. Available: https://itrpv.vdma.org/
3. “International Technology Roadmap for Photovoltiac (ITRPV): 2020 Results,” VDMA, ITRPV, Apr. 2021. Accessed: Apr. 30, 2021. [Online]. Available: https://itrpv.vdma.org/documents/27094228/29066965/2021%30ITRPV/08ccda3a-585e-6a58-6afa-6c20e436cf41

Degradation rate (in percentage power loss per year) from: 
(D. C. Jordan, S. R. Kurtz, K. VanSant, and J. Newmiller, "Compendium of photovoltaic degradation rates," Progress in Photovoltaics: Research and Applications, vol. 24, no. 7, pp. 978–989, 2016, doi: 10.1002/pip.2744.)

Failure probability data, i.e. T50 and T90, in years from:
(D. C. Jordan, B. Marion, C. Deline, T. Barnes, and M. Bolinger, "PV field reliability status - Analysis of 100 000 solar systems," Progress in Photovoltaics: Research and Applications, vol. n/a, no. n/a, Feb. 2020, doi: 10.1002/pip.3262.)

Module lifetime, representing the economic project life in years from:
(R. Wiser, M. Bolinger, and J. Seel, “Benchmarking Utility-Scale PV Operational Expenses and Project Lifetimes: Results from a Survey of U.S. Solar Industry Professionals,” None, 1631678, ark:/13030/qt2pd8608q, Jun. 2020. doi: 10.2172/1631678.)

Material Baselines
~~~~~~~~~~~~~~~~~~~~

Glass
^^^^^^^
The ITRPV Results Reports for 2010 and forward provided glass thickness data, and where report data was missing, reasonable assumptions or interpolations were made. See jupyter journal "Glass per M2 Calculations" for each year's calculations, and SupportingMaterial Glass_FrontThickness_ITRPV and Module_Conformation_ITRPV files for extracted data ("ITRPV - VDMA." https://itrpv.vdma.org/).

Silicon
^^^^^^^^
See Jupyter Journal "(baseline development) Silicon per m2" for calculations
1. All ITRPV reports 2010 and forward
2. G. P. Willeke, “The Fraunhofer ISE roadmap for crystalline silicon solar cell technology,” in Conference Record of the Twenty-Ninth IEEE Photovoltaic Specialists Conference, 2002., May 2002, pp. 53–57. doi: 10.1109/PVSC.2002.1190454.
3. W. C. Sinke, “A Strategic Research Agenda for Photovoltaic Solar Energy Technology - Research and development in support of realizing the Vision for Photovoltaic Technology,” EU PV Technology Platform, Working Group 3, Oct. 2007. Accessed: Oct. 22, 2020. [Online]. Available: https://ec.europa.eu/jrc/en/publication/eur-scientific-and-technical-research-reports/strategic-research-agenda-photovoltaic-solar-energy-technology-research-and-development
4. X. Sun, “Solar PV module technology market report 2020,” Wood Mackenzie Power & Renewables, 2020.
5. M. A. Green, “Photovoltaics: technology overview,” Energy Policy, vol. 28, no. 14, pp. 989–998, Nov. 2000, doi: 10.1016/S0301-4215(00)00086-0.
6. “Different Wafer Sizes.” https://sinovoltaics.com/learning-center/solar-cells/different-wafer-sizes/ (accessed Oct. 19, 2020).
7. G. Barbose and N. Darghouth, “Tracking the Sun 2019,” LBNL, Oct. 2019. Accessed: Aug. 13, 2020. [Online]. Available: https://emp.lbl.gov/sites/default/files/tracking_the_sun_2019_report.pdf
8. M. Bolinger, J. Seel, and D. Robson, “Utility-Scale Solar 2019,” LBNL, Dec. 2019. Accessed: Aug. 13, 2020. [Online]. Available: https://emp.lbl.gov/sites/default/files/lbnl_utility_scale_solar_2019_edition_final.pdf
9. D. Costello and P. Rappaport, “The Technological and Economic Development of Photovoltaics,” Annu. Rev. Energy., vol. 5, no. 1, pp. 335–356, Nov. 1980, doi: 10.1146/annurev.eg.05.110180.002003.
10. P. Mints, “SPV Market Research: March 2020 Update.” SPV Market Research, Mar. 2020.
11. P. D. Maycock and P. O. Box, “INTERNATIONAL PHOTOVOLTAIC MARKETS, DEVELOPMENTS AND TRENDS FORECAST TO 2010,” p. 8, 1993.
12. P. D. Maycock, “World Photovoltaic Markets,” in Practical Handbook of Photovoltaics, Elsevier, 2003, pp. 887–912. doi: 10.1016/B978-185617390-2/50039-8.
13. P. D. Maycock, “PV review: World Solar PV market continues explosive growth,” Refocus, vol. 6, no. 5, pp. 18–22, Sep. 2005, doi: 10.1016/S1471-0846(05)70452-2.

Silver
^^^^^^^
See Jupyer Journal "(baseline development) Silver per m2" for calculations
1. G. J. M. Phylipsen and E. A. Alsema, “Environmental life-cycle assessment of multicrystalline silicon solar cell modules,” Netherlands Agency for Energy and the Environment,NOVEM, Netherlands, Sep. 1995.
2. All ITRPV reports 2010 and forward.

Copper (Encapsulated)
^^^^^^^^^^^^^^^^^^^^^^
See Jupyer Journal "(baseline development) Copper per module m2" for calculations
1. “Standard PV Ribbon Datasheet.” Ulbrich Solar Technologies. Accessed: Jan. 14, 2021. [Online]. Available: https://www.pvribbon.com/wp-content/uploads/Datasheets/SPR_Datasheet.pdf
2. All ITRPV reports 2010 and forward
***Under Development to better account for busbars, tabs, and wire technology***

Aluminum Frames
^^^^^^^^^^^^^^^^
See Jupyter Journal "(baseline development) Aluminum Frames per m2" for calculations
1. J. R. Peeters, D. Altamirano, W. Dewulf, and J. R. Duflou, “Forecasting the composition of emerging waste streams with sensitivity analysis: A case study for photovoltaic (PV) panels in Flanders,” Resources, Conservation and Recycling, vol. 120, pp. 14–26, May 2017, doi: 10.1016/j.resconrec.2017.01.001.
2. All ITRPV 2010 and forward

Encapsulants
^^^^^^^^^^^^^^
See Jupyter Journal "(baseline development) Encapsulants and Backsheets" for calculations
1. All ITRPV 2010 and forward

Backsheets
^^^^^^^^^^^
***Under Development***
See Jupyter Journal "(baseline development) Encapsulants and Backsheets" for calculations
1. All ITRPV 2010 and forward

Data: Energy
=============

The energy flows are based on the tracked mass flows with units of energy per mass basis. As with the mass flows and to the best of our ability, the energy flows are sourced from real world values and literature, are dynamic to the annual level, and granular to specific processes. Below the variables are defined and their mass counterparts identified. For modules and each material, references used for creating the energy flow are listed as well.

baseline_energy_module
~~~~~~~~~~~~~~~~~~~~~~~~
year : int
Year. 

e_mod_MFG [kWh/m^2]: float
The energy associated with the module level processes in manufacturing, including . Anything not captured in this energy is captured at the material level.

e_mod_Install [kWh/m^2]: float 
The energy assiciated with transporting the completed module to the installation site, and energies required to prepare the site and mount the panel.

e_mod_OandM [kWh/m^2]: float
Energies associated with operation and maintenance of a PV site. This includes truck trips for maintenance, and any overnight energy required by the site. This can be set to 0 if desired.

e_mod_Repair [kWh/m^2]: float
Energy required to complete an in-field, on-site repair to a module. This includes truck trips, and cumulative embodied energy of standard replacement parts (ex: junction box, backsheet tape).

e_mod_MerchantTail [kWh/m^2]: float
For the reuse pathway "Merchant Tail", this implies the module is not removed from the site at EoL and continues to generate energy. The energy associated with this reuse pathway is 0, and this variable is to account for the "benefit" of reuse in place.

e_mod_Demount [kWh/m^2]: float
At EoL, modules must be removed from the site, regardless of their final disposition. This is the energy associated with demounting PV modules for EoL disposition. It includes truck trips and tooling needs.

e_mod_Landfill [kWh/m^2]: float
The energy associated with transporting the modules to the nearest landfill. Truck trips or potentially train container trips are included in this energy.

e_mod_CollectedDisposition [kWh/m^2]: float
For modules not sent straight to the landfill, they are considered "collected" in the mass flow to be actively dispositioned at EoL. This energy accounts for truck trips to a sorting facility, flash tester energy to power test unbroken modules, and any other sorting energies.

e_mod_Resell [kWh/m^2]: float
The reuse pathway "resell" implies reuse on the 2ndary market, where a module is removed from the field, tested, and deemed sufficiently functional (>250W or >125W/m^2 of a 2 m^2 module) for resale. Currently, used modules from the USA are being sold out of country. Therefore, this energy value includes energy for minor repairs or testing, cleaning and packaging, and international shipping via container ship.

e_mod_Remanufacture [kWh/m^2]: float
Modules which do not pass the collection/disposition flash test (<250W or <125/m^2 of a 2 m^2 module) OR are partially broken (ex: broken frame, cracked backsheet, bad junction box) may have the ability to recover still functional components, such as the glass or silicon cells, for direct reuse in manufacturing - i.e. remanufacture. This energy includes the energy associated with separating the targeted material from the rest of the module.

e_mod_Recycled [kWh/m^2]: float
Modules which are sent for recycling. This energy value includes module level recycling process energies, such as removing frames, crushing, grinding and physical separation of materials. Each material then has recycling energy associated with individual material recovery and refinement. 

baseline_energy_material
~~~~~~~~~~~~~~~~~~~~~~~~~~~
e_mat_extraction [kWh/kg]: float
	Energies associated with mining and extracting the material to a base level market available product (ex: MG-Si, silver bars)

e_mat_refinement [kWh/kg]: float
	Energies associated with turning the base level material product into the component or material composition used in PV manufacturing. This includes further purification steps as well as processing. These steps are particular to each material (ex: silicon from MG-Si to 9N Si, silver bar to silver paste). This includes the cumulative embodied energy of all non-tracked but process necessary materials, such as solvents, additives, in addition to all production steps required to generate the PV material product.

e_mat_MFG [kWh/kg]: float
	Energies associated with the material specificstep of a PV manufacturing line. This includes the equipment energy as well as the cumulative embodied energy of process necessary materials such as solvents. (ex: screen printing silver, IPA/acetone cleaning solvents)

e_mat_MFGScrap_Landfill [kWh/kg]: float
	The energy associated with landfilling the manufacturing scrap material. This includes truck trip to the landfill.

e_mat_MFGScrap_LQ [kWh/kg]: float
	The energy associated with recycling the MFG scrap to a low quality. This is the lowest energy level of recycling for a material. This includes all material specific processing and refining to return it to base level market available product.

e_mat_MFGScrap_HQ [kWh/kg]: float
	The energy associated with the refinement steps necessary to take the base level market product to a higher purity/quality such that it could be reused for PV Manufacturing or in a comparable alternate use (ex: computer chips). This energy is additive to e_mat_MFGScrap_LQ. 

e_mat_MFGScrap_HQ4MFG [kWh/kg]: float
	The energy associated with making the refined material into the PV specific material for PV Manufacturing. This energy is additive to e_mat_MFGScrap_LQ and e_mat_MFGScrap_HQ. ***SHOULD THIS BE DIFFERENT THAN HQ?***

e_mat_EoL_Remanufacture [kWh/kg]: float
	The energy associated with cleaning and prepping the material targeted for remanufacture such that it can be directly reused in MFG.

e_mat_RecycleScrap_Landfilled [kWh/kg]: float
	The energy associated with landfilling the inefficiencies from the material recycling process. This inlcudes truck trip to the landfill.

e_mat_Recycled_LQ [kWh/kg]: float
	The energy required to recycle the EoL material to a base level market available product. This includes process energy as well as cumulative embodied energy of process necessary non-tracked materials like solvents.

e_mat_Recycled_HQ [kWh/kg]:float
	The energy associated with the refinement steps necessary to take the base level market product to a higher purity/quality such that it could be reused for PV Manufacturing or in a comparable alternate use (ex: computer chips). This energy is additive to e_mat_Recycled_LQ. 

e_mat_Recycled_HQ4MFG [kWh/kg]: float
	The energy associated with making the refined material into the PV specific material for PV Manufacturing. This energy is additive to e_mat_Recycled_LQ and e_mat_Recycled_HQ. ***SHOULD THIS BE DIFFERENT THAN HQ?***


Energy Data References
---------------------

Module Energies
~~~~~~~~~~~~~~~~~
Module Manufacturing Energies from:
1. G. J. M. Phylipsen and E. A. Alsema, “Environmental life-cycle assessment of multicrystalline silicon solar cell modules,” Netherlands Agency for Energy and the Environment,NOVEM, Netherlands, Sep. 1995.
2. 

Material Energies
~~~~~~~~~~~~~~~~~~
Glass
^^^^^^^


Silicon
^^^^^^^^^


Silver
^^^^^^^^


Copper
^^^^^^^^


Aluminum Frames
^^^^^^^^^^^^^^^^


Encapsulants
^^^^^^^^^^^^^^


Backsheets
^^^^^^^^^^^


