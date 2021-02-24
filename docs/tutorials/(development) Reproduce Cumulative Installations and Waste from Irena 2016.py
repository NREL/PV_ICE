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
# - Installation Data < 2010 from D. Jordan (Values too low to digitize properly)
# - Installation data >= 2010 from IRENA report (digitized from plot)
# 
# 
# Other considerations:
#   <ul> 
#     <li> Global projected installations from IEA/IRENA (picture below). </li>
#     <li> No recycling, no reuse, no repair.  </li>
#     <li> 30-year average lifetime with early lifetime failures </li>
#     <li> Power to Glass conversion: 76 t/MW </li>
# </ul>

# In[14]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[15]:


import PV_ICE


# In[16]:


import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# ## PV ICE

# In[30]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='PV_ICE', file=r'..\baselines\baseline_modules_World_Irena_2019.csv')
r1.scenario['PV_ICE'].addMaterial('glass', file=r'..\baselines\baseline_material_glass_Irena_2019.csv')

r1.createScenario(name='PV_ICE_base', file=r'..\baselines\baseline_modules_World_Irena_2019.csv')
r1.scenario['PV_ICE_base'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')


r1.createScenario(name='A_MassBased', file=r'..\baselines\baseline_modules_World_Irena_2019_A_MassBased.csv')
r1.scenario['A_MassBased'].addMaterial('glass', file=r'..\baselines\baseline_material_glass_Irena_A_MassBased.csv')

r1.createScenario(name='B_PowerBased', file=r'..\baselines\baseline_modules_World_Irena_2019_B_PowerBased.csv')
r1.scenario['B_PowerBased'].addMaterial('glass', file=r'..\baselines\baseline_material_glass_Irena_B_PowerBased.csv')


# In[ ]:





# Plot same plot from Garvin's paper from digitized data input

# In[31]:


fig = plt.figure(figsize=(20,10))
ax1 = plt.subplot(111)
ax1.yaxis.grid()
plt.axvspan(2000, 2018, facecolor='0.9', alpha=0.5)
plt.axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
ax1.bar(r1.scenario['PV_ICE'].data['year'], r1.scenario['PV_ICE'].data['new_Installed_Capacity_[MW]']/1000, color='gold', label='IRENA')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Annual Deployments (GW/yr)')
plt.xlim([2000, 2050.5])
plt.ylim([0, 400])


# #### Adjusting input parameters to represent the inputs from the IRENA analysis:

# In[ ]:





# In[ ]:





# In[32]:


IRENA= True
ELorRL = 'RL'
if IRENA:
    if ELorRL == 'RL':
        weibullInputParams = {'alpha': 5.3759}  # Regular-loss scenario IRENA
    if ELorRL == 'EL':
        weibullInputParams = {'alpha': 2.49}  # Regular-loss scenario IRENA
    r1.calculateMassFlow(weibullInputParams=weibullInputParams, weibullAlphaOnly=True)
    title_Method = 'Irena_'+ELorRL
else:
    r1.calculateMassFlow()
    title_Method = 'PVICE'


# In[ ]:





# ## Irena Conversion from Mass to Energy --> 
# mat_Total_Landfilled is in g, 1 t --> 907.185 kg 
#  1 MW --> 76 t conversion for the Mass in PV service.

# Querying some of the values for plotting the flags

# In[33]:


x2020 = r1.scenario['PV_ICE'].data['year'].iloc[25]
y2020 = r1.scenario['PV_ICE'].data['Installed_Capacity_[W]'].iloc[25]*76/1000000
t2020 = r1.scenario['PV_ICE'].data['Installed_Capacity_[W]'].iloc[25]/(1E12)


x2030 = r1.scenario['PV_ICE'].data['year'].iloc[35]
y2030 = r1.scenario['PV_ICE'].data['Installed_Capacity_[W]'].iloc[35]*76/1000000
t2030 = r1.scenario['PV_ICE'].data['Installed_Capacity_[W]'].iloc[35]/(1E12)

x2050 = r1.scenario['PV_ICE'].data['year'].iloc[55]
y2050 = r1.scenario['PV_ICE'].data['Installed_Capacity_[W]'].iloc[55]*76/1000000
t2050 = r1.scenario['PV_ICE'].data['Installed_Capacity_[W]'].iloc[55]/(1E12)

print(x2050)


# Calculating Cumulative Waste isntead of yearly waste
# 
# Using glass for proxy of the module; glass is ~76% of the module's mass [REF]
# 

# In[35]:


cumWaste = r1.scenario['PV_ICE'].material['glass'].materialdata['mat_Total_Landfilled'].cumsum()
cumWaste = (cumWaste*100/76)/1000000  # Converting to tonnes

cumWaste0 = r1.scenario['PV_ICE_base'].material['glass'].materialdata['mat_Total_Landfilled'].cumsum()
cumWaste0 = (cumWaste0*100/76)/1000000  # Converting to tonnes



cumWaste2 = r1.scenario['A_MassBased'].material['glass'].materialdata['mat_Total_Landfilled'].cumsum()
cumWaste2 = (cumWaste2*100/76)/1000000  # Converting to tonnes

cumWaste3 = r1.scenario['B_PowerBased'].material['glass'].materialdata['mat_Total_Landfilled'].cumsum()
cumWaste3 = (cumWaste3*100/76)/1000000  # Converting to tonnes


# PLOT:

# In[38]:


fig = plt.figure(figsize=(10,10))
plt.semilogy(r1.scenario['PV_ICE'].data.year,r1.scenario['PV_ICE'].data['Installed_Capacity_[W]']*76/1000000, color='C1', label='Mass of PV in service')
plt.semilogy(r1.scenario['PV_ICE_base'].data.year,cumWaste0, 'r', label='PV ICE Base-ish Cum Waste')
plt.semilogy(r1.scenario['PV_ICE'].data.year,cumWaste, 'r.', label='PV ICE Perfect Efficiencies')
plt.semilogy(r1.scenario['A_MassBased'].data.year,cumWaste2, 'k.', label='A - Material Based Cum Waste')
plt.semilogy(r1.scenario['B_PowerBased'].data.year,cumWaste3, 'g', label='B - Power Based Cum Waste')


plt.ylim([1E4, 1E9])
plt.legend()
plt.tick_params(axis='y', which='minor')
plt.xlim([2020,2050])
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



# In[28]:


fig = plt.figure(figsize=(10,10))
plt.semilogy(r1.scenario['PV_ICE'].data.year,r1.scenario['PV_ICE'].material['glass'].materialdata['mat_Total_Landfilled'], label='PV Glass Waste per Year')
plt.legend()


# In[ ]:





# In[ ]:





# In[ ]:




