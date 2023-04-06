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


# In[22]:


plt.scatter(e_peteva_mfging_raw.index,e_peteva_mfging['E_mfg_sum_kWhpkg'], marker='P', label='sum')
plt.scatter(e_peteva_mfging_raw.index,e_peteva_mfging_raw.iloc[:,3], label='fuel', color='red')
plt.scatter(e_peteva_mfging.index,e_peteva_mfging.iloc[:,0], label='electricity', color='black')
plt.title('Energy mfging (electricity+fuel)')
plt.ylabel('[kWh/kg]')
plt.ylim(0,)
plt.legend()


# In[13]:


e_peteva_mfging_PET = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('PET', na = False)]
e_peteva_mfging_LDPE = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('LDPE', na = False)]
e_peteva_mfging_ethylene = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('ethylene', na = False)]
e_peteva_mfging_eva = e_peteva_mfging[e_peteva_mfging['Notes'].str.contains('EVA', na = False)]


# In[32]:


plt.scatter(e_peteva_mfging_eva.index, e_peteva_mfging_eva['E_mfg_sum_kWhpkg'], label='eva', marker='^', s=60)
plt.scatter(e_peteva_mfging_ethylene.index, e_peteva_mfging_ethylene['E_mfg_sum_kWhpkg'], label='ethylene')
plt.title('Energy mfging (electricity+fuel): EVA')
plt.ylabel('[kWh/kg]')
plt.xlim(1995,2023)
plt.ylim(0,)
plt.legend()


# In[33]:


e_peteva_mfging_eva


# In[15]:


e_peteva_mfging_ethylene


# Ethylene is used to make EVA at ~1:1, the vinyl acetate component is lower, ~20%. It is still disturbing that the energy for ethylene seems to be higher than the sum of the processes for EVA...
# 
# I am going to take the 2000 value from Ecoinvent and Nicholson et al 2021 using MFI data from 2019 and interpolate for EVA.
# 
# ## EVA: granulate production

# In[17]:


idx_temp = pd.Series(range(1995,2051,1))
E_mfg_eva_temp = pd.DataFrame(index=idx_temp)
E_mfg_eva_temp.loc[2000,'E_mfg_eva_kWhpkg'] = e_peteva_mfging_eva.loc[2000,'E_mfg_sum_kWhpkg']
E_mfg_eva_temp.loc[2019,'E_mfg_eva_kWhpkg'] = e_peteva_mfging_eva.loc[2019,'E_mfg_sum_kWhpkg']
E_mfg_eva_temp.loc[2000,'E_mfg_eva_fuelfraction'] = e_peteva_mfging_eva.loc[2000,'E_mfg_FUEL_kWhpkg']/e_peteva_mfging_eva.loc[2000,'E_mfg_sum_kWhpkg']
E_mfg_eva_temp.loc[2019,'E_mfg_eva_fuelfraction'] = e_peteva_mfging_eva.loc[2000,'E_mfg_FUEL_kWhpkg']/e_peteva_mfging_eva.loc[2019,'E_mfg_sum_kWhpkg']


# In[18]:


E_mfg_eva = E_mfg_eva_temp.interpolate(limit_direction='both')


# In[44]:


fig, ax1 = plt.subplots()

ax1.plot(E_mfg_eva['E_mfg_eva_kWhpkg'], label='Total Energy: EVA')
plt.scatter(e_peteva_mfging_raw.index,e_peteva_mfging['E_mfg_sum_kWhpkg'], marker='P', color='black', label='raw all plastics')
ax1.scatter(e_peteva_mfging_eva.index,e_peteva_mfging_eva.iloc[:,0], label='raw eva', marker='^', s=60)
plt.scatter(e_peteva_mfging_ethylene.index, e_peteva_mfging_ethylene['E_mfg_sum_kWhpkg'], label='raw ethylene')

ax1.set_ylim(0,10)
ax1.set_ylabel('Energy Demand[kWh/kg]')

ax2 = ax1.twinx()
ax2.plot(E_mfg_eva['E_mfg_eva_fuelfraction']*100, color='red', label='Fuel Fraction')
#ax2.scatter(E_mfg_eva.index,E_mfg_eva.iloc[:,1], color='red', marker='^', label='fuel fraction data')
ax2.set_ylim(0,100)
plt.ylabel('Fuel Fraction [%]', color='red')
ax2.tick_params(axis='y', color='red', labelcolor='red')

plt.xlim(1979,2025)
plt.title('Energy Total: EVA granulate Production')

ax1.legend(loc='upper right')
#ax2.legend(loc='upper right')
plt.show()


# # PET
# All backsheet materials that are not PP based (which is a small marketshare) have a PET interlayer. Therefore, we will include the energy of PET manufacture to add to PVDF for creating backsheet energy flows.

# In[93]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_backsheetPET_mfg_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-backsheetPET-mfging.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[94]:


e_backsheetPET_mfg_raw.dropna(how='all')


# In[96]:


plt.scatter(e_backsheetPET_mfg_raw.index, e_backsheetPET_mfg_raw.iloc[:,0], label='electricity', )
plt.scatter(e_backsheetPET_mfg_raw.index, e_backsheetPET_mfg_raw.iloc[:,3], label='fuel')
plt.title('Energy backsheet PET mfging')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# The two high points are CEDs. Exclude and replot

# In[103]:


e_backsheetPET_mfg = e_backsheetPET_mfg_raw.copy()
e_backsheetPET_mfg.loc[2018] = np.nan
e_backsheetPET_mfg.loc[2020] = np.nan

e_backsheetPET_mfg['E_sum_kWhpkg'] = e_backsheetPET_mfg['E_mfg_kWhpkg']+e_backsheetPET_mfg['E_mfg_FUEL_kWhpkg']
e_backsheetPET_mfg['E_fuelfraction_kWhpkg'] = e_backsheetPET_mfg['E_mfg_FUEL_kWhpkg']/e_backsheetPET_mfg['E_sum_kWhpkg']


# In[102]:


plt.scatter(e_backsheetPET_mfg.index, e_backsheetPET_mfg.iloc[:,0], label='electricity', )
plt.scatter(e_backsheetPET_mfg.index, e_backsheetPET_mfg.iloc[:,3], label='fuel')
plt.scatter(e_backsheetPET_mfg.index, e_backsheetPET_mfg.iloc[:,6], label='sum', marker='P', color='black')

plt.title('Energy backsheet PET mfging')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# In[105]:


e_backsheetPET_mfg.dropna(how='all')


# With this lovely scatter plot, we're going to use 4 kWh/kg for total energy and fuel fraction of 80%

# In[106]:


idx_temp = pd.Series(range(1995,2051,1))
E_mfg_pet = pd.DataFrame(index=idx_temp)
E_mfg_pet.loc[:,'E_mfg_pet_kWhpkg'] = 4.0
E_mfg_pet.loc[:,'E_mfg_petFUEL_kWhpkg'] = 0.8


# # PVDF granulate energy
# PVDF and PVF

# In[73]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_backsheet_mfg_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-backsheet-mfging.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[74]:


e_backsheet_mfg_raw.dropna(how='all')


# In[75]:


plt.scatter(e_backsheet_mfg_raw.index, e_backsheet_mfg_raw.iloc[:,0], label='electricity', )
plt.scatter(e_backsheet_mfg_raw.index, e_backsheet_mfg_raw.iloc[:,3], label='fuel')
plt.title('Energy backsheet mfging')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# In[76]:


e_backsheet_mfg_route1 = e_backsheet_mfg_raw[e_backsheet_mfg_raw['Notes'].str.contains('Route 1', na = False)]
e_backsheet_mfg_route2 = e_backsheet_mfg_raw[e_backsheet_mfg_raw['Notes'].str.contains('Route 2', na = False)]
e_backsheet_mfg_raw['E_sum_kWhpkg'] = e_backsheet_mfg_raw['E_mfg_kWhpkg']+e_backsheet_mfg_raw['E_mfg_FUEL_kWhpkg']


# In[78]:


plt.scatter(e_backsheet_mfg_raw.index, e_backsheet_mfg_raw.iloc[:,0], label='electricity', )
plt.scatter(e_backsheet_mfg_raw.index, e_backsheet_mfg_raw.iloc[:,3], label='fuel')

plt.scatter(e_backsheet_mfg_route1.index, e_backsheet_mfg_route1.iloc[:,0], label='Route1')
plt.scatter(e_backsheet_mfg_route2.index, e_backsheet_mfg_route2.iloc[:,0], label='Route2')

plt.scatter(e_backsheet_mfg_raw.index, e_backsheet_mfg_raw.loc[:,'E_sum_kWhpkg'], label='sum', color='black', marker='P')

plt.title('Energy backsheet mfging')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# The lack of detailed LCIs for PVF or PVDF that are industry based makes the two studies which examine the synthesis paths are likely the best resources. The 1995 and 2005 data are based on rough estimates from other plastics. Hu 2022 is based on Abbasi 2014, but somehow comes up with a wider range of energy associate wtih the two synthesis paths studied. Even Abbasi has estimations of energy demand, but there is a partial eletricity vs fuel breakdown. 
# 
# Therefore, we will use the average of the two routes from Abbasi and apply the higher fuel fraction (there a several heating steps that at industrial scale are likely to be done with natgas.

# In[86]:


mean_abbasi = (e_backsheet_mfg_raw.loc[2011,'E_mfg_kWhpkg']+e_backsheet_mfg_raw.loc[2012,'E_mfg_kWhpkg'])/2
print('The average of Abbasi Route 1 and 2 is '+str(mean_abbasi)+' kWh/kg')


# In[90]:


fuelfraction_abbasi = e_backsheet_mfg_raw.loc[2014,'E_mfg_FUEL_kWhpkg']/e_backsheet_mfg_raw.loc[2014,'E_sum_kWhpkg']
print('The fuel fraction of Abassi from Route 1 is '+str(fuelfraction_abbasi))


# In[91]:


idx_temp = pd.Series(range(1995,2051,1))
E_mfg_pvdf = pd.DataFrame(index=idx_temp)
E_mfg_pvdf.loc[:,'E_mfg_pvdf_kWhpkg'] = mean_abbasi
E_mfg_pvdf.loc[:,'E_mfg_pvdfFUEL_kWhpkg'] = fuelfraction_abbasi


# # Forming energy
# Turning granulate polymer into sheets

# In[107]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_plastic_sheet_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-plastic-forming.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[108]:


e_plastic_sheet_raw.dropna(how='all')


# In[110]:


plt.scatter(e_plastic_sheet_raw.index, e_plastic_sheet_raw.iloc[:,0], label='electricity', )
plt.scatter(e_plastic_sheet_raw.index, e_plastic_sheet_raw.iloc[:,3], label='fuel')
plt.title('Energy sheet forming')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# In[ ]:





# In[ ]:





# In[ ]:




