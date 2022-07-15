#!/usr/bin/env python
# coding: utf-8

# # 1. First simulations with PV_ICE

# This notebook will guide you through the basic functionality of PV_ICE. Once you are done with this tutorial, you will be able to:
# * Set up a PV_ICE simulation and create scenarios.
# * Compute mass flow calculations.
# * Plot results.

# ### 1.1. Simulation setup

# To setup a PV_ICE simulation we need (1) import necessary packages, (2) create simulation folder path, (3) create a baseline path.
# 
# First let's import the necessary libraries for this notebook:

# In[1]:


import os
from pathlib import Path
import PV_ICE


# Let's set the folder where the **simulation** will be saved. By default, this is the TEMP folder in the PV_ICE distribution, however, we have created a TEMP folder in the present folder for simplicity.
# 
# *Note:* The lines below find the location of the folder relative to this Jupyter Journal, where `Path().resolve()` points at the current notebook absolute location, add `.parent` to navigate to previous folders and `/ 'folder' / ...` to navigate within a specific folder.. You can alternatively point to an empty directory (it will open a load GUI Visual Interface) or specify any other directory in your computer.
# 
# Using the same logic, setup the **baselines** folder. This is where all the baselines are stored in .csv format. A folder with multiple baselines can be found in the PV_ICE repository (PV_ICE/PV_ICE/baselines), you can always copy this folder and put it in a path of your choice. You may also create your own baselines (folowing the key structure used in PV_ICE for scenarios and materials).

# In[2]:


testfolder = str(Path().resolve() / 'TEMP') # Path to the simulation folder.

baselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE'/ 'PV_ICE' / 'baselines') # Path to baselines and data.

print ("Your simulation will be stored in {}, and your baselines are found in %s", testfolder)
print ("Your baselines are stored in %s", baselinesfolder)


# ### 2.2.  Create simulation object

# The simulation object will create a cointainer for all the different scenario(s) you might want to test. The method Simulation requires two inputs:
# * `name` for the simulation (in this example `Simulation_0`), if no name is given the program will autogenerate a default name with the current date
# * `path`, this is where we insert `testfolder` defined above, we named this simulation object `r1`

# In[3]:


r1 = PV_ICE.Simulation(name='Simulation_0', path=testfolder); # Is it possible to define more than one simulation here?
print(r1.name) # Shows the name of the simulation object
print(r1.path) # Shows the path of the simulation object


# *Warning:* If you re-run this cell it will mess with the path folder location by apending parent folders. To fix this, restart kernel and clear outputs!

# ### 3. Specify baseline scenario
# 
# In baselines there are scenarios representing average module for various situations, e.g. throughout US history. Let us load that scenario and name is `standard`:

# In[ ]:





# In[ ]:


r1.createScenario(name='standard0', file=baselinesfolder + '/baseline_modules_US.csv') # No popup in jupyter nor Code if I only provide directory IsADirectoryError: [Errno 21] Is a directory


# ### 4. Specify material(s)

# In[ ]:


r1.scenario['standard0'].addMaterial('glass', file=baselinesfolder + '/baseline_material_glass.csv')


# ### 5. Run the Mass Flow with Circulkar Pathways Calculations 

# In[ ]:


r1.calculateMassFlow()


# In[ ]:


r1.scenario['standard0'].data.head()


# ### 6. Plot mass flow results

# In[ ]:





# In[ ]:




r1.plotScenariosComparison() #keyError raised - KeyError: 'Cumulative_Area_disposedby_Failure'
# In[ ]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_EOL_Recycled_2_HQ')


# In[ ]:


import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

now = datetime.datetime.now()


# r1.createScenario(name='standard1', file=baselines + '/baseline_modules_US.csv') # No popup in jupyter nor Code if I only provide directory IsADirectoryError: [Errno 21] Is a directory

# In[ ]:


df = r1.scenario['standard0'].data


# In[ ]:


df.columns


# In[ ]:




