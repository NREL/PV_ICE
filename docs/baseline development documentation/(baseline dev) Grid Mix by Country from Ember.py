#!/usr/bin/env python
# coding: utf-8

# # Import and update Grid electricity mix by country Automatically
# This journal points at Ember grid electricity data, pulls the file, parses it for the countrywise grid mix percentages. These are then saved into the carbon baseline_countrygridmix.csv and used for the carbon calculations in PV ICE.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
from urllib.request import urlretrieve
#import PV_ICE
cwd = os.getcwd() #grabs current working directory


# In[2]:


supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
baselinesFolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
cwd


# In[3]:


#print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("pyplot ", plt.matplotlib.__version__)
#print("PV_ICE version ", PV_ICE.__version__)


# In[4]:


url = 'https://ember-climate.org/app/uploads/2022/07/yearly_full_release_long_format.csv'


# In[5]:


storage_options = {'User-Agent': 'Mozilla/5.0'}
emberdata_raw = pd.read_csv(url, storage_options=storage_options)

emberdata_raw.head()


# In[6]:


#down select for only columsn of interest
emberdata = emberdata_raw.filter(items=['Area','Year','Variable','Unit','Value'])

#downselect for only variables of interest (that don't overlap/double count)
Variables = ['Bioenergy','Coal','Gas','Hydro','Nuclear','Other Fossil','Solar','Wind']
emberdata_vars = emberdata.loc[emberdata['Variable'].isin(Variables)]

#select only the % of energy generation, % only used for energy generation (I checked)
#emberdata_vars['Unit'].unique()
Units = ['%']
emberdata_vars_perc = emberdata_vars.loc[emberdata_vars['Unit'].isin(Units)]
emberdata_vars_perc


# In[38]:


#for unique values of area, do a pivot table with year on index, variable on column, and value in thingy
emberdata_vars_perc['Area'].unique()


# In[8]:


Areas = emberdata_vars_perc['Area'].unique() #an array


# In[10]:


gridmix_bycountry_2000topresent = pd.DataFrame()
for a in range(0,len(Areas)):
    tempdf = emberdata_vars_perc.loc[emberdata_vars_perc['Area'] == Areas[a]] #select each area individually
    tempdf2 = tempdf.pivot(columns='Variable', values='Value', index='Year') #pivot table of this area
    tempdf_rename = tempdf2.add_prefix(str(Areas[a]+'_'))
    gridmix_bycountry_2000topresent = pd.concat([gridmix_bycountry_2000topresent,tempdf_rename], axis=1)

gridmix_bycountry_2000topresent


# In[30]:


#add in the 1995 to 2000 and present to 2050, ffill and bfill
indx_temp = pd.Series(range(1995,2051,1))
gridmix_bycountry_1995to2050 = gridmix_bycountry_2000topresent.reindex(indx_temp, method='nearest') #still leaving NaN if 2023 value NaN
gridmix_bycountry_1995to2050_full = gridmix_bycountry_1995to2050.fillna(method='ffill') #fix nan values throughout
gridmix_bycountry_1995to2050_full


# In[35]:


#emberdata_vars_perc['Area'].unique()
areaofinterest = 'United States'
gridmix_bycountry_1995to2050_full.filter(like=areaofinterest).plot.area()


# In[37]:


gridmix_bycountry_1995to2050_full.to_csv(os.path.join(baselinesFolder,'CarbonLayer','baseline_countrygridmix.csv'))


# In[ ]:





# In[ ]:




