#!/usr/bin/env python
# coding: utf-8

# # (baseline development) Silicon per M2 Calculations

# This journal documents the methods and assumptions made to create a baseline material file for silicon.

# ## Mass per M2

# The mass of silicon contained in a PV module is dependent on the size, thickness and number of cells in an average module. Since there is a range of sizes and number of cells per module, we will attempt a weighted average. These weighted averages are based on ITRPV data, which goes back to 2010, Fraunhofer data back to 1990, and 

# In[69]:


import numpy as np
import pandas as pd
import os,sys

density_si = 2.3290 #g/cm^3 from Wikipedia of Silicon (https://en.wikipedia.org/wiki/Silicon) 
#it might be better to have mono-Si and multi-Si densities, including dopants, 
#but that density is not readily available


# A Fraunhofer report indicates that in 1990, wafers were 400 micron thick, decreasing to the more modern 180 micron thickness by 2008. ITRPVs back to 2010 indicate that 156 mm x 156mm was the standard size wafer through 2015.

# In[70]:


#weighted average for wafer size 2016 through 2030
#2016
wafer2016mcsi = (0.90*156 + 0.10*156.75)/100
wafer2016monosi = (0.55*156 + 0.45*156.75)/100
wafer2016avg = 0.9*wafer2016mcsi + 0.1*wafer2016monosi
print("Average Wafer size in 2016 was", wafer2016avg, "cm on a side")


# In[71]:


#now lets try to do this for 2019 through 2030 all at once with dataframes
#taking the average of the ranges specified in ITRPVs

#first we input the market share data for mcSi and monoSi
marketshare_mcSi = {'share156':[0.9,0.37,0.1,0,0,0,0,0,0],
                   'share156.75':[0.1,0.63,0.9,0.7,0.3,0.08,0.03,0.01,0],
                   'share157.75':[0,0,0,0.24,0.35,0.30,0.15,0.04,0.05],
                   'share163':[0,0,0.02,0.04,0.2,0.32,0.32,0.3,0.2],
                   'share166up':[0,0,0,0.02,0.15,0.3,0.4,0.65,0.75]}
marketshare_monoSi = {'share156':[0.55,0.21,0.08,0,0,0,0,0,0],
                   'share156.75':[0.45,0.78,0.9,0.68,0.35,0.15,0,0,0],
                   'share157.75':[0,0,0,0.23,0.3,0.3,0.15,0.05,0.01],
                   'share163':[0,0.01,0.02,0.07,0.14,0.18,0.15,0.08,0.06],
                   'share166up':[0,0,0,0.02,0.21,0.37,0.7,0.87,0.93]}
#then shove them into panda dataframes
dfmarketshare_mcSi = pd.DataFrame(marketshare_mcSi, index = ['2016','2017','2018','2019','2020','2022','2024','2027','2030'])
dfmarketshare_monoSi = pd.DataFrame(marketshare_monoSi, index = ['2016','2017','2018','2019','2020','2022','2024','2027','2030'])
    #it is necessary to put the year as the row index 
    #because otherwise it gets added in the aggregation of columns
    #later when we obtain the average cell size
print(dfmarketshare_mcSi)
print(dfmarketshare_monoSi)
#columns = dfmarketshare_monoSi.columns
#print(columns)


# In[72]:


#multiply each marketshare dataframe column by it's respective size
#dfmarketshare_mcSi.share156 *=156 #this is a manual way to multiply each column by its respective size

cellsizes = {'share156':156,
            'share156.75':156.75,
            'share157.75':157.75,
            'share163':163,
            'share166up':166} #dictionary of the average cell dimension for each market share option

#multiply cell dimensions by their market share to get a weighted average
df_scalecell_mcSi = dfmarketshare_mcSi.mul(cellsizes,'columns')
df_scalecell_monoSi = dfmarketshare_monoSi.mul(cellsizes,'columns')

print(df_scalecell_mcSi)
print(df_scalecell_monoSi)


# In[80]:


#now add the columns together to get the weighted average cell size for each year for each technology
df_avgcell_mcSi = pd.DataFrame(df_scalecell_mcSi.agg("sum", axis="columns"))
df_avgcell_monoSi = pd.DataFrame(df_scalecell_monoSi.agg("sum", axis="columns")) #agg functions return a series not a dictionary
#print(df_avgcell_mcSi)

#join the two dataframes into single one with two columns
df_avgcell = pd.concat([df_avgcell_monoSi,df_avgcell_mcSi], axis=1)
df_avgcell.columns = ['monoSi','mcSi']
print(df_avgcell)
type(df_avgcell.monoSi)


# Now we have an average cell dimension for mc-Si and mono-Si for 2016 through 2030. Next, we apply the marketshare of mc-Si vs mono-Si to get the average cell dimension for the year. Market share of mc-Si vs mono-Si is taken from LBNL "Tracking the Sun" report (warning: this is non-utility scale data i.e. <5MW, and is from 2002-2018).

# In[74]:


#read in a csv that was copied from CE Data google sheet
cwd = os.getcwd() #grabs current working directory
techmarketshare = pd.read_csv(cwd+"/../../CEMFC/baselines/SupportingMaterial/ModuleType_MarketShare_LBNL.csv")
#this file path navigates from current working directory back up 2 folders, and over to the csv
techmarketshare.index = techmarketshare['Year'] #make the year column the row index
del techmarketshare['Year'] #delete the year column
techmarketshare /=100 #turn whole numbers into decimal percentages
print(techmarketshare)


# In[90]:


#now combine technology market share of mcSi and monoSi with their respective cell dimensions
#which have already been marketshare weighted
#going to ignore "otherSi" because for the most part less than 2%

#join the mcSi together and the monoSi together in separate dataframes
monoSicell = pd.DataFrame(df_avgcell.monoSi)
monoSimarket = pd.DataFrame(techmarketshare.monoSi)
df_monoSi = monoSimarket.join(monoSicell, lsuffix='share',rsuffix='size') #join is not the right command
print(df_monoSi)


# In[ ]:





# In[ ]:




