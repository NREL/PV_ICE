#!/usr/bin/env python
# coding: utf-8

# # Silver per m2 Calculations

# This journal documents the calculations and assumptions for the silver baseline file used in the calculator.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)

density_Ag = 10.49 #g/cm3, source Wikipedia


# From the ITRPVs, we have grams of Ag per cell from 2009 through 2019, with projections through 2030. While the standard cell size has changed in that time frame, it appears that cell size makes less of a difference than cell type (n-type vs p-type), therefore we will use this as contiguous average data.
# Note: raw number extracted from ITRPV graphs with "webplotdigitizer"

# ### Some assumptions that will be made:
# 
# 1) n-type cells account for only 5% of the world market share and have for the last decade. While these require more silver per cell than p-type, they make up a small portion of the marketshare and will therefore be ignored.
# 
# 2) The difference in silver per cell between bifacial and monofacial cells is not significant for this calculation, and will therefore be averaged together.

# In[3]:


#read in the csv of 2009 through 2030 data for silver per cell.
cwd = os.getcwd() #grabs current working directory
itrpv_ag_gpc = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/ag_g_per_cell.csv", index_col='Year')


# In[4]:


plt.plot(itrpv_ag_gpc)


# In[ ]:




