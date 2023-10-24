#!/usr/bin/env python
# coding: utf-8

# # 2 - 15 vs 50 Year Module
# 
# Comparison of a 15-year module lifetime vs 50-year module lifetime from a material circularity standpoint. 
# 
# 
# 
# 
# 
# ![Folder 15 vs 50 year Module](../images_wiki/2_15vs50Overview.PNG)
# 
# This scenario is a though experiment comparing a 15-year 95% recyclable module versus a 50-year module 30% recyclable module.
# This is done to understand potential tradeoffs in PV technology evolution - is it better to create
# a completely recyclable PV panel, or to extend the module lifetime.
# This scenario assumes that the 15-year module is 95% recyclable into high quality material, i.e. it will be used to create new modules.
# 
# 95% recyclability is represented by a 100% collection rate and a 95% efficient recycling process.
# 
# The 50-year module uses the previous settings.
# 
# Plot the annual waste glass sent to the landfill for this scenario. 
# Here, because the 15-module is 100% collected and only 5% is landfilled during the recycling process
# the landfilled glass is very low regardless of capacity assumptions.
# Thus, if the intent is to avoid landfilled material, a 95% recyclable module is the best technology evolution.
# 

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'Tutorial2')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


import PV_ICE


# In[3]:


import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.figsize'] = (12, 5)


# In[4]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='50_Year_Module', massmodulefile='baseline_modules_mass_US.csv')
r1.scenario['50_Year_Module'].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant'])

r1.createScenario(name='15_Year_Module', massmodulefile='baseline_modules_mass_US.csv')
r1.scenario['15_Year_Module'].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant'])

r1.createScenario(name='base', massmodulefile='baseline_modules_mass_US.csv')
r1.scenario['base'].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant'])


# In[5]:


r1.scenario['50_Year_Module'].dataIn_m.keys()


# ## Change Reliability Values

# In[6]:


r1.scenario['50_Year_Module'].dataIn_m['mod_reliability_t50'] = 60
r1.scenario['50_Year_Module'].dataIn_m['mod_reliability_t90'] = 70
r1.scenario['50_Year_Module'].dataIn_m['mod_lifetime'] = 50
r1.scenario['15_Year_Module'].dataIn_m['mod_degradation'] = 0.4

r1.scenario['15_Year_Module'].dataIn_m['mod_reliability_t50'] = 20
r1.scenario['15_Year_Module'].dataIn_m['mod_reliability_t90'] = 25
r1.scenario['15_Year_Module'].dataIn_m['mod_lifetime'] = 15
r1.scenario['15_Year_Module'].dataIn_m['mod_degradation'] = 1.4



# ## Change Recyclability Values

# In[7]:


