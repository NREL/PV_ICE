#!/usr/bin/env python
# coding: utf-8

# # 1 - Estimate when US Installs will reach EoL
# 
# 
# Historical installations for U.S. Utility and non-Residential sector was calculated from:
# 1. 1995 through 1998: K. Bolcar and K. Ardani, “National Survey Report of PV Power Applications in the United States 2010,” IEA-PVPS, National Survey T1-19:2010, 2010. [Online]. Available: https://iea-pvps.org/national-survey-reports/.
# 2. L. Sherwood, “U.S. Solar Market Trends 2008,” Interstate Renewable Energy Council, Jul. 2009. Accessed: Sep. 15, 2021. [Online]. Available: https://irecusa.org/wp-content/uploads/2021/07/Solar-Market-Trends-2008.pdf
# 3. All Sherwood reports 2009-2014 for 1999 through 2009
# 4. Wood Mackenzie Data from 2010 forward.
# 5. “U.S. Solar Market Insight Report: 2012 Year in Review Full Report,” Greentech Media Inc. & SEIA, 2013 as a sanity check.
# 
# The calculations to select for only these 2 sectors and weight for c-Si can be found in Supporting Materials folder, files "Calculations-Installs-Subset-CommUtility.xlsx", "Installs-SubsetCommUtility.xlsx", and "Installs-SubsetCommUtility.csv".
# 
# These installations where then put into a module file. Installations after 2020 are set to 0, manufacturing efficiency is set to 100, and all circular EoL pathways are set to 0, sending all EoL material to the landfill. All lifetime and reliability, module efficiencies, and module degradation rates are taken from PV ICE baseline. The purpose of this calculation is to estimate when currently installed PV modules will come out of the field and need to be managed at EoL.
# 
# NOTE: this analysis has been updated for a 2022 release of an NREL decommissioning report. The update includes resolving a bug in how the Weibull function was applied to the cohorts, resolution of edge cases, and an update to the installation inputs, examining all 3 sectors of PV installs using Wood Mackenzie assumptions.

# This analysis conducted for Taylor Curtis

# In[1]:


import os
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


PV_ICE.__version__


# ### Add Scenarios and Materials
# 

# In[3]:


cwd=os.getcwd()
print(os.getcwd())


# In[4]:


MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
MATERIAL = MATERIALS[0]
moduleFile = r'..\baselines\baseline_modules_mass_US_HistoryUtilCommOnly.csv'


# In[5]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='USHistory', massmodulefile=moduleFile)
for mat in range (0, len(MATERIALS)):
    MATERIALBASELINE = r'..\baselines\baseline_material_mass_'+MATERIALS[mat]+'.csv'
    r1.scenario['USHistory'].addMaterial(MATERIALS[mat], massmatfile=MATERIALBASELINE)


# ### Set All Material Virgin, MFG, and circularity to 0
# 
# The effective this will be to neglect all inefficiencies in the extraction and manufacturing process, looking at just the PV module material coming out of the field, and assuming it all goes to the landfill.

# In[6]:


r1.scenMod_noCircularity() # sets all module and material circular variables to 0, creating fully linear
r1.scenMod_PerfectManufacturing() #sets all manufacturing values to 100% efficiency/yield
#check:
#r1.scenario['USHistory'].material['glass'].materialdata['mat_MFG_eff']


# ### Run the Mass Flow Calculations on All Scenarios and Materials

# In[7]:


r1.calculateMassFlow()


# ###  Use internal plotting functions to plot results

# Pull out the keywords by printing the keys to the module data or the material data:
# 
#     print(r1.scenario.keys())
#     
#     print(r1.scenario['standard'].data.keys())
#     
#     print(r1.scenario['standard'].material['glass'].materialdata.keys())

# In[8]:


#print(r1.scenario.keys())
print(r1.scenario['USHistory'].dataOut_m.keys())
#print(r1.scenario['USHistory'].material['glass'].materialdata.keys())


# In[9]:


r1.plotScenariosComparison(keyword='Yearly_Sum_Area_disposed')


# In[ ]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_Total_MFG_Landfilled')


# In[ ]:


plt.plot(r1.scenario['USHistory'].dataIn_m['year'], 
         r1.scenario['USHistory'].dataOut_m['Installed_Capacity_[W]'], label='Installed [W]')

plt.title('Installed Capacity Annually')
plt.ylabel('Installed Cap [W]')


# In[10]:


usyearlyr1, uscumr1 = r1.aggregateResults()
usyearlyr1.to_csv('historicalUS-yearly.csv')
uscumr1.to_csv('historicalUS-cumulative.csv')


# ## Pretty Plots

# In[11]:


#create a yearly Module Waste Mass
USyearly=pd.DataFrame()
keyword = 'mat_Total_Landfilled'
for mat in range (0, len(MATERIALS)):
    material = MATERIALS[mat]
    foo = r1.scenario['USHistory'].material[material].matdataOut_m[keyword].copy()
    foo = foo.to_frame(name=material)
    USyearly["Waste_"+material] = foo[material]

#sum the columns for module mass
USyearly['Waste_Module'] = USyearly.sum(axis=1)

USyearly.head(10)


# In[12]:


#add index
USyearly.index = r1.scenario['USHistory'].dataIn_m['year']


# In[13]:


#Convert to million metric tonnes
USyearly_mil_tonnes=USyearly/1000000000000


# In[14]:


#Adding new installed capacity for decomissioning calc
USyearly_mil_tonnes['new_Installed_Capacity_[MW]'] = r1.scenario['USHistory'].dataIn_m['new_Installed_Capacity_[MW]'].values


# In[15]:


UScum = USyearly_mil_tonnes.copy()
UScum = UScum.cumsum()

UScum.head()


# In[16]:


bottoms = pd.DataFrame(UScum.loc[2050])
bottoms


# In[17]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (15, 8)

f, (a0, a1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})

########################    
# SUBPLOT 1
########################
a0.plot(USyearly_mil_tonnes.index, USyearly_mil_tonnes['Waste_Module'], 'k.', linewidth=5, label='EoL Module Mass')
a0.plot(USyearly_mil_tonnes.index, USyearly_mil_tonnes['Waste_glass'], 'k', linewidth=5, label='EoL Glass Mass')
a0.fill_between(USyearly_mil_tonnes.index, USyearly_mil_tonnes['Waste_glass'], USyearly_mil_tonnes['Waste_Module'],
                color='k', alpha=0.3, interpolate=True)

a0.legend()
a0.set_title('Yearly EoL Material Mass')
a0.set_ylabel('Mass [Million Tonnes]')
a0.set_xlim([1995, 2050])
a0.set_xlabel('Years')

########################    
# SUBPLOT 2
########################
## Plot BARS Stuff
ind=np.arange(1)
width=0.35 # width of the bars.

bottoms = pd.DataFrame(UScum.loc[2050])

p0 = a1.bar(ind, UScum.loc[2050]['Waste_glass'], width, color='c')
p1 = a1.bar(ind, UScum.loc[2050]['Waste_aluminium_frames'], width, bottom=bottoms.iloc[0])
p2 = a1.bar(ind, UScum.loc[2050]['Waste_silicon'], width, bottom=(bottoms.iloc[1]+bottoms.iloc[0]))
p3 = a1.bar(ind, UScum.loc[2050]['Waste_copper'], width, bottom=(bottoms.iloc[2]+bottoms.iloc[1]+bottoms.iloc[0]))
p4 = a1.bar(ind, UScum.loc[2050]['Waste_silver'], width, bottom=(bottoms.iloc[3]+bottoms.iloc[2]+bottoms.iloc[1]+bottoms.iloc[0]))
p5 = a1.bar(ind, UScum.loc[2050]['Waste_encapsulant'], width, bottom=(bottoms.iloc[4]+bottoms.iloc[3]+bottoms.iloc[2]+bottoms.iloc[1]+bottoms.iloc[0]))
p6 = a1.bar(ind, UScum.loc[2050]['Waste_backsheet'], width, bottom=(bottoms.iloc[5]+bottoms.iloc[4]+bottoms.iloc[3]+bottoms.iloc[2]+bottoms.iloc[1]+bottoms.iloc[0]))

a1.yaxis.set_label_position("right")
a1.yaxis.tick_right()
a1.set_ylabel('EoL PV Material [Million Tonnes]')
a1.set_xlabel('Cumulative in 2050')
a1.set_xticks(ind)
a1.legend((p0[0], p1[0], p2[0], p3[0], p4[0], p5[0], p6[0] ), ('Glass', 'Aluminium frames', 'Silicon','Copper','Silver', 'Encapsulant', 'Backsheet'))


# # Plot and Table of decommissioned in MW
# decommissioned yearly = cumulative new installs - yearly active capacity
# 
# the decommissioned yearly column is actually cumulative, so do reverse cum on it.
# 
# Create a table output of installs, active generating capacity annually decommissioned, cumulatively decomissioned, and cumulative decomissioned module mass.

# In[18]:


usyearlyr1.head()


# In[19]:


tidy_results = usyearlyr1.iloc[:,32:]
tidy_results.columns = ('new_Installed_Capacity_[MW]', 'Active_Capacity_[MW]','Cumulative_Decomissioned_Capacity_[MW]')


# In[20]:


#tidy_results['Annual_Decommissioned_Capacity_[MW]'] = 
tidy_results['Annual_Decomissioned_Capacity_[MW]'] = tidy_results['Cumulative_Decomissioned_Capacity_[MW]']-tidy_results['Cumulative_Decomissioned_Capacity_[MW]'].shift(1).fillna(0)
tidy_results['Cumulative_Module_Mass_Decommissioned_[million tonnes]'] = usyearlyr1.filter(like='WasteAll_Module')/1e6
tidy_results


# In[21]:


tidy_results.to_csv(path_or_buf=r'..\baselines\SupportingMaterial\US_Historical_PV_Decomissioning.csv')


# In[ ]:





# In[ ]:





# In[ ]:




