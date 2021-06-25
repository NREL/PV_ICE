#!/usr/bin/env python
# coding: utf-8

# # 8 - Monte Carlo Analysis (in development)
# 
# Currently using a normal distribution.
# Next steps: modify distribution to random distribution between limits, or triangular. 
#     Also, check with experts the boundaries guestimates.

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path
import numpy as np

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# ### Start PV_ICE baseline

# In[3]:


import PV_ICE


# In[4]:


MATERIAL = 'glass'
SANITYCHECK = False

if SANITYCHECK:
    MODULEBASELINE = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\tests\baseline_module_test_2.csv'
    MATERIALBASELINE = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\tests\baseline_material_test_2.csv'
else:
    MODULEBASELINE = r'..\baselines\baseline_modules_US.csv'
    MATERIALBASELINE = r'..\baselines\baseline_material_'+MATERIAL+'.csv'


# In[5]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='baseline', file=MODULEBASELINE)
r1.scenario['baseline'].addMaterial(MATERIAL, file=MATERIALBASELINE)


# ### Montecarlo Parameters

# In[6]:


avg = 1
std_dev = .1
num_reps = len(r1.scenario['baseline'].data['mod_MFG_eff'])   # So each row gets a new value
num_simulations = 500


# ### Variables that are  being MonteCarlo-ed

# In[7]:


stages_mod = ['mod_eff', 'mod_degradation', 'mod_MFG_eff', 'mod_EOL_collection_eff',
          'mod_EOL_collected_recycled']

stages_mat = ['mat_massperm2', 'mat_MFG_eff', 'mat_MFG_scrap_Recycled', 
          'mat_MFG_scrap_Recycled_into_HQ', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG',
          'mat_EOL_collected_Recycled', 'mat_EOL_Recycling_eff', 'mat_EOL_Recycled_into_HQ',
          'mat_EOL_RecycledHQ_Reused4MFG']


# ### Creating the Multiple Monte Carlo Scenarios

# In[8]:


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


# ##### Visual Check of changes

# In[9]:


r1.scenario['baseline'].data.head()


# In[10]:


r1.scenario['mod_0'].data.head()


# ### Calculate Mass Flow for all Monte Carlo Simulations 
# 
# This might take a wile depending on number. ~1.5 mississipis per simulation.

# In[11]:


r1.calculateMassFlow()


# ### Compiling Results

# In[12]:


scenarios = list(r1.scenario.keys())


# In[13]:


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


# In[14]:


stages = scenarios[1::]    # Removing the baseline

df = pd.DataFrame(list(zip(virginStock_Changes, waste_Changes)), 
               columns=['Virgin Needs Change', 'Waste Change'],index=stages) 


# In[15]:


df.hist()
plt.text(0.85, -20.5, 'Change compared to baseline [%]', ha='center');

