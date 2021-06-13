#!/usr/bin/env python
# coding: utf-8

# # Electrification Futures: Baseline Study with Bifacial Projection Assumptions 
# ## PVSC 2021 Paper

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'PVSC')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper',]
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'..\..\baselines\LiteratureProjections\baseline_modules_US_NREL_Energy_Futures_2021_basecase.csv'


# In[3]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# In[4]:


PV_ICE.__version__


# In[5]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[86]:


r1 = PV_ICE.Simulation(name='PV_ICE', path=testfolder)

r1.createScenario(name='Today', file=MODULEBASELINE)
MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_hold2020.csv'
r1.scenario['Today'].addMaterial('glass', file=MATERIALBASELINE)
MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
r1.scenario['Today'].addMaterial('aluminium_frames', file=MATERIALBASELINE)
for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r1.scenario['Today'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)

r1.createScenario(name='Bifacial', file=MODULEBASELINE)
MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_bifacialTrend.csv'
r1.scenario['Bifacial'].addMaterial('glass', file=MATERIALBASELINE)
MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_bifacialTrend.csv'
r1.scenario['Bifacial'].addMaterial('aluminium_frames', file=MATERIALBASELINE)
for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r1.scenario['Bifacial'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)

    


# In[ ]:





# In[87]:


# Irena EL 
r2 = PV_ICE.Simulation(name='Irena_EL', path=testfolder)

r2.createScenario(name='Today', file=MODULEBASELINE)
r2.scenario['Today'].data['mod_lifetime'] = 40
r2.scenario['Today'].data['mod_MFG_eff'] = 100.0

MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_hold2020.csv'
r2.scenario['Today'].addMaterial('glass', file=MATERIALBASELINE)
r2.scenario['Today'].material['glass'].materialdata['mat_MFG_eff'] = 100.0   
r2.scenario['Today'].material['glass'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
r2.scenario['Today'].addMaterial('aluminium_frames', file=MATERIALBASELINE)
r2.scenario['Today'].material['aluminium_frames'].materialdata['mat_MFG_eff'] = 100.0   
r2.scenario['Today'].material['aluminium_frames'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r2.scenario['Today'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)
    r2.scenario['Today'].material[MATERIALS[mat]].materialdata['mat_MFG_eff'] = 100.0   
    r2.scenario['Today'].material[MATERIALS[mat]].materialdata['mat_MFG_scrap_Recycled'] = 0.0
    

r2.createScenario(name='Bifacial', file=MODULEBASELINE)
r2.scenario['Bifacial'].data['mod_lifetime'] = 40
r2.scenario['Bifacial'].data['mod_MFG_eff'] = 100.0

MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_bifacialTrend.csv'
r2.scenario['Bifacial'].addMaterial('glass', file=MATERIALBASELINE)
r2.scenario['Bifacial'].material['glass'].materialdata['mat_MFG_eff'] = 100.0   
r2.scenario['Bifacial'].material['glass'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_bifacialTrend.csv'
r2.scenario['Bifacial'].addMaterial('aluminium_frames', file=MATERIALBASELINE)
r2.scenario['Bifacial'].material['aluminium_frames'].materialdata['mat_MFG_eff'] = 100.0   
r2.scenario['Bifacial'].material['aluminium_frames'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r2.scenario['Bifacial'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)
    r2.scenario['Bifacial'].material[MATERIALS[mat]].materialdata['mat_MFG_eff'] = 100.0   
    r2.scenario['Bifacial'].material[MATERIALS[mat]].materialdata['mat_MFG_scrap_Recycled'] = 0.0
    
    


# In[88]:


# Irena RL
r3 = PV_ICE.Simulation(name='Irena_RL', path=testfolder)

r3.createScenario(name='Today', file=MODULEBASELINE)
r3.scenario['Today'].data['mod_lifetime'] = 40
r3.scenario['Today'].data['mod_MFG_eff'] = 100.0

MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_hold2020.csv'
r3.scenario['Today'].addMaterial('glass', file=MATERIALBASELINE)
r3.scenario['Today'].material['glass'].materialdata['mat_MFG_eff'] = 100.0   
r3.scenario['Today'].material['glass'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
r3.scenario['Today'].addMaterial('aluminium_frames', file=MATERIALBASELINE)
r3.scenario['Today'].material['aluminium_frames'].materialdata['mat_MFG_eff'] = 100.0   
r3.scenario['Today'].material['aluminium_frames'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r3.scenario['Today'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)
    r3.scenario['Today'].material[MATERIALS[mat]].materialdata['mat_MFG_eff'] = 100.0   
    r3.scenario['Today'].material[MATERIALS[mat]].materialdata['mat_MFG_scrap_Recycled'] = 0.0
    

r3.createScenario(name='Bifacial', file=MODULEBASELINE)
r3.scenario['Bifacial'].data['mod_lifetime'] = 40
r3.scenario['Bifacial'].data['mod_MFG_eff'] = 100.0

MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_bifacialTrend.csv'
r3.scenario['Bifacial'].addMaterial('glass', file=MATERIALBASELINE)
r3.scenario['Bifacial'].material['glass'].materialdata['mat_MFG_eff'] = 100.0   
r3.scenario['Bifacial'].material['glass'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_bifacialTrend.csv'
r3.scenario['Bifacial'].addMaterial('aluminium_frames', file=MATERIALBASELINE)
r3.scenario['Bifacial'].material['aluminium_frames'].materialdata['mat_MFG_eff'] = 100.0   
r3.scenario['Bifacial'].material['aluminium_frames'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r3.scenario['Bifacial'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)
    r3.scenario['Bifacial'].material[MATERIALS[mat]].materialdata['mat_MFG_eff'] = 100.0   
    r3.scenario['Bifacial'].material[MATERIALS[mat]].materialdata['mat_MFG_scrap_Recycled'] = 0.0
    


# # RELIABILITY MESS

# ### Variables modified on each case:
# <li> Case1 -- r4 : mod_lifetime, mod_reliability_t50, mod_reliability_t90
# <li> Case2 -- r5: mod_lifetime, mod_reliability_t50, mod_reliability_t90, mod_degradation
# <li> Case3 -- r6: mod_degradation
# 

# In[89]:


Life_Good = [3, 6, 9, 12, 15, 18, 21, 24]
degradation_Good = [-0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8]
Life_Bad = [element * -1 for element in Life_Good]
degradation_Bad = [0.2, 0.4, 0.6, 0.8, 1.2, 1.6, 2.0, 3.0]


# In[90]:


r4 = PV_ICE.Simulation(name='Reliability_Case1', path=testfolder)

for i in range(0, len(Life_Good)):
    scenname = 'Lifetime_Improvements_of_'+str(Life_Good[i])+'_years'
    r4.createScenario(name=scenname, file=MODULEBASELINE)
    r4.scenario[scenname].data['mod_reliability_t50'] = r4.scenario[scenname].data['mod_reliability_t50'] + Life_Good[i]
    r4.scenario[scenname].data['mod_reliability_t90'] = r4.scenario[scenname].data['mod_reliability_t90'] + Life_Good[i]
    r4.scenario[scenname].data['mod_lifetime'] = r4.scenario[scenname].data['mod_lifetime'] + Life_Good[i]
    MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_hold2020.csv'
    r4.scenario[scenname].addMaterial('glass', file=MATERIALBASELINE)
    MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
    r4.scenario[scenname].addMaterial('aluminium_frames', file=MATERIALBASELINE)
    for mat in range (2, len(MATERIALS)):
        MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
        r4.scenario[scenname].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)

    scenname = 'Lifetime_Decline_of_'+str(Life_Good[i])+'_years'
    r4.createScenario(name=scenname, file=MODULEBASELINE)
    r4.scenario[scenname].data['mod_reliability_t50'] = r4.scenario[scenname].data['mod_reliability_t50'] + Life_Bad[i]
    r4.scenario[scenname].data['mod_reliability_t90'] = r4.scenario[scenname].data['mod_reliability_t90'] + Life_Bad[i]
    r4.scenario[scenname].data['mod_lifetime'] = r4.scenario[scenname].data['mod_lifetime'] + Life_Bad[i]
    r4.scenario[scenname].data['mod_reliability_t50'][r4.scenario[scenname].data['mod_reliability_t50']<=3.0] = 1.0
    r4.scenario[scenname].data['mod_reliability_t90'][r4.scenario[scenname].data['mod_reliability_t90']<=3.0] = 2.0
    r4.scenario[scenname].data['mod_lifetime'][r4.scenario[scenname].data['mod_lifetime']<=3.0] = 3.0

    MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_hold2020.csv'
    r4.scenario[scenname].addMaterial('glass', file=MATERIALBASELINE)
    MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
    r4.scenario[scenname].addMaterial('aluminium_frames', file=MATERIALBASELINE)
    for mat in range (2, len(MATERIALS)):
        MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
        r4.scenario[scenname].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)   


# In[91]:


# Sanity Check
print('Scenario', list(r4.scenario.keys())[0] , 't50 in 2030: ', r4.scenario[list(r4.scenario.keys())[0]].data['mod_reliability_t50'][35])
print('Scenario', list(r4.scenario.keys())[1] , 't50 in 2030: ', r4.scenario[list(r4.scenario.keys())[1]].data['mod_reliability_t50'][35])


# In[92]:


r5 = PV_ICE.Simulation(name='Reliability_Case2', path=testfolder)

for i in range(0, len(Life_Good)):
    scenname = 'Lifetime_Improvements_of_'+str(Life_Good[i])+'_years'
    r5.createScenario(name=scenname, file=MODULEBASELINE)
    r5.scenario[scenname].data['mod_reliability_t50'] = r5.scenario[scenname].data['mod_reliability_t50'] + Life_Good[i]
    r5.scenario[scenname].data['mod_reliability_t90'] = r5.scenario[scenname].data['mod_reliability_t90'] + Life_Good[i]
    r5.scenario[scenname].data['mod_lifetime'] = r5.scenario[scenname].data['mod_lifetime'] + Life_Good[i]
    r5.scenario[scenname].data['mod_degradation'] = r5.scenario[scenname].data['mod_degradation'] + degradation_Good[i]
    r5.scenario[scenname].data['mod_degradation'][r5.scenario[scenname].data['mod_degradation']<=0.0] = 0.000000001
    
    MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_hold2020.csv'
    r5.scenario[scenname].addMaterial('glass', file=MATERIALBASELINE)
    MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
    r5.scenario[scenname].addMaterial('aluminium_frames', file=MATERIALBASELINE)
    for mat in range (2, len(MATERIALS)):
        MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
        r5.scenario[scenname].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)

    scenname = 'Lifetime_Decline_of_'+str(Life_Good[i])+'_years'
    r5.createScenario(name=scenname, file=MODULEBASELINE)
    r5.scenario[scenname].data['mod_reliability_t50'] = r5.scenario[scenname].data['mod_reliability_t50'] + Life_Bad[i]
    r5.scenario[scenname].data['mod_reliability_t90'] = r5.scenario[scenname].data['mod_reliability_t90'] + Life_Bad[i]
    r5.scenario[scenname].data['mod_lifetime'] = r5.scenario[scenname].data['mod_lifetime'] + Life_Bad[i]
    r5.scenario[scenname].data['mod_degradation'] = r5.scenario[scenname].data['mod_degradation'] + degradation_Bad[i]

    r5.scenario[scenname].data['mod_reliability_t50'][r5.scenario[scenname].data['mod_reliability_t50']<=3.0] = 1.0
    r5.scenario[scenname].data['mod_reliability_t90'][r5.scenario[scenname].data['mod_reliability_t90']<=3.0] = 2.0
    r5.scenario[scenname].data['mod_lifetime'][r5.scenario[scenname].data['mod_lifetime']<=3.0] = 3.0

    MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_hold2020.csv'
    r5.scenario[scenname].addMaterial('glass', file=MATERIALBASELINE)
    MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
    r5.scenario[scenname].addMaterial('aluminium_frames', file=MATERIALBASELINE)
    for mat in range (2, len(MATERIALS)):
        MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
        r5.scenario[scenname].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)   


# In[93]:


r6 = PV_ICE.Simulation(name='Reliability_Case3', path=testfolder)

for i in range(0, len(Life_Good)):
    scenname = 'Lifetime_Improvements_of_'+str(Life_Good[i])+'_years'
    r6.createScenario(name=scenname, file=MODULEBASELINE)
    r6.scenario[scenname].data['mod_degradation'] = r6.scenario[scenname].data['mod_degradation'] + degradation_Good[i]
    r6.scenario[scenname].data['mod_degradation'][r6.scenario[scenname].data['mod_degradation']<=0.0] = 0.000000001
    
    MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_hold2020.csv'
    r6.scenario[scenname].addMaterial('glass', file=MATERIALBASELINE)
    MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
    r6.scenario[scenname].addMaterial('aluminium_frames', file=MATERIALBASELINE)
    for mat in range (2, len(MATERIALS)):
        MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
        r6.scenario[scenname].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)

    scenname = 'Lifetime_Decline_of_'+str(Life_Good[i])+'_years'
    r6.createScenario(name=scenname, file=MODULEBASELINE)
    r6.scenario[scenname].data['mod_degradation'] = r6.scenario[scenname].data['mod_degradation'] + degradation_Bad[i]

    r6.scenario[scenname].data['mod_reliability_t50'][r6.scenario[scenname].data['mod_reliability_t50']<=3.0] = 1.0
    r6.scenario[scenname].data['mod_reliability_t90'][r6.scenario[scenname].data['mod_reliability_t90']<=3.0] = 2.0
    r6.scenario[scenname].data['mod_lifetime'][r6.scenario[scenname].data['mod_lifetime']<=3.0] = 3.0

    MATERIALBASELINE = r'..\..\baselines\baseline_material_glass_hold2020.csv'
    r6.scenario[scenname].addMaterial('glass', file=MATERIALBASELINE)
    MATERIALBASELINE = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
    r6.scenario[scenname].addMaterial('aluminium_frames', file=MATERIALBASELINE)
    for mat in range (2, len(MATERIALS)):
        MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
        r6.scenario[scenname].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)   


# # Run Simulations 

# In[94]:


r1.calculateMassFlow()


# In[95]:


weibullInputParams = {'alpha': 2.49, 'beta':30}  # Early-loss scenario IRENA
r2.calculateMassFlow(weibullInputParams=weibullInputParams)

weibullInputParams = {'alpha': 5.3759, 'beta':30}  # Regular-loss scenario IRENA
r3.calculateMassFlow(weibullInputParams=weibullInputParams)


# In[96]:


r4.calculateMassFlow()
r5.calculateMassFlow()
r6.calculateMassFlow()


# In[97]:


r4.scenario[list(r4.scenario.keys())[-1]].data


# ## Creating Summary of results 
# 

# In[98]:


#Simulations = [r1, r2, r3, r4, r5, r6]
Simulations = [r1, r2, r3]
#scenarios = ['Today', 'Bifacial']


# In[99]:


r1.scenario['Today'].material['copper'].materialdata['mat_Total_Landfilled'].tail(5)


# In[100]:


r1.scenario['Bifacial'].material['copper'].materialdata['mat_Total_Landfilled'].tail(5)


# In[101]:


USyearly=pd.DataFrame()


# In[102]:


keyword='mat_Total_Landfilled'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']

# Loop over objects
for kk in range(0, len(Simulations)):
    obj = Simulations[kk]

    # Loop over Scenarios
    for jj in range(0, len(obj.scenario)):
        case = list(obj.scenario.keys())[jj]

        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = obj.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["Waste_"+material+'_'+obj.name+'_'+case] = foo[material]

        filter_col = [col for col in USyearly if (col.startswith('Waste') and col.endswith(obj.name+'_'+case)) ]
        USyearly['Waste_Module_'+obj.name+'_'+case] = USyearly[filter_col].sum(axis=1)

# Converting to grams to Tons. 
USyearly.head(20)


# In[103]:


keyword='mat_Total_EOL_Landfilled'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']

# Loop over objects
for kk in range(0, len(Simulations)):
    obj = Simulations[kk]

    # Loop over Scenarios
    for jj in range(0, len(obj.scenario)):
        case = list(obj.scenario.keys())[jj]

        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = obj.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["Waste_EOL_"+material+'_'+obj.name+'_'+case] = foo[material]

        filter_col = [col for col in USyearly if (col.startswith('Waste') and col.endswith(obj.name+'_'+case)) ]
        USyearly['Waste_EOL_Module_'+obj.name+'_'+case] = USyearly[filter_col].sum(axis=1)

# Converting to grams to Tons. 
USyearly.head(20)


# In[104]:


keyword='mat_Total_MFG_Landfilled'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']

# Loop over objects
for kk in range(0, len(Simulations)):
    obj = Simulations[kk]

    # Loop over Scenarios
    for jj in range(0, len(obj.scenario)):
        case = list(obj.scenario.keys())[jj]

        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = obj.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["Waste_MFG_"+material+'_'+obj.name+'_'+case] = foo[material]

        filter_col = [col for col in USyearly if (col.startswith('Waste') and col.endswith(obj.name+'_'+case)) ]
        USyearly['Waste_MFG_Module_'+obj.name+'_'+case] = USyearly[filter_col].sum(axis=1)

# Converting to grams to Tons. 
USyearly.head(20)


# In[105]:


keyword='mat_Virgin_Stock'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']

# Loop over objects
for kk in range(0, len(Simulations)):
    obj = Simulations[kk]

    # Loop over Scenarios
    for jj in range(0, len(obj.scenario)):
        case = list(obj.scenario.keys())[jj]

        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = obj.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["VirginStock_"+material+'_'+obj.name+'_'+case] = foo[material]

        filter_col = [col for col in USyearly if (col.startswith('Waste') and col.endswith(obj.name+'_'+case)) ]
        USyearly['VirginStock_Module_'+obj.name+'_'+case] = USyearly[filter_col].sum(axis=1)

# Converting to grams to Tons. 
USyearly.head(20)


# ### Converting to grams to METRIC Tons. 
# 

# In[106]:


USyearly = USyearly/1000000  # This is the ratio for Metric tonnes
#907185 -- this is for US tons


# In[107]:


UScum = USyearly.copy()
UScum = UScum.cumsum()
UScum.head()


# ### Adding Installed Capacity to US

# In[108]:


keyword='Installed_Capacity_[W]'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']

# Loop over objects
for kk in range(0, len(Simulations)):
    obj = Simulations[kk]

    # Loop over Scenarios
    for jj in range(0, len(obj.scenario)):
        case = list(obj.scenario.keys())[jj]

        foo = obj.scenario[case].data[keyword]
        foo = foo.to_frame(name=keyword)
        UScum["Capacity_"+obj.name+'_'+case] = foo[keyword]
        
# Converting to grams to Tons. 
USyearly.head(20)


# In[109]:


UScum.tail(20)


# ## Mining Capacity

# In[110]:


USyearly.index = r1.scenario['Today'].data['year']
UScum.index = r1.scenario['Today'].data['year']


# In[111]:


mining2020_aluminum = 65267000
mining2020_silver = 22260
mining2020_copper = 20000000
mining2020_silicon = 8000000


# # PLOTTING GALORE

# In[112]:


list(USyearly.keys())


# In[ ]:





# In[113]:


#VirginStock_glass_PVSC_Today
#VirginStock_glass_PVSC_Bifacial

plt.rcParams.update({'font.size': 10})
plt.rcParams['figure.figsize'] = (12, 8)
    
keyw='VirginStock_'
materials = ['glass', 'silicon','silver', 'copper', 'aluminium_frames']

fig, axs = plt.subplots(1,1, figsize=(4, 6), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.2)


# Loop over CASES
name2 = 'PV_ICE_Today'
name0 = 'PV_ICE_Bifacial'
# ROW 2, Aluminum and Silicon:        g-  4 aluminum k - 1 silicon   orange - 3 copper  gray - 2 silver
axs.plot(USyearly[keyw+materials[2]+'_'+name2]*100/mining2020_silver, 
         color = 'gray', linewidth=2.0, label='Silver')

axs.fill_between(USyearly.index, USyearly[keyw+materials[2]+'_'+name0]*100/mining2020_silver, 
                 USyearly[keyw+materials[2]+'_'+name2]*100/mining2020_silver,
                   color='gray', lw=3, alpha=.3)
    

axs.plot(USyearly[keyw+materials[1]+'_'+name2]*100/mining2020_silicon, 
         color = 'k', linewidth=2.0, label='Silicon')
axs.fill_between(USyearly.index, USyearly[keyw+materials[1]+'_'+name0]*100/mining2020_silicon, 
                                USyearly[keyw+materials[1]+'_'+name2]*100/mining2020_silicon,
                   color='k', lw=3, alpha=.5)



axs.plot(USyearly[keyw+materials[4]+'_'+name2]*100/mining2020_aluminum, 
         color = 'g', linewidth=2.0, label='Aluminum')

axs.fill_between(USyearly.index, USyearly[keyw+materials[4]+'_'+name0]*100/mining2020_aluminum, 
                                USyearly[keyw+materials[4]+'_'+name2]*100/mining2020_aluminum,
                   color='g', lw=3, alpha=.3)



axs.plot(USyearly[keyw+materials[3]+'_'+name2]*100/mining2020_copper, 
         color = 'orange', linewidth=2.0, label='Copper')

axs.fill_between(USyearly.index, USyearly[keyw+materials[3]+'_'+name0]*100/mining2020_copper, 
                                USyearly[keyw+materials[3]+'_'+name2]*100/mining2020_copper,
                   color='orange', lw=3, alpha=.3)



axs.set_xlim([2020,2050])
axs.legend()
#axs.set_yscale('log')

axs.set_ylabel('Virgin material needs as a percentage of \n 2020 global mining production capacity [%]')

#fig.savefig(os.path.join(testfolder,'Fig_1x1_MaterialNeeds Ratio to Production_NREL2018.png'), dpi=600)


# In[ ]:





# In[114]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='VirginStock_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name0 = 'PV_ICE_Today'
name2 = 'PV_ICE_Bifacial'


# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k.', linewidth=5, label='S1: '+name0+' module mass')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='S1: '+name0+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'c.', linewidth=5, label='S2: '+name2+' module mass')
a0.plot(USyearly.index, glassmat, 'c', linewidth=5, label='S2: '+name2+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='c', alpha=0.3,
                 interpolate=True)

a0.legend()
a0.set_title('Yearly Virgin Material Needs by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
    
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


## Plot BARS Stuff
ind=np.arange(2)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.set_ylabel('Virgin Material Cumulative Needs 2020-2050 [Million Tonnes]')
a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))

f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly Virgin Material Needs by Scenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Virgin Needs by 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[116]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_EOL_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name0 = 'PV_ICE_Today'
name2 = 'PV_ICE_Bifacial'

# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k.', linewidth=5, label='S1: '+name0+' module mass')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='S1: '+name0+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'c.', linewidth=5, label='S2: '+name2+' module mass')
a0.plot(USyearly.index, glassmat, 'c', linewidth=5, label='S2: '+name2+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='c', alpha=0.3,
                 interpolate=True)

a0.legend()
a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


## Plot BARS Stuff
ind=np.arange(2)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))

f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# # Waste_ EOL 

# In[250]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_EOL_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2,0.8,0.8]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name0 = 'Irena_EL_Today'
name2 = 'Irena_EL_Bifacial'

# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k', linestyle='dotted', linewidth=5, label='Today: module')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='Today: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Bifacial Evolution: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Bifacial Evolution: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

a0.legend()
#a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']

dfcumulations2050_Prev_A = dfcumulations2050.copy()


## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
#a1.yaxis.set_visible(False)
a1.yaxis.set_ticklabels([]) 
#a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)



print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)



########################    
# SUBPLOT 3
########################
#######################
# Calculate    


cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']

dfcumulations2050_Prev_B = dfcumulations2050.copy()

## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a2.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a2.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a2.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a2.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a2.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a2.yaxis.set_label_position("right")
a2.yaxis.tick_right()
a2.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a2.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a2.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'),
          bbox_to_anchor=(0.6, -0.25),
          fancybox=True, shadow=True, ncol=5)
a2.set_ylim([0, 28])

plt.sca(a2)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[251]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_EOL_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2,0.8,0.8]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name0 = 'Irena_RL_Today'
name2 = 'Irena_RL_Bifacial'

# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k', linestyle='dotted', linewidth=5, label='Today: module')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='Today: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Bifacial Evolution: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Bifacial Evolution: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

a0.legend()
#a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']

dfcumulations2050.iloc[1] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_A.iloc[0]

dfcumulations2050_Prev_A = dfcumulations2050.copy()

## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.yaxis.set_ticklabels([]) 
a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)



print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)

########################    
# SUBPLOT 3
########################
#######################
# Calculate    


cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


dfcumulations2050.iloc[1] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_B.iloc[0]

dfcumulations2050_Prev_B = dfcumulations2050.copy()

## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a2.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a2.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a2.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a2.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a2.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a2.yaxis.set_label_position("right")
a2.yaxis.tick_right()
a2.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a2.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a2.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'),
          bbox_to_anchor=(0.6, -0.25),
          fancybox=True, shadow=True, ncol=5)
a2.set_ylim([0, 28])

plt.sca(a2)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[255]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_EOL_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2,0.8,0.8]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name0 = 'PV_ICE_Today'
name2 = 'PV_ICE_Bifacial'

# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k', linestyle='dotted', linewidth=5, label='Today: module')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='Today: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Bifacial Evolution: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Bifacial Evolution: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

a0.legend(loc=2)
#a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']

dfcumulations2050.iloc[2] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_A.iloc[0]
dfcumulations2050.iloc[1] = dfcumulations2050_Prev_A.iloc[1]

dfcumulations2050_Prev_A = dfcumulations2050.copy()

## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.yaxis.set_ticklabels([]) 

a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
a1.yaxis.set_ticklabels([]) 
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)



print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


########################    
# SUBPLOT 3
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


dfcumulations2050.iloc[2] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_B.iloc[0]
dfcumulations2050.iloc[1] = dfcumulations2050_Prev_B.iloc[1]

dfcumulations2050_Prev_B = dfcumulations2050.copy()


## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a2.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a2.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a2.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a2.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a2.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a2.yaxis.set_label_position("right")
a2.yaxis.tick_right()
a2.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a2.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a2.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'),
          bbox_to_anchor=(0.6, -0.25),
          fancybox=True, shadow=True, ncol=5)
a2.set_ylim([0, 28])

plt.sca(a2)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# # Waste_ EOL + MFG

# In[256]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2,0.8,0.8]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name0 = 'Irena_EL_Today'
name2 = 'Irena_EL_Bifacial'

# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k', linestyle='dotted', linewidth=5, label='Today: module')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='Today: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Bifacial Evolution: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Bifacial Evolution: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

a0.legend()
#a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']

dfcumulations2050_Prev_A = dfcumulations2050.copy()


## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
#a1.yaxis.set_visible(False)
a1.yaxis.set_ticklabels([]) 
#a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)



print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)



########################    
# SUBPLOT 3
########################
#######################
# Calculate    


cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']

dfcumulations2050_Prev_B = dfcumulations2050.copy()

## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a2.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a2.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a2.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a2.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a2.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a2.yaxis.set_label_position("right")
a2.yaxis.tick_right()
a2.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a2.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a2.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'),
          bbox_to_anchor=(0.6, -0.25),
          fancybox=True, shadow=True, ncol=5)
a2.set_ylim([0, 28])

plt.sca(a2)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[257]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2,0.8,0.8]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name0 = 'Irena_RL_Today'
name2 = 'Irena_RL_Bifacial'

# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k', linestyle='dotted', linewidth=5, label='Today: module')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='Today: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Bifacial Evolution: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Bifacial Evolution: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

a0.legend()
#a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']

dfcumulations2050.iloc[1] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_A.iloc[0]

dfcumulations2050_Prev_A = dfcumulations2050.copy()

## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.yaxis.set_ticklabels([]) 
a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)



print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)

########################    
# SUBPLOT 3
########################
#######################
# Calculate    


cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


dfcumulations2050.iloc[1] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_B.iloc[0]

dfcumulations2050_Prev_B = dfcumulations2050.copy()

## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a2.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a2.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a2.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a2.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a2.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a2.yaxis.set_label_position("right")
a2.yaxis.tick_right()
a2.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a2.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a2.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'),
          bbox_to_anchor=(0.6, -0.25),
          fancybox=True, shadow=True, ncol=5)
a2.set_ylim([0, 28])

plt.sca(a2)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[258]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2,0.8,0.8]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name0 = 'PV_ICE_Today'
name2 = 'PV_ICE_Bifacial'

# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k', linestyle='dotted', linewidth=5, label='Today: module')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='Today: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Bifacial Evolution: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Bifacial Evolution: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

a0.legend(loc=2)
#a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']

dfcumulations2050.iloc[2] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_A.iloc[0]
dfcumulations2050.iloc[1] = dfcumulations2050_Prev_A.iloc[1]

dfcumulations2050_Prev_A = dfcumulations2050.copy()

## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.yaxis.set_ticklabels([]) 

a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
a1.yaxis.set_ticklabels([]) 
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)



print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


########################    
# SUBPLOT 3
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


dfcumulations2050.iloc[2] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_B.iloc[0]
dfcumulations2050.iloc[1] = dfcumulations2050_Prev_B.iloc[1]

dfcumulations2050_Prev_B = dfcumulations2050.copy()


## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a2.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a2.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a2.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a2.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a2.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a2.yaxis.set_label_position("right")
a2.yaxis.tick_right()
a2.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a2.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a2.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'),
          bbox_to_anchor=(0.6, -0.25),
          fancybox=True, shadow=True, ncol=5)
a2.set_ylim([0, 28])

plt.sca(a2)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# # Installed Capacity

# In[263]:


UScum.keys()


# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0) = plt.subplots(1, 1, gridspec_kw={'width_ratios': [2]})


# In[262]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0) = plt.subplots(1, 1, gridspec_kw={'width_ratios': [2]})


# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2,0.8,0.8]})

########################    
# SUBPLOT 
########################
#######################
   
# Loop over CASES
name0 = 'PV_ICE_Today'
name2 = 'PV_ICE_Bifacial'

# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k', linestyle='dotted', linewidth=5, label='Today: module')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='Today: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Bifacial Evolution: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Bifacial Evolution: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

a0.legend(loc=2)
#a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']

dfcumulations2050.iloc[2] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_A.iloc[0]
dfcumulations2050.iloc[1] = dfcumulations2050_Prev_A.iloc[1]

dfcumulations2050_Prev_A = dfcumulations2050.copy()

## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.yaxis.set_ticklabels([]) 

a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
a1.yaxis.set_ticklabels([]) 
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)



print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


########################    
# SUBPLOT 3
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    empty = 0
    matcum.append(empty)
    matcum.append(empty)
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


dfcumulations2050.iloc[2] = dfcumulations2050.iloc[0] 
dfcumulations2050.iloc[0] = dfcumulations2050_Prev_B.iloc[0]
dfcumulations2050.iloc[1] = dfcumulations2050_Prev_B.iloc[1]

dfcumulations2050_Prev_B = dfcumulations2050.copy()


## Plot BARS Stuff
ind=np.arange(3)
width=0.35 # width of the bars.
p0 = a2.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a2.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a2.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a2.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a2.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a2.yaxis.set_label_position("right")
a2.yaxis.tick_right()
a2.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a2.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a2.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'),
          bbox_to_anchor=(0.6, -0.25),
          fancybox=True, shadow=True, ncol=5)
a2.set_ylim([0, 28])

plt.sca(a2)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # WEIBULL PLOTS

# In[193]:


firstgen = r1.scenario['Today'].data.WeibullParams.iloc[0]
ares = PV_ICE.weibull_cdf_vis(firstgen['alpha'],firstgen['beta'])

twentythirtygen = firstgen = r1.scenario['Today'].data.WeibullParams.iloc[-1]
bres = PV_ICE.weibull_cdf_vis(twentythirtygen['alpha'],twentythirtygen['beta'])

#userWeibulls = {'alpha': 3.4,
#               'beta': 4.5}
#userres = PV_ICE.weibull_cdf_vis(userWeibulls['alpha'],userWeibulls['beta'])

# Irena 'EL' 2016
alpha = 2.4928
Lifetime = 30
IrenaEarly = PV_ICE.weibull_cdf_vis(alpha, beta=Lifetime)

# Irena 'RL' 2016
alpha = 5.3759
Lifetime = 30
IrenaReg = PV_ICE.weibull_cdf_vis(alpha, beta=Lifetime)


# In[ ]:





# In[220]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (10, 8)
    
#plt.plot(ares, label=r'$ \alpha $ : '+str(round(firstgen['alpha'],2))+ r' $ \beta $ : '+ str(round(firstgen['beta'],2)) + ' PV ICE, gen 1995')
#plt.plot(bres, color='b', label=r'$ \alpha $ : '+str(round(twentythirtygen['alpha'],2))+ r' $ \beta $ : '+ str(round(twentythirtygen['beta'],2)) + ' PV ICE, gen 2050')
plt.plot(IrenaEarly, color='red', linewidth=16.0, label=r'$ \alpha $ : 2.49, Early Loss Baseline Irena 2016')
#plt.plot(IrenaReg, color='orange', linewidth=4.0, label=r'$ \alpha $ : 5.3759, Regular Loss Baseline Irena 2016')
#plt.legend()
plt.ylabel('Cumulative Distribution Function (CDF)')
plt.xlabel('Years since install')
plt.xlim([0,50])
ax = plt.gca()
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)

#plt.legend(bbox_to_anchor=(1.05, 1.0), loc='bottom');


# In[219]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (10, 8)
    
#plt.plot(ares, label=r'$ \alpha $ : '+str(round(firstgen['alpha'],2))+ r' $ \beta $ : '+ str(round(firstgen['beta'],2)) + ' PV ICE, gen 1995')
#plt.plot(bres, color='b', label=r'$ \alpha $ : '+str(round(twentythirtygen['alpha'],2))+ r' $ \beta $ : '+ str(round(twentythirtygen['beta'],2)) + ' PV ICE, gen 2050')
#plt.plot(IrenaEarly, color='red', linewidth=4.0, label=r'$ \alpha $ : 2.49, Early Loss Baseline Irena 2016')
plt.plot(IrenaReg, color='darkgreen', linewidth=16.0, label=r'$ \alpha $ : 5.3759, Regular Loss Baseline Irena 2016')
#plt.legend()
plt.ylabel('Cumulative Distribution Function (CDF)')
plt.xlabel('Years since install')
plt.xlim([0,50])
ax = plt.gca()
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)

#plt.legend(bbox_to_anchor=(1.05, 1.0), loc='bottom');


# In[203]:


from matplotlib.pyplot import gca,show


# In[ ]:





# In[245]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (10, 8)
    
plt.plot(ares, linewidth=16.0, label=r'$ \alpha $ : '+str(round(firstgen['alpha'],2))+ r' $ \beta $ : '+ str(round(firstgen['beta'],2)) + ' PV ICE, gen 1995')
plt.plot(bres, linewidth=16.0, color='b', label=r'$ \alpha $ : '+str(round(twentythirtygen['alpha'],2))+ r' $ \beta $ : '+ str(round(twentythirtygen['beta'],2)) + ' PV ICE, gen 2050')
#plt.plot(IrenaEarly, color='red', linewidth=4.0, label=r'$ \alpha $ : 2.49, Early Loss Baseline Irena 2016')
#plt.plot(IrenaReg, color='orange', linewidth=4.0, label=r'$ \alpha $ : 5.3759, Regular Loss Baseline Irena 2016')
#plt.legend()
plt.ylabel('Cumulative Distribution Function (CDF)')
plt.xlabel('Years since install')
plt.xlim([0,50])
ax = plt.gca()
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)


opt = dict(color='r',width=12, headwidth=60, headlength=60)

gca().annotate('',xy=(38,0.5), xycoords='data',xytext =(18,0.5),textcoords = 'data',arrowprops=opt)

#plt.legend(bbox_to_anchor=(1.05, 1.0), loc='bottom');


# In[ ]:





# In[ ]:





# In[122]:





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


# Loop over CASES
name0 = 'PV_ICE_base'
name2 = 'PV_ICE_high'
name3 = 'Irena_EL_high'
name4 = 'Irena_RL_high'

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2040])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2040])
    matcum.append(UScum[keyw+materials[ii]+'_'+name3].loc[2040])
    matcum.append(UScum[keyw+materials[ii]+'_'+name4].loc[2040])
    
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes
dfcumulations2050['Module'] = dfcumulations2050.sum(axis=1)
dfcumulations2050['Module']


# In[ ]:





# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name2 = 'PV_ICE_high'
name0 = 'PV_ICE_base'


# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k.', linewidth=5, label='S1: '+name0+' module mass')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='S1: '+name0+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'c.', linewidth=5, label='S2: '+name2+' module mass')
a0.plot(USyearly.index, glassmat, 'c', linewidth=5, label='S2: '+name2+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='c', alpha=0.3,
                 interpolate=True)

a0.legend()
a0.set_title('Yearly Manufacturing Scrap and EoL Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
    
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


## Plot BARS Stuff
ind=np.arange(2)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.set_ylabel('Cumulative Manufacturing Scrap and EoL Material \n by 2050 [Million Tonnes]')
a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))

f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly MFG and EOL Material by Scenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste Scrap and EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_MFG_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name2 = 'PV_ICE_high'
name0 = 'PV_ICE_base'


# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k.', linewidth=5, label='S1: '+name0+' module mass')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='S1: '+name0+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'c.', linewidth=5, label='S2: '+name2+' module mass')
a0.plot(USyearly.index, glassmat, 'c', linewidth=5, label='S2: '+name2+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='c', alpha=0.3,
                 interpolate=True)

a0.legend()
a0.set_title('Yearly Manufacturing Scrap by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
    
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


## Plot BARS Stuff
ind=np.arange(2)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.set_ylabel('Cumulative Manufacturing Scrap by 2050 [Million Tonnes]')
a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))

f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_YYearly MFG Waste by Scenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative MFG Scrap 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='VirginStock_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']

fig, axs = plt.subplots(3,2, figsize=(18, 10), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=.2)
axs = axs.ravel()

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name2 = 'PV_ICE_high'
name0 = 'PV_ICE_base'
name3 = 'Irena_EL_high'
name4 = 'Irena_RL_high'


# SCENARIO 1 ***************

modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[0].plot(USyearly.index, modulemat, 'k.', linewidth=5, label='S1: '+name0+' module mass')
axs[0].plot(USyearly.index, glassmat, 'k', linewidth=5, label='S1: '+name0+' glass mass only')
axs[0].fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[0].plot(USyearly.index, modulemat, 'c.', linewidth=5, label='S2: '+name2+' module mass')
axs[0].plot(USyearly.index, glassmat, 'c', linewidth=5, label='S2: '+name2+' glass mass only')
axs[0].fill_between(USyearly.index, glassmat, modulemat, color='c', alpha=0.3,
                 interpolate=True)

#axs[0].legend()
axs[0].set_title('Yearly Virgin Material Needs by Scenario')
axs[0].set_ylabel('Mass [Million Tonnes]')
axs[0].set_xlim([2020, 2050])
axs[0].set_xlabel('Years')
    
# SCENARIO 3 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name3]+USyearly[keyw+materials[1]+'_'+name3]+
            USyearly[keyw+materials[2]+'_'+name3]+USyearly[keyw+materials[3]+'_'+name3]+
            USyearly[keyw+materials[4]+'_'+name3])
glassmat = (USyearly[keyw+materials[0]+'_'+name3])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[1].plot(USyearly.index, modulemat, 'g.', linewidth=5, label='S2: '+name3+' module mass')
axs[1].plot(USyearly.index, glassmat, 'g', linewidth=5, label='S2: '+name3+' glass mass only')
axs[1].fill_between(USyearly.index, glassmat, modulemat, color='g', alpha=0.3,
                 interpolate=True)

# SCENARIO 4 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name4]+USyearly[keyw+materials[1]+'_'+name4]+
            USyearly[keyw+materials[2]+'_'+name4]+USyearly[keyw+materials[3]+'_'+name4]+
            USyearly[keyw+materials[4]+'_'+name4])
glassmat = (USyearly[keyw+materials[0]+'_'+name4])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[1].plot(USyearly.index, modulemat, 'b.', linewidth=5, label='S4: '+name4+' module mass')
axs[1].plot(USyearly.index, glassmat, 'b', linewidth=5, label='S4: '+name4+' glass mass only')
axs[1].fill_between(USyearly.index, glassmat, modulemat, color='b', alpha=0.3,
                 interpolate=True)

#axs[1].legend()
axs[1].set_title('Yearly Virgin Material Needs by Scenario')
axs[1].set_ylabel('Mass [Million Tonnes]')
axs[1].set_xlim([2020, 2050])
axs[1].set_xlabel('Years')

#### ROW 2
keyw='Waste_EOL_'


# SCENARIO 1 ***************

modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[2].plot(USyearly.index, modulemat, 'k.', linewidth=5, label='S1: '+name0+' module mass')
axs[2].plot(USyearly.index, glassmat, 'k', linewidth=5, label='S1: '+name0+' glass mass only')
axs[2].fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[2].plot(USyearly.index, modulemat, 'c.', linewidth=5, label='S2: '+name2+' module mass')
axs[2].plot(USyearly.index, glassmat, 'c', linewidth=5, label='S2: '+name2+' glass mass only')
axs[2].fill_between(USyearly.index, glassmat, modulemat, color='c', alpha=0.3,
                 interpolate=True)

#axs[0].legend()
axs[2].set_title('Yearly EoL Material by Scenario')
axs[2].set_ylabel('Mass [Million Tonnes]')
axs[2].set_xlim([2020, 2050])
axs[2].set_xlabel('Years')
    
# SCENARIO 3 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name3]+USyearly[keyw+materials[1]+'_'+name3]+
            USyearly[keyw+materials[2]+'_'+name3]+USyearly[keyw+materials[3]+'_'+name3]+
            USyearly[keyw+materials[4]+'_'+name3])
glassmat = (USyearly[keyw+materials[0]+'_'+name3])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[3].plot(USyearly.index, modulemat, 'g.', linewidth=5, label='S2: '+name3+' module mass')
axs[3].plot(USyearly.index, glassmat, 'g', linewidth=5, label='S2: '+name3+' glass mass only')
axs[3].fill_between(USyearly.index, glassmat, modulemat, color='g', alpha=0.3,
                 interpolate=True)



# SCENARIO 4 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name4]+USyearly[keyw+materials[1]+'_'+name4]+
            USyearly[keyw+materials[2]+'_'+name4]+USyearly[keyw+materials[3]+'_'+name4]+
            USyearly[keyw+materials[4]+'_'+name4])
glassmat = (USyearly[keyw+materials[0]+'_'+name4])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[3].plot(USyearly.index, modulemat, 'b.', linewidth=5, label='S4: '+name4+' module mass')
axs[3].plot(USyearly.index, glassmat, 'b', linewidth=5, label='S4: '+name4+' glass mass only')
axs[3].fill_between(USyearly.index, glassmat, modulemat, color='b', alpha=0.3,
                 interpolate=True)

#axs[1].legend()
axs[3].set_title('Yearly EoL Material by Scenario')
axs[3].set_ylabel('Mass [Million Tonnes]')
axs[3].set_xlim([2020, 2050])
axs[3].set_xlabel('Years')



#### ROW 3
keyw='Waste_MFG_'


# SCENARIO 1 ***************

modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[4].plot(USyearly.index, modulemat, 'k.', linewidth=5, label='S1: '+name0+' module mass')
axs[4].plot(USyearly.index, glassmat, 'k', linewidth=5, label='S1: '+name0+' glass mass only')
axs[4].fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
axs[4].plot(USyearly.index, modulemat, 'c.', linewidth=5, label='S2: '+name2+' module mass')
axs[4].plot(USyearly.index, glassmat, 'c', linewidth=5, label='S2: '+name2+' glass mass only')
axs[4].fill_between(USyearly.index, glassmat, modulemat, color='c', alpha=0.3,
                 interpolate=True)

#axs[0].legend()
axs[4].set_title('Yearly Manufacturing Waste by Scenario')
axs[4].set_ylabel('Mass [Million Tonnes]')
axs[4].set_xlim([2020, 2050])
axs[4].set_xlabel('Years')
    


########################    
# SUBPLOT 2
########################
#######################
# Calculate    

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly Virgin Material Needs by Scenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Virgin Needs by 2050 Million Tones by Scenario")


# ### TABLES

# In[ ]:


# 3 sig figs

USyearly3sig = USyearly.copy()
UScum3sig = UScum.copy()
N = 2

UScum3sig = UScum3sig.drop(UScum3sig.index[0])
USyearly3sig = USyearly3sig.drop(USyearly3sig.index[0])

UScum3sig = UScum3sig.loc[:, ~UScum3sig.columns.str.startswith('Waste_MFG_')]
USyearly3sig = USyearly3sig.loc[:, ~USyearly3sig.columns.str.startswith('Waste_MFG_')]

USyearly3sig = USyearly3sig.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
USyearly3sig = USyearly3sig.applymap(lambda x: int(x))

UScum3sig = UScum3sig.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
UScum3sig = UScum3sig.applymap(lambda x: int(x))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


materials = ['Module','glass', 'aluminium_frames', 'copper', 'silicon', 'silver']
scencases = ['_base', '_high']

print(" Appendix Table I: Metric Tonnes Installed in field in 2030")
print(" ########################################################### \n")
#Loop over scenarios
for zz in range(0, len(scencases)):
    scencase = scencases[zz]
    for kk in range (0, len(objects)):
        obj = objects[kk].name
        print("SCENARIO :", obj),      print("~~~~>>>> Case ", scencase)


        print("********************************")
        print("********************************")

        modulemat = 0
        for ii in range(0, len(materials)):
            installedmat = (UScum3sig['VirginStock_'+materials[ii]+'_'+obj+scencase].loc[2030]-
                  UScum3sig['Waste_'+materials[ii]+'_'+obj+'_base'].loc[2030])
            print(materials[ii], ':', round(installedmat/1000)*1000, 'tons')

        print("Capacity in Year 2030 [GW]:", round(UScum3sig['Capacity_'+obj+scencase].loc[2030]/1e9))
        print("Capacity in Year 2050 [GW]:", round(UScum3sig['Capacity_'+obj+scencase].loc[2050]/1e9))
        print("****************************\n")


# In[ ]:


UScum3sig


# In[ ]:


print(" WASTE EoL CUMULATIVE RESULTS [Tonnes] ")
print(" ******************************************")
filter_col = [col for col in UScum3sig if (col.startswith('Waste_EOL_Module')) ]
display(UScum3sig[filter_col].loc[[2016,2020,2030, 2040, 2050]])


# In[ ]:


UScum['Waste_EOL_Module_PV_ICE_base'].iloc[-1]


# In[ ]:


print(" WASTE EoL CUMULATIVE RESULTS [Tonnes] ")
print(" ******************************************")
filter_col = [col for col in UScum if (col.startswith('Waste_EOL_Module')) ]
display(UScum[filter_col].loc[[2016,2020,2030, 2040, 050]])


# ### Bonus: Bifacial Trend Cumulative Virgin Needs (not plotted, just values)

# In[ ]:


name2 = 'bifacialTrend_high'
name0 = 'bifacialTrend_base'

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes
 
print("Cumulative Virgin Needs by 2050 Million Tones by Scenario for Bifacial Trend")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:


name2 = 'Irena_EL_high'
name0 = 'Irena_EL_base'

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes
 
print("Cumulative Virgin Needs by 2050 Million Tones by Scenario for Irena_EL")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:


name2 = 'Irena_RL_high'
name0 = 'Irena_RL_base'

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes
 
print("Cumulative Virgin Needs by 2050 Million Tones by Scenario for Irena_RL")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# ### Waste by year

# In[ ]:





# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})

########################    
# SUBPLOT 1
########################
#######################
   
# loop plotting over scenarios
name2 = 'Simulation1_high'
name0 = 'Simulation1_base'


# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k.', linewidth=5, label='S1: '+name0+' module mass')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='S1: '+name0+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'c.', linewidth=5, label='S2: '+name2+' module mass')
a0.plot(USyearly.index, glassmat, 'c', linewidth=5, label='S2: '+name2+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='c', alpha=0.3,
                 interpolate=True)

a0.legend()
a0.set_title('Yearly Material Waste by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
    
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


## Plot BARS Stuff
ind=np.arange(2)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.set_ylabel('Cumulative Waste by 2050 [Million Tonnes]')
a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))

f.tight_layout()

f.savefig(title_Method+' Fig_2x1_Yearly WASTE by Scenario and Cumulatives_NREL2018.png', dpi=600)

print("Cumulative Waste by 2050 Million Tones by case")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_EOL_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})

########################    
# SUBPLOT 1
########################
#######################
   
# loop plotting over scenarios
name2 = 'Simulation1_high'
name0 = 'Simulation1_base'


# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k.', linewidth=5, label='S1: '+name0+' module mass')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='S1: '+name0+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'c.', linewidth=5, label='S2: '+name2+' module mass')
a0.plot(USyearly.index, glassmat, 'c', linewidth=5, label='S2: '+name2+' glass mass only')
a0.fill_between(USyearly.index, glassmat, modulemat, color='c', alpha=0.3,
                 interpolate=True)

a0.legend()
a0.set_title('Yearly Material Waste by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
    
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']


## Plot BARS Stuff
ind=np.arange(2)
width=0.35 # width of the bars.
p0 = a1.bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a1.bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a1.bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a1.bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a1.bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.set_ylabel('Cumulative EOL Only Waste by 2050 [Million Tonnes]')
a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))

f.tight_layout()

f.savefig(title_Method+' Fig_2x1_Yearly EOL Only WASTE by Scenario and Cumulatives_NREL2018.png', dpi=600)

print("Cumulative Eol Only Waste by 2050 Million Tones by case")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:




