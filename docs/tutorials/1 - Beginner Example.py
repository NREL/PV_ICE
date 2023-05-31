#!/usr/bin/env python
# coding: utf-8

# # 1 - Create Two Scenarios with Two Materials
# 
# 
# This journal shows how to load the baselines and run the dynamic mas flow analysis, plotting the results for two scenarios and two materials.

# ### Step 1: Set Working Folder and Import PV ICE

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'Tutorial1')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


import PV_ICE


# In[3]:


PV_ICE.__version__


# ### Step 2: Add Scenarios and Materials
# 
# ``silicon`` and ``glass`` materials are added to the two simulations, along with a scenario, in this case the ``baseline_modules_US``. The baseline files for decadence scenario will be modified.
# 

# In[4]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='standard', massmodulefile=r'..\..\baselines\baseline_modules_mass_US.csv')
r1.scenario['standard'].addMaterial('glass', massmatfile=r'..\..\baselines\baseline_material_mass_glass.csv' )
r1.scenario['standard'].addMaterial('silicon', massmatfile=r'..\..\baselines\baseline_material_mass_silicon.csv' )

r1.createScenario('decadence', massmodulefile=r'..\..\baselines\baseline_modules_mass_US.csv')
r1.scenario['decadence'].addMaterial('glass', massmatfile=r'..\..\baselines\baseline_material_mass_glass.csv')
r1.scenario['decadence'].addMaterial('silicon', massmatfile=r'..\..\baselines\baseline_material_mass_silicon.csv')


# Exploring that the data got loaded properly, we can look at each scenario object, and material object saved dataframe and properties

# In[5]:


r1.scenario['standard'].dataIn_m.head(2)


# In[6]:


r1.scenario['standard'].material['silicon'].matdataIn_m.head(2)


# ### Step 4: Run the Mass Flow Calculations on All Scenarios and Materials

# In[7]:


r1.calculateMassFlow()


# Now we have results on the mass layer that we can access

# In[8]:


r1.scenario['standard'].dataOut_m.keys()


# What can aggregate results from dataOut_m and matdataOut_m and compile the data so we can use it more easily

# In[9]:


USyearly, UScum = r1.aggregateResults()
# r1.USyearly
# r1.UScum


# In[10]:


USyearly.keys()


# In[11]:


UScum.keys()


# In[12]:


r1.saveSimulation()


# ### Step 5: Use internal plotting functions to plot results

# Pull out the keywords by printing the keys to the module data or the material data

# In[13]:


print(r1.scenario['standard'].material['silicon'].matdataIn_m.keys())


# In[14]:


r1.plotScenariosComparison()


# In[15]:


r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_virgin_eff')


# In[16]:


r1.plotMaterialResults(keyword='VirginStock')


# In[17]:


r1.plotMetricResults()


# In[18]:


r1.plotInstalledCapacityResults()


# In[ ]:




