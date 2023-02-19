#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'debug19')
baselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
#resultsfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial'/ 'USHistoryResults')


print ("Your simulation will be stored in %s" % testfolder)

modulefile = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_glass.csv')


# In[4]:


r1 = PV_ICE.Simulation(name='sim1', path=testfolder)
r1.createScenario(name='scen1', massmodulefile=modulefile) #create the scenario, name and mod file attach
r1.scenario['scen1'].addMaterial('mat1', massmatfile=materialfile) # add all materials listed in MATERIALS


# In[5]:


r1.scenario['scen1'].dataIn_m


# In[7]:


r1.trim_Years(startYear=2022, endYear=2070)


# In[9]:


r1.scenario['scen1'].dataIn_m.head(2)


# In[16]:


r1.modifyScenario('scen1','new_Installed_Capacity_[MW]', 100.0, start_year=2022) #changing module eff


# In[19]:


r1.modifyScenario('scen1','mod_eff', 100.0, start_year=2022) #changing module eff


# In[33]:


r1.modifyScenario('scen1','new_Installed_Capacity_[MW]', 0.0, start_year=2023) #changing module eff
r1.modifyScenario('scen1','mod_MerchantTail', 100.0, start_year=2022)
r1.modifyScenario('scen1','mod_degradation', 0.0, start_year=2022)


# In[34]:


r1.scenario['scen1'].dataIn_m.head(2)


# In[35]:


r1.scenMod_noCircularity() # sets all module and material circular variables to 0, creating fully linear
r1.scenMod_PerfectManufacturing() #sets all manufacturing values to 100% efficiency/yield ignoring MFG waste


# In[36]:


r1.calculateMassFlow()


# In[37]:


alives = r1.scenario['scen1'].dataOut_m['Cumulative_Active_Area']

