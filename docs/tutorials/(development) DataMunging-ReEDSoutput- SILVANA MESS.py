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


# In[2]:


import os
from pathlib import Path

reedsFile = str(Path().resolve().parent.parent.parent / 'December Core Scenarios ReEDS Outputs Solar Futures.xlsx')
testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

print ("Input file is stored in %s" % reedsFile)
print ("Your simulation will be stored in %s" % testfolder)


# In[3]:


cwd = os.getcwd() #grabs current working directory
rawdf = pd.read_excel(reedsFile,
                        sheet_name="Solar Capacity (GW)")
                        #index_col=[0,2,3]) #this casts scenario, PCA and State as levels
#now set year as an index in place
rawdf.drop(columns=['State'], inplace=True)
rawdf.set_index(['scenario','year','PCA'], inplace=True)


# In[4]:


rawdf.index.get_level_values('scenario').unique()


# In[5]:


for ii in range (len(rawdf.unstack(level=1))):
    PCA = rawdf.unstack(level=1).iloc[ii].name[1]
    SCEN = rawdf.unstack(level=1).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = SCEN+'_'+PCA +'.csv'
    filetitle = os.path.join(testfolder, filetitle)
    A = rawdf.unstack(level=1).iloc[0]
    A = A.droplevel(level=0)
    A.name = 'new_Installed_Capacity_[MW]'
    pd.DataFrame(A).to_csv(filetitle)
    


# In[ ]:





# In[ ]:





# In[ ]:





# ## Playing with Multiindex Stuff

# In[7]:


rawdf.unstack(level=0).head()
rawdf.unstack(level=1).head()
rawdf.unstack(level=2).head()


# In[8]:


rawdf.unstack(level=1).iloc[0]


# In[9]:


rawdf.unstack(level=1).iloc[2].name[1]


# In[10]:


rawdf.loc[('Reference.Mod',2010)].head()


# In[11]:


scenarios = rawdf.groupby(level=0)
PCA = rawdf.groupby(level=2)


# In[12]:


for a,b in scenarios:
    for c,d in PCA:
        print(a, c)


# In[13]:


PCAs = rawdf.index.get_level_values('PCA').unique()
scenarios = rawdf.index.get_level_values('scenario').unique()
years = rawdf.index.get_level_values('year').unique()


# In[14]:


rawdf.loc[(scenarios[1])].head()


# In[15]:


rawdf.loc[scenarios[1]].head()


# In[16]:


rawdf.loc[[scenarios[1]]].head()


# In[ ]:




