#!/usr/bin/env python
# coding: utf-8

# # 1 - Basics run
# 
# **Requirements:**
# - Files linked via URL.
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
PV_ICE.__version__


# In[ ]:


testfolder = 'Tuesday'

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[ ]:


r1 = PV_ICE.Simulation(name='Sim1', path=testfolder); # Is it possible to define more than one simulation here?


# In[ ]:


r1


# PV ICE uses <i>object oriented programing</i>, so this created a ``PV_ICE.main.Simulation`` Object. An Object is data field that has unique attributes and behaviors. We can crack open objects with the `.__dict__` command

# In[ ]:


r1.__dict__


# In[ ]:


r1.baselinepath = '/content'


# ## 2. Add the Files to the Folder now
# 
# Drag the files to the `/content` folder 
# 
# Alternatively, the cell below can open a upload window

# In[ ]:


#from google.colab import files
#files.upload()


# ## 3. Create your Scenario
# 
# First create scenario and add its module files 

# In[ ]:


r1.createScenario(name='standard', 
                  massmodulefile=r'baseline_modules_mass_US.csv', 
                  energymodulefile = 'baseline_modules_energy.csv' )


# Then add at least one material file

# In[ ]:


r1.scenario['standard'].addMaterial(materialname='glass', 
                                    massmatfile='/content/baseline_material_mass_glass.csv', 
                                    energymatfile='/content/baseline_material_energy_glass.csv')


# We can explore the module and material objects now. For example:

# In[ ]:


r1.scenario['standard'].material['glass']


# In[ ]:


r1.scenario['standard'].material['glass'].__dict__


# In[ ]:


r1.scenario['standard'].material['glass'].matdataIn_m


# ## 4. Run the flows 

# In[ ]:


r1.calculateMassFlow()


# In[ ]:


r1.calculateEnergyFlow()


# Same thing, but together 

# In[ ]:


r1.calculateFlows()


# We can explore the outputs. They are still a bit raw at this step

# In[ ]:


r1.scenario['standard'].dataOut_m.keys()


# ## 5. Aggregate Results

# In[ ]:


USyearly, UScum = r1.aggregateResults()

# The results are also saved into the simulation object itself:
# r1.USyearly
# r1.UScum


# In[ ]:


USyearly.keys()


# In[ ]:


UScum.keys()


# ## 6. Save Simulation
# 
# This is useful to see the inputs (in case you modified the values with some of the support functions), the full dataframes of internal processing data, and the outputs in an organized manner

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

