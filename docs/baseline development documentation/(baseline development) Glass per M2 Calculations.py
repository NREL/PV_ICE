#!/usr/bin/env python
# coding: utf-8

# # (baseline development) Glass per M2 Calculations
# 

# Based on ITRPV numbers for the most part, this journal attempts to correlate front glass thickness values with the introduction of glass-glass modules.
# 
# Standard front glass thickness is set to 3.2 mm, based on ITRPV 2014, 2012 and 2011. Starting 2017, front glass are divided into >3 mm, 2-3 mm. Assuming that >3mm is still 3.2 mm. Thinner modules in the range of 2-3mm coincide with the values of Glass-Glass modules, so we are assuming all thiner modules have a backside of same thickness as front of 2.5 mm
# 
# So overall thickness of glass per panel goes from 3.2 to 5 mm for Glass-backsheet to Glass-Glass modules.
# 

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)

cwd = os.getcwd() #grabs current working directory
skipcols = ['Source', 'Source.1']
density_glass = 2500*1000 # g/m^3    


# #### Up to 2012

# In[2]:


thickness_glass = 0.0032  # m
glassperm2 = thickness_glass * density_glass
print("Glass g/m2 up to 2012:", glassperm2)


# #### 2013 - 2016

# Glass-Glass percentage starts to increase over the following years. 
# 
# On ITRPV, percentage for 2013 is 98% glass-backsheet,
# percentage for 2014 is 96 % glass-backsheet
# percentage for 2016 is 97 % glass -backsheet.
# 
# We think it's strange that the % of glass-glass modules went suddenly up in 2014 and then back down in 2016. However we're going ahead with this percentages and will quantify this disaprity as uncertainty with the MC analysis.
# 
# Data is not available on Glass-Glass modules for 2015 so we're interpolating between previous year

# In[3]:


#2013
thickness_glass = 0.0032 * 0.98 + (0.0032+0.0032)*0.02 # m
glassperm2 = thickness_glass * density_glass
print("Glass g/m2 2013:", glassperm2)


# In[4]:


#2014
thickness_glass = 0.0032 * 0.96 + (0.0032+0.0032)*0.04 # m
glassperm2 = thickness_glass * density_glass
print("Glass for 2014:", glassperm2)


# In[5]:


#2015
thickness_glass = 0.0032 * 0.965 + (0.0032+0.0032)*0.035 # m
glassperm2 = thickness_glass * density_glass
print("Glass g/m2 2015:", glassperm2)


# In[6]:


#2016 
thickness_glass = 0.0032 * 0.97 + (0.0032+0.0032)*0.03 # m
glassperm2 = thickness_glass * density_glass
print("Glass g/m2 2016:", glassperm2)


# #### 2017 onwards
# 
# Starting 2017, ITRPV includes data on modules with Front glass between 2-3mm thick. Data is also available in various years for the percentage of modules that are Glass-Backsheet, vs Glass-Glass. The percentages for 2-3mm and Glass-Glass modules are very similar. We're assuming that 100% of the Glass-Glass modules are therefore 2-3mm thick for their front AND their back glass. Remaining percentage (if any) of 2-3mm front glasses are assumed to be Glass-backsheet.
# For example for 2017:
# 
# ![ITRPV Glass thicknesses deduction example](../images_wiki/ITRPV_GlassDeduction.PNG)
# 

# In[7]:


#2017
thickness_glass = 0.0032 * (0.94 + 0.01) + (0.0025+0.0025)*0.05 # m
glassperm2 = thickness_glass * density_glass
print("2017:", glassperm2)


# Years afer 2017 that don't have values for any these two categories got interpolated.

# ## Calculations of glass per m2 using ITRPV projections

# Typically, glass-glass modules use 2 different sheets of glass on the front and back. The frontside thickness has slowly but steadily decreased, as recorded by ITRPVs. The back side glass is typically thinner or equal to the front side; here we will assume it is of equal thickness. 

# In[8]:


glass_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/Marketshare_glass.csv", 
                           index_col='Year', usecols=lambda x: x not in skipcols)
#print(glass_raw)


# We are going to take the glass thickness projections from ITRPV through 2030, and then hold constant through 2050. We will assume the greater than 3 mm thickness to be 3.2mm (as stated before), and we will assume less than 2mm thickness is 1.8mm.

# In[9]:


#subset glass raw down to only thickness data
glass_thick = glass_raw.filter(regex = 'mm')

#combine 3.2mm column and greater than 3mm column together
glass_thick['assume3pt2mm'] = glass_thick.pop('3pt2mm').fillna(glass_thick.pop('gtr3mm')).astype(float)

#set the 2-3mm 2013 datapoint to 0 (i.e. everything was 3.2mm)
glass_thick['2to3mm'].loc[2013] = 0.0

#interpolate
glass_thick_full = glass_thick.interpolate(limit_direction='both')

#check that percents add to 100
#check = pd.DataFrame(glass_thick_full.agg("sum", axis="columns"))

plt.plot(glass_thick_full)
plt.title('marketshares of 3 different glass thicknesses')
#print(glass_thick_full)


# In[10]:


thicknesses = {'assume3pt2mm':3.2,
            '2to3mm':2.5,
            'less2mm':1.8} #dictionary of the glass thicknesses
glass_thick_percs = glass_thick_full/100

#Multiply each marketshare by the thickness of glass
wtd_glass_thick_split = glass_thick_percs.mul(thicknesses,'columns')
wtd_glass_thick = pd.DataFrame(wtd_glass_thick_split.agg("sum", axis="columns"))
wtd_glass_thick.columns = ['avg_glass_thickness_mm']

#print(wtd_glass_thick)
plt.plot(wtd_glass_thick)
plt.title('Weighted average glass thickness (front and back) in mm')


# Now fill in the gaps of the marketshares of glass-glass vs glass-backsheet for all time, again holding constant 2030 through 2050.

# In[11]:


conformation = glass_raw.filter(regex = '-')
conformation['foil-foil'].loc[2020] = 0
#there is mention of glass-glass in the 2012 ITRPV, but not before that, 
#therefore, we will assume everything is glass-backsheet 2011 and earlier
conformation['glass-backsheet'].loc[2011] = 100
conformation['glass-glass'].loc[2011] = 0

#interpolate to fill in marketshare gaps
conformation_filled = conformation.interpolate(limit_direction='both')
#print(conformation_filled)


# Combine average thickness of glass with marketshare of each conformation, with density of glass to get mass glass per m^2

# In[12]:


conformation_perc = conformation_filled/100
#print out to csv for use in backsheet journal
conformation_perc.to_csv(cwd+'/../../../PV_ICE/baselines/SupportingMaterial/output_marketshare_glassVbacksheet.csv')


# In[13]:


#eqn = density glass * mm to m * [(mrktshr g-g * 2 * avg glass thickmm )+ (mrktshr g-b * 1 * avg glass thick)]
mass_glass_pm2 = density_glass*(0.001)*((conformation_perc['glass-glass']*2*wtd_glass_thick['avg_glass_thickness_mm']) + (conformation_perc['glass-backsheet']*wtd_glass_thick['avg_glass_thickness_mm']))
mass_glass_pm2_baseline = pd.DataFrame(mass_glass_pm2)
mass_glass_pm2_baseline.to_csv(cwd+'/../../../PV_ICE/baselines/SupportingMaterial/output_glass_g_per_m2.csv', index=True)

#print(mass_glass_pm2)
plt.plot(mass_glass_pm2_baseline)
plt.title('Baseline g/m^2 of glass')


# ### UPDATE: Baseline calculation for CdTe
# 
# CdTe is glass-glass, so the marketshare will be 100% for it, which simplifies everything. What i will o is taking the weighted average glass thickness and remake the baseline with the same thickness reduction assumptions.

# In[14]:


#eqn = density glass * mm to m * [(mrktshr g-g * 2 * avg glass thickmm )
mass_glass_pm2_cdte = density_glass*(0.001)*(2*wtd_glass_thick['avg_glass_thickness_mm']) 
mass_glass_pm2_baseline_cdte = pd.DataFrame(mass_glass_pm2_cdte)
mass_glass_pm2_baseline_cdte.to_csv(cwd+'/../../../PV_ICE/baselines/SupportingMaterial/output_glass_g_per_m2_cdte.csv', index=True)

#print(mass_glass_pm2)
plt.plot(mass_glass_pm2_baseline_cdte)
plt.title('Baseline g/m^2 of glass in CdTe')


# # Calculations for increasing fraction of glass-glass to 50% by 2030 (hold through 2050)

# In[15]:


#We would like to predict 50% glass-glass by 2030, and hold at 50% glass-glass through 2050
#collect only historical data on conformation
history_glass = conformation_filled.loc[(conformation_filled.index<=2020),['glass-backsheet','glass-glass']]

#create an empty df to append to historical data, populate with our projections
yrs = pd.Series(index=range(2021,2051), dtype='float64')
tempdf = pd.DataFrame(yrs, columns=['glass-backsheet'])
tempdf['glass-glass'] = tempdf['glass-backsheet']#creates a new NaN column - IMPROVE THIS METHOD

tempdf['glass-glass'].loc[2030] = 50
tempdf['glass-backsheet'].loc[2030] = 50

#Now append history to placeholder
halfglass2030 = pd.concat([history_glass,tempdf])

#And interpolate for values.
halfglass2030proj = halfglass2030.interpolate(limit_direction='both')
#print(halfglass2030proj)
#check that percents add to 100
#check = pd.DataFrame(halfglass2030proj.agg("sum", axis="columns"))
#print(check)

plt.plot(halfglass2030proj)
plt.title('marketshares of glass-backsheet and glass-glass')


# Now we have the weighted average thickness of glass annually, as well as the marketshares of glass-backsheet and glass-glass module conformation. These will be combined to determine a glass mass per module m^2 annually for 50% glass-glass by 2030.

# In[16]:


#convert to % marketshare 
halfglass2030_percs = halfglass2030proj/100

#eqn = density glass * mm to m * [(mrktshr g-g * 2 * avg glass thickmm )+ (mrktshr g-b * 1 * avg glass thick)]
mass_glass = density_glass*(0.001)*((halfglass2030_percs['glass-glass']*2*wtd_glass_thick['avg_glass_thickness_mm']) + (halfglass2030_percs['glass-backsheet']*wtd_glass_thick['avg_glass_thickness_mm']))
#print(mass_glass)
#print out to a csv
glass_pm2 = pd.DataFrame(mass_glass)
glass_pm2.to_csv(cwd+'/../../../PV_ICE/baselines/SupportingMaterial/output_glass_g_per_m2_projection.csv', index=True)


# In[17]:


plt.plot(mass_glass)
plt.title('g of glass per module m^2, 50% glass-glass by 2030')
plt.ylim([7500,11000])


# In[18]:


#For comparison, here is what we previously had for predictions
#print(glass_baseline)
plt.plot(mass_glass, label='50% glass-glass by 2030')
plt.plot(mass_glass_pm2_baseline, label='ITRPV projections of glass pm2')
plt.legend()


# In[19]:


#For comparison, plot marketshare of glass-glass vs marketshare of 2-3mm, because glass-glass means you can use thinner glass
plt.plot(halfglass2030_percs['glass-glass']*100, label='50% glass-glass by 2030')
plt.plot(glass_thick_full['2to3mm'], label='marketshare 2 to 3mm thick glass')
plt.plot(conformation_filled['glass-glass'], label='ITRPV marketshare glass-glass')
plt.legend()


# # Upper Error bar - everything is 3.2 mm glass

# Creating a baseline as an "upper error bar" of what if all PV tech used 3.2 mm in future, as an absolute upper limit of how much glass that would entail. Keeping historical data, so modifications from 2021 forward.

# In[20]:


#print(conformation_perc)
#eqn = density glass * mm to m * [(mrktshr g-g * 2 * avg glass thickmm )+ (mrktshr g-b * 1 * avg glass thick)]

#multiply glass-backsheet by wtd average glass trend
mass_glass_pm2_glassbacksheet = density_glass*(0.001)*(conformation_perc['glass-backsheet']*3.2)
#print(mass_glass_pm2_glassbacksheet)
#multiply g-g by (3.2 mm *2)
mass_glass_pm2_glassglass = density_glass*(0.001)*(conformation_perc['glass-glass']*2*3.2)
#print(mass_glass_pm2_glassglass)

#combine 
mass_glass_pm2_errorUpper = pd.DataFrame(mass_glass_pm2_glassbacksheet+mass_glass_pm2_glassglass)
#print(mass_glass_pm2_errorUpper)

#overwrite 2020 and earlier with historical data
mass_glass_pm2_errorUpper.loc[:2020] = mass_glass_pm2_baseline.loc[:2020]

#output and plot
mass_glass_pm2_errorUpper.to_csv(cwd+'/../../../PV_ICE/baselines/SupportingMaterial/output_glass_g_per_m2_projection.csv', index=True)
plt.plot(mass_glass_pm2_errorUpper, label='Upper Error, all PV reverts to 3.2mm after 2020')
plt.plot(mass_glass_pm2_baseline, label = 'Glass ITRPV improvement baseline')
plt.legend(bbox_to_anchor=(0, -0.2, 1, 0), loc=2, mode="expand")


# # Lower Error bar - Everything is 1.8 mm

# On the converse side, let's assume everything improves to use 1.8mm glass

# In[21]:


#print(conformation_perc)
#eqn = density glass * mm to m * [(mrktshr g-g * 2 * avg glass thickmm )+ (mrktshr g-b * 1 * avg glass thick)]

#multiply glass-backsheet by wtd average glass trend
mass_glass_pm2_glassbacksheet = density_glass*(0.001)*(conformation_perc['glass-backsheet']*1.8)
#print(mass_glass_pm2_glassbacksheet)
#multiply g-g by (3.2 mm *2)
mass_glass_pm2_glassglass = density_glass*(0.001)*(conformation_perc['glass-glass']*2*2.0)
#print(mass_glass_pm2_glassglass)

#combine 
mass_glass_pm2_errorLower = pd.DataFrame(mass_glass_pm2_glassbacksheet+mass_glass_pm2_glassglass)
#print(mass_glass_pm2_errorUpper)

#overwrite 2020 and earlier with historical data
mass_glass_pm2_errorLower.loc[:2020] = mass_glass_pm2_baseline.loc[:2020]
plt.plot(mass_glass_pm2_errorLower, label='Lower Error, all PV achieves 1.8mm after 2020')
plt.plot(mass_glass_pm2_errorUpper, label='Upper Error, all PV reverts to 3.2mm after 2020')
plt.plot(mass_glass_pm2_baseline, label = 'Glass improvement baseline')
plt.legend(bbox_to_anchor=(0, -0.2, 1, 0), loc=2, mode="expand")

