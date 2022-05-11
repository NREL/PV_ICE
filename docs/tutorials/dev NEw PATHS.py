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


# ### 2. Create your Simulation Object
# 
# This will create the container for all the different scenario(s) you might want to test. We are also pointing to the testfolder defined above.

# In[3]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)


# In[4]:


r1.createScenario(name='standard', file=r'..\baselines\baseline_modules_US_dev.csv')


# In[5]:


r1.scenario['standard'].addMaterial('glass', file=r'..\baselines\baseline_material_glass_dev.csv')


# In[6]:


r1.calculateMassFlow()


# In[7]:


import pandas as pd
import numpy as np


# In[8]:


PG = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                   columns=['a', 'b', 'c'])
PG


# In[9]:


df = PG.copy()
df


# In[10]:


100/(100-df['a'])


# In[11]:


PG.mul(100/(100-df['a']), axis=0)


# In[12]:


r1.scenario['standard'].data.head()


# ###  6. Plot Mass Flow Results

# In[13]:


r1.plotScenariosComparison(keyword='Cumulative_Area_disposedby_Failure')
r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_EOL_Recycled_2_HQ')

