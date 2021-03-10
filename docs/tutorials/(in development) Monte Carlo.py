#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from pathlib import Path
import numpy as np
testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


MATERIAL = 'glass'
SANITYCHECK = False

if SANITYCHECK:
    MODULEBASELINE = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\tests\baseline_module_test_2.csv'
    MATERIALBASELINE = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\tests\baseline_material_test_2.csv'
else:
    MODULEBASELINE = r'..\baselines\baseline_modules_US.csv'
    MATERIALBASELINE = r'..\baselines\baseline_material_'+MATERIAL+'.csv'


# In[3]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd


# In[4]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[5]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='baseline', file=MODULEBASELINE)
r1.scenario['baseline'].addMaterial(MATERIAL, file=MATERIALBASELINE)


# In[6]:


r1.scenario['baseline'].data['mod_MFG_eff']


# In[ ]:





# In[ ]:





# In[14]:



avg = 1
std_dev = .1
num_reps = len(r1.scenario['baseline'].data['mod_MFG_eff'])
"""
num_simulations = 100
pct_to_target = np.random.normal(avg, std_dev, num_reps).round(2)
pct_to_target
""";


# In[15]:


stages_mod = ['mod_eff', 'mod_degradation', 'mod_MFG_eff', 'mod_EOL_collection_eff',
          'mod_EOL_collected_recycled']

stages_mat = ['mat_massperm2', 'mat_MFG_eff', 'mat_MFG_scrap_Recycled', 
          'mat_MFG_scrap_Recycled_into_HQ', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG',
          'mat_EOL_collected_Recycled', 'mat_EOL_Recycling_eff', 'mat_EOL_Recycled_into_HQ',
          'mat_EOL_RecycledHQ_Reused4MFG']


# In[16]:


num_simulations = 500

for i in range (0, num_simulations):
    simname = 'mod_'+str(i)
    r1.createScenario(name=simname, file=MODULEBASELINE)
    r1.scenario[simname].addMaterial(MATERIAL, file=MATERIALBASELINE)

    for jj in range (0, len(stages_mod)):
        r1.scenario[simname].data[stages_mod[jj]]=r1.scenario[simname].data[stages_mod[jj]]*np.random.normal(avg, std_dev, num_reps).round(2)
        r1.scenario[simname].data[stages_mod[jj]].clip(lower=0.0, upper=100.0, inplace=True)
        
    for jj in range (0, len(stages_mat)):
        r1.scenario[simname].material[MATERIAL].materialdata[stages_mat[jj]]=r1.scenario[simname].material[MATERIAL].materialdata[stages_mat[jj]]*np.random.normal(avg, std_dev, num_reps).round(2)
        r1.scenario[simname].material[MATERIAL].materialdata[stages_mat[jj]].clip(lower=0.0, upper=100.0, inplace=True)


# In[17]:


scenarios = list(r1.scenario.keys())
scenarios


# In[18]:


r1.scenario['baseline'].data.head()


# In[ ]:





# In[22]:


r1.calculateMassFlow()


# In[32]:


virginStock_Changes = []
waste_Changes = []

virgin_keyword = 'mat_Virgin_Stock'
waste_keyword = 'mat_Total_Landfilled'

virginStock_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].materialdata[virgin_keyword].sum()
waste_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].materialdata[waste_keyword].sum()

for i in range (1, len(scenarios)):
    stage_name = scenarios[i]
    virginStock_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].materialdata[virgin_keyword].sum()/virginStock_baseline_cum2050,2))
    waste_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].materialdata[waste_keyword].sum()/waste_baseline_cum2050,2))


# In[33]:


stages = scenarios[1::]


# In[34]:


df = pd.DataFrame(list(zip(virginStock_Changes, waste_Changes)), 
               columns=['Virgin Needs Change', 'Waste Change'],index=stages) 


# In[57]:


df.hist()
#plt.text(0.9, -0.2, 'Percent Change compared to baseline', ha='center');
plt.text(0.85, -20.5, 'Change compared to baseline [%]', ha='center');


# In[27]:





# In[ ]:





# In[ ]:


r"""
avg = r1.scenario['baseline'].data['mod_MFG_eff'][0]
std_dev = .1
num_reps = 100
num_simulations = 100
pct_to_target = np.random.normal(avg, std_dev, 1).round(2)
pct_to_target
""";


# In[ ]:




