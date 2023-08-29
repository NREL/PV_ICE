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

supportMatfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
baselinesFolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines')


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
cu_minig_prctfuel = 20.0


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

# In[22]:


mrktshr_pyrohydro_filled = mrktshr_pyrohydro.loc[1995:].ffill() #create through 2050 (just maintained marketshare)
Cu_metallurgy_e = mrktshr_pyrohydro_filled['% PYRO']*cu_pyro_final['E_Pyro_Cu_kWhpkg']+mrktshr_pyrohydro_filled['% HYDRO']*cu_hydro_final['E_hydro_Cu_kWhpkg']
Cu_metallurgy_e_fuel = mrktshr_pyrohydro_filled['% PYRO']*cu_pyro_final['E_Pyro_Cu_fuel_kWhpkg']+mrktshr_pyrohydro_filled['% HYDRO']*cu_hydro_final['E_hydro_Cu_fuel_kWhpkg']
Cu_metallurgy_e_prctfuel = Cu_metallurgy_e_fuel/Cu_metallurgy_e*100 #back into percent fuel
Cu_metallurgy_energy = pd.concat([Cu_metallurgy_e,Cu_metallurgy_e_prctfuel], axis=1, keys=['E_Cu_metallurgy_kWhpkg','PrctFuel'])


# In[ ]:





# ### Add the Energy to turn Cu cathode in to Cu wire

# In[26]:


cu_wireDraw_raw = pd.read_csv(os.path.join(supportMatfolder+"\energy-input-copper-wireDraw.csv"), index_col='year')
cu_wireDraw_raw.dropna(how='all')


# In[24]:


#subtract the average historical CED of Cu from the 2012 data to get just wire pulling part
adj_wire = cu_wireDraw_raw.loc[2012,'E_wireDraw_kWhpkg']-CED_mrktshr.mean() #using the historical with marketshare hydro/pyro wtd
cu_wireDraw_raw.loc[2012,'E_wireDraw_kWhpkg'] = adj_wire[0]
adj_wire


# In[ ]:


cu_wireDraw_raw.dropna(how='all')


# None of these are very large. We will average these values to estimate the wire drawing requirements, then add it to the CED to get a MFGing of virgin Cu. This value will also be added to the recycling processing requirements below.

# In[ ]:


e_wireDraw = cu_wireDraw_raw['E_wireDraw_kWhpkg'].mean()
e_wireDraw


# In[ ]:


CED_Cu_virgin = round(CED_Cu_filled+e_wireDraw,2)
CED_Cu_virgin.to_csv(os.path.join(supportMatfolder+'\output_energy_Cu_Mfging.csv'))


# # Cu Recycling

# In[ ]:


cu_recycle_raw = pd.read_csv(os.path.join(supportMatfolder+"\energy-input-copper-recycle.csv"), index_col='year')
cu_recycle_raw.dropna(how='all')


# In[ ]:


plt.scatter(cu_recycle_raw.index, cu_recycle_raw['E_recycleCu_kWhpkg'])


# We will use Dong et al 2022, based on their inventory in their supplemental information. We will use the WEEE specific data (2018), CED, which account for processing e-waste (which is the closest approximation to a PV module), then smelts and refines the copper.
# 
# I cannot find any information on low purity copper recycling, therefore, we will assume all this copper gets recycled to high quality (i.e. LQ recycling will be all energy). The energy associated with HQ will be the wire drawing energy (calculated above). We will also assume the same fuel fraction for recycling as primary since it is using the same smelting processes.

# In[ ]:




