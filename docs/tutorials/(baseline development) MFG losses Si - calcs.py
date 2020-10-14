#!/usr/bin/env python
# coding: utf-8

# # Manufacturing Efficiency Estimation Calculations

# This notebook covers the calculations used to estimate the manufacturing efficiency of silicon for mono and mc Si modules. This data will be utilized in the baseline files for PV DEMICE.
# 
# NOTE: You must run Silicon per m2 journal before running this one, as the calculations depend on grams of silicon per cell.

# In[62]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[63]:


#read in supporting csv files
cwd = os.getcwd() #grabs current working directory
si_g_percell = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/si_g_per_cell.csv", index_col='Year')
kerf_loss_raw = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/kerf_loss_microns.csv", index_col='Year')
utilize_gperwafer_raw = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/utilization_g_perwafer.csv", index_col='Year')
wafer_thickness = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/Wafer_thickness.csv", index_col='Year')


# From the literature resources, we have data points that indicate a 50% input material waste for Silicon per cell prior to 2003. Therefore, we will assume a 50% manufacturing efficiency 1995 through 2003.
# 
# There is a derth of data 2004 through 2009.
# 
# As of 2010, ITRPV data provides kerf loss data, through 2017. This combined with wafer thickness, will be used as a proxy for mfg losses, combined with insights from the ITRPV "polysilicon utilization" data (which includes wafer thickness, kerf loss, crucible size, from squaring to cropping).
# 
# Similarly, as of 2017, ITRPV provides data on "polysilicon utilization", which is expressed as a number of grams of silicon used to make a wafer, and proken down by mono-Si vs. mc-Si and diamond wire vs. slurry cut, and includes projections out to 2030. This data will be utilized for 2017 onward to calculate % manufacturing efficiency relative to the average cell mass calculated by "Silicon g per m2" OR shold we use on a 10g/cell basis that ITRPV uses??

# ## 2010 through 2017

# mfg efficiency by kerf loss proxy is calculated by:
#             
#             [Wafer Thickness/(Wafer Thickness + Kerf Loss)] * 100 = % mfg efficiency (proxy)
# 
# And the inverse or manufacturing inefficiency should be calculated by:
# 
#             [(Wafer Thickness + Kerf Loss)/Wafer Thickness] * 100 = % mfg "inefficeincy"

# In[64]:


#There are missing data in wafer thickness, so we will interpolate linearly for missing years
wafer_thick = wafer_thickness.interpolate(method='linear',axis=0)

#Kerf loss also has missing data (projections), same linear interpolate
kerf_loss = kerf_loss_raw.interpolate(method='linear',axis=0, limit_area='inside')

#concat wafer thickness and kerf loss dfs together
df_thick_kerf = pd.concat([wafer_thick,kerf_loss], axis=1) #concatinate on the columns axis

#print(df_thick_kerf)


# Because slurry and diamond have significantly different kerf losses, we will keep these seperate for as long as possible before averaging.

# In[87]:


df_thick_kerf['slurry_eff'] = df_thick_kerf['wafer_thickness']/(df_thick_kerf['wafer_thickness']+df_thick_kerf['slurry'])
df_thick_kerf['diamond_eff'] = df_thick_kerf['wafer_thickness']/(df_thick_kerf['wafer_thickness']+df_thick_kerf['diamond'])
#for maths, create the "inefficiency" percentage by slurry and diamond
#i.e. this is how much extra material needed to be put in to get out a single wafer unit
df_thick_kerf['slurry_ineff'] = (df_thick_kerf['wafer_thickness']+df_thick_kerf['slurry'])/df_thick_kerf['wafer_thickness']
df_thick_kerf['diamond_ineff'] = (df_thick_kerf['wafer_thickness']+df_thick_kerf['diamond'])/df_thick_kerf['wafer_thickness']
#print(df_thick_kerf)


# As a reality check, and because we have data for 2017 of both kerf loss and "utilization", we can check how good a proxy kerf loss is for utilization of input material.

# In[83]:


#Multiply the proxy mfg efficiency by the averaged g/cell of silicon (as calculated by "Silicon per m2")
check2017_slurry = (si_g_percell['Si_gpercell'][2017])*(df_thick_kerf['slurry_ineff'][2017])
check2017_diamond = (si_g_percell['Si_gpercell'][2017])*(df_thick_kerf['diamond_ineff'][2017])

#extract ITRPV 2017 values for g/wafer utilization, and compute their mean
itrpv2017_slurrys = [utilize_gperwafer_raw['mc-Si-slurry'][2017],utilize_gperwafer_raw['mono-Si-slurry'][2017]]
itrpv2017_diamonds = [utilize_gperwafer_raw['mc-Si-diamond'][2017],utilize_gperwafer_raw['Mono-Si-diamond'][2017]]
itrpv2017_slurry = np.mean(itrpv2017_slurrys)
itrpv2017_diamond = np.mean(itrpv2017_diamonds)

#Compare this calculated value to ITRPV value in 2017
#print("In 2017, the calculated silicon utilization for the slurry cut is ",check2017_slurry, 
      #"g/wafer, and diamond wire cut is",check2017_diamond, "g/wafer.")
#print("In comparison, the 2017 ITRPV average silicon utilization for slurry cut is",itrpv2017_slurry, 
      #"g/wafer, and diamond wire cut is", itrpv2017_diamond, "g/wafer.")

#Compare in a printed out table, since this is hard to see
data = {'Slurry':[check2017_slurry,itrpv2017_slurry],'Diamond':[check2017_diamond,itrpv2017_diamond]}
gperwafer_compare = pd.DataFrame(data, index= ['Calculated','ITRPV'])
print(gperwafer_compare)


# In both cases, the calculated silicon utilization is less than the ITRPV survey collected data. This is unsurprising because the ITRPV utilization accounts for more than kerf loss (which is the basis for the calculated value). Therefore, we will compute the difference, and use this as a factor to add to all calculated values based on kerf loss alone.

# In[80]:


#gperwafer_compared = gperwafer_compare.append(gperwafer_compare.diff())
gperwafer_compared = gperwafer_compare.diff()
#print(gperwafer_compared)
slurry_factor = gperwafer_compared['Slurry']['ITRPV']
diamond_factor = gperwafer_compared['Diamond']['ITRPV']
print("Add ", slurry_factor, "to slurry cut wafer values, and ", diamond_factor, "to diamond wire cut values.")


# In[89]:


#Multiply the proxy mfg efficiency by the averaged g/cell of silicon (as calculated by "Silicon per m2")
#and add the 2017 computed factors
slurry_gpw = (si_g_percell['Si_gpercell']*df_thick_kerf['slurry_ineff'])+ slurry_factor
diamond_gpw = (si_g_percell['Si_gpercell']*df_thick_kerf['diamond_ineff'][2017])+ diamond_factor 
#these are now pd.series, need to create a single value based on marketshare of diamond vs slurry
#we know slurry was around until 2017, last year of ITRPV slurry cut data
#and in 2010, diamond cut isn't mentioned only slurry


# ## 2017 through 2030

# In[ ]:





# ## 1995 through 2003

# Here, as previously stated, we set 2003 and earlier years to 50% mfg efficiency

# In[ ]:





# ## 2004 through 2009

# Until better data is found for this time period, simple linear interpolation will be used.

# In[ ]:




