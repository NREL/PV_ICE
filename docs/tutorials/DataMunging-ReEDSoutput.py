#!/usr/bin/env python
# coding: utf-8

# # Data Munging ReEDS output data files for input installations

# To explore different scenarios for furture installation projections of PV (or any technology), ReEDS output data can be useful in providing standard scenarios. This input data will be used in the module files input to the PVDEMICE tool. Some will be used to explore middle, low and high projections, some for the Solar Futures Report. This journal extracts the data relevant for the current status of the PVDEMICE tool from ReEDS outputs.

# In[3]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[15]:


import os
from pathlib import Path

reedsFile = str(Path().resolve().parent.parent.parent / '2020-11-2-ReEDS Outputs Solar Futures ANL.xlsx')
testfolder = str(Path().resolve().parent.parent / 'PV_DEMICE' / 'TEMP')

print ("Input file is stored in %s" % reedsFile)
print ("Your simulation will be stored in %s" % testfolder)


# In[17]:


cwd = os.getcwd() #grabs current working directory
rawdf = pd.read_excel(reedsFile,
                        sheet_name="Solar Capacity (GW)",
                        index_col=[0,1,2,3]) #this casts scenario, year, PCA and State as levels


# ### First, split up the data by scenario

# In[66]:


#get the scenario names
scenario_names = rawdf.index.unique(level='scenario')
years = rawdf.index.unique(level='year')
print(scenario_names)


# In[50]:


#adv_tech = rawdf.loc[(rawdf.index.get_level_values('scenario')==scenario_names[0])]
#find a way to cycle through the full list of names with an appropriate variable name for each
#print(adv_tech.tail(10))


# The goal for the tool is to have annual installations projection 1995 through 2050.

# In[65]:


#returns a df with all scenarios, but installes are summed for each decade
decade_installs_byScenario = rawdf.groupby(['scenario', 'year']).sum()
print(decade_installs_byScenario)


# In[69]:


#Make a pretty plot to show scenarios
#for i in scenario_names:
plt.plot(decade_installs_byScenario.index['year'], decade_installs_byScenario.columns['Capacity (GW)'],marker='o',label=scenario_names[0])


# In[ ]:


#Are these cumulative or incremental capacity numbers?!?!


# In[ ]:


#Create data for between decades - interpolation non-linear


# In[ ]:


#print out separate csvs for each scenario

