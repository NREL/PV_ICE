#!/usr/bin/env python
# coding: utf-8

# # Energy Graphing
# 
# A simple journal to explore and graph energy contributions

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 18})
#plt.rcParams['figure.figsize'] = (10, 6)

cwd = os.getcwd() #grabs current working directory

#testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / '')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')

#if not os.path.exists(testfolder):
#    os.makedirs(testfolder)


# In[2]:


#creating scenarios for identical power and identical area deployed
MATERIALS = ['glass','silver','silicon', 'copper', 'aluminium_frames'] # 'encapsulant', 'backsheet', 
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[3]:


#load in a baseline and materials for modification
import PV_ICE

sim_anModule = PV_ICE.Simulation(name='sim_anModule', path=inputfolder)
sim_anModule.createScenario(name='PVICE', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim_anModule.scenario['PVICE'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[4]:


#no circularity
sim_anModule.scenMod_noCircularity()


# In[5]:


#create an area dataframe to feed in a module each year
idx_temp = pd.RangeIndex(start=1995,stop=2051,step=1) #create the index
area_deploy_anModule = pd.DataFrame(index=idx_temp, dtype=float) #create an empty DF
area_deploy_anModule['Area'] = 2.0
area_deploy_anModule.head()


# In[6]:


sim_anModule.calculateFlows(scenarios='PVICE', 
                            installByArea=list(area_deploy_anModule['Area']))


# In[7]:


anmodule_yearly, anmodule_cumu = sim_anModule.aggregateResults()
allenergy, energyGen, energy_demands = sim_anModule.aggregateEnergyResults()


# In[8]:


energy_demands.head(3)


# Sum the Energy demands by material and by module

# In[9]:


e_module_sum = energy_demands.filter(like='mod').sum(axis=1)

e_glass_sum = energy_demands.filter(like='glass').sum(axis=1)
e_silicon_sum = energy_demands.filter(like='silicon').sum(axis=1)
e_silver_sum = energy_demands.filter(like='silver').sum(axis=1)
e_copper_sum = energy_demands.filter(like='copper').sum(axis=1)
e_alframes_sum = energy_demands.filter(like='aluminium_frames').sum(axis=1)

e_bkdwn_mod_mat = pd.concat([e_module_sum,e_glass_sum,e_silicon_sum,e_silver_sum,e_copper_sum,e_alframes_sum],
                            axis=1, keys=['module','glass','silicon','silver', 'copper','alframes'])


# In[10]:


e_bkdwn_mod_mat.head(3)


# In[13]:


fig, ax = plt.subplots()

#module
ax.bar(e_bkdwn_mod_mat.index, e_bkdwn_mod_mat['module']/1e3, label='module', color='slategray')
#glass
ax.bar(e_bkdwn_mod_mat.index, e_bkdwn_mod_mat['glass']/1e3, label='glass', color = 'lightskyblue',
       bottom=e_bkdwn_mod_mat['module']/1e3)
#silicon
ax.bar(e_bkdwn_mod_mat.index, e_bkdwn_mod_mat['silicon']/1e3, label='silicon', color='cornflowerblue',
       bottom=(e_bkdwn_mod_mat['module']+e_bkdwn_mod_mat['glass'])/1e3)
#silver
ax.bar(e_bkdwn_mod_mat.index, e_bkdwn_mod_mat['silver']/1e3, label='silver', color = 'blue',
       bottom=(e_bkdwn_mod_mat['module']+e_bkdwn_mod_mat['glass']+e_bkdwn_mod_mat['silicon'])/1e3)
#copper
ax.bar(e_bkdwn_mod_mat.index, e_bkdwn_mod_mat['copper']/1e3, label='copper', color = 'white',
       bottom=(e_bkdwn_mod_mat['module']+e_bkdwn_mod_mat['glass']+e_bkdwn_mod_mat['silicon']+e_bkdwn_mod_mat['silver'])/1e3)
#Al frames
ax.bar(e_bkdwn_mod_mat.index, e_bkdwn_mod_mat['alframes']/1e3, label='alframes', color = 'black',
       bottom=(e_bkdwn_mod_mat['module']+e_bkdwn_mod_mat['glass']+e_bkdwn_mod_mat['silicon']+e_bkdwn_mod_mat['silver']+e_bkdwn_mod_mat['copper'])/1e3)


plt.legend()
ax.set_ylabel('Energy Demand \n[kWh/module]')
plt.title('Change in Manufacturing Energy by Component')
plt.rc('font', size=14) #controls default text size
plt.rcParams['figure.figsize'] = (10, 8)
plt.xlim(1994.5,2030.5)
plt.show()

