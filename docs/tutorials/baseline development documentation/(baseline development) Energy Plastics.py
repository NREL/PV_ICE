#!/usr/bin/env python
# coding: utf-8

# # Plastics Energies
# This journal covers the energy requirements of different lifecycle stages for the encapsulant and Backsheet. This includes manufacturing, incineration and recycling. This is the electrical and heating energies of the process, not the CED.
# 
# The main focus materials are EVA, PET, and PVDF.
# 
# EVA, the encapsulant, is made from ethylene and vinyl acetate.
# 
# PET, a standard plastic, is well documented and typically forms a layer of the backsheet. PET is the polymerization of ethylene.
# 
# PVF, also known as Tedlar, is part of the backsheet and is formed by: PVF<-vinylfluoride<-difluoroethane<-acetylene<-natgas (ecoinvent). PVDF, also known as Kynar is similar and newer. Both formulations are proprietary and exact synthesis is unknown. 

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (10, 6)
cwd = os.getcwd() #grabs current working directory


# In[2]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_peteva_mfging_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-plastics-mfging.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[3]:


e_peteva_mfging_raw.dropna(how='all')


# In[4]:


e_peteva_mfging_CEDs = e_peteva_mfging_raw[e_peteva_mfging_raw['Notes'].str.contains('CED', na = False)]
e_peteva_mfging_CEDs


# In[5]:


plt.scatter(e_peteva_mfging_raw.index,e_peteva_mfging_raw.iloc[:,0])
plt.scatter(e_peteva_mfging_CEDs.index, e_peteva_mfging_CEDs.iloc[:,0], color='black')
plt.title('Electricity: Ethylene, LDPE mfging')
plt.ylabel('[kWh/kg]')


# In[6]:


e_peteva_mfging_CEDs.index


# In[7]:


e_peteva_mfging = e_peteva_mfging_raw
e_peteva_mfging.loc[e_peteva_mfging_CEDs.index,:]=np.nan
#e_peteva_mfging.head(20)


# In[8]:


e_peteva_mfging_PET = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('PET', na = False)]
e_peteva_mfging_LDPE = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('LDPE', na = False)]
e_peteva_mfging_ethylene = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('ethylene', na = False)]
e_peteva_mfging_eva = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('EVA', na = False)]


# In[9]:


plt.scatter(e_peteva_mfging.index,e_peteva_mfging.iloc[:,0], label='all', color='black')
plt.scatter(e_peteva_mfging_PET.index,e_peteva_mfging_PET.iloc[:,0], label='PET', color='yellow', marker='^')
plt.scatter(e_peteva_mfging_LDPE.index,e_peteva_mfging_LDPE.iloc[:,0], label='LDPE', color='blue', marker='*')
plt.scatter(e_peteva_mfging_ethylene.index,e_peteva_mfging_ethylene.iloc[:,0], label='ethylene', color='pink', marker='v')
plt.scatter(e_peteva_mfging_eva.index,e_peteva_mfging_eva.iloc[:,0], label='EVA', color='green', marker='P')
plt.title('Electricity: mfging')
plt.ylabel('[kWh/kg]')
plt.legend()


# In[10]:


plt.scatter(e_peteva_mfging_raw.index,e_peteva_mfging_raw.iloc[:,3], color='red')
plt.scatter(e_peteva_mfging_CEDs.index, e_peteva_mfging_CEDs.iloc[:,3], color='black', label='CED')

plt.scatter(e_peteva_mfging_PET.index,e_peteva_mfging_PET.iloc[:,3], label='PET', color='yellow', marker='^')
plt.scatter(e_peteva_mfging_LDPE.index,e_peteva_mfging_LDPE.iloc[:,3], label='LDPE', color='blue', marker='*')
plt.scatter(e_peteva_mfging_ethylene.index,e_peteva_mfging_ethylene.iloc[:,3], label='ethylene', color='pink', marker='v')
plt.scatter(e_peteva_mfging_eva.index,e_peteva_mfging_eva.iloc[:,3], label='EVA', color='green', marker='P')

plt.title('Fuel: Ethylene, LDPE mfging')
plt.ylabel('[kWh/kg]')
plt.legend()


# In[11]:


# sum the electricity and fuel
e_peteva_mfging['E_mfg_sum_kWhpkg'] = e_peteva_mfging['E_mfg_kWhpkg']+e_peteva_mfging['E_mfg_FUEL_kWhpkg']


# In[12]:


plt.scatter(e_peteva_mfging_raw.index,e_peteva_mfging['E_mfg_sum_kWhpkg'], marker='P')
plt.scatter(e_peteva_mfging_raw.index,e_peteva_mfging_raw.iloc[:,3], color='red')
plt.scatter(e_peteva_mfging.index,e_peteva_mfging.iloc[:,0], label='all', color='black')
plt.title('Energy mfging (electricity+fuel)')
plt.ylabel('[kWh/kg]')


# In[13]:


e_peteva_mfging_PET = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('PET', na = False)]
e_peteva_mfging_LDPE = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('LDPE', na = False)]
e_peteva_mfging_ethylene = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('ethylene', na = False)]
e_peteva_mfging_eva = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('EVA', na = False)]


# In[14]:


plt.scatter(e_peteva_mfging_eva.index, e_peteva_mfging_eva['E_mfg_sum_kWhpkg'])
plt.title('Energy mfging (electricity+fuel): EVA')
plt.ylabel('[kWh/kg]')
plt.xlim(1995,2023)


# In[15]:


e_peteva_mfging_ethylene


# In[16]:


plt.scatter(e_peteva_mfging_ethylene.index, e_peteva_mfging_ethylene['E_mfg_sum_kWhpkg'])
plt.title('Energy mfging (electricity+fuel): Ethylene')
plt.ylabel('[kWh/kg]')
plt.xlim(1995,2023)


# Ethylene is used to make EVA at ~1:1, the vinyl acetate component is lower, ~20%. It is still disturbing that the energy for ethylene seems to be higher than the sum of the processes for EVA...
# 
# I am going to take the 2000 value from Ecoinvent and Nicholson et al 2021 using MFI data from 2019 and interpolate for EVA.
# 
# ## EVA

# In[24]:


idx_temp = pd.Series(range(1995,2051,1))
E_mfg_eva_temp = pd.DataFrame(index=idx_temp)
E_mfg_eva_temp.loc[2000,'E_mfg_eva_kWhpkg'] = e_peteva_mfging_eva.loc[2000,'E_mfg_sum_kWhpkg']
E_mfg_eva_temp.loc[2019,'E_mfg_eva_kWhpkg'] = e_peteva_mfging_eva.loc[2019,'E_mfg_sum_kWhpkg']
E_mfg_eva_temp.loc[2000,'E_mfg_eva_fuelfraction'] = e_peteva_mfging_eva.loc[2000,'E_mfg_FUEL_kWhpkg']/e_peteva_mfging_eva.loc[2000,'E_mfg_sum_kWhpkg']
E_mfg_eva_temp.loc[2019,'E_mfg_eva_fuelfraction'] = e_peteva_mfging_eva.loc[2000,'E_mfg_FUEL_kWhpkg']/e_peteva_mfging_eva.loc[2019,'E_mfg_sum_kWhpkg']


# In[28]:


E_mfg_eva = E_mfg_eva_temp.interpolate(limit_direction='both')


# In[29]:


E_mfg_eva


# In[ ]:




