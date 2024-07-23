#!/usr/bin/env python
# coding: utf-8

# # Copper Energy Demands
# This journal documents the energy demands of mining, refining, drawing and recycling of copper for use inside the PV cell. Probably also applies to copper in wiring (not yet considered)

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (8, 4)
cwd = os.getcwd() #grabs current working directory

supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
baselinesFolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')


# ### Mining Energy

# In[2]:


cu_mining_raw = pd.read_csv(os.path.join(supportMatfolder+"\energy-input-copper-mining.csv"), index_col='year')
cu_mining_raw.dropna(how='all')


# In[3]:


fig, ax1 = plt.subplots()

ax1.scatter(cu_mining_raw.index, cu_mining_raw['E_CuMining_kWhpkg'], marker='o')
ax1.set_ylabel('kWh/kg')

ax2 = ax1.twinx()
ax2.scatter(cu_mining_raw.index, cu_mining_raw['PrctFuel'], marker='^', color='red')
ax2.set_ylabel('Percent Fuel [%]', color='red')
ax2.set_ylim(0,100)

plt.title('Cu_Mining_kWhpkg')
plt.show()


# The two highest pre-1990 data points include milling and floation, which start getting into processing of the material (pyro vs hydro). The Marsden data points in 2007-2008 have two mining options, and Lagos et al in 2015 has open pit and underground mining. Both sources may include transportation energies.
# 
# To reconcile all the nuanced data points, we will take the average of post-1990 energy data.
# 
# The percent fuel differs in Lagos et al between openpit and underground. This is likely due to the inclusion of transportation energy (i.e. openpit which involves more driving is higher fuel). Farjana which excludes transportation is 20% fuels, therefore we will use this.

# In[4]:


cu_mining_data = cu_mining_raw.loc[1995:,'E_CuMining_kWhpkg']
cu_mining_avg = cu_mining_data.mean()
cu_mining_prctfuel = 20.0
indx_temp = pd.Series(range(1995,2051,1))
cu_mining_energy = pd.DataFrame({'E_Cu_Mining_kWhpkg':cu_mining_avg, 'PrctFuel':cu_mining_prctfuel}, index=indx_temp)
#cu_mining_energy


# In[ ]:





# ## PYRO
# Pyrometallurgy is the dominant technology for copper mining, although hydrometallurgy market share is growing. Pyro metallurgy is also known as/includes grinding, froth floatation, converting, Smelting, and electrolysis. This final electrorefining step is not to be confused with the hydrometallurgical electrowinning.
# 
# This data includes grinding and milling, floatation, smelting, and electrolysis refining.

# In[5]:


cu_pyro_raw = pd.read_csv(os.path.join(supportMatfolder+"\energy-input-copper-pyro.csv"), index_col='year')
cu_pyro_raw.dropna(how='all')


# In[6]:


fig, ax1 = plt.subplots()

ax1.scatter(cu_pyro_raw.index, cu_pyro_raw['E_Pyro_Cu_kWhpkg'], marker='o')
ax1.set_ylabel('kWh/kg')

ax2 = ax1.twinx()
ax2.scatter(cu_pyro_raw.index, cu_pyro_raw['PrctFuel'], marker='^', color='red')
ax2.set_ylabel('Percent Fuel [%]', color='red')
ax2.set_ylim(0,100)

plt.title('Cu Pyrometallurgy kWhpkg')
plt.show()


# The final two datapoints from Marsden are two different process pathways and therefore represent a range of potential energies for pyrometallurgy. The Alvarado data may not include grinding, and therfore may be low. We will take the average of the Marsden data, and do a linear interpolation from the Pitt 1980.
# 
# Fuel fractions are fairly consistent across all data, therefore we will take the average.

# In[7]:


cu_pyro = cu_pyro_raw.copy()
cu_pyro.loc[2002] = np.nan
cu_pyro_avg_2007 = cu_pyro.loc[2007:2008,'E_Pyro_Cu_kWhpkg'].mean()
cu_pyro.loc[2007:2008,'E_Pyro_Cu_kWhpkg'] = cu_pyro_avg_2007

cu_pyro_filled = cu_pyro.interpolate()
cu_pyro_final = cu_pyro_filled.loc[1995:,'E_Pyro_Cu_kWhpkg':'PrctFuel']


# In[8]:


#cu_pyro_final
fig, ax1 = plt.subplots()

ax1.plot(cu_pyro_final.index, cu_pyro_final['E_Pyro_Cu_kWhpkg'])
ax1.set_ylabel('kWh/kg')
ax1.set_xlim(1995,2030)
ax1.set_ylim(0,12)

ax2 = ax1.twinx()
ax2.plot(cu_pyro_final.index, cu_pyro_final['PrctFuel'], color='red')
ax2.set_ylabel('Percent Fuel [%]', color='red')
ax2.set_ylim(0,100)

plt.title('Cu Pyrometallurgy kWhpkg')
plt.show()


# ## HYDRO

# In[9]:


cu_hydro_raw = pd.read_csv(os.path.join(supportMatfolder+"\energy-input-copper-hydro.csv"), index_col='year')
cu_hydro_raw.dropna(how='all')


# In[10]:


fig, ax1 = plt.subplots()

ax1.scatter(cu_hydro_raw.index, cu_hydro_raw['E_hydro_Cu_kWhpkg'], marker='o')
ax1.set_ylabel('kWh/kg')
ax1.set_ylim(0,)

ax2 = ax1.twinx()
ax2.scatter(cu_hydro_raw.index, cu_hydro_raw['PrctFuel'], marker='^', color='red')
ax2.set_ylabel('Percent Fuel [%]', color='red')
ax2.set_ylim(0,100)

plt.title('Cu Hydrometallurgy kWhpkg')
plt.show()


# Since 2002, the energy intensity looks pretty constant. Therefore, we'll take the average after 2002. 
# 
# the 1980 data point is quite high, but this might be real. Will interpolate between 1980 and 2002.

# In[11]:


cu_hydro_post_2002 = cu_hydro_raw.loc[2002:,'E_hydro_Cu_kWhpkg'].mean()
cu_hydro_post_2002_fuel = cu_hydro_raw.loc[2002:,'PrctFuel'].mean()

cu_hydro = cu_hydro_raw.copy()
cu_hydro.loc[2002:,'E_hydro_Cu_kWhpkg']=cu_hydro_post_2002
cu_hydro.loc[2002:,'PrctFuel']=cu_hydro_post_2002_fuel

cu_hydro_filled = cu_hydro.interpolate()
cu_hydro_final = cu_hydro_filled.loc[1995:,['E_hydro_Cu_kWhpkg','PrctFuel']]


# In[12]:


#cu_hydro_final
fig, ax1 = plt.subplots()

ax1.plot(cu_hydro_final.index, cu_hydro_final['E_hydro_Cu_kWhpkg'])
ax1.set_ylabel('kWh/kg')
ax1.set_xlim(1995,2030)
ax1.set_ylim(0,)

ax2 = ax1.twinx()
ax2.plot(cu_hydro_final.index, cu_hydro_final['PrctFuel'], color='red')
ax2.set_ylabel('Percent Fuel [%]', color='red')
ax2.set_ylim(0,100)

plt.title('Cu Hydrometallurgy kWhpkg')
plt.show()


# In[ ]:





# ## Import Market share of Pyro vs Hydro Metallurgy

# In[13]:


#import marketshare
mrktshr_pyrohydro_raw = pd.read_excel(os.path.join(supportMatfolder+"\energy-inputs-copper-maths.xlsx"),
              sheet_name='pyrovshydro', index_col=0, header=[0])


# In[14]:


mrktshr_pyrohydro = mrktshr_pyrohydro_raw[['% PYRO','% HYDRO']]

plt.stackplot(mrktshr_pyrohydro.index, mrktshr_pyrohydro['% PYRO'], mrktshr_pyrohydro['% HYDRO'], colors=['orange','skyblue'])
plt.legend(mrktshr_pyrohydro.columns, loc='lower right')


# Now we multiply the energies by their percentages, and re-calculate fuel percentage

# In[15]:


#calculate fuel energy
cu_hydro_final['E_hydro_Cu_fuel_kWhpkg'] = cu_hydro_final['E_hydro_Cu_kWhpkg']*(cu_hydro_final['PrctFuel']/100)
cu_pyro_final['E_Pyro_Cu_fuel_kWhpkg'] = cu_pyro_final['E_Pyro_Cu_kWhpkg']*(cu_pyro_final['PrctFuel']/100)


# In[16]:


cu_hydro_final.head(5)


# In[17]:


cu_pyro_final.head(5)


# hydro_e*hydroprct + pyro_e*pyroprct
# same for fuel

# In[18]:


mrktshr_pyrohydro_filled = mrktshr_pyrohydro.loc[1995:].ffill() #create through 2050 (just maintained marketshare)
Cu_metallurgy_e = mrktshr_pyrohydro_filled['% PYRO']*cu_pyro_final['E_Pyro_Cu_kWhpkg']+mrktshr_pyrohydro_filled['% HYDRO']*cu_hydro_final['E_hydro_Cu_kWhpkg']
Cu_metallurgy_e_fuel = mrktshr_pyrohydro_filled['% PYRO']*cu_pyro_final['E_Pyro_Cu_fuel_kWhpkg']+mrktshr_pyrohydro_filled['% HYDRO']*cu_hydro_final['E_hydro_Cu_fuel_kWhpkg']
Cu_metallurgy_e_prctfuel = Cu_metallurgy_e_fuel/Cu_metallurgy_e*100 #back into percent fuel
Cu_metallurgy_energy = pd.concat([Cu_metallurgy_e,Cu_metallurgy_e_prctfuel], axis=1, keys=['E_Cu_metallurgy_kWhpkg','PrctFuel'])


# In[19]:


Cu_metallurgy_energy.head(5)


# In[32]:


Cu_metallurgy_energy.to_csv(os.path.join(supportMatfolder,"output-energy-copper-metallurgy.csv"))


# ### Energy Drawing Cu wire

# In[21]:


cu_wireDraw_raw = pd.read_csv(os.path.join(supportMatfolder+"\energy-input-copper-wireDraw.csv"), index_col='year')
cu_wireDraw_raw.dropna(how='all')


# In[22]:


fig, ax1 = plt.subplots()

ax1.scatter(cu_wireDraw_raw.index, cu_wireDraw_raw['E_wireDraw_kWhpkg'], marker='o')
ax1.set_ylabel('kWh/kg')
ax1.set_ylim(0,5)

ax2 = ax1.twinx()
ax2.scatter(cu_wireDraw_raw.index, cu_wireDraw_raw['PrctFuel'], marker='^', color='red')
ax2.set_ylabel('Percent Fuel [%]', color='red')
ax2.set_ylim(0,100)

plt.title('Cu_WireDraw_kWhpkg')
plt.show()


# Not a huge range. The lowest point is likely too low, paper is demonstrating software optimization. Dropping two low points and interpolate the rest.

# In[23]:


cu_wireDraw_mod = cu_wireDraw_raw.copy()
cu_wireDraw_mod.loc[2009:2018] = np.nan
cu_wireDraw_mod.interpolate(inplace=True)
cu_wireDraw_mod['PrctFuel'] = 0.0
cu_wireDraw_final = cu_wireDraw_mod.iloc[:,[0,1]]


# ## Sum the virgin copper energies

# In[24]:


Cu_MFGing_e_final = pd.DataFrame(index=indx_temp, columns=['E_Cu_mfging_kWhpkg','PrctFuel'])


# In[25]:


#percent fuel to fuel energy for each
cu_mining_energy['E_Cu_mining_fuel_kWhpkg'] = cu_mining_energy['E_Cu_Mining_kWhpkg']*cu_mining_energy['PrctFuel']/100
Cu_metallurgy_energy['E_Cu_metallurgy_fuel_kWhpkg'] = Cu_metallurgy_energy['E_Cu_metallurgy_kWhpkg']*Cu_metallurgy_energy['PrctFuel']/100
cu_wireDraw_final['E_wireDraw_fuel_kWhpkg'] = cu_wireDraw_final['E_wireDraw_kWhpkg']*cu_wireDraw_final['PrctFuel']/100


# In[26]:


Cu_mfging_fuel_e = cu_mining_energy['E_Cu_mining_fuel_kWhpkg']+Cu_metallurgy_energy['E_Cu_metallurgy_fuel_kWhpkg']+cu_wireDraw_final['E_wireDraw_fuel_kWhpkg']
Cu_mfging_e = cu_mining_energy['E_Cu_Mining_kWhpkg']+Cu_metallurgy_energy['E_Cu_metallurgy_kWhpkg']+cu_wireDraw_final['E_wireDraw_kWhpkg']

Cu_MFGing_e_final['PrctFuel']=Cu_mfging_fuel_e/Cu_mfging_e*100
Cu_MFGing_e_final['E_Cu_mfging_kWhpkg'] = Cu_mfging_e


# In[27]:


#Cu_MFGing_e_final
fig, ax1 = plt.subplots()

ax1.scatter(Cu_MFGing_e_final.index, Cu_MFGing_e_final['E_Cu_mfging_kWhpkg'], marker='o')
ax1.set_ylabel('kWh/kg')
ax1.set_ylim(0,20)

ax2 = ax1.twinx()
ax2.scatter(Cu_MFGing_e_final.index, Cu_MFGing_e_final['PrctFuel'], marker='^', color='red')
ax2.set_ylabel('Percent Fuel [%]', color='red')
ax2.set_ylim(0,100)

plt.title('Cu_MFGing_Energy_kWhpkg')
plt.show()


# In[28]:


Cu_MFGing_e_final = round(Cu_MFGing_e_final,2)
Cu_MFGing_e_final.to_csv(os.path.join(supportMatfolder+'\output_energy_Cu_Mfging.csv'))


# # Cu Recycling

# In[29]:


cu_recycle_raw = pd.read_csv(os.path.join(supportMatfolder+"\energy-input-copper-recycle.csv"), index_col='year')
cu_recycle_raw.dropna(how='all')


# In[30]:


plt.scatter(cu_recycle_raw.index, cu_recycle_raw['E_recycleCu_kWhpkg'])


# We will use Dong et al 2022, based on their inventory in their supplemental information. We will use the WEEE specific data (2018), CED, which account for processing e-waste (which is the closest approximation to a PV module), then smelts and refines the copper.
# 
# I cannot find any information on low purity copper recycling, therefore, we will assume all this copper gets recycled to high quality (i.e. LQ recycling will be all energy). The energy associated with HQ will be the wire drawing energy (calculated above). We will also assume the same fuel fraction for recycling as primary since it is using the same smelting processes.

# In[ ]:




