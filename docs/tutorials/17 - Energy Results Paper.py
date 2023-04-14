#!/usr/bin/env python
# coding: utf-8

# # Energy Analysis
# We will be using the new energy layer to analyze the following future PV options
# - SHJ
# - TOPCon
# - Perovskite Tandem c-Si
# - 50-year PERC module 
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

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'EnergyAnalysis')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# Graphing settings

# In[2]:


#https://www.learnui.design/tools/data-color-picker.html#palette
#color pallette - modify here for all graphs below
colorpalette=['#003f5c','#374c80','#7a5195','#bc5090','#ef5675','#ff764a','#ffa600']
import matplotlib as mpl #import matplotlib
from cycler import cycler #import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=colorpalette) #reset the default color palette of mpl

plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.figsize'] = (8, 6)

scennames_labels = ['PV_ICE','PERC_50','High Eff','Idealized\nPerovskite\nSi-Tandem','Lightweight'
                    'SHJ','TOPCon','Recycled\nPERC','Cheap\nCrap'] #


# Scenarios and materials

# In[3]:


#creating scenarios for identical power of multiple technologies
scennames = ['PV_ICE','PERC_50','High_eff', 'Perovskite','Lightweight', #extreme cases
            'SHJ', 'TOPCon','RecycledPERC','CheapCrap'] #realistic cases
MATERIALS = ['glass','silver','silicon', 'copper', 'aluminium_frames','encapsulant', 'backsheet']
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# We will be deploying based on power (not area) because each of these have different efficiencies, and those differences should be accounted for in the simulation. Additionally, we will run the installation compensation to simulate the required replacements for each module type.

# In[4]:


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

# In[5]:


sim1.scenario.keys()


# In[6]:


celltech_modeff = pd.read_csv(os.path.join(supportMatfolder, 'output-celltech-modeffimprovements.csv'),index_col=0) #pull in module eff
celltech_aguse = pd.read_csv(os.path.join(supportMatfolder, 'output-celltech-Agusageimprovements.csv'),index_col=0) #pull in Ag use


# In[7]:


celltech_modeff.loc[2020]


# In[8]:


#glass-glass package mass per area calculation
#ITRPV 2022 Figs 36 and 38, we are assuming that the front and back glass heave equal thickness of 2.5mm
density_glass = 2500*1000 # g/m^3 
glassperm2 = (2.5/1000)* 2 * density_glass
print('The mass per module area of glass is '+str(glassperm2)+' g/m^2 for all modules with a glass-glass package')


# In[ ]:


timeshift = 2022-1995


# ## Extreme modules

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


# ### High Efficiency
# This represents a 25 year lifetime module where efficiency has been prioritized. This could represent a silicon based tandem, along the lines of SHJ 

# In[14]:


idx_temp = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
df_higheff = pd.DataFrame(index=idx_temp, columns=['mod_eff_p'], dtype=float)
df_higheff.loc[2022] = 23.5
df_higheff.loc[2030] = 26.0
df_higheff.loc[2050] = 32.0
df_higheff.interpolate(inplace=True)
#module efficiency modify for PERC
sim1.modifyScenario('High_eff', 'mod_eff', df_higheff.loc[2022:,], start_year=2022) #changing module eff


# In[15]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('High_eff', 'mod_degradation', 0.7, start_year=2022) #standard current degrdation
#T50
sim1.modifyScenario('High_eff', 'mod_reliability_t50', 25, start_year=2022)
#t90
sim1.modifyScenario('High_eff', 'mod_reliability_t90', 31, start_year=2022) 
#Mod Project Lifetime
sim1.modifyScenario('High_eff', 'mod_lifetime', 25, start_year=2022) #project lifetime of 25 years


# In[ ]:





# In[ ]:





# ### Perovskite
# This perovskite module uses current best module and cell efficiencies, has a prospective life of 15 years and 1.5% degradation rate, and is highly circular. This is a best case scenario for perovskites given current data.

# In[16]:


#2022 module eff = 17.9% #https://www.nrel.gov/pv/assets/pdfs/champion-module-efficiencies-rev220401b.pdf
#2050 module eff = 32.5% # https://www.nrel.gov/pv/assets/pdfs/best-research-cell-efficiencies.pdf
idx_perovskite_eff = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
df_perovskite_eff = pd.DataFrame(index=idx_perovskite_eff, columns=['mod_eff_p'], dtype=float)
df_perovskite_eff.loc[2022] = 17.9
df_perovskite_eff.loc[2050] = 32.5
df_perovskite_eff.interpolate(inplace=True)


# In[17]:


#module efficiency modify for PERC
sim1.modifyScenario('Perovskite', 'mod_eff', df_perovskite_eff['mod_eff_p'], start_year=2022) #changing module eff


# In[18]:


#modify package to glass glass
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_massperm2', glassperm2, start_year=2022)


# In[19]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('Perovskite', 'mod_degradation', 1.47, start_year=2022) #annual power degradation
#Mod Project Lifetime
sim1.modifyScenario('Perovskite', 'mod_lifetime', 15, start_year=2022) #project lifetime of 15 years
#T50
sim1.modifyScenario('Perovskite', 'mod_reliability_t50', 14, start_year=2022)
#t90
sim1.modifyScenario('Perovskite', 'mod_reliability_t90', 20, start_year=2022) 


# In[20]:


#As Circular as possible
#100% collection rate
sim1.modifyScenario('Perovskite', 'mod_EOL_collection_eff', 100.0, start_year=2022) #100% collection
sim1.modifyScenario('Perovskite', 'mod_EOL_pg1_landfill', 0.0, start_year=2022) #100% collection
sim1.modifyScenario('Perovskite', 'mod_EOL_pb1_landfill', 0.0, start_year=2022) #100% collection

# remanufacturing
sim1.modifyScenario('Perovskite', 'mod_EOL_pg3_reMFG', 100.0, start_year=2022) #all modules attempt remfg
sim1.modifyScenario('Perovskite', 'mod_EOL_sp_reMFG_recycle', 100.0, start_year=2022) # recycle if can't remfg
sim1.modifyScenario('Perovskite', 'mod_EOL_pb3_reMFG', 100.0, start_year=2022) # remfg bad mods too
sim1.modifyScenario('Perovskite', 'mod_EOL_reMFG_yield', 98.0, start_year=2022) # REMFG YIELD 98%

#set all other paths to 0
sim1.modifyScenario('Perovskite', 'mod_EOL_pg0_resell', 0.0, start_year=2022) # 
sim1.modifyScenario('Perovskite', 'mod_EOL_pg1_landfill', 0.0, start_year=2022) # 
sim1.modifyScenario('Perovskite', 'mod_EOL_pg2_stored', 0.0, start_year=2022) #
sim1.modifyScenario('Perovskite', 'mod_EOL_pg4_recycled', 0.0, start_year=2022) # 
sim1.modifyScenario('Perovskite', 'mod_EOL_pb1_landfill', 0.0, start_year=2022) # 
sim1.modifyScenario('Perovskite', 'mod_EOL_pb2_stored', 0.0, start_year=2022) # 
sim1.modifyScenario('Perovskite', 'mod_EOL_pb4_recycled', 0.0, start_year=2022) # 
sim1.modifyScenario('Perovskite', 'mod_Repair', 0.0, start_year=2022) #
sim1.modifyScenario('Perovskite', 'mod_MerchantTail', 0.0, start_year=2022) #


#Material Remanufacture
#Glass
#mfg scrap
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022) #send mfg scrap to recycle
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_MFG_scrap_Recycling_eff', 99.0, start_year=2022) #99% yield
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0, start_year=2022) #closed-loop
#eol
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_PG3_ReMFG_target', 100.0, start_year=2022) #send all to remfg
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_PG4_Recycling_target', 100.0, start_year=2022) #send none to recycle
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_ReMFG_yield', 99.0, start_year=2022) #99% yeild
sim1.scenario['Perovskite'].modifyMaterials('glass', 'mat_Recycling_yield', 99.0, start_year=2022) #99% yeild


#silicon Recycle (or should it be remfg?)
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
sim1.scenario['Perovskite'].modifyMaterials('silicon', 'mat_ReMFG_yield', 0.0, start_year=2022) #99% yeild

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
sim1.scenario['Perovskite'].modifyMaterials('aluminium_frames', 'mat_ReMFG_yield', 0.0, start_year=2022) #0% yeild


# ### Lightweighting
# - 10% Si
# - 50% encapsulant
# - 2mm glass
# - frameless
# - possibly reduced reliability
# 
# Could represent a thin film

# In[21]:


#module efficiency modify for PERC
sim1.modifyScenario('Lightweight', 'mod_eff', celltech_modeff.loc[2022:,'PERC'], start_year=2022) #changing module eff


# In[31]:





# In[33]:


#2mm glass calculation
lightweightglass = (2.0/1000)* 1 * density_glass

#50% encapsulant
light_encap = pd.Series(sim1.scenario['PV_ICE'].material['encapsulant'].matdataIn_m.loc[timeshift:,'mat_massperm2']*0.5)

#10% silicon
light_Si = pd.Series(sim1.scenario['PV_ICE'].material['silicon'].matdataIn_m.loc[timeshift:,'mat_massperm2']*0.1)

#modify package
sim1.scenario['Lightweight'].modifyMaterials('glass', 'mat_massperm2', lightweightglass, start_year=2022) #glass
sim1.scenario['Lightweight'].modifyMaterials('aluminium_frames', 'mat_massperm2', 0.0, start_year=2022) #frameless
sim1.scenario['Lightweight'].modifyMaterials('encapsulant', 'mat_massperm2', light_encap, start_year=2022) #50% encapsulant
sim1.scenario['Lightweight'].modifyMaterials('silicon', 'mat_massperm2', light_Si, start_year=2022) #10% silicon


# In[35]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('Lightweight', 'mod_degradation', 0.7, start_year=2022) #annual power degradation
#Mod Project Lifetime
sim1.modifyScenario('Lightweight', 'mod_lifetime', 25, start_year=2022) #project lifetime of 15 years
#T50
sim1.modifyScenario('Lightweight', 'mod_reliability_t50', 25, start_year=2022)
#t90
sim1.modifyScenario('Lightweight', 'mod_reliability_t90', 31, start_year=2022) 


# In[ ]:





# ## Evolving Realistic Modules

# ### SHJ
# This is a modern SHJ module with expected silver and module efficiency improvements taken from Zhang et al 2021, Gervais et al 2021, and ITPRV 2022. See PERC vs SHJ vs TOPCon for a more detailed evaluation.

# In[36]:


#module efficiency modify for SHJ
sim1.modifyScenario('SHJ', 'mod_eff', celltech_modeff.loc[2022:,'SHJ'], start_year=2022) #changing module eff
#sim1.scenario['SHJ'].dataIn_m.loc[timeshift:,'mod_eff'] = celltech_modeff.loc[2022:,'SHJ'].values


# In[37]:


#modify silver usage for SHJ
sim1.scenario['SHJ'].modifyMaterials('silver', 'mat_massperm2', celltech_aguse.loc[2022:,'SHJ'], start_year=2022)


# In[38]:


#modify package to glass glass
sim1.scenario['SHJ'].modifyMaterials('glass', 'mat_massperm2', glassperm2, start_year=2022)


# In[39]:


#Lifetime and Degradation
#median annual power degradation Jordan et al 2022, Table 6
idx_temp = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
df_shj_deg = pd.DataFrame(index=idx_temp, columns=['mod_deg'], dtype=float)
df_shj_deg.loc[2022] = 0.7
df_shj_deg.loc[2030] = 0.6
df_shj_deg.loc[2050] = 0.5
df_shj_deg.interpolate(inplace=True)

#degradation rate:
sim1.modifyScenario('SHJ', 'mod_degradation', df_shj_deg.loc[2022:,'mod_deg'], start_year=2022) 

#Mod Project Lifetime
df_shj_life = pd.DataFrame(index=idx_temp, columns=['mod_lifetime'], dtype=float)
df_shj_life.loc[2022] = 30
df_shj_life.loc[2030] = 35
df_shj_life.loc[2050] = 38
df_shj_life.interpolate(inplace=True)
sim1.modifyScenario('SHJ', 'mod_lifetime', df_shj_life.loc[2022:,'mod_lifetime'], start_year=2022) #

#T50
df_shj_t50 = pd.DataFrame(index=idx_temp, columns=['mod_t50'], dtype=float)
df_shj_t50.loc[2022] = 28
df_shj_t50.loc[2030] = 40
df_shj_t50.loc[2050] = 41
df_shj_t50.interpolate(inplace=True)
sim1.modifyScenario('SHJ', 'mod_reliability_t50', df_shj_t50.loc[2022:,'mod_t50'], start_year=2022)
#t90
df_shj_t90 = pd.DataFrame(index=idx_temp, columns=['mod_t90'], dtype=float)
df_shj_t90.loc[2022] = 33
df_shj_t90.loc[2030] = 44
df_shj_t90.loc[2050] = 45
df_shj_t90.interpolate(inplace=True)
sim1.modifyScenario('SHJ', 'mod_reliability_t90', df_shj_t90.loc[2022:,'mod_t90'], start_year=2022) 


# In[40]:


#Merchant Tail set high
#sim1.modifyScenario('SHJ', 'mod_MerchantTail', 50, start_year=2022) #50% stay for merchant tail, possibly change to DYNAMIC


# Improving recycling:
# - 2022: 15% collection, 75% recycled module, 100% downcycled glass, 100% HQ al frames, 20% closed loop
# - 2030: 45% collection, 80% recycled module, 45% closed-loop glass, 40% closed-loop silicon, 60% closed loop Al frames
# - 2050: 75% collection, 95% recycled module, 75% closed loop glass, 75% closed loop silicon, 100% closed loop al frames

# In[61]:


idx_temp = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
#module collection
df_shj_modcollect = pd.DataFrame(index=idx_temp, columns=['mod_collect'], dtype=float)
df_shj_modcollect.loc[2022] = 15
df_shj_modcollect.loc[2030] = 45
df_shj_modcollect.loc[2050] = 75
df_shj_modcollect.interpolate(inplace=True)
#collection
sim1.modifyScenario('SHJ', 'mod_EOL_collection_eff', df_shj_modcollect.loc[2022:,'mod_collect'], start_year=2022) #
#module recycling target
df_shj_modrecycle = pd.DataFrame(index=idx_temp, columns=['mod_recycle'], dtype=float)
df_shj_modrecycle.loc[2022] = 75
df_shj_modrecycle.loc[2030] = 80
df_shj_modrecycle.loc[2050] = 95
df_shj_modrecycle.interpolate(inplace=True)
#recycling target
sim1.modifyScenario('SHJ', 'mod_EOL_pg4_recycled', df_shj_modrecycle, start_year=2022) #

#glass 
#MFGing
#sim1.scenario['SHJ'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ', 0.0, start_year=2022) 
#EoL
#recycling target
df_shj_recycleglass_target = 100.0
sim1.scenario['SHJ'].modifyMaterials('glass', 'mat_PG4_Recycling_target', 100.0, start_year=2022)
#glass recycling yield
df_shj_recycleglass_yld = pd.DataFrame(index=idx_temp, columns=['glass_recycle_yield'], dtype=float)
df_shj_recycleglass_yld.loc[2022] = 40
df_shj_recycleglass_yld.loc[2030] = 60
df_shj_recycleglass_yld.loc[2050] = 80
df_shj_recycleglass_yld.interpolate(inplace=True)
sim1.scenario['SHJ'].modifyMaterials('glass', 'mat_Recycling_yield', df_shj_recycleglass_yld.loc[2022:,'glass_recycle_yield'], start_year=2022)
#glass to HQ
df_shj_recycleglass_HQ = pd.DataFrame(index=idx_temp, columns=['glass_recycle_HQ'], dtype=float)
df_shj_recycleglass_HQ.loc[2022] = 0
df_shj_recycleglass_HQ.loc[2030] = 100
df_shj_recycleglass_HQ.loc[2050] = 100
df_shj_recycleglass_HQ.interpolate(inplace=True)
sim1.scenario['SHJ'].modifyMaterials('glass', 'mat_EOL_Recycled_into_HQ', df_shj_recycleglass_HQ.loc[2022:,'glass_recycle_HQ'], start_year=2022)
#glass to HQCL
df_shj_recycleglass_HQCL = pd.DataFrame(index=idx_temp, columns=['glass_recycle_HQCL'], dtype=float)
df_shj_recycleglass_HQCL.loc[2022] = 0
df_shj_recycleglass_HQCL.loc[2030] = 45
df_shj_recycleglass_HQCL.loc[2050] = 75
df_shj_recycleglass_HQCL.interpolate(inplace=True)
sim1.scenario['SHJ'].modifyMaterials('glass', 'mat_EOL_RecycledHQ_Reused4MFG', df_shj_recycleglass_HQCL.loc[2022:,'glass_recycle_HQCL'], start_year=2022)

#AL frames 
#aluminium_frames recycle
#mfg scrap
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022) 
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycling_eff', 98.0, start_year=2022) #98% yield
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0, start_year=2022) #closed-loop
#eol
#no remfg
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_PG3_ReMFG_target', 0.0, start_year=2022) #send to recycle
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_ReMFG_yield', 0.0, start_year=2022) #0% yeild

#recycling target
df_shj_recyclealframe_target = 100.0
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_PG4_Recycling_target',100.0, start_year=2022) #send to recycle
#Al frame yield
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_Recycling_yield', 98.0, start_year=2022) #
#al frames to HQ
df_shj_recyclealframe_HQ = 100.0
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_EOL_Recycled_into_HQ', 100.0, start_year=2022) #all HQ
#Al frames to closed loop
df_shj_recyclealframe_HQCL = pd.DataFrame(index=idx_temp, columns=['al_frames_recycle_HQCL'], dtype=float)
df_shj_recyclealframe_HQCL.loc[2022] = 20
df_shj_recyclealframe_HQCL.loc[2030] = 60
df_shj_recyclealframe_HQCL.loc[2050] = 100
df_shj_recyclealframe_HQCL.interpolate(inplace=True)
sim1.scenario['SHJ'].modifyMaterials('aluminium_frames', 'mat_EOL_RecycledHQ_Reused4MFG', df_shj_recyclealframe_HQCL.loc[2022:,'al_frames_recycle_HQCL'], start_year=2022) #closed-loop

#silicon 
#MFGing
#EoL
#recycling target
df_shj_recycleSi_target = pd.DataFrame(index=idx_temp, columns=['si_recycled'], dtype=float)
df_shj_recycleSi_target.loc[2022] = 20
df_shj_recycleSi_target.loc[2030] = 100
df_shj_recycleSi_target.loc[2050] = 100
df_shj_recycleSi_target.interpolate(inplace=True)
sim1.scenario['SHJ'].modifyMaterials('silicon', 'mat_PG4_Recycling_target', df_shj_recycleSi_target.loc[2022:,'si_recycled'], start_year=2022)
#recycling yield
sim1.scenario['SHJ'].modifyMaterials('silicon', 'mat_Recycling_yield', 90.0, start_year=2022) 
sim1.scenario['SHJ'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycling_eff', 90.0, start_year=2022) 
#silicon recycling to HQ
df_shj_recycleSi_HQ = pd.DataFrame(index=idx_temp, columns=['si_recycled_HQ'], dtype=float)
df_shj_recycleSi_HQ.loc[2022] = 0
df_shj_recycleSi_HQ.loc[2030] = 40
df_shj_recycleSi_HQ.loc[2050] = 75
df_shj_recycleSi_HQ.interpolate(inplace=True)
sim1.scenario['SHJ'].modifyMaterials('silicon', 'mat_EOL_Recycled_into_HQ', df_shj_recycleSi_HQ.loc[2022:,'si_recycled_HQ'], start_year=2022) 
sim1.scenario['SHJ'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycled_into_HQ', df_shj_recycleSi_HQ.loc[2022:,'si_recycled_HQ'], start_year=2022) 
#silicon recycling to HQCL
df_shj_recycleSi_HQCL = pd.DataFrame(index=idx_temp, columns=['si_recycled_HQCL'], dtype=float)
df_shj_recycleSi_HQCL.loc[2022] = 0
df_shj_recycleSi_HQCL.loc[2030] = 100
df_shj_recycleSi_HQCL.loc[2050] = 100
df_shj_recycleSi_HQCL.interpolate(inplace=True)
sim1.scenario['SHJ'].modifyMaterials('silicon', 'mat_EOL_RecycledHQ_Reused4MFG', df_shj_recycleSi_HQCL.loc[2022:,'si_recycled_HQCL'], start_year=2022) #closed-loop
sim1.scenario['SHJ'].modifyMaterials('silicon', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', df_shj_recycleSi_HQCL.loc[2022:,'si_recycled_HQCL'], start_year=2022) #closed-loop


# In[62]:


sim1.scenario['SHJ'].material['silicon'].matdataIn_m#.iloc[:,2:]


# In[71]:


plt.plot(sim1.scenario['SHJ'].material['silicon'].matdataIn_m.iloc[:,0],sim1.scenario['SHJ'].material['silicon'].matdataIn_m.iloc[:,3:])
plt.legend(sim1.scenario['PV_ICE'].material['silicon'].matdataIn_m.iloc[:,3:].columns, 
           bbox_to_anchor=(0, -0.1), loc='upper left', ncol=1)
plt.title('Silicon Management Evolution')


# In[69]:


plt.plot(sim1.scenario['SHJ'].material['glass'].matdataIn_m.iloc[:,0],sim1.scenario['SHJ'].material['glass'].matdataIn_m.iloc[:,3:])
plt.legend(sim1.scenario['PV_ICE'].material['glass'].matdataIn_m.iloc[:,3:].columns, 
           bbox_to_anchor=(0, -0.1), loc='upper left', ncol=1)
plt.title('Glass Management Ev')


# In[ ]:





# ### TOPCon

# In[20]:


#module efficiency modify for PERC
sim1.modifyScenario('TOPCon', 'mod_eff', celltech_modeff.loc[2022:,'TOPCon'], start_year=2022) #changing module eff
#sim1.scenario['SHJ'].dataIn_m.loc[timeshift:,'mod_eff'] = celltech_modeff.loc[2022:,'SHJ'].values


# In[21]:


#modify silver usage for SHJ
sim1.scenario['TOPCon'].modifyMaterials('silver', 'mat_massperm2', celltech_aguse.loc[2022:,'TOPCon'], start_year=2022)


# In[22]:


#modify package to glass glass
sim1.scenario['TOPCon'].modifyMaterials('glass', 'mat_massperm2', glassperm2, start_year=2022)


# In[23]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('TOPCon', 'mod_degradation', 0.7, start_year=2022) #annual power degradation
#Mod Project Lifetime
sim1.modifyScenario('TOPCon', 'mod_lifetime', 30, start_year=2022) #project lifetime of 30 years
#T50
sim1.modifyScenario('TOPCon', 'mod_reliability_t50', 28, start_year=2022)
#t90
sim1.modifyScenario('TOPCon', 'mod_reliability_t90', 33, start_year=2022) 


# In[ ]:





# #### Recycled PERC
# This module is based on the recent test from Fraunhofer ISE in which an old module was dissassembled, and the silicon wafer cleaned, put into a Cz ingot growth process and made using standard PERC processing, creating a 19% efficient module.
# https://www.ise.fraunhofer.de/en/press-media/press-releases/2022/solar-cells-from-recycled-silicon.html

# In[29]:


#https://www.ise.fraunhofer.de/en/press-media/press-releases/2022/solar-cells-from-recycled-silicon.html
#lets assume this gets slightly better over time
idx_RePerc_eff = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
df_RePerc_eff = pd.DataFrame(index=idx_RePerc_eff, columns=['mod_eff_RePerc'], dtype=float)
df_RePerc_eff.loc[2022] = 19.7
df_RePerc_eff.loc[2050] = 22.2
df_RePerc_eff.interpolate(inplace=True)


# In[30]:


#module efficiency
sim1.modifyScenario('RecycledPERC', 'mod_eff', df_RePerc_eff['mod_eff_RePerc'], start_year=2022)


# In[31]:


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





# In[32]:


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


# In[33]:


#the cool feature of this module was that the wafer was directly put into the Cz process
#therefore, we need to modify the recycling energy to reflect this
#this energy profile is output by the (baseline development) Energy Silicon Manufacturing journal.
altHQRecycle_e = pd.read_csv(os.path.join(supportMatfolder, 'output_energy_silicon_eol_recycleHQ_ALT.csv'), index_col=0)


# In[34]:


altHQRecycle_e


# In[35]:


sim1.scenario['RecycledPERC'].modifyMaterialEnergy('silicon', 'e_mat_Recycled_HQ', altHQRecycle_e.loc[2022:,'E_MFG_kWhpkg'], start_year=2022)
sim1.scenario['RecycledPERC'].modifyMaterialEnergy('silicon', 'e_mat_Recycled_HQ_fuelfraction', altHQRecycle_e.loc[2022:,'E_mfgFuelFraction'], start_year=2022)


# In[36]:


sim1.scenario['RecycledPERC'].material['silicon'].matdataIn_e.iloc[25:30,]


# In[ ]:





# In[ ]:





# ### Cheap Crap
# This module represents second tier or low quality and low up front cost modules. The module is monofacial, glass-backsheet, degrades quickly, high failure rates, and low open-loop recycling rates.

# In[ ]:





# In[37]:


#module efficiency modify for PERC
sim1.modifyScenario('CheapCrap', 'mod_eff', 19.0, start_year=2022) #changing module eff


# In[38]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('CheapCrap', 'mod_degradation', 1.0, start_year=2022) #annual power degradation
#Mod Project Lifetime
sim1.modifyScenario('CheapCrap', 'mod_lifetime', 25, start_year=2022) #project lifetime of 25 years

#modify alpha beta instead of T50T90, according to Henry Hieslmair bin D quality values
#alpha = 5.692, beta = 29.697
#H. Hieslmair, “Assessing the ‘useful life’ of PV Modules: Reaching for 40 and 50 year module useful life,” 
#presented at the NREL PVRW, Feb. 18, 2021. Accessed: Feb. 26, 2021. [Online]. Available: https://www.youtube.com/watch?v=M7BHcxxugwY&feature=youtu.be
#do this when we run the simulation below
#Modify weibull params for cheap crap only and re run
cheapcrapweibull = {'alpha':5.692,
                   'beta':29.697}


# In[ ]:





# In[ ]:





# #### Repowered

# In[ ]:





# In[ ]:





# In[ ]:





# ### Modify Years 2000 to 2100
# We do this after we modify the baselines to propogate the modified 2050 values forward

# In[39]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim1.trim_Years(startYear=2000, endYear=2100)


# In[40]:


#check
sim1.scenario['SHJ'].material['glass'].matdataIn_e


# ### Apply deployment curve
# For the full derivation of the deployment curve, see the "PV Installations - Global" development journal. Essentially, the projection is 2000-2021 IRENA historical installation data, 2022 through 2050 is a quadratic fit to achieve 50 TW in 2050, and from 2050 to 2100 is a linear increase to approx 60 TW based on 2000-2021 global increase in electricity capacity (219.32 GW/year).
# 
# This is the deployment curve applied to all PV technologies - however, it will be modified for each PV tech using the installation compensation method, increasing it for any replacement modules required to maintain capacity.

# In[41]:


global_projection = pd.read_csv(os.path.join(supportMatfolder,'output-globalInstallsProjection.csv'), index_col=0)

fig, ax1 = plt.subplots()

ax1.stackplot(global_projection.index, global_projection['World_cum']/1e6, color='#F7A11A')
ax1.set_ylabel('Cumulative Solar Capacity [TW]', color='#F7A11A')
ax2 = ax1.twinx()
ax2.plot(global_projection['World_annual_[MWdc]']/1e6)
ax2.set_ylabel('Annual Installations [TW]')
plt.show()


# In[42]:


#deployment projection for all scenarios
sim1.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', value= global_projection['World_annual_[MWdc]'], start_year=2000)
#for scen in scennames:
#    sim1.scenario[scen].dataIn_m.loc[0:len(global_projection.index-1),'new_Installed_Capacity_[MW]'] = global_projection['World_annual_[MWdc]'].values


# In[ ]:





# # Calculate Mass flow
# Can just calc mass here (exclude energy) because we're going to immediately do Install Compensation.

# In[43]:


sim1.calculateMassFlow()
sim1.calculateFlows(scenarios=['CheapCrap'], weibullInputParams=cheapcrapweibull)


# In[44]:


ii_yearly, ii_cumu = sim1.aggregateResults() #have to do this to get auto plots


# In[45]:


ii_cumu['newInstalledCapacity_sim1_PV_ICE_[MW]']


# In[46]:


sim1.scenario['CheapCrap'].dataOut_m['WeibullParams']


# In[47]:


effective_capacity = ii_yearly.filter(like='ActiveCapacity')
plt.plot(ii_cumu['newInstalledCapacity_sim1_PV_ICE_[MW]']/1e6, label='Capacity Target', color='black', ls='--')
plt.plot(effective_capacity/1e6, label=scennames_labels)
plt.legend()
plt.ylabel('Effective Capacity [TW]')
plt.title('Effective Capacity: No Replacements')
plt.ylim(0,)


# # Installation Compensation
# Make the installations always match up to the cumulative capacity deployment schedule. (i.e. not the PV ICE baseline)

# #### Bifacial Factors

# In[43]:


bifiFactors = {'PERC_50':0.7, # ITRPV 2022, Fig. 58
               'SHJ':0.9, # ITRPV 2022, Fig. 58
               'TOPCon':0.8, # ITRPV 2022, Fig. 58
               'Perovskite': 0.0,
               'RecycledPERC':0.6,
                'PV_ICE':0.0,
                'CheapCrap':0.0} 

#MAY NEED TO CHANGE TO BE DYNAMIC


# In[44]:


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


# In[50]:


#currently takes 15 mins to run with 5 mateirals and 5 scenarios

for row in range (0,len(sim1.scenario['PV_ICE'].dataIn_m)): #loop over length of years
    print(row)
    for scen in scennames: #loop over scenarios
        print(scen)
        Under_Installment = global_projection.iloc[row,0] - ((sim1.scenario[scen].dataOut_m['Installed_Capacity_[W]'][row])/1e6)  # MWATTS
        sim1.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][row] += Under_Installment #overwrite new installed
        #calculate flows for that scenario with it's bifi factor and modified weibull
        if scen == 'CheapCrap':
            sim1.calculateFlows(scenarios=[scen], bifacialityfactors=bifiPathDict[scen], weibullInputParams=cheapcrapweibull)
        else:
            sim1.calculateFlows(scenarios=[scen], bifacialityfactors=bifiPathDict[scen]) 


# In[51]:


sim1.scenario['CheapCrap'].dataOut_m['WeibullParams'].tail(2)


# In[52]:


plt.plot(sim1.scenario['CheapCrap'].dataOut_m['Installed_Capacity_[W]'])


# In[53]:


#sim1.scenario['PV_ICE'].dataOut_m['irradiance_stc'].head(2)
sim1.scenario['PV_ICE'].dataOut_m['WeibullParams']


# In[54]:


sim1.scenario['PERC_50'].dataOut_m['irradiance_stc'].head(2)


# In[55]:


sim1.scenario['Perovskite'].dataOut_m['irradiance_stc'].head(2)


# In[56]:


sim1.scenario['RecycledPERC'].dataOut_m['irradiance_stc'].head(2)


# In[58]:


#aggregate results - mass
cc_yearly, cc_cumu = sim1.aggregateResults() #have to do this to get auto plots
cc_yearly.to_csv(os.path.join(testfolder, 'cc_yearly.csv'))
cc_cumu.to_csv(os.path.join(testfolder, 'cc_cumu.csv'))


# In[59]:


#aggregate results - energy
allenergy, energyGen, energy_demands = sim1.aggregateEnergyResults()
allenergy.to_csv(os.path.join(testfolder, 'cc_allenergy.csv'))
energyGen.to_csv(os.path.join(testfolder, 'cc_energyGen.csv'))
energy_demands.to_csv(os.path.join(testfolder, 'cc_energy_demands.csv'))


# In[45]:


#read in saved results files for speed
cc_yearly = pd.read_csv(os.path.join(testfolder, 'cc_yearly.csv'), index_col='year')
cc_cumu = pd.read_csv(os.path.join(testfolder, 'cc_cumu.csv'), index_col='year')
allenergy = pd.read_csv(os.path.join(testfolder, 'cc_allenergy.csv'), index_col='year')
energyGen = pd.read_csv(os.path.join(testfolder, 'cc_energyGen.csv'), index_col='year')
energy_demands = pd.read_csv(os.path.join(testfolder, 'cc_energy_demands.csv'), index_col='year')


# In[61]:


sim1.plotMetricResults()


# # RESULTS: Effective Capacity and Replacements

# In[62]:


effective_capacity = cc_yearly.filter(like='ActiveCapacity')
plt.plot(effective_capacity/1e6)
plt.legend(scennames_labels)
plt.ylabel('Effective Capacity [TW]')
plt.title('Effective Capacity: With Replacements')
plt.ylim(0,)


# In[63]:


annual_EoL = cc_yearly.filter(like='DecommisionedCapacity')
plt.plot(annual_EoL/1e6)
plt.legend(scennames_labels)
plt.ylabel('Annual EoL [TW]')
plt.title('Annual Decommissions [TW]')
plt.ylim(0,)


# In[64]:


annual_installs = cc_yearly.filter(like='newInstalled')
plt.plot(annual_installs/1e6)
plt.legend(scennames_labels)
plt.ylabel('Annual installed [TW]')
plt.title('Annual Installs with Replacements')
plt.ylim(0,)


# In[65]:


cumu_installs_annually = cc_cumu.filter(like='newInstalled')
plt.plot(cumu_installs_annually/1e6)
plt.legend(scennames_labels)
plt.ylabel('Cumulative installed [TW]')
plt.title('Replacements Adjusted Deployment Curve \n Cumulative Installs with Replacements')
plt.ylim(0,)


# In[66]:


cumu_installs = cc_cumu.filter(like='newInstalled')
plt.bar(scennames, cumu_installs.loc[2100]/1e6, tick_label=scennames_labels, color=colorpalette)
#plt.legend(scennames)
plt.ylabel('Cumulative installed [TW]')
plt.title('Cumulative Installs with Replacements')


# In[67]:


cumulative_nameplate_installs = global_projection.loc[2100,'World_cum'] #MW
print('The nameplate installations for energy transition and through 2100 are '+str(cumulative_nameplate_installs/1e6)+' TW.')


# In[68]:


global_projection['World_annual_[MWdc]'].sum()


# In[69]:


Additional_installs = cumu_installs.loc[2100]-global_projection.loc[2100,'World_cum']
plt.bar(scennames, Additional_installs/1e6, tick_label=scennames_labels, color=colorpalette)
#plt.legend(scennames)
plt.ylabel('Cumulative Replacements [TW]')
plt.title('Replacements Required by Technology')


# # RESULTS: Virgin Material Demands

# In[47]:


cumu_virgin_module = cc_cumu.filter(like='VirginStock_Module')
plt.bar(scennames, cumu_virgin_module.loc[2100]/1e9, tick_label=scennames_labels, color=colorpalette)
#plt.legend(scennames)
plt.title('Cumulative Virgin Material Demands')
plt.ylabel('Virgin Material Requirements\n[billion tonnes]')


# In[76]:





# In[77]:


recycledperc_virginstock = cc_cumu.filter(like='VirginStock').filter(like='Recycled')
recycledperc_virginstock.drop('VirginStock_Module_sim1_RecycledPERC_[Tonnes]',axis=1, inplace=True)
plt.bar(recycledperc_virginstock.columns, recycledperc_virginstock.loc[2100], tick_label = MATERIALS, color=colorpalette)


# In[71]:


cumu_virgin_module = cc_cumu.filter(like='VirginStock_Module')
plt.plot(cumu_virgin_module/1e9)
plt.legend(scennames_labels)
plt.title('Cumulative Virgin Material Extraction: Module')
plt.ylabel('Virgin Material Requirements\n[billion tonnes]')
plt.ylim(0,)


# In[72]:


annual_virgin_module = cc_yearly.filter(like='VirginStock_Module')
plt.plot(annual_virgin_module/1e6)
plt.legend(scennames_labels)
plt.title('Annual Virgin Material Extraction: Module')
plt.ylabel('Virgin Material Requirements\n[million tonnes]')
plt.ylim(0,)


# In[73]:


#print out masses for stacked bar charts
#mass_cumu = cc_cumu.loc[[2100]].filter(like='PV_ICE_[Tonnes]')
mass_cumu_virgin = cc_cumu.filter(like='VirginStock').loc[2100]
mass_cumu_wasteall = cc_cumu.filter(like='WasteAll').loc[2100]
mass_cumu = pd.concat([mass_cumu_virgin,mass_cumu_wasteall])
mass_cumu.to_csv(os.path.join(testfolder, 'cc_cumu_mass_2100results.csv'))


# In[ ]:





# In[74]:


cc_cumu.to_csv(os.path.join(testfolder, 'cc_cumu_mass_results.csv'))


# # RESULTS: Lifecycle Wastes

# In[75]:


cumu_lifecycle_wastes = cc_cumu.filter(like='WasteAll_Module')

plt.bar(scennames, cumu_lifecycle_wastes.loc[2100]/1e6, 
        tick_label=scennames_labels, color=colorpalette)
#plt.legend(scennames)
plt.title('Cumulative Lifecycle Wastes')
plt.ylabel('Lifecycle Wastes\n[million tonnes]')


# # RESULTS: Energy

# In[76]:


sim1.scenario['SHJ'].dataOut_e


# ## Energy Generation
# Because of different bifi factors, they do NOT produce the same energy

# In[77]:


#energyGen = allenergy.filter(like='e_out_annual')
plt.plot(energyGen/1e12)
plt.legend(scennames_labels)
plt.title('Annual Energy Generation')
plt.ylabel('Energy Generation [TWh]')
plt.ylim(0,)


# ## Net Energy

# In[78]:


e_annual_sumDemands = energy_demands.filter(like='demand_total')


# In[79]:


plt.plot(e_annual_sumDemands/1e12)
plt.legend(scennames_labels)
plt.title('Annual Lifecycle Energy Demands')
plt.ylabel('Energy Demands\n[TWh]')
plt.ylim(0,)


# In[80]:


e_annual_sumDemands_cumu = e_annual_sumDemands.cumsum()


# In[81]:


plt.bar(e_annual_sumDemands_cumu.columns, e_annual_sumDemands_cumu.loc[2100]/1e12, 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('Cumulative Lifecycle Energy Demands')
plt.ylabel('Cumulative Energy Demands\n[TWh]')


# In[82]:


energyGen_cumu = energyGen.cumsum()
energyGen_cumu.columns = e_annual_sumDemands_cumu.columns = scennames
netEnergy_cumu = energyGen_cumu.loc[[2100]] - e_annual_sumDemands_cumu.loc[[2100]]


# In[83]:


e_annual_sumDemands_cumu.loc[[2100]]


# In[84]:


netEnergy_cumu


# In[85]:


plt.bar(netEnergy_cumu.columns, netEnergy_cumu.loc[2100]/1e12, 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('Net Energy Cumulatively')
plt.ylabel('Cumulative Net Energy [TWh]')
plt.ylim(4e6,5.5e6)


# In[86]:


netEnergy_relative = netEnergy_cumu - netEnergy_cumu.loc[2100,'PV_ICE']
netEnergy_relative
plt.bar(netEnergy_relative.columns, netEnergy_relative.loc[2100]/1e12, 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('Cumulatively Net Energy Relative to PV ICE')
plt.ylabel('Relative Cumulative Net Energy [TWh]')


# In[87]:


netEnergy_cumu_norm = netEnergy_cumu/netEnergy_cumu.loc[2100,'PV_ICE']
netEnergy_cumu_norm_waterfall = netEnergy_cumu_norm-1
netEnergy_cumu_norm


# In[88]:


plt.bar(netEnergy_cumu.columns, netEnergy_cumu_norm_waterfall.loc[2100], 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('Net Energy Cumulatively Relative to PV ICE')
plt.ylabel('Relative Cumulative Net Energy')
#plt.ylim(-0.026,0.005)
plt.plot(0.0, lw=2)


# In[89]:


plt.bar(netEnergy_cumu.columns, netEnergy_cumu.loc[2100]/1e12, 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('Net Energy Cumulatively')
plt.ylabel('Cumulative Net Energy\n[TWh]')


# In[90]:


energyGen.columns = e_annual_sumDemands.columns = scennames
annual_net_energy = energyGen - e_annual_sumDemands


# In[91]:


plt.plot(annual_net_energy/1e12)
plt.legend(scennames_labels)
plt.title('Annual Net Energy')
plt.ylabel('Net Energy (Eout - Ein)\n[TWh]')
plt.ylim(0,100000)
plt.xlim(2000,2100)


# ## System Level EROI
# This may not be an accurate use of EROI, but I want to see what will happen

# In[92]:


eroi_sys_cumu = energyGen_cumu/e_annual_sumDemands_cumu


# In[93]:


plt.bar(eroi_sys_cumu.columns, eroi_sys_cumu.loc[2100], 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('EROI of all Deployments')
plt.ylabel('Unitless')


# In[ ]:





# In[ ]:





# # CE-TE Metric
# Net Energy over Linear mass flow

# In[ ]:


#cumulatively
netEnergy_cumu.columns = cumu_virgin_module.columns = cumu_lifecycle_wastes.columns = scennames_labels

CEETmetric = (netEnergy_cumu.loc[2100]/1e6)/ (cumu_virgin_module.loc[2100]+ cumu_lifecycle_wastes.loc[2100])


# In[ ]:


plt.bar(CEETmetric.index, CEETmetric, 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('CETE Metric')
plt.ylabel('Net Energy / Linear Mass \n[MWh/tonne]')


# In[ ]:





# # EROI
# Create single installation simulation to evaluate EROI of modules. Do one round of 2022 modules and one of 2050 modules.
# ## EROI 2022

# In[ ]:


single_deploy_2022 = pd.DataFrame(index=idx_temp, columns=['MW'], dtype=float)
single_deploy_2022['MW'] = 0.0
single_deploy_2022.loc[2022] = 100.0 #install a single 100 MW system


# In[ ]:


sim2 = PV_ICE.Simulation(name='sim2', path=testfolder)
for scen in scennames:
    sim2.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim2.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[ ]:


#use the settings from the first simulation to create the identical settings for sim2
for scen in scennames:
    sim2.scenario[scen].dataIn_m = sim1.scenario[scen].dataIn_m
    sim2.scenario[scen].dataIn_e = sim1.scenario[scen].dataIn_e
    for mat in MATERIALS:
        sim2.scenario[scen].material[mat].matdataIn_m = sim1.scenario[scen].material[mat].matdataIn_m
        sim2.scenario[scen].material[mat].matdataIn_e = sim1.scenario[scen].material[mat].matdataIn_e
        


# In[ ]:


sim2.scenario['Perovskite'].material['glass'].matdataIn_m


# In[ ]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim2.trim_Years(startYear=2000, endYear=2100)


# In[ ]:


#deployment projection for all scenarios
sim2.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', value= single_deploy_2022['MW'], start_year=2000)


# In[ ]:


sim2.scenario['Perovskite'].dataIn_m.loc[19:25]


# In[ ]:


for scen in scennames:
    sim2.calculateFlows(scenarios=[scen],bifacialityfactors=bifiPathDict[scen])


# In[ ]:


sim2_yearly, sim2_cumulative = sim2.aggregateResults()


# In[ ]:


allenergy2, energyGen2, energy_demands2 = sim2.aggregateEnergyResults()


# In[ ]:


allenergy2_cumu = allenergy2.cumsum()
energyGen2_cumu = energyGen2.cumsum()
energy_demands2_cumu = energy_demands2.cumsum()


# In[ ]:


energy_demands2_cumu_total = energy_demands2_cumu.filter(like='demand_total')
#energy_demands2_cumu_total


# In[ ]:


plt.bar(energy_demands2_cumu_total.columns, energy_demands2_cumu_total.loc[2100], 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('Energy Demands Cumulative')
plt.ylabel('Energy Demands [Wh]')


# In[ ]:


energyGen2_cumu.columns=energy_demands2_cumu_total.columns=scennames_labels
eroi_2022 = energyGen2_cumu.iloc[100]/energy_demands2_cumu_total.iloc[100]
eroi_2022


# In[ ]:


plt.bar(eroi_2022.index, eroi_2022, 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('EROI')
plt.ylabel('Arb.')


# In[ ]:


plt.plot(energyGen2/1e9)
plt.legend(scennames_labels)
plt.title('Energy Generation - Single 2022 System')
plt.ylabel('[GWh]')


# ## EROI of 2050 module

# In[ ]:



single_deploy_2050 = pd.DataFrame(index=idx_temp, columns=['MW'], dtype=float)
single_deploy_2050['MW'] = 0.0
single_deploy_2050.loc[2050] = 100.0 #install a single 100 MW system


# In[ ]:


sim3 = PV_ICE.Simulation(name='sim3', path=testfolder)
for scen in scennames:
    sim3.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim3.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[ ]:


#use the settings from the first simulation to create the identical settings for sim2
for scen in scennames:
    sim3.scenario[scen].dataIn_m = sim1.scenario[scen].dataIn_m
    sim3.scenario[scen].dataIn_e = sim1.scenario[scen].dataIn_e
    for mat in MATERIALS:
        sim3.scenario[scen].material[mat].matdataIn_m = sim1.scenario[scen].material[mat].matdataIn_m
        sim3.scenario[scen].material[mat].matdataIn_e = sim1.scenario[scen].material[mat].matdataIn_e
        


# In[ ]:


sim3.scenario['Perovskite'].material['glass'].matdataIn_m


# In[ ]:


#deployment projection for all scenarios
sim3.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', value= single_deploy_2050['MW'], start_year=2000)


# In[ ]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim3.trim_Years(startYear=2000, endYear=2150)


# In[ ]:


sim3.scenario['Perovskite'].dataIn_e.tail(4)#loc[49:55]


# In[ ]:


#PV ICE currently set up to read in a csv of bifi factors, so generate files to read in 
#need to adjust for length to 2150
idx_temp_2150 = pd.RangeIndex(start=2000,stop=2151,step=1) #create the index
df_temp_2150 = pd.DataFrame(index=idx_temp_2150, columns=['bifi'], dtype=float)
bifiPathDict_2150={}

for f in bifiFactors.keys(): #loop over module types
    bifi_2150 = df_temp_2150.copy() #copy of df
    bifi_2150['bifi'] = bifiFactors[f] #assign column
    bifipath_2150 = os.path.join(testfolder,'bifi_'+str(f)+'.csv') #create file path
    bifi_2150.to_csv(path_or_buf=bifipath_2150, index_label='year') #create file
    bifiPathDict_2150[str(f)] = bifipath_2150
    #append bifi path to dict? or list?


# In[ ]:


for scen in scennames:
    sim3.calculateFlows(scenarios=[scen], bifacialityfactors=bifiPathDict_2150[scen])


# In[ ]:





# In[ ]:


sim3_yearly, sim3_cumulative = sim3.aggregateResults()


# In[ ]:


allenergy3, energyGen3, energy_demands3 = sim3.aggregateEnergyResults()


# In[ ]:


allenergy3_cumu = allenergy3.cumsum()
energyGen3_cumu = energyGen3.cumsum()
energy_demands3_cumu = energy_demands3.cumsum()


# In[ ]:


energy_demands3_cumu_total = energy_demands3_cumu.filter(like='demand_total')
#energy_demands3_cumu_total


# In[ ]:


plt.bar(energy_demands3_cumu_total.columns, energy_demands3_cumu_total.loc[2150], 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('Energy Demands Cumulative 2050 System')
plt.ylabel('Energy Demands [Wh]')


# In[ ]:


energyGen3_cumu.columns = energy_demands3_cumu_total.columns = scennames_labels
eroi_2050 = energyGen3_cumu.loc[2150]/energy_demands3_cumu_total.loc[2150]
eroi_2050


# In[ ]:


plt.bar(eroi_2050.index, eroi_2050, 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('EROI of a 100 MW deployment in 2050')
plt.ylabel('Arbitrary units')


# In[ ]:


plt.plot(energyGen3/1e9)
plt.legend(scennames_labels)
plt.title('Energy Generation - Single 2050 System')
plt.ylabel('[GWh]')


# # To Do
# - energy requirements on a per MW installed for a single install, what is MFG
# - Y axis = normalized net energy of perovskites, x axis = remanufacturing energy variation, maybe add recycling Just change one variable 
# 
# lowest nergy = remfg
# mid energy = recycle
# high energy = virgin mfg

# In[ ]:




