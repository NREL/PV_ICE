#!/usr/bin/env python
# coding: utf-8

# # (baseline development) Silicon per M2 Calculations

# This journal documents the methods and assumptions made to create a baseline material file for silicon.

# ## Mass per M2

# The mass of silicon contained in a PV module is dependent on the size, thickness and number of cells in an average module. Since there is a range of sizes and number of cells per module, we will attempt a weighted average. These weighted averages are based on ITRPV data, which goes back to 2010, Fraunhofer data back to 1990, and 

# In[32]:


import numpy as np
import pandas as pd
import os,sys

density_si = 2.3290 #g/cm^3 from Wikipedia of Silicon (https://en.wikipedia.org/wiki/Silicon) 
#it might be better to have mono-Si and multi-Si densities, including dopants, 
#but that density is not readily available


# A Fraunhofer report indicates that in 1990, wafers were 400 micron thick, decreasing to the more modern 180 micron thickness by 2008. ITRPVs back to 2010 indicate that 156 mm x 156mm was the standard size wafer through 2015.

# In[33]:


#weighted average for wafer size 2016 through 2030
#2016
wafer2016mcsi = (0.90*156 + 0.10*156.75)/100
wafer2016monosi = (0.55*156 + 0.45*156.75)/100
wafer2016avg = 0.9*wafer2016mcsi + 0.1*wafer2016monosi
print("Average Wafer size in 2016 was", wafer2016avg, "cm on a side")


# In[43]:


#now lets try to do this for 2019 through 2030 all at once with dataframes
#taking the average of the ranges specified in ITRPVs

#first we input the market share data for mcSi and monoSi, read in from csv
cwd = os.getcwd() #grabs current working directory
mrktshr_cellsize = pd.read_csv(cwd+"/../../CEMFC/baselines/SupportingMaterial/MarketShare_CellSize.csv", index_col='Year')
mrktshr_cellsize /=100 #turn whole numbers into decimal percentages
#print(mrktshr_cellsize)

#then split them into two dataframes for later computations
dfmarketshare_mcSi = mrktshr_cellsize.filter(regex = 'mcSi')
dfmarketshare_monoSi = mrktshr_cellsize.filter(regex = 'monoSi')
#adjust column names for matching computation later
dfmarketshare_mcSi.columns = ['share156','share156.75','share157.75','share163','share166up']
dfmarketshare_monoSi.columns = ['share156','share156.75','share157.75','share163','share166up']

print(dfmarketshare_mcSi)
print(dfmarketshare_monoSi)


# Interpolate marketshare for missing years in ITRPV 2020 predictions
# ----
# choosing to interpolate market share of different sizes rather than cell size because this should be more basedin technology - i.e. crystals only grow certain sizes. Additionally, it is more helpful to understand the impact silicon usage by keeping cell size and marketshare seperate.

# In[57]:


#interpolate for missing marketshare data
##the interpolate function returns a view of the df, doesn't modify the df itself
##therefore you have to set the old df, or a new one = the df.interpolate function
dfmarketshare_mcSi=dfmarketshare_mcSi.interpolate(method='linear',axis=0,limit=2,limit_area='inside')
dfmarketshare_monoSi=dfmarketshare_monoSi.interpolate(method='linear',axis=0,limit=2,limit_area='inside')

#fill remaining NaN/outside with 0 (i.e., no market share)
dfmarketshare_mcSi=dfmarketshare_mcSi.fillna(0.0)
dfmarketshare_monoSi=dfmarketshare_monoSi.fillna(0.0)

print(dfmarketshare_mcSi)
print(dfmarketshare_monoSi)


# In[58]:


#multiply each marketshare dataframe column by it's respective size
#dfmarketshare_mcSi.share156 *=156 #this is a slow way to multiply each column by its respective size

cellsizes = {'share156':156,
            'share156.75':156.75,
            'share157.75':157.75,
            'share163':163.875,
            'share166up':166} #dictionary of the average cell dimension for each market share bin (ITRPV 2020)

#multiply cell dimensions by their market share to get a weighted average
##this is where the column names needed to match
df_scalecell_mcSi = dfmarketshare_mcSi.mul(cellsizes,'columns')
df_scalecell_monoSi = dfmarketshare_monoSi.mul(cellsizes,'columns')

print(df_scalecell_mcSi)
print(df_scalecell_monoSi)


# In[59]:


#now add the columns together to get the weighted average cell size for each year for each technology
df_avgcell_mcSi = pd.DataFrame(df_scalecell_mcSi.agg("sum", axis="columns"))
df_avgcell_monoSi = pd.DataFrame(df_scalecell_monoSi.agg("sum", axis="columns")) #agg functions return a series not a dictionary
#print(df_avgcell_mcSi)

#join the two dataframes into single one with two columns
df_avgcell = pd.concat([df_avgcell_monoSi,df_avgcell_mcSi], axis=1) #concatinate on the columns axis
df_avgcell.columns = ['monoSi','mcSi'] #name the columns
print(df_avgcell)


# Now we have an average cell dimension for mc-Si and mono-Si for 1995 through 2030. 

# ## Marketshare Data Manipulation

# Next, we apply the marketshare of mc-Si vs mono-Si to get the average cell dimension for the year. Market share of mc-Si vs mono-Si is taken from LBNL "Tracking the Sun" report (warning: this is non-utility scale data i.e. <5MW, and is from 2002-2018), from Mints 2019 SPV report, from ITRPVs, and old papers (Costello & Rappaport 1980, Maycock 2003 & 2005).

# In[68]:


#read in a csv that was copied from CE Data google sheet
cwd = os.getcwd() #grabs current working directory
techmarketshare = pd.read_csv(cwd+"/../../CEMFC/baselines/SupportingMaterial/ModuleType_MarketShare.csv",index_col='Year')
#this file path navigates from current working directory back up 2 folders, and over to the csv
techmarketshare /=100 #turn whole numbers into decimal percentages
print(techmarketshare)


# #### create a harmonization of annual market share, and interpolate

# In[70]:


# first, create a single value of tech market share in each year or NaN
#split mcSi and monoSi
mcSi_cols = techmarketshare.filter(regex = 'mcSi')
monoSi_cols = techmarketshare.filter(regex = 'mono')
#print (mcSi_cols)

#aggregate all the columns of mono or mcSi into one averaged market share
est_mktshr_mcSi = pd.DataFrame(mcSi_cols.agg("mean", axis="columns"))
#print(est_mktshr_mcSi)
est_mktshr_monoSi = pd.DataFrame(monoSi_cols.agg("mean", axis="columns"))
#print(est_mktshr_monoSi)

#Join the monoSi and mcSi back together as a dataframe
est_mrktshrs = pd.concat([est_mktshr_monoSi,est_mktshr_mcSi], axis=1) #concatinate on the columns axis
est_mrktshrs.columns = ['monoSi','mcSi'] #name the columns


#sanity check of market share data - does it add up?
est_mrktshrs['Total'] = est_mrktshrs.monoSi+est_mrktshrs.mcSi

print(est_mrktshrs)
#Warning: 2002, 10% of the silicon marketshare was "other", including amorphous, etc.
del est_mrktshrs['Total']

#interpolate marketshares for each year


# In[71]:


#Interpolate for marketshare NaN values
est_mrktshrs['mcSi'][1980]=0.0
est_mrktshrs = est_mrktshrs.interpolate(method='linear',axis=0,limit_area='inside')

#sanity check of market share data - does it add up?
est_mrktshrs['Total'] = est_mrktshrs.monoSi+est_mrktshrs.mcSi
print(est_mrktshrs)
#Warning: 2002, 10% of the silicon marketshare was "other", including amorphous, etc.
del est_mrktshrs['Total']


# Combining Cell Size shares and Market Share Data
# ----------
# Now we have separate mono and mcSi dataframes, which contain the average cell size, based on the market share of the cell size bin as enumerated in ITRPV 2020. The next step is to combine these technology specific (mono vs mc) based on the module technology market share.

# In[83]:


#now combine technology market share of mcSi and monoSi with their respective average cell dimensions
#which have already been cell size marketshare weighted
#going to ignore "otherSi" because for the most part less than 2%, except 2002

#trim the techmarketshare data to 1995 through 2030
est_mrktshrs_sub = est_mrktshrs.loc[est_mrktshrs.index>=1995] #could also use a filter function instead

#multiply the share of each tech by the weighted average cell size
mrkt_wtd_cells = est_mrktshrs_sub.mul(df_avgcell,'columns')
#sum across monoSi and mcSi for the total market average cell size (x and y)
market_average_cell_final = pd.DataFrame(mrkt_wtd_cells.agg("sum", axis="columns"))
market_average_cell_final.columns = ['avg_cell']

#print(mrkt_wtd_cells)
print(market_average_cell_final)


# The annual average cell size should be 156 mm on a side through 2015, but due to marketshare weighting not always adding up to 100%, there are some deviations. For example, 2002 is missing 10% of the marketshare due to exclusion of amorphous silicon and other thin films. This is a direct result from averaging the marketshare data from multiple sources ( LBNL "Tracking the Sun" report (warning: this is non-utility scale data i.e. <5MW, and is from 2002-2018), from Mints 2019 SPV report, from ITRPVs, and old papers (Costello & Rappaport 1980, Maycock 2003 & 2005)).
# 
# The years subject to this marketshare averaging problem are: 

# In[86]:


est_mrktshrs['Total'] = est_mrktshrs.monoSi+est_mrktshrs.mcSi
est_mrktshrs_bad = est_mrktshrs.loc[est_mrktshrs.Total<1.0]
Bad_years = est_mrktshrs_bad.index
print(Bad_years)


# In[ ]:




