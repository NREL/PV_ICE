#!/usr/bin/env python
# coding: utf-8

# # Analysis of Cell Technology
# 3 competing cell technologies may claim marketshare in future; Bifacial PERC, bifacial SHJ, and Bifacial TOPCon. Each design has different efficiency and a different silver intensity. This analysis seeks compare these technologies on a mass and energy basis. A global deployment projection is used so that silver demand can be evaluated at the global level.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'CellTechCompare')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


scennames = ['PERC','SHJ','TOPCon']
MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[ ]:





# In[ ]:





# In[ ]:


#load in a baseline and materials for modification
sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames:
    sim1.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
        for mat in range (0, len(MATERIALS)):
            matbaseline_m = r'..\baselines\baseline_material_mass_'+MATERIALS[mat]+'.csv'
            matbaseline_e = r'..\baselines\baseline_material_energy_'+MATERIALS[mat]+'.csv'
            sim1.scenario['USHistory'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[ ]:





# In[ ]:





# In[ ]:


rtest = PV_ICE.Simulation(name='Sim1', path=inputfolder) #create fake simulation
rtest.createScenario(name='test', massmodulefile=r'..\baselines\baseline_modules_mass_US.csv') #create fake scenario, pull in module baseline
baseline = rtest.scenario['test'].dataIn_m #save baseline data as a seperate dataframe
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]']) #drop the installs column
baseline.set_index('year', inplace=True) #set index inplace to the year column
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual #inform the index that it is an annual period


# In[ ]:


for scen in scennames:
    filetitle = scen+'.csv'
    subtestfolder = os.path.join(testfolder, 'Inputs')
    if not os.path.exists(subtestfolder):
        os.makedirs(subtestfolder)
    filetitle = os.path.join(subtestfolder, filetitle)


# In[ ]:





# In[ ]:


#load in a baseline and materials for modification
r1 = PV_ICE.Simulation(name='sim1', path=testfolder)
r1.createScenario(name='USHistory', massmodulefile=moduleFile) #points at the old module history installs file
for mat in range (0, len(MATERIALS)):
    MATERIALBASELINE = r'..\baselines\baseline_material_mass_'+MATERIALS[mat]+'.csv'
    r1.scenario['USHistory'].addMaterial(MATERIALS[mat], massmatfile=MATERIALBASELINE)


# In[ ]:


for scens in scennames:
    r1.scenario[scens].dataIn_m.loc[0:len(installs_df['year']-1),'new_Installed_Capacity_[MW]'] = installs_df[scens]

