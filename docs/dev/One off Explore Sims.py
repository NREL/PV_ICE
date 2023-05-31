#!/usr/bin/env python
# coding: utf-8

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
scennames = ['test'] #might need a PV ICE baseline too
MATERIALS = ['glass','silver','silicon', 'copper', 'aluminium_frames'] #'encapsulant', 'backsheet',
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


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


# In[4]:


#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('test', 'mod_degradation',0.2, start_year=2000) 
sim1.modifyScenario('test', 'mod_lifetime', 50, start_year=2000) 
sim1.modifyScenario('test', 'new_Installed_Capacity_[MW]', 0.0, start_year=1995) 
sim1.modifyScenario('test', 'mod_eff', 17.0, start_year=1995) 

#sim1.scenMod_perfectRecycling()
sim1.scenMod_noCircularity()


# In[5]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim1.trim_Years(startYear=2000, endYear=2100)


# In[6]:


sim1.scenario['test'].dataIn_m.loc[20,'new_Installed_Capacity_[MW]'] =100.0 #install 100 MW in 2020 a single year


# In[7]:


sim1.scenario['test'].dataIn_m


# In[8]:


sim1.calculateFlows(scenarios='test')


# In[9]:


plt.plot(sim1.scenario['test'].dataOut_m['Installed_Capacity_[W]'])


# In[10]:


sim1_annual, sim1_cum = sim1.aggregateResults()


# In[11]:


#MASS
sim1_cum.filter(like='Module')


# In[12]:


#ENERGY
sim1.scenario['test'].dataOut_e.cumsum()


# In[13]:


energy_mat = pd.DataFrame()
for scen in scennames:
    for mat in MATERIALS:
        # add the scen name as a prefix for later filtering
        scenmatde = sim1.scenario[scen].material[mat].matdataOut_e.add_prefix(str(scen+'_'+mat+'_'))
        #concat into one large df
        energy_mat = pd.concat([energy_mat, scenmatde], axis=1)

energy_mat.tail()


# In[14]:


energy_mat.cumsum().loc[100].sum()

