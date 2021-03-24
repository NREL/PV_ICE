#!/usr/bin/env python
# coding: utf-8

# # 6 - Sensitivity Analysis

# In[69]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[70]:


MATERIAL = 'glass'
SANITYCHECK = False

if SANITYCHECK:
    MODULEBASELINE = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\tests\baseline_module_test_2.csv'
    MATERIALBASELINE = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\tests\baseline_material_test_2.csv'
else:
    MODULEBASELINE = r'..\baselines\baseline_modules_US.csv'
    MATERIALBASELINE = r'..\baselines\baseline_material_'+MATERIAL+'.csv'


# In[71]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd


# In[72]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[73]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='baseline', file=MODULEBASELINE)
r1.scenario['baseline'].addMaterial(MATERIAL, file=MATERIALBASELINE)


# # Goal; Compare Virgin Material Extraction , and Waste. 

# ## MATERIAL BASELINES

# ### mat_virgin_eff | Virgin Material Efficiency

# In[74]:


# Material baseline mod.
stage = 'mat_virgin_eff'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage


r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_massperm2
# 

# In[75]:


# Material baseline mod.
stage = 'mat_massperm2'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_MFG_eff      |      Material Manfuacturing Efficiency 

# In[76]:


# Material baseline mod.
stage = 'mat_MFG_eff'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_MFG_scrap_Recycled

# In[77]:


# Material baseline mod.
stage = 'mat_MFG_scrap_Recycled'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_MFG_scrap_Recycling_eff

# In[78]:


# Material baseline mod.
stage = 'mat_MFG_scrap_Recycling_eff'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_MFG_scrap_Recycled_into_HQ

# In[79]:


# Material baseline mod.
stage = 'mat_MFG_scrap_Recycling_eff'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_MFG_scrap_Recycled_into_HQ_Reused4MFG

# In[80]:


# Material baseline mod.
stage = 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_MFG_Scrap_Overall_Improvement | OVERALL SCRAP Improvement
# 
# mat_MFG_Scrap_Overall_Improvement includes:
# 
#     mat_MFG_scrap_Recycled
#     mat_MFG_scrap_Recycling_eff
#     mat_MFG_scrap_Recycled_into_HQ
#     mat_MFG_scrap_Recycled_into_HQ_Reused4MFG
# 

# In[81]:


# Material baseline mod.
stage = 'mat_MFG_Scrap_Overall_Improvement'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)

stages = ['mat_MFG_scrap_Recycled','mat_MFG_scrap_Recycling_eff',
          'mat_MFG_scrap_Recycled_into_HQ', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG']


for i in range(0, len(stages)):
    stage = stages[i]
    r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                                 stage=stage, improvement=modhigh, start_year=0)

    r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                                 stage=stage, improvement=modlow, start_year=0)


# ### mat_EOL_collected_Recycled
# 

# In[82]:


# Material baseline mod.
stage = 'mat_EOL_collected_Recycled'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_EOL_Recycling_eff
# 

# In[83]:


# Material baseline mod.
stage = 'mat_EOL_Recycling_eff'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_EOL_Recycled_into_HQ
# 

# In[84]:


# Material baseline mod.
stage = 'mat_EOL_Recycled_into_HQ'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_EOL_RecycledHQ_Reused4MFG
# 

# In[85]:


# Material baseline mod.
stage = 'mat_EOL_RecycledHQ_Reused4MFG'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mat_EOL_Recycling_Overall_Improvement | OVERALL Recycling Improvement
# 
# Includes:
# 
#     mat_EOL_collected_Recycled
#     mat_EOL_Recycling_eff
#     mat_EOL_Recycled_into_HQ
#     mat_EOL_RecycledHQ_Reused4MFG
# 

# In[86]:


# Material baseline mod.
stage = 'mat_EOL_Recycling_Overall_Improvement'
modhigh = 1.10 
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)

stages = ['mat_EOL_collected_Recycled', 'mat_EOL_Recycling_eff',
        'mat_EOL_Recycled_into_HQ', 'mat_EOL_RecycledHQ_Reused4MFG']

for i in range(0, len(stages)):
    stage = stages[i]
    r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                                 stage=stage, improvement=modhigh, start_year=0)

    r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                                 stage=stage, improvement=modlow, start_year=0)


# # Module baseline mod.
# 
# 

# ### new_Installed_Capacity_[MW]
# 

# In[87]:


# Module baseline mod.
stage = 'new_Installed_Capacity_[MW]'
modhigh = 1.05 
modlow = 0.95
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage


r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].data, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mod_eff
# 

# In[88]:


# Module baseline mod.
stage = 'mod_eff'
modhigh = 1.05 
modlow = 0.95
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage


r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].data, 
                             stage=stage, improvement=modlow, start_year=0)


# ## reliability
# 
# Includes:
#     
#     mod_reliability_t50 
#     mod_reliability_t90 
#     mod_lifetime
# 
# 

# In[89]:


# Module baseline mod.
stage = 'reliability'
modhigh = 1.10
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)

stages = ['mod_reliability_t50', 'mod_reliability_t90', 'mod_lifetime']

for i in range(0, len(stages)):
    stage = stages[i]
    r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                                 stage=stage, improvement=modhigh, start_year=0)
    r1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].data, 
                                 stage=stage, improvement=modlow, start_year=0)


# ### mod_MFG_eff

# In[90]:


# Module baseline mod.
stage = 'mod_MFG_eff'
modhigh = 1.10
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage


r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].data, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mod_EOL_collection_eff
# 

# In[91]:


# Module baseline mod.
stage = 'mod_EOL_collection_eff'
modhigh = 1.10
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage


r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].data, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mod_EOL_collected_recycled
# 

# In[92]:


# Module baseline mod.
stage = 'mod_EOL_collected_recycled'
modhigh = 1.10
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage


r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].data, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mod_Repowering
# 

# In[93]:


# Module baseline mod.
stage = 'mod_Repowering'
modhigh = 1.10
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage


r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].data, 
                             stage=stage, improvement=modlow, start_year=0)


# ### mod_Repairing
# 

# In[94]:


# Module baseline mod.
stage = 'mod_Repairing'
modhigh = 1.10
modlow = 0.90
stage_highname = 'HighEff_'+stage
stage_lowname = 'LowEff'+stage


r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                             stage=stage, improvement=modhigh, start_year=0)

r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].data, 
                             stage=stage, improvement=modlow, start_year=0)


# ## Improving All EOL CE Pathways
# 
# Includes
# 
#     mod_EOL_collection_eff
#     mod_EOL_collected_recycled
#     mod_Repowering
#     mod_Repairing

# In[95]:


# Module baseline mod.
stage = 'EOL_CE_Pathways'
modhigh = 1.10 
stage_highname = 'HighEff_'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)

stages = ['mod_EOL_collection_eff', 'mod_EOL_collected_recycled', 'mod_Repowering', 'mod_Repairing']

for i in range(0, len(stages)):
    stage = stages[i]
    r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                                 stage=stage, improvement=modhigh, start_year=0)


# ## Improving All EOL CE Pathways & Reliability
# 
# Includes
# 
#     mod_EOL_collection_eff
#     mod_EOL_collected_recycled
#     mod_Repowering
#     mod_Repairing
#     mod_reliability_t50
#     mod_reliability_t90
#     mod_lifetime

# In[96]:


# Module baseline mod.
stage = 'Reliability_and_CE_Pathways'
modhigh = 1.10
stage_highname = 'HighEff_'+stage

r1.createScenario(name=stage_highname, file=MODULEBASELINE)
r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)

stages = ['mod_EOL_collection_eff', 'mod_EOL_collected_recycled', 'mod_Repowering', 'mod_Repairing', 
          'mod_reliability_t50', 'mod_reliability_t90', 'mod_lifetime']

for i in range(0, len(stages)):
    stage = stages[i]
    r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                                 stage=stage, improvement=modhigh, start_year=0)


# # MASS FLOWS

# In[97]:


r1.calculateMassFlow()


# In[98]:


scenarios = list(r1.scenario.keys())


# In[99]:


scenarios


# In[100]:


virginStock_Changes = []
waste_Changes = []

virgin_keyword = 'mat_Virgin_Stock'
waste_keyword = 'mat_Total_Landfilled'

virginStock_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].materialdata[virgin_keyword].sum()
waste_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].materialdata[waste_keyword].sum()

for i in range (1, len(scenarios)):
    stage_name = scenarios[i]
    virginStock_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].materialdata[virgin_keyword].sum()/virginStock_baseline_cum2050,5)-100)
    waste_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].materialdata[waste_keyword].sum()/waste_baseline_cum2050,5)-100)


# In[ ]:





# In[101]:


stages = scenarios[1::]


# In[102]:


df = pd.DataFrame(list(zip(virginStock_Changes, waste_Changes)), 
               columns=['Virgin Needs Change', 'Waste Change'],index=stages) 


# In[103]:


df[['HighEff' in s for s in df.index]]


# In[104]:


df[['LowEff' in s for s in df.index]]


# In[ ]:





# # Print Values for a Senki Diagram, 1 year

# In[ ]:





# In[ ]:


mat_UsedSuccessfullyinModuleManufacturing = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_UsedSuccessfullyinModuleManufacturing'].sum()
mat_MFG_Scrap = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap'].sum()
mat_MFG_Scrap_Sentto_Recycling = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap_Sentto_Recycling'].sum()
mat_MFG_Scrap_Landfilled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap_Landfilled'].sum()
mat_MFG_Scrap_Recycled_Successfully = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap_Recycled_Successfully'].sum()
mat_MFG_Scrap_Recycled_Losses_Landfilled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap_Recycled_Losses_Landfilled'].sum()
mat_MFG_Recycled_into_HQ = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Recycled_into_HQ'].sum()
mat_MFG_Recycled_into_OQ = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Recycled_into_OQ'].sum()
mat_MFG_Recycled_HQ_into_MFG = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Recycled_HQ_into_MFG'].sum()
mat_MFG_Recycled_HQ_into_OU = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Recycled_HQ_into_OU'].sum()

mat_modules_NotCollected = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_modules_NotCollected'].sum()
mat_EOL_Collected = mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected
mat_EOL_collected_Recycled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_collected_Recycled'].sum()
mat_EOL_NotRecycled_Landfilled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_NotRecycled_Landfilled'].sum()
mat_EOL_Recycled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled'].sum()
mat_EOL_Recycled_Losses_Landfilled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled_Losses_Landfilled'].sum()
mat_EOL_Recycled_2_HQ = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled_2_HQ'].sum()
mat_EOL_Recycled_2_OQ = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled_2_OQ'].sum()
mat_EoL_Recycled_HQ_into_MFG = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EoL_Recycled_HQ_into_MFG'].sum()
mat_EOL_Recycled_HQ_into_OU = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled_HQ_into_OU'].sum()


# mat_Virgin_Stock, mat_UsedSuccessfullyinModuleManufacturing
# mat_Virgin_Stock, mat_MFG_Scrap
# mat_MFG_Scrap, mat_MFG_Scrap_Sentto_Recycling
# mat_MFG_Scrap, mat_MFG_Scrap_Landfilled
# mat_MFG_Scrap_Sentto_Recycling, mat_MFG_Scrap_Recycled_Successfully
# mat_MFG_Scrap_Sentto_Recycling, mat_MFG_Scrap_Recycled_Losses_Landfilled
# mat_MFG_Scrap_Recycled_Successfully, mat_MFG_Recycled_into_HQ
# mat_MFG_Scrap_Recycled_Successfully, mat_MFG_Recycled_into_OQ
# mat_MFG_Recycled_into_HQ, mat_MFG_Recycled_HQ_into_MFG
# mat_MFG_Recycled_into_HQ, mat_MFG_Recycled_HQ_into_OU
# 
# mat_UsedSuccessfullyinModuleManufacturing, mat_modules_NotCollected
# mat_UsedSuccessfullyinModuleManufacturing, (mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected) # mat collected
# (mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected), mat_EOL_collected_Recycled
# (mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected), mat_EOL_NotRecycled_Landfilled
# mat_EOL_collected_Recycled, mat_EOL_Recycled
# mat_EOL_collected_Recycled, mat_EOL_Recycled_Losses_Landfilled
# mat_EOL_Recycled, mat_EOL_Recycled_2_HQ
# mat_EOL_Recycled, mat_EOL_Recycled_2_OQ
# mat_EOL_Recycled_2_HQ, mat_EoL_Recycled_HQ_into_MFG
# mat_EOL_Recycled_2_HQ, mat_EOL_Recycled_HQ_into_OU
# 

# In[ ]:


print(mat_UsedSuccessfullyinModuleManufacturing,', ','Virgin Stock',', ','Modules')
print(mat_MFG_Scrap,', ','Virgin Stock',', ','Manufacturing Scrap')
print(mat_MFG_Scrap_Sentto_Recycling,', ','Manufacturing Scrap',', ','Sent to Recycling')
print(mat_MFG_Scrap_Landfilled,', ','Manufacturing Scrap',', ','Waste')
print(mat_MFG_Scrap_Recycled_Successfully,', ','Sent to Recycling',', ','Recycled')
print(mat_MFG_Scrap_Recycled_Losses_Landfilled,', ','Sent to Recycling',', ','Waste')
print(mat_MFG_Recycled_into_HQ,', ','Recycled',', ','HQ')
print(mat_MFG_Recycled_into_OQ,', ','Recycled',', ','OQ')
print(mat_MFG_Recycled_HQ_into_MFG,', ','HQ',', ','HQ_Mfg')
print(mat_MFG_Recycled_HQ_into_OU,', ','HQ',', ','HQ Other Uses')

print(mat_modules_NotCollected,', ','Modules,', ',mat_modules_NotCollected')
print((mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected),', ','Modules',', ','EOL Collected')
print(mat_EOL_collected_Recycled,', ','EOL Collected',', ','Sent to Recycling')
print(mat_EOL_NotRecycled_Landfilled,', ','EOL Collected',', ','Waste')
print(mat_EOL_Recycled,', ','Sent to Recycling',', ','Recycled')
print(mat_EOL_Recycled_Losses_Landfilled,', ','Sent to Recycling',', ','Waste')
print(mat_EOL_Recycled_2_HQ,', ','Recycled',', ','HQ')
print(mat_EOL_Recycled_2_OQ,', ','Recycled',', ','OQ')
print(mat_EoL_Recycled_HQ_into_MFG,', ','HQ',', ','HQ_Mfg')
print(mat_EOL_Recycled_HQ_into_OU,', ','HQ',', ','HQ Other Uses')


# In[ ]:


print('Virgin Stock',',','Modules',',',mat_UsedSuccessfullyinModuleManufacturing)
print('Virgin Stock',',','Manufacturing Scrap',',',mat_MFG_Scrap)
print('Manufacturing Scrap',',','Sent to Recycling',',',mat_MFG_Scrap_Sentto_Recycling)
print('Manufacturing Scrap',',','Waste',',',mat_MFG_Scrap_Landfilled)
print('Sent to Recycling',',','Recycled',',',mat_MFG_Scrap_Recycled_Successfully)
print('Sent to Recycling',',','Waste',',',mat_MFG_Scrap_Recycled_Losses_Landfilled)
print('Recycled',',','HQ',',',mat_MFG_Recycled_into_HQ)
print('Recycled',',','OQ',',',mat_MFG_Recycled_into_OQ)
print('HQ',',','HQ_Mfg',',',mat_MFG_Recycled_HQ_into_MFG)
print('HQ',',','HQ Other Uses',',',mat_MFG_Recycled_HQ_into_OU)

print('Modules,',',mat_modules_NotCollected',',',mat_modules_NotCollected)
print('Modules',',','EOL Collected',',',mat_EOL_Collected)
print('EOL Collected',',','Sent to Recycling',',',mat_EOL_collected_Recycled)
print('EOL Collected',',','Waste',',',mat_EOL_NotRecycled_Landfilled)
print('Sent to Recycling',',','Recycled',',',mat_EOL_Recycled)
print('Sent to Recycling',',','Waste',',',mat_EOL_Recycled_Losses_Landfilled)
print('Recycled',',','HQ',',',mat_EOL_Recycled_2_HQ)
print('Recycled',',','OQ',',',mat_EOL_Recycled_2_OQ)
print('HQ',',','HQ_Mfg',',',mat_EoL_Recycled_HQ_into_MFG)
print('HQ',',','HQ Other Uses',',',mat_EOL_Recycled_HQ_into_OU)


# In[ ]:


print('Virgin Stock,Modules,',mat_UsedSuccessfullyinModuleManufacturing)
print('Virgin Stock,Manufacturing Scrap,',mat_MFG_Scrap)
print('Manufacturing Scrap,Sent to Recycling,',mat_MFG_Scrap_Sentto_Recycling)
print('Manufacturing Scrap,Waste,',mat_MFG_Scrap_Landfilled)
print('Sent to Recycling,Recycled,',mat_MFG_Scrap_Recycled_Successfully)
print('Sent to Recycling,Waste,',mat_MFG_Scrap_Recycled_Losses_Landfilled)
print('Recycled,HQ,',mat_MFG_Recycled_into_HQ)
print('Recycled,OQ,',mat_MFG_Recycled_into_OQ)
print('HQ,HQ_Mfg,',mat_MFG_Recycled_HQ_into_MFG)
print('HQ,HQ Other Uses,',mat_MFG_Recycled_HQ_into_OU)

print('Modules,mat_modules_NotCollected,',mat_modules_NotCollected)
print('Modules,EOL Collected,',mat_EOL_Collected)
print('EOL Collected,Sent to Recycling,',mat_EOL_collected_Recycled)
print('EOL Collected,Waste,',mat_EOL_NotRecycled_Landfilled)
print('Sent to Recycling,Recycled,',mat_EOL_Recycled)
print('Sent to Recycling,Waste,',mat_EOL_Recycled_Losses_Landfilled)
print('Recycled,HQ,',mat_EOL_Recycled_2_HQ)
print('Recycled,OQ,',mat_EOL_Recycled_2_OQ)
print('HQ,HQ_Mfg,',mat_EoL_Recycled_HQ_into_MFG)
print('HQ,HQ Other Uses,',mat_EOL_Recycled_HQ_into_OU)


# In[ ]:





# In[ ]:


# Material Baseline Mod. Results
"""
resultkeyword = 'mat_Virgin_Stock'
print("Baseline Cum Value 2050 ", resultkeyword, ": ", r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum())
print("High Eff ", stage, resultkeyword, ": ", int(100*r1.scenario[stage_highname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
print("Low Eff", stage, resultkeyword, ": ", int(100*r1.scenario[stage_lowname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))

resultkeyword = 'mat_Total_Landfilled'
print("Baseline Cum Value 2050 ", resultkeyword, ": ", r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum())
print("High Eff ", stage, resultkeyword, ": ", int(100*r1.scenario[stage_highname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
print("Low Eff", stage, resultkeyword, ": ", int(100*r1.scenario[stage_lowname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
r""";


# In[ ]:


"""
fig, ax1 = plt.subplots()
ax1.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Total_Landfilled']/r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Total_Landfilled'], label='base eff')
ax1.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline_HighMatManufEff'].material[MATERIAL].materialdata['mat_Total_Landfilled']/r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Total_Landfilled'], label='high eff')
ax1.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline_lowMatManufEff'].material[MATERIAL].materialdata['mat_Total_Landfilled']/r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Total_Landfilled'], label='low eff')

ax2 = ax1.twinx()
ax2.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_eff'], '.')
ax2.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline_HighMatManufEff'].material[MATERIAL].materialdata['mat_MFG_eff'], '.')
ax2.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline_lowMatManufEff'].material[MATERIAL].materialdata['mat_MFG_eff'], '.')
ax1.legend()
""";


# In[ ]:





# In[ ]:





# In[ ]:




