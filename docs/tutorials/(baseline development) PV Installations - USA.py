#!/usr/bin/env python
# coding: utf-8

# In[58]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 28})
plt.rcParams['figure.figsize'] = (30, 15)


# This journal documents the manipulation of PV installation data for the USA. This covers selection of data, and weighting by marketshare.

# In[65]:


cwd = os.getcwd() #grabs current working directory
df_installs_raw = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/PVInstalls_USA_AllSources.csv", index_col='Year')


# In[74]:


sources = df_installs_raw.columns
#print(len(sources))
plt.plot(df_installs_raw.index,df_installs_raw[sources[0]],lw=4,marker='*',label=sources[0])
plt.plot(df_installs_raw.index,df_installs_raw[sources[1]],lw=3,marker='o',label=sources[1])
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

# In[67]:


installs_2010_2019 = df_installs_raw.loc[(df_installs_raw.index>=2010) & (df_installs_raw.index<=2019)]
installs_recent = pd.DataFrame(installs_2010_2019[sources[0]])
installs_recent.columns = ['installed_pv_MW']
print(installs_recent)


# Only 1 dataset exists from 1995 to 2000, from IEA PVPS 2010 National Survey report. This seems to track reasonably well with Wood Mackenzie data between 2008 and 2010. Therefore, this will be used up to 2010. 

# In[82]:


installs_upto2010 = df_installs_raw.loc[(df_installs_raw.index<2010)]
installs_old = pd.DataFrame(installs_upto2010[sources[1]])
installs_old.columns = ['installed_pv_MW']
print(installs_old)


# However, there are 2 problems with this data. 1) There is an error in the original published table, such that it appears only 4 MW of PV were installed in 2006. To address this problem we will utilize SEIA & GTM/Wood Mackenzie data for 2006. 2) Due to the way the original data was presented, we had to calculate the difference between years to capture installed PV data, meaning that we don't have data for 1995. To address this problem, we will fill in the data point from “IEA PVPS Task 1 1997,” IEA-PVPS, IEA PVPS T1:1997, Mar. 1997. Accessed: Aug. 13, 2020. [Online]. Available: https://iea-pvps.org/wp-content/uploads/2020/01/tr_1995_01.pdf, which specifies the added PV in 1995 in the US (Table 2.2).
# 

# In[86]:


#dealing with 2006 error
installs_old['installed_pv_MW'][2006] = df_installs_raw[sources[5]][2006]

#dealing with 1995 error
installs_old['installed_pv_MW'][1995] = 12.5 #MW

#print(installs_old)


# ### Collect the installation data together into a single df

# In[87]:


installs = pd.concat([installs_old,installs_recent])
plt.plot(installs)
plt.yscale('log')


# # Marketshare weight the installation data for percent of Silicon vs Thin Film

# In addition to compiling a single installation record for 1995 through the present, this data is total cumulative, but the tool it currently considering silicon technology only. Especially in the United States, where First Solar holds significant marketshare, this distinction is important. Currently, we also do not feel it is critical track circular economy of CdTe given that First Solar already recycles all their panels.

# In[ ]:




