#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
resultsfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial'/ 'USHistoryResults')

cwd=os.getcwd()
print(os.getcwd())


# In[2]:


PV_ICE.__version__


# In[3]:


MATERIALS = ['glass']#,'aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
moduleFile = os.path.join(baselinesfolder, 'TEST_baseline_modules_mass_US.csv')
#newmodfilesPAth = os.path.join(supportMatfolder,'Calculations-Installs-Subset-CommUtility.xlsx')


# In[4]:


r1 = PV_ICE.Simulation(name='sim1', path=testfolder)
r1.createScenario(name='test', massmodulefile=moduleFile) #create the scenario, name and mod file attach
for mat in MATERIALS:
    materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
    r1.scenario['test'].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS


# In[5]:


r1.calculateMassFlow()


# In[6]:


usyearlyr1, uscumr1 = r1.aggregateResults()


# In[7]:


r1.scenario['test'].dataOut_m.keys()


# In[8]:


'Yearly_Sum_Power_EOLby_Degradation',
'Yearly_Sum_Power_EOLby_Failure',
'Yearly_Sum_Power_EOLby_ProjectLifetime',
'Yearly_Sum_Power_PathsBad',
'Yearly_Sum_Power_PathsGood',
'Yearly_Sum_Power_atEOL'


# In[9]:


yspeol_deg = r1.scenario['test'].dataOut_m['Yearly_Sum_Power_EOLby_Degradation']


# In[10]:


yspeol_fail =r1.scenario['test'].dataOut_m['Yearly_Sum_Power_EOLby_Failure']


# In[11]:


yspeol_plife =r1.scenario['test'].dataOut_m['Yearly_Sum_Power_EOLby_ProjectLifetime']


# In[12]:


yspeol_sum =r1.scenario['test'].dataOut_m['Yearly_Sum_Power_atEOL']


# In[13]:


plt.plot(yspeol_deg, label='deg')
plt.plot(yspeol_fail, label='fail')
plt.plot(yspeol_plife, label='life')
plt.plot(yspeol_sum, ls=':', label='sum')
plt.legend()


# In[14]:


yspeol = pd.concat([yspeol_deg,yspeol_fail,yspeol_plife,yspeol_sum],axis=1)
yspeol


# In[15]:


yspeol_MW = yspeol/1000000#), index = usyearlyr1.index)
yspeol_MW_cumu = yspeol_MW.cumsum()
yspeol_MW_cumu.index = usyearlyr1.index
#yspeol_MW_cumu
decomm_cap = usyearlyr1.filter(like='Decomm')
compare_decom = pd.concat([yspeol_MW_cumu,decomm_cap],axis=1)
compare_decom.tail()


# In[16]:


plt.plot(compare_decom)


# In[17]:


decomm_cap.diff()


# In[18]:


plt.plot(usyearlyr1.filter(like='Waste'))
plt.legend(usyearlyr1.filter(like='Waste').keys())


# In[19]:


usyearlyr1.filter(like='Waste')


# In[ ]:




