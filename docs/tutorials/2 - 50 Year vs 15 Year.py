#!/usr/bin/env python
# coding: utf-8

# # 2 - 50 Year vs 15 Year Module
# 
# Comparison case using the functions in CE-MFC to compare 15 year module reliability vs 50 year module reliability.

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_DEMICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


import PV_DEMICE


# In[3]:


import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[4]:


r1 = PV_DEMICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='50_Year_Module', file=r'..\baselines\baseline_modules_US.csv')
r1.scenario['50_Year_Module'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
r1.scenario['50_Year_Module'].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')

r1.createScenario(name='15_Year_Module', file=r'..\baselines\baseline_modules_US.csv')
r1.scenario['15_Year_Module'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
r1.scenario['15_Year_Module'].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')


# In[5]:


r1.scenario['50_Year_Module'].data.keys()


# In[6]:


r1.scenario['50_Year_Module'].data['mod_reliability_t50'] = 50
r1.scenario['50_Year_Module'].data['mod_reliability_t90'] = 60
r1.scenario['50_Year_Module'].data['mod_lifetime'] = 50

r1.scenario['15_Year_Module'].data['mod_reliability_t50'] = 15
r1.scenario['15_Year_Module'].data['mod_reliability_t90'] = 25
r1.scenario['15_Year_Module'].data['mod_lifetime'] = 15


# In[7]:


r1.calculateMassFlow()


# In[8]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_Total_Landfilled')


# In[10]:


r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_Total_Landfilled')


# In[9]:


r1.plotScenariosComparison(keyword='Installed_Capacity_[W]')


# ### Modifying Installed Capacity requirements to match 50 Year Module

# In[11]:


r1.createScenario(name='15_Year_Module_IncreasedInstalls', file=r'..\baselines\baseline_modules_US.csv')
r1.scenario['15_Year_Module_IncreasedInstalls'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
r1.scenario['15_Year_Module_IncreasedInstalls'].data['mod_reliability_t50'] = 15
r1.scenario['15_Year_Module_IncreasedInstalls'].data['mod_reliability_t90'] = 25
r1.scenario['15_Year_Module_IncreasedInstalls'].data['mod_lifetime'] = 15

r1.calculateMassFlow()


# In[12]:


# Modifing the installed capacity requiremetns according to t50. 
# Needs to run each year becuase it needs to calculate the acumulated installs and deads.

Under_Installment = []
for i in range (0, len(r1.scenario['50_Year_Module'].data)):
    Under_Installment = ( (r1.scenario['50_Year_Module'].data['Installed_Capacity_[W]'][i] - 
                         r1.scenario['15_Year_Module_IncreasedInstalls'].data['Installed_Capacity_[W]'][i])/1000000 )  # MWATTS
    r1.scenario['15_Year_Module_IncreasedInstalls'].data['new_Installed_Capacity_[MW]'][i] += Under_Installment
    r1.calculateMassFlow()


# In[13]:


r1.plotScenariosComparison(keyword='Installed_Capacity_[W]')


# ### No Deaths Allowed Scenario

# ## SCENARIO: Modification of 15-year for high recycling

# This scenario is a though experiment comparing a 15-year 95% recyclable module versus a 50-year module 30% recyclable module.
# This is done to understand potential tradeoffs in PV technology evolution - is it better to create
# a completely recyclable PV panel, or to extend the module lifetime.
# This scenario assumes that the 15-year module is 95% recyclable into high quality material, i.e. it will be used to create new modules.
# 
# 95% recyclability is represented by a 100% collection rate and a 95% efficient recycling process.
# 
# The 50-year module uses the previous settings.

# In[14]:


r1.scenario['50_Year_Module'].data.keys()
r1.scenario['50_Year_Module'].material['glass'].materialdata.keys()


# In[14]:


#modify 15-year module attributes df2, with no compensation for capacity
r1.scenario['15_Year_Module'].data['mod_EOL_collected_recycled'] = 100 #100% collection
r1.scenario['15_Year_Module'].data['mod_EOL_collection_eff'] = 100
r1.scenario['15_Year_Module'].material['glass'].materialdata['mat_MFG_eff'] = 100 #100% efficiency of recycling
r1.scenario['15_Year_Module'].material['glass'].materialdata['mat_EOL_Recycled_into_HQ'] = 100 
r1.scenario['15_Year_Module'].material['glass'].materialdata['mat_EoL_Recycled_HQ_into_MFG'] = 95 #95% of the above 2 gets turned into new panels
r1.scenario['15_Year_Module'].material['glass'].materialdata['mat_MFG_scrap_recycled'] = 100
r1.scenario['15_Year_Module'].material['glass'].materialdata['mat_MFG_scrap_recycling_eff'] = 95
r1.scenario['15_Year_Module'].material['glass'].materialdata['mat_MFG_scrap_Recycled_into_HQ'] = 100
r1.scenario['15_Year_Module'].material['glass'].materialdata['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] = 100

#modify df3, includes compensation for capacity
r1.scenario['15_Year_Module_IncreasedInstalls'].data['mod_EOL_collected_recycled'] = 100 #100% collection
r1.scenario['15_Year_Module_IncreasedInstalls'].data['mod_EOL_collection_eff'] = 100
r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].materialdata['mat_MFG_eff'] = 100 #100% efficiency of recycling
r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].materialdata['mat_EOL_Recycled_into_HQ'] = 100 
r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].materialdata['mat_EoL_Recycled_HQ_into_MFG'] = 95 #95% of the above 2 gets turned into new panels
r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].materialdata['mat_MFG_scrap_recycled'] = 100
r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].materialdata['mat_MFG_scrap_recycling_eff'] = 95
r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].materialdata['mat_MFG_scrap_Recycled_into_HQ'] = 100
r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].materialdata['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] = 100


# In[ ]:


#potentially add silicon recycling modifications here?


# In[15]:


r1.calculateMassFlow()


# In[16]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_Virgin_Stock')


# Plot the annual waste glass sent to the landfill for this scenario. 
# Here, because the 15-module is 100% collected and only 5% is landfilled during the recycling process
# the landfilled glass is very low regardless of capacity assumptions.
# Thus, if the intent is to avoid landfilled material, a 95% recyclable module is the best technology evolution.

# In[17]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_Total_Landfilled')


# # IN DEVELOPMENT

# In[19]:


r1.createScenario(name='No_Deaths', file=r'..\baselines\baseline_modules_US.csv')
r1.scenario['No_Deaths'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')

r1.scenario['No_Deaths'].data['mod_reliability_t50'] = 100
r1.scenario['No_Deaths'].data['mod_reliability_t90'] = 150
r1.scenario['No_Deaths'].data['mod_Repowering'] = 99
r1.scenario['No_Deaths'].data['mod_Repairing'] = 99
r1.scenario['No_Deaths'].data['mod_lifetime'] = 100


# In[20]:


r1.calculateMassFlow()

r1.plotScenariosComparison(keyword='Installed_Capacity_[W]')


# ## LCA Analysis of 15 vs 50 Year Module
# 
# We have previously obtained results for ladnfilled waste for 50 year module, 15 year module, and 15 year module with increased installations to reach to 50 year module installed capacity. This is applies the LCA methodology to evaluate environmetnal impacts based on landfilled area.

# In[21]:


Area_50years = r1.scenario['50_Year_Module'].material['glass'].materialdata['mat_Total_Landfilled'].sum()
Area_15years = r1.scenario['15_Year_Module'].material['glass'].materialdata['mat_Total_Landfilled'].sum()
Area_15years_Increased_Installs = r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].materialdata['mat_Total_Landfilled'].sum()


# #### First we calculate the Area, based on the glass thickness and glass density and the Total Landfilled Waste [kg]. The PV panel area will be equal to the Glass Area for our modeled scenarios so far.

# In[22]:


[acidification, carcinogenics, ecotoxicity, eutrophication, 
fossil_fuel_depletion, global_warming,
non_carcinogenics, ozone_depletion, respiratory_effects, smog] = PV_DEMICE.calculateLCA(Area_50years)


# In[23]:


[acidification2, carcinogenics2, ecotoxicity2, eutrophication2, 
fossil_fuel_depletion2, global_warming2,
non_carcinogenics2, ozone_depletion2, respiratory_effects2, smog2] = PV_DEMICE.calculateLCA(Area_15years)


# In[24]:


[acidification3, carcinogenics3, ecotoxicity3, eutrophication3, 
fossil_fuel_depletion3, global_warming3,
non_carcinogenics3, ozone_depletion3, respiratory_effects3, smog3] = PV_DEMICE.calculateLCA(Area_15years_Increased_Installs)


# In[25]:


global_warming = pd.DataFrame({'Global warming':['50 year', '15 year', '15 year*'], 
                               'val':[global_warming, global_warming2, global_warming3]})


# In[26]:


ax = global_warming.plot.bar(x='Global warming', y='val', rot=0)
plt.title('Global Warming Effect, in kg CO2 eq')


# In[ ]:




