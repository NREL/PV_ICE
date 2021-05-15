#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'ElectricFutures')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[27]:


MATERIALS = ['glass','silver','silicon', 'copper','aluminium_frames']
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'..\..\PV_ICE\baselines\LiteratureProjections\EF-CapacityByState-basecase.csv'
MODULEBASELINE_High = r'..\..\PV_ICE\baselines\LiteratureProjections\EF-CapacityByState-LowREHighElec.csv'


# In[28]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# In[29]:


PV_ICE.__version__


# In[30]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[42]:


df = pd.read_csv(MODULEBASELINE)
df.set_index(['time','gid'], inplace=True)


# In[43]:


#df.set_index('time', inplace=True)
#df.index=pd.PeriodIndex(df.index, freq='A')


# In[47]:


df['time']


# In[ ]:




