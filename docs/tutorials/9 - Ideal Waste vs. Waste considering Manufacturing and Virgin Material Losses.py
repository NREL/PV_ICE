#!/usr/bin/env python
# coding: utf-8

# # 9 - Ideal Waste vs. Waste considering Manufacturing and Virgin Material Losses
# 
# 

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


import PV_ICE


# In[3]:


import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[13]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='standard', file=r'..\baselines\baseline_modules_US.csv')
r1.scenario['standard'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
r1.scenario['standard'].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')

# Ideal Manufacturing Scenario
r1.createScenario(name='ideal', file=r'..\baselines\baseline_modules_World.csv')
r1.scenario['ideal'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
r1.scenario['ideal'].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')

# Modify Ideal Scenario
r1.scenario['ideal'].data['mod_MFG_eff'] = 100.0
r1.scenario['ideal'].material['glass'].materialdata['mat_MFG_eff'] = 100.0
r1.scenario['ideal'].material['glass'].materialdata['mat_virgin_eff'] = 100.0
r1.scenario['ideal'].material['silicon'].materialdata['mat_MFG_eff'] = 100.0
r1.scenario['ideal'].material['silicon'].materialdata['mat_virgin_eff'] = 100.0

# Considering only waste, no circularity paths at EOL or Manufacturing.
r1.scenario['standard'].material['silicon'].materialdata['mat_MFG_scrap_Recycled'] = 0.0
r1.scenario['standard'].material['glass'].materialdata['mat_MFG_scrap_Recycled'] = 0.0
# not necessary to set mat_MFG_scrap_Recycled for ideal scenario, as the mat_MFG effis 100
r1.scenario['standard'].data['mod_EOL_collection_eff'] = 0.0
r1.scenario['ideal'].data['mod_EOL_collection_eff'] = 0.0


# In[14]:


IRENA= True
ELorRL = 'RL'
if IRENA:
    if ELorRL == 'RL':
        weibullInputParams = {'alpha': 5.3759, 'beta': 30}  # Regular-loss scenario IRENA
    if ELorRL == 'EL':
        weibullInputParams = {'alpha': 2.49, 'beta': 30}  # Regular-loss scenario IRENA
    r1.calculateMassFlow(weibullInputParams=weibullInputParams)
    title_Method = 'Irena_'+ELorRL
else:
    r1.calculateMassFlow()
    title_Method = 'PVICE'


# In[15]:


r1.scenario['standard'].material['glass'].materialdata.keys()


# In[16]:


r1.scenario['standard'].data.iloc[-1]


# In[17]:


r1.scenario['standard'].material['glass'].materialdata.iloc[-1]


# In[18]:


r1.scenario['standard'].material['glass'].materialdata.tail()


# In[ ]:





# In[19]:


cumWaste_ideal_glass = r1.scenario['ideal'].material['glass'].materialdata['mat_Total_Landfilled'].cumsum()
cumWaste_ideal_glass = cumWaste_ideal_glass/1000000  # Converting to tonnes

cumWaste_ideal_Si = r1.scenario['ideal'].material['silicon'].materialdata['mat_Total_Landfilled'].cumsum()
cumWaste_ideal_Si = cumWaste_ideal_Si/1000000  # Converting to tonnes

cumWaste_std_glass = r1.scenario['standard'].material['glass'].materialdata['mat_Total_Landfilled'].cumsum()
cumWaste_std_glass = cumWaste_std_glass/1000000  # Converting to tonnes

cumWaste_std_Si = r1.scenario['standard'].material['silicon'].materialdata['mat_Total_Landfilled'].cumsum()
cumWaste_std_Si = cumWaste_std_Si/1000000  # Converting to tonnes


# In[20]:


x = r1.scenario['standard'].data['year']

fig, (ax1, ax2) = plt.subplots(1, 2)
#fig.suptitle('Cumulative Waste', y = 0.02)

ax1.plot(x,cumWaste_std_glass, 'c',  label='Standard')
ax1.plot(x,cumWaste_ideal_glass, 'c--', label='Ideal')
ax1.set_yscale('log')
ax1.legend()
ax1.set_xlim([2020, 2050])
ax1.set_ylim([1e2, 1e9])
ax1.set_ylabel('Cumulative Waste [Metric Tonnes]', fontsize=16)
ax1.set_title('Glass')

ax2.plot(x,cumWaste_std_Si, color='k',  label='Standard')
ax2.plot(x,cumWaste_ideal_Si, 'k--', label='Ideal')
ax2.set_yscale('log')
ax2.legend()
ax2.set_xlim([2020, 2050])
ax2.set_ylim([1e2, 1e9])
ax2.set_title('Silicon')


# In[ ]:




