#!/usr/bin/env python
# coding: utf-8

# # Energy in the Balance: PV reliability to power the Energy Transition
# 
# This journal documents the analysis presented at PVRW 2023 by Heather Mirletz. We explore the energy balance as it is effected by the different aspects of PV reliability, or un-reliability. We will use the PV ICE tool baseline and assume immortal PV modules. Then we will add in predicted degradation, and examine the new deployment, mass, and energy requirements to meet energy transition targets. Next we will add in Weibull controlled failures, and finally economic project lifetimes to examine repowering problems.
# 
# Through this we will identify the key aspects of PV reliability to emphasize for easing the challenge of energy transition.

# In[5]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
import PV_ICE

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'PVRW2023')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[6]:


#print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("pyplot ", plt.matplotlib.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# In[7]:


#https://www.learnui.design/tools/data-color-picker.html#palette
#color pallette - modify here for all graphs below
colorpalette=['#0079C2','#00A4E4','#F7A11A','#5D9732','#933C06','#5E6A71'] # 
import matplotlib as mpl #import matplotlib
from cycler import cycler #import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=colorpalette) #reset the default color palette of mpl

plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.figsize'] = (8, 6)

scennames_labels = ['PV ICE','Immortal','Degradation','Failures','Project Life'] #


# In[8]:


#gradient generator
def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

color1 = '#0079C2'
color2 = '#F7A11A'


# Scenarios and Materials

# In[9]:


#creating scenarios
scennames = ['PV ICE','Immortal','Degradation','Failures','ProjectLife']
MATERIALS = ['glass','silver','silicon', 'copper', 'aluminium_frames'] #'encapsulant', 'backsheet',
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[10]:


#load in a baseline and materials for modification


sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames:
    sim1.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim1.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# ## Modify Scenarios

# ### Immortal

# In[11]:


# Immortal

#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('Immortal', 'mod_degradation', 0.0, start_year=2022) #
#Mod Project Lifetime
sim1.modifyScenario('Immortal', 'mod_lifetime', 200, start_year=2022) #
#T50
sim1.modifyScenario('Immortal', 'mod_reliability_t50', 250, start_year=2022)
#t90
sim1.modifyScenario('Immortal', 'mod_reliability_t90', 280, start_year=2022) 



# ### Degradation

# In[12]:


# Degradation

#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('Degradation', 'mod_degradation', 0.7, start_year=2022) # Jordan et al 2022
#Mod Project Lifetime
sim1.modifyScenario('Degradation', 'mod_lifetime', 200, start_year=2022) #
#T50
sim1.modifyScenario('Degradation', 'mod_reliability_t50', 250, start_year=2022)
#t90
sim1.modifyScenario('Degradation', 'mod_reliability_t90', 280, start_year=2022) 


# ### Failures

# In[13]:


# Failures

#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('Failures', 'mod_degradation', 0.7, start_year=2022) # Jordan et al 2022
#Mod Project Lifetime
sim1.modifyScenario('Failures', 'mod_lifetime', 200, start_year=2022) #
#T50
sim1.modifyScenario('Failures', 'mod_reliability_t50', 32, start_year=2022) #for a 30 year module
#t90
sim1.modifyScenario('Failures', 'mod_reliability_t90', 36, start_year=2022) #for a 30 year module


# ### Project Lifetime/Repowering

# In[14]:


# Project Lifetime/Repowering

#Lifetime and Degradation
#values taken from lifetime vs recycling paper
#degradation rate:
sim1.modifyScenario('ProjectLife', 'mod_degradation', 0.7, start_year=2022) # Jordan et al 2022
#Mod Project Lifetime
sim1.modifyScenario('ProjectLife', 'mod_lifetime', 30, start_year=2022) #30 year project life
#T50
sim1.modifyScenario('ProjectLife', 'mod_reliability_t50', 32, start_year=2022) #for a 30 year module
#t90
sim1.modifyScenario('ProjectLife', 'mod_reliability_t90', 36, start_year=2022) #for a 30 year module


# Modify Years

# In[15]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim1.trim_Years(startYear=2000, endYear=2100)


# # Global Deployment Projection

# In[17]:


global_projection = pd.read_csv(os.path.join(supportMatfolder,'input-globalDeploymentProjection-HieslmairPlus.csv'), index_col=0)
#global_projection = pd.read_csv(os.path.join(supportMatfolder,'output-globalInstallsProjection.csv'), index_col=0)
#global_projection = pd.read_csv(os.path.join(supportMatfolder,'input-expotoflatGlobalInstallsProjection.csv'), index_col=0)

#global_projection = pd.read_csv(os.path.join(supportMatfolder,'output-globalInstallsProjection.csv'), index_col=0)

fig, ax1 = plt.subplots()

ax1.plot(global_projection['World_Cumu_[MW]']/1e6, color='orange')
ax1.set_ylabel('Cumulative Solar Capacity [TW]', color='orange')
ax2 = ax1.twinx()
ax2.plot(global_projection['World_Annual_[MW]']/1e6)
ax2.set_ylabel('Annual Installations [TW]')
plt.show()


# Single Install in time

# In[18]:


idx_temp = pd.RangeIndex(start=2000,stop=2101,step=1) #create the index
single_deploy_2025 = pd.DataFrame(index=idx_temp, columns=['MW'], dtype=float)
single_deploy_2025['MW'] = 0.0
single_deploy_2025.loc[2025,'MW'] = 100.0


# In[20]:


#deployment projection for all scenarios
sim1.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', 
                    value=global_projection['World_Annual_[MW]'], start_year=2000) #
#single deployment: single_deploy_2025['MW']
#global deployment: global_projection['World_annual_[MWdc]']


# ## Run Simulation - No Replacements

# In[21]:


sim1.calculateFlows()
#sim1.calculateFlows(scenarios=['CheapCrap'], weibullInputParams=cheapcrapweibull)


# In[22]:


sim1.scenario['PV ICE'].dataOut_m.to_pickle('dataOut_m.pkl')
sim1.scenario['PV ICE'].dataIn_m.to_pickle('dataIn_m.pkl')
sim1.scenario['PV ICE'].dataOut_e.to_pickle('dataOut_e.pkl')
sim1.scenario['PV ICE'].dataIn_e.to_pickle('dataIn_e.pkl')
sim1.scenario['PV ICE'].material['silicon'].matdataIn_e.to_pickle('matdataIn_e.pkl')
sim1.scenario['PV ICE'].material['silicon'].matdataIn_m.to_pickle('matdataIn_m.pkl')
sim1.scenario['PV ICE'].material['silicon'].matdataOut_e.to_pickle('matdataOut_e.pkl')
sim1.scenario['PV ICE'].material['silicon'].matdataOut_m.to_pickle('matdataOut_m.pkl')


# In[23]:


ii_yearly, ii_cumu = sim1.aggregateResults() #have to do this to get auto plots
ii_allenergy, ii_energyGen, ii_energy_demands = sim1.aggregateEnergyResults()


# In[24]:


effective_capacity = ii_yearly.filter(like='ActiveCapacity')
#plt.plot(ii_cumu['newInstalledCapacity_sim1_PV_ICE_[MW]']/1e6, label='Capacity Target', color='black', ls='--')
plt.plot(effective_capacity.iloc[:,1:5]/1e6, label=scennames_labels[1:5])
plt.legend(loc='center left')
plt.ylabel('Effective Capacity [TW]')
plt.title('Effective Capacity: No Replacements')
#plt.ylim(0,)


# Note to self: changing the degradation of nameplate to 80% instead of 50% kill threshold did not change the above result

# In[ ]:





# ## Run Simulation - Replacements

# In[25]:


#currently takes 15 mins to run with 5 mateirals and 5 scenarios

for row in range (0,len(sim1.scenario['PV ICE'].dataIn_m)): #loop over length of years
    for scen in scennames: #loop over scenarios
        Under_Installment = global_projection.iloc[row,0] - ((sim1.scenario[scen].dataOut_m['Effective_Capacity_[W]'][row])/1e6)  # MWATTS
        sim1.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][row] += Under_Installment #overwrite new installed
        #calculate flows for that scenario with it's bifi factor and modified weibull
        sim1.calculateFlows(scenarios=[scen]) # , bifacialityfactors=bifiPathDict[scen]


# In[ ]:


cc_yearly, cc_cumu = sim1.aggregateResults() #have to do this to get auto plots
allenergy, energyGen, energy_demands = sim1.aggregateEnergyResults()


# In[ ]:


effective_capacity = cc_yearly.filter(like='ActiveCapacity')
#plt.plot(ii_cumu['newInstalledCapacity_sim1_PV_ICE_[MW]']/1e6, label='Capacity Target', color='black', ls='--')
plt.plot(effective_capacity, label=scennames_labels)
plt.legend()
plt.ylabel('Effective Capacity [TW]')
plt.title('Effective Capacity: No Replacements')
#plt.ylim(0,)


# ### Cumulative Installs with Replacements

# In[ ]:


cumu_installs = cc_cumu.filter(like='newInstalled')
plt.bar(scennames, cumu_installs.loc[2100]/1e6, tick_label=scennames_labels, color=colorpalette)
#plt.legend(scennames)
plt.ylabel('Cumulative installed [TW]')
plt.title('Cumulative Installs with Replacements')
plt.ylim(0,160)


# In[ ]:


cumu_installs.loc[2100]/1e6


# In[ ]:


e_annual_sumDemands = energy_demands.filter(like='demand_total')
e_annual_sumDemands_cumu = e_annual_sumDemands.cumsum()
energyGen_cumu = energyGen.cumsum()
energyGen_cumu.columns = e_annual_sumDemands_cumu.columns = scennames
netEnergy_cumu = energyGen_cumu.loc[[2100]] - e_annual_sumDemands_cumu.loc[[2100]]


# In[ ]:


plt.bar(netEnergy_cumu.columns, netEnergy_cumu.loc[2100]/1e12, 
        tick_label=(scennames_labels), color=colorpalette)
plt.title('Net Energy Cumulatively with Replacements')
plt.ylabel('Cumulative Net Energy [TWh]')
plt.ylim(4e6,5.5e6)


# In[ ]:


eroi = energyGen_cumu.loc[[2100]] / e_annual_sumDemands_cumu.loc[[2100]]

plt.bar(eroi.columns, eroi.loc[2100], 
        tick_label=(scennames), color=colorpalette)
plt.title('EROI ')
plt.ylabel('Arbitrary units')


# In[ ]:


eroi


# # Explore Degradation
# explore effect of the range of degradation rates as presented in Jordan et al 2022

# In[26]:


# from Jordan et al 2022: -1.9%/yr is lowest (P90), will do one more for visual effect
#25% quartile is -0.55% for PERC
#outliers read in up to +0.5%
Degradation_Range = round(pd.Series(np.linspace(0.1,2.0, num=20)), 1)
#Degradation_Range


# In[27]:


sim2 = PV_ICE.Simulation(name='sim2_deg', path=testfolder) #init simulation

for degs in range(0,len(Degradation_Range)):
        scenname = 'deg_' + str(Degradation_Range[degs])+'%/yr' #name the scenario
        sim2.createScenario(name=scenname, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e) #create the scenario with name
        for mat in range (0, len(MATERIALS)):
            matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
            matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
            sim2.scenario[scenname].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[28]:


scennames2 = pd.Series(sim2.scenario.keys())
scennames2


# In[29]:


# Degradation

#Lifetime and Degradation
# use scenarios is none to set all
#Mod Project Lifetime
sim2.modifyScenario(scenarios=None, stage='mod_lifetime', value=200, start_year=2022) #
#T50
sim2.modifyScenario(scenarios=None, stage='mod_reliability_t50', value=250, start_year=2022)
#t90
sim2.modifyScenario(scenarios=None, stage='mod_reliability_t90', value=280, start_year=2022) 


# In[30]:


#degradation rates:
#modify scenarios with dictionary of deg rates range from Jordan et al 2022

for scen in range(0,len(scennames2)):
    sim2.modifyScenario(scennames2[scen], 'mod_degradation', Degradation_Range[scen], start_year=2022) # Jordan et al 2022


# In[31]:


sim2.scenario['deg_1.6%/yr'].dataIn_m.tail(2)


# In[32]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim2.trim_Years(startYear=2000, endYear=2100)

#deployment projection for all scenarios
sim2.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', 
                    value=global_projection['World_Annual_[MW]'], start_year=2000) #
#single deployment: single_deploy_2025['MW']
#global deployment: global_projection['World_annual_[MWdc]']


# In[33]:


sim2.calculateFlows(nameplatedeglimit=0.8)


# In[34]:


sim2_ii_yearly, sim2_ii_cumu = sim2.aggregateResults() #have to do this to get auto plots
sim2_ii_allenergy, sim2_ii_energyGen, sim2_ii_energy_demands = sim2.aggregateEnergyResults()


# In[37]:


effective_capacity = sim2_ii_yearly.filter(like='ActiveCapacity')
#plt.plot(ii_cumu['newInstalledCapacity_sim1_PV_ICE_[MW]']/1e6, label='Capacity Target', color='black', ls='--')
    
#plt.plot(effective_capacity/1e6)
#plt.legend()
#plt.ylabel('Effective Capacity [TW]')
#plt.title('Effective Capacity: No Replacements')
#plt.ylim(0,)

colors = get_color_gradient(color1, color2, len(scennames2)) #generates a list of hex values
effective_capacity_tw = effective_capacity/1e6
effective_capacity_tw.plot(color=colors, legend=False, title='Effective Capacity: No Replacements')
plt.plot(ii_cumu['newInstalledCapacity_sim1_Immortal_[MW]']/1e6, label='Capacity Target', color='black', ls='--') 
plt.ylim(0,)


# In[38]:


plt.plot(ii_cumu['newInstalledCapacity_sim1_Immortal_[MW]']/1e6, label='Capacity Target', color='black', ls='--')
plt.ylabel('Effective Capacity [TW]')
plt.xlabel('year')
plt.title('Effective Capacity: No Replacements')


# In[39]:


colors = get_color_gradient(color1, color2, len(scennames2)) #generates a list of hex values

effective_capacity_tw = effective_capacity/1e6
for scen in range(0,len(scennames2)):
    effective_capacity_tw.iloc[:,0:scen+1].plot(color=colors, legend=False, title='Effective Capacity: No Replacements')
    plt.plot(ii_cumu['newInstalledCapacity_sim1_Immortal_[MW]']/1e6, label='Capacity Target', color='black', ls='--') 
    plt.ylim(0,)
    plt.ylabel('Effective Capacity [TW]')
    plt.savefig(os.path.join(testfolder, 'deg'+str(scen)))
    
#plt.title('Effective Capacity: No Replacements')


# In[40]:


for row in range (0,len(sim2.scenario['deg_1.5%/yr'].dataIn_m)): #loop over length of years
    for scen in scennames2: #loop over scenarios
        Under_Installment = global_projection.iloc[row,0] - ((sim2.scenario[scen].dataOut_m['Effective_Capacity_[W]'][row])/1e6)  # MWATTS
        sim2.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][row] += Under_Installment #overwrite new installed
        #calculate flows for that scenario with it's bifi factor and modified weibull
        sim2.calculateFlows(scenarios=[scen], nameplatedeglimit=0.8) # , bifacialityfactors=bifiPathDict[scen]


# In[41]:


sim2_cc_yearly, sim2_cc_cumu = sim2.aggregateResults() #have to do this to get auto plots
sim2_allenergy, sim2_energyGen, sim2_energy_demands = sim2.aggregateEnergyResults()


# In[42]:


sim2_cc_yearly.to_csv(os.path.join(testfolder,'deg_cc_yearly_m.csv'))
sim2_cc_cumu.to_csv(os.path.join(testfolder,'deg_cc_cumu_m.csv'))
sim2_allenergy.to_csv(os.path.join(testfolder,'deg_cc_allE.csv'))
sim2_energyGen.to_csv(os.path.join(testfolder,'deg_cc_Egen.csv'))
sim2_energy_demands.to_csv(os.path.join(testfolder,'deg_cc_Edemand.csv'))


# In[ ]:


cumu_installs = sim2_cc_cumu.filter(like='newInstalled')
plt.barh(scennames2[::-1], cumu_installs.loc[2100,::-1]/1e6, color=colors[::-1])
#plt.legend(scennames)
plt.xlabel('Cumulative installed [TW]')
plt.title('Cumulative Installs with Replacements')
#plt.ylim(0,160)
#plt.xticks(rotation=90)


# In[ ]:


(cumu_installs.loc[2100,'newInstalledCapacity_sim2_deg_deg_2.0%/yr_[MW]']-cumu_installs.loc[2100,'newInstalledCapacity_sim2_deg_deg_0.7%/yr_[MW]'])/1e6


# In[ ]:


(cumu_installs.loc[2100,'newInstalledCapacity_sim2_deg_deg_0.1%/yr_[MW]']-cumu_installs.loc[2100,'newInstalledCapacity_sim2_deg_deg_0.7%/yr_[MW]'])/1e6


# In[ ]:


(cumu_installs.loc[2100,'newInstalledCapacity_sim2_deg_deg_0.6%/yr_[MW]']-cumu_installs.loc[2100,'newInstalledCapacity_sim2_deg_deg_0.7%/yr_[MW]'])/1e6


# In[ ]:


(cumu_installs.loc[2100,'newInstalledCapacity_sim2_deg_deg_0.8%/yr_[MW]']-cumu_installs.loc[2100,'newInstalledCapacity_sim2_deg_deg_0.7%/yr_[MW]'])/1e6


# In[ ]:


#sim2_allenergy, sim2_energyGen, sim2_energy_demands
e_annual_sumDemands = sim2_energy_demands.filter(like='demand_total')
e_annual_sumDemands_cumu = e_annual_sumDemands.cumsum()
energyGen_cumu = sim2_energyGen.cumsum()
energyGen_cumu.columns = e_annual_sumDemands_cumu.columns = scennames2
netEnergy_cumu = energyGen_cumu.loc[[2100]] - e_annual_sumDemands_cumu.loc[[2100]]


# In[ ]:


eroi = energyGen_cumu.loc[[2100]] / e_annual_sumDemands_cumu.loc[[2100]]

plt.barh(eroi.columns[::-1], eroi.loc[2100,::-1], 
        tick_label=(scennames2[::-1]), color=colors[::-1])
plt.title('EROI ')
plt.xlabel('Arbitrary units')
#plt.xticks(rotation=90)


# # Explore Failures
# Explore the effect of the range of failures from Heislmair and IRENA

# In[8]:


weibulls= {'class_a':[2.810, 100.238], 
           'class_b':[3.841,57.491], 
           'class_c':[4.602,40.767], 
           'class_d':[5.692,29.697], 
           'regular loss':[5.3759,30],
           'early loss':[2.4928,30]}
#weibulls[scen]
weibullist = list(weibulls.keys())
weibullsdf = pd.DataFrame(weibulls, index=['alpha','beta'])
#weibullist[0]


# In[9]:


for col in weibullist:
    a = weibullsdf.loc['alpha', col]
    b = weibullsdf.loc['beta', col]
    cdf = PV_ICE.weibull_cdf_vis(a, b,xlim=100)
    plt.plot(cdf, label=col)
#plt.legend(weibullist)
plt.title('Weibull Failure CDF')
plt.ylabel('Probability')
plt.xlabel('Years')


# In[10]:


sim3 = PV_ICE.Simulation(name='sim3_fail', path=testfolder) #init simulation

for var in range(0,len(weibulls)):
        scenname = str(weibullist[var]) #name the scenario
        sim3.createScenario(name=scenname, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e) #create the scenario with name
        for mat in range (0, len(MATERIALS)):
            matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
            matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
            sim3.scenario[scenname].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[11]:


scennames3 = sim3.scenario.keys()


# In[12]:


#Mod Project Lifetime on all 
sim3.modifyScenario(scenarios=None, stage='mod_lifetime', value=200, start_year=2022) #
#degradation rate:
sim3.modifyScenario(scenarios=None, stage='mod_degradation', value=0.0, start_year=2022)


# In[13]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim3.trim_Years(startYear=2000, endYear=2100)

#deployment projection for all scenarios
sim3.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', 
                    value=global_projection['World_annual_[MWdc]'], start_year=2000) #
#single deployment: single_deploy_2025['MW']
#global deployment: global_projection['World_annual_[MWdc]']


# In[14]:


for scen in scennames3:
    sim3.calculateFlows(scenarios=[scen], weibullInputParams=dict(weibullsdf[scen].T))


# In[15]:


sim3_ii_yearly, sim3_ii_cumu = sim3.aggregateResults() #have to do this to get auto plots
sim3_ii_allenergy, sim3_ii_energyGen, sim3_ii_energy_demands = sim3.aggregateEnergyResults()


# In[21]:


effective_capacity = sim3_ii_yearly.filter(like='ActiveCapacity')
#effective_capacity_tw = effective_capacity/1e6
#effective_capacity_tw.plot(color=colors, legend=False, title='Effective Capacity: No Replacements')

plt.plot(ii_cumu['newInstalledCapacity_sim1_Immortal_[MW]']/1e6, label='Capacity Target', color='black', ls='--')    
plt.plot(effective_capacity/1e6, label=scennames3)
plt.legend()
plt.ylabel('Effective Capacity [TW]')
plt.title('Effective Capacity: No Replacements')
plt.ylim(0,)


# In[22]:


effective_capacity_tw = effective_capacity/1e6



for scen in range(0,len(scennames3)):
    effective_capacity_tw.iloc[:,0:scen+1].plot(color=colorpalette, legend=False, title='Effective Capacity: No Replacements')
    plt.plot(ii_cumu['newInstalledCapacity_sim1_Immortal_[MW]']/1e6, label='Capacity Target', color='black', ls='--')
    plt.ylim(0,)
    plt.ylabel('Effective Capacity [TW]')
    #plt.legend(scennames3)
    plt.savefig(os.path.join(testfolder, 'fail'+str(scen)))
    
#plt.title('Effective Capacity: No Replacements')


# In[ ]:





# In[23]:


for row in range (0,len(sim3.scenario['class_a'].dataIn_m)): #loop over length of years
    for scen in scennames3: #loop over scenarios
        Under_Installment = global_projection.iloc[row,0] - ((sim3.scenario[scen].dataOut_m['Effective_Capacity_[W]'][row])/1e6)  # MWATTS
        sim3.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][row] += Under_Installment #overwrite new installed
        #calculate flows for that scenario with it's bifi factor and modified weibull
        sim3.calculateFlows(scenarios=[scen], weibullInputParams=dict(weibullsdf[scen].T))


# In[24]:


sim3_cc_yearly, sim3_cc_cumu = sim3.aggregateResults() #have to do this to get auto plots
sim3_allenergy, sim3_energyGen, sim3_energy_demands = sim3.aggregateEnergyResults()


# In[25]:


sim3_cc_yearly.to_csv(os.path.join(testfolder,'fail_cc_yearly_m.csv'))
sim3_cc_cumu.to_csv(os.path.join(testfolder,'fail_cc_cumu_m.csv'))
sim3_allenergy.to_csv(os.path.join(testfolder,'fail_cc_allE.csv'))
sim3_energyGen.to_csv(os.path.join(testfolder,'fail_cc_Egen.csv'))
sim3_energy_demands.to_csv(os.path.join(testfolder,'fail_cc_Edemand.csv'))


# In[28]:


effective_capacity = sim3_cc_yearly.filter(like='ActiveCapacity')
#effective_capacity_tw = effective_capacity/1e6
#effective_capacity_tw.plot(color=colors, legend=False, title='Effective Capacity: No Replacements')

#plt.plot(ii_cumu['newInstalledCapacity_sim1_Immortal_[MW]']/1e6, label='Capacity Target', color='black', ls='--')    
plt.plot(effective_capacity/1e6, label=scennames3)
plt.legend()
plt.ylabel('Effective Capacity [TW]')
plt.title('Effective Capacity: No Replacements')
plt.ylim(0,)


# In[ ]:


cumu_installs = sim3_cc_cumu.filter(like='newInstalled')
plt.bar(scennames3, cumu_installs.loc[2100]/1e6, color=colorpalette)
#plt.legend(scennames3)
plt.ylabel('Cumulative installed [TW]')
plt.title('Cumulative Installs with Replacements')
#plt.ylim(0,160)
plt.xticks(rotation=45)


# In[ ]:


cumu_installs.loc[2100]/1e6


# In[ ]:


(cumu_installs.loc[2100,'newInstalledCapacity_sim3_fail_class_a_[MW]'] - cumu_installs.loc[2100,'newInstalledCapacity_sim3_fail_early loss_[MW]'])/1e6


# In[ ]:


#sim3_allenergy, sim3_energyGen, sim3_energy_demands 
e_annual_sumDemands = sim3_energy_demands.filter(like='demand_total')
e_annual_sumDemands_cumu = e_annual_sumDemands.cumsum()
energyGen_cumu = sim3_energyGen.cumsum()
energyGen_cumu.columns = e_annual_sumDemands_cumu.columns = scennames3
netEnergy_cumu = energyGen_cumu.loc[[2100]] - e_annual_sumDemands_cumu.loc[[2100]]


# In[ ]:


e_annual_sumDemands_cumu.loc[2100]


# In[ ]:


energyGen_cumu.loc[2100]


# In[ ]:


eroi = energyGen_cumu.loc[[2100]] / e_annual_sumDemands_cumu.loc[[2100]]

plt.bar(eroi.columns, eroi.loc[2100], tick_label=eroi.columns, color=colorpalette)
plt.title('EROI ')
plt.ylabel('Arbitrary units')
plt.xticks(rotation=45)


# In[ ]:


eroi


# # Explore Project Life / Repowering
# Explore if repowering happens at varying lifetimes

# In[ ]:


# years of project life: 8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 45, 50
lifes = pd.Series([8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 45, 50])
switchindex = lifes.index
lifes = lifes[::-1]
lifes.index = switchindex
#lifes


# In[ ]:


sim4 = PV_ICE.Simulation(name='sim4_projectlife', path=testfolder) #init simulation

for var in range(0,len(lifes)):
        scenname = str(lifes[var])+ ' years' #name the scenario
        sim4.createScenario(name=scenname, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e) #create the scenario with name
        for mat in range (0, len(MATERIALS)):
            matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
            matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
            sim4.scenario[scenname].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[ ]:


scennames4 = list(sim4.scenario.keys())
scennames4


# In[ ]:


#Mod Project Lifetime on all 
for scen in range(0,len(scennames4)):
    sim4.modifyScenario(scenarios=scennames4[scen], stage='mod_lifetime', value=lifes[scen], start_year=2022) #


# In[ ]:


#degradation rate:
sim4.modifyScenario(scenarios=None, stage='mod_degradation', value=0.0, start_year=2022) 
#T50
sim4.modifyScenario(scenarios=None, stage='mod_reliability_t50', value=250, start_year=2022)
#t90
sim4.modifyScenario(scenarios=None, stage='mod_reliability_t90', value=280, start_year=2022) 


# In[ ]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim4.trim_Years(startYear=2000, endYear=2100)

#deployment projection for all scenarios
sim4.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', 
                    value=global_projection['World_annual_[MWdc]'], start_year=2000) #
#single deployment: single_deploy_2025['MW']
#global deployment: global_projection['World_annual_[MWdc]']


# In[ ]:


sim4.scenario['35 years'].dataIn_m.tail(3)


# In[ ]:


sim4.calculateFlows()


# In[ ]:


sim4_ii_yearly, sim4_ii_cumu = sim4.aggregateResults() #have to do this to get auto plots
sim4_ii_allenergy, sim4_ii_energyGen, sim4_ii_energy_demands = sim4.aggregateEnergyResults()


# In[ ]:


effective_capacity = sim4_ii_yearly.filter(like='ActiveCapacity')
#effective_capacity_tw = effective_capacity/1e6
#effective_capacity_tw.plot(color=colors, legend=False, title='Effective Capacity: No Replacements')

plt.plot(ii_cumu['newInstalledCapacity_sim1_Immortal_[MW]']/1e6, label='Capacity Target', color='black', ls='--')    
plt.plot(effective_capacity/1e6, label=scennames4)
plt.legend()
plt.ylabel('Effective Capacity [TW]')
plt.title('Effective Capacity: No Replacements')
#plt.ylim(0,)


# In[ ]:


colors4 = get_color_gradient(color2, color1, len(scennames4)) #generates a list of hex values
effective_capacity_tw = effective_capacity/1e6
effective_capacity_tw.plot(color=colors4, legend=False, title='Effective Capacity: No Replacements')
plt.plot(ii_cumu['newInstalledCapacity_sim1_Immortal_[MW]']/1e6, label='Capacity Target', color='black', ls='--')
plt.ylim(0,)
#plt.legend(scennames4)


# In[ ]:


for scen in range(0,len(scennames4)):
    effective_capacity_tw.iloc[:,0:scen+1].plot(color=colors4[::-1], legend=False, title='Effective Capacity: No Replacements')
    plt.plot(ii_cumu['newInstalledCapacity_sim1_Immortal_[MW]']/1e6, label='Capacity Target', color='black', ls='--') 
    plt.ylim(0,)
    plt.ylabel('Effective Capacity [TW]')
    plt.savefig(os.path.join(testfolder, 'life'+str(scen)))


# #### Install comp

# In[ ]:


for row in range (0,len(sim4.scenario['8 years'].dataIn_m)): #loop over length of years
    for scen in scennames4: #loop over scenarios
        Under_Installment = global_projection.iloc[row,0] - ((sim4.scenario[scen].dataOut_m['Installed_Capacity_[W]'][row])/1e6)  # MWATTS
        sim4.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][row] += Under_Installment #overwrite new installed
        #calculate flows for that scenario with it's bifi factor and modified weibull
    sim4.calculateFlows()


# In[ ]:


sim4_cc_yearly, sim4_cc_cumu = sim4.aggregateResults() #have to do this to get auto plots
sim4_allenergy, sim4_energyGen, sim4_energy_demands = sim4.aggregateEnergyResults()


# In[ ]:


sim4_cc_yearly.to_csv(os.path.join(testfolder,'life_cc_yearly_m.csv'))
sim4_cc_cumu.to_csv(os.path.join(testfolder,'life_cc_cumu_m.csv'))
sim4_allenergy.to_csv(os.path.join(testfolder,'life_cc_allE.csv'))
sim4_energyGen.to_csv(os.path.join(testfolder,'life_cc_Egen.csv'))
sim4_energy_demands.to_csv(os.path.join(testfolder,'life_cc_Edemand.csv'))


# In[ ]:


cumu_installs = sim4_cc_cumu.filter(like='newInstalled')
plt.barh(scennames4[::-1], cumu_installs.loc[2100,::-1]/1e6, color=colors4)
#plt.legend(scennames)
plt.xlabel('Cumulative installed [TW]')
plt.title('Cumulative Installs with Replacements')
#plt.ylim(0,160)
plt.xticks(rotation=45)


# In[ ]:


(cumu_installs.loc[2100,'newInstalledCapacity_sim4_projectlife_50 years_[MW]'] - cumu_installs.loc[2100,'newInstalledCapacity_sim4_projectlife_30 years_[MW]'])/1e6


# In[ ]:


(cumu_installs.loc[2100,'newInstalledCapacity_sim4_projectlife_8 years_[MW]'] - cumu_installs.loc[2100,'newInstalledCapacity_sim4_projectlife_30 years_[MW]'])/1e6


# In[ ]:


cumu_installs.loc[2100,'newInstalledCapacity_sim4_projectlife_30 years_[MW]']/1e6


# In[ ]:





# In[ ]:


#sim2_allenergy, sim2_energyGen, sim2_energy_demands
e_annual_sumDemands = sim4_energy_demands.filter(like='demand_total')
e_annual_sumDemands_cumu = e_annual_sumDemands.cumsum()
energyGen_cumu = sim4_energyGen.cumsum()
energyGen_cumu.columns = e_annual_sumDemands_cumu.columns = scennames4
netEnergy_cumu = energyGen_cumu.loc[[2100]] - e_annual_sumDemands_cumu.loc[[2100]]


# In[ ]:


eroi = energyGen_cumu.loc[[2100]] / e_annual_sumDemands_cumu.loc[[2100]]

plt.barh(eroi.columns[::-1], eroi.loc[2100, ::-1], 
        tick_label=(scennames4[::-1]), color=colors4)
plt.title('EROI ')
plt.xlabel('Arbitrary units')
#plt.xticks(rotation=90)


# In[ ]:





# In[ ]:





# # Repowering with Bifi
# Run a scenario where an older (PV ICE baseline) single install is put in. Then at economic lifetime, repower with bifi panels (change the module type after first install before second install).

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#modify silver usage
#sim1.scenario['TOPCon'].modifyMaterials('silver', 'mat_massperm2', celltech_aguse.loc[2022:,'TOPCon'], start_year=2022)


# In[ ]:


single_deploy_2020 = pd.DataFrame(index=idx_temp, columns=['MW'], dtype=float)
single_deploy_2020['MW'] = 0.0
single_deploy_2020.loc[2020,'MW'] = 100.0


# In[ ]:


bifiFactors = {'PERC_50':0.7, # ITRPV 2022, Fig. 58
               'SHJ':0.9, # ITRPV 2022, Fig. 58
               'TOPCon':0.8, # ITRPV 2022, Fig. 58
               'Perovskite': 0.0,
               'RecycledPERC':0.6,
                'PV_ICE':0.0,
                'CheapCrap':0.0} 

#MAY NEED TO CHANGE TO BE DYNAMIC


# In[ ]:


#PV ICE currently set up to read in a csv of bifi factors, so generate files to read in 
idx_temp = pd.RangeIndex(start=2050,stop=2101,step=1) #create the index
df_temp = pd.DataFrame(index=idx_temp, columns=['bifi'], dtype=float)
bifi_perc = df_temp.copy()
bifi_perc['bifi'] = bifiFactors['PERC']
bifi_shj = df_temp.copy()
bifi_shj['bifi'] = bifiFactors['SHJ']
bifi_topcon = df_temp.copy()
bifi_topcon['bifi'] = bifiFactors['TOPCon']


# In[ ]:


bifi_perc.to_csv(path_or_buf=os.path.join(testfolder,'bifi_perc.csv'), index_label='Year')
bifi_shj.to_csv(path_or_buf=os.path.join(testfolder,'bifi_shj.csv'), index_label='Year')
bifi_topcon.to_csv(path_or_buf=os.path.join(testfolder,'bifi_topcon.csv'), index_label='Year')


# In[ ]:


bifi_perc_path = os.path.join(testfolder,'bifi_perc.csv')
bifi_shj_path = os.path.join(testfolder,'bifi_shj.csv')
bifi_topcon_path = os.path.join(testfolder,'bifi_topcon.csv')


# In[ ]:





# In[ ]:




