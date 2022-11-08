#!/usr/bin/env python
# coding: utf-8

# # Energy Requirements of Aluminum Frames MFGing
# This journal documents the processing of literature data of the manufacturing energy of aluminum frames, from mining through extrusion, and recycling.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (10, 6)
cwd = os.getcwd() #grabs current working directory


# ### Aluminum LCI 2019
# This is a nice LCI/LCA from the International Aluminum Inst. updated in 2019. Pulling all the details in here.

# In[6]:


pd.read_excel(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/InternationalAluminumInst-2019-LCI-energyGLO.xlsx")


# This resource also has timelines of energy demand of the two most energy intensive steps over time.

# In[13]:


#alumina to aluminum
IAI_alumina_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/InternationalAluminumInst-1995-2021-PrimaryAluminaRefineEnergy-MJpTonne.csv",
                                     index_col='year')
IAI_alumina_raw


# In[21]:


IAI_alumina_kwhpkg = (IAI_alumina_raw*0.2777)/1000 #convert from MJ/tonne to kWh/kg
IAI_alumina_kwhpkg.loc[2001] = np.nan# drop the weirdness at 2001
IAI_alumina_kwhpkg.interpolate(inplace=True) #replace with interpolated data


# In[22]:


plt.plot(IAI_alumina_kwhpkg)
plt.legend(IAI_alumina_kwhpkg.columns)
plt.ylabel('kWh/kg')


# In[ ]:





# In[9]:


#Smelting energy
pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/InternationalAluminumInst-1995-2021-PrimaryAlSmeltEnergy-kWhpTonne.csv",
                                     index_col='year')


# In[ ]:





# In[ ]:





# In[ ]:





# ## Bauxite Mining

# In[7]:


#skipcols = ['Source', 'Notes','Country']
e_mineAl_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-mining.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[8]:


e_mineAl_raw.dropna(how='all')


# So this is a massively wide range. I have confidence in the International Aluminum Inst. LCI, but it is also the highest value. However, when compared to the other numbers from that report, it is still <1% of the overall energy demand

# In[ ]:





# In[ ]:





# ## Alumina Production

# In[ ]:





# In[ ]:





# In[ ]:





# ## Aluminum Smelting

# In[ ]:





# In[ ]:





# In[ ]:





# ## Casting, Extruding, Anodizing

# In[ ]:





# In[ ]:





# In[ ]:





# ## Cumulative Energy Demand Comparison

# In[ ]:





# In[ ]:





# In[ ]:





# ## Recycling

# In[11]:


#skipcols = ['Source', 'Notes','Country']
e_recycleAl_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-recycle.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[12]:


e_recycleAl_raw.dropna(how='all')


# The regular reported energy savings is that recycling is only ~5% of primary Al production. So either I can use these raw data, OR can take 5% of the CED of Al MFGing energy

# In[ ]:





# In[ ]:




