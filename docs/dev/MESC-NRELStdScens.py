#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.express as px

import PV_ICE

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'MESC-NRELStdScens')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines'/'NRELStdScenarios')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
#altBaselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'Energy_CellModuleTechCompare')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("pyplot ", plt.matplotlib.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# ### Bring in NREL Standard Scenarios data for projection
# https://scenarioviewer.nrel.gov/ download the data, save it to the NRELStdScenarios folder in baselines. 
# 
# ReEDS capacity data is cumulative, and only reports even years, so we need to data munge.

# In[3]:


stdsceninput_raw = pd.read_csv(os.path.join(inputfolder, 'StdScen23_Mid_Case_annual_national.csv'),
           skiprows=[0,1,2,4], header=[0], index_col=1)
#other scenario options:
#StdScen23_Mid_Case_NoNascent_annual_national.csv


# In[4]:


stdscen_pv_evens = stdsceninput_raw.filter(like='(MW)').filter(like='PV')


# In[5]:


#take the difference betwen even years to get annual additions from cumulative
stdscens_evens_added_cap = stdscen_pv_evens.diff()
#divide by 2 to evenly distribute across odd and even years
stdscens_added_cap = stdscens_evens_added_cap/2


# In[1]:


#now make previous odds = next year evens deployment
idx_temp = pd.RangeIndex(start=2024,stop=2051,step=1) #create the index
stdscens_added_cap_filled = stdscens_added_cap.reindex(idx_temp, method='bfill')
#stdscens_added_cap_filled


# In[7]:


#Reeds is in MWac, we're in MWdc, so multiply residential by 1.1 and utility by 1.3
stdscens_pv_filled_dc = pd.DataFrame()
stdscens_pv_filled_dc['Behind-the-meter PV capacity (MWdc)'] = stdscens_added_cap_filled['Behind-the-meter PV capacity (MW)']*1.1
stdscens_pv_filled_dc['Utility-scale PV capacity (MWdc)'] = stdscens_added_cap_filled['Utility-scale PV capacity (MW)']*1.3
stdscens_pv_filled_dc


# In[8]:


plt.plot(stdscens_pv_filled_dc)
plt.legend(stdscens_pv_filled_dc.columns)
plt.ylabel('Annual Installed Capacity\n[MWdc]')


# ### Set up PV ICE simulation using historical US installs with the NREL Std Scenarios projection
# 

# In[9]:


#c-Si
MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
moduleFile = os.path.join(baselinesfolder, 'baseline_modules_mass_US_updatedT50T90.csv')
#CdTe
MATERIALS_CdTe = ['glass_cdte','aluminium_frames_cdte', 'copper_cdte', 'encapsulant_cdte','cadmium','tellurium']
moduleFile_CdTe = os.path.join(baselinesfolder, 'baseline_modules_mass_US_CdTe.csv')


# In[10]:


sim1 = PV_ICE.Simulation(name='MESC_StdScen', path=testfolder)
scens = ['23_MidCase_cSi', '23_MidCase_CdTe']

#c-Si
sim1.createScenario(name='23_MidCase_cSi', massmodulefile=moduleFile) #create the scenario, name and mod file attach
for mat in MATERIALS:
    materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
    sim1.scenario['23_MidCase_cSi'].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS
#CdTe
sim1.createScenario(name='23_MidCase_CdTe', massmodulefile=moduleFile_CdTe) #create the scenario, name and mod file attach
for mat in MATERIALS_CdTe:
    materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
    sim1.scenario['23_MidCase_CdTe'].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS_cdte


# For future deployment in the US of c-Si and CdTe, the assumptions are:
# - all Residential will be c-Si
# - CdTe will max out at 22 GW in 2030, and c-Si will make up the remaining demand to fullfill Utility deployment
# 
# We will linearly interpolate between historical CdTe Deployment and the 22 GW in 2030.

# In[11]:


plt.plot(sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[:(2024-1995),['year','new_Installed_Capacity_[MW]']])


# In[12]:


#linearly interpolate CdTe
#estimated 2024 install = 14GW
idx_temp = pd.RangeIndex(start=2024,stop=2051,step=1) #create the index
CdTeRamp = pd.DataFrame(index=idx_temp, columns=['CdTe_deploy_[MWdc]'], dtype=float)
CdTeRamp.loc[2024] = 14000
CdTeRamp.loc[2030] = 22000
CdTeRamp_full = round(CdTeRamp.interpolate(),0)
#CdTeRamp_full


# In[13]:


#Modify the CdTe Scenario deployment schedule
sim1.modifyScenario(scenarios='23_MidCase_CdTe',stage='new_Installed_Capacity_[MW]', 
                    value=CdTeRamp_full.sum(axis=1), start_year=2024) #


# In[14]:


plt.plot(sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[:,'new_Installed_Capacity_[MW]'])
plt.ylabel('Annual Installed Capacity\n[MWdc]')


# In[15]:


#now create the silicon deployment by subtracting CdTe from the total Utility deployment, add resi
mescdeploybytech = pd.DataFrame()
utilitydeploytotal = stdscens_pv_filled_dc['Utility-scale PV capacity (MWdc)'].values
CdTedeployutility = sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[(2024-1995):,'new_Installed_Capacity_[MW]'].values
resi = stdscens_pv_filled_dc['Behind-the-meter PV capacity (MWdc)'].values
mescdeploybytech['cSi_[MWdc]'] = utilitydeploytotal-CdTedeployutility+resi
mescdeploybytech.iloc[0,0]=14000 #fix nan issue
mescdeploybytech['CdTe_[MWdc]'] = sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[(2024-1995):,'new_Installed_Capacity_[MW]'].values
mescdeploybytech.index = idx_temp


# In[16]:


plt.plot(mescdeploybytech)
plt.legend(mescdeploybytech.columns)
plt.ylabel('Annual Installed Capacity\n[MWdc]')


# In[17]:


#Modify the c-Si deployment schedule
sim1.modifyScenario(scenarios=['23_MidCase_cSi'],stage='new_Installed_Capacity_[MW]', 
                    value=mescdeploybytech['cSi_[MWdc]'], start_year=2024) #


# In[18]:


yeargraph = sim1.scenario['23_MidCase_cSi'].dataIn_m.loc[:,'year']
plt.plot(yeargraph,sim1.scenario['23_MidCase_cSi'].dataIn_m.loc[:,'new_Installed_Capacity_[MW]'], label='cSi')
plt.plot(yeargraph,sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[:,'new_Installed_Capacity_[MW]'], label='CdTe')
plt.legend()
plt.ylim(0,)
plt.xlim(1995,2050)
plt.ylabel('Annual Installed Capacity\n[MWdc]')


# ### Create High recycling scenario
# Assume high recycling = Solar Cycle ideal (Dias 2022, Renewable and Sustainable Energy Reviews)
# - modules, 75% sent to recycling
# - glass, 100% closed loop
# - aluminium frames, 100% closed loop
# - silver, 100% closed loop
# - copper, 100% closed loop
# - silicon, 100% LQ recycling
# 
# We don't need to create a high CdTe recycling scenario, already set to 100% collect and recycle.

# In[19]:


sim1.createScenario(name='23_MidCase_cSi_hiR', massmodulefile=moduleFile)
for mat in MATERIALS:
    materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
    sim1.scenario['23_MidCase_cSi_hiR'].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS

#modify deployment curve as before
sim1.modifyScenario(scenarios=['23_MidCase_cSi_hiR'],stage='new_Installed_Capacity_[MW]', 
                    value=mescdeploybytech['cSi_[MWdc]'], start_year=2024) #
#modify EoL recycling variables
#module
sim1.modifyScenario(scenarios=['23_MidCase_cSi_hiR'],stage='mod_EOL_collection_eff', value=75, start_year=2024) #collect 75%
sim1.modifyScenario(scenarios=['23_MidCase_cSi_hiR'],stage='mod_EOL_pg4_recycled', value=100, start_year=2024) #recycle all collected
sim1.modifyScenario(scenarios=['23_MidCase_cSi_hiR'],stage='mod_EOL_pb4_recycled', value=100, start_year=2024) #

#material, all become a recycling target, and send to high quality
sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('glass', 'mat_PG4_Recycling_target', 100, start_year=2024)
sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('glass', 'mat_EOL_Recycled_into_HQ', 100, start_year=2024)

sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('aluminium_frames', 'mat_PG4_Recycling_target', 100, start_year=2024)
sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('aluminium_frames', 'mat_EOL_Recycled_into_HQ', 100, start_year=2024)

sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('silver', 'mat_PG4_Recycling_target', 100, start_year=2024)
sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('silver', 'mat_EOL_Recycled_into_HQ', 100, start_year=2024)

sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('copper', 'mat_PG4_Recycling_target', 100, start_year=2024)
sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('copper', 'mat_EOL_Recycled_into_HQ', 100, start_year=2024)

sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('silicon', 'mat_PG4_Recycling_target', 100, start_year=2024)
sim1.scenario['23_MidCase_cSi_hiR'].modifyMaterials('silicon', 'mat_EOL_Recycled_into_HQ', 100, start_year=2024)


# In[20]:


#create 0 recycling scenario to calculate end of life mass demand in 2030.
sim1.createScenario(name='23_MidCase_cSi_0R', massmodulefile=moduleFile)
for mat in MATERIALS:
    materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
    sim1.scenario['23_MidCase_cSi_0R'].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS

#modify deployment curve as before
sim1.modifyScenario(scenarios=['23_MidCase_cSi_0R'],stage='new_Installed_Capacity_[MW]', 
                    value=mescdeploybytech['cSi_[MWdc]'], start_year=2024) #

#set recycling to 0, only consider EoL
sim1.scenMod_noCircularity(scenarios='23_MidCase_cSi_0R')
sim1.scenMod_PerfectManufacturing(scenarios='23_MidCase_cSi_0R')


# In[21]:


#sim1.scenario['23_MidCase_CdTe'].dataIn_m['mod_EOL_collection_eff']
#sim1.scenario['23_MidCase_cSi'].dataIn_m['mod_EOL_collection_eff']
#sim1.scenario['23_MidCase_cSi_hiR'].material['glass'].matdataIn_m.keys()


# In[ ]:





# # Run the scenarios

# In[22]:


sim1.calculateMassFlow()


# In[23]:


ii_yearly, ii_cumu = sim1.aggregateResults()


# In[24]:


sim1.plotMetricResults()


# In[25]:


recycled_by_mat = pd.DataFrame()
for mats in MATERIALS:
    recycled_by_mat[str(mats)] = sim1.scenario['23_MidCase_cSi'].material[mats].matdataOut_m['mat_EOL_Recycled_2_HQ']
for mats in MATERIALS:
    recycled_by_mat[str(mats+'_hiR')] = sim1.scenario['23_MidCase_cSi_hiR'].material[mats].matdataOut_m['mat_EOL_Recycled_2_HQ']
for mats_cdte in MATERIALS_CdTe:
    recycled_by_mat[str(mats_cdte)] = sim1.scenario['23_MidCase_CdTe'].material[mats_cdte].matdataOut_m['mat_EOL_Recycled_2_HQ']
recycled_by_mat.index = pd.RangeIndex(start=1995,stop=2051,step=1)
recycled_by_mat_tonnes = recycled_by_mat/1000000  # This is the ratio for grams to Metric tonnes
#SUM and Annual 2024-2030, 


# In[26]:


recycled_by_mat_tonnes.loc[2024:2030,]


# In[27]:


recycled_by_mat_tonnes.loc[2024:2030,'glass':'backsheet']


# In[28]:


#set plot parameters
plt.rcParams.update({'font.size': 16})


# In[29]:


plt.plot(recycled_by_mat_tonnes.loc[2024:2030,'glass':'backsheet'])
plt.ylim(0,10000)
plt.xlim(2024,2030)
plt.title('Annual End of Life Module Materials:\nc-Si Low Recycling')
plt.ylabel('EoL Module Materials\n[metric tonnes]')
plt.legend(recycled_by_mat_tonnes.columns, fontsize=14)
plt.grid()


# In[30]:


plt.plot(recycled_by_mat_tonnes.loc[2024:2030,].filter(like='_hiR'))
plt.ylim(0,10000)
plt.xlim(2024,2030)
plt.title('Annual End of Life Module Materials:\nc-Si High Recycling')
plt.ylabel('EoL Module Materials\n[metric tonnes]')
plt.legend(recycled_by_mat_tonnes.columns, fontsize=14)
plt.grid()


# In[31]:


plt.plot(recycled_by_mat_tonnes.loc[2024:2030,'glass_cdte':])
plt.ylim(0,2000)
plt.xlim(2024,2030)
plt.title('Annual End of Life Module Materials:\nCdTe')
plt.ylabel('EoL Module Materials\n[metric tonnes]')
plt.legend(recycled_by_mat_tonnes.loc[2024:2030,'glass_cdte':].columns, fontsize=14)
plt.grid()


# In[32]:


recycled_by_mat_tonnes.loc[2024:2030,].sum(axis=0)


# ## Annual Future Demand through 2030
# i.e. how much module mass is leaving the field each year 2024-2030, is the "total demand"

# In[33]:


sim1.scenario['23_MidCase_cSi'].dataOut_m.keys()


# In[34]:


sim1.scenario['23_MidCase_cSi'].material['glass'].matdataOut_m.keys()


# In[35]:


annualEoLModules_tonnes = ii_yearly.loc[2024:2030].filter(like='WasteEOL_Module')
annualEoLModules_tonnes


# In[39]:


annualEoLModules_tonnes.max().max()


# In[40]:


plt.plot(annualEoLModules_tonnes)
plt.legend(['c-Si Low Recycling','CdTe','c-Si High Recycling','c-Si No Recycling'])
plt.ylim(0,40500)
plt.xlim(2024,2030)
plt.ylabel('Annual End of Life Module Mass\n[metric tonnes]', fontsize=14)
plt.title('Annual Mass of Modules at EoL\nby Scenario')


# In[ ]:




