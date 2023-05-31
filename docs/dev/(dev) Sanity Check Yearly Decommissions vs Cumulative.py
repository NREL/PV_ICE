#!/usr/bin/env python
# coding: utf-8

# While the cumulative numbers are working okay, there is some +1 or -1 year offset in the yearly decommisions that throws the Area to Power calculation off

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


# In[2]:


modulefile = r'C:\Users\sayala\Documents\GitHub\PV_ICE\tests\baseline_modules_test_3.csv'
materialfile = r'C:\Users\sayala\Documents\GitHub\PV_ICE\tests\baseline_material_test_3.csv'


# In[3]:


PV_ICE.__version__


# In[4]:


r1 = PV_ICE.Simulation(name='sim1', path=testfolder)
r1.createScenario(name='scen1', massmodulefile=modulefile) #create the scenario, name and mod file attach
r1.scenario['scen1'].addMaterial('mat1', massmatfile=materialfile) # add all materials listed in MATERIALS


# In[5]:


r1.calculateMassFlow()


# In[6]:


r1.scenario['scen1'].dataOut_m.to_csv('dataOut_m.csv')


# In[ ]:


r1.scenario['scen1'].dataOut_m.to_csv('dataOut_m.csv')


# In[ ]:




