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


# In[2]:


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


# In[3]:


print('Hydro fraction attributable to ew: '+str(round(hydro_refine_fract*100,2)))
print('Pyro #1 fraction attributable to refining: '+str(round(pyro_refine_fract_1*100,2)))
print('Pyro #2 fraction attributable to refining: '+str(round(pyro_refine_fract_2*100,2)))


# In[4]:


print('Hydro fraction attributable to sx: '+str(round(hydro_sx_fract*100,2)))
print('Pyro #1 fraction attributable to smelt: '+str(round(pyro_smelt_fract_1*100,2)))
print('Pyro #2 fraction attributable to smelt: '+str(round(pyro_smelt_fract_2*100,2)))


# In[5]:


print('Hydro fraction attributable to mining: '+str(round(hydro_mine_fract*100,2)))
print('Pyro #1 fraction attributable to mining: '+str(round(pyro_mine_fract_1*100,2)))
print('Pyro #2 fraction attributable to mining: '+str(round(pyro_mine_fract_2*100,2)))


# In[6]:


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

# In[7]:


e_refine_fract = 0.2
e_smelt_fract = 0.2
e_mine_fract = 0.6


# In[8]:


cu_refine_country_raw = pd.read_csv(os.path.join(carbonfolder, 'input-USGS-Cu-RefinePrimaryCountries.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)
cu_smelt_country_raw = pd.read_csv(os.path.join(carbonfolder, 'input-USGS-Cu-SmeltPrimaryCountries.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)
cu_mine_country_raw = pd.read_csv(os.path.join(carbonfolder, 'input-USGS-Cu-MinePrimaryCountries.csv'),
                                     index_col='Country')#, usecols=lambda x: x not in skipcols)


# Methods:
# 
# - sum countrywise into overall energy by country %, check sum 100%

# In[9]:


#fill blanks with 0
cu_refine_country_filled = cu_refine_country_raw.fillna(0)
cu_smelt_country_filled = cu_smelt_country_raw.fillna(0)
cu_mine_country_filled = cu_mine_country_raw.fillna(0)


# In[10]:


#get the sums of each step
cu_refine_country_filled['SUM_refine'] = cu_refine_country_filled.sum(axis=1)
cu_smelt_country_filled['SUM_smelt'] = cu_smelt_country_filled.sum(axis=1)
cu_mine_country_filled['SUM_mine'] = cu_mine_country_filled.sum(axis=1)


# In[11]:


#divide by sums to get fractional country contributions
cu_refine_country_fraction = cu_refine_country_filled.divide(cu_refine_country_filled['SUM_refine'], axis=0)
cu_smelt_country_fraction = cu_smelt_country_filled.divide(cu_smelt_country_filled['SUM_smelt'], axis=0)
cu_mine_country_fraction = cu_mine_country_filled.divide(cu_mine_country_filled['SUM_mine'], axis=0)
#cu_mine_country_fraction


# In[12]:


#multiply country % by energy %
cu_refine_country_fraction_WTD = cu_refine_country_fraction*e_refine_fract
cu_smelt_country_fraction_WTD = cu_smelt_country_fraction*e_smelt_fract
cu_mine_country_fraction_WTD = cu_mine_country_fraction*e_mine_fract


# In[13]:


#sum by country
Cu_country_eWTD = pd.concat([cu_refine_country_fraction_WTD, cu_smelt_country_fraction_WTD, 
           cu_mine_country_fraction_WTD]).groupby(['Country']).sum()


# In[39]:


#remove sums, determine most important countries
Cu_country_eWTD_trim = Cu_country_eWTD.filter(regex='^(?!SUM_)')

countries_avg_contribution = Cu_country_eWTD_trim.mean(axis=0)*100
important_countries = countries_avg_contribution.where(countries_avg_contribution>1).dropna()
important_countries.index


# In[47]:


#select only the important countries (so we don't have infinite grid file)
cu_countries_ewtd_important = Cu_country_eWTD_trim.loc[:,list(important_countries.index)]
cu_countries_ewtd_important.columns


# In[62]:


#renormalize to the new sum
normalize_factor = cu_countries_ewtd_important.sum(axis=1)
cu_importantcountries_ewtd2 = cu_countries_ewtd_important.mul((1/normalize_factor), axis=0)*100


# In[64]:


#print out
cu_importantcountries_ewtd2.to_csv(os.path.join(carbonfolder, 'output-copper-CountryMarketshare-MFGing.csv'))


# In[ ]:




