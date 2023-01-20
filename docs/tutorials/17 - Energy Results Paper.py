#!/usr/bin/env python
# coding: utf-8

# # Energy Analysis
# We will be using the new energy layer to analyze the following future PV options
# - SHJ
# - Perovskite (tandem?)
# - 50-year PERC module (multiple uses)
# - Recycled Si PERC (Fraunhofer)
# - Cheap crap module
# - CdTe?
# 
# We will use a literture-sourced global scale deployment schedule through 2050, then assume that capacity increases at a lower constant rate through 2100.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (10, 6)

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'EnergyAnalysis')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


#creating scenarios for identical power of multiple technologies
scennames = ['PV_ICE','PERC_50','SHJ','Perovskite','RecycledPERC']#,'CheapCrap','Repowered'] #
MATERIALS = ['glass','silver','silicon', 'copper', 'aluminium_frames'] #'encapsulant', 'backsheet',
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# We will be deploying based on power (not area) because each of these have different efficiencies, and those differences should be accounted for in the simulation. Additionally, we will run the installation compensation to simulate the required replacements for each module type.

# In[3]:


#load in a baseline and materials for modification
import PV_ICE

sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames:
    sim1.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim1.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# ## Module Types Creation
# Starting modifications in 2022, using PV ICE baseline as historical for all modules
# 
# **NOTE: Currently have to modify all scenarios before extending the years to avoid errors.**
# 
# **NOTE: all dynamic values changed with PV ICE modify functions must feed in a Pandas Series**

# In[4]:


sim1.scenario.keys()


# In[5]:


celltech_modeff = pd.read_csv(os.path.join(supportMatfolder, 'output-celltech-modeffimprovements.csv'),index_col=0) #pull in module eff
celltech_aguse = pd.read_csv(os.path.join(supportMatfolder, 'output-celltech-Agusageimprovements.csv'),index_col=0) #pull in Ag use


# In[6]:


#glass-glass package mass per area calculation
#ITRPV 2022 Figs 36 and 38, we are assuming that the front and back glass heave equal thickness of 2.5mm
density_glass = 2500*1000 # g/m^3 
glassperm2 = (2.5/1000)* 2 * density_glass
print('The mass per module area of glass is '+str(glassperm2)+' g/m^2 for all modules with a glass-glass package')


# In[7]:


#time shift for modifications


# In[8]:


sim_start_year = sim1.scenario['Perovskite'].dataIn_m.iloc[0,0]
mod_start_year = 2022
timeshift = mod_start_year - sim_start_year
print('Time shift: '+str(timeshift))


# In[ ]:





# ### PERC_50
# This module represents current PERC technology (so good efficiency) if it were to have it's lifetime extended significantly. Glass-glass technology is assumed, expected decreases in silver usage and increases in module efficiency are derived from Zhang et al 2021, Gervais et al 2021 and ITRPV 2022. It is assumed that this module is no more recyclable than current technology (downcycle glass and recycle aluminium frames).

# In[9]:


#module efficiency modify for PERC
sim1.modifyScenario('PERC_50', 'mod_eff', celltech_modeff.loc[2022:,'PERC'], start_year=2022) #changing module eff


# In[10]:


#silver modify for PERC
sim1.scenario['PERC_50'].modifyMaterials('silver', 'mat_massperm2', celltech_aguse.loc[2022:,'PERC'], start_year=2022)
#old way
#sim1.scenario['PERC_50'].material['silver'].matdataIn_m.loc[timeshift:,'mat_massperm2'] = celltech_aguse.loc[2022:,'PERC'].values


# In[11]:


#modify package to glass glass
sim1.scenario['PERC_50'].modifyMaterials('glass', 'mat_massperm2', glassperm2, start_year=2022) #


# In[12]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('PERC_50', 'mod_degradation', 0.445, start_year=2022) #annual power degradation to reach 80% at 50 yrs
#T50
sim1.modifyScenario('PERC_50', 'mod_reliability_t50', 56.07, start_year=2022)
#t90
sim1.modifyScenario('PERC_50', 'mod_reliability_t90', 59.15, start_year=2022) 
#Mod Project Lifetime
sim1.modifyScenario('PERC_50', 'mod_lifetime', 50, start_year=2022) #project lifetime of 50 years


# In[13]:


#Merchant Tail set high
sim1.modifyScenario('PERC_50', 'mod_MerchantTail', 100, start_year=2022) #all installations stay for merchant tail
#Change recycling?


# In[ ]:





# ### SHJ
# This is a modern SHJ module with expected silver and module efficiency improvements taken from Zhang et al 2021, Gervais et al 2021, and ITPRV 2022. See PERC vs SHJ vs TOPCon for a more detailed evaluation.

# In[14]:


#module efficiency modify for PERC
sim1.modifyScenario('SHJ', 'mod_eff', celltech_modeff.loc[2022:,'SHJ'], start_year=2022) #changing module eff
#sim1.scenario['SHJ'].dataIn_m.loc[timeshift:,'mod_eff'] = celltech_modeff.loc[2022:,'SHJ'].values


# In[15]:


#modify silver usage for SHJ
sim1.scenario['SHJ'].modifyMaterials('silver', 'mat_massperm2', celltech_aguse.loc[2022:,'SHJ'], start_year=2022)


# In[16]:


#modify package to glass glass
sim1.scenario['SHJ'].modifyMaterials('glass', 'mat_massperm2', glassperm2, start_year=2022)


# In[17]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('SHJ', 'mod_degradation', 0.5, start_year=2022) #annual power degradation
#Mod Project Lifetime
sim1.modifyScenario('SHJ', 'mod_lifetime', 30, start_year=2022) #project lifetime of 30 years
#T50
sim1.modifyScenario('SHJ', 'mod_reliability_t50', 28, start_year=2022)
#t90
sim1.modifyScenario('SHJ', 'mod_reliability_t90', 33, start_year=2022) 


# In[18]:


#Merchant Tail set high
sim1.modifyScenario('SHJ', 'mod_MerchantTail', 50, start_year=2022) #50% stay for merchant tail, possibly change to DYNAMIC
#recycling?!?!


# In[ ]:





# ### Perovskite
# This perovskite module uses current best module and cell efficiencies, has a prospective life of 15 years and 1.5% degradation rate, and is highly circular. This is a best case scenario for perovskites given current data.

# In[19]:


#2022 module eff = 17.9% #https://www.nrel.gov/pv/assets/pdfs/champion-module-efficiencies-rev220401b.pdf
#2050 module eff = 32.5% # https://www.nrel.gov/pv/assets/pdfs/best-research-cell-efficiencies.pdf
idx_perovskite_eff = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
df_perovskite_eff = pd.DataFrame(index=idx_perovskite_eff, columns=['mod_eff_p'], dtype=float)
df_perovskite_eff.loc[2022] = 17.9
df_perovskite_eff.loc[2050] = 32.5
df_perovskite_eff.interpolate(inplace=True)


# In[20]:


#module efficiency modify for PERC
sim1.modifyScenario('Perovskite', 'mod_eff', df_perovskite_eff['mod_eff_p'], start_year=2022) #changing module eff


# In[21]:


#modify package to glass glass
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_massperm2', glassperm2, start_year=2022)


# In[22]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('Perovskite', 'mod_degradation', 1.5, start_year=2022) #annual power degradation
#Mod Project Lifetime
sim1.modifyScenario('Perovskite', 'mod_lifetime', 15, start_year=2022) #project lifetime of 30 years
#T50
sim1.modifyScenario('Perovskite', 'mod_reliability_t50', 19, start_year=2022)
#t90
sim1.modifyScenario('Perovskite', 'mod_reliability_t90', 23, start_year=2022) 


# In[23]:


#As Circular as possible
#100% collection rate
sim1.modifyScenario('Perovskite', 'mod_EOL_collection_eff', 100, start_year=2022) #100% collection
sim1.modifyScenario('Perovskite', 'mod_EOL_pg1_landfill', 0.0, start_year=2022) #100% collection
sim1.modifyScenario('Perovskite', 'mod_EOL_pb1_landfill', 0.0, start_year=2022) #100% collection

# remanufacturing
sim1.modifyScenario('Perovskite', 'mod_EOL_pg3_reMFG', 100, start_year=2022) #all modules attempt remfg
sim1.modifyScenario('Perovskite', 'mod_EOL_sp_reMFG_recycle', 100, start_year=2022) # recycle if can't remfg
sim1.modifyScenario('Perovskite', 'mod_EOL_pb3_reMFG', 100, start_year=2022) # remfg bad mods too
sim1.modifyScenario('Perovskite', 'mod_EOL_reMFG_yield', 98, start_year=2022) # REMFG YIELD 98%

#set all other paths to 0
sim1.modifyScenario('Perovskite', 'mod_EOL_pg0_resell', 0.0, start_year=2022) # REMFG YIELD 98%
sim1.modifyScenario('Perovskite', 'mod_EOL_pg1_landfill', 0.0, start_year=2022) # REMFG YIELD 98%
sim1.modifyScenario('Perovskite', 'mod_EOL_pg4_recycled', 0.0, start_year=2022) # REMFG YIELD 98%
sim1.modifyScenario('Perovskite', 'mod_EOL_pb1_landfill', 0.0, start_year=2022) # REMFG YIELD 98%
sim1.modifyScenario('Perovskite', 'mod_EOL_pb2_stored', 0.0, start_year=2022) # REMFG YIELD 98%
sim1.modifyScenario('Perovskite', 'mod_EOL_pb4_recycled', 0.0, start_year=2022) # REMFG YIELD 98%


#Material Remanufacture
#Glass
#mfg scrap
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022) #send mfg scrap to recycle
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_MFG_scrap_Recycling_eff', 99.0, start_year=2022) #99% yield
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0, start_year=2022) #closed-loop
#eol
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_PG3_ReMFG_target', 100.0, start_year=2022) #send all to remfg
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_PG4_Recycling_target', 0.0, start_year=2022) #send none to recycle
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_ReMFG_yield', 99.0, start_year=2022) #99% yeild

#silicon Remanufacture or recycle?
#mfg scrap
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022) #send mfg scrap to recycle
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycling_eff', 98.0, start_year=2022) #98% yield
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0, start_year=2022) #closed-loop
#eol
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_PG3_ReMFG_target', 0.0, start_year=2022) #send to recycle
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_PG4_Recycling_target', 100.0, start_year=2022) #send to recycle
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_Recycling_yield', 98.0, start_year=2022) #99% yeild
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_EOL_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_EOL_RecycledHQ_Reused4MFG', 100.0, start_year=2022) #closed-loop

#aluminium_frames recycle
#mfg scrap
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022) #send mfg scrap to recycle
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycling_eff', 99.0, start_year=2022) #98% yield
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0, start_year=2022) #closed-loop
#eol
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_PG3_ReMFG_target', 0.0, start_year=2022) #send to recycle
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_PG4_Recycling_target', 100.0, start_year=2022) #send to recycle
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_Recycling_yield', 99.0, start_year=2022) #99% yeild
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_EOL_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_EOL_RecycledHQ_Reused4MFG', 100.0, start_year=2022) #closed-loop


# In[ ]:





# #### Recycled PERC
# This module is based on the recent test from Fraunhofer ISE in which an old module was dissassembled, and the silicon wafer cleaned, put into a Cz ingot growth process and made using standard PERC processing, creating a 19% efficient module.
# https://www.ise.fraunhofer.de/en/press-media/press-releases/2022/solar-cells-from-recycled-silicon.html

# In[24]:


#https://www.ise.fraunhofer.de/en/press-media/press-releases/2022/solar-cells-from-recycled-silicon.html
#lets assume this gets slightly better over time
idx_RePerc_eff = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
df_RePerc_eff = pd.DataFrame(index=idx_RePerc_eff, columns=['mod_eff_RePerc'], dtype=float)
df_RePerc_eff.loc[2022] = 19.7
df_RePerc_eff.loc[2050] = 22.2
df_RePerc_eff.interpolate(inplace=True)


# In[25]:


#module efficiency
sim1.modifyScenario('RecycledPERC', 'mod_eff', df_RePerc_eff['mod_eff_RePerc'], start_year=2022)


# In[26]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('RecycledPERC', 'mod_degradation', 0.8, start_year=2022) #slightly higher than current std
#Mod Project Lifetime
sim1.modifyScenario('RecycledPERC', 'mod_lifetime', 20, start_year=2022) #project lifetime of 20 years
#T50
sim1.modifyScenario('RecycledPERC', 'mod_reliability_t50', 21, start_year=2022)
#t90
sim1.modifyScenario('RecycledPERC', 'mod_reliability_t90', 26, start_year=2022) 


