#!/usr/bin/env python
# coding: utf-8

# # PVSC 2021 Paper
# ### Electrification Futures BASE Installations, 
# ### with Module Composition Scenarios for 'TODAY' and 'Bifacial Projection';
# ### RELIABILITY APPROACHES: IRENA EL, IRENA RL, PV ICE
# ### And Bifaciality Factor Considerations PV ICE Same Installs and PV ICE Reduced Installs
# 

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'PVSC')

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper']
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'..\..\baselines\ElectrificationFutures_2021\baseline_modules_US_NREL_Electrification_Futures_2021_basecase.csv'


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


# # Simulation 1: Regular PV ICE

# In[6]:


MATERIALBASELINE_GLASS_TODAY = r'..\..\baselines\PVSC_2021\baseline_material_glass_hold2020.csv'
MATERIALBASELINE_ALFrames_TODAY = r'..\..\baselines\PVSC_2021\baseline_material_aluminium_frames_hold2020.csv'
MATERIALBASELINE_GLASS_BIFACIALPROJECTION = r'..\..\baselines\PVSC_2021\baseline_material_glass_bifacialTrend.csv'
MATERIALBASELINE_ALFrames_BIFACIALPROJECTION = r'..\..\baselines\PVSC_2021\baseline_material_aluminium_frames_bifacialTrend.csv'


# In[7]:


r1 = PV_ICE.Simulation(name='PV_ICE', path=testfolder)

r1.createScenario(name='Today', file=MODULEBASELINE)
r1.scenario['Today'].addMaterial('glass', file=MATERIALBASELINE_GLASS_TODAY)
r1.scenario['Today'].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_TODAY)
for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r1.scenario['Today'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)
    
r1.createScenario(name='Bifacial', file=MODULEBASELINE)
r1.scenario['Bifacial'].addMaterial('glass', file=MATERIALBASELINE_GLASS_BIFACIALPROJECTION)
r1.scenario['Bifacial'].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_BIFACIALPROJECTION)
for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r1.scenario['Bifacial'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)


# In[8]:


MATERIALBASELINE_Mono = r'..\..\baselines\PVSC_2021\baseline_modules_US_ITRPVPrediction_monofacialModules.csv'
MATERIALBASELINE_Bifi = r'..\..\baselines\PVSC_2021\baseline_modules_US_ITRPVPrediction_bifacialModules.csv'
bifacialityfactors = r'..\..\baselines\baseline_bifaciality_factor.csv'

r0a = PV_ICE.Simulation(name='Mono', path=testfolder)

r0a.createScenario(name='Bifacial', file=MATERIALBASELINE_Mono)
r0a.scenario['Bifacial'].addMaterial('glass', file=MATERIALBASELINE_GLASS_TODAY)
r0a.scenario['Bifacial'].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_TODAY)
for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r0a.scenario['Bifacial'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)

r0b = PV_ICE.Simulation(name='Bifacial_ReducedInstalls', path=testfolder)

r0b.createScenario(name='Bifacial', file=MATERIALBASELINE_Bifi)
r0b.scenario['Bifacial'].addMaterial('glass', file=MATERIALBASELINE_GLASS_BIFACIALPROJECTION)
r0b.scenario['Bifacial'].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_BIFACIALPROJECTION)
for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r0b.scenario['Bifacial'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)


# In[9]:


r0c = PV_ICE.Simulation(name='Bifacial_SameInstalls', path=testfolder)

r0c.createScenario(name='Bifacial', file=MATERIALBASELINE_Bifi)
r0c.scenario['Bifacial'].addMaterial('glass', file=MATERIALBASELINE_GLASS_BIFACIALPROJECTION)
r0c.scenario['Bifacial'].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_BIFACIALPROJECTION)
for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r0c.scenario['Bifacial'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)


# In[10]:


# BifacialProjection.Bifacial --> now "Bifacial_ReducedInstalls.Bifacial"
# BifacialProjection.Mono --> now 'Mono.Bifacial'
# SameInstalls.Bifacial_SameInstalls --> now Bifacial_SameInstalls.Bifacial"


# In[11]:


# Irena EL 
r2 = PV_ICE.Simulation(name='Irena_EL', path=testfolder)

r2.createScenario(name='Today', file=MODULEBASELINE)
r2.scenario['Today'].data['mod_lifetime'] = 40
r2.scenario['Today'].data['mod_MFG_eff'] = 100.0

r2.scenario['Today'].addMaterial('glass', file=MATERIALBASELINE_GLASS_TODAY)
r2.scenario['Today'].material['glass'].materialdata['mat_MFG_eff'] = 100.0   
r2.scenario['Today'].material['glass'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

r2.scenario['Today'].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_TODAY)
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

r2.scenario['Bifacial'].addMaterial('glass', file=MATERIALBASELINE_GLASS_BIFACIALPROJECTION)
r2.scenario['Bifacial'].material['glass'].materialdata['mat_MFG_eff'] = 100.0   
r2.scenario['Bifacial'].material['glass'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

r2.scenario['Bifacial'].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_BIFACIALPROJECTION)
r2.scenario['Bifacial'].material['aluminium_frames'].materialdata['mat_MFG_eff'] = 100.0   
r2.scenario['Bifacial'].material['aluminium_frames'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r2.scenario['Bifacial'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)
    r2.scenario['Bifacial'].material[MATERIALS[mat]].materialdata['mat_MFG_eff'] = 100.0   
    r2.scenario['Bifacial'].material[MATERIALS[mat]].materialdata['mat_MFG_scrap_Recycled'] = 0.0   


# In[12]:


# Irena RL
r3 = PV_ICE.Simulation(name='Irena_RL', path=testfolder)

r3.createScenario(name='Today', file=MODULEBASELINE)
r3.scenario['Today'].data['mod_lifetime'] = 40
r3.scenario['Today'].data['mod_MFG_eff'] = 100.0

r3.scenario['Today'].addMaterial('glass', file=MATERIALBASELINE_GLASS_TODAY)
r3.scenario['Today'].material['glass'].materialdata['mat_MFG_eff'] = 100.0   
r3.scenario['Today'].material['glass'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

r3.scenario['Today'].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_TODAY)
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

r3.scenario['Bifacial'].addMaterial('glass', file=MATERIALBASELINE_GLASS_BIFACIALPROJECTION)
r3.scenario['Bifacial'].material['glass'].materialdata['mat_MFG_eff'] = 100.0   
r3.scenario['Bifacial'].material['glass'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

r3.scenario['Bifacial'].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_BIFACIALPROJECTION)
r3.scenario['Bifacial'].material['aluminium_frames'].materialdata['mat_MFG_eff'] = 100.0   
r3.scenario['Bifacial'].material['aluminium_frames'].materialdata['mat_MFG_scrap_Recycled'] = 0.0 

for mat in range (2, len(MATERIALS)):
    MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r3.scenario['Bifacial'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)
    r3.scenario['Bifacial'].material[MATERIALS[mat]].materialdata['mat_MFG_eff'] = 100.0   
    r3.scenario['Bifacial'].material[MATERIALS[mat]].materialdata['mat_MFG_scrap_Recycled'] = 0.0
    


# # Run Simulations 

# In[13]:


r0a.calculateMassFlow() # Mono.Bifacial
r0b.calculateMassFlow(bifacialityfactors=bifacialityfactors) #  Bifacial_ReducedInstalls.Bifacial
r0c.calculateMassFlow(bifacialityfactors=bifacialityfactors, reducecapacity=False) # Bifacial_SameInstalls.Bifacial
r1.calculateMassFlow()


# In[14]:


weibullInputParams = {'alpha': 2.49, 'beta':30}  # Early-loss scenario IRENA
r2.calculateMassFlow(weibullInputParams=weibullInputParams)

weibullInputParams = {'alpha': 5.3759, 'beta':30}  # Regular-loss scenario IRENA
r3.calculateMassFlow(weibullInputParams=weibullInputParams)


# ## Creating Summary of results 
# 

# In[15]:


Simulations = [r0a, r0b, r0c, r1, r2, r3]


# In[16]:


USyearly=pd.DataFrame()


# In[17]:


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


# In[18]:


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


# In[19]:


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


# In[20]:


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


# ### Converting to grams to METRIC Tons. 
# 

# In[21]:


USyearly = USyearly/1000000  # This is the ratio for Metric tonnes
#907185 -- this is for US tons


# ### Adding NEW Installed Capacity to US

# In[22]:


keyword='new_Installed_Capacity_[MW]'

# Loop over objects
for kk in range(0, len(Simulations)):
    obj = Simulations[kk]
    newcolname = keyword+'_'+obj.name
    
    if newcolname in USyearly:
        USyearly[newcolname] = USyearly[newcolname]+obj.scenario[list(obj.scenario.keys())[0]].data[keyword]
    else:
        USyearly[keyword+'_'+obj.name] = obj.scenario[list(obj.scenario.keys())[0]].data[keyword]

USyearly.head(10)


# # Combining BifacialProjection

# In[23]:


filter_col_Bifacial_ReducedInstalls = [col for col in USyearly if col.endswith('Bifacial_ReducedInstalls_Bifacial')]
filter_col_Mono = [col for col in USyearly if col.endswith('Mono_Bifacial')]
filter_col_Bifacial_SameInstalls = [col for col in USyearly if col.endswith('Bifacial_SameInstalls_Bifacial')]


# In[24]:


new_col_titles = filter_col_Bifacial_ReducedInstalls.copy()
new_col_titles = [x[:-9] for x in new_col_titles]
df_Bifacial_ReducedInstalls = pd.DataFrame(USyearly[filter_col_Bifacial_ReducedInstalls].values + USyearly[filter_col_Mono].values, columns=new_col_titles)
USyearly = pd.concat([USyearly, df_Bifacial_ReducedInstalls], axis=1)
USyearly = USyearly[USyearly.columns.drop(filter_col_Bifacial_ReducedInstalls)]


# In[25]:


new_col_titles = filter_col_Bifacial_SameInstalls.copy()
new_col_titles = [x[:-9] for x in new_col_titles]
df_Bifacial_SameInstalls = pd.DataFrame(USyearly[filter_col_Bifacial_SameInstalls].values + USyearly[filter_col_Mono].values, columns=new_col_titles)
USyearly = pd.concat([USyearly, df_Bifacial_SameInstalls], axis=1)
USyearly = USyearly[USyearly.columns.drop(filter_col_Bifacial_SameInstalls)]


# In[26]:


USyearly = USyearly[USyearly.columns.drop(filter_col_Mono)]


# ### Creating Cuulatives 

# In[27]:


UScum = USyearly.copy()
UScum = UScum.cumsum()
UScum.head()


# ### Adding Installed Capacity to US

# In[28]:


keyword='Installed_Capacity_[W]'

# Loop over objects
for kk in range(0, len(Simulations)):
    obj = Simulations[kk]

    # Loop over Scenarios
    for jj in range(0, len(obj.scenario)):
        case = list(obj.scenario.keys())[jj]
        foo = obj.scenario[case].data[keyword]
        foo = foo.to_frame(name=keyword)
        UScum["Capacity_"+obj.name+'_'+case] = foo[keyword]
        
        


# In[29]:


UScum['Capacity_Bifacial_ReducedInstalls'] = UScum['Capacity_Mono_Bifacial'] + UScum['Capacity_Bifacial_ReducedInstalls_Bifacial']
UScum['Capacity_Bifacial_SameInstalls'] = UScum['Capacity_Mono_Bifacial'] + UScum['Capacity_Bifacial_SameInstalls_Bifacial']


# In[30]:


UScum = UScum[UScum.columns.drop(['Capacity_Mono_Bifacial','Capacity_Bifacial_ReducedInstalls_Bifacial', 'Capacity_Bifacial_SameInstalls_Bifacial'])]


# ### Reindexing

# In[31]:


USyearly.index = r1.scenario['Today'].data['year']
UScum.index = r1.scenario['Today'].data['year']


# In[32]:


UScum.tail(5)


# In[33]:


UScum.to_csv('Cumulative_Results.csv')
USyearly.to_csv('Yearly_Results.csv')


# In[ ]:





# ## Mining Capacity

# In[34]:


mining2020_aluminum = 65267000
mining2020_silver = 22260
mining2020_copper = 20000000
mining2020_silicon = 8000000


# # PLOTTING GALORE

# In[35]:


list(USyearly.keys())


# In[ ]:





# In[36]:


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


# In[37]:


bifacial_foo = USyearly[keyw+materials[4]+'_'+name0].iloc[-1]*100/mining2020_aluminum
today_foo = USyearly[keyw+materials[4]+'_'+name2].iloc[-1]*100/mining2020_aluminum
print(today_foo)
print(bifacial_foo)
print("In Year 2050, AL Needs Ratio to Mining Supply REDUCTION Of ", (today_foo-bifacial_foo)*100/today_foo-bifacial_foo)


# In[38]:


bifacial_foo = USyearly[keyw+materials[4]+'_'+name0].sum()*100/mining2020_aluminum
today_foo = USyearly[keyw+materials[4]+'_'+name2].sum()*100/mining2020_aluminum
print(today_foo)
print(bifacial_foo)
print("Cumulative 2020-2050 AL Needs Ratio to Mining Supply REDUCTION Of ", (today_foo-bifacial_foo)*100/today_foo-bifacial_foo)


# In[39]:


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


# In[40]:


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

# In[41]:


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


# In[42]:


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


# In[43]:


list(USyearly.keys())


# In[44]:



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
#name3 = 'BifacialProjection'

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

'''
# SCENARIO 3 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name3]+USyearly[keyw+materials[1]+'_'+name3]+
            USyearly[keyw+materials[2]+'_'+name3]+USyearly[keyw+materials[3]+'_'+name3]+
            USyearly[keyw+materials[4]+'_'+name3])
glassmat = (USyearly[keyw+materials[0]+'_'+name3])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'g', linestyle='dotted', linewidth=5, label='Bifacial Evolution: module')
a0.plot(USyearly.index, glassmat, 'g', linewidth=5, label='Bifacial Evolution: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

'''

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
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n'], color='black', rotation=45)
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


# In[45]:


# PLOT FOR PAPER 


plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_EOL_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


#f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2,0.8,0.8]})
f, (a0, a1, a2) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [0.5,0.25,0.25]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name0 = 'PV_ICE_Today'
name2 = 'PV_ICE_Bifacial'
#name3 = 'BifacialProjection'

# SCENARIO 1 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name0]+USyearly[keyw+materials[1]+'_'+name0]+
            USyearly[keyw+materials[2]+'_'+name0]+USyearly[keyw+materials[3]+'_'+name0]+
            USyearly[keyw+materials[4]+'_'+name0])
glassmat = (USyearly[keyw+materials[0]+'_'+name0])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'k', linestyle='dotted', linewidth=5, label='Current tech: module')
a0.plot(USyearly.index, glassmat, 'k', linewidth=5, label='Current tech: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='k', alpha=0.3,
                 interpolate=True)

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Incrased bifacial: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Incrased bifacial: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

'''
# SCENARIO 3 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name3]+USyearly[keyw+materials[1]+'_'+name3]+
            USyearly[keyw+materials[2]+'_'+name3]+USyearly[keyw+materials[3]+'_'+name3]+
            USyearly[keyw+materials[4]+'_'+name3])
glassmat = (USyearly[keyw+materials[0]+'_'+name3])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'g', linestyle='dotted', linewidth=5, label='Incrased bifacial: module')
a0.plot(USyearly.index, glassmat, 'g', linewidth=5, label='Bifacial Evolution: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

'''

#a0.title('Yearly')

a0.legend(loc=2)
a0.set_title('Yearly')
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

#a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
a1.yaxis.set_ticklabels([]) 
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n'], color='black', rotation=45, fontsize=17)
plt.tick_params(axis='y', which='minor', bottom=False)
plt.title('Current Tech')



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
a2.set_ylabel('Cumulative End of Life Material \nby 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a2.set_xticks(ind, ('S1', 'S2'))
#plt.yticks(np.arange(0, 81, 10))
a2.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'),
          bbox_to_anchor=(1.2, -0.25),
          fancybox=True, shadow=True, ncol=5)
a2.set_ylim([0, 28])

plt.sca(a2)
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'High\nElec.'], color='black', rotation=45, fontsize=17)
plt.tick_params(axis='y', which='minor', bottom=False)
plt.title('Increased bifacial')

f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# # Waste_ EOL + MFG

# In[ ]:





# In[ ]:





# In[46]:


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


# In[47]:


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


# In[48]:


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
#name3 = 'BifacialProjection'

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
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'Bifacial'], color='black', rotation=45)
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
plt.xticks(range(3), ['Irena\nEarly Loss', 'Irena\nRegular Loss', 'PV ICE\n', 'BIFACIAL.'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


f.tight_layout()

fig.savefig(os.path.join(testfolder,'Fig_2x1_Yearly EoL Waste by SCenario and Cumulatives_NREL2018.png'), dpi=600)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[49]:


USyearly.keys()


# # BIFACIAL PROJECTION COMPARISON

# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2,0.8]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name2 = 'Bifacial_SameInstalls'
name3 = 'Bifacial_ReducedInstalls'

# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Same Installs: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Same Installs: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

# SCENARIO 3 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name3]+USyearly[keyw+materials[1]+'_'+name3]+
            USyearly[keyw+materials[2]+'_'+name3]+USyearly[keyw+materials[3]+'_'+name3]+
            USyearly[keyw+materials[4]+'_'+name3])
glassmat = (USyearly[keyw+materials[0]+'_'+name3])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'gold', linestyle='dotted', linewidth=5, label='Reduced Installs: module')
a0.plot(USyearly.index, glassmat, 'gold', linewidth=5, label='Reduced Installs: glass')
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
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name3].loc[2050])
    empty = 0
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
#a1.yaxis.set_ticklabels([]) 

a1.set_ylabel('Cumulative End of Life Material and MFG Scrap \n by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#a1.yaxis.set_ticklabels([]) 
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
#a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(2), ['Same\n Installs\n', 'Reduced\n Installs'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
change = dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:


print("Reduced Installs reduces EOL Material & MFG Scrap landfilled by {} % ".format(round((change[0] - change[1])*100/change[0],2)))


# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='VirginStock_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2,0.8]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name2 = 'Bifacial_SameInstalls'
name3 = 'Bifacial_ReducedInstalls'


# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Same Installs: module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Same Installs: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

# SCENARIO 3 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name3]+USyearly[keyw+materials[1]+'_'+name3]+
            USyearly[keyw+materials[2]+'_'+name3]+USyearly[keyw+materials[3]+'_'+name3]+
            USyearly[keyw+materials[4]+'_'+name3])
glassmat = (USyearly[keyw+materials[0]+'_'+name3])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'gold', linestyle='dotted', linewidth=5, label='Reduced Installs: module')
a0.plot(USyearly.index, glassmat, 'gold', linewidth=5, label='Reduced Installs: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)


a0.legend(loc=2)
#a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
#a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name3].loc[2050])
    empty = 0
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
#a1.yaxis.set_ticklabels([]) 

a1.set_ylabel('Cumulative Virgin Stock Needs [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#a1.yaxis.set_ticklabels([]) 
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
#a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(2), ['Same\n Installs\n', 'Reduced\n Installs'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)


print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
change1 = dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:


print("Reduction in Manufacturing needs for Reduced Installs of {} %".format(round((change1[0]-change1[1])*100/change1[0],2)))


# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)
keyw='VirginStock_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2,0.8]})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name2 = 'Bifacial_SameInstalls'
name3 = 'Bifacial_ReducedInstalls'


# SCENARIO 2 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name2]+USyearly[keyw+materials[1]+'_'+name2]+
            USyearly[keyw+materials[2]+'_'+name2]+USyearly[keyw+materials[3]+'_'+name2]+
            USyearly[keyw+materials[4]+'_'+name2])
glassmat = (USyearly[keyw+materials[0]+'_'+name2])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'lightcoral', linestyle='dotted', linewidth=5, label='Irena Installs (no MFG losses): module')
a0.plot(USyearly.index, glassmat, 'lightcoral', linewidth=5, label='Irena Installs (no MFG losses):: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)

# SCENARIO 3 ***************
modulemat = (USyearly[keyw+materials[0]+'_'+name3]+USyearly[keyw+materials[1]+'_'+name3]+
            USyearly[keyw+materials[2]+'_'+name3]+USyearly[keyw+materials[3]+'_'+name3]+
            USyearly[keyw+materials[4]+'_'+name3])
glassmat = (USyearly[keyw+materials[0]+'_'+name3])
modulemat = modulemat/1000000
glassmat = glassmat/1000000 
a0.plot(USyearly.index, modulemat, 'gold', linestyle='dotted', linewidth=5, label='Reduced Installs: module')
a0.plot(USyearly.index, glassmat, 'gold', linewidth=5, label='Reduced Installs: glass')
a0.fill_between(USyearly.index, glassmat, modulemat, color='lightcoral', alpha=0.3,
                 interpolate=True)


a0.legend(loc=2)
#a0.set_title('Yearly End of Life Material by Scenario')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([2020, 2050])
a0.set_xlabel('Years')
#a0.set_ylim([0, 1.8])
    
########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name3].loc[2050])
    empty = 0
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
#a1.yaxis.set_ticklabels([]) 

a1.set_ylabel('Cumulative End of Life Material by 2050 [Million Tonnes]')
#a1.set_xlabel('Scenario')
a1.set_xticks(ind, ('S1', 'S2'))
#a1.yaxis.set_ticklabels([]) 
#plt.yticks(np.arange(0, 81, 10))
#a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0] ), ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver'))
#a1.set_ylim([0, 28])


plt.sca(a1)
plt.xticks(range(2), ['\n Irena Installs \n(no MFG losses)) \n', 'Reduced\n Installs'], color='black', rotation=45)
plt.tick_params(axis='y', which='minor', bottom=False)

print("Cumulative Waste by EoL 2050 Million Tones by Scenario")
change2 = dfcumulations2050[['glass','silicon','silver','copper','aluminium_frames']].sum(axis=1)


# In[ ]:


print("Manufacturing Loss represents {} % of Virgin Stock Needs ".format(round((change1[0]-change2[0])*100/change1[0],2)))


# # Installed Capacity

# In[ ]:


filter_col_Capacity = [col for col in UScum if col.startswith('Capacity')]
filter_col_Capacity


# In[ ]:


UScum[filter_col_Capacity].loc[2050]/1e12


# In[ ]:


# Sanity Check
plt.plot(UScum['Capacity_Irena_EL_Today']/1e12, 'r', linewidth=4.0, label='Irena Early Loss')
plt.plot(UScum['Capacity_Irena_EL_Bifacial']/1e12, 'b.', linewidth=4.0, label='Irena Regular Loss')
print("No difference in Capacity between Today and Bifacial for Irena", sum(UScum['Capacity_Irena_EL_Today']/1e12-UScum['Capacity_Irena_EL_Bifacial']/1e12))


# In[ ]:


"""
p1 = (UScum['new_Installed_Capacity_[MW]BifacialProjection']-
UScum['new_Installed_Capacity_[MW]BifacialProjection_p2'])

UScum['new_Installed_Capacity_[MW]SameInstalls_p2'] = UScum['new_Installed_Capacity_[MW]SameInstalls'] + p1

""" 
pass


# In[ ]:





# In[ ]:


filter_col_newInstalls = [col for col in UScum if col.startswith('new_Installed_Capacity_[MW]')]
UScum[filter_col_newInstalls].loc[2050]/1e6


# In[ ]:


list(UScum.keys())


# In[ ]:





# In[ ]:





# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (7.5, 8)
keyw='Waste_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']

f, (a0) = plt.subplots(1, 1, gridspec_kw={'width_ratios': [2]})

plt.plot(UScum['new_Installed_Capacity_[MW]_Irena_EL']/1e6, 'k', label='Cumulative New Installs')
plt.plot(UScum['Capacity_Irena_EL_Bifacial']/1e12, 'r', linewidth=4.0, label='Irena EL Reliability')
plt.plot(UScum['Capacity_Irena_RL_Bifacial']/1e12, 'g', linewidth=4.0, label='Irena RL Reliability')#
plt.plot(UScum['Capacity_Bifacial_ReducedInstalls']/1e12, 'gold', linestyle='dashed', linewidth=4.0, label='PV ICE Reduced Installs')
plt.plot(UScum['Capacity_Bifacial_SameInstalls']/1e12, 'lightcoral', linewidth=4.0, label='PV ICE Reliability')

plt.legend()
#plt.yscale('log')
plt.xlim([2020, 2050])
#plt.ylim([5e10, 1e12])
plt.ylabel('Installed Capacity [TW]')


# In[ ]:


print("Nameplate Capcaity of Bifacial Installations augment by", (UScum['Capacity_Bifacial_SameInstalls'][2050]-UScum['Capacity_Bifacial_ReducedInstalls'][2050])*100/UScum['Capacity_Bifacial_SameInstalls'][2050])


# In[ ]:


print("% loss with Irena EL ")
((UScum['new_Installed_Capacity_[MW]_Irena_EL'].loc[2050]/1e6)-(UScum['Capacity_Irena_EL_Bifacial'].loc[2050]/1e12))*100/(UScum['new_Installed_Capacity_[MW]_Irena_EL'].loc[2050]/1e6)


# In[ ]:


print("% loss with Irena RL ")
((UScum['new_Installed_Capacity_[MW]_Irena_RL'].loc[2050]/1e6)-(UScum['Capacity_Irena_RL_Bifacial'].loc[2050]/1e12))*100/(UScum['new_Installed_Capacity_[MW]_Irena_RL'].loc[2050]/1e6)


# In[ ]:


print("% loss with PV ICE, Reducing Bifacial Installs ")
((UScum['new_Installed_Capacity_[MW]_Irena_RL'].loc[2050]/1e6)-(UScum['Capacity_Bifacial_ReducedInstalls'].loc[2050]/1e12))*100/(UScum['new_Installed_Capacity_[MW]_Irena_RL'].loc[2050]/1e6)


# In[ ]:


print("% loss with PV ICE, Keeping Bifacial Installs ")
((UScum['new_Installed_Capacity_[MW]_Irena_RL'].loc[2050]/1e6)-(UScum['Capacity_Bifacial_SameInstalls'].loc[2050]/1e12))*100/(UScum['new_Installed_Capacity_[MW]_Irena_RL'].loc[2050]/1e6)


# In[ ]:





# # WEIBULL PLOTS

# In[ ]:


from matplotlib.pyplot import gca,show


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


# # SAVE RESULTS OPENEI

# In[ ]:


# WORK ON THIS FOIR OPENEI

keyw=['mat_Virgin_Stock','mat_Total_EOL_Landfilled','mat_Total_MFG_Landfilled', 'mat_Total_Landfilled', 
      'new_Installed_Capacity_[MW]','Installed_Capacity_[W]']
keywprint = ['VirginMaterialDemand','EOLMaterial', 'ManufacturingScrap','ManufacturingScrapAndEOLMaterial',
             'NewInstalledCapacity','InstalledCapacity'] 
keywunits = ['MetricTonnes', 'MetricTonnes', 'MetricTonnes', 'MetricTonnes', 
            'MW','MW']
keywdcumneed = [True,True,True,True,
                True,False]
keywdlevel = ['material','material','material','material',
             'module','module']
keywscale = [1000000, 1000000, 1000000, 1000000,
            1,1e6]
#materials = ['glass', 'silicon', 'silver', 'copper', 'aluminum']
materials = ['glass','aluminium_frames','silver','silicon', 'copper']

# Loop over SF Scenarios

scenariolist = pd.DataFrame()

# Loop over Simularionts r1 r2, r3... 
for kk in range(3, len(Simulations)):
    obj = Simulations[kk]

    # Loop over Scenarios
    for zz in range(0, len(obj.scenario)):
        case = list(obj.scenario.keys())[zz]
        
        foo = pd.DataFrame()
        for jj in range (0, len(keyw)):

            if keywdlevel[jj] == 'material':
                for ii in range (0, len(materials)):    
                    sentit = '@value|'+keywprint[jj]+'|'+materials[ii].capitalize() +'#'+keywunits[jj]
                    foo[sentit] = obj.scenario[case].material[materials[ii]].materialdata[keyw[jj]]/keywscale[jj] 
            
            else:
                sentit = '@value|'+keywprint[jj]+'|'+'PV' +'#'+keywunits[jj]
                #sentit = '@value|'+keywprint[jj]+'#'+keywunits[jj]
                foo[sentit] = obj.scenario[case].data[keyw[jj]]/keywscale[jj] 



        foo['@case'] = case
        foo['@scenario|Module Composition'] = obj.name
        foo['@timeseries|Year'] = obj.scenario[case].data.year

        scenariolist = scenariolist.append(foo)   

cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
#scenariolist = scenariolist/1000000 # Converting to Metric Tons
#scenariolist = scenariolist.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
#scenariolist = scenariolist.applymap(lambda x: int(x))
scenariolist.to_csv('OPENEI 4 - Nation by Year.csv', index=False)

print("Done")


# ### UNFINISHED FOR OPENEI STARTING HERE

# In[ ]:





# In[ ]:


ReliabilityApproach=['Irena_RL', 'Irena_EL', 'PV_ICE', 'Bifacial_ReducedInstalls', 'Bifacial_SameInstalls']

ReliabilityApproachandScenario=['Irena_RL_Today', 'Irena_RL_Bifacial',
                                'Irena_EL_Today', 'Irena_EL_Bifacial',
                                'PV_ICE_Today','PV_ICE_Today', 
                                'Bifacial_ReducedInstalls', 
                                'Bifacial_SameInstalls']
TodayModuleComposition = ['Irena_RL_Today', 'Irena_EL_Today', 'PV_ICE_Today']
BifacialModuleComposition = ['Irena_RL_Bifacial', 'Irena_EL_Bifacial', 'Bifacial_SameInstalls', 'Bifacial_ReducedInstalls']


# In[ ]:


# WORK ON THIS FOIR OPENEI

keyw=['VirginStock','Waste_EOL','Waste_MFG', 'Waste', 
      'new_Installed_Capacity_[MW]','Capacity']
keywprint = ['VirginMaterialDemand','EOLMaterial', 'ManufacturingScrap','ManufacturingScrapAndEOLMaterial',
             'NewInstalledCapacity','InstalledCapacity'] 
keywunits = ['MetricTonnes', 'MetricTonnes', 'MetricTonnes', 'MetricTonnes', 
            'MW','MW']
keywdcumneed = [True,True,True,True,
                True,False]
keywdlevel = ['material','material','material','material',
             'module','module']
keywscale = [1000000, 1000000, 1000000, 1000000,
            1,1e6]
#materials = ['glass', 'silicon', 'silver', 'copper', 'aluminum']
materials = ['glass','aluminium_frames','silver','silicon', 'copper','Module']

# Loop over SF Scenarios

scenariolist = pd.DataFrame()

# Loop over Simularionts r1 r2, r3... 
for kk in range(3, len(TodayModuleComposition)):
    obj = Simulations[kk]

        
        foo = pd.DataFrame()
        for jj in range (0, len(keyw)):

            if keywdlevel[jj] == 'material':
                for ii in range (0, len(materials)):    
                    sentit = '@value|'+keywprint[jj]+'|'+materials[ii].capitalize() +'#'+keywunits[jj]
                    foo[sentit] = obj.scenario[case].material[materials[ii]].materialdata[keyw[jj]]/keywscale[jj] 
            
            else:
                sentit = '@value|'+keywprint[jj]+'|'+'PV' +'#'+keywunits[jj]
                #sentit = '@value|'+keywprint[jj]+'#'+keywunits[jj]
                foo[sentit] = obj.scenario[case].data[keyw[jj]]/keywscale[jj] 



        foo['@case'] = case
        foo['@scenario|Solar Futures'] = obj.name
        foo['@timeseries|Year'] = obj.scenario[case].data.year

        scenariolist = scenariolist.append(foo)   

cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
#scenariolist = scenariolist/1000000 # Converting to Metric Tons
#scenariolist = scenariolist.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
#scenariolist = scenariolist.applymap(lambda x: int(x))
scenariolist.to_csv('OPENEI 4 - Nation by Year.csv', index=False)

print("Done")


# In[ ]:


"""
colNames = result.columns[result.columns.str.contains('|ManufacturingScrap|')] 
result['@value|ManufacturingScrap|Module#MetricTonnes'] = result[colNames].sum(axis=1)

mask = df1['@scenario|Solar Futures']=='SameInstalls'
df1 = df1[~mask]

df1.rename(columns={'@scenario|Solar Futures': '@scenario|Module Composition Scenario'}, inplace=True)

"""


# @scenario   @ timeseries    @ value|VirginMateiralDemand|Glass#MEtric Tonnes ........
# PVV_ICE             2020
# PV_ICE               2030

# In[ ]:




