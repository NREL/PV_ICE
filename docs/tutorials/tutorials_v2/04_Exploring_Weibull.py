#!/usr/bin/env python
# coding: utf-8

# # 4 &emsp; Exploring Weibull

# PV ICE handles failures through a probabilistic distribution, so far in specific the Weibull. The Weibull equation is defined by an Alfa and a Beta parameters. These parameters can be found on literature [some literature here could be goood], or they can be calculated if the reliability is known. Altough other values can be set by changing the probabilities, we use by default:
# 
# - T50: number of years until 50 % of the modules fail 
# - T90: number of years until 90 % of the modules fail
# 
# Below we show a couple ways of passing the parameters, plot a comparison between different literature values, and highlight the significance of T50 and T90.

# In[32]:


import os, sys
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
    
dfindex = pd.RangeIndex(0,56,1)


# In[33]:


testfolder = str(Path().resolve() / 'TEMP') # Path to the simulation folder.

baselinefolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines')  # Path to baselines and data.

print ("Your simulation will be stored in %s" % testfolder)
print ("Your baselines are stored in %s" % baselinefolder)


# In[34]:


r3 = PV_ICE.Simulation(name='Simulation_3', path=testfolder)
r3.createScenario(name='Repair_0', file=baselinefolder + '/baseline_modules_US.csv')
r3.scenario['Repair_0'].addMaterial('glass', file=baselinefolder + '/baseline_material_glass.csv')
r3.scenario['Repair_0'].addMaterial('silicon', file=baselinefolder + '/baseline_material_silicon.csv')

r3.createScenario(name='Repair_50', file=baselinefolder + '/baseline_modules_US.csv')
r3.scenario['Repair_50'].addMaterial('glass', file=baselinefolder + '/baseline_material_glass.csv')
r3.scenario['Repair_50'].addMaterial('silicon', file=baselinefolder + '/baseline_material_silicon.csv')


# In[41]:


df = r3.scenario['Repair_0'].data
df['new_Installed_Capacity_[W]'] = df['new_Installed_Capacity_[MW]']*1e6 #Transforming from W to MW


# In[40]:





# In[ ]:




