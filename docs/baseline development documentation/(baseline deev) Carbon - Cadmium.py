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


# In[2]:


cwd = os.getcwd() #grabs current working directory
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')


# In[ ]:





# In[3]:


#skipcols = ['Source', 'Notes']
Cd_refine_location_raw = pd.read_csv(os.path.join(supportMatfolder, 'CarbonIntensities', "input-USGS-Cd-RefineryProduction.csv"),
                                     index_col=0, dtype=np.float64)
                           #, usecols=lambda x: x not in skipcols)
Cd_refine_location_raw.index = Cd_refine_location_raw.index.astype(int)
Cd_refine_location = Cd_refine_location_raw.copy()


# In[6]:


Cd_refine_location_raw['SUM'] = Cd_refine_location_raw.sum(axis=1, skipna=True)
Cd_refine_location.div(Cd_refine_location_raw['SUM'], axis=0)


# In[ ]:




