#!/usr/bin/env python
# coding: utf-8

# In[38]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[8]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder =  str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# This Journal supports the documentation of the baseline input files for the PV_ICE calculator by graphing all baseline inputs of modules and materials for all years. Currently, this includes:
# - USA module installs
# - Global module intalls
# - glass
# - silicon
# - silver (preliminary)

# In[1]:


import PV_ICE


# In[12]:


filelist = sorted(os.listdir(baselinesfolder))
matcher = "modules"
module_baselines = [s for s in filelist if matcher in s]
matcher = "material"
material_baselines = [s for s in filelist if matcher in s]  


# # Plot only 1st module baseline example

# In[16]:


i=0
r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='standard', file=os.path.join(baselinesfolder, material_baselines[i]))


# In[21]:


r1.scenario['standard'].data.head()


# In[36]:


keys = list(r1.scenario['standard'].metdata[0].keys())


# In[44]:


for k in keys:
    plt.figure()
    plt.plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data[k])
    plt.xlabel('Year')
    plt.ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')


# # Module Files 

# ## USA

# In[8]:


print(baseline_modules_US)


# In[7]:


plt.plot(baseline_modules_US)

