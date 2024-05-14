#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

import PV_ICE

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'MESC-NRELStdScens')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines'/'NRELStdScenarios')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
#altBaselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'Energy_CellModuleTechCompare')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[46]:


print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("pyplot ", plt.matplotlib.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# ### Bring in NREL Standard Scenarios data for projection
# https://scenarioviewer.nrel.gov/ download the data, save it to the NRELStdScenarios folder in baselines.

# In[18]:


stdsceninput_raw = pd.read_csv(os.path.join(inputfolder, 'StdScen23_Mid_Case_NoNascent_annual_national.csv'),
           skiprows=[0,1,2,4], header=[0], index_col=1)


# In[23]:


stdscen_pv_evens = stdsceninput_raw.filter(like='(MW)').filter(like='PV')


# In[38]:


#now make previous odds = next year evens deployment
idx_temp = pd.RangeIndex(start=2024,stop=2051,step=1) #create the index
stdscens_pv_filled = stdscen_pv_evens.reindex(idx_temp, method='bfill')
stdscens_pv_filled


# In[49]:


#stdscens_pv_filled.sum(axis=1)


# ### Set up PV ICE simulation using historical US installs with the NREL Std Scenarios projection
# 

# In[ ]:


MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
moduleFile = os.path.join(baselinesfolder, 'baseline_modules_mass_US_updatedT50T90.csv')


# In[ ]:


sim1 = PV_ICE.Simulation(name='MESC_StdScen', path=testfolder)
sim1.createScenario(name=scens, massmodulefile=moduleFile) #create the scenario, name and mod file attach
for mat in MATERIALS:
    materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
    sim1.scenario[scens].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




