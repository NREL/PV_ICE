#!/usr/bin/env python
# coding: utf-8

# # Baseline Development: Energy of Tellurium
# This journal documents the calculations of extracting and refining Tellurim. Te is a 2ndary mineral typically from copper anode slimes. The anode slime is processed via electrowinning to extract the Te at low quality, then upgraded to semiconductor purity through vacuum distillation, although zone refining is also sometimes used. The manufacturing energy includes a % fuel contribution. Because Te is a secondary product of copper, e_mat_extraction will be copper mining energy, and copper extraction+refining energy will be added to the Te refining and purification energy.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt


# In[2]:


plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (10, 5)


# In[3]:


baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')


# In[4]:


cwd = os.getcwd() #grabs current working directory
print(cwd)


# ### Copper Refining Energy - Metallurgy

# In[12]:


skipcols = ['Source', 'Notes']
e_CuMetallurgy_raw = pd.read_csv(os.path.join(supportMatfolder, "output-energy-copper-metallurgy.csv"), index_col=0)
                           #, usecols=lambda x: x not in skipcols)


# In[13]:


e_CuMetallurgy_raw.head()


# ### Refine Te to ~3N

# In[5]:


skipcols = ['Source', 'Notes']
e_TeRefine_raw = pd.read_csv(os.path.join(supportMatfolder, "input-energy-CdTe-TeRefining.csv"), index_col='year')
                           #, usecols=lambda x: x not in skipcols)


# In[6]:


e_TeRefine_raw.dropna(how='all')


# In[8]:


plt.plot(e_TeRefine_raw.index, e_TeRefine_raw.iloc[:,0], marker='o')
plt.xlim(2000,2025)
plt.ylim(0,5)
plt.title(e_TeRefine_raw.columns[0])


# The 2009 data point is from a thesis that doesn't provide recovery of Te in mass (only ppm), therefore, we will drop this data point.
# 
# The others are hovering around 2 kWh/kg. Therefore, we will take the electrowinning of Te to achieve ~3N to be 2 kWh/kg.

# ### Purify Te to Semiconductor grade

# In[ ]:


e_TePurify_raw = pd.read_csv(os.path.join(supportMatfolder, "input-energy-CdTe-ZnRefining.csv"), index_col='year')
                           #, usecols=lambda x: x not in skipcols)


# In[ ]:





# In[ ]:




