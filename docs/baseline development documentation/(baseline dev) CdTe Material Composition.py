#!/usr/bin/env python
# coding: utf-8

# # CdTe Annual % Material Composition
# This journal graphs the average composition of a CdTe module over time.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
from urllib.request import urlretrieve
import glob
#import PV_ICE
cwd = os.getcwd() #grabs current working directory


# In[2]:


supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
baselinesFolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
cwd


# In[3]:


#print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("pyplot ", plt.matplotlib.__version__)
#print("PV_ICE version ", PV_ICE.__version__)


# In[4]:


#materials in CdTe
MATERIALS_CdTe = ['glass_cdte','aluminium_frames_cdte','encapsulant_cdte','copper_cdte','cadmium','tellurium']
tidynameMats_CdTe = ['glass','aluminium_frames','encapsulant','copper','cadmium','tellurium']


# In[5]:


pd.read_csv(os.path.join(baselinesFolder, 'baseline_material_mass_cadmium.csv'), 
            index_col = 0, usecols=['year','mat_massperm2'], skiprows=[1])


# In[6]:


df_component_mats = pd.DataFrame()
for mat in MATERIALS_CdTe:
    filename = os.path.join(baselinesFolder, 'baseline_material_mass_'+str(mat)+'.csv')
    tempdf = pd.read_csv(filename, index_col = 0, usecols=['year','mat_massperm2'], skiprows=[1])
    df_component_mats = pd.concat([df_component_mats,tempdf], axis=1)
    


# In[7]:


df_component_mats.columns = tidynameMats_CdTe
df_component_mats


# In[8]:


df_component_mats['module_mass_gpm2'] = df_component_mats.sum(axis=1) #run only once


# In[9]:


df_percent_mats = df_component_mats.loc[:,df_component_mats.columns !='module_mass_gpm2'].div(df_component_mats['module_mass_gpm2'], axis=0)*100


# In[21]:


plt.rcParams.update({'font.size': 14})
fig, ax = plt.subplots()
ax.stackplot(df_percent_mats.index, df_percent_mats.T)
ax.legend(df_percent_mats.columns, loc='lower left')
plt.title('Material Composition of CdTe') 
plt.ylabel('Material Composition by weight (%)') 
plt.xlim(1995,2050)
plt.ylim(75,100)

fig.savefig(os.path.join(supportMatfolder,'MaterialComp_CdTeModule.png'))
plt.show()


# In[23]:





# In[ ]:




