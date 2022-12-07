#!/usr/bin/env python
# coding: utf-8

# # Copper Energy Demands
# This journal documents the energy demands of mining, refining, drawing and recycling of copper for use inside the PV cell. Probably also applies to copper in wiring (not yet considered)

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (8, 4)
cwd = os.getcwd() #grabs current working directory


# ### Mining Energy

# In[2]:


cu_mining_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-copper-mining.csv",
                                     index_col='year')
cu_mining_raw.dropna(how='all')


# In[3]:


plt.scatter(cu_mining_raw.index, cu_mining_raw['E_CuMining_kWhpkg'], marker='o')
plt.title('CED_Cu_kWhpkg')
plt.ylabel('kWh/kg')


# In[12]:


#drop ones that include more than just mining and concentration.
cu_mining_raw.loc[1975] = np.nan
cu_mining_raw.loc[2010] = np.nan
cu_mining_raw.loc[2011] = np.nan


# In[15]:


plt.scatter(cu_mining_raw.index, cu_mining_raw['E_CuMining_kWhpkg'], marker='o')
plt.xlim(1995,2020)
plt.title('CED_Cu_kWhpkg')
plt.ylabel('kWh/kg')


# In[ ]:





# ### CED

# In[4]:


cu_CED_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-copper-CED.csv",
                                     index_col='year')
cu_CED_raw.dropna(how='all')


# In[5]:


plt.scatter(cu_CED_raw.index, cu_CED_raw['CED_Cu_kWhpkg'], marker='o')
plt.title('CED_Cu_kWhpkg')
plt.ylabel('kWh/kg')


# In[6]:


#drop the low outlier
cu_CED_raw.loc[1999] = np.nan
#drop the 2009 Nuss datapoint because it includes recycled content
cu_CED_raw.loc[2009] = np.nan
#drop 2012 EU survey, includes scrap content
cu_CED_raw.loc[2012] = np.nan


# The remaining lower energy points are associated with the difference between Hydro and Pyro metallurgy. 

# In[7]:


cu_CED_raw.loc[2000:2001,['Notes']]


# In[8]:


cu_CED_raw.loc[2006:2007,['Notes']]


# In[9]:


#find pyro data
cu_CED_trim = cu_CED_raw.dropna(how='all')
cu_CED_trim_pyro = cu_CED_trim[cu_CED_trim['Notes'].str.contains('pyro')]
cu_CED_trim_pyro#.index


# In[10]:


#find hydro data
cu_CED_trim_hydro = cu_CED_trim[cu_CED_trim['Notes'].str.contains('hydro')]
cu_CED_trim_hydro#.index


# In[11]:


plt.scatter(cu_CED_raw.index, cu_CED_raw['CED_Cu_kWhpkg'], marker='o')
plt.scatter(cu_CED_trim_pyro.index, cu_CED_trim_pyro['CED_Cu_kWhpkg'], marker='o')
plt.scatter(cu_CED_trim_hydro.index, cu_CED_trim_hydro['CED_Cu_kWhpkg'], marker='o')

plt.ylim(0,)
plt.title('CED_Cu_kWhpkg')
plt.ylabel('kWh/kg')


# Another way to go about the calculation of energy for primary Cu is to use the relationship between ore grade and energy demands. These appear regularly in literature, and history+projections of ore grade over time exist.

# In[ ]:





# In[ ]:





# In[ ]:




