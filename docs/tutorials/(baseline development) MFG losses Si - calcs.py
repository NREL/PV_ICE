#!/usr/bin/env python
# coding: utf-8

# # Manufacturing Efficiency Estimation Calculations

# This notebook covers the calculations used to estimate the manufacturing efficiency of silicon for mono and mc Si modules. This data will be utilized in the baseline files for PV DEMICE.
# 
# NOTE: You must run Silicon per m2 journal before running this one, as the calculations depend on grams of silicon per cell.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[2]:


#read in supporting csv files
cwd = os.getcwd() #grabs current working directory
si_g_percell = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/si_g_per_cell.csv", index_col='Year')
kerf_loss_raw = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/kerf_loss_microns.csv", index_col='Year')
utilize_gperwafer_raw = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/utilization_g_perwafer.csv", index_col='Year')
wafer_thickness = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/Wafer_thickness.csv", index_col='Year')
wafering_marketshare = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/wafering_marketshare.csv", index_col='Year')
marketshare_mono_mc = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/scaledmrktshr_mcSi_mono.csv", index_col='Year')


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

# In[3]:


#There are missing data in wafer thickness, so we will interpolate linearly for missing years
wafer_thick = wafer_thickness.interpolate(method='linear',axis=0)

#Kerf loss also has missing data (projections), same linear interpolate
kerf_loss = kerf_loss_raw.interpolate(method='linear',axis=0, limit_area='inside')

#concat wafer thickness and kerf loss dfs together
df_thick_kerf = pd.concat([wafer_thick,kerf_loss], axis=1) #concatinate on the columns axis

#print(df_thick_kerf)


# Because slurry and diamond have significantly different kerf losses, we will keep these seperate for as long as possible before averaging.

# In[4]:


df_thick_kerf['slurry_eff'] = df_thick_kerf['wafer_thickness']/(df_thick_kerf['wafer_thickness']+df_thick_kerf['slurry'])
df_thick_kerf['diamond_eff'] = df_thick_kerf['wafer_thickness']/(df_thick_kerf['wafer_thickness']+df_thick_kerf['diamond'])
#for maths, create the "inefficiency" percentage by slurry and diamond
#i.e. this is how much extra material needed to be put in to get out a single wafer unit
df_thick_kerf['slurry_ineff'] = (df_thick_kerf['wafer_thickness']+df_thick_kerf['slurry'])/df_thick_kerf['wafer_thickness']
df_thick_kerf['diamond_ineff'] = (df_thick_kerf['wafer_thickness']+df_thick_kerf['diamond'])/df_thick_kerf['wafer_thickness']
#print(df_thick_kerf)


# ### 2017 check - compare kerf loss calc to ITRPV "utilization"

# As a reality check, and because we have data for 2017 of both kerf loss and "utilization", we can check how good a proxy kerf loss is for utilization of input material.

# In[5]:


#Multiply the proxy mfg efficiency by the averaged g/cell of silicon (as calculated by "Silicon per m2")
check2017_slurry = (si_g_percell['Si_gpercell'][2017])*(df_thick_kerf['slurry_ineff'][2017])
check2017_diamond = (si_g_percell['Si_gpercell'][2017])*(df_thick_kerf['diamond_ineff'][2017])

#Compare in a printed out table
data = {'Slurry':[check2017_slurry,utilize_gperwafer_raw['mc-Si-slurry'][2017],utilize_gperwafer_raw['mono-Si-slurry'][2017]],
        'Diamond':[check2017_diamond,utilize_gperwafer_raw['mc-Si-diamond'][2017],utilize_gperwafer_raw['Mono-Si-diamond'][2017]]}
gperwafer_compare = pd.DataFrame(data, index= ['Calculated','ITRPV_mc-Si','ITRPV_mono'])

print(gperwafer_compare)


# The calculated values based on just kerf loss are lower than ITRPV findings. This is unsurprising, since the ITRPV polysilicon utilization includes more than just kerf losses. We will compute the differences, and use this as a factor to add to all calculated values based on kerf loss alone.

# In[6]:


#gperwafer_compared = gperwafer_compare.append(gperwafer_compare.diff()) 
    #diff compares to a prior or later row always relative to current index
calcd = gperwafer_compare.loc['Calculated']
gperwafer_factors = gperwafer_compare.sub(calcd)
print(gperwafer_factors)


# Now we will add these factors in and create a section of the final MFG losses (2010-2017).

# In[7]:


#Multiply the proxy mfg inefficiency by the averaged g/cell of silicon (as calculated by "Silicon per m2")
#and add the 2017 computed factors, keeping mono and mc-Si separate.
slurry_mcSi_gpw = (si_g_percell['Si_gpercell']*df_thick_kerf['slurry_ineff'])+ gperwafer_factors['Slurry']['ITRPV_mc-Si']
slurry_mono_gpw = (si_g_percell['Si_gpercell']*df_thick_kerf['slurry_ineff'])+ gperwafer_factors['Slurry']['ITRPV_mono']
diamond_mcSi_gpw = (si_g_percell['Si_gpercell']*df_thick_kerf['diamond_ineff'])+ gperwafer_factors['Diamond']['ITRPV_mc-Si']
diamond_mono_gpw = (si_g_percell['Si_gpercell']*df_thick_kerf['diamond_ineff'])+ gperwafer_factors['Diamond']['ITRPV_mono']
mfg_losses_bytype = pd.concat([slurry_mcSi_gpw, slurry_mono_gpw, diamond_mcSi_gpw, diamond_mono_gpw], axis=1)
mfg_losses_bytype.columns = ['slurry_mcSi','slurry_mono','diamond_mcSi','diamond_mono']
#print(mfg_losses_bytype)


# Because the market shares of slurry + diamond sum to 1 for each mono and mcSi, we will first weight (multiply and sum) the grams per wafer by technology. i.e. slurry_mcSi and diamond_mcSi will be combined.

# In[8]:


#Now weight the data by marketshare of type of cut
#Convert wafering marketshares to percentages for multiplication, and interpolate for the missing year
wafering_mrktshr = wafering_marketshare/100
wafering_mrktshr = wafering_mrktshr.interpolate(method='linear',axis=0, limit_area='inside')
#print(wafering_mrktshr)

#set column names identical for multiplying
mfg_losses_bytype.columns = wafering_mrktshr.columns = mfg_losses_bytype.keys()
mfg_losses_wtd = wafering_mrktshr.mul(mfg_losses_bytype, 'columns')

#combine by tech type (mono vs. mc-Si)
mfg_losses_wtd_mcSi = mfg_losses_wtd.filter(regex = 'mcSi')
mfg_losses_mcSi = pd.DataFrame(mfg_losses_wtd_mcSi.agg("sum", axis="columns"))
mfg_losses_mcSi.columns = ['mcSi_gpw']

mfg_losses_wtd_mono = mfg_losses_wtd.filter(regex = 'mono')
mfg_losses_mono = pd.DataFrame(mfg_losses_wtd_mono.agg("sum", axis="columns"))
mfg_losses_mono.columns = ['mono_gpw']

#combine into a single dataframe
gpw_cutwtd = pd.concat([mfg_losses_mono,mfg_losses_mcSi], axis=1)
gpw_cutwtd.columns = ['monoSi', 'mcSi']
plt.plot(gpw_cutwtd)
#print(gpw_cutwtd)


# Now that we have a grams per wafer based on cut type for each PV tech type (mono vs mcSi), we will weight these data by the marketshare of installed PV type, creating an average module for the year.

# In[9]:


#Now weight by marketshare of mcSi vs Mono Si installed/made, as based on the silicon per m2 journal
#CAUTION: This is a lot of market weighting and averaging - may obsecure original data
gpw = gpw_cutwtd.mul(marketshare_mono_mc, 'columns')
gpw_avg = pd.DataFrame(gpw.agg("sum", axis="columns"))
gpw_avg.columns = ['avg_g_per_wafer']

#slice the dataframe for the relevant years and plot
gpw_avg_2010_2017 = gpw_avg.loc[(gpw_avg.index>=2010) & (gpw_avg.index<=2016)]
plt.plot(gpw_avg_2010_2017)
plt.title('Weighted Average grams of Si to make a Cell')
plt.ylabel('Grams of Silicon per cell')
#print(gpw_avg_2010_2017)


# ## 2017 through 2030

# Now that 2010 through 2016 is accounted for through kerf loss and compensation, we will use the ITRPV forward looking projections of "polysilicon utilization" to determine mfg efficiency. This will be done simply by linearly interpolating ITRPV data for the missing years through 2030, then weighting by marketshare of mcSi vs mono. 2017 will also have weighting by slurry vs diamond.

# In[10]:


#fill in missing ITRPV years
utilize_gpw = utilize_gperwafer_raw.interpolate(method='linear',axis=0, limit_area='inside')

#2017 double weighting
gpw2017_mcSi = wafering_mrktshr['slurry_mcSi'][2017]*utilize_gpw['mc-Si-slurry'][2017]+wafering_mrktshr['diamond_mcSi'][2017]*utilize_gpw['mc-Si-diamond'][2017]
gpw2017_mono = wafering_mrktshr['slurry_mono'][2017]*utilize_gpw['mono-Si-slurry'][2017]+wafering_mrktshr['diamond_mono'][2017]*utilize_gpw['Mono-Si-diamond'][2017]
gpw2017 = gpw2017_mcSi*marketshare_mono_mc['mcSi'][2017] + gpw2017_mono*marketshare_mono_mc['monoSi'][2017]
#print(gpw2017)

#now do 2018 through 2030, and append together to create single df
utilize_gpw_trim = utilize_gpw.drop(['mc-Si-slurry','mono-Si-slurry'], axis=1)
gpw_1980t2030 = utilize_gpw_trim['mc-Si-diamond']*marketshare_mono_mc['mcSi'] + utilize_gpw_trim['Mono-Si-diamond']*marketshare_mono_mc['monoSi']
gpw_2017t2030 = pd.DataFrame(gpw_1980t2030.loc[(gpw_1980t2030.index>=2017)])

#put the data together
gpw_2017t2030.columns = ['avg_g_per_wafer']
gpw_2017t2030['avg_g_per_wafer'][2017] = gpw2017
#print(gpw_2017t2030)
plt.plot(gpw_2017t2030)
plt.title('Weighted Average grams of Si to make a Cell')
plt.ylabel('Grams of Silicon per cell')


# ## 1995 through 2003

# INSERT WILLEKE 2002 45%-35% MFG YIELD DATA, FIG 3

# Here, as previously stated, we set 2003 and earlier years to 50% mfg efficiency. A 50% MFG efficiency corresponds to using 2x as much material as ends up in the final cell. Therefore, we will multiply the grams of silicon per cell, as calculated by the silicon baseline, by 2.0. Because the cell size changes from 100mm on a side to 125 mm on a side (step change) there is a resulting step change increase in the amount of silicon used per cell.

# In[15]:


#multiply by the "inefficiency"
si_gpc_ineff = si_g_percell*2.0
#Trim to relevant years, 1995 through 2003
gpw_1995t2003 = si_gpc_ineff.loc[(si_gpc_ineff.index<=2003)]
gpw_1995t2003.columns = ['avg_g_per_wafer']
#print(gpw_1995t2003)
plt.plot(gpw_1995t2003)


# ## 2004 through 2009

# Until better data is found for this time period, simple linear interpolation between 2003 and 2010 will be used.

# In[12]:


#create an empty df as a place holder for interpolation with years
yrs = pd.Series(index=range(2004,2010), dtype='float64')
tempdf = pd.DataFrame(yrs, columns=['avg_g_per_wafer'])

#squish prior datasets together
gpc = pd.concat([gpw_1995t2003, tempdf, gpw_avg_2010_2017, gpw_2017t2030])
gpc_final = gpc.interpolate()
#print(gpc_final)
plt.plot(gpc_final)
plt.ylabel('Grams of Silicon per cell')
plt.title('Average grams of silicon input per cell')


# # Calculate MFG efficiency from grams input per cell and cell mass

# Now that we have a mass of silicon needed to create a cell for each year, this will be compared to the calculated mass of silicon per cell (again, silicon baseline avg calculation), and the resulting comparison will provide a manufacturing efficiency. This efficiency is specified in terms of what percent(%) of material input ends up in the cell (inefficiency here is defined as the % extra needed). i.e.
#                 Mass of cell / Mass of input material *100 = MFG efficiency (%)

# In[13]:


si_g_percell.columns = gpc_final.columns
mfg_eff_si = (si_g_percell / gpc_final)*100
#print(mfg_eff_si)
plt.plot(mfg_eff_si)
plt.ylabel('Manufacturing Efficiency of Si(%)')
plt.title('Manufacturing Efficiency of Si on a per cell basis, Averaged')
mfg_eff_si.to_csv(cwd+'/../../PV_DEMICE/baselines/SupportingMaterial/mfg_eff_si.csv', index=True)


# The reason there is a massive drop in mfg efficiency between 2004 and 2009 is primarily due to a rapid decrease in wafer thickness (300 micron to 180 micron).

# In[18]:


#other pretty plots to tell the diamond wire saw story
#create the forward and backward "history" of type of wafercut
years = pd.Series(index=range(1995,2031), dtype='float64')
df_empty = pd.DataFrame(years)
wafercut_mrktshr = df_empty.join(wafering_mrktshr)
wafercut_mrktshr.drop([0,'slurry_mcSi','slurry_mono'], axis=1, inplace=True)
wafercut_diamond_history = wafercut_mrktshr.interpolate(limit_direction='both')
wafercut_diamond_history = wafercut_diamond_history*100
#print(wafercut_diamond_history)

#now plot wafer cut history and g/cell mfg eff on the same plot
#labels = wafercut_diamond_history.columns
plt.plot(wafercut_diamond_history.diamond_mcSi/100, label='mcSi')
plt.plot(wafercut_diamond_history.diamond_mono/100, label='monoSi')
plt.plot(mfg_eff_si/100, '--k', label='MFG eff Si')
plt.plot(wafer_thick/1000, label='Wafer Thickness (mm)')
plt.ylabel('% Market share or % MFG Efficiency')
plt.title('History of Si MFG eff vs rise of Diamond wire')
plt.legend()