# In[ ]:





# In[27]:


#silicon recycled
#mfg scrap
sim1.scenario['RecycledPERC'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022) #send mfg scrap to recycle
sim1.scenario['RecycledPERC'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycling_eff', 98.0, start_year=2022) #98% yield
sim1.scenario['RecycledPERC'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['RecycledPERC'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0, start_year=2022) #closed-loop
#eol
sim1.scenario['RecycledPERC'].modifyMaterials('silicon', 'mat_PG3_ReMFG_target', 0.0, start_year=2022) #send to recycle
sim1.scenario['RecycledPERC'].modifyMaterials('silicon', 'mat_PG4_Recycling_target', 100.0, start_year=2022) #send to recycle
sim1.scenario['RecycledPERC'].modifyMaterials('silicon', 'mat_Recycling_yield', 98.0, start_year=2022) #99% yeild
sim1.scenario['RecycledPERC'].modifyMaterials('silicon', 'mat_EOL_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['RecycledPERC'].modifyMaterials('silicon', 'mat_EOL_RecycledHQ_Reused4MFG', 100.0, start_year=2022) #closed-loop

#aluminium_frames recycle
#mfg scrap
sim1.scenario['RecycledPERC'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022) #send mfg scrap to recycle
sim1.scenario['RecycledPERC'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycling_eff', 99.0, start_year=2022) #98% yield
sim1.scenario['RecycledPERC'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['RecycledPERC'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0, start_year=2022) #closed-loop
#eol
sim1.scenario['RecycledPERC'].modifyMaterials('aluminium_frames', 'mat_PG3_ReMFG_target', 0.0, start_year=2022) #send to recycle
sim1.scenario['RecycledPERC'].modifyMaterials('aluminium_frames', 'mat_PG4_Recycling_target', 100.0, start_year=2022) #send to recycle
sim1.scenario['RecycledPERC'].modifyMaterials('aluminium_frames', 'mat_Recycling_yield', 99.0, start_year=2022) #99% yeild
sim1.scenario['RecycledPERC'].modifyMaterials('aluminium_frames', 'mat_EOL_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['RecycledPERC'].modifyMaterials('aluminium_frames', 'mat_EOL_RecycledHQ_Reused4MFG', 100.0, start_year=2022) #closed-loop


# In[28]:


#the cool feature of this module was that the wafer was directly put into the Cz process
#therefore, we need to modify the recycling energy to reflect this
#this energy profile is output by the (baseline development) Energy Silicon Manufacturing journal.
altHQRecycle_e = pd.read_csv(os.path.join(supportMatfolder, 'output_energy_silicon_eol_recycleHQ_ALT.csv'), index_col=0)


# In[29]:


altHQRecycle_e


# In[30]:


sim1.scenario['RecycledPERC'].modifyMaterialEnergy('silicon', 'e_mat_Recycled_HQ', altHQRecycle_e.loc[2022:,'E_MFG_kWhpkg'], start_year=2022)
sim1.scenario['RecycledPERC'].modifyMaterialEnergy('silicon', 'e_mat_Recycled_HQ_fuelfraction', altHQRecycle_e.loc[2022:,'E_mfgFuelFraction'], start_year=2022)


# In[31]:


sim1.scenario['RecycledPERC'].material['silicon'].matdataIn_e.iloc[25:30,]


# In[ ]:





# In[ ]:





# #### Cheap Crap

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# #### Repowered

# In[ ]:





# In[ ]:





# In[ ]:





# ### Modify Years 2000 to 2100
# We do this after we modify the baselines to propogate the modified 2050 values forward

# In[32]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim1.trim_Years(startYear=2000, endYear=2100)


# In[33]:


#check
sim1.scenario['SHJ'].material['glass'].matdataIn_e


# ### Apply deployment curve
# For the full derivation of the deployment curve, see the "PV Installations - Global" development journal. Essentially, the projection is 2000-2021 IRENA historical installation data, 2022 through 2050 is a quadratic fit to achieve 50 TW in 2050, and from 2050 to 2100 is a linear increase to approx 60 TW based on 2000-2021 global increase in electricity capacity (219.32 GW/year).
# 
# This is the deployment curve applied to all PV technologies - however, it will be modified for each PV tech using the installation compensation method, increasing it for any replacement modules required to maintain capacity.

# In[34]:


global_projection = pd.read_csv(os.path.join(supportMatfolder,'output-globalInstallsProjection.csv'), index_col=0)

fig, ax1 = plt.subplots()

ax1.plot(global_projection['World_cum']/1e6, color='orange')
ax1.set_ylabel('Cumulative Solar Capacity [TW]', color='orange')
ax2 = ax1.twinx()
ax2.plot(global_projection['World_annual_[MWdc]']/1e6)
ax2.set_ylabel('Annual Installations [TW]')
plt.show()


# In[35]:


#deployment projection for all scenarios
sim1.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', value= global_projection['World_annual_[MWdc]'], start_year=2000)
#for scen in scennames:
#    sim1.scenario[scen].dataIn_m.loc[0:len(global_projection.index-1),'new_Installed_Capacity_[MW]'] = global_projection['World_annual_[MWdc]'].values


# In[ ]:





# # Calculate Mass flow
# Can just calc mass here (exclude energy) because we're going to immediately do Install Compensation.

# In[36]:


sim1.calculateMassFlow()


# In[37]:


ii_yearly, ii_cum = sim1.aggregateResults() #have to do this to get auto plots


# In[38]:


sim1.plotMetricResults()


# In[39]:


effective_capacity = ii_yearly.filter(like='ActiveCapacity')
plt.plot(effective_capacity)
plt.legend(scennames)
plt.ylabel('Effective Capacity [MW]')
plt.title('Effective Capacity: No Replacements')


# # Installation Compensation
# Make the installations always match up to the cumulative capacity deployment schedule. (i.e. not the PV ICE baseline)

# #### Bifacial Factors

# In[40]:


bifiFactors = {'PERC_50':0.7,
               'SHJ':0.9,
               'Perovskite': 0.0,
               'RecycledPERC':0.6,
              'PV_ICE':0.0} 

#MAY NEED TO CHANGE TO BE DYNAMIC
#              'TOPCon':0.8, # ITRPV 2022, Fig. 58
#               'Repowered':0.56


# In[41]:


#PV ICE currently set up to read in a csv of bifi factors, so generate files to read in 
idx_temp = pd.RangeIndex(start=2000,stop=2101,step=1) #create the index
df_temp = pd.DataFrame(index=idx_temp, columns=['bifi'], dtype=float)
bifiPathDict={}

for f in bifiFactors.keys(): #loop over module types
    bifi = df_temp.copy() #copy of df
    bifi['bifi'] = bifiFactors[f] #assign column
    bifipath = os.path.join(testfolder,'bifi_'+str(f)+'.csv') #create file path
    bifi.to_csv(path_or_buf=bifipath, index_label='year') #create file
    bifiPathDict[str(f)] = bifipath
    #append bifi path to dict? or list?


# In[42]:



for row in range (0,len(sim1.scenario['PV_ICE'].dataIn_m)): #loop over length of years
    for scenario in range (0, len(sim1.scenario.keys())): #loop over scenarios
        scen = list(sim1.scenario.keys())[scenario] #select the nth scenario in a list of scenarios
        Under_Installment = ( (global_projection.iloc[row,0] - sim1.scenario[scen].dataOut_m['Installed_Capacity_[W]'][row])/1000000 )  # MWATTS
        sim1.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][row] += Under_Installment
    sim1.calculateFlows(bifacialityfactors=bifiPathDict[scen]) #figure this out for multiple bifi factors


# In[43]:


cc_yearly, cc_cum = sim1.aggregateResults() #have to do this to get auto plots


# In[58]:


effective_capacity = cc_yearly.filter(like='ActiveCapacity')
plt.plot(effective_capacity)
plt.legend(scennames)
plt.ylabel('Effective Capacity [TW]')
plt.title('Effective Capacity: With Replacements')


# In[54]:


annual_installs = cc_yearly.filter(like='Installed')
plt.plot(annual_installs)
plt.legend(scennames)
plt.ylabel('Annual installed [MW]')
plt.title('Annual Installs with Replacements')


# In[57]:


cc_cum.filter(like='Installed')


# In[ ]:


annual_installs = cc_yearly.filter(like='Installed')
plt.bar(annual_installs)
plt.legend(scennames)
plt.ylabel('Annual installed [MW]')
plt.title('Annual Installs with Replacements')


# In[ ]:




