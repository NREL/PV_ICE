#!/usr/bin/env python
# coding: utf-8

# # 1 - Create Two Scenarios with Two Materials
# 
# 
# This journal shows how to load the baselines and run the dynamic mas flow analysis, plotting the results for two scenarios and two materials.

# ### Step 1: Set Working Folder and Import PV ICE

# In[3]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'Tutorial1')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)

print ("Your simulation will be stored in %s" % testfolder)


# In[6]:


import PV_ICE
import pandas as pd


# In[7]:


# This information helps with debugging and getting support :)
import sys, platform
print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# ### Step 2: Add Scenarios and Materials
# 
# ``silicon`` and ``glass`` materials are added to the two simulations, along with a scenario, in this case the ``baseline_modules_US``. The baseline files for decadence scenario will be modified.
# 

# In[8]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='standard', massmodulefile=r'..\..\baselines\baseline_modules_mass_US.csv')
r1.scenario['standard'].addMaterial('glass', massmatfile=r'..\..\baselines\baseline_material_mass_glass.csv' )
r1.scenario['standard'].addMaterial('silicon', massmatfile=r'..\..\baselines\baseline_material_mass_silicon.csv' )

r1.createScenario('low_quality', massmodulefile=r'..\..\baselines\baseline_modules_mass_US.csv')
r1.scenario['low_quality'].addMaterial('glass', massmatfile=r'..\..\baselines\baseline_material_mass_glass.csv')
r1.scenario['low_quality'].addMaterial('silicon', massmatfile=r'..\..\baselines\baseline_material_mass_silicon.csv')


# Exploring that the data got loaded properly, we can look at each scenario object, and material object saved dataframe and properties

# In[9]:


r1.scenario['standard'].dataIn_m.head(2)


# In[10]:


r1.scenario['standard'].material['silicon'].matdataIn_m.head(2)


# # Step 3: Modify values
#     
# PV_ICE has some dedicated functions that create changes based on improvements, but for this example we'll just be modifying values for the full column and comparing effects. To modify these columns, we specify the scenario or material parameter we want to modify, and assign the new value. In this case we are updating:
# * module lifetime
# * module degradation

# In[16]:


r1.scenario['low_quality'].dataIn_m['mod_lifetime'] = 15 
r1.scenario['low_quality'].dataIn_m['mod_degradation'] = 1.4 


# ### Step 4: Run the Mass Flow Calculations on All Scenarios and Materials

# In[17]:


r1.calculateMassFlow()


# Now we have results on the mass layer that we can access

# In[18]:


r1.scenario['standard'].dataOut_m.keys()


# What can aggregate results from dataOut_m and matdataOut_m and compile the data so we can use it more easily

# In[19]:


USyearly, UScum = r1.aggregateResults()
# r1.USyearly # another way of accessing after running aggregateResults()
# r1.UScum


# In[20]:


USyearly.keys()


# In[21]:


UScum.keys()


# In[22]:


r1.saveSimulation()


# ### Step 5: Use internal plotting functions to plot results

# From this list, select the one that fits your study and select the type of plotting method. There are various plotting options:
# * `plotScenariosComparison`
# * `plotMaterialComparisonAcrossScenarios`
# * `plotMetricResults`: You can select the following keyword options: 'VirginStock', 'WasteALL', 'WasteEOL', 'WasteMFG'
# * `plotMaterialResults`
# * `plotInstalledCapacityResults`

# You can also view all the keywords you can use by calling the function without argumnets, or by printing the keys to the module data or the material data

# In[23]:


r1.plotScenariosComparison()


# In[28]:


r1.plotScenariosComparison('Effective_Capacity_[W]')


# In[26]:


r1.plotMetricResults()


# In[ ]:




