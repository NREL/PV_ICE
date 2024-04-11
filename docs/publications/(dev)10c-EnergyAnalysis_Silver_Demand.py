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

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'EnergyAnalysis')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
altBaselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'Energy_CellModuleTechCompare')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


print(cwd)


# In[3]:


#print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("pyplot ", plt.matplotlib.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# In[4]:


plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.figsize'] = (8, 6)


# This journal pulls out the silver demand projections for the 3 projected technologies, PERC, TOPCon, SHJ, as projected for the Energy Analysis paper (10a). We also do a literature comparison, since this is a highly studied space.
# 
# We pull in the output dataframes from journal 10a and do graphing here.

# In[5]:


cc_13scen_yearly_dataOut = pd.read_csv(os.path.join(inputfolder, 'EnergyAnalysis','Deploy_MirletzLinear','cc_13scen_yearly.csv'),
           index_col = 0)


# In[6]:


silver_annual_demand = cc_13scen_yearly_dataOut.filter(like='VirginStock_silver') #tonnes
silver_annual_demand_pvice = silver_annual_demand.filter(like='PV_ICE')
silver_annual_demand_perc = silver_annual_demand.filter(like='r_PERC')
silver_annual_demand_topcon = silver_annual_demand.filter(like='r_TOPCon')
silver_annual_demand_shj = silver_annual_demand.filter(like='r_SHJ')


# In[7]:


plt.plot(silver_annual_demand_pvice, color='black', label='Baseline')
plt.plot(silver_annual_demand_perc, color = 'tab:blue', label='PERC')
plt.plot(silver_annual_demand_topcon, color='tab:orange', label='TOPCon')
plt.plot(silver_annual_demand_shj, color='tab:red', label='SHJ')
plt.ylim(0,)
plt.xlim(2000,2100)
plt.ylabel('Virgin Material Demand for Silver\n[Metric Tonnes]')
plt.legend()


# In[8]:


plt.bar(silver_annual_demand_shj.index, silver_annual_demand_shj.iloc[:2051,0], color='tab:red', label='SHJ')
plt.bar(silver_annual_demand_topcon.index, silver_annual_demand_topcon.iloc[:2051,0], color='tab:orange', label='TOPCon')
plt.bar(silver_annual_demand_pvice.index, silver_annual_demand_pvice.iloc[:2051,0], color='black', label='Baseline')
plt.bar(silver_annual_demand_perc.index, silver_annual_demand_perc.iloc[:2051,0], color='tab:blue', label='PERC')
plt.ylim(0,)
plt.xlim(2000,2050)
plt.ylabel('Virgin Material Demand for Silver\n[Metric Tonnes]')
plt.legend()
plt.title('Silver Demand by Technology to Achieve 75 TW')


# ## Add in Historical Silver Demand and Other Literature projections for Comparison

# In[9]:


ag_WSS = pd.read_csv(os.path.join(supportMatfolder, 'WorldSilverSurvey-AgProduction-PVuse.csv'), index_col=0)
ag_WSS.head()


# In[10]:


ag_WSS_flatforward = ag_WSS.interpolate()


# In[12]:


plt.bar(silver_annual_demand_shj.index, silver_annual_demand_shj.iloc[:2051,0], color='tab:red', label='SHJ')
plt.bar(silver_annual_demand_topcon.index, silver_annual_demand_topcon.iloc[:2051,0], color='tab:orange', label='TOPCon')
plt.bar(silver_annual_demand_pvice.index, silver_annual_demand_pvice.iloc[:2051,0], color='black', label='Baseline')
plt.bar(silver_annual_demand_perc.index, silver_annual_demand_perc.iloc[:2051,0], color='tab:blue', label='PERC')

plt.plot(ag_WSS.index, ag_WSS['PV Silver Demand [metric tonnes]'], color='black', label='Historical PV Silver Demand')
plt.plot(ag_WSS.index, ag_WSS['Silver Production [metric tonnes]'], color='gray', ls='--', label='Historical Mining production')
plt.plot(ag_WSS_flatforward.loc[2023:,'Silver Production [metric tonnes]'], color='red', ls='--', label='Constant Current Mining')
plt.plot(ag_WSS.index, ag_WSS['Total Supply [metric tonnes]'], color='gray', ls='-.', label='Historical Total Supply')
plt.plot(ag_WSS_flatforward.loc[2023:,'Total Supply [metric tonnes]'], color='purple', ls='-.', label='Constant Total Supply')

#plt.grid(axis='y', color='0.9', ls='--', zorder=0)
#plt.set_axisbelow(True)
plt.legend(fontsize=12)
plt.ylim(0,)
plt.xlim(2005,2050)
plt.ylabel('Virgin Material Demand for Silver\n[Metric Tonnes]')
plt.title('Silver Demand by Technology to Achieve 75 TW')


# In[13]:


pd.read_csv(os.path.join(supportMatfolder, 'Ag_Literature_Compare.csv'))


# ### Energy Compare of these techs

# In[ ]:





# In[ ]:




