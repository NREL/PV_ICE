#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'EnergyAnalysis'/'Sensitivity')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
altBaselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'Energy_CellModuleTechCompare')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


from platform import python_version 
print(python_version())


# In[3]:


import PV_ICE
PV_ICE.__version__


# In[4]:


MATERIAL = ['glass']#
moduleFile_m = os.path.join(baselinesfolder, 'TEST_baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'TEST_baseline_modules_energy.csv')


# In[5]:


#load in a baseline and materials for modification
sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)

sim1.createScenario(name='No_circ', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIAL)):
    matbaseline_m = os.path.join(baselinesfolder,'TEST_baseline_material_mass_'+MATERIAL[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'TEST_baseline_material_energy_'+MATERIAL[mat]+'.csv')
    sim1.scenario['No_circ'].addMaterial(MATERIAL[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[6]:


sim1.createScenario(name='circ_mfg_LQ', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIAL)):
    matbaseline_m = os.path.join(baselinesfolder,'TEST_baseline_material_mass_'+MATERIAL[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'TEST_baseline_material_energy_'+MATERIAL[mat]+'.csv')
    sim1.scenario['circ_mfg_LQ'].addMaterial(MATERIAL[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
#mod mod
#sim1.modifyScenario('MFGScrap_LQ', '',100.0, start_year=1995) #collect everything

#mat mod
sim1.scenario['circ_mfg_LQ'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled',100.0, start_year=1995) #


# In[7]:


sim1.createScenario(name='circ_mfg_HQOL', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIAL)):
    matbaseline_m = os.path.join(baselinesfolder,'TEST_baseline_material_mass_'+MATERIAL[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'TEST_baseline_material_energy_'+MATERIAL[mat]+'.csv')
    sim1.scenario['circ_mfg_HQOL'].addMaterial(MATERIAL[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
#mod mod
#sim1.modifyScenario('MFGScrap_LQ', '',100.0, start_year=1995) #collect everything

#mat mod
sim1.scenario['circ_mfg_HQOL'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled',100.0, start_year=1995) #
sim1.scenario['circ_mfg_HQOL'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ',100.0, start_year=1995) #


# In[8]:


sim1.createScenario(name='circ_mfg_HQCL', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIAL)):
    matbaseline_m = os.path.join(baselinesfolder,'TEST_baseline_material_mass_'+MATERIAL[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'TEST_baseline_material_energy_'+MATERIAL[mat]+'.csv')
    sim1.scenario['circ_mfg_HQCL'].addMaterial(MATERIAL[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
#mod mod
#sim1.modifyScenario('MFGScrap_LQ', '',100.0, start_year=1995) #collect everything

#mat mod
sim1.scenario['circ_mfg_HQCL'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled',100.0, start_year=1995) #
sim1.scenario['circ_mfg_HQCL'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ',100.0, start_year=1995) #
sim1.scenario['circ_mfg_HQCL'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG',100.0, start_year=1995) #


# In[9]:


sim1.calculateFlows()


# In[10]:


cc_yearly, cc_cumu = sim1.aggregateResults()
allenergy, energyGen, energy_demands = sim1.aggregateEnergyResults()


# In[11]:


sim1.plotMetricResults()


# In[12]:


plt.plot(cc_yearly.filter(like='VirginStock_glass'))
plt.legend(cc_yearly.filter(like='VirginStock_glass').columns)


# In[13]:


allenergy.filter(like='MFGScrap_LQ').tail(10)


# In[14]:


plt.plot(allenergy.filter(like='MFGScrap_LQ'))
plt.legend(allenergy.filter(like='MFGScrap_LQ').columns)


# In[15]:


allenergy.filter(regex='MFGScrap_HQ$').tail(10)


# In[16]:


plt.plot(allenergy.filter(regex='MFGScrap_HQ$'))
plt.legend(allenergy.filter(regex='MFGScrap_HQ$').columns)


# In[17]:


allenergy['circ_mfg_HQOL_glass_mat_MFGScrap_HQ']#-allenergy['circ_mfg_HQOL_glass_mat_MFGScrap_LQ']
#-allenergy['circ_mfg_LQ_glass_mat_MFGScrap_LQ']


# In[18]:


allenergy['circ_mfg_LQ_glass_mat_MFGScrap_LQ']


# In[19]:


allenergy['circ_mfg_HQOL_glass_mat_MFGScrap_LQ']


# In[20]:


e_annual_sumDemands = energy_demands.filter(like='demand_total')
e_annual_sumDemands_cumu = e_annual_sumDemands.cumsum()
cumu_e_demands = e_annual_sumDemands_cumu.iloc[-1]
cumu_e_demands.index= sim1.scenario.keys()

plt.bar(sim1.scenario.keys(), cumu_e_demands/cumu_e_demands['No_circ']-1)
plt.title('Cumulative Lifecycle Energy Demands')
plt.ylabel('Cumulative Energy Demands\n[TWh]')


# In[21]:


cumu_e_demands

