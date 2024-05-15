#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.express as px

import PV_ICE

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'MESC-NRELStdScens')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines'/'NRELStdScenarios')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
#altBaselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'Energy_CellModuleTechCompare')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("pyplot ", plt.matplotlib.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# ### Bring in NREL Standard Scenarios data for projection
# https://scenarioviewer.nrel.gov/ download the data, save it to the NRELStdScenarios folder in baselines.

# In[3]:


stdsceninput_raw = pd.read_csv(os.path.join(inputfolder, 'StdScen23_Mid_Case_NoNascent_annual_national.csv'),
           skiprows=[0,1,2,4], header=[0], index_col=1)


# In[4]:


stdscen_pv_evens = stdsceninput_raw.filter(like='(MW)').filter(like='PV')


# In[5]:


#now make previous odds = next year evens deployment
idx_temp = pd.RangeIndex(start=2024,stop=2051,step=1) #create the index
stdscens_pv_filled = stdscen_pv_evens.reindex(idx_temp, method='bfill')
stdscens_pv_filled


# In[6]:


#stdscens_pv_filled.sum(axis=1)


# ### Set up PV ICE simulation using historical US installs with the NREL Std Scenarios projection
# 

# In[7]:


MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
moduleFile = os.path.join(baselinesfolder, 'baseline_modules_mass_US_updatedT50T90.csv')


# In[9]:


sim1 = PV_ICE.Simulation(name='MESC_StdScen', path=testfolder)
scens = '23_MidCase_NoNascent'
sim1.createScenario(name=scens, massmodulefile=moduleFile) #create the scenario, name and mod file attach
for mat in MATERIALS:
    materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
    sim1.scenario[scens].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS


# In[10]:


#deployment projection for all scenarios
sim1.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', 
                    value=stdscens_pv_filled.sum(axis=1), start_year=2024) #


# In[15]:


plt.plot(sim1.scenario['23_MidCase_NoNascent'].dataIn_m.loc[:,'new_Installed_Capacity_[MW]'])


# In[17]:


sim1.calculateMassFlow()


# In[23]:


ii_yearly, ii_cumu = sim1.aggregateResults()


# In[24]:


sim1.plotMetricResults()


# In[26]:


wasteEoL = ii_yearly['WasteEOL_Module_MESC_StdScen_23_MidCase_NoNascent_[Tonnes]']
decomm = ii_yearly['DecommisionedCapacity_MESC_StdScen_23_MidCase_NoNascent_[MW]']


# In[42]:


plt.plot(wasteEoL)
plt.ylim(0,)
plt.xlim(1995,2050)
plt.title('Annual End of Life Module Waste')
plt.ylabel('EoL Module Waste [metric tonnes]')
plt.grid()


# So taking the peaks as peak demand for later years for recycling:
# - around 100k metric tonnes by 2030
# - around 300k metric tonnes by 2040
# - around 800k metric tonnes by 2050
# 
# Explain the jaggedy nature of the EoL

# In[32]:


EoLByMethod_MW = sim1.scenario['23_MidCase_NoNascent'].dataOut_m.filter(like='Yearly_Sum_Power_EOLby_')
EoLByMethod_MW.columns


# In[35]:


#plotly plot
fig = px.bar(EoLByMethod_MW, x=EoLByMethod_MW.index, y=EoLByMethod_MW.columns, barmode = 'stack')
fig.show()


# Most PV failing before 2050 is due to old installations with shorter project lifetimes. 

# In[ ]:





# In[ ]:





# In[ ]:




