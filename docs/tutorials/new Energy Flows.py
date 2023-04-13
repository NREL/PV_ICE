#!/usr/bin/env python
# coding: utf-8

# # Energy Flows for PV ICE

# This journal documents and demonstrates the new Energy flows calculation capacity of PV ICE

# In[8]:


import os
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[9]:


PV_ICE.__version__


# ### Add Scenarios and Materials

# In[10]:


cwd=os.getcwd()
print(os.getcwd())


# In[11]:


MATERIALS = ['glass']#,'aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
MATERIAL = MATERIALS[0]

moduleFile_m = r'..\baselines\baseline_modules_mass_US.csv'
moduleFile_e = r'..\baselines\baseline_modules_energy.csv'


# In[13]:


r1 = PV_ICE.Simulation(name='energy_test', path=testfolder)

r1.createScenario(name='energy_test', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    r1.scenario['energy_test'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# # Calculate flows

# In[14]:


r1.calculateFlows()


# Now run the energy calculation. Currently this is not a class, just a function that will return a dataframe. Each scenario will need to be run seperately, and read in the perovskite energy files.

# ## Energy Analysis

# In[15]:


allenergy, energyGen, energy_demands = r1.aggregateEnergyResults()


# In[19]:


energy_demands#.filter(like='_fuel')
energy_demands.columns


# In[20]:


energy_demands['energy_test_glass_mat_MFG_virgin_fuel']/energy_demands['energy_test_glass_mat_MFG_virgin']

