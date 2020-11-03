#!/usr/bin/env python
# coding: utf-8

# # Data Munging ReEDS output data files for input installations

# To explore different scenarios for furture installation projections of PV (or any technology), ReEDS output data can be useful in providing standard scenarios. This input data will be used in the module files input to the PVDEMICE tool. Some will be used to explore middle, low and high projections, some for the Solar Futures Report. This journal extracts the data relevant for the current status of the PVDEMICE tool from ReEDS outputs.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[24]:


cwd = os.getcwd() #grabs current working directory
rawdf = pd.read_excel(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/2020-11-2-ReEDS Outputs Solar Futures ANL.xlsx",
                        sheet_name="Solar Capacity (GW)",
                        index_col=[0,1,2,3]) #this casts scenario, year, PCA and State as levels


# ### First, split up the data by scenario

# In[39]:


#get the scenario names
scenario_names = rawdf.index.unique(level='scenario')
print(scenario_names)


# In[40]:


adv_tech = rawdf.loc[(rawdf.index.get_level_values('scenario')==scenario_names[0])]
#find a way to cycle through the full list of names with an appropriate variable name for each
print(adv_tech.tail(10))


# In[ ]:




