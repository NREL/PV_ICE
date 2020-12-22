#!/usr/bin/env python
# coding: utf-8

# # Data Munging ReEDS output data files for input installations

# To explore different scenarios for furture installation projections of PV (or any technology), ReEDS output data can be useful in providing standard scenarios. This input data will be used in the module files input to the PVDEMICE tool. Some will be used to explore middle, low and high projections, some for the Solar Futures Report. This journal extracts the data relevant for the current status of the PVDEMICE tool from ReEDS outputs.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[2]:


import os
from pathlib import Path

reedsFile = str(Path().resolve().parent.parent.parent / 'December Core Scenarios ReEDS Outputs Solar Futures.xlsx')
testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

print ("Input file is stored in %s" % reedsFile)
print ("Your simulation will be stored in %s" % testfolder)


# In[3]:


cwd = os.getcwd() #grabs current working directory
rawdf = pd.read_excel(reedsFile,
                        sheet_name="Solar Capacity (GW)")
                        #index_col=[0,2,3]) #this casts scenario, PCA and State as levels
#now set year as an index in place
rawdf.drop(columns=['State'], inplace=True)
rawdf.set_index(['scenario','year','PCA'], inplace=True)


# In[4]:


rawdf.index.get_level_values('scenario').unique()


# In[5]:


scenarios = list(rawdf.index.get_level_values('scenario').unique())
PCAs = list(rawdf.index.get_level_values('PCA').unique())
scenarios


# In[ ]:





# In[6]:


import PV_ICE
r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='US', file=r'..\baselines\baseline_modules_US.csv')
baseline = r1.scenario['US'].data
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]'])
baseline.set_index('year', inplace=True)
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual


# In[ ]:





# In[ ]:


for ii in range (len(rawdf.unstack(level=1))):
    PCA = rawdf.unstack(level=1).iloc[ii].name[1]
    SCEN = rawdf.unstack(level=1).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = SCEN+'_'+PCA +'.csv'
    filetitle = os.path.join(testfolder, filetitle)
    A = rawdf.unstack(level=1).iloc[0]
    A = A.droplevel(level=0)
    A.name = 'new_Installed_Capacity_[MW]'
    A = pd.DataFrame(A)
    A.index=pd.PeriodIndex(A.index, freq='A')
    A = A.resample('Y').asfreq()
    A = A['new_Installed_Capacity_[MW]'].fillna(0).groupby(A['new_Installed_Capacity_[MW]'].notna().cumsum()).transform('mean')    
    A = pd.DataFrame(A)

    # Add other columns
    A = pd.concat([A, baseline.reindex(A.index)], axis=1)

    header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,"    "mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,"    "mod_Repowering,mod_Repairing\n"    "year,MW,%,years,years,%,years,%,%,%,%,%\n"

    with open(filetitle, 'w', newline='') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
        for line in header:
            ict.write(line)

        #    savedata.to_csv(ict, index=False)
        A.to_csv(ict, header=False)


# In[7]:


# EXAMPLE FOR JUST ONE 
ii = 0
PCA = rawdf.unstack(level=1).iloc[ii].name[1]
SCEN = rawdf.unstack(level=1).iloc[ii].name[0]
SCEN=SCEN.replace('+', '_')
filetitle = SCEN+'_'+PCA +'.csv'
filetitle = os.path.join(testfolder, filetitle)
A = rawdf.unstack(level=1).iloc[0]
A = A.droplevel(level=0)
A.name = 'new_Installed_Capacity_[MW]'
A = pd.DataFrame(A)
A.index=pd.PeriodIndex(A.index, freq='A')
B = A.resample('Y').asfreq()
B = B['new_Installed_Capacity_[MW]'].fillna(0).groupby(B['new_Installed_Capacity_[MW]'].notna().cumsum()).transform('mean')
B = pd.DataFrame(B)
B.to_csv(filetitle)

# Add other columns
B = pd.concat([B, baseline.reindex(B.index)], axis=1)


header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,""mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,""mod_Repowering,mod_Repairing\n""year,MW,%,years,years,%,years,%,%,%,%,%\n"

with open(filetitle, 'w', newline='') as ict:
# Write the header lines, including the index variable for
# the last one if you're letting Pandas produce that for you.
# (see above).
    for line in header:
        ict.write(line)

    #    savedata.to_csv(ict, index=False)
    B.to_csv(ict, header=False)


# In[8]:


## Reading inputs adn creating scenarios


# In[9]:


GISfile = str(Path().resolve().parent.parent.parent / 'gis_centroid_n.xlsx')
GIS = pd.read_excel(GISfile)
GIS = GIS.set_index('id')


# In[10]:


GIS.head()


# In[11]:


GIS.loc['p1'].long


# In[12]:


simulationname = scenarios[0]
simulationname
PCA = PCAs[0]


# In[18]:


PCA


# In[24]:


for ii in range (0, 1): #len(scenarios):
    r1 = PV_ICE.Simulation(name=scenarios[ii], path=testfolder)
    for jj in range (0, 2): #len(PCAs)): 
        r1.createScenario(name=PCAs[jj], file=r'..\baselines\baseline_modules_US.csv')
        r1.scenario[PCAs[jj]].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
        r1.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
        r1.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long


# In[ ]:





# In[ ]:





# In[ ]:





# In[16]:





# In[ ]:





# ## Playing with Multiindex Stuff

# In[ ]:


rawdf.unstack(level=0).head()
rawdf.unstack(level=1).head()
rawdf.unstack(level=2).head()


# In[ ]:


rawdf.unstack(level=1).iloc[0]


# In[ ]:


rawdf.unstack(level=1).iloc[2].name[1]


# In[ ]:


rawdf.loc[('Reference.Mod',2010)].head()


# In[ ]:


scenarios = rawdf.groupby(level=0)
PCA = rawdf.groupby(level=2)


# In[ ]:


for a,b in scenarios:
    for c,d in PCA:
        print(a, c)


# In[ ]:


PCAs = rawdf.index.get_level_values('PCA').unique()
scenarios = rawdf.index.get_level_values('scenario').unique()
years = rawdf.index.get_level_values('year').unique()


# In[ ]:


rawdf.loc[(scenarios[1])].head()


# In[ ]:


rawdf.loc[scenarios[1]].head()


# In[ ]:


rawdf.loc[[scenarios[1]]].head()


# In[ ]:




