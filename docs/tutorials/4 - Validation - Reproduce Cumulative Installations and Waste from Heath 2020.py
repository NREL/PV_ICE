#!/usr/bin/env python
# coding: utf-8

# # 4 - Validation - Reproduce Cumulative Installations and Waste from Heath 2020

# This journal will reproduce the results from Garvin Heath & Tim Silverman's paper 2020. Plotting Cumulative Installations and Cumulative Waste, such that:
# 
# ![Garvin Results](../images_wiki/GARVIN_2020.PNG)
# 
# Input is from IRENA projections:
# ![Input from IRENA_projections](../images_wiki/IRENA_projections.PNG)
# 
# Notes on IRENA Data:
# - Installation Data < 2010 from D. Jordan
# - Installation data >= 2010 from IRENA report
# 
# 
# Other considerations:
#   <ul> 
#     <li> Global projected installations from IEA/IRENA (picture below). </li>
#     <li> No recycling, no reuse, no repair.  </li>
#     <li> 30-year average lifetime with early lifetime failures </li>
#     <li> Power to Glass conversion: 76 t/MW </li>
# </ul>

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


import PV_ICE


# In[3]:


import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# ## REPAIR

# In[42]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='Garvin_2020', file=r'..\baselines\baseline_modules_World_Irena.csv')
r1.scenario['Garvin_2020'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')

r1.createScenario(name='PV_ICE_default', file=r'..\baselines\baseline_modules_World.csv')
r1.scenario['PV_ICE_default'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')


# In[43]:


r1.scenario['Garvin_2020'].data.keys()


# In[44]:


plt.plot(r1.scenario['Garvin_2020'].data['year'], r1.scenario['Garvin_2020'].data['new_Installed_Capacity_[MW]']/1000, 'r', label = 'Irena Digitized')
plt.plot(r1.scenario['PV_ICE_default'].data['year'], r1.scenario['PV_ICE_default'].data['new_Installed_Capacity_[MW]']/1000, 'g', label = 'World Baseline')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Annual Deployments (GW/yr)')
plt.xlim([2000, 2050])
plt.ylim([0, 400])
#plt.axhspan(200, 2018, facecolor='0.2', alpha=0.5)
plt.axvspan(2000, 2018, facecolor='0.9', alpha=0.9)

#plt.axvspan(2019, 2050, facecolor='0.2', alpha=0.5)


# In[45]:


#fig = plt.figure()
fig = plt.figure(figsize=(20,10))
ax1 = plt.subplot(111)
ax1.yaxis.grid()
plt.axvspan(2000, 2018, facecolor='0.9', alpha=0.5)
plt.axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
ax1.bar(r1.scenario['Garvin_2020'].data['year'], r1.scenario['Garvin_2020'].data['new_Installed_Capacity_[MW]']/1000, color='gold', label='IRENA')
plt.plot(r1.scenario['PV_ICE_default'].data['year'], r1.scenario['PV_ICE_default'].data['new_Installed_Capacity_[MW]']/1000, 'r', label = 'World Baseline')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Annual Deployments (GW/yr)')
plt.xlim([2000, 2050.5])
plt.ylim([0, 400])


# In[147]:


r1.scenario['Garvin_2020'].data['mod_Repairing'] = 0
r1.scenario['Garvin_2020'].data['mod_Repowering'] = 0

r1.scenario['Garvin_2020'].data['mod_degradation'] = 0
r1.scenario['Garvin_2020'].data['mod_EOL_collection_eff'] = 0  # Everything goes to landfill
r1.scenario['Garvin_2020'].data['mod_reliability_t50'] = 25
r1.scenario['Garvin_2020'].data['mod_reliability_t90'] = 38
# Setting Project Lifetime beyond Failures
r1.scenario['Garvin_2020'].data['mod_lifetime'] = 40


# In[148]:


r1.scenario['PV_ICE_default'].data.keys()


# In[149]:


r1.calculateMassFlow()


# In[150]:


r1.scenario['Garvin_2020'].data.keys()


# In[151]:


r1.scenario['Garvin_2020'].material['glass'].materialdata.keys()


# In[152]:


r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[-1]/(1E9)


# In[153]:


r1.scenario['Garvin_2020'].data['year'].iloc[25]
r1.scenario['Garvin_2020'].data['year'].iloc[35]
r1.scenario['Garvin_2020'].data['year'].iloc[55]


# In[154]:


print(r1.scenario['Garvin_2020'].data['year'].iloc[25], r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[25]/(1E12))
print(r1.scenario['Garvin_2020'].data['year'].iloc[35], r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[35]/(1E12))
print(r1.scenario['Garvin_2020'].data['year'].iloc[55], r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[55]/(1E12))


# ### Remidner NOTES:
#  mat_Total_Landfilled is in kg, 1 t --> 907.185 kg 
#  1 MW --> 76 t conversion for the Mass in PV service.

# In[177]:


x2050 = r1.scenario['Garvin_2020'].data['year'].iloc[55]
y2050 = r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[55]*76/1000000
t2050 = r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[55]/(1E12)

x2030 = r1.scenario['Garvin_2020'].data['year'].iloc[35]
y2030 = r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[35]*76/1000000
t2030 = r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[35]/(1E12)

x2020 = r1.scenario['Garvin_2020'].data['year'].iloc[25]
y2020 = r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[25]*76/1000000
t2020 = r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]'].iloc[25]/(1E12)


# In[196]:


fig = plt.figure(figsize=(10,10))
plt.semilogy(r1.scenario['Garvin_2020'].data.year,r1.scenario['Garvin_2020'].material['glass'].materialdata['mat_Total_Landfilled']/907.185, label='Mass of PV in service')
plt.semilogy(r1.scenario['Garvin_2020'].data.year,r1.scenario['Garvin_2020'].data['Installed_Capacity_[W]']*76/1000000, label='Cumulative PV Waste')
plt.ylim([1E5, 1E9])
plt.legend()
plt.tick_params(axis='y', which='minor')
plt.xlim([2016,2050])
plt.grid()
plt.ylabel('Mass of PV systems (t)')
plt.xlabel('Years')

offset = (0, 30)

plt.annotate(
    '{:.1f} TW'.format(t2050), (x2050, y2050),
    ha='center', va='center',
    size=15,
    xytext=offset, textcoords='offset points',
    bbox=dict(boxstyle='round', fc='#ff7f0e', ec='none'),
    arrowprops=dict(arrowstyle='wedge,tail_width=1.',
                    fc='#ff7f0e', ec='none',
                    relpos=(0.5, 1.5),
                    )
)

plt.annotate(
    '{:.1f} TW'.format(t2030), (x2030, y2030),
    ha='center', va='center',
    size=15,
    xytext=offset, textcoords='offset points',
    bbox=dict(boxstyle='round', fc='#ff7f0e', ec='none'),
    arrowprops=dict(arrowstyle='wedge,tail_width=1.',
                    fc='#ff7f0e', ec='none',
                    relpos=(0.5, 1.5),
                    )
)


plt.annotate(
    '{:.1f} TW'.format(t2020), (x2020, y2020),
    ha='center', va='center',
    size=15,
    xytext=offset, textcoords='offset points',
    bbox=dict(boxstyle='round', fc='#ff7f0e', ec='none'),
    arrowprops=dict(arrowstyle='wedge,tail_width=1.',
                    fc='#ff7f0e', ec='none',
                    relpos=(0.5, 1.5),
                    )
)

plt.show()


