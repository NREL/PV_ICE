#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path

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


# # Goal; Compare Virgin Material Extraction , and Waste. 

# ### Virgin Material Efficiency

# In[6]:


r1.createScenario(name='baseline_highVirginMaterialEfficiency', file=MODULEBASELINE)
r1.scenario['baseline_highVirginMaterialEfficiency'].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario['baseline_highVirginMaterialEfficiency'].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario['baseline_highVirginMaterialEfficiency'].material[MATERIAL].materialdata, 
                             stage='mat_virgin_eff', improvement=1.10, start_year=0)

r1.createScenario(name='baseline_lowVirginMaterialEfficiency', file=MODULEBASELINE)
r1.scenario['baseline_lowVirginMaterialEfficiency'].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.scenario['baseline_lowVirginMaterialEfficiency'].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario['baseline_lowVirginMaterialEfficiency'].material[MATERIAL].materialdata, 
                             stage='mat_virgin_eff', improvement=0.90, start_year=0)


# In[7]:


r1.calculateMassFlow()


# In[8]:


if SANITYCHECK:
    r1.plotMaterialComparisonAcrossScenarios(material=MATERIAL, keyword='mat_Virgin_Stock_Raw')
    r1.plotMaterialComparisonAcrossScenarios(material=MATERIAL, keyword='mat_Virgin_Stock')
    print(r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Virgin_Stock_Raw'].sum())
    print(r1.scenario['baseline_highVirginMaterialEfficiency'].material[MATERIAL].materialdata['mat_Virgin_Stock_Raw'].sum())
    print(r1.scenario['baseline_lowVirginMaterialEfficiency'].material[MATERIAL].materialdata['mat_Virgin_Stock_Raw'].sum())
    print("WASTE IS ALL THE SAME, bceause we are not counting landfilled Virgin Material Mining + Refining Waste")
    print(r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Virgin_Stock'].sum())
    print(r1.scenario['baseline_highVirginMaterialEfficiency'].material[MATERIAL].materialdata['mat_Virgin_Stock'].sum())
    print(r1.scenario['baseline_lowVirginMaterialEfficiency'].material[MATERIAL].materialdata['mat_Virgin_Stock'].sum())
    # RATIOS
    print("Baseline Virgin Needs:", 100*r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Virgin_Stock_Raw'].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Virgin_Stock_Raw'].sum())
    print("High Efficiency Scenario Virgin Needs:", int(100*r1.scenario['baseline_highVirginMaterialEfficiency'].material[MATERIAL].materialdata['mat_Virgin_Stock_Raw'].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Virgin_Stock_Raw'].sum()))
    print("Low Efficiency Scenario Virgin Needs:", int(100*r1.scenario['baseline_lowVirginMaterialEfficiency'].material[MATERIAL].materialdata['mat_Virgin_Stock_Raw'].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Virgin_Stock_Raw'].sum()))


# # Material Manfuacturing Efficiency 

# In[9]:


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
"""


# In[10]:


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


# In[11]:


r1.calculateMassFlow()    


# In[12]:


# RATIOS
resultkeyword = 'mat_Virgin_Stock'
print("Baseline Cum Value 2050 ", resultkeyword, ": ", r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum())
print("High Eff ", stage, resultkeyword, ": ", int(100*r1.scenario[stage_highname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
print("Low Eff", stage, resultkeyword, ": ", int(100*r1.scenario[stage_lowname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))

# RATIOS
resultkeyword = 'mat_Total_Landfilled'
print("Baseline Cum Value 2050 ", resultkeyword, ": ", r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum())
print("High Eff ", stage, resultkeyword, ": ", int(100*r1.scenario[stage_highname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
print("Low Eff", stage, resultkeyword, ": ", int(100*r1.scenario[stage_lowname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))


# In[13]:


r1.scenario[stage_highname].data.keys()


# # Module baseline mod.
# 
# ### mod_MFG_eff

# In[14]:


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


# In[15]:


r1.calculateMassFlow()

# RATIOS
resultkeyword = 'mat_Virgin_Stock'
print("Baseline Cum Value 2050 ", resultkeyword, ": ", r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum())
print("High Eff ", stage, resultkeyword, ": ", int(100*r1.scenario[stage_highname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
print("Low Eff", stage, resultkeyword, ": ", int(100*r1.scenario[stage_lowname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))

# RATIOS
resultkeyword = 'mat_Total_Landfilled'
print("Baseline Cum Value 2050 ", resultkeyword, ": ", r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum())
print("High Eff ", stage, resultkeyword, ": ", int(100*r1.scenario[stage_highname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
print("Low Eff", stage, resultkeyword, ": ", int(100*r1.scenario[stage_lowname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