r1.scenario['15_Year_Module'].dataIn_m['mod_EOL_pg4_recycled'] = 100.0 #100% collection
r1.scenario['15_Year_Module'].dataIn_m['mod_EOL_collection_eff'] = 100.0
#r1.scenario['15_Year_Module'].material['glass'].materialdata['mat_MFG_eff'] = 100 #100% efficiency of recycling
r1.scenario['15_Year_Module'].material['glass'].matdataIn_m['mat_MFG_scrap_Recycled'] = 100.0
r1.scenario['15_Year_Module'].material['glass'].matdataIn_m['mat_MFG_scrap_Recycling_eff'] = 90.0
r1.scenario['15_Year_Module'].material['glass'].matdataIn_m['mat_MFG_scrap_Recycled_into_HQ'] = 100.0
r1.scenario['15_Year_Module'].material['glass'].matdataIn_m['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] = 100.0
r1.scenario['15_Year_Module'].material['glass'].matdataIn_m['mat_PG4_Recycling_target'] = 100.0
r1.scenario['15_Year_Module'].material['glass'].matdataIn_m['mat_Recycling_yield'] = 90.0
r1.scenario['15_Year_Module'].material['glass'].matdataIn_m['mat_EOL_Recycled_into_HQ'] = 100.0
r1.scenario['15_Year_Module'].material['glass'].matdataIn_m['mat_EOL_RecycledHQ_Reused4MFG'] = 100.0 #95% of the above 2 gets turned into new panels

r1.scenario['50_Year_Module'].dataIn_m['mod_EOL_pg4_recycled'] = 100.0 #100% collection
r1.scenario['50_Year_Module'].dataIn_m['mod_EOL_collection_eff'] = 100.0
#r1.scenario['50_Year_Module'].material['glass'].materialdata['mat_MFG_eff'] = 100 #100% efficiency of recycling
r1.scenario['50_Year_Module'].material['glass'].matdataIn_m['mat_MFG_scrap_Recycled'] = 100.0
r1.scenario['50_Year_Module'].material['glass'].matdataIn_m['mat_MFG_scrap_Recycling_eff'] = 30.0
r1.scenario['50_Year_Module'].material['glass'].matdataIn_m['mat_MFG_scrap_Recycled_into_HQ'] = 100.0
r1.scenario['50_Year_Module'].material['glass'].matdataIn_m['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] = 100.0
r1.scenario['50_Year_Module'].material['glass'].matdataIn_m['mat_PG4_Recycling_target'] = 100.0
r1.scenario['50_Year_Module'].material['glass'].matdataIn_m['mat_Recycling_yield'] = 30.0
r1.scenario['50_Year_Module'].material['glass'].matdataIn_m['mat_EOL_Recycled_into_HQ'] = 100.0
r1.scenario['50_Year_Module'].material['glass'].matdataIn_m['mat_EOL_RecycledHQ_Reused4MFG'] = 100.0 #95% of the above 2 gets turned into new panels


# ## Turn IRENA lifetime values on or off & run PV ICE simulation

# In[8]:


IRENA= False
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


# In[9]:


r1.scenario['base'].material['glass'].matdataOut_m.keys()


# In[10]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_Total_Landfilled')
print("Modules installed between 2010 and 2020 become decommissioned on ~2035-2045, that is why the baseline has 'jaggedy' lines that follow the installs on those years.")
print("This jaggedy lines are not seen in the 15_Year_Module example, because 90% of it is going into recycling. You can still see a bit of effect on 2025-2035.")
print("For base, after 2045, and for 15_years, after 2035 become nice curves because the installs follow a CAGR projection.")
print("IF more years where plotted for the 50_year_module, we would see the same jaggediness around 2065-2075")


# In[11]:


r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_Total_Landfilled')


# In[12]:


r1.scenario['base'].dataOut_m.keys()


# In[13]:


r1.plotScenariosComparison(keyword='Effective_Capacity_[W]')


# ### Modifying Installed Capacity requirements to match 50 Year Module

# In[14]:


import copy


# In[15]:


r1.scenario['15_Year_Module_IncreasedInstalls'] = copy.deepcopy(r1.scenario['15_Year_Module'])


# In[16]:


r1.calculateMassFlow(scenarios='15_Year_Module_IncreasedInstalls')


# ### Modifing the installed capacity requiremetns according to t50. 
# 
# Needs to run each year becuase it needs to calculate the acumulated installs and deads.
# 

# In[17]:


a = r1.scenario['15_Year_Module_IncreasedInstalls'].dataIn_m


# In[18]:


Under_Installment = []
for i in range (0, len(r1.scenario['base'].dataIn_m)):
    Under_Installment = ( (r1.scenario['base'].dataOut_m['Effective_Capacity_[W]'][i] - 
                         r1.scenario['15_Year_Module_IncreasedInstalls'].dataOut_m['Effective_Capacity_[W]'][i])/1000000 )  # MWATTS
    r1.scenario['15_Year_Module_IncreasedInstalls'].dataIn_m.loc[i, 'new_Installed_Capacity_[MW]'] += Under_Installment
    r1.calculateMassFlow(scenarios='15_Year_Module_IncreasedInstalls')


# In[19]:


plt.plot(r1.scenario['15_Year_Module'].dataIn_m['new_Installed_Capacity_[MW]'], 'r')
plt.plot(r1.scenario['15_Year_Module_IncreasedInstalls'].dataIn_m['new_Installed_Capacity_[MW]'])


# Now copying to make the 50-year module with decreased installs

# In[20]:


r1.scenario['50_Year_Module_DecreasedInstalls'] = copy.deepcopy(r1.scenario['50_Year_Module'])


# In[21]:


r1.calculateMassFlow(scenarios='50_Year_Module_DecreasedInstalls')


# In[22]:


Over_Installment = []
for i in range (0, len(r1.scenario['base'].dataIn_m)):
    Over_Installment = ( (r1.scenario['50_Year_Module_DecreasedInstalls'].dataOut_m['Effective_Capacity_[W]'][i] - 
                         r1.scenario['base'].dataOut_m['Effective_Capacity_[W]'][i])/1000000 )  # MWATTS
    r1.scenario['50_Year_Module_DecreasedInstalls'].dataIn_m.loc[i, 'new_Installed_Capacity_[MW]'] -= Over_Installment
    r1.calculateMassFlow(scenarios='50_Year_Module_DecreasedInstalls')


# In[23]:


r1.plotScenariosComparison(keyword='new_Installed_Capacity_[MW]')


# In[24]:


r1.plotScenariosComparison(keyword='Effective_Capacity_[W]')


# In[25]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_Virgin_Stock')


# In[26]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_Total_Landfilled')


# ## Same plots but not automatic from the software to control more the parameters

# In[27]:


plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['base'].dataOut_m['Effective_Capacity_[W]']/1e12, 'g', label='base')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['50_Year_Module'].dataOut_m['Effective_Capacity_[W]']/1e12, 'r', label='50 year Module')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['15_Year_Module'].dataOut_m['Effective_Capacity_[W]']/1e12, 'b', label='15 year Module')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['50_Year_Module_DecreasedInstalls'].dataOut_m['Effective_Capacity_[W]']/1e12, 'r--', label='50 year Module w base capacity')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['15_Year_Module_IncreasedInstalls'].dataOut_m['Effective_Capacity_[W]']/1e12, 'b--', label='15 year Module w. base capacity')

plt.ylabel('Power [TW]')

plt.title('Installed Active Capacity')
plt.xlim([2000, 2050])
plt.legend()


# In[28]:


plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['base'].dataIn_m['new_Installed_Capacity_[MW]']/1e3, 'g', label='base')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['50_Year_Module'].dataIn_m['new_Installed_Capacity_[MW]']/1e3, 'r', label='50 year Module')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['15_Year_Module'].dataIn_m['new_Installed_Capacity_[MW]']/1e3, 'b', label='15 year Module')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['50_Year_Module_DecreasedInstalls'].dataIn_m['new_Installed_Capacity_[MW]']/1e3, 'r--', label='50 year Module w base capacity')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['15_Year_Module_IncreasedInstalls'].dataIn_m['new_Installed_Capacity_[MW]']/1e3, 'b--', label='15 year Module w. base capacity')

plt.ylabel('Power [GW]')

plt.title('New Installed Capacity')
plt.xlim([2000, 2050])
plt.legend()


# In[29]:


plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['base'].material['glass'].matdataOut_m['mat_Virgin_Stock']/1e9, 'g', label='base')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['50_Year_Module'].material['glass'].matdataOut_m['mat_Virgin_Stock']/1e9, 'r', label='50 Year Module')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['15_Year_Module'].material['glass'].matdataOut_m['mat_Virgin_Stock']/1e9, 'b', label='15 Year Module')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['50_Year_Module_DecreasedInstalls'].material['glass'].matdataOut_m['mat_Virgin_Stock']/1e9, 'r--', label='50 Year Module w. base capacity')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].matdataOut_m['mat_Virgin_Stock']/1e9, 'b--', label='15 Year Module w. base capacity')

plt.ylabel('Virgin Glass [Million Tonnes]')
plt.legend()
plt.title('Annual Virgin Material Input')
plt.xlim([2000, 2050])



# In[30]:


plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['base'].material['glass'].matdataOut_m['mat_Total_Landfilled']/1e9, 'g', label='base')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['50_Year_Module'].material['glass'].matdataOut_m['mat_Total_Landfilled']/1e9, 'r', label='50 Year Module')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['15_Year_Module'].material['glass'].matdataOut_m['mat_Total_Landfilled']/1e9, 'b', label='15 Year Module')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['50_Year_Module_DecreasedInstalls'].material['glass'].matdataOut_m['mat_Total_Landfilled']/1e9, 'r--', label='50 Year Module w. base capacity')
plt.plot(r1.scenario['base'].dataIn_m['year'], r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].matdataOut_m['mat_Total_Landfilled']/1e9, 'b--', label='15 Year Module w. base capacity')

plt.ylabel('Landfilled Glass\n [Million Tonnes]')
plt.legend()
plt.title('Annual Landfilled Waste')
plt.xlim([2000, 2050])


# In[ ]:


USyearly, UScum = r1.aggregateResults()


# In[ ]:


r1.saveSimulation()


# # Calculating Overall changes between the Scenarios

# In[31]:


cum_Waste = []
cum_VirginNeeds = []
cum_InstalledCapacity = []
cum_NewInstalls = []

for ii in range (0, len(r1.scenario.keys())):
    # Cumulative
    scen = list(r1.scenario.keys())[ii]
    cum_Waste.append(r1.scenario[scen].material['glass'].matdataOut_m['mat_Total_Landfilled'].sum())
    cum_VirginNeeds.append(r1.scenario[scen].material['glass'].matdataOut_m['mat_Virgin_Stock'].sum())
    cum_NewInstalls.append(r1.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'].sum())
    cum_InstalledCapacity.append(r1.scenario[scen].dataOut_m['Effective_Capacity_[W]'].iloc[-1])

df = pd.DataFrame(list(zip(list(r1.scenario.keys()), cum_Waste, cum_VirginNeeds, cum_NewInstalls, cum_InstalledCapacity)),
               columns =['scenarios','cum_Waste', 'cum_VirginNeeds', 'cum_NewInstalls', 'cum_InstalledCapacity'])


# ##  Normalize by Base Scenario (row 2)

# In[32]:


df[['cum_Waste', 'cum_VirginNeeds', 'cum_NewInstalls', 'cum_InstalledCapacity']] = df[['cum_Waste', 'cum_VirginNeeds', 'cum_NewInstalls', 'cum_InstalledCapacity']]*100/df[['cum_Waste', 'cum_VirginNeeds', 'cum_NewInstalls', 'cum_InstalledCapacity']].iloc[2] -100


# In[33]:


df.round(2)


# ## LCA Analysis of 15 vs 50 Year Module
# 
# We have previously obtained results for ladnfilled waste for 50 year module, 15 year module, and 15 year module with increased installations to reach to 50 year module installed capacity. This is applies the LCA methodology to evaluate environmetnal impacts based on landfilled area.

# In[34]:


Area_50years = r1.scenario['50_Year_Module'].material['glass'].matdataOut_m['mat_Virgin_Stock'].sum()
Area_15years = r1.scenario['15_Year_Module'].material['glass'].matdataOut_m['mat_Virgin_Stock'].sum()
Area_15years_Increased_Installs = r1.scenario['15_Year_Module_IncreasedInstalls'].material['glass'].matdataOut_m['mat_Virgin_Stock'].sum()


# #### First we calculate the Area, based on the glass thickness and glass density and the Total Landfilled Waste [kg]. The PV panel area will be equal to the Glass Area for our modeled scenarios so far.

# In[35]:


[acidification, carcinogenics, ecotoxicity, eutrophication, 
fossil_fuel_depletion, global_warming,
non_carcinogenics, ozone_depletion, respiratory_effects, smog] = PV_ICE.calculateLCA(Area_50years)


# In[36]:


[acidification2, carcinogenics2, ecotoxicity2, eutrophication2, 
fossil_fuel_depletion2, global_warming2,
non_carcinogenics2, ozone_depletion2, respiratory_effects2, smog2] = PV_ICE.calculateLCA(Area_15years)


# In[37]:


[acidification3, carcinogenics3, ecotoxicity3, eutrophication3, 
fossil_fuel_depletion3, global_warming3,
non_carcinogenics3, ozone_depletion3, respiratory_effects3, smog3] = PV_ICE.calculateLCA(Area_15years_Increased_Installs)


# In[38]:


global_warming = pd.DataFrame({'Global warming':['50 year', '15 year', '15 year Increased Installs'], 
                               'val':[global_warming, global_warming2, global_warming3]})


# In[39]:


ax = global_warming.plot.bar(x='Global warming', y='val', rot=0)
plt.title('Global Warming Effect, in kg CO2 eq')

