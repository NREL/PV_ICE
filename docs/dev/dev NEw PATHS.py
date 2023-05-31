#!/usr/bin/env python
# coding: utf-8

# # 0 - quickStart Example

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


import PV_ICE

PV_ICE.__version__


# ### 2. Create your Simulation Object
# 
# This will create the container for all the different scenario(s) you might want to test. We are also pointing to the testfolder defined above.

# In[3]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)


# In[4]:


mainbranch = False
if mainbranch:
    r1.createScenario(name='standard', file=r'..\baselines\baseline_modules_US.csv')
    r1.scenario['standard'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')    
else:
    r1.createScenario(name='standard', file=r'..\baselines\baseline_modules_US_dev.csv')
    r1.scenario['standard'].addMaterial('glass', file=r'..\baselines\baseline_material_glass_dev.csv')


# In[5]:


r1.calculateMassFlow()


# In[6]:


r1.scenario['standard'].data.head()


# In[7]:


r1.scenario['standard'].data.tail()


# In[8]:


r1.scenario['standard'].material['glass'].materialdata.head()


# In[9]:


r1.scenario['standard'].material['glass'].materialdata.tail()


# In[10]:


if mainbranch:
    r1.scenario['standard'].data.to_csv('test_MAIN.csv')
    r1.scenario['standard'].material['glass'].materialdata.to_csv('test_MAIN_Mat.csv')
else:
    r1.scenario['standard'].data.to_csv('test_Dev.csv')
    r1.scenario['standard'].data.to_csv('test_Dev_Mat.csv')
    


# ###  6. Plot Mass Flow Results

# In[11]:


r1.plotScenariosComparison(keyword='Cumulative_Area_disposedby_Failure')
r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_EOL_Recycled_2_HQ')


# In[17]:


r1.scenario['standard'].data.keys()


# In[19]:


for key in r1.scenario['standard'].data.keys():
    try:
        r1.plotScenariosComparison(keyword=key)
    except:
        print("FAILED ON KEY : ", key)


# In[20]:


for key in r1.scenario['standard'].material['glass'].materialdata.keys():
    try:
        r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword=key)
    except:
        print("FAILED ON KEY : ", key)

