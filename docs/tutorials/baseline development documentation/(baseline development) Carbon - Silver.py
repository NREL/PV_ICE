#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (10, 6)
cwd = os.getcwd() #grabs current working directory
carbonfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial' / 'CarbonIntensities')
supportmatfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')


# # Manufacturing by country
# We appear to only have mine production data, which may not be a good representation of where silver is refined, but lacking other data, we will use country market share of mining data from the World Silver Survey and USGS.

# In[130]:


ag_WSS2023_raw = pd.read_csv(os.path.join(carbonfolder, 'input-worldsilversurvey2023-silverminebycountry.csv'),
                                     index_col=0)#, usecols=lambda x: x not in skipcols)
ag_WSS2014_raw = pd.read_csv(os.path.join(carbonfolder, 'input-worldsilversurvey2014-silverminebycountry.csv'),
                                     index_col=0)#, usecols=lambda x: x not in skipcols)
ag_USGS_raw = pd.read_csv(os.path.join(carbonfolder, 'input-USGS-silverminebycountry.csv'),
                                     index_col=0)#, usecols=lambda x: x not in skipcols)


# In[131]:


ag_WSS = pd.concat([ag_WSS2014_raw,ag_WSS2023_raw]).groupby(['Mine Production Million Ounces']).sum()
ag_WSS_kg = ag_WSS*0.02835*1e6 #convert to kg
ag_WSS_kg = ag_WSS_kg.rename_axis('MineProduction_[kg]')
ag_WSS_kg = ag_WSS_kg.fillna(0)

ag_USGS = ag_USGS_raw.interpolate()


# In[132]:


ag_USGS_raw.interpolate()


# In[139]:


#compare the values of the two dataframes
common = ag_USGS.index.intersection(ag_WSS_kg.index)
common_yrs = ag_USGS.columns.intersection(ag_WSS_kg.columns)

ag_USGS.loc[common,common_yrs]/ag_WSS_kg.loc[common,common_yrs]


# So it looks like on average, USGS is reporting higher than the world silver survey, but it is really inconsistent. MAybe I will take both dataframes through the process, and see if they come out with the same countries that matter.

# In[142]:


#USGS country market share
ag_USGS['SUM'] = ag_USGS.sum(axis=1)
ag_USGS_mrktshr = ag_USGS.div(ag_USGS['SUM'], axis=0)*100
#ag_USGS_mrktshr


# In[143]:


ag_WSS_kg['SUM'] = ag_WSS_kg.sum(axis=1)
ag_WSS_mrktshr = ag_WSS_kg.div(ag_WSS_kg['SUM'], axis=0)*100
#ag_WSS_mrktshr


# In[ ]:





# In[141]:


#compare the values of the two dataframes
common = ag_USGS_mrktshr.index.intersection(ag_WSS_mrktshr.index)
common_yrs = ag_USGS_mrktshr.columns.intersection(ag_WSS_mrktshr.columns)

ag_USGS_mrktshr.loc[common,common_yrs]/ag_WSS_mrktshr.loc[common,common_yrs]


# In[ ]:





# In[110]:


pd.merge(ag_USGS_raw, ag_WSS_kg, on='MineProduction_[kg]', how='outer', indicator='indicator_col')


# In[77]:


ag_USGS_raw.join(ag_WSS_kg, how='outer', lsuffix='_USGS',rsuffix='_WSS')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




