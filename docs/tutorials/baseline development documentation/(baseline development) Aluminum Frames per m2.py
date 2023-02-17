#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)

cwd = os.getcwd() #grabs current working directory
skipcols = ['Source']


# This journal documents the maths undertaken to estimate the amount of aluminium per meter squared of module as contributed by the frame (i.e. not the aluminium found within the module).

# In[2]:


al_frame_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/marketshare_moduleSize_al_frames.csv", 
                           index_col='Year', usecols=lambda x: x not in skipcols)
module_size_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/MarketShare_moduleSize_Peeters2017.csv", 
                           index_col='Year')


# # 1992 through 2015

# First, we're going to create a lovely baseline from the module size data as derived from Peeters et al. 2017. These data were drawn from PV datasheets, and given a marketshare value from 1992 through 2015. This data may be more specific to Flanders, but it appears to be consistent with ITRPV 2019 and 2020 data, as well as older sources. Therefore, we will utilize this data to represent the increasing size of the module and the perimeter of the module (for the frame).
# 
# J. R. Peeters, D. Altamirano, W. Dewulf, and J. R. Duflou, “Forecasting the composition of emerging waste streams with sensitivity analysis: A case study for photovoltaic (PV) panels in Flanders,” Resources, Conservation and Recycling, vol. 120, pp. 14–26, May 2017, doi: 10.1016/j.resconrec.2017.01.001.
# 

# In[3]:


module_size_fill = module_size_raw.interpolate(limit_direction='both') #fill in 0s and 100s
print(module_size_fill)


# In[4]:


mrktshr_sizes_1992_2015 = module_size_fill/100 #turn into fractions
#check = mrktshr_sizes_1992_2015.agg('sum', 'columns')
#print(check)

d = {'1':[0.5,1],
    '2':[0.7,1.4],
    '3':[0.55,1.2],
    '4':[0.8,1.2],
    '5':[0.8,1.6],
    '6':[0.7,1.5],
    '7':[1,1.5],
    '8':[1,1.65]} #dataframe of module area values to multiply

peeters_dims = pd.DataFrame(data=d)
peeters_dims_cols = peeters_dims.transpose()
peeters_dims_cols.columns = ['x','y']
peeters_dims_cols['area'] = peeters_dims_cols['x']*peeters_dims_cols['y']
peeters_dims_cols['perimeter'] = peeters_dims_cols['x']*2+2*peeters_dims_cols['y']
peeters_dims_full = peeters_dims_cols.transpose()
peeters_dims_cols.index = peeters_dims_full.columns = mrktshr_sizes_1992_2015.columns

print(peeters_dims_cols)
print(peeters_dims_full)


# In[5]:


#multiply the above dataframes together to get module size and perimeter weighted by marketshare
area = pd.Series(peeters_dims_full.loc['area'])
wtd_module_area = mrktshr_sizes_1992_2015.mul(area,'columns')

perimeter = pd.Series(peeters_dims_full.loc['perimeter'])
wtd_module_perimeter = mrktshr_sizes_1992_2015.mul(perimeter,'columns')

#print(wtd_module_area)
#print(wtd_module_perimeter)


# In[6]:


#now agg together for annual average area and perimeter
avg_module_area = pd.DataFrame(wtd_module_area.agg('sum', 'columns'))
avg_module_perimeter = pd.DataFrame(wtd_module_perimeter.agg('sum', 'columns'))
avg_module_area.columns = ['area']
avg_module_perimeter.columns = ['perimeter']

#print(avg_module_area)
#print(avg_module_perimeter)

plt.plot(avg_module_area, label='area [m2]')
plt.plot(avg_module_perimeter, label = 'perimeter [m]')
plt.legend()
plt.ylabel('[m2] and [m]')


# These data only go through 2015, therefore we need more data for recent history. The trend in larger, higher Wp modules has continued, with the ITRPV 2020 restandardizing their average module to 1.7 m^2 in 2019, from 1.64 m^2 previously. This area will be assumed starting in 2019, and it will be assumed to be 1m x 1.7m in dimensions. These assumptions will be added to the datasets below.

# In[7]:


#add years to perimeter data
#create an empty df as a place holder
yrs2 = pd.Series(index=range(2016,2025), dtype='float64')
tempdf2 = pd.DataFrame(yrs2, columns=avg_module_perimeter.columns)
avg_module_perimeter_addrange = pd.concat([avg_module_perimeter, tempdf2]) #attach it to rest of df
#print(avg_module_perimeter_addrange)


# In[8]:


#calculate the perimeter in 2019 from 1.7
perimeter_2019 = 2*1+2*1.7
avg_module_perimeter_addrange.loc[2019] = perimeter_2019
avg_module_perimeter_full = avg_module_perimeter_addrange.interpolate(limit_direction='both')
#print(avg_module_perimeter_full)


# In[9]:


#add years to area data
#create an empty df as a place holder
yrs3 = pd.Series(index=range(2016,2025), dtype='float64')
tempdf3 = pd.DataFrame(yrs3, columns=avg_module_area.columns)
avg_module_area_addrange = pd.concat([avg_module_area, tempdf3]) #attach it to rest of df

#now set 2019 = 1.7m^2
avg_module_area_addrange.loc[2019] = 1.7
avg_module_area_full = avg_module_area_addrange.interpolate(limit_direction='both')
#print(avg_module_area_full)


# In[10]:


plt.plot(avg_module_area_full, label = 'area [m2]')
plt.plot(avg_module_perimeter_full, label='perimeter [m]')
plt.legend()


# Now we have module area and perimeter through 2025, we can combine these with the density of aluminum OR mass per meter of Al. The maths to arrive at mass of Al per m2 of module will be:
# 
#     kg/meter * module perimeter (m) / module area (m2) = kg/m2 of module
#     
# The ITRPV has kg/m values of Al frames in the 2012 and 2013 editions, indicating an average of 0.6 kg/m in 2012. A 1995 LCA used 0.35 kg/m, and 1 to 1.4 kg of aluminum per module. And Finally, Peeters et al (from above) used 0.45 kg/m, and was published in 2017, and agrees closely with ITRPV data. It seems unlikely that the aluminum frame got thicker or heavier between 1995 and 2012, therefore, we will assume the heavier frame all the way back.

# ## Mass per Meter of Frame Data Munging

# In[11]:


al_mass_per_m_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/al_kg_per_m.csv", 
                           index_col='Year', usecols=lambda x: x not in skipcols)
print(al_mass_per_m_raw)


# In[12]:


#create an empty df as a place holder
yrs = pd.Series(index=range(1992,2012), dtype='float64')
tempdf = pd.DataFrame(yrs, columns=['AL_kg_per_m'])
al_kgpm_addrange = pd.concat([tempdf,al_mass_per_m_raw]) #attach it to rest of df
#print(al_kgpm_addrange)
#set the 2050 value to the same as 2030
#fulldf.loc[2050] = fulldf.loc[2030]
#interpolate for missing values
#ag_gpm2_full = fulldf.interpolate()


# Knowing that the 2017 data point is from Peeters et al.2017, we observe it is slightly higher than the ITRPV projection on either side (0.45 vs 0.4). Given that the 0.45 from Peeters etal was base on manufacturers datasheets, whereas the ITRPV was a 2014 projection, we will use the 0.45 kg/m data from 2017 forward, and correct 2016 up to 0.45.

# In[13]:


al_kgpm_addrange.loc[2016:] = 0.45 #set 2016 on equal to Peeters values
al_kgpm_addrange.loc[1992] = al_kgpm_addrange.loc[2012] #extend the 0.6 kg/m back through 1992
al_kgpm = al_kgpm_addrange.interpolate(limit_direction='both')
#print(al_kgpm)
plt.plot(al_kgpm)


# Now multiply the perimeter of the module annually by the mass per meter annually

# In[14]:


#bind mass and perimeter together for calcs
mass_perimeter = pd.concat([al_kgpm, avg_module_perimeter_full], axis=1)
mass_perimeter['mass_total_kg'] = mass_perimeter['AL_kg_per_m']*mass_perimeter['perimeter']
print(mass_perimeter)


# Now we have a mass per module in kg due to the Aluminum frame. This value will now be divided by module area.

# In[15]:


al_kgpm2 = pd.concat([mass_perimeter['mass_total_kg'], avg_module_area_full], axis=1)
al_kgpm2['Al_gpm2'] = al_kgpm2['mass_total_kg']/al_kgpm2['area']*1000
#print(al_kgpm2)
plt.plot(al_kgpm2['Al_gpm2'], label='Al_gpm2')
plt.legend()


# ## Then, weight this value by the marketshare of framed vs frameless

# In addition to the average module size, there are some modules which have no frame. The ITRPVs captured this data, and it will be applied here to appropriately weight the average module having a frame or not.

# In[16]:


frame_noframe_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/marketshare_frame-noframe.csv", 
                           index_col='Year', usecols=lambda x: x not in skipcols)
print(frame_noframe_raw)


# Prior to 2013, the ITRPV describes aluminum frames as "the norm", therefore we will assume prior to 2013 that all modules had aluminum frames. Similarly, the fraction of frameless modules continues to grow, therefore the 2020 projection out to 2030 will be used, then held constant through 2050.

# In[17]:


#Select down to only Al frame percentage
framed_perc = pd.DataFrame(frame_noframe_raw['Al_framed'])

#create an empty df as a place holder
yrs4 = pd.Series(index=range(1992,2013), dtype='float64')
tempdf4 = pd.DataFrame(yrs4, columns=['Al_framed'])
framed_fract_empty = pd.concat([tempdf4,framed_perc]) #attach it to rest of df
framed_perc_full = framed_fract_empty.interpolate(limit_direction='both')
#print(framed_perc_full)
plt.plot(framed_perc_full)


# In[18]:


#Convert percentage to fraction
framed_perc = framed_perc_full/100

#bind together
al_kgpm2_mrktshr = pd.concat([framed_perc, al_kgpm2['Al_gpm2']], axis=1)
al_kgpm2_mrktshr.ffill(axis=0, inplace=True) #hold 2024 values of al g/m2 through 2030

#multiply to get 3rd column of marketshare weighted data
al_kgpm2_mrktshr['Al_wtd_gpm2'] = al_kgpm2_mrktshr['Al_framed']*al_kgpm2_mrktshr['Al_gpm2']

#print(al_kgpm2_mrktshr)
plt.plot(al_kgpm2_mrktshr['Al_wtd_gpm2'])
plt.title('Final Marketshare-Weighted Al Frame Mass per Module m2')
plt.ylabel("g/m2 of module")


# In[19]:


final_al_gpm2 = pd.DataFrame(al_kgpm2_mrktshr['Al_wtd_gpm2'])
final_al_gpm2.to_csv(cwd+'/../../../PV_ICE/baselines/SupportingMaterial/output_al_g_per_m2.csv', index=True)


# # Calculations for increasing fraction of glass-glass to 50% by 2030 (hold through 2050)

# Matching the glass calculations, bifacial glass-glass modules are typically frameless. Therefore, to project bifacial trends, we need to change the fraction of frameless going forward. In the Glass projection, we predict 50% glass-glass bifacial by 2030, original ITRPV was 30% glass-glass. ITRPV predicts 23% frameless by 2030, so the corresponding increase in frameless for 50% bifacial would be 38.3% frameless (simple ratio calc). If we assume 4% plastic frames (ITRPV), then framed marketshare is 100-4-38.3 = 57.7%

# In[20]:


#Create new projection for 38.3% frameless by 2030
framed_perc_history = framed_perc_full.loc[(framed_perc_full.index<=2020)]

yrs_future = pd.Series(index=range(2021,2031), dtype='float64')
framed_future = pd.DataFrame(yrs_future, columns=['Al_framed'])
framed_future['Al_framed'].loc[2030] = 57.7

bifi_future_alframes = pd.concat([framed_perc_history, framed_future])
bifi_future_alframes_full = bifi_future_alframes.interpolate(limit_direction='both')
bifi_future_alframes_perc = bifi_future_alframes_full/100

al_kgpm2_bifimrktshr = pd.concat([bifi_future_alframes_perc, al_kgpm2['Al_gpm2']], axis=1)
al_kgpm2_bifimrktshr.ffill(axis=0, inplace=True) #hold 2024 values of al g/m2 through 2030
bifi_future = al_kgpm2_bifimrktshr['Al_framed']*al_kgpm2_bifimrktshr['Al_gpm2']

#print(bifi_future)
plt.plot(bifi_future, label='bifacial future')
plt.plot(al_kgpm2_mrktshr['Al_wtd_gpm2'], label='ITRPV 23% frameless')
plt.legend()

bifi_future_al_gpm2 = pd.DataFrame(bifi_future)
bifi_future_al_gpm2.to_csv(cwd+'/../../../PV_ICE/baselines/SupportingMaterial/output_al_g_per_m2_bifacial.csv', index=True)

