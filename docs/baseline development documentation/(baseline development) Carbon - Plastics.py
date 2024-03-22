#!/usr/bin/env python
# coding: utf-8

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


# # Encapsulant and Backsheet MFGing by country
# Most of the market report data is behind paywalls. One that isn't, but doesnt provide market share is ENF solar database of PV material Manufacturers. 

# In[32]:


enf_encapsulants = pd.read_csv(os.path.join(carbonfolder, 'input-encapsulantMFGers-ENFData.csv'),
                                     index_col=0)#, usecols=lambda x: x not in skipcols)
enf_backsheets = pd.read_csv(os.path.join(carbonfolder, 'input-backsheetMFGers-ENFData.csv'),
                                     index_col=0)#, usecols=lambda x: x not in skipcols)


# In[50]:


encaps_bycountry = enf_encapsulants.groupby(['Region']).size()
encaps_bycountry


# In[68]:


encaps_bycountry_marketshare = encaps_bycountry/encaps_bycountry.sum()*100
encaps_bycountry_marketshare
#if we want to downselect and renormalize, do the below:
#importantcountries_encap = encaps_bycountry_marketshare.loc[encaps_bycountry_marketshare>=1].index
#encaps_bycountry.loc[importantcountries_encap]


# In[ ]:





# In[64]:


backsheets_bycountry = enf_backsheets.groupby(['Region']).size()
backsheets_bycountry


# In[67]:


backsheets_bycountry/backsheets_bycountry.sum()*100


# In[ ]:




