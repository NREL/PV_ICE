#!/usr/bin/env python
# coding: utf-8

# # 0 - quickStart Example

# #### 1. Create a folder for your simulation, and load PV ICE
# 
# First let's set the folder where the simulation will be saved. By default, this is the TEMP folder in the PV_ICE distribution.
# 
# The lines below find the location of the folder relative to this Jupyter Journal. You can alternatively point to an empty directory (it will open a load GUI Visual Interface) or specify any other directory in your computer, for example:
# 
# 

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


import PV_ICE


# ### 2. Create your Simulation Object
# 
# This will create the container for all the different scenario(s) you might want to test. We are also pointing to the testfolder defined above.

# In[3]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)


# ### 3. Specify your baseline Scenario 
# 
# We have put together scenarios representing the average module for various situations, for example throughout the US history. We will load this baseline scenario now, and it will be named ``standard``:

# In[4]:


r1.createScenario(name='standard', file=r'..\baselines\baseline_modules_US.csv')


# If a file is not provided, the automatic file loader will pop-up.
# 
# 
# 
# ### 4. Specify material(s)
# 
# We will add the material 'glass' to our simulation. Years of data must match, and they do if using the provided baselines.

# In[5]:


r1.scenario['standard'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')


# ### 5. Run the Mass Flow with Circular Pathways Calculations

# In[6]:


r1.calculateMassFlow()


# In[7]:


r1.scenario['standard'].data.head()


# ###  6. Plot Mass Flow Results

# In[8]:


r1.plotScenariosComparison(keyword='Cumulative_Area_disposedby_Failure')
r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_EOL_Recycled_2_HQ')

