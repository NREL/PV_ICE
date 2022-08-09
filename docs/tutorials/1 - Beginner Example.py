#!/usr/bin/env python
# coding: utf-8

# # 1 - Create Two Scenarios with Two Materials
# 
# 
# This journal shows how to load the baselines and run the dynamic mas flow analysis, plotting the results for two scenarios and two materials.

# ### Step 1: Set Working Folder and Import PV ICE

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


import PV_ICE


# ### Step 2: Add Scenarios and Materials
# 
# ``silicon`` and ``glass`` materials are added to the two simulations, along with a scenario, in this case the ``baseline_modules_US``. The baseline files for decadence scenario will be modified.
# 

# In[3]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='standard', file=r'..\baselines\baseline_modules_US.csv')
rr1.scenario['standard'].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv' )

r1.createScenario('decadence', file=r'..\baselines\baseline_modules_US.csv')
r1.scenario['decadence'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
r1.scenario['decadence'].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')


# ### Step 3: Modify Parameters in the Scenarios
# 
# We have some functions to create changes based on improvements, but for this example we'll just be modifying values for the full column and comparing effects.
# 

# In[4]:


r1.scenario['decadence'].data['mod_lifetime'] = 35
r1.scenario['decadence'].material['glass'].materialdata['mat_virgin_eff'] = 70.0

r1.scenario['decadence'].material['silicon'].materialdata['mat_virgin_eff'] = 80.0
r1.scenario['decadence'].material['silicon'].materialdata['mat_EOL_collected_Recycled'] = 100.0
r1.scenario['decadence'].material['silicon'].materialdata['mat_massperm2'] = 22


# ### Step 4: Run the Mass Flow Calculations on All Scenarios and Materials

# In[5]:


r1.calculateMassFlow()
r1.aggregateResults();


# ### Step 5: Use internal plotting functions to plot results

# Pull out the keywords by printing the keys to the module data or the material data:
# 
#     print(r1.scenario.keys())
#     
#     print(r1.scenario['standard'].data.keys())
#     
#     print(r1.scenario['standard'].material['glass'].materialdata.keys())

# In[6]:


#print(r1.scenario.keys())
#print(r1.scenario['standard'].data.keys())
print(r1.scenario['standard'].material['glass'].materialdata.keys())


# In[8]:


r1.plotScenariosComparison()


# In[ ]:


r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_Total_Landfilled')


# In[ ]:


r1.plotMaterialResults(keyword='VirginStock')


# In[ ]:


r1.plotMetricResults()


# In[ ]:


r1.plotInstalledCapacityResults()


# In[ ]:


datay = r1.USyearly
datac = r1.UScum


# In[ ]:


filter_colc = [col for col in datac if col.startswith('newInstalledCapacity')]
filter_coly = [col for col in datay if col.startswith('Capacity')]


# In[ ]:


datac[filter_colc]


# In[ ]:


data = datac[filter_colc].copy()
data.join(datay[filter_coly].copy())


# In[ ]:


data


# In[ ]:


mylegend = [col.split('_')[1:] for col in data]
mylegend = [col[:-1] for col in mylegend]
mylegend


# In[ ]:


test_list=['standard', 'decadence', '2standard', '2decadence']
test_list2=['asdfadsf', 'dfdffd', 'dfsfs', 'ssssssss']
#str(test_list)[1:-1]
test_list + test_list2


# In[ ]:


test_list


# In[ ]:




