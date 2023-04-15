#!/usr/bin/env python
# coding: utf-8

# # Energy Carbon: Marketshare by Country Weighting
# In this first section we will determine the country-wise countribution to each of the energy steps of the silicon supply chain to correctly attribute carbon intensities to grids.

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


# Pull in crunched data from BNEF commissioned capacity to create country marketshare. Everything that was less than 1% of global marketshare was excluded (things don't currently sum to 100). 

# In[2]:


#skipcols = ['Source', 'Notes','Country']
mrktshare_country_si_cell = pd.read_csv(os.path.join(carbonfolder, 'input-silicon-CountryMarketshare-cell.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)
mrktshare_country_si_wafer = pd.read_csv(os.path.join(carbonfolder, 'input-silicon-CountryMarketshare-wafer.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)
mrktshare_country_si_ingot_multi = pd.read_csv(os.path.join(carbonfolder, 'input-silicon-CountryMarketshare-ingot-multi.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)
mrktshare_country_si_ingot_mono = pd.read_csv(os.path.join(carbonfolder, 'input-silicon-CountryMarketshare-ingot-mono.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)
mrktshare_country_si_polysi = pd.read_csv(os.path.join(carbonfolder, 'input-silicon-CountryMarketshare-polysilicon.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)
#mrktshare_country_si_silica = pd.read_csv(os.path.join(carbonfolder, 'input-silicon-CountryMarketshare-silica.csv'),
#                                     index_col='Country')#, usecols=lambda x: x not in skipcols)


# Pull in silicon energy files to create a % of energy attributable to each step of the MFGing process. This will be multiplied by the country market shares to create an overall country marketshare of the energy supply chain (i.e. energy weighted...)
# 
# Also the mono vs multi to attribute marketshare of these two technologies.

# In[3]:


energy_silicon_mfg = pd.read_csv(os.path.join(supportmatfolder, 'output_energy_silicon_mfg.csv'),
                                     index_col=0)#, usecols=lambda x: x not in skipcols)
marketshare_silicon_monoVmulti = pd.read_csv(os.path.join(supportmatfolder, 'output_scaledmrktshr_mcSi_mono.csv'),
                                     index_col=0)#, usecols=lambda x: x not in skipcols)
energy_silicon_mfg_STEPS_raw = pd.read_csv(os.path.join(supportmatfolder, 'output_energy_silicon_mfg_STEPS.csv'),
                                     index_col=0)#, usecols=lambda x: x not in skipcols)


# In[4]:


energy_silicon_mfg_STEPS = energy_silicon_mfg_STEPS_raw.filter(like="kWhpkg") #drop the fuel fraction columns
energy_silicon_mfg.drop(['E_mfgFuelFraction'], axis=1, inplace=True) #drop fuel fraction


# In[5]:


energyShare_silicon_mfg_STEPS = energy_silicon_mfg_STEPS.div(energy_silicon_mfg.values)
#sanity check that everything adds to 100% or 1
#energyShare_silicon_mfg_STEPS.sum(axis=1)


# In[6]:


energyShare_silicon_mfg_STEPS.columns


# The math is:
# 
#     % of energy for mfging step * % country contribution, then sum for each country across all energy steps to get the country contribution to MFGing energy

# In[7]:


energyShare_silicon_mfg_STEPS_subset = energyShare_silicon_mfg_STEPS.loc[2004:2022]
#energyShare_silicon_mfg_STEPS_subset


# ### Cell

# In[8]:


energy_cell_fract = energyShare_silicon_mfg_STEPS_subset['E_cellProcess_kWhpkg']


# In[9]:


mrktshare_country_si_cell_fractbyyear = mrktshare_country_si_cell/100 #turn it into a decimal


# In[10]:


cell_by_country = mrktshare_country_si_cell_fractbyyear*energy_cell_fract.values*100
# sanity check: that all countries each year add to the value from energy_cell_fract or pretty close
#cell_by_country.sum()/100


# ### Wafer

# In[11]:


energy_wafer_fract = energyShare_silicon_mfg_STEPS_subset['E_Wafering_kWhpkg']
#energy_wafer_fract


# In[12]:


mrktshare_country_si_wafer_fractbyyear = mrktshare_country_si_wafer/100 #turn it into a decimal
#mrktshare_country_si_wafer_fractbyyear


# In[13]:


wafer_by_country = mrktshare_country_si_wafer_fractbyyear*energy_wafer_fract.values*100
# sanity check: that all countries each year add to the value from energy_cell_fract or pretty close
#wafer_by_country.sum()/100
#wafer_by_country


# ### Ingot
# More complicated due to mono vs multi marketshare. The total ingot energy is already weighted by this marketshare. Math is:
#         
#         (mono% * % mono country production + multi% * % multi country production)* Ingot % of energy.

# In[14]:


marketshare_silicon_monoVmulti_subset = marketshare_silicon_monoVmulti.loc[2004:2022] #in fraction form
marketshare_silicon_monoVmulti_subset.head()


# In[15]:


energy_ingot_fract = energyShare_silicon_mfg_STEPS_subset['E_Ingot_kWhpkg']
#energy_ingot_fract


# In[16]:


mrktshare_country_si_ingot_multi_fractbyyear = mrktshare_country_si_ingot_multi/100 #turn it into a decimal
mrktshare_country_si_ingot_mono_fractbyyear = mrktshare_country_si_ingot_mono/100 #turn it into a decimal


# In[17]:


#mono multi deployment marketshares * the countrywise marketshare of mfging these techs
country_multi = mrktshare_country_si_ingot_multi_fractbyyear*marketshare_silicon_monoVmulti_subset['mcSi'].values
country_mono = mrktshare_country_si_ingot_mono_fractbyyear*marketshare_silicon_monoVmulti_subset['monoSi'].values


# In[18]:


#weight both by the ingot energy
country_multi_energy = country_multi*energy_ingot_fract.values
country_mono_energy = country_mono*energy_ingot_fract.values


# In[19]:


country_multi_energy.index


# In[20]:


country_mono_energy.index


# In[21]:


#keeps all countries, while grouping and summing any duplicates
country_wtdenergy_ingot = pd.concat([country_mono_energy, country_multi_energy]).groupby(['Country']).sum()
#sanity check that sums by year are the same as the ingot energy fraction
#country_wtdenergy_ingot.sum(axis=0)


# In[22]:


ingot_by_country = country_wtdenergy_ingot*100
ingot_by_country


# ### Polysilicon

# In[23]:


energy_polysi_fract = energyShare_silicon_mfg_STEPS_subset['E_refineSiemens_kWhpkg']
#energy_polysi_fract


# In[24]:


mrktshare_country_si_polysi_fractbyyear = mrktshare_country_si_polysi/100 #turn it into a decimal


# In[25]:


polysi_by_country = mrktshare_country_si_polysi_fractbyyear*energy_polysi_fract.values*100
# sanity check: that all countries each year add to the value from energy_cell_fract or pretty close
polysi_by_country#.sum()/100


# ### Mg-Si
# from USGS

# In[26]:


mrktshare_country_si_mgsi = pd.read_csv(os.path.join(carbonfolder, 'input-silicon-CountryMarketshare-mgSi.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)


# In[27]:


energy_reducesilica_fract = energyShare_silicon_mfg_STEPS_subset.loc[2007:2021,'E_reduce_sum_kWhpkg']
#energy_reducesilica_fract


# In[28]:


mrktshare_country_si_silica_fractbyyear = mrktshare_country_si_mgsi/100 #turn it into a decimal
#mrktshare_country_si_silica_fractbyyear


# In[29]:


silicareduce_by_country = mrktshare_country_si_silica_fractbyyear*energy_reducesilica_fract.values*100
# sanity check: that all countries each year add to the value from energy_cell_fract or pretty close
#wafer_by_country.sum()/100


# In[30]:


silicareduce_by_country


# # Sum MFGing by country contributions

# In[31]:


pd.concat([cell_by_country, wafer_by_country, ingot_by_country, 
           polysi_by_country, silicareduce_by_country]).groupby(['Country']).sum()


# In[ ]:




