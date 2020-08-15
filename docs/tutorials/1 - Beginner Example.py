#!/usr/bin/env python
# coding: utf-8

# # 1 - Beginner Example
# 
# 
# This journal shows how to load the baselines and run the dynamic mas flow analysis, plotting the results

# ### Step 1: import the CEMFC functions

# In[1]:


import CEMFC


# Here I am importing some plotting functions from matplotlib, and setting some of my preferences for displaying the plots, and other functions that we will need.

# In[2]:


import os
from pathlib import Path
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

font = {'family' : 'arial',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)


# ### Step 2: Create your Scenario Object
# 
# This will hold all the data for the modules and materials, metdata, etc. for your scenario. Other scenarios for  comparisons can be created afterwards based on this first scenario, so let's define it first.

# In[4]:



real=CEMFC.ScenarioObj()


# In[6]:


baselinefolder = Path().resolve().parent.parent / 'CEMFC' / 'baselines'

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\bifacial_radiance\TEMP')  

print ("Your simulation will be stored in %s" % baselinefolder)

file = os.path.join(baselinefolder,'baseline_modules_US.csv')


# ##  Step 3: Set the baseline for the Modules

# In[ ]:


real.set_baseline_module(file)


# #### Print some of the baseline values

# In[9]:


plt.plot(real.module['new_Installed_Capacity_[MW]'])


# In[ ]:




plt.plot(real.module['new_Installed_Capacity_[MW]'])


# #### Explore the contents of your scenario object:
# 

# In[10]:


real.__dict__


# ### Step 4: Load the Baseline for the Material being Analyzed

# In[ ]:




