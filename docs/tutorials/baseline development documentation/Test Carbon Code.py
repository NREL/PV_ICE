#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (8, 4)
cwd = os.getcwd() #grabs current working directory

supportMatfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
baselinesFolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines')
carbonfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE'/ 'baselines'/ 'CarbonLayer')
testfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE'/ 'TEMP')


# In[2]:


#creating scenarios for identical power of multiple technologies
scennames = ['PV_ICE', 'test1']
MATERIALS = ['silicon'] #'glass','silver',, 'copper', 'aluminium_frames','encapsulant', 'backsheet'
moduleFile_m = os.path.join(baselinesFolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesFolder, 'baseline_modules_energy.csv')


# In[3]:


#load in a baseline and materials for modification
import PV_ICE

sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames:
    sim1.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesFolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesFolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim1.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[4]:


#sim1.modifyScenario('test1', 'mod_EOL_collection_eff', 100.0, start_year=2022) #100% collection
#sim1.scenario['test1'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022)
#sim1.trim_Years(startYear=2000, endYear=2100)
#sim1.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', value= global_projection['World_annual_[MWdc]'], start_year=2000)


# In[5]:


sim1.calculateFlows()


# In[6]:


sim1.calculateCarbonFlows()


# In[7]:


sim1.scenario['PV_ICE'].material['silicon'].matdataOut_c


# # DUMMY TEST

# In[8]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (8, 4)
cwd = os.getcwd() #grabs current working directory

supportMatfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
baselinesFolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines')
carbonfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE'/ 'PV_ICE'/ 'baselines'/ 'CarbonLayer')
testfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE'/ 'PV_ICE'/ 'TEMP')


# In[9]:


#creating scenarios for identical power of multiple technologies
scennames = ['PV_ICE', 'test1']
MATERIALS = ['silicon'] #'glass','silver',, 'copper', 'aluminium_frames','encapsulant', 'backsheet'
moduleFile_m = os.path.join(carbonfolder, 'dummy_baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(carbonfolder, 'dummy_baseline_modules_energy.csv')


# In[10]:


carbonfolder


# In[11]:


#load in a baseline and materials for modification
import PV_ICE

sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames:
    sim1.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(carbonfolder,'dummy_baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(carbonfolder,'dummy_baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim1.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[12]:


#sim1.modifyScenario('test1', 'mod_EOL_collection_eff', 100.0, start_year=2022) #100% collection
#sim1.scenario['test1'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022)
#sim1.trim_Years(startYear=2000, endYear=2100)
#sim1.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', value= global_projection['World_annual_[MWdc]'], start_year=2000)


# In[13]:


sim1.calculateFlows()


# In[14]:


sim1.calculateCarbonFlows()


# In[16]:


sim1.scenario['PV_ICE'].material['silicon'].matdataOut_c['mat_Recycled_HQ_elec_gCO2eq']


# In[ ]:


sim1.scenario['PV_ICE'].material['silicon'].matdataOut_m#['mat_L0']#.filter(like='China')#.iloc[55].values


# In[ ]:


sim1.scenario['PV_ICE'].material['silicon'].matdataIn_e#.filter(like='China').iloc[55].values


# In[ ]:


sim1.scenario['PV_ICE'].material['silicon'].matdataIn_m

