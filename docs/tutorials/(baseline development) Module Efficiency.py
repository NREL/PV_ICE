#!/usr/bin/env python
# coding: utf-8

# # Module Efficiency History and Projections

# In[12]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# This journal covers the development of a historical baseline and baseline future projection of average module efficiency for each installation year.

# In[28]:


cwd = os.getcwd() #grabs current working directory
mod_eff_raw = pd.read_csv(cwd+"/../../PV_DEMICE/baselines/SupportingMaterial/module_eff.csv", index_col='Year')
mod_eff_raw['mod_eff'] = pd.to_numeric(mod_eff_raw['mod_eff'])


# In[29]:


plt.plot(mod_eff_raw, marker='o')


# There appears to be an "outlier" in 2003. This is from a different source. It does however, fit within the range of module efficiency specified in the prior data point (2001, avg = 13.6, min = 12, max = 16.1). For the purposes of interpolation, we will drop this single datapoint.

# In[30]:


mod_eff_raw['mod_eff'][2003]=np.nan
plt.plot(mod_eff_raw, marker='o')


# Now interpolate for missing years. Going to break into 2 parts for this, a linear historical part, and an exponential decay out to 2050.

# In[81]:


mod_eff_early = mod_eff_raw.loc[(mod_eff_raw.index<2019)]
mod_eff_history = mod_eff_early.interpolate(method='linear',axis=0)
plt.plot(mod_eff_history)


# In[82]:


# Import curve fitting package from scipy
from scipy.optimize import curve_fit
# Function to calculate the power-law with constants a and b
def power_law(x, a, b):
    return a*np.power(x, b)


# In[83]:


#generae a dataset for the area in between
mod_eff_late = mod_eff_raw.loc[(mod_eff_raw.index>=2019)]
y_dummy = power_law(mod_eff_late.index-2018, mod_eff_late['mod_eff'][2019], 0.077) 
#played around with the exponential until y_dummy[31] closely matched projected 25.06% value.
print(y_dummy[31])
plt.plot(y_dummy)


# In[84]:


#create a dataframe of the projection
mod_eff_late['mod_eff'] = y_dummy
#print(mod_eff_late)
plt.plot(mod_eff_late)


# Now smash the two dataframes back together for our average module efficiency baseline.

# In[88]:


mod_eff = pd.concat([mod_eff_history, mod_eff_late])
mod_eff.to_csv(cwd+'/../../PV_DEMICE/baselines/SupportingMaterial/avg_module_eff_final.csv', index=True)
plt.plot(mod_eff)
plt.title('Average Module Efficiency (%)')
plt.ylabel('Efficiency (%)')

