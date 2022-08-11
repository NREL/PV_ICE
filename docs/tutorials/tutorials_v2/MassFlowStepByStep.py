#!/usr/bin/env python
# coding: utf-8

# # Following mass flow calculations

# ### Project  setup 

# In[1]:


import os, sys
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
    
dfindex = pd.RangeIndex(0,56,1)


# In[2]:


testfolder = str(Path().resolve() / 'TEMP') # Path to the simulation folder.

baselinefolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines')  # Path to baselines and data.

print ("Your simulation will be stored in %s" % testfolder)
print ("Your baselines are stored in %s" % baselinefolder)


# In[3]:


r0 = PV_ICE.Simulation(name='Simulation_0', path=testfolder) #If no path if given, the default is the current folder, if no name: then the current date is given
r0.createScenario(name='Scenario_test_1', file=baselinefolder + '/baseline_modules_US.csv') # With no path given, a window opens up but after selecting, nothing happens :D
r0.scenario['Scenario_test_1'].addMaterial('glass', file=baselinefolder + '/baseline_material_glass.csv')
r0.scenario['Scenario_test_1'].addMaterial('silicon', file=baselinefolder + '/baseline_material_silicon.csv')


# r3.createScenario(name='Repair_0', file=baselinefolder + '/baseline_modules_US.csv')
# r3.scenario['Repair_0'].addMaterial('glass', file=baselinefolder + '/baseline_material_glass.csv')
# r3.scenario['Repair_0'].addMaterial('silicon', file=baselinefolder + '/baseline_material_silicon.csv')

# r3.createScenario(name='Repair_50', file=baselinefolder + '/baseline_modules_US.csv')
# r3.scenario['Repair_50'].addMaterial('glass', file=baselinefolder + '/baseline_material_glass.csv')
# r3.scenario['Repair_50'].addMaterial('silicon', file=baselinefolder + '/baseline_material_silicon.csv')


# ### Mass Flow Calculation

# In[4]:


df = r0.scenario['Scenario_test_1'].data  # The dataframe created is just the baseline implemented with a pointer to the materials dataframes


# In[5]:


df.shape


# In[6]:


mat_df = r0.scenario['Scenario_test_1'].material['glass'].materialdata # This is how I can access the material dataframe


# In[7]:


print(df.shape)
print(mat_df.shape)


# 1) `calculateMassFlow` iterates over the scenarios  `df = self.scenario[scen].data`
# 2) Check the `bifacialityfactors` (if any!) you pass it as a string for each studied year:
#     - if passed, `irradiance_stc` is calculated: `1000.0 + bf['bifi']*100.0 # W/m^2 (min. Bifacial STC Increase)`
#     - if not, `irradiance_stc` is set to 1000.00 W/m<sup>2</sup> like in the present case:

# In[8]:


df['irradiance_stc'] = 1000.0 # We add one column!!
df.shape


# Line 394 is confusing for me, but it does not seem to be working—thus, we do not care :D.
# We then add another column where we pass `'new_Installed_Capacity_[MW]` to [W]:

# In[9]:


df['new_Installed_Capacity_[W]'] = df['new_Installed_Capacity_[MW]']*1e6
df.shape


# Now it checks if `reducecapacity` is `True` or `False`, by default is `True`.

# In[10]:


df['Area'] = df['new_Installed_Capacity_[W]']/(df['mod_eff']*0.01)/df['irradiance_stc'] # m^2
df.shape


# If `reducecapacity = False` it runs: `df['Area'] = df['new_Installed_Capacity_[W]']/(df['mod_eff']*0.01)/1000.0 # m^2
# `

# In[11]:


df['Area'] = df['Area'].fillna(0) # Change NA for 0 (if any!) I counted, there are no NAs df['Area'].isnull().sum()


# Calculating waste by generation by year, and cumulative waste by year. Initialize lists:

# In[12]:


Generation_Disposed_byYear = []
Matrix_Landfilled_noncollected = []
Matrix_area_bad_status = []
Matrix_Failures = []
            # Generation_Active_byYear= [] Not being used at the moment, commenting out.
            # Generation_Power_byYear = [] Not being used at the moment, commenting out.
weibullParamList = []


# Now, the program iterated over the rows: `or generation, row in df.iterrows():`. Within the loop, the following happens:

# 1) Check for Weibull parameters.

# In[ ]:


if weibullInputParams:
weibullIParams = weibullInputParams
elif 'weibull_alpha' in row:
# "Weibull Input Params passed internally as a column"
weibullIParams = {'alpha': row['weibull_alpha'], 'beta': row['weibull_beta']}
else:
# "Calculating Weibull Params from Modules t50 and T90"
t50, t90 = row['t50'], row['t90']
weibullIParams = weibull_params({t50: 0.50, t90: 0.90})


# In[ ]:





# In[ ]:


df['weibull_alpha']


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# For Silvana:

# In[ ]:


for i in range (0, 56):
    print('\'EOL_L0_Year_' + str(i) + '\': {\'unit\': \'m$^2$\', \'source\': \'generated\'},');
    
for i in range (0, 56):
    print('\'EOL_PG_Year_' + str(i) + '\': {\'unit\': \'m$^2$\', \'source\': \'generated\'},');
    
for i in range (0, 56):
    print('\'EOL_BS_Year_' + str(i) + '\': {\'unit\': \'m$^2$\', \'source\': \'generated\'},');
    


# In[ ]:




