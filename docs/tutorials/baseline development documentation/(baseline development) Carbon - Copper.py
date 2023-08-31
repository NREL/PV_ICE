#!/usr/bin/env python
# coding: utf-8

# # Energy Carbon from Copper Manufacturing
# The copper manufacturing can be split into the mining, smelting/SX and the refining/EW process. The Manufacturing energ is broken up differently, so we will use literature sources to weight the country energy

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


# In[15]:


#from Marsden 2008
hydro_refine_fract = 3840/(12440+960+1980+3840) #hydro refining energy fraction
pyro_refine_fract_1 = 2700/((6000+900+410+1000+4420+1870+120)+5150+2700) # pyro energy #1 refining energy fraction, includes crushing and milling
pyro_refine_fract_2 = 2700/((6000+900+5760+4640+1870+120)+5150+2700) #pyro energy #2 refining energy fraction, includes crushing and milling

hydro_sx_fract = 1980/(12440+960+1980+3840) #hydro refining energy fraction
pyro_smelt_fract_1 = 5150/((6000+900+410+1000+4420+1870+120)+5150+2700) # pyro energy #1 refining energy fraction, includes crushing and milling
pyro_smelt_fract_2 = 5150/((6000+900+5760+4640+1870+120)+5150+2700) #pyro energy #2 refining energy fraction, includes crushing and milling

hydro_mine_fract = (12440+960)/(12440+960+1980+3840) #hydro refining energy fraction
pyro_mine_fract_1 = (6000+900+410+1000+4420+1870+120)/((6000+900+410+1000+4420+1870+120)+5150+2700) # pyro energy #1 refining energy fraction, includes crushing and milling
pyro_mine_fract_2 = (6000+900+5760+4640+1870+120)/((6000+900+5760+4640+1870+120)+5150+2700) #pyro energy #2 refining energy fraction, includes crushing and milling


# In[16]:


print('Hydro fraction attributable to ew: '+str(round(hydro_refine_fract*100,2)))
print('Pyro #1 fraction attributable to refining: '+str(round(pyro_refine_fract_1*100,2)))
print('Pyro #2 fraction attributable to refining: '+str(round(pyro_refine_fract_2*100,2)))


# In[17]:


print('Hydro fraction attributable to sx: '+str(round(hydro_sx_fract*100,2)))
print('Pyro #1 fraction attributable to smelt: '+str(round(pyro_smelt_fract_1*100,2)))
print('Pyro #2 fraction attributable to smelt: '+str(round(pyro_smelt_fract_2*100,2)))


# In[18]:


print('Hydro fraction attributable to mining: '+str(round(hydro_mine_fract*100,2)))
print('Pyro #1 fraction attributable to mining: '+str(round(pyro_mine_fract_1*100,2)))
print('Pyro #2 fraction attributable to mining: '+str(round(pyro_mine_fract_2*100,2)))


# In[14]:


hydro_refine_fract+hydro_sx_fract


# “Chapter 7 Energy Use in the Copper Industry.” 1988. In . https://www.princeton.edu/~ota/disk2/1988/8808/880809.PDF.	
# - Mining	20%
# - milling	40%
# - smelt, convert, refine	40%

# Allen, Marc. 2021. “MINING ENERGY CONSUMPTION 2021.” engeco. https://www.mining-technology.com/wp-content/uploads/sites/19/2021/07/Weir_Minerals_engeco_Mining_Energy_Consumption_2021.pdf.	
# - Mining - movers	60%
# - mining-griding	36%
# - mining-flotation, filter, dry	4%

# It seems the mining and moreover the milling process or mining for SX is very energy intensive. We are assuming that the milling takes place in the same location as the mining (this may be a bad assumption). Additionally, the Pyro vs Hydro routes have different energy intensities per step (EW> pyro refining). Lacking a more complex model, we will average this out to say 20% each.
# From these three literature sources, we will estimate that:
# - Mining = 60%
# - Smelt/SX = 20%
# - Refine/EW = 20%

# In[ ]:





# In[10]:


cu_refine_country_raw = pd.read_csv(os.path.join(carbonfolder, 'input-USGS-Cu-RefinePrimaryCountries.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)
cu_smelt_country_raw = pd.read_csv(os.path.join(carbonfolder, 'input-USGS-Cu-SmeltPrimaryCountries.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)
cu_mine_country_raw = pd.read_csv(os.path.join(carbonfolder, 'input-USGS-Cu-MinePrimaryCountries.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)


# Methods:
# - interpolate or fill the missing values in each dataframe
# - sum column and get countries to fractions of step production
# - renormalize to 100%
# - multiply by % energy associated with each step (mine, smelt, refine)
# - sum countrywise into overall energy by country %, check sum 100%
