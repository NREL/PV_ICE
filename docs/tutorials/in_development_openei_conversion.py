#!/usr/bin/env python
# coding: utf-8

# # Converting output files from "11c - Electric Futures Simulations BIFACIAL (PVSC) CLEANUP" 
# ## into OpenEi format for the various graphs shown on the PVSC PVICE wiki page

# In[1]:


import PV_ICE
import numpy as np
import pandas as pd
import os,sys
from pathlib import Path


# In[2]:


testfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'TEMP')
baselinesfolder =  str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)
print(baselinesfolder)


# In[3]:


yearly_results = pd.read_csv(r'C:\Users\ahegedus\Documents\Open EI Data\PVSC PVICE Python Data Files to Convert to Open EI\CONVERT FROM THESE\Yearly_Results.csv')
cumulative_results = pd.read_csv(r'C:\Users\ahegedus\Documents\Open EI Data\PVSC PVICE Python Data Files to Convert to Open EI\CONVERT FROM THESE\PVSC_Cumulative_Results.csv')


# ## Create "PVSC_Yearly, with Source Comparison, Materials Summed.csv"

# In[4]:


yearly_source_comparison = pd.DataFrame()


# In[5]:


scenario_col = ["Today"]*(2050-1994)+["Bifacial Projection"]*(2050-1994)
yearly_source_comparison['@scenario|Module Composition Scenario'] = scenario_col


# In[6]:


yearly_source_comparison['@timeseries|Year'] = list(yearly_results['year'])*2


# ### Total Virgin Material Demand Columns

# In[7]:


virgin_material_demand_PVICE_bireduced = yearly_results['VirginStock_glass_Bifacial_ReducedInstalls'] + yearly_results['VirginStock_aluminium_frames_Bifacial_ReducedInstalls'] + yearly_results['VirginStock_silver_Bifacial_ReducedInstalls'] + yearly_results['VirginStock_silicon_Bifacial_ReducedInstalls'] + yearly_results['VirginStock_copper_Bifacial_ReducedInstalls']
yearly_source_comparison['@value|TotalVirginMaterialDemand|PV ICE Bifacial Reduced Installs#MetricTonnes'] = ["NA"]*(2050-1994) + list(virgin_material_demand_PVICE_bireduced.values)


# In[8]:


virgin_material_demand_PVICE_bi = yearly_results['VirginStock_glass_Bifacial_SameInstalls'] + yearly_results['VirginStock_aluminium_frames_Bifacial_SameInstalls'] + yearly_results['VirginStock_silver_Bifacial_SameInstalls'] + yearly_results['VirginStock_silicon_Bifacial_SameInstalls'] + yearly_results['VirginStock_copper_Bifacial_SameInstalls']
yearly_source_comparison['@value|TotalVirginMaterialDemand|PV ICE Bifacial#MetricTonnes'] = ["NA"]*(2050-1994) + list(virgin_material_demand_PVICE_bi.values)


# In[9]:


virgin_material_demand_PVICE_today = yearly_results['VirginStock_glass_PV_ICE_Today'] + yearly_results['VirginStock_aluminium_frames_PV_ICE_Today'] + yearly_results['VirginStock_silver_PV_ICE_Today'] + yearly_results['VirginStock_silicon_PV_ICE_Today'] + yearly_results['VirginStock_copper_PV_ICE_Today']
virgin_material_demand_PVICE_bifacialproj = yearly_results['VirginStock_glass_PV_ICE_Bifacial'] + yearly_results['VirginStock_aluminium_frames_PV_ICE_Bifacial'] + yearly_results['VirginStock_silver_PV_ICE_Bifacial'] + yearly_results['VirginStock_silicon_PV_ICE_Bifacial'] + yearly_results['VirginStock_copper_PV_ICE_Bifacial']
yearly_source_comparison['@value|TotalVirginMaterialDemand|PV ICE#MetricTonnes'] = list(virgin_material_demand_PVICE_today.values) + list(virgin_material_demand_PVICE_bifacialproj.values)


# In[10]:


lit_sources = ["PV_ICE","Irena_EL","Irena_RL"]
pretty_sources = ['PV ICE','Irena EL','Irena RL']
#virgin material demand cols for lit_sources
for source in lit_sources:
    virgin_material_demand_today = yearly_results['VirginStock_glass_' + source + '_Today'] + yearly_results['VirginStock_aluminium_frames_' + source + '_Today'] + yearly_results['VirginStock_silver_' + source + '_Today'] + yearly_results['VirginStock_silicon_' + source + '_Today'] + yearly_results['VirginStock_copper_' + source + '_Today']
    virgin_material_demand_bifacialproj = yearly_results['VirginStock_glass_' + source + '_Bifacial'] + yearly_results['VirginStock_aluminium_frames_' + source + '_Bifacial'] + yearly_results['VirginStock_silver_' + source + '_Bifacial'] + yearly_results['VirginStock_silicon_' + source + '_Bifacial'] + yearly_results['VirginStock_copper_' + source + '_Bifacial']
    better_source_name = pretty_sources[lit_sources.index(source)]
    yearly_source_comparison['@value|TotalVirginMaterialDemand|' + better_source_name + '#MetricTonnes'] = list(virgin_material_demand_today.values) + list(virgin_material_demand_bifacialproj.values)
    


# ### Total EOL Material Columns

# In[11]:


bifacial_scenarios = ["Bifacial_ReducedInstalls","Bifacial_SameInstalls"]
pretty_scenarios = ["PV ICE Bifacial Reduced Installs", "PV ICE Bifacial"]
for myscenario in bifacial_scenarios:
    total_eol_material_bifacialproj = yearly_results['Waste_EOL_glass_' + myscenario] + yearly_results['Waste_EOL_aluminium_frames_' + myscenario] + yearly_results['Waste_EOL_silver_' + myscenario] + yearly_results['Waste_EOL_silicon_' + myscenario] + yearly_results['Waste_EOL_copper_' + myscenario]
    better_scenario_name = pretty_scenarios[bifacial_scenarios.index(myscenario)]
    yearly_source_comparison['@value|TotalEOLMaterial|' + better_scenario_name + '#MetricTonnes'] = ["NA"]*(2050-1994) + list(total_eol_material_bifacialproj.values) 


# In[12]:


lit_sources = ["PV_ICE","Irena_EL","Irena_RL"]
pretty_sources = ['PV ICE','Irena EL','Irena RL']
for source in lit_sources:
    total_eol_today = yearly_results['Waste_EOL_glass_' + source + '_Today'] + yearly_results['Waste_EOL_aluminium_frames_' + source + '_Today'] + yearly_results['Waste_EOL_silver_' + source + '_Today'] + yearly_results['Waste_EOL_silicon_' + source + '_Today'] + yearly_results['Waste_EOL_copper_' + source + '_Today']
    total_eol_bifacialproj = yearly_results['Waste_EOL_glass_' + source + '_Bifacial'] + yearly_results['Waste_EOL_aluminium_frames_' + source + '_Bifacial'] + yearly_results['Waste_EOL_silver_' + source + '_Bifacial'] + yearly_results['Waste_EOL_silicon_' + source + '_Bifacial'] + yearly_results['Waste_EOL_copper_' + source + '_Bifacial']
    better_source_name = pretty_sources[lit_sources.index(source)]
    yearly_source_comparison['@value|TotalEOLMaterial|' + better_source_name + '#MetricTonnes'] = list(total_eol_today.values) + list(total_eol_bifacialproj.values)
    


# ### Manufacturing Scrap Columns

# In[13]:


bifacial_scenarios = ["Bifacial_ReducedInstalls","Bifacial_SameInstalls"]
pretty_scenarios = ["PV ICE Bifacial Reduced Installs", "PV ICE Bifacial"]
for myscenario in bifacial_scenarios:
    total_mfg_scrap_bifacialproj = yearly_results['Waste_MFG_glass_' + myscenario] + yearly_results['Waste_MFG_aluminium_frames_' + myscenario] + yearly_results['Waste_MFG_silver_' + myscenario] + yearly_results['Waste_MFG_silicon_' + myscenario] + yearly_results['Waste_MFG_copper_' + myscenario]
    better_scenario_name = pretty_scenarios[bifacial_scenarios.index(myscenario)]
    yearly_source_comparison['@value|ManufacturingScrap|' + better_scenario_name + '#MetricTonnes'] = ["NA"]*(2050-1994) + list(total_mfg_scrap_bifacialproj.values) 


# In[14]:


lit_sources = ["PV_ICE","Irena_EL","Irena_RL"]
pretty_sources = ['PV ICE','Irena EL','Irena RL']
for source in lit_sources:
    total_mfg_today = yearly_results['Waste_MFG_glass_' + source + '_Today'] + yearly_results['Waste_MFG_aluminium_frames_' + source + '_Today'] + yearly_results['Waste_MFG_silver_' + source + '_Today'] + yearly_results['Waste_MFG_silicon_' + source + '_Today'] + yearly_results['Waste_MFG_copper_' + source + '_Today']
    total_mfg_bifacialproj = yearly_results['Waste_MFG_glass_' + source + '_Bifacial'] + yearly_results['Waste_MFG_aluminium_frames_' + source + '_Bifacial'] + yearly_results['Waste_MFG_silver_' + source + '_Bifacial'] + yearly_results['Waste_MFG_silicon_' + source + '_Bifacial'] + yearly_results['Waste_MFG_copper_' + source + '_Bifacial']
    better_source_name = pretty_sources[lit_sources.index(source)]
    yearly_source_comparison['@value|ManufacturingScrap|' + better_source_name + '#MetricTonnes'] = list(total_mfg_today.values) + list(total_mfg_bifacialproj.values)


# ### Manufacturing Scrap and EOL Material Columns

# In[15]:


bifacial_scenarios = ["Bifacial_ReducedInstalls","Bifacial_SameInstalls"]
pretty_scenarios = ["PV ICE Bifacial Reduced Installs", "PV ICE Bifacial"]
for myscenario in bifacial_scenarios:
    better_scenario_name = pretty_scenarios[bifacial_scenarios.index(myscenario)]
    total_waste = yearly_source_comparison['@value|TotalEOLMaterial|' + better_scenario_name + '#MetricTonnes'] + yearly_source_comparison['@value|ManufacturingScrap|' + better_scenario_name + '#MetricTonnes']
    yearly_source_comparison['@value|ManufacturingScrapAndEOLMaterial|' + better_scenario_name + '#MetricTonnes'] = ["NA"]*(2050-1994) + list(total_waste.values)[56:] 


# In[16]:


lit_sources = ["PV_ICE","Irena_EL","Irena_RL"]
pretty_sources = ['PV ICE','Irena EL','Irena RL']
for source in lit_sources:
    better_source_name = pretty_sources[lit_sources.index(source)]
    total_waste = yearly_source_comparison['@value|TotalEOLMaterial|' + better_source_name + '#MetricTonnes'] + yearly_source_comparison['@value|ManufacturingScrap|' + better_source_name + '#MetricTonnes']
    yearly_source_comparison['@value|ManufacturingScrapAndEOLMaterial|' + better_source_name + '#MetricTonnes'] = list(total_waste.values)


# ### New Installed Capacity Columns

# In[17]:


bifacial_scenarios = ["Bifacial_ReducedInstalls","Bifacial_SameInstalls"]
pretty_scenarios = ["PV ICE Bifacial Reduced Installs", "PV ICE Bifacial"]
for myscenario in bifacial_scenarios:
    new_installs = yearly_results['new_Installed_Capacity_[MW]_' + myscenario]
    better_scenario_name = pretty_scenarios[bifacial_scenarios.index(myscenario)]
    yearly_source_comparison['@value|NewInstalledCapacity|' + better_scenario_name + '#MW'] = ["NA"]*(2050-1994) + list(new_installs.values) 


# In[18]:


lit_sources = ["PV_ICE","Irena_EL","Irena_RL"]
pretty_sources = ['PV ICE','Irena EL','Irena RL']
for source in lit_sources:
    new_installs = yearly_results['new_Installed_Capacity_[MW]_' + source]
    better_source_name = pretty_sources[lit_sources.index(source)]
    yearly_source_comparison['@value|NewInstalledCapacity|' + better_source_name + '#MW'] = list(new_installs.values) * 2


# ### Installed Capacity Columns

# In[19]:


bifacial_scenarios = ["Bifacial_ReducedInstalls","Bifacial_SameInstalls"]
pretty_scenarios = ["PV ICE Bifacial Reduced Installs", "PV ICE Bifacial"]
for myscenario in bifacial_scenarios:
    capacity = cumulative_results['Capacity_' + myscenario]
    better_scenario_name = pretty_scenarios[bifacial_scenarios.index(myscenario)]
    yearly_source_comparison['@value|InstalledCapacity|' + better_scenario_name + '#MW'] = ["NA"]*(2050-1994) + list(capacity.values) 


# In[20]:


lit_sources = ["PV_ICE","Irena_EL","Irena_RL"]
pretty_sources = ['PV ICE','Irena EL','Irena RL']
for source in lit_sources:
    capacity_today = cumulative_results['Capacity_' + source + '_Today']
    capacity_bifacialproj = cumulative_results['Capacity_' + source + '_Bifacial']
    better_source_name = pretty_sources[lit_sources.index(source)]
    yearly_source_comparison['@value|InstalledCapacity|' + better_source_name + '#MW'] = list(capacity_today.values) + list(capacity_bifacialproj.values)


# In[21]:


yearly_source_comparison['@value|InstalledCapacity|Cumulative New Installs#MW'] = cumulative_results['new_Installed_Capacity_[MW]_PV_ICE']


# In[22]:


### Save results as CSV, saves in tutorial folder
yearly_source_comparison.to_csv('New_PVSC_Yearly, with Source Comparison, Materials Summed.csv')


# ## Create "PVSC_Installed Capacity.csv"
# ### Using Capacity_Today values

# In[23]:


installed_capacity = pd.DataFrame()


# In[24]:


scenario_col = ["Bifacial Projection"]*(2050-1994)
installed_capacity['@scenario|Module Composition Scenario'] = scenario_col


# In[25]:


installed_capacity['@timeseries|Year'] = list(yearly_results['year'])


# In[26]:


bifacial_scenarios = ["Bifacial_ReducedInstalls","Bifacial_SameInstalls"]
pretty_scenarios = ["PV ICE Bifacial Reduced Installs", "PV ICE Bifacial"]
for myscenario in bifacial_scenarios:
    capacity = cumulative_results['Capacity_' + myscenario]
    better_scenario_name = pretty_scenarios[bifacial_scenarios.index(myscenario)]
    installed_capacity['@value|InstalledCapacity|' + better_scenario_name + '#MW'] = list(capacity.values) 


# In[27]:


lit_sources = ["Irena_EL","Irena_RL"]
pretty_sources = ['Irena EL','Irena RL']
for source in lit_sources:
    capacity_today = cumulative_results['Capacity_' + source + '_Today']
    better_source_name = pretty_sources[lit_sources.index(source)]
    installed_capacity['@value|InstalledCapacity|' + better_source_name + '#MW'] = list(capacity_today.values)


# In[28]:


installed_capacity['@value|InstalledCapacity|Cumulative New Installs#MW'] = cumulative_results['new_Installed_Capacity_[MW]_PV_ICE']


# In[29]:


### Save results as CSV, saves in tutorial folder
installed_capacity.to_csv('New_PVSC_Installed Capacity.csv')


# ## Create "PVSC_Cumulative Today with Decade Increments.csv"

# In[30]:


cumulative_today = pd.DataFrame()


# In[31]:


cumulative_today['@scenario|Reliability Approach'] = ["PV ICE"]*(2050-1994) + ["Irena EL"]*(2050-1994) + ["Irena RL"]*(2050-1994) + ["PV ICE with MFG Scrap"]*(2050-1994)


# In[32]:


cumulative_today['@timeseries|Year'] = list(yearly_results['year'])*4


# In[33]:


#Virgin Material Demand Columns
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    virgin_material_demand = list(cumulative_results['VirginStock_'+ mymaterial + '_PV_ICE_Today'].values) + list(cumulative_results['VirginStock_'+ mymaterial + '_Irena_EL_Today'].values) + list(cumulative_results['VirginStock_'+ mymaterial + '_Irena_RL_Today'].values) + ['NA'] * (2050-1994)
    cumulative_today['@value|VirginMaterialDemand|' + better_material_name + '#MetricTonnes'] = virgin_material_demand


# In[34]:


#EOL Material Columns
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    pv_ice_eol = cumulative_results['Waste_EOL_' + mymaterial + '_PV_ICE_Today'].values
    pv_ice_mfg = cumulative_results['Waste_MFG_' + mymaterial + '_PV_ICE_Today'].values                                        
    pv_ice_with_mfg = list(pv_ice_eol + pv_ice_mfg)
    eol_material = list(cumulative_results['Waste_EOL_' + mymaterial + '_PV_ICE_Today'].values) + list(cumulative_results['Waste_EOL_' + mymaterial + '_Irena_EL_Today'].values) + list(cumulative_results['Waste_EOL_' + mymaterial + '_Irena_RL_Today'].values) + list(pv_ice_with_mfg)
    cumulative_today['@value|EOLMaterial|' + better_material_name + '#MetricTonnes'] = eol_material


# In[35]:


#Manufacturing Scrap Columns (NA) -- not used in OpenEI
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    cumulative_today['@value|ManufacturingScrap|' + better_material_name + '#MetricTonnes'] = ["NA"] * len(cumulative_today)


# In[36]:


#Manufacturing Scrap and EOL Columns (NA) -- not used in OpenEI
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    cumulative_today['@value|ManufacturingScrapAndEOLMaterial|' + better_material_name + '#MetricTonnes'] = ["NA"] * len(cumulative_today)


# In[37]:


#New Installed Capacity (NA) -- not used in OpenEI
cumulative_today['@value|NewInstalledCapacity|PV|#MetricTonnes'] = ["NA"] * len(cumulative_today)
cumulative_today['@value|InstalledCapacity|PV|#MetricTonnes'] = ["NA"] * len(cumulative_today)


# In[ ]:


#SAVE NOW IF ALL YEARS ARE WANTED
#cumulative_today.to_csv("New_PVSC_Cumulative Today.csv")


# In[63]:


#filter for decade increments
df_new = cumulative_today.rename(columns={'@timeseries|Year':'year'})
cumulative_today = cumulative_today[df_new.year.isin([2020, 2030,2040,2050])]
cumulative_today = cumulative_today.rename(columns={'year':'@timeseries|Year'})


# In[64]:


cumulative_today.to_csv("New_PVSC_Cumulative Today with Decade Increments.csv")


# ## Create "PVSC_Cumulative Bifacial Projection with Decade Increments.csv"

# In[65]:


cumulative_bifacial = pd.DataFrame()


# In[66]:


cumulative_bifacial['@scenario|Reliability Approach'] = ["PV ICE"]*(2050-1994) + ["Irena EL"]*(2050-1994) + ["Irena RL"]*(2050-1994) + ["PV ICE with MFG Scrap"]*(2050-1994)


# In[67]:


cumulative_bifacial['@timeseries|Year'] = list(yearly_results['year'])*4


# In[68]:


#Virgin Material Demand Columns
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    virgin_material_demand = list(cumulative_results['VirginStock_'+ mymaterial + '_PV_ICE_Bifacial'].values) + list(cumulative_results['VirginStock_'+ mymaterial + '_Irena_EL_Bifacial'].values) + list(cumulative_results['VirginStock_'+ mymaterial + '_Irena_RL_Bifacial'].values) + ['NA'] * (2050-1994)
    cumulative_bifacial['@value|VirginMaterialDemand|' + better_material_name + '#MetricTonnes'] = virgin_material_demand


# In[69]:


#EOL Material Columns
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    pv_ice_eol = cumulative_results['Waste_EOL_' + mymaterial + '_PV_ICE_Bifacial'].values
    pv_ice_mfg = cumulative_results['Waste_MFG_' + mymaterial + '_PV_ICE_Bifacial'].values                                        
    pv_ice_with_mfg = list(pv_ice_eol + pv_ice_mfg)
    eol_material = list(cumulative_results['Waste_EOL_' + mymaterial + '_PV_ICE_Bifacial'].values) + list(cumulative_results['Waste_EOL_' + mymaterial + '_Irena_EL_Bifacial'].values) + list(cumulative_results['Waste_EOL_' + mymaterial + '_Irena_RL_Bifacial'].values) + list(pv_ice_with_mfg)
    cumulative_bifacial['@value|EOLMaterial|' + better_material_name + '#MetricTonnes'] = eol_material


# In[70]:


#Manufacturing Scrap Columns (NA) -- not used in OpenEI
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    cumulative_bifacial['@value|ManufacturingScrap|' + better_material_name + '#MetricTonnes'] = ["NA"] * len(cumulative_bifacial)


# In[71]:


#Manufacturing Scrap and EOL Columns (NA) -- not used in OpenEI
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    cumulative_bifacial['@value|ManufacturingScrapAndEOLMaterial|' + better_material_name + '#MetricTonnes'] = ["NA"] * len(cumulative_bifacial)


# In[72]:


#New Installed Capacity (NA) -- not used in OpenEI
cumulative_bifacial['@value|NewInstalledCapacity|PV|#MetricTonnes'] = ["NA"] * len(cumulative_bifacial)
cumulative_bifacial['@value|InstalledCapacity|PV|#MetricTonnes'] = ["NA"] * len(cumulative_bifacial)


# In[73]:


#SAVE NOW IF ALL YEARS ARE WANTED
#cumulative_bifacial.to_csv("New_PVSC_Cumulative Bifacial.csv")


# In[74]:


#filter for decade increments
df_new = cumulative_bifacial.rename(columns={'@timeseries|Year':'year'})
cumulative_bifacial = cumulative_bifacial[df_new.year.isin([2020, 2030,2040,2050])]
cumulative_bifacial = cumulative_bifacial.rename(columns={'year':'@timeseries|Year'})


# In[75]:


cumulative_bifacial.to_csv("New_PVSC_Cumulative Bifacial Projection with Decade Increments.csv")


# ### Now all CSVs are created and are ready to import to OpenEI.
