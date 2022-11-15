#!/usr/bin/env python
# coding: utf-8

# # Calculations for PV CdTe installs, CdTe Market Share

# **UPDATE:** Since the data from CdTe was obtained from eia860 and the PV data afrom literature, there are conflicting values in the market share. Therefore I invite you to visit the notebook **EIA860 Processing - cSi CdTe Installation** for the most updated version of installs and market share, both for cSi and CdTe.

# This journal documents the manipulation of CdTe PV installation data for US installs. This covers selection of data, and weighting by marketshare.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


sns.set_style("white")

plt.rcParams.update({'font.size': 28})
plt.rcParams['figure.figsize'] = (30, 15)

cwd = os.getcwd() #grabs current working directory

supportMatfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
baselinesFolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines')


# #### Load new PV capacity generated from 2001 to 2021 by [eia](https://www.eia.gov/electricity/data/eia860/)
# 
# I downloaded the 2021 zip file and filtered for Thin Film (CdTe).

# In[3]:


df_cdte_installs = pd.read_excel(os.path.join(supportMatfolder, 'RELOG_PV_ICE.xlsx'), sheet_name='CdTe Capacity from eia')


# In[4]:


df_cdte_installs.columns


# In[5]:


df_cdte_installs_total = df_cdte_installs.drop(['Cummulative Capacity (MW)'], axis=1)
df_cdte_installs_total


# Group by year.

# In[6]:


df_cdte_installs_total_grouped = df_cdte_installs_total.groupby('Operating Year').sum()
df_cdte_installs_total_grouped


# Insert the years that don't have new capacity instlled.

# In[7]:


dict_missing = {'years' : list(range(2002,2008)), 'CdTe New Installs Capacity (MW)':[0, 0, 0, 0, 0, 0]}
missing_years = pd.DataFrame(dict_missing).set_index('years')
df_cdte_installs_total_grouped = pd.concat([df_cdte_installs_total_grouped, missing_years]).sort_index()
df_cdte_installs_total_grouped.columns
df_cdte_installs_total_grouped


# #### Load US all PV tech dataframe

# In[8]:


df_us_installs = pd.read_csv(os.path.join(supportMatfolder,'output_USA_allPV_installs.csv'), index_col='Year')
df_us_installs;


# #### Calculate market share

# In[9]:


df_cdte_installs_total_grouped['Total PV US installs (MW)'] = df_us_installs['installed_pv_MW']


# In[10]:


df_cdte_installs_total_grouped


# In[11]:


df_cdte_installs_total_grouped['Market share [%]'] = df_cdte_installs_total_grouped['CdTe New Installs Capacity (MW)']/df_cdte_installs_total_grouped['Total PV US installs (MW)']*100
df_cdte_installs_total_grouped


# #### Import Si installs and market share

# In[12]:


si_installs_us = pd.read_csv(os.path.join(supportMatfolder,'output_USA_SiPV_installs.csv'), index_col='Year')
si_installs_us;


# In[13]:


df_cdte_installs_total_grouped.loc[2009:2021]['CdTe New Installs Capacity (MW)']


# In[14]:


df_cdte_installs_total_grouped.describe()


# In[15]:


si_installs_us_baseline = pd.read_csv(os.path.join(baselinesFolder,'baseline_modules_mass_US.csv'), index_col='year')
si_installs_us_baseline = si_installs_us_baseline.iloc[1: , :]
si_installs_us_baseline['new_Installed_Capacity_[MW]'] = si_installs_us_baseline['new_Installed_Capacity_[MW]'].astype(float)
si_installs_us_baseline.info()


# In[16]:


plt.plot(df_cdte_installs_total_grouped.index,df_cdte_installs_total_grouped['CdTe New Installs Capacity (MW)'],lw=2,marker='*', label='CdTe New Installs')
plt.plot(df_cdte_installs_total_grouped.index,df_cdte_installs_total_grouped['Total PV US installs (MW)'],lw=2,marker='o', label='All PV Tech New Installs')
plt.plot(si_installs_us.index,si_installs_us['0'],lw=2,marker='.', label='Si New Installs')
plt.plot(range(1995, 2051), si_installs_us_baseline['new_Installed_Capacity_[MW]'],lw=2,marker='v', label='PV ICE baseline Si New Installs')


# ax = plt.gca()
# ax.set_ylim([-10, 10^5])
#plt.yscale('symlog') # This way we can see the zero values
#plt.ylim(0, 30000)
plt.ylim(0, 3000)
plt.xlim(2001, 2020)
plt.ylabel('PV Installed (MW)')
plt.xlabel('Years')
#plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left")
plt.legend(frameon=False, bbox_to_anchor=(1.05, 1.0), loc='upper left')
#plt.plot(df_installs_raw, marker='o')


# In[17]:


plt.plot(df_cdte_installs_total_grouped.index,df_cdte_installs_total_grouped['CdTe New Installs Capacity (MW)'],lw=2,marker='*', label='CdTe New Installs')
plt.plot(df_cdte_installs_total_grouped.index,df_cdte_installs_total_grouped['Total PV US installs (MW)'],lw=2,marker='o', label='All PV Tech New Installs')
plt.plot(si_installs_us.index,si_installs_us['0'],lw=2,marker='.', label='Si New Installs')
plt.plot(range(1995, 2051), si_installs_us_baseline['new_Installed_Capacity_[MW]'],lw=2,marker='v', label='PV ICE baseline Si New Installs')


# ax = plt.gca()
# ax.set_ylim([-10, 10^5])
#plt.yscale('symlog') # This way we can see the zero values
#plt.ylim(0, 30000)
plt.ylim(0, 3000)
plt.xlim(2001, 2020)
plt.ylabel('PV Installed (MW)')
plt.xlabel('Years')
#plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left")
plt.legend(frameon=False, bbox_to_anchor=(1.05, 1.0), loc='upper left')
#plt.plot(df_installs_raw, marker='o')


# #### Import Si market share

# In[18]:


si_maketshare_us = pd.read_csv(os.path.join(supportMatfolder,'output_USA_Si_marketshare.csv'), index_col='Year')
si_maketshare_us;


# In[19]:


plt.plot(si_maketshare_us.index,si_maketshare_us['All_Marketshare']*100,lw=2,marker='*', label='Si Market Share')
plt.plot(df_cdte_installs_total_grouped.index,df_cdte_installs_total_grouped['Market share [%]'],lw=2,marker='o', label='CdTe Market Share')

# ax = plt.gca()
# ax.set_ylim([-10, 10^5])
#plt.yscale('symlog') # This way we can see the zero values
#plt.ylim(0, 16000)

plt.ylabel('PV Maket Share (%)')
plt.xlabel('Years')
#plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left")
plt.legend(frameon=False, bbox_to_anchor=(1.05, 1.0), loc='upper left')
#plt.plot(df_installs_raw, marker='o')


# In[20]:


total_share = df_cdte_installs_total_grouped['Market share [%]'] + si_maketshare_us['All_Marketshare']*100


# In[21]:


total_share


# ### To do:
# 
# * Check out with Heather or Silvana why total market shares of Si and CdTe are over 100 in some instances.
# * Ask how to do the projection of CdTe over time. Do I assume a % growth of market share of CdTe over time and multiply it by the installed capacity of Solar Futures?

# In[ ]:





# In[ ]:




