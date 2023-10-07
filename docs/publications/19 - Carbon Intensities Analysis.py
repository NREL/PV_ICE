#!/usr/bin/env python
# coding: utf-8

# # Carbon instensity of Sustainable PV for Energy Transition
# This analysis explores the carbon implications of different PV sustainability/circular economy designs in the context of achieving energy transition. These calculations build upon previous work that can be found in journals 13 and 17.
# 
# Attempt 1

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'CarbonAnalysis')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
carbonfolder = str(Path().resolve().parent.parent / 'PV_ICE'/ 'baselines'/ 'CarbonLayer')
altBaselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'Energy_CellModuleTechCompare')
energyanalysisfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'EnergyAnalysis')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


from platform import python_version 
print(python_version())


# In[3]:


import PV_ICE
PV_ICE.__version__


# In[4]:


MATERIALS = ['glass', 'silicon', 'silver', 'aluminium_frames', 'copper', 'encapsulant', 'backsheet']
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[5]:


#load in the simulation from previous journal/work
sim1 = PV_ICE.Simulation.load_Simpickle(filename=r'C:\Users\hmirletz\Documents\GitHub\PV_ICE\PV_ICE\TEMP\EnergyAnalysis\sim1.pkl')


# In[6]:


sim1.calculateCarbonFlows()


# In[7]:


sim1.scenario['r_PERC'].dataOut_c


# In[ ]:





# ## Project grid forward to 100% re in 2050
# To parallel the PV deployment, we will assume that we globally hit 100% RE in 2050 with the 75 TW of PV. As such, we need to change the future projection of marketshares of the different country grids.
# 
# One scenario with decarb grid, one scenario with decarb grid and heat
# 
# Estimating that 60-70% generation will be from Solar, 30-40% from wind, and any remainder from "other renewables"

# In[ ]:


countrygridmix = pd.read_csv(os.path.join(carbonfolder,'baseline_countrygridmix.csv'), index_col='year')
gridsources = ['Bioenergy','Hydro','Nuclear','OtherFossil','OtherRenewables','Solar','Wind']
nonRE = ['Coal','Gas','OtherFossil','Nuclear','Bioenergy']


# In[ ]:


countrygridmix.loc[2023:,:]=np.nan #delete 2023 to 2050
nonRE_search = '|'.join(nonRE) #create nonRE search
countrygridmix.loc[2050, countrygridmix.columns.str.contains(nonRE_search)] = 0.0 #set all nonRE to 0 in 2050


# In[ ]:


countrygridmix.loc[2050, countrygridmix.columns.str.contains('Solar')] = 63.0
countrygridmix.loc[2050, countrygridmix.columns.str.contains('Wind')] = 33.0
countrygridmix.loc[2050, countrygridmix.columns.str.contains('Hydro')] = 3.0
countrygridmix.loc[2050, countrygridmix.columns.str.contains('OtherRenewables')] = 1.0
#numbers derived from leading scenario electricity generation Breyer et al 2022 scenarios (EU focused)


# In[ ]:


countrygridmix_100RE2050 = countrygridmix.interpolate() 


# This is a simple projection, assumes all countries have same ratio of PV and wind (which we know can't be true). Update in future with country specific projections.

# In[ ]:


sim1.calculateCarbonFlows(countrygridmixes=countrygridmix_100RE2050)


# In[ ]:


sim1.scenario['PV_ICE'].material['encapsulant'].matdataOut_c#/test_base


# In[ ]:


mod_carbon_results = sim1.scenario['PV_ICE'].dataOut_c
mod_carbon_results


# variables which are the sum of other steps:
# - Global_Sum_gCO2eqpWh_mod_MFG_gCO2eq
# - mat_Recycle_e_p_gCO2eq (process, elec, fuel)
# - mat_vMFG_total_gCO2eq (process, elec, fuel)
# - mat_vMFG_energy_gCO2eq (elec, fuel)

# In[ ]:


for scen in scenarios:
    print(scen)
    mod_carbon_scen_results = sim1.scenario[scen].dataOut_c.add_prefix(str(scen+'_'))
    scenmatdc = pd.DataFrame()
    for mat in MATERIALS:
        print(mat)
        mat_carbon_scen_results = sim1.scenario[scen].material[mat].matdataOut_c.add_prefix(str(scen+'_'+mat+'_')) 
        scenmatdc = pd.concat([scenmatdc,mat_carbon_scen_results], axis=1) #group all material dc
    scen_carbon_results = pd.concat([mod_carbon_scen_results,scenmatdc], axis=1)


# In[ ]:


#calculation for annual carbon emissions total (selecting to avoid double countings)
mats_vmfg_total = scen_carbon_results.filter(like='total')
mats_ce_recycle = scen_carbon_results.filter(like='Recycle_e_p')
mats_ce_remfg = scen_carbon_results.filter(like='ReMFG_clean')
mats_landfill = scen_carbon_results.filter(like='landfill_total')

mod_mfg_carbon_total = scen_carbon_results.filter(like='Global_gCO2eqpwh_mod_MFG_gCO2eq')

mod_nonvMFG = ['Install','OandM','Repair','Demount','Store','Resell','ReMFG','Recycle']
nonvMFG_search = '|'.join(mod_nonvMFG) #create nonRE search
mod_carbon_sum_nonvmfg = scen_carbon_results.loc[:,scen_carbon_results.columns.str.contains(nonvMFG_search)].filter(like='mod')


# In[ ]:


scen_annual_carbon_all = pd.concat([mod_mfg_carbon_total,mod_carbon_sum_nonvmfg,
                                mats_vmfg_total,mats_ce_recycle,mats_ce_remfg,mats_landfill], axis=1)
scen_annual_carbon_all['Annual_Emit_total_gCO2eq'] = scen_annual_carbon.sum(axis=1)

scen_annual_carbon_mod = pd.concat([mod_mfg_carbon_total,mod_carbon_sum_nonvmfg], axis=1)
scen_annual_carbon_mats = pd.concat([mats_vmfg_total,mats_ce_recycle,mats_ce_remfg,mats_landfill], axis=1)


# In[ ]:


scen_annual_carbon_mats.groupby()


# In[ ]:


plt.plot(scen_annual_carbon/1e12) #meggatonnes
plt.legend(scen_annual_carbon_all.columns, bbox_to_anchor=(1.05,-0.05))
plt.title('Annual Carbon Emissions from all aspects of Mods and Mats')
plt.ylabel('Annual GHG emissions from PV Lifecycle\n[million tonnes CO2eq]')


# In[ ]:


scen_cumu_carbon = scen_annual_carbon.cumsum()


# In[ ]:


scen_cumu_carbon.loc[55,'Annual_Emit_total_gCO2eq']/1e12


# In[ ]:


scen_annual_carbon.columns


# In[ ]:





# In[ ]:




