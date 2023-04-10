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


# In[14]:


plt.scatter(e_peteva_mfging_eva.index, e_peteva_mfging_eva['E_mfg_sum_kWhpkg'], label='eva', marker='^', s=60)
plt.scatter(e_peteva_mfging_ethylene.index, e_peteva_mfging_ethylene['E_mfg_sum_kWhpkg'], label='ethylene')
plt.title('Energy mfging (electricity+fuel): EVA')
plt.ylabel('[kWh/kg]')
plt.xlim(1995,2023)
plt.ylim(0,)
plt.legend()


# In[15]:


e_peteva_mfging_eva


# In[16]:


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


# In[19]:


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

# In[20]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_backsheetPET_mfg_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-backsheetPET-mfging.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[21]:


e_backsheetPET_mfg_raw.dropna(how='all')


# In[22]:


plt.scatter(e_backsheetPET_mfg_raw.index, e_backsheetPET_mfg_raw.iloc[:,0], label='electricity', )
plt.scatter(e_backsheetPET_mfg_raw.index, e_backsheetPET_mfg_raw.iloc[:,3], label='fuel')
plt.title('Energy backsheet PET mfging')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# The two high points are CEDs. Exclude and replot

# In[23]:


e_backsheetPET_mfg = e_backsheetPET_mfg_raw.copy()
e_backsheetPET_mfg.loc[2018] = np.nan
e_backsheetPET_mfg.loc[2020] = np.nan

e_backsheetPET_mfg['E_sum_kWhpkg'] = e_backsheetPET_mfg['E_mfg_kWhpkg']+e_backsheetPET_mfg['E_mfg_FUEL_kWhpkg']
e_backsheetPET_mfg['E_fuelfraction_kWhpkg'] = e_backsheetPET_mfg['E_mfg_FUEL_kWhpkg']/e_backsheetPET_mfg['E_sum_kWhpkg']


# In[24]:


plt.scatter(e_backsheetPET_mfg.index, e_backsheetPET_mfg.iloc[:,0], label='electricity', )
plt.scatter(e_backsheetPET_mfg.index, e_backsheetPET_mfg.iloc[:,3], label='fuel')
plt.scatter(e_backsheetPET_mfg.index, e_backsheetPET_mfg.iloc[:,6], label='sum', marker='P', color='black')

plt.title('Energy backsheet PET mfging')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# In[25]:


e_backsheetPET_mfg.dropna(how='all')


# With this lovely scatter plot, we're going to use 4 kWh/kg for total energy and fuel fraction of 80%

# In[26]:


idx_temp = pd.Series(range(1995,2051,1))
E_mfg_pet = pd.DataFrame(index=idx_temp)
E_mfg_pet.loc[:,'E_mfg_pet_kWhpkg'] = 4.0
E_mfg_pet.loc[:,'E_mfg_pet_fuelfraction'] = 0.8


# # PVDF granulate energy
# PVDF and PVF

# In[27]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_backsheet_mfg_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-backsheet-mfging.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[28]:


e_backsheet_mfg_raw.dropna(how='all')


# In[29]:


plt.scatter(e_backsheet_mfg_raw.index, e_backsheet_mfg_raw.iloc[:,0], label='electricity', )
plt.scatter(e_backsheet_mfg_raw.index, e_backsheet_mfg_raw.iloc[:,3], label='fuel')
plt.title('Energy backsheet mfging')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# In[30]:


e_backsheet_mfg_route1 = e_backsheet_mfg_raw[e_backsheet_mfg_raw['Notes'].str.contains('Route 1', na = False)]
e_backsheet_mfg_route2 = e_backsheet_mfg_raw[e_backsheet_mfg_raw['Notes'].str.contains('Route 2', na = False)]
e_backsheet_mfg_raw['E_sum_kWhpkg'] = e_backsheet_mfg_raw['E_mfg_kWhpkg']+e_backsheet_mfg_raw['E_mfg_FUEL_kWhpkg']


# In[31]:


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

# In[32]:


mean_abbasi = (e_backsheet_mfg_raw.loc[2011,'E_mfg_kWhpkg']+e_backsheet_mfg_raw.loc[2012,'E_mfg_kWhpkg'])/2
print('The average of Abbasi Route 1 and 2 is '+str(mean_abbasi)+' kWh/kg')


# In[33]:


fuelfraction_abbasi = e_backsheet_mfg_raw.loc[2014,'E_mfg_FUEL_kWhpkg']/e_backsheet_mfg_raw.loc[2014,'E_sum_kWhpkg']
print('The fuel fraction of Abassi from Route 1 is '+str(fuelfraction_abbasi))


# In[34]:


idx_temp = pd.Series(range(1995,2051,1))
E_mfg_pvdf = pd.DataFrame(index=idx_temp)
E_mfg_pvdf.loc[:,'E_mfg_pvdf_kWhpkg'] = mean_abbasi
E_mfg_pvdf.loc[:,'E_mfg_pvdfFUEL_fraction'] = fuelfraction_abbasi


# # Forming energy
# Turning granulate polymer into sheets

# In[35]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_plastic_sheet_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-plastic-forming.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[36]:


e_plastic_sheet_raw.dropna(how='all')


# In[37]:


plt.scatter(e_plastic_sheet_raw.index, e_plastic_sheet_raw.iloc[:,0], label='electricity', )
plt.scatter(e_plastic_sheet_raw.index, e_plastic_sheet_raw.iloc[:,3], label='fuel')
plt.title('Energy sheet forming')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# Based on the assumption that the energy required to form the film from a granualate is unlikely to be greater than the energy to create the granualte from feedstock, we will remove the high outlier, and average the rest.

# In[38]:


e_plastic_sheet = e_plastic_sheet_raw.copy()
e_plastic_sheet.loc[2005] = np.nan
e_filmform = e_plastic_sheet.mean()


# In[39]:


e_filmform.sum()


# In[40]:


idx_temp = pd.Series(range(1995,2051,1))
E_mfg_film = pd.DataFrame(index=idx_temp)
E_mfg_film.loc[:,'E_mfg_pvdf_kWhpkg'] = e_filmform.sum()
E_mfg_film.loc[:,'E_mfg_pvdfFUEL_fraction'] = e_filmform['E_mfg_FUEL_kWhpkg']/ e_filmform.sum()


# # Sum and Weight manufacturing Energies
# We need to add the film formation to each of the 3 plastics. Then EVA+film will be multiplied by the encapsulant baseline. 
# 
# For the backsheet, the PET core is typically 200 um thick, with two layers of PVF or PVDF of 40 um thick. The mass of the backsheet was weighted by the relative thicknesses of each material. We also have weighting by Kynar, Tedlar, and other - however, we didn't find energy data to support this level of detail for energy weighting - we will assume that PVDF and PVF have similar energy of manufacture. We will use the same weighting factor for fraction of the backsheet attributable to PET vs PVF/PVDF as we did in the mass baseline, i.e.; 80/280 * pvf energy + 200/280 * PET energy = average energy
# 
# ### EVA+film = encapsuant energy manufacturing

# In[64]:


idx_temp = pd.Series(range(1995,2051,1))
E_encapsulant = pd.DataFrame(index=idx_temp)
E_encapsulant['E_mfg_kWhpkg'] = E_mfg_film['E_mfg_pvdf_kWhpkg'] + E_mfg_eva['E_mfg_eva_kWhpkg']
E_encapsulant['E_mfg_fuel_kWhpkg'] = e_filmform['E_mfg_FUEL_kWhpkg']+E_mfg_eva['E_mfg_eva_fuelfraction']*E_mfg_eva['E_mfg_eva_kWhpkg']
E_encapsulant['E_mfg_fuelfraction'] = 100*(E_encapsulant['E_mfg_fuel_kWhpkg']/E_encapsulant['E_mfg_kWhpkg'])
E_encapsulant_final = round(E_encapsulant.iloc[:,[0,2]],2)
#E_encapsulant_final


# In[65]:


E_encapsulant_final.head()


# In[66]:


E_encapsulant_final.to_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/output_energy_encapsulant_MFGing.csv")


# ### PVDF+Film and PET+film = backsheet energy manufacturing
# *note all these values are static with time currently.*

# In[44]:


pvf_fraction = 80/280
pet_fraction = 200/280


# In[45]:


e_petfilm_kwhpkg = E_mfg_film['E_mfg_pvdf_kWhpkg'] + E_mfg_pet['E_mfg_pet_kWhpkg']
e_petfilm_fuelfraction = (E_mfg_film['E_mfg_pvdf_kWhpkg']*E_mfg_film['E_mfg_pvdfFUEL_fraction'] + 
                          E_mfg_pet['E_mfg_pet_kWhpkg']*E_mfg_pet['E_mfg_pet_fuelfraction'])/e_petfilm_kwhpkg
e_petfilm_fuel_kwhpkg = (E_mfg_film['E_mfg_pvdf_kWhpkg']*E_mfg_film['E_mfg_pvdfFUEL_fraction'] + 
                          E_mfg_pet['E_mfg_pet_kWhpkg']*E_mfg_pet['E_mfg_pet_fuelfraction'])


# In[46]:


e_pvdffilm_kwhpkg = E_mfg_film['E_mfg_pvdf_kWhpkg'] + E_mfg_pvdf['E_mfg_pvdf_kWhpkg']
e_pvdffilm_fuelfraction = (E_mfg_film['E_mfg_pvdf_kWhpkg']*E_mfg_film['E_mfg_pvdfFUEL_fraction'] + 
                           E_mfg_pvdf['E_mfg_pvdf_kWhpkg']*E_mfg_pvdf['E_mfg_pvdfFUEL_fraction'])/e_pvdffilm_kwhpkg
e_pvdffilm_fuel_kwhpkg = (E_mfg_film['E_mfg_pvdf_kWhpkg']*E_mfg_film['E_mfg_pvdfFUEL_fraction'] + 
                           E_mfg_pvdf['E_mfg_pvdf_kWhpkg']*E_mfg_pvdf['E_mfg_pvdfFUEL_fraction'])


# In[68]:


idx_temp = pd.Series(range(1995,2051,1))
E_backsheet = pd.DataFrame(index=idx_temp)
E_backsheet['E_mfg_kWhpkg'] = pvf_fraction * e_pvdffilm_kwhpkg + pet_fraction * e_petfilm_kwhpkg
E_backsheet['E_mfg_fuelfraction'] = 100*((pet_fraction *e_petfilm_fuel_kwhpkg+pvf_fraction *e_pvdffilm_fuel_kwhpkg)/E_backsheet['E_mfg_kWhpkg'])
E_backsheet = round(E_backsheet,2)


# In[69]:


E_backsheet.head()


# In[70]:


E_backsheet.to_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/output_energy_backsheet_MFGing.csv")


# # Landfill Energy
# There was really only one plastic specific landfilling energy found; Xayachak, T. et al. (2023) ‘Assessing the environmental footprint of plastic pyrolysis and gasification: A life cycle inventory study’, Process Safety and Environmental Protection, 173, pp. 592–603. Available at: https://doi.org/10.1016/j.psep.2023.03.061.
# The energy denoted in Table S3 is miniscual: 4e-4 kWh/kg, mostly electricity. Previous material baselines have used 0.09 kWh/kg from Ravikumar 2016. We will maintain consistency, and use the 0.09 value.
# 
# There is a potential for incineration with heat/energy recovery, however, we will currently neglect this option and assume things are landfilled without incineration. Potential upgrades could include energy credit or negative energy, but would also require carbon intensity.

# # Recycling Energies
# Low Quality = Mechanical Recycling
# 
# High Quality = chemical recycling (pyrolysis or glycolysis)
# 
# We will not distingiush between recycling energies of the different plastics as little information was found, and mixed plastic recycling is uncommon (e.g.; backsheet)

# In[50]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_plastic_LQrecycle_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-plastic-LQrecycling.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[51]:


e_plastic_LQrecycle_raw['E_sum_kWhpkg'] = e_plastic_LQrecycle_raw['E_LQrecycle_kWhpkg']+e_plastic_LQrecycle_raw['E_LQrecycle_fuel_kWhpkg']


# In[52]:


e_plastic_LQrecycle_raw.dropna(how='all')


# In[53]:


plt.scatter(e_plastic_LQrecycle_raw.index, e_plastic_LQrecycle_raw.iloc[:,0], label='electricity', )
plt.scatter(e_plastic_LQrecycle_raw.index, e_plastic_LQrecycle_raw.iloc[:,3], label='fuel')
plt.scatter(e_plastic_LQrecycle_raw.index, e_plastic_LQrecycle_raw.iloc[:,6], label='sum', marker='P', color='black')

plt.title('Energy LQ Recycle (mechanical)')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# Three of the data sources are in close agreement on the energy requirements. There is also useful data for decreasing fuel fraction from Uekert et al. Therefore, we will interpolate from Joosten, Arena, and Uekert.

# In[73]:


e_plastic_LQrecycle_maths = e_plastic_LQrecycle_raw.loc[[1998,2003,2022],['E_LQrecycle_kWhpkg','E_LQrecycle_fuel_kWhpkg']]
e_plastic_LQrecycle_maths.loc[2022,'E_LQrecycle_fuel_kWhpkg'] = 0.03*8.58*0.277777 #from Uekert supplemental
e_plastic_LQrecycle_maths['E_LQrecycle_sum_kWhpkg'] = e_plastic_LQrecycle_maths.sum(axis=1)
e_plastic_LQrecycle_maths['E_LQrecycle_fuelfraction'] = 100*e_plastic_LQrecycle_maths['E_LQrecycle_fuel_kWhpkg']/e_plastic_LQrecycle_maths['E_LQrecycle_sum_kWhpkg'] 
e_plastic_LQrecycle_maths


# In[74]:


idx_temp = pd.Series(range(1995,2051,1))
E_plastic_LQrecycle_temp = e_plastic_LQrecycle_maths.iloc[:,[2,3]]
E_plastic_LQrecycle_gappy = E_plastic_LQrecycle_temp.reindex(index=idx_temp)
E_plastic_LQrecycle = E_plastic_LQrecycle_gappy.interpolate(limit_direction='both')


# In[76]:


E_plastic_LQrecycle.to_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/output_energy_plastics_LQrecycle.csv")


# ### HQ recycling
# These numbers will be added to the LQ recycling numbers

# In[57]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_plastic_HQrecycle_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-plastic-HQrecycling.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[58]:


e_plastic_HQrecycle_raw['E_sum_kWhpkg'] = e_plastic_HQrecycle_raw['E_HQrecycle_kWhpkg']+e_plastic_HQrecycle_raw['E_HQrecycle_fuel_kWhpkg']


# In[59]:


e_plastic_HQrecycle_raw.dropna(how='all')


# In[60]:


plt.scatter(e_plastic_HQrecycle_raw.index, e_plastic_HQrecycle_raw.iloc[:,0], label='electricity', )
plt.scatter(e_plastic_HQrecycle_raw.index, e_plastic_HQrecycle_raw.iloc[:,3], label='fuel')
plt.scatter(e_plastic_HQrecycle_raw.index, e_plastic_HQrecycle_raw.iloc[:,6], label='sum', marker='P', color='black')

plt.title('Energy HQ Recycle')
plt.ylabel('[kWh/kg]')
plt.xlim(1994,2023)
plt.ylim(0,)
plt.legend()


# We will select the Uekert methanolysis (of PET) values for HQ closed loop recycling, as it is indicated that this process produces a high material quality with no discoloration.

# In[61]:


e_plasticHQrecyle_fuelfraction = e_plastic_HQrecycle_raw.loc[2020,'E_HQrecycle_fuel_kWhpkg']/e_plastic_HQrecycle_raw.loc[2020,'E_sum_kWhpkg']


# In[71]:


idx_temp = pd.Series(range(1995,2051,1))
E_plastic_HQrecycle = pd.DataFrame(index=idx_temp)
E_plastic_HQrecycle['E_HQrecycle_kWhpkg'] = round(e_plastic_HQrecycle_raw.loc[2020,'E_sum_kWhpkg'],2)
E_plastic_HQrecycle['E_HQrecycle_fuelfraction'] = round(e_plasticHQrecyle_fuelfraction,2)*100


# In[72]:


E_plastic_HQrecycle.head()


# While this is high, higher than some of the manufacturing energies, this is not unreasonable when we consider the energy for extraction (which will be added to the manufacturing energies above.

# # Extraction Energy
# The above manufacturing energies do not include extraction and processing of natural gas. This will be captured in the e_mat_extraction and will be added to MFGing energies. The electricity and fuel data used for this is from ecoinvent, derived from NETL 2014, which is US centric 2010 conventional extraction.
# 
# This energy is 0.05 kWh/kg of electricity and 16.6 kWh/kg of natural gas for nat gas extraction, so a total of 16.65, with a majority being fossil derived.
