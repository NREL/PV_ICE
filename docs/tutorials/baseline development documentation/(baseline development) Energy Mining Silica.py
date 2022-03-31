#!/usr/bin/env python
# coding: utf-8

# # Energy Requirements of Mining Silica

# This journal creates a baseline for the energy required to mine and refine quartz or industrial silica deposits into silica sand usable for either the glass or mg-si industry. 

# In[2]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[3]:


cwd = os.getcwd() #grabs current working directory
skipcols = ['Source', 'Notes']
e_minesilica_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-miningsilica.csv",
                                     index_col='year', usecols=lambda x: x not in skipcols)


# In[4]:


plt.plot(e_minesilica_raw, marker='o')
plt.title(e_minesilica_raw.columns[0])


# The first point is from G. J. M. Phylipsen and E. A. Alsema, “Environmental life-cycle assessment of multicrystalline silicon solar cell modules,” Netherlands Agency for Energy and the Environment,NOVEM, Netherlands, Sep. 1995. and has the note that this energy is "less than 0.3% of reduction energy" for MG-Si. However, it appears to be an order of magnitude higher than the others, I don't think this is empirical, and I have the least confidence in this number. Therefore, we will drop this point.
# 
# The last two points are from S. M. Heidari and A. Anctil, “Country-specific carbon footprint and cumulative energy demand of metallurgical grade silicon production for silicon photovoltaics,” Resources, Conservation and Recycling, vol. 180, p. 106171, May 2022, doi: 10.1016/j.resconrec.2022.106171. The lower energy represents the energy required to prepare high quality silica deposits (mining and washing, small amounts of magnetic separation and floation). The higher energy requirement represents industrial or low quality silica deposits which require significant benefication. This one is a blending of 3 methods (magnetic separation, flotation, and gravity). Currently, because China is producing the majority of MG-Si and they have no high quality silca deposits, we will assume that the energy will remain at the higher point into future.
# 
# Energy values associated with the creation of silica sand were used, and other side-related processes were excluded. This can be thought of as scope 1 energy requirements.

# In[5]:


e_minesilica_tidy = e_minesilica_raw.copy()
e_minesilica_tidy.loc[e_minesilica_tidy.idxmax(),]=np.nan #find the max and set it to Nan
plt.plot(e_minesilica_tidy, marker='o')


# These data points are all good, and generally represent different locations and proceses. We will use these as optional values, rather than a time series, depending on location and quality of silica supply.

# In[6]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes']
e_minesilica_meta = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-miningsilica.csv",
                                     index_col='year')


# In[25]:


e_minesilica = e_minesilica_meta.dropna()
e_minesilica.drop([1992], inplace=True)
e_minesilica.loc[:,'Location'] = ['China', 'Croatia', 'Poland', 'USA', 'China']
e_minesilica.loc[:,'Quality'] = ['Low', 'Industrial', 'Industrial','High','Low']


# For now, we will select the Heidari and Anctil 2022 Low Quality China data point, since a majority of MG-Si and glass are coming from China.
