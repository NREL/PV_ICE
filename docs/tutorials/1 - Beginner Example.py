#!/usr/bin/env python
# coding: utf-8

# # 1 - Create Two Scenarios with Two Materials
# 
# 
# This journal shows how to load the baselines and run the dynamic mas flow analysis, plotting the results for two scenarios and two materials.

# ### Step 1: Set Working Folder and Import PV DEMISE

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_DEMICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


import PV_DEMICE


# ### Step 2: Add Scenarios and Materials
# 
# ``silicon`` is just a demonstration name at the moment, we'll be using the same file for glass and modifying it to see the plotting.
# 

# In[3]:


r1 = PV_DEMICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='standard', file=r'..\baselines\baseline_modules_US.csv')
r1.scenario['standard'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
r1.scenario['standard'].addMaterial('silicon', file=r'..\baselines\baseline_material_glass.csv' )

r1.createScenario('decadence', file=r'..\baselines\baseline_modules_US.csv')
r1.scenario['decadence'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
r1.scenario['decadence'].addMaterial('silicon', file=r'..\baselines\baseline_material_glass.csv')


# ### Step 3: Modify Parameters in the Scenarios
# 
# We have some functions to create changes based on improements, but for this example we'll just be modifying values for the full column and comparing effects.
# 

# In[4]:


r1.scenario['standard'].material['silicon'].materialdata['mat_virgin_eff'] = 30.0
r1.scenario['standard'].material['silicon'].materialdata['mat_EOL_collected_Recycled'] = 40.0
r1.scenario['standard'].material['silicon'].materialdata['mat_massperm2'] = 4


r1.scenario['decadence'].data['mod_lifetime'] = 35
r1.scenario['decadence'].material['glass'].materialdata['mat_virgin_eff'] = 70.0

r1.scenario['decadence'].material['silicon'].materialdata['mat_virgin_eff'] = 80.0
r1.scenario['decadence'].material['silicon'].materialdata['mat_EOL_collected_Recycled'] = 100.0
r1.scenario['decadence'].material['silicon'].materialdata['mat_massperm2'] = 22


# ### Step 4: Run the Mass Flow Calculations on All Scenarios and Materials

# In[5]:


r1.calculateMassFlow()


# ### Step 5: Use internal plotting functions to plot results

# In[6]:


r1.plotScenariosComparison(keyword='Cumulative_Area_disposedby_Failure')


# In[7]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_EoL_Recycled_into_HQ')


# In[ ]:




