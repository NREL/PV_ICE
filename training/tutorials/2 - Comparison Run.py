#!/usr/bin/env python
# coding: utf-8

# # 2 - Comparison Run
# 
# **Objectives:**
# 1. Read in necessary mass and energy data
# 2. Run
# 3. Generate plots 

# ## 1. Setup and Create PV ICE Simulation Object

# In[ ]:


# if running on google colab, uncomment the next line and execute this cell to install the dependencies and prevent "ModuleNotFoundError" in later cells:
get_ipython().system('pip install git+https://github.com/NREL/PV_ICE.git@development')


# In[ ]:


import PV_ICE
import os
PV_ICE.__version__


# In[ ]:


pwd


# In[ ]:


testfolder = 'Second'

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[ ]:


r1 = PV_ICE.Simulation(name='Sim2', path=testfolder, baselinepath='/content'); # Is it possible to define more than one simulation here?


# ## 2. Modify the files and add to the folder now 
# 
# Let's discuss as a group what would be a good scenario comparison to define.

# In[1]:


#from google.colab import files
#files.upload()


# ## 3. Create standard and modified scenarios
# 

# In[ ]:


r1.createScenario(name='standard', 
                  massmodulefile=r'baseline_modules_mass_US.csv', 
                  energymodulefile = 'baseline_modules_energy.csv' )

r1.scenario['standard'].addMaterial(materialname='glass', 
                                    massmatfile='/content/baseline_material_mass_glass.csv', 
                                    energymatfile='/content/baseline_material_energy_glass.csv')

r1.scenario['standard'].addMaterial(materialname='glass', 
                                    massmatfile='/content/baseline_material_mass_glass.csv', 
                                    energymatfile='/content/baseline_material_energy_glass.csv')


# In[ ]:


r1.createScenario(name='modified', 
                  massmodulefile=r'baseline_modules_mass_US_modified.csv', 
                  energymodulefile = 'baseline_modules_energy.csv' )

r1.scenario['modified'].addMaterial(materialname='glass', 
                                    massmatfile='/content/baseline_material_mass_glass_modified.csv', 
                                    energymatfile='/content/baseline_material_energy_glass.csv')

r1.scenario['modified'].addMaterial(materialname='silicon', 
                                    massmatfile='/content/baseline_material_mass_glass_modified.csv', 
                                    energymatfile='/content/baseline_material_energy_glass.csv')


# Alternatively, use one of the PV_ICE support functions to modify 
# 
# * modifyScenario
# * modifyScenario Energy
# 
# or 
# * scenMod_PerfectManufacturing
# * scenMod_noCircularity
# * scenMod_perfectRecycling
# * scenMod_IRENIFY
# 

# ## 4. Run the flows 

# In[ ]:


r1.calculateFlows()


# ## 5. Aggregate Results

# In[ ]:


USyearly, UScum = r1.aggregateResults()


# ## 6. Save Simulation
# 

# In[ ]:


r1.saveSimulation()


# ## 7. Use internal plotting functions to plot results

# From this list, select the one that fits your study and select the type of plotting method. There are various plotting options:
# * `plotScenariosComparison`
# * `plotMaterialComparisonAcrossScenarios`
# * `plotMetricResults`: You can select the following keyword options: 'VirginStock', 'WasteALL', 'WasteEOL', 'WasteMFG'
# * `plotMaterialResults`
# * `plotInstalledCapacityResults`

# You can also view all the keywords you can use by calling the function without argumnets, or by printing the keys to the module data or the material data

# In[ ]:


r1.plotMetricResults()


# In[ ]:


r1.plotScenariosComparison()


# In[ ]:


r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_virgin_eff')


# In[ ]:


r1.plotMaterialResults(keyword='VirginStock')


# In[ ]:


r1.plotInstalledCapacityResults()

