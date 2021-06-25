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


# In[4]:


testfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'TEMP')
baselinesfolder =  str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)
print(baselinesfolder)


# In[6]:


yearly_results = pd.read_csv(r'C:\Users\ahegedus\Documents\Open EI Data\PVSC PVICE Python Data Files to Convert to Open EI\Yearly_Results.csv')


# ## Create "PVSC_Yearly, with Source Comparison, Materials Summed.csv"

# In[41]:


yearly_source_comparison = pd.DataFrame()


# In[42]:


scenario_col = ["Today"]*(2050-1994)+["Bifacial Projection"]*(2050-1994)
yearly_source_comparison['@scenario'] = scenario_col


# In[43]:


yearly_source_comparison['@timeseries|Year'] = list(yearly_results['year'])*2


# In[69]:


virgin_material_demand_PVICE_bireduced = yearly_results['VirginStock_glass_Bifacial_ReducedInstalls'] + yearly_results['VirginStock_aluminium_frames_Bifacial_ReducedInstalls'] + yearly_results['VirginStock_silver_Bifacial_ReducedInstalls'] + yearly_results['VirginStock_silicon_Bifacial_ReducedInstalls'] + yearly_results['VirginStock_copper_Bifacial_ReducedInstalls']
yearly_source_comparison['@value|TotalVirginMaterialDemand|PV ICE Bifacial Reduced Installs#MetricTonnes'] = ["NA"]*(2050-1994) + list(virgin_material_demand_PVICE_bireduced.values)


# In[ ]:


virgin_material_demand_PVICE_bi = yearly_results['VirginStock_glass_Bifacial_SameInstalls'] + yearly_results['VirginStock_aluminium_frames_Bifacial_SameInstalls'] + yearly_results['VirginStock_silver_Bifacial_SameInstalls'] + yearly_results['VirginStock_silicon_Bifacial_SameInstalls'] + yearly_results['VirginStock_copper_Bifacial_SameInstalls']
yearly_source_comparison['@value|TotalVirginMaterialDemand|PV ICE Bifacial#MetricTonnes'] = ["NA"]*(2050-1994) + list(virgin_material_demand_PVICE_bi.values)


# In[71]:


virgin_material_demand_PVICE_today = yearly_results['VirginStock_glass_PV_ICE_Today'] + yearly_results['VirginStock_aluminium_frames_PV_ICE_Today'] + yearly_results['VirginStock_silver_PV_ICE_Today'] + yearly_results['VirginStock_silicon_PV_ICE_Today'] + yearly_results['VirginStock_copper_PV_ICE_Today']
virgin_material_demand_PVICE_bifacialproj = yearly_results['VirginStock_glass_PV_ICE_Bifacial'] + yearly_results['VirginStock_aluminium_frames_PV_ICE_Bifacial'] + yearly_results['VirginStock_silver_PV_ICE_Bifacial'] + yearly_results['VirginStock_silicon_PV_ICE_Bifacial'] + yearly_results['VirginStock_copper_PV_ICE_Bifacial']
yearly_source_comparison['@value|TotalVirginMaterialDemand|PV ICE#MetricTonnes'] = list(virgin_material_demand_PVICE_today.values) + list(virgin_material_demand_PVICE_bifacialproj.values)


# In[73]:


lit_sources = ["PV_ICE","Irena_EL","Irena_RL"]
pretty_sources = ['PV ICE','Irena EL','Irena RL']
#virign material demand cols for lit_sources
for source in lit_sources:
    virgin_material_demand_today = yearly_results['VirginStock_glass_' + source + '_Today'] + yearly_results['VirginStock_aluminium_frames_' + source + '_Today'] + yearly_results['VirginStock_silver_' + source + '_Today'] + yearly_results['VirginStock_silicon_' + source + '_Today'] + yearly_results['VirginStock_copper_' + source + '_Today']
    virgin_material_demand_bifacialproj = yearly_results['VirginStock_glass_' + source + '_Bifacial'] + yearly_results['VirginStock_aluminium_frames_' + source + '_Bifacial'] + yearly_results['VirginStock_silver_' + source + '_Bifacial'] + yearly_results['VirginStock_silicon_' + source + '_Bifacial'] + yearly_results['VirginStock_copper_' + source + '_Bifacial']
    better_source_name = pretty_sources[lit_sources.index(lit_sources[source])]
    yearly_source_comparison['@value|TotalVirginMaterialDemand|' + better_source_name + '#MetricTonnes'] = list(virgin_material_demand_today.values) + list(virgin_material_demand_bifacialproj.values)
    


# In[80]:


lit_sources = ["PV_ICE","Irena_EL","Irena_RL"]
pretty_sources = ['PV ICE','Irena EL','Irena RL']
source = "Irena_EL"
virgin_material_demand_today = yearly_results['VirginStock_glass_' + source + '_Today'] + yearly_results['VirginStock_aluminium_frames_' + source + '_Today'] + yearly_results['VirginStock_silver_' + source + '_Today'] + yearly_results['VirginStock_silicon_' + source + '_Today'] + yearly_results['VirginStock_copper_' + source + '_Today']
virgin_material_demand_bifacialproj = yearly_results['VirginStock_glass_' + source + '_Bifacial'] + yearly_results['VirginStock_aluminium_frames_' + source + '_Bifacial'] + yearly_results['VirginStock_silver_' + source + '_Bifacial'] + yearly_results['VirginStock_silicon_' + source + '_Bifacial'] + yearly_results['VirginStock_copper_' + source + '_Bifacial']
#########PROBLEM TO FIX better_source_name = pretty_sources[int(lit_sources.index(lit_sources[source]))]
yearly_source_comparison['@value|TotalVirginMaterialDemand|' + better_source_name + '#MetricTonnes'] = list(virgin_material_demand_today.values) + list(virgin_material_demand_bifacialproj.values)


# In[82]:


lit_sources[source]


# In[70]:


bifacial_scenarios = ["Bifacial_ReducedInstalls","Bifacial_SameInstalls"]


# In[ ]:


#WRITE A LOOP

