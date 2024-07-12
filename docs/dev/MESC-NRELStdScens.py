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
# 
# ReEDS capacity data is cumulative, and only reports even years, so we need to data munge.

# In[3]:


stdsceninput_raw = pd.read_csv(os.path.join(inputfolder, 'StdScen23_Mid_Case_annual_national.csv'),
           skiprows=[0,1,2,4], header=[0], index_col=1)
#other scenario options:
#StdScen23_Mid_Case_NoNascent_annual_national.csv


# In[4]:


stdscen_pv_evens = stdsceninput_raw.filter(like='(MW)').filter(like='PV')


# In[5]:


#take the difference betwen even years to get annual additions from cumulative
stdscens_evens_added_cap = stdscen_pv_evens.diff()
#divide by 2 to evenly distribute across odd and even years
stdscens_added_cap = stdscens_evens_added_cap/2


# In[6]:


#now make previous odds = next year evens deployment
idx_temp = pd.RangeIndex(start=2024,stop=2051,step=1) #create the index
stdscens_added_cap_filled = stdscens_added_cap.reindex(idx_temp, method='bfill')
stdscens_added_cap_filled


# In[7]:


#Reeds is in MWac, we're in MWdc, so multiply residential by 1.1 and utility by 1.3
stdscens_pv_filled_dc = pd.DataFrame()
stdscens_pv_filled_dc['Behind-the-meter PV capacity (MWdc)'] = stdscens_added_cap_filled['Behind-the-meter PV capacity (MW)']*1.1
stdscens_pv_filled_dc['Utility-scale PV capacity (MWdc)'] = stdscens_added_cap_filled['Utility-scale PV capacity (MW)']*1.3
stdscens_pv_filled_dc


# In[8]:


plt.plot(stdscens_pv_filled_dc)
plt.legend(stdscens_pv_filled_dc.columns)
plt.ylabel('Annual Installed Capacity\n[MWdc]')


# ### Set up PV ICE simulation using historical US installs with the NREL Std Scenarios projection
# 

# In[9]:


#c-Si
MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
moduleFile = os.path.join(baselinesfolder, 'baseline_modules_mass_US_updatedT50T90.csv')
#CdTe
MATERIALS_CdTe = ['glass_cdte','aluminium_frames_cdte', 'copper_cdte', 'encapsulant_cdte','cadmium','tellurium']
moduleFile_CdTe = os.path.join(baselinesfolder, 'baseline_modules_mass_US_CdTe.csv')


# In[10]:


sim1 = PV_ICE.Simulation(name='MESC_StdScen', path=testfolder)
scens = ['23_MidCase_cSi', '23_MidCase_CdTe']

#c-Si
sim1.createScenario(name='23_MidCase_cSi', massmodulefile=moduleFile) #create the scenario, name and mod file attach
for mat in MATERIALS:
    materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
    sim1.scenario['23_MidCase_cSi'].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS
#CdTe
sim1.createScenario(name='23_MidCase_CdTe', massmodulefile=moduleFile_CdTe) #create the scenario, name and mod file attach
for mat in MATERIALS_CdTe:
    materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
    sim1.scenario['23_MidCase_CdTe'].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS_cdte


# For future deployment in the US of c-Si and CdTe, the assumptions are:
# - all Residential will be c-Si
# - CdTe will max out at 22 GW in 2030, and c-Si will make up the remaining demand to fullfill Utility deployment
# 
# We will linearly interpolate between historical CdTe Deployment and the 22 GW in 2030.

# In[11]:


plt.plot(sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[:(2024-1995),['year','new_Installed_Capacity_[MW]']])


# In[12]:


#linearly interpolate CdTe
#estimated 2024 install = 14GW
idx_temp = pd.RangeIndex(start=2024,stop=2051,step=1) #create the index
CdTeRamp = pd.DataFrame(index=idx_temp, columns=['CdTe_deploy_[MWdc]'], dtype=float)
CdTeRamp.loc[2024] = 14000
CdTeRamp.loc[2030] = 22000
CdTeRamp_full = round(CdTeRamp.interpolate(),0)
#CdTeRamp_full


# In[13]:


sim1.modifyScenario(scenarios='23_MidCase_CdTe',stage='new_Installed_Capacity_[MW]', 
                    value=CdTeRamp_full.sum(axis=1), start_year=2024) #


# In[14]:


plt.plot(sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[:,'new_Installed_Capacity_[MW]'])


# In[15]:


#now create the silicon deployment by subtracting CdTe from the total Utility deployment, add resi
mescdeploybytech = pd.DataFrame()
utilitydeploytotal = stdscens_pv_filled_dc['Utility-scale PV capacity (MWdc)'].values
CdTedeployutility = sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[(2024-1995):,'new_Installed_Capacity_[MW]'].values
resi = stdscens_pv_filled_dc['Behind-the-meter PV capacity (MWdc)'].values
mescdeploybytech['cSi_[MWdc]'] = utilitydeploytotal-CdTedeployutility+resi
mescdeploybytech.iloc[0,0]=14000 #fix nan issue
mescdeploybytech['CdTe_[MWdc]'] = sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[(2024-1995):,'new_Installed_Capacity_[MW]'].values
mescdeploybytech.index = idx_temp


# In[16]:


plt.plot(mescdeploybytech)
plt.legend(mescdeploybytech.columns)
plt.ylabel('Annual Installed Capacity\n[MWdc]')


# In[17]:


#deployment projection for all scenarios, using MWdc

sim1.modifyScenario(scenarios=['23_MidCase_cSi'],stage='new_Installed_Capacity_[MW]', 
                    value=mescdeploybytech['cSi_[MWdc]'], start_year=2024) #


# In[31]:


yeargraph = sim1.scenario['23_MidCase_cSi'].dataIn_m.loc[:,'year']
plt.plot(yeargraph,sim1.scenario['23_MidCase_cSi'].dataIn_m.loc[:,'new_Installed_Capacity_[MW]'], label='cSi')
plt.plot(yeargraph,sim1.scenario['23_MidCase_CdTe'].dataIn_m.loc[:,'new_Installed_Capacity_[MW]'], label='CdTe')
plt.legend()
plt.ylim(0,)
plt.xlim(1995,2050)


# In[ ]:





# In[ ]:


sim1.calculateMassFlow()


# In[ ]:


ii_yearly, ii_cumu = sim1.aggregateResults()


# In[ ]:


sim1.plotMetricResults()


# In[ ]:


wasteEoL = ii_yearly['WasteEOL_Module_MESC_StdScen_23_MidCase_NoNascent_[Tonnes]']
decomm = ii_yearly['DecommisionedCapacity_MESC_StdScen_23_MidCase_NoNascent_[MW]']


# In[ ]:


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

# In[ ]:


EoLByMethod_MW = sim1.scenario['23_MidCase_NoNascent'].dataOut_m.filter(like='Yearly_Sum_Power_EOLby_')
EoLByMethod_MW.columns


# In[ ]:


#plotly plot
fig = px.bar(EoLByMethod_MW, x=EoLByMethod_MW.index, y=EoLByMethod_MW.columns, barmode = 'stack')
fig.show()


# Most PV failing before 2050 is due to old installations with shorter project lifetimes. 

# In[ ]:


sim1.scenario['23_MidCase_NoNascent'].dataOut_m.keys()


# In[ ]:





# In[ ]:




