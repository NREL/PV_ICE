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


# In[ ]:


#creating scenarios for identical power of multiple technologies
scennames = ['PV_ICE', 'test1']
MATERIALS = ['silicon'] #'glass','silver',, 'copper', 'aluminium_frames','encapsulant', 'backsheet'
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[13]:


#load in a baseline and materials for modification
import PV_ICE

sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames:
    sim1.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim1.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[ ]:


#sim1.modifyScenario('test1', 'mod_EOL_collection_eff', 100.0, start_year=2022) #100% collection
#sim1.scenario['test1'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled', 100.0, start_year=2022)
#sim1.trim_Years(startYear=2000, endYear=2100)
#sim1.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', value= global_projection['World_annual_[MWdc]'], start_year=2000)


# In[ ]:


#default files
gridemissionfactors = pd.read_csv(os.path.join(carbonfolder,'baseline_electricityemissionfactors.csv'))
materialprocesscarbon = pd.read_csv(os.path.join(carbonfolder,'baseline_materials_processCO2.csv'), index_col='Material')
countrygridmixes = pd.read_csv(os.path.join(carbonfolder, 'baseline_countrygridmix.csv'))
countrymodmfg = pd.read_csv(os.path.join(carbonfolder, 'baseline_module_countrymarketshare.csv'))

countrymatmfg = pd.read_csv(os.path.join(carbonfolder, 'baseline_silicon_MFGing_countrymarketshare.csv'))


# In[ ]:


sim1.calculateFlows()


# In[ ]:


sim1.calculateCarbonFlows()

