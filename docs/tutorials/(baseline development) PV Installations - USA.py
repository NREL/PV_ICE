#!/usr/bin/env python
# coding: utf-8

# In[37]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 28})
plt.rcParams['figure.figsize'] = (30, 15)


# This journal documents the manipulation of PV installation data for the USA. This covers selection of data, and weighting by marketshare.

# In[38]:


cwd = os.getcwd() #grabs current working directory
df_installs_raw = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/PVInstalls-USA-AllSources.csv", index_col='Year')


# In[39]:


sources = df_installs_raw.columns
#print(len(sources))
plt.plot(df_installs_raw.index,df_installs_raw[sources[0]],lw=2,marker='o',label=sources[0])
plt.plot(df_installs_raw.index,df_installs_raw[sources[1]],lw=2,marker='o',label=sources[1])
plt.plot(df_installs_raw.index,df_installs_raw[sources[2]],lw=2,marker='o',label=sources[2])
plt.plot(df_installs_raw.index,df_installs_raw[sources[3]],lw=2,marker='o',label=sources[3])
plt.plot(df_installs_raw.index,df_installs_raw[sources[4]],lw=2,marker='o',label=sources[4])
plt.plot(df_installs_raw.index,df_installs_raw[sources[5]],lw=2,marker='o',label=sources[5])
plt.yscale('log')
plt.ylabel('PV Installed (MW)')
plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left")
#plt.plot(df_installs_raw, marker='o')


# # Select the data to use for installs

# The IRENA is consistently lower than the other sources from 2012 through the present. Given that all other sources are in agreement, we will select one of these data sets to use for installation data, rather than IRENA. In this case, we will select the Wood Mackenzie Power & Renewables quarterly reports and PV forecasts from 2010 through 2019.

# In[51]:


installs_2010_2019 = df_installs_raw.loc[(df_installs_raw.index>=2010) & (df_installs_raw.index<=2019)]
installs_recent = pd.DataFrame(installs_2010_2019[sources[0]])
installs_recent.columns = ['installed_pv_MW']
print(installs_recent)


# Only 1 dataset exists from 1995 to 2000, from IEA PVPS 2010 National Survey report.

# In[ ]:





# # Marketshare weight the installation data for percent of Silicon vs Thin Film

# In[ ]:




