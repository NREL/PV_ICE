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
baselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')

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
moduleFile = os.path.join(baselinesfolder, 'baseline_modules_mass_US_HistoryUtilCommOnly.csv')
newmodfilesPAth = os.path.join(supportMatfolder,'Calculations-Installs-Subset-CommUtility.xlsx')


# In[5]:


newmoduleFile_raw = pd.read_excel(newmodfilesPAth, sheet_name='SectorInstalls', header=2)


# In[6]:


newmoduleFile_raw.columns


# In[7]:


installs_allPV_df = newmoduleFile_raw.loc[:,newmoduleFile_raw.columns[0:5]] # all PV tech installs
installs_cSiPV_df = newmoduleFile_raw.loc[:,['Residential c-Si', 'Commercial c-Si', 'Utility c-Si',
                                          'All Sector c-Si Installs_[MWdc]']] # c-Si PV tech installs
installs_df = pd.concat([installs_allPV_df, installs_cSiPV_df], axis=1)


# In[8]:


installs_df.columns


# In[9]:


#load in a baseline and materials for modification
r1 = PV_ICE.Simulation(name='sim1', path=testfolder)
r1.createScenario(name='USHistory', massmodulefile=moduleFile) #points at the old module history installs file
for mat in range (0, len(MATERIALS)):
    MATERIALBASELINE = r'..\baselines\baseline_material_mass_'+MATERIALS[mat]+'.csv'
    r1.scenario['USHistory'].addMaterial(MATERIALS[mat], massmatfile=MATERIALBASELINE)


# ### Modify the Simulation, create scenarios for each install/deployment history
# Using the old/standard module baseline, we will modify/replace for each deployment schedule in the excel file. We will run the simulation for all tech and for just c-Si tech. For the all tech deployment, we will disregard the mass out since it it not representative of technologies (this will be improved in future). 

# In[10]:


scennames = installs_df.columns[1:]
#['Residential', 'Commercial', 'Utility', 'All Sector All Tech Installs_[MWdc]',
#             'Residential c-Si', 'Commercial c-Si', 'Utility c-Si', 'All Sector c-Si Installs_[MWdc]']
scennames


# In[11]:


for scens in scennames: #create all scenarios
    r1.createScenario(name=scens, massmodulefile=moduleFile) #create the scenario, name and mod file attach
    for mat in MATERIALS:
        materialfile = os.path.join(baselinesfolder, 'baseline_material_mass_'+str(mat)+'.csv')
        r1.scenario[scens].addMaterial(mat, massmatfile=materialfile) # add all materials listed in MATERIALS


# In[12]:


#modify the scenario for deployments
#IF WE GET SECTOR-wise T5-T90, modify here!
for scens in scennames:
    r1.scenario[scens].dataIn_m.loc[0:len(installs_df['year']-1),'new_Installed_Capacity_[MW]'] = installs_df[scens]

# make sure 2022 and forward installs = 0, change degradation, and remove circularity and MFG wastes
enddeploydat = installs_df['year'].iloc[-1]
r1.modifyScenario(scenarios=None, stage='new_Installed_Capacity_[MW]', value=0, start_year=enddeploydat)
r1.modifyScenario(scenarios=None, stage='mod_degradation', value=0.75, start_year=2016) #based on Jordan et al 2022 doi/pdf/10.1002/pip.3566
r1.scenMod_noCircularity() # sets all module and material circular variables to 0, creating fully linear
r1.scenMod_PerfectManufacturing() #sets all manufacturing values to 100% efficiency/yield ignoring MFG waste

#check:
#r1.scenario['USHistory'].material['glass'].materialdata['mat_MFG_eff']


# In[13]:


r1.scenario['Utility c-Si'].dataIn_m


# ### Run the Mass Flow Calculations on All Scenarios and Materials

# In[14]:


r1.calculateMassFlow()


# ###  Use internal plotting functions to plot results

# Pull out the keywords by printing the keys to the module data or the material data:
# 
#     print(r1.scenario.keys())
#     
#     print(r1.scenario['standard'].data.keys())
#     
#     print(r1.scenario['standard'].material['glass'].materialdata.keys())

# In[15]:


#print(r1.scenario.keys())
print(r1.scenario['USHistory'].dataOut_m.keys())
#print(r1.scenario['USHistory'].material['glass'].materialdata.keys())


# In[16]:


for scen in scennames:
    plt.plot(r1.scenario[scen].dataIn_m['year'], 
             r1.scenario[scen].dataOut_m['Installed_Capacity_[W]']/10e6, label=scen)

plt.title('Effective Capacity Annually')
plt.ylabel('Installed Cap [MW]')
plt.legend()


# In[17]:


usyearlyr1, uscumr1 = r1.aggregateResults()
usyearlyr1.to_csv('historicalUS-yearly.csv')
uscumr1.to_csv('historicalUS-cumulative.csv')


# Examine a specific year

# In[19]:


#subset result dataframes to look at all tech and just cSi and remove old USHistory file
usyearlyr1_sub = usyearlyr1[usyearlyr1.columns.drop(list(usyearlyr1.filter(like='USHistory')))]
yearlycSi_agg = usyearlyr1_sub.filter(like='c-Si')
yearlyallPV_agg = usyearlyr1_sub[usyearlyr1_sub.columns.difference(yearlycSi_agg.columns)]


# #### Area Equivilent Calcs

# In[20]:


keys = pd.DataFrame(r1.scenario['USHistory'].dataOut_m.keys())
import re
keys[keys[0].str.contains('area', flags=re.IGNORECASE)]


# In[21]:


for scen in scennames:
    plt.plot(r1.scenario[scen].dataIn_m['year'], 
             r1.scenario[scen].dataOut_m['Yearly_Sum_Area_disposed'], label=scen)

plt.title('Yearly sum Disposed')
plt.ylabel('Disposed Area [m2]')
plt.legend()


# In[22]:


#extract area disposed from simulation #should be m2
yearly_AreaDisposed_Results = pd.DataFrame()
for scen in scennames:
    temp = r1.scenario[scen].dataOut_m['Yearly_Sum_Area_disposed']
    yearly_AreaDisposed_Results = pd.concat([yearly_AreaDisposed_Results,temp], axis=1)


# In[23]:


yearly_AreaDisposed_Results.index = r1.scenario['Residential'].dataIn_m['year']
yearly_AreaDisposed_Results.columns = scennames
yearly_AreaDisposed_Results.tail()


# In[24]:


yearly_AreaDisposed_Results_cum = yearly_AreaDisposed_Results.cumsum()
yearly_AreaDisposed_Results_cum.tail()


# Now we take the area and divide it by 1.6 m2 or 2 m2 to approximate the # of modules. And Also extract the 2030 and 2050 values for area equivilence estimations.

# In[25]:


subset_areaDisposed_yearly = yearly_AreaDisposed_Results.loc[[2030,2050]]
subset_areaDisposed_cum = yearly_AreaDisposed_Results_cum.loc[[2030,2050]]


# In[26]:


subset_1pt6m2ModulesDisposed_yearly = subset_areaDisposed_yearly/1.6
subset_1pt6m2ModulesDisposed_cum = subset_areaDisposed_cum/1.6
subset_2m2ModulesDisposed_yearly = subset_areaDisposed_yearly/2
subset_2m2ModulesDisposed_cum = subset_areaDisposed_cum/2
idxmulti = pd.MultiIndex.from_arrays([['yearly','yearly','cumulative','cumulative'],['1.6m$^2$','2m$^2$','1.6m$^2$','2m$^2$']])
subset_NoModules = pd.concat([subset_1pt6m2ModulesDisposed_yearly,
           subset_2m2ModulesDisposed_yearly,
           subset_1pt6m2ModulesDisposed_cum,
           subset_2m2ModulesDisposed_cum],
         keys = idxmulti)
subset_NoModules.to_csv(path_or_buf=r'..\baselines\SupportingMaterial\US_Historical_NoModulesDisposed.csv')
subset_NoModules


# ### in 2022

# In[79]:


#annual
round(yearly_AreaDisposed_Results.loc[[2022]]/1.6,0)


# In[80]:


#cumulative
round(yearly_AreaDisposed_Results_cum.loc[[2022]]/1.6,0)


# In[27]:


AreaDisposed_Eq = pd.concat([subset_areaDisposed_yearly,subset_areaDisposed_cum], keys = ['yearly','cumulative'])
AreaDisposed_Eq.to_csv(path_or_buf=r'..\baselines\SupportingMaterial\US_Historical_AreaDisposed_EQ.csv')
AreaDisposed_Eq


# ## Pretty Plots

# In[28]:


#all techs plot
plt.plot([],[],color='blue', label='Residential')
plt.plot([],[],color='orange', label='Commercial')
plt.plot([],[],color='brown', label='Utility')


plt.stackplot(yearlyallPV_agg.index, 
              yearlyallPV_agg['ActiveCapacity_sim1_Residential_[MW]'], 
              yearlyallPV_agg['ActiveCapacity_sim1_Commercial_[MW]'],
              yearlyallPV_agg['ActiveCapacity_sim1_Utility_[MW]'], 
              colors = ['blue','orange','brown'])
plt.title('Effective Capacity All PV tech')
plt.ylabel('Effective Capacity [MWdc]')
plt.xlim(1995,2050)
plt.legend(loc='upper left')
plt.show()


# In[29]:


#cSi plot
plt.plot([],[],color='red', label='Residential')
plt.plot([],[],color='purple', label='Commercial')
plt.plot([],[],color='grey', label='Utility')


plt.stackplot(yearlycSi_agg.index, 
              yearlycSi_agg['ActiveCapacity_sim1_Residential c-Si_[MW]'], 
              yearlycSi_agg['ActiveCapacity_sim1_Commercial c-Si_[MW]'],
              yearlycSi_agg['ActiveCapacity_sim1_Utility c-Si_[MW]'], 
              colors = ['red','purple','grey'])
plt.title('Effective Capacity c-Si')
plt.ylabel('Effective Capacity [MWdc]')
plt.xlim(1995,2050)
plt.legend(loc='upper left')
plt.show()


# In[30]:


yearlyallPV_agg.filter(like='Decommisioned').columns


# In[31]:


#all techs plot
plt.plot([],[],color='blue', label='Residential')
plt.plot([],[],color='orange', label='Commercial')
plt.plot([],[],color='brown', label='Utility')


plt.stackplot(yearlyallPV_agg.index, 
              yearlyallPV_agg['DecommisionedCapacity_sim1_Residential_[MW]'], 
              yearlyallPV_agg['DecommisionedCapacity_sim1_Commercial_[MW]'],
              yearlyallPV_agg['DecommisionedCapacity_sim1_Utility_[MW]'], 
              colors = ['blue','orange','brown'])
plt.title('Decommissioned  Capacity All PV tech')
plt.ylabel('Cumulative Decommissioned Capacity [MWdc]')
plt.xlim(1995,2050)
plt.legend(loc='upper left')
plt.show()


# In[33]:


#cSi plot
plt.plot([],[],color='red', label='Residential')
plt.plot([],[],color='purple', label='Commercial')
plt.plot([],[],color='grey', label='Utility')


plt.stackplot(yearlycSi_agg.index, 
              yearlycSi_agg['DecommisionedCapacity_sim1_Residential c-Si_[MW]'], 
              yearlycSi_agg['DecommisionedCapacity_sim1_Commercial c-Si_[MW]'],
              yearlycSi_agg['DecommisionedCapacity_sim1_Utility c-Si_[MW]'], 
              colors = ['red','purple','grey'])
plt.title('Decommissioned Capacity c-Si')
plt.ylabel('Cumulative Decommissioned Capacity [MWdc]')
plt.xlim(1995,2050)
plt.legend(loc='upper left')
plt.show()


# In[34]:


cSiMatWastes_cum = uscumr1.filter(like='WasteAll').filter(like='c-Si').filter(like='All Sector')/1e6 #convert to million metric tonnes
cSiMatWastes_cum.columns


# In[35]:


#cSi plot
plt.plot([],[],color='aqua', label='glass')
plt.plot([],[],color='lightcoral', label='aluminium_frames')
plt.plot([],[],color='silver', label='silver')
plt.plot([],[],color='blue', label='silicon')
plt.plot([],[],color='orange', label='copper')
plt.plot([],[],color='purple', label='encapsulant')
plt.plot([],[],color='black', label='backsheet')


plt.stackplot(cSiMatWastes_cum.index, 
              cSiMatWastes_cum.iloc[:,0], 
              cSiMatWastes_cum.iloc[:,1],
              cSiMatWastes_cum.iloc[:,2],
              cSiMatWastes_cum.iloc[:,3],
              cSiMatWastes_cum.iloc[:,4],
              cSiMatWastes_cum.iloc[:,5],
              cSiMatWastes_cum.iloc[:,6],
              colors = ['aqua','lightcoral','silver','blue','orange','purple','black'])
plt.title('Cumulative c-Si Material Waste from All Sectors')
plt.ylabel('Cumulative Mass Waste [million metric tonnes]')
plt.xlim(1995,2050)
plt.legend(loc='upper left')
plt.show()


# In[36]:


#2050 stacked bar graph of cumulative waste by Material


# # Table of decommissioned in MW
# decommissioned yearly = cumulative new installs - yearly active capacity
# 
# the decommissioned yearly column is actually cumulative, so do reverse cum on it.
# 
# Create a table output of installs, active generating capacity annually decommissioned, cumulatively decomissioned, and cumulative decomissioned module mass.

# In[37]:


df_Capacity_all = usyearlyr1_sub[usyearlyr1_sub.filter(like='[MW]').columns]


# In[38]:


capacity_results_alltech = yearlyallPV_agg.filter(like='[MW]')
capacity_results_cSi = yearlycSi_agg.filter(like='[MW]')


# In[39]:


#caution, run this only once
for colname in df_Capacity_all.filter(like='Decommisioned').columns:
    df_Capacity_all[str('Annual_'+colname)] = df_Capacity_all[colname]-df_Capacity_all[colname].shift(1).fillna(0)


# In[40]:


df_Capacity_all.to_csv(path_or_buf=r'..\baselines\SupportingMaterial\US_Historical_PV_Decomissioning_Sectorwise.csv')


# ### Pull out the 2030 and 2050 Values of interest
# the request was for 2030 and 2050 values for decommissioning and cumulative c-Si waste, by sector. Create a table of just those results.

# In[41]:


subset_results_capacity = df_Capacity_all.filter(like='Decommisioned').loc[[2030,2050]]
subset_results_capacity.to_csv(path_or_buf=r'..\baselines\SupportingMaterial\US_Historical_PV_Decomissioning20302050_Sectorwise.csv')
round(subset_results_capacity.T,)


# In[42]:


cSiwaste_cum = uscumr1.filter(like='WasteAll_Module').filter(like='c-Si')/1e6 #convert to million metric tonnes
subset_results_waste = cSiwaste_cum.loc[[2030,2050]]
subset_results_waste.to_csv(path_or_buf=r'..\baselines\SupportingMaterial\US_Historical_PV_cSiWaste20302050_Sectorwise.csv')
round(subset_results_waste.T,2)


# ## 2022 Values

# In[74]:


subset_results_capacity = df_Capacity_all.filter(like='Decommisioned').loc[[2022]]
#subset_results_capacity.to_csv(path_or_buf=r'..\baselines\SupportingMaterial\US_Historical_PV_Decomissioning20302050_Sectorwise.csv')
round(subset_results_capacity.T,)


# In[76]:


cSiwaste_cum = uscumr1.filter(like='WasteAll_Module').filter(like='c-Si')#/1e6 #convert to million metric tonnes
subset_results_waste = cSiwaste_cum.loc[[2022]]
#subset_results_waste.to_csv(path_or_buf=r'..\baselines\SupportingMaterial\US_Historical_PV_cSiWaste20302050_Sectorwise.csv')
round(subset_results_waste.T,2)


# In[ ]:




