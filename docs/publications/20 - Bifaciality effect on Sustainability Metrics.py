#!/usr/bin/env python
# coding: utf-8

# # 20 - Bifacial effects on Sustainability Metrics
# 
# Close look at improvements in energy and carbon due to variying bifaciality 70 to 95%
# 

# ## 1. Setup and Create PV ICE Simulation Object

# In[1]:


import PV_ICE
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
PV_ICE.__version__


# In[2]:


# This information helps with debugging and getting support :)
import sys, platform
print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# In[3]:


testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'BifacialityStudy')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[4]:


r1 = PV_ICE.Simulation(name='Sim', path=testfolder, baselinepath=baselinesfolder); # Is it possible to define more than one simulation here?


# ## 3. Create standard and modified scenarios
# 

# In[5]:


r1.createScenario(name='standard', 
                  massmodulefile=r'baseline_modules_mass_World.csv', 
                  energymodulefile = 'baseline_modules_energy.csv' )

r1.scenario['standard'].addMaterial(materialname='glass', 
                                    massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_glass.csv'),
                                    energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_glass.csv'))

r1.scenario['standard'].addMaterial(materialname='silicon', 
                                    massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_silicon.csv'),
                                    energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_silicon.csv'))

r1.scenario['standard'].addMaterial(materialname='copper', 
                                    massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_copper.csv'),
                                    energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_copper.csv'))

r1.scenario['standard'].addMaterial(materialname='silver', 
                                    massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_silver.csv'),
                                    energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_silver.csv'))
r1.scenario['standard'].addMaterial(materialname='aluminium_frames', 
                                    massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_aluminium_frames.csv'),
                                    energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_aluminium_frames.csv'))

r1.scenario['standard'].addMaterial(materialname='encapsulant', 
                                    massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_encapsulant.csv'),
                                    energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_encapsulant.csv'))

r1.scenario['standard'].addMaterial(materialname='backsheet', 
                                    massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_backsheet.csv'),
                                    energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_backsheet.csv'))




# In[6]:


bififactorsfile = os.path.join(baselinesfolder, 'baseline_bifaciality_factor.csv')
bifioriginal = pd.read_csv(bififactorsfile)
bifiyearly = bifioriginal.set_index('Year')


# In[7]:


bifiFactors = {}
for ii in range(70, 101):
    bifiFactors[str(ii)]=ii


# In[8]:


bifioriginal = pd.read_csv(bififactorsfile)
bifiyearly = bifioriginal.set_index('Year')


# In[9]:


#PV ICE currently set up to read in a csv of bifi factors, so generate files to read in 
idx_temp = pd.RangeIndex(start=1995,stop=2050,step=1) #create the index
df_temp = pd.DataFrame(index=idx_temp, columns=['bifi'], dtype=float)
bifiPathDict={}

for f in bifiFactors.keys(): #loop over module types
    bifi = df_temp.copy() #copy of df
    bifi['bifi'] = bifiFactors[f]/100 #assign column
    bifi.loc[1995:2023]= bifiyearly.loc[1995:2023]
    bifipath = os.path.join(testfolder,'bifi_'+str(f)+'.csv') #create file path
    bifi.to_csv(path_or_buf=bifipath, index_label='year') #create file
    bifiPathDict[str(f)] = bifipath
    #append bifi path to dict? or list?

bifiPathDict;


# In[10]:


for f in bifiFactors.keys():
    r1.createScenario(name=f, 
                      massmodulefile=r'baseline_modules_mass_World.csv', 
                      energymodulefile = 'baseline_modules_energy.csv' )

    r1.scenario[f].addMaterial(materialname='glass', 
                                        massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_glass.csv'),
                                        energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_glass.csv'))

    r1.scenario[f].addMaterial(materialname='silicon', 
                                        massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_silicon.csv'),
                                        energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_silicon.csv'))

    r1.scenario[f].addMaterial(materialname='copper', 
                                        massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_copper.csv'),
                                        energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_copper.csv'))
    
    r1.scenario[f].addMaterial(materialname='silver', 
                                        massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_silver.csv'),
                                        energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_silver.csv'))
    r1.scenario[f].addMaterial(materialname='aluminium_frames', 
                                        massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_aluminium_frames.csv'),
                                        energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_aluminium_frames.csv'))

    r1.scenario[f].addMaterial(materialname='encapsulant', 
                                        massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_encapsulant.csv'),
                                        energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_encapsulant.csv'))

    r1.scenario[f].addMaterial(materialname='backsheet', 
                                        massmatfile=os.path.join(baselinesfolder, 'baseline_material_mass_backsheet.csv'),
                                        energymatfile=os.path.join(baselinesfolder, 'baseline_material_energy_backsheet.csv'))



# In[11]:


r1.calculateFlows(scenarios='standard', reducecapacity=False, bifacialityfactors=bififactorsfile)

for f in bifiFactors.keys():
    r1.calculateFlows(scenarios=f, reducecapacity=False, bifacialityfactors=bifiPathDict[f])


# In[12]:


USyearly, UScum = r1.aggregateResults()


# In[13]:


USyearly.to_csv('USyearly.csv')
UScum.to_csv('UScum.csv')


# In[14]:


r1.scenario['70'].dataOut_m['Effective_Capacity_[W]']


# In[15]:


allenergy, energyGen, energy_demands = r1.aggregateEnergyResults()
allenergy.to_csv('Energy_all.csv')
energyGen.to_csv('Energy_Generation.csv')
energy_demands.to_csv('Energy_demands.csv')


# In[16]:


r1.saveSimulation()
r1.pickle_Sim()


# ## Energy Plotting 

# In[17]:


annual_EoL = USyearly.filter(like='DecommisionedCapacity')
plt.plot(annual_EoL/1e6)
plt.legend(r1.scenario.keys())
plt.ylabel('Annual EoL [TW]')
plt.title('Annual Decommissions [TW]')
plt.ylim(0,)


# In[18]:


recycledperc_virginstock = UScum.filter(like='VirginStock')#.filter(like='Recycled')
#recycledperc_virginstock.drop('VirginStock_Module_sim1_h_RecycledPERC_[Tonnes]',axis=1, inplace=True)
plt.bar(recycledperc_virginstock.columns, recycledperc_virginstock.loc[2050]/1e6)# tick_label = MATERIALS, color=colormats)
plt.ylabel('Million Metric tonnes')
plt.xticks(rotation=45)


# In[19]:


e_annual_sumDemands = energy_demands.filter(like='demand_total')


# In[20]:


e_annual_sumDemands_TWh = e_annual_sumDemands/1e12

fig, ax1 = plt.subplots()

#world electricity demand
#ax1.plot(world_elec_demand.iloc[0:2022,0], label='Global Electricity Demand', ls='dashdot')

#BAU
ax1.plot(e_annual_sumDemands_TWh.iloc[:,0:2])

#ax1.legend(scennames_labels_flat)
plt.title('Annual Energy Demands')
plt.ylabel('Energy Demands\n[TWh]')
plt.ylim(0,)
plt.xlim(2000,2050)

plt.show()


# In[21]:


e_annual_sumDemands_cumu = e_annual_sumDemands.cumsum()


# In[22]:


scennames_labels = ['Baseline', 'Extreme']
cumu_e_demands_twh = e_annual_sumDemands_cumu.loc[2050]/1e12
cumu_e_demands_twh


# In[23]:


scenenames_labels_flat = ['baseline']

for f in bifiFactors.keys():
    scenenames_labels_flat.append(f)


# In[24]:


energyGen_cumu = energyGen.cumsum()
e_annual_sumDemands_cumu.columns=e_annual_sumDemands_cumu.columns.str.rstrip('_e_demand_total')
energyGen_cumu.columns = energyGen_cumu.columns.str.strip('e_out_annual[Wh]')
e_annual_sumDemands_cumu = e_annual_sumDemands_cumu.rename(columns={'standar':'standard'})

#energyGen_cumu.columns = e_annual_sumDemands_cumu.columns = scennames_labels_flat
netEnergy_cumu = energyGen_cumu.loc[[2049]] - e_annual_sumDemands_cumu.loc[[2049]]


# In[26]:


cumu_netEnergy_twh = netEnergy_cumu.loc[2049]/1e15

fig, (ax0) = plt.subplots(1,1,figsize=(11,6), sharey=True, 
                                      gridspec_kw={'wspace': 0, 'width_ratios': [1]})
ax0.plot(cumu_netEnergy_twh[1::])
ax0.set_ylabel('Cumulative Net Energy\n[thousand TWh]', fontsize=20)


# In[27]:


print("Cumulative net Energy baseline", cumu_netEnergy_twh[0], " thousan TWh")
print("Change in net Energy for every % improvmeent", (cumu_netEnergy_twh.iloc[3]-cumu_netEnergy_twh.iloc[2])*1000, " Twh")


# In[28]:


foo = netEnergy_cumu/netEnergy_cumu['70'].loc[2049]
foo = foo.T


# In[29]:


plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.figsize'] = (8, 6)


# In[30]:


listyears=[]
fooval = []
for ii in range(70, 101):
        listyears.append(ii)
        fooval.append(foo.loc['standard'][2049])


# In[31]:


fig, (ax0) = plt.subplots(1,1,figsize=(9,6), sharey=True, 
                                      gridspec_kw={'wspace': 0, 'width_ratios': [1]})
ax0.plot(listyears,foo[1::])
ax0.set_ylabel('Normalized Cumulative Net Energy by 2050\ ', fontsize=14)
#ax0.plot(listyears,fooval)
ax0.set_xlabel('Bifaciality Factor')
#ax0.set_title('Cumulative Net Energy produced by 2050, \nassuming PV installations become bifacial at specific bifaciality factor starting 2024')


# In[ ]:




