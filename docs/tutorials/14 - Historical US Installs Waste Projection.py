#!/usr/bin/env python
# coding: utf-8

# # 1 - Estimate when US Installs will reach EoL
# 
# 
# Historical installations for U.S. Utility and non-Residential sector was calculated from
# 1. L. Sherwood, “U.S. Solar Market Trends 2008,” Interstate Renewable Energy Council, Jul. 2009. Accessed: Sep. 15, 2021. [Online]. Available: https://irecusa.org/wp-content/uploads/2021/07/Solar-Market-Trends-2008.pdf
# 2. All Sherwood reports 2009-2014 for 1999 through 2009
# 3. Wood Mackenzie Data from 2010 forward.
# 4. “U.S. Solar Market Insight Report: 2012 Year in Review Full Report,” Greentech Media Inc. & SEIA, 2013 as a sanity check.
# The calculations to select for only these 2 sectors and weight for c-Si can be found in Supporting Materials folder, files "Calculations-Installs-Subset-CommUtility.xlsx", "Installs-SubsetCommUtility.xlsx", and "Installs-SubsetCommUtility.csv".
# 
# These installations where then put into a module file. Installations after 2020 are set to 0, manufacturing efficiency is set to 100, and all circular EoL pathways are set to 0, sending all EoL material to the landfill. All lifetime and reliability, module efficiencies, and module degradation rates are taken from PV ICE baseline. The purpose of this calculation is to estimate when currently installed PV modules will come out of the field and need to be managed at EoL.
# 

# This analysis conducted for Taylor Curtis

# In[1]:


import os
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

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
moduleFile = r'..\baselines\baseline_modules_US_HistoryUtilCommOnly.csv'


# In[5]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='USHistory', file=moduleFile)
for mat in range (0, len(MATERIALS)):
    MATERIALBASELINE = r'..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r1.scenario['USHistory'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)


# ### Set All Material Virgin, MFG, and circularity to 0
# 
# The effective this will be to neglect all inefficiencies in the extraction and manufacturing process, looking at just the PV module material coming out of the field, and assuming it all goes to the landfill.

# In[6]:


r1.scenario['USHistory'].material['glass'].materialdata.keys()


# In[7]:


#list of material recycling variables
RecyclingPaths = ['mat_MFG_scrap_Recycled', 'mat_MFG_scrap_Recycled_into_HQ', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 'mat_EOL_collected_Recycled', 'mat_EOL_Recycled_into_HQ', 'mat_EoL_Recycled_HQ_into_MFG']
RecyclingYields = ['mat_MFG_scrap_Recycling_eff', 'mat_EOL_Recycling_eff']


# In[8]:


for mat in range (0, len(MATERIALS)):
    r1.scenario['USHistory'].material[MATERIALS[mat]].materialdata['mat_virgin_eff'] = 100.0
    r1.scenario['USHistory'].material[MATERIALS[mat]].materialdata['mat_MFG_eff'] = 100.0
    for var in range (0,len(RecyclingPaths)):
        r1.scenario['USHistory'].material[MATERIALS[mat]].materialdata[RecyclingPaths[var]] = 0.0
    for ylds in range(0,len(RecyclingYields)):
        r1.scenario['USHistory'].material[MATERIALS[mat]].materialdata[RecyclingYields[ylds]] = 0.0


# ### Run the Mass Flow Calculations on All Scenarios and Materials

# In[9]:


r1.calculateMassFlow()


# ###  Use internal plotting functions to plot results

# Pull out the keywords by printing the keys to the module data or the material data:
# 
#     print(r1.scenario.keys())
#     
#     print(r1.scenario['standard'].data.keys())
#     
#     print(r1.scenario['standard'].material['glass'].materialdata.keys())

# In[10]:


#print(r1.scenario.keys())
#print(r1.scenario['USHistory'].data.keys())
print(r1.scenario['USHistory'].material['glass'].materialdata.keys())


# In[11]:


r1.plotScenariosComparison(keyword='Cumulative_Area_disposed')


# In[12]:


r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_Total_MFG_Landfilled')


# In[13]:


plt.plot(r1.scenario['USHistory'].data['year'], 
         r1.scenario['USHistory'].data['Installed_Capacity_[W]'], label='Installed [W]')

plt.title('Installed Capacity Annually')
plt.ylabel('Installed Cap [W]')


# In[14]:


usyearlyr1, uscumr1 = r1.aggregateResults()
usyearlyr1.to_csv('r1-usyearly-func.csv')
uscumr1.to_csv('r1-uscum-func.csv')


# ## Pretty Plots

# In[15]:


#create a yearly Module Waste Mass
USyearly=pd.DataFrame()
keyword = 'mat_Total_Landfilled'
for mat in range (0, len(MATERIALS)):
    material = MATERIALS[mat]
    foo = r1.scenario['USHistory'].material[material].materialdata[keyword].copy()
    foo = foo.to_frame(name=material)
    USyearly["Waste_"+material] = foo[material]

#sum the columns for module mass
USyearly['Waste_Module'] = USyearly.sum(axis=1)

USyearly.head(10)


# In[16]:


#add index
USyearly.index = r1.scenario['USHistory'].data['year']


# In[17]:


#Convert to million metric tonnes
USyearly_mil_tonnes=USyearly/1000000000000


# In[18]:


#Adding new installed capacity for decomissioning calc
USyearly_mil_tonnes['new_Installed_Capacity_[MW]'] = r1.scenario['USHistory'].data['new_Installed_Capacity_[MW]'].values


# In[19]:


UScum = USyearly_mil_tonnes.copy()
UScum = UScum.cumsum()

UScum.head()


# In[20]:


bottoms = pd.DataFrame(UScum.loc[2050])
bottoms


# In[38]:


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


# ### plot of decommissioned in MW
# decommissioned yearly = cumulative new installs - yearly active capacity

# In[22]:


#Add Installed capacity to yearly
USyearly_mil_tonnes['Active_Capacity_[W]'] = r1.scenario['USHistory'].data['Installed_Capacity_[W]'].values
USyearly_mil_tonnes.head()


# In[23]:


USyearly_mil_tonnes.to_csv('r1-usyearly.csv')
UScum.to_csv('r1-uscum.csv')


# In[24]:


USyearly_mil_tonnes['Decommissioned_yearly_[MW]'] = UScum['new_Installed_Capacity_[MW]'] - (USyearly_mil_tonnes['Active_Capacity_[W]']/1e6)
plt.plot(USyearly_mil_tonnes['Decommissioned_yearly_[MW]'], label='decommissioned', color='r')
plt.plot(UScum['new_Installed_Capacity_[MW]'], label='cum installs')
plt.plot((USyearly_mil_tonnes['Active_Capacity_[W]']/1e6), label='active capacity')
plt.plot(USyearly_mil_tonnes['new_Installed_Capacity_[MW]'], label='yearly new installs')
plt.legend()
plt.ylabel('MW')


# In[25]:


#Print out results to file for Taylor
tidy_results = pd.DataFrame()
tidy_results['Annual_Installations_[MW]'] = USyearly_mil_tonnes['new_Installed_Capacity_[MW]']
tidy_results['Active_Generating_Capacity_[MW]'] = (USyearly_mil_tonnes['Active_Capacity_[W]']/1e6)
tidy_results['Annually_Decommissioned_[MW]'] = USyearly_mil_tonnes['Decommissioned_yearly_[MW]']
tidy_results['Cumulative_Decommissioned_[MW]'] = USyearly_mil_tonnes['Decommissioned_yearly_[MW]'].cumsum()
tidy_results['Cumulative_Decommissioned_Module_Mass_[million metric tonnes]'] = UScum['Waste_Module']

tidy_results


# In[26]:


tidy_results.to_csv(path_or_buf=r'..\baselines\SupportingMaterial\US_Historical_PV_Decomissioning.csv')


# # Test with New PV ICE functions

# In[27]:


import os
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[28]:


PV_ICE.__version__


# In[29]:


cwd=os.getcwd()
print(os.getcwd())


# In[30]:


MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper', 'encapsulant']
MATERIAL = MATERIALS[0]
moduleFile = r'..\baselines\baseline_modules_US_HistoryUtilCommOnly.csv'


# In[31]:


r2 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r2.createScenario(name='USHistory', file=moduleFile)
for mat in range (0, len(MATERIALS)):
    MATERIALBASELINE = r'..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
    r2.scenario['USHistory'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)


# ### Set circular paths to 0 using new PV ICE function

# In[32]:


#format r2.scenMod_Description(scenarios='scenariolist')
r2.scenMod_noCircularity() # sets all module and material circular variables to 0, creating fully linear
r2.scenMod_PerfectManufacturing() #sets all manufacturing values to 100% efficiency/yield
#check:
r2.scenario['USHistory'].material['glass'].materialdata['mat_MFG_eff']


# In[33]:


r2.calculateMassFlow()


# In[34]:


Usyearlyr2, UScumr2 = r2.aggregateResults()


# In[35]:


Usyearlyr2.head()


# In[36]:


UScumr2.head()


# In[37]:


Usyearlyr2.to_csv('r2-usyearly.csv')
UScumr2.to_csv('r2-uscum.csv')


# In[ ]:




