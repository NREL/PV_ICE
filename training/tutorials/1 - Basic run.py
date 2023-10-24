#!/usr/bin/env python
# coding: utf-8

# # 1 - Basics run
# 
# **Requirements:**
# - Files linked via URL.
# 
# **Objectives:**
# 1. Read in necessary mass and energy data
# 2. Modify necessary values manually and programatically
# 3. Generate plots 

# In[1]:


# if running on google colab, uncomment the next line and execute this cell to install the dependencies and prevent "ModuleNotFoundError" in later cells:
# !pip install git+https://github.com/NREL/PV_ICE.git@development


# In[ ]:


import PV_ICE
PV_ICE.__version__


# In[ ]:


from google.colab import files
files.upload()


# In[ ]:


import os
os.listdir()


# In[ ]:


pwd


# In[ ]:


testfolder = 'Tuesday'

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[ ]:


r1 = PV_ICE.Simulation(name='Sim1', path=testfolder); # Is it possible to define more than one simulation here?


# In[ ]:


r1.__dict__


# In[ ]:


r1.baselinepath = '/content'


# In[ ]:


r1.createScenario(name='standard', massmodulefile=r'baseline_modules_mass_US.csv', energymodulefile = 'baseline_modules_energy.csv' )


# In[ ]:


r1.scenario['standard'].addMaterial('glass', massmatfile='/content/baseline_material_mass_glass.csv', energymatfile='/content/baseline_material_energy_glass.csv')


# In[ ]:


r1.scenario['standard'].material['glass'].__dict__


# In[ ]:


r1.scenario['standard'].material['glass'].matdataIn_m


# In[ ]:


r1.calculateMassFlow()
r1.calculateEnergyFlow()


# In[ ]:


r1.calculateFlows()


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

# From this list, select the one that fits your study and select the type of plotting method. There are various plotting options:
# * `plotScenariosComparison`
# * `plotMaterialComparisonAcrossScenarios`
# * `plotMetricResults`: You can select the following keyword options: 'VirginStock', 'WasteALL', 'WasteEOL', 'WasteMFG'
# * `plotMaterialResults`
# * `plotInstalledCapacityResults`

# You can also view all the keywords you can use by calling the function without argumnets, or by printing the keys to the module data or the material data

# In[13]:


r1.plotScenariosComparison()


# In[14]:


r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_virgin_eff')


# In[15]:


r1.plotMaterialResults(keyword='VirginStock')


# In[16]:


r1.plotMetricResults()


# In[17]:


r1.plotInstalledCapacityResults()


# In[ ]:




