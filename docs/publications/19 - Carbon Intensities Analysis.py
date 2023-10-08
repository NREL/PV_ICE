#!/usr/bin/env python
# coding: utf-8

# # Carbon instensity of Sustainable PV for Energy Transition
# This analysis explores the carbon implications of different PV sustainability/circular economy designs in the context of achieving energy transition. These calculations build upon previous work that can be found in journals 13 and 17.
# 
# Attempt 1

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'CarbonAnalysis')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
carbonfolder = str(Path().resolve().parent.parent / 'PV_ICE'/ 'baselines'/ 'CarbonLayer')
altBaselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'Energy_CellModuleTechCompare')
energyanalysisfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'EnergyAnalysis')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


from platform import python_version 
print(python_version())


# In[3]:


import PV_ICE
PV_ICE.__version__


# In[4]:


MATERIALS = ['glass', 'silicon', 'silver', 'aluminium_frames', 'copper', 'encapsulant', 'backsheet']
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[5]:


#load in the simulation from Energy Analysis journal
sim1 = PV_ICE.Simulation.load_Simpickle(filename=r'C:\Users\hmirletz\Documents\GitHub\PV_ICE\PV_ICE\TEMP\EnergyAnalysis\sim1.pkl')


# sim1.calculateCarbonFlows()

# sim1.scenario['r_PERC'].dataOut_c

# In[6]:


sim1.scenario['r_PERC'].dataOut_m


# ## Project grid forward to 100% re in 2050
# To parallel the PV deployment, we will assume that we globally hit 100% RE in 2050 with the 75 TW of PV. As such, we need to change the future projection of marketshares of the different country grids.
# 
# One scenario with decarb grid, one scenario with decarb grid and heat
# 
# Estimating that 60-70% generation will be from Solar, 30-40% from wind, and any remainder from "other renewables"

# In[7]:


countrygridmix = pd.read_csv(os.path.join(carbonfolder,'baseline_countrygridmix.csv'), index_col='year')
gridsources = ['Bioenergy','Hydro','Nuclear','OtherFossil','OtherRenewables','Solar','Wind']
nonRE = ['Coal','Gas','OtherFossil','Nuclear','Bioenergy']


# In[8]:


countrygridmix.loc[2023:,:]=np.nan #delete 2023 to 2050
nonRE_search = '|'.join(nonRE) #create nonRE search
countrygridmix.loc[2050, countrygridmix.columns.str.contains(nonRE_search)] = 0.0 #set all nonRE to 0 in 2050


# In[9]:


countrygridmix.loc[2050, countrygridmix.columns.str.contains('Solar')] = 63.0
countrygridmix.loc[2050, countrygridmix.columns.str.contains('Wind')] = 33.0
countrygridmix.loc[2050, countrygridmix.columns.str.contains('Hydro')] = 3.0
countrygridmix.loc[2050, countrygridmix.columns.str.contains('OtherRenewables')] = 1.0
#numbers derived from leading scenario electricity generation Breyer et al 2022 scenarios (EU focused)


# In[10]:


countrygridmix_100RE2050 = countrygridmix.interpolate() #linearly interpolate between 2022 and 2050


# In[11]:


apnd_idx = pd.RangeIndex(start=2051,stop=2101,step=1) #create temp df
apnd_df = pd.DataFrame(columns=countrygridmix_100RE2050.columns, index=apnd_idx )
countrygridmix_100RE20502100 = pd.concat([countrygridmix_100RE2050.loc[2000:],apnd_df], axis=0) #extend through 2100
countrygridmix_100RE20502100.ffill(inplace=True) #propogate 2050 values through 2100


# In[12]:


countrygridmix_100RE20502100.loc[2050]


# This is a simple projection, assumes all countries have same ratio of PV and wind (which we know can't be true). Update in future with country specific projections.

# In[59]:


pd.read_csv(os.path.join(carbonfolder,'baseline_electricityemissionfactors.csv'))


# In[13]:


sim1.calculateCarbonFlows(countrygridmixes=countrygridmix_100RE20502100)


# In[ ]:





# # Carbon Analysis
# this will become the aggregate carbon results function

# In[14]:


scenarios = sim1.scenario


# In[25]:


sim_carbon_results = pd.DataFrame()
sim_annual_carbon = pd.DataFrame()
for scen in scenarios:
    print(scen)
    mod_carbon_scen_results = sim1.scenario[scen].dataOut_c.add_prefix(str(scen+'_'))
    
    #mod annual carbon calcs here (selecting to avoid double counting)
    mod_mfg_carbon_total = mod_carbon_scen_results.filter(like='Global_gCO2eqpwh_mod_MFG_gCO2eq') #annual mfging carbon

    mod_nonvMFG = ['Install','OandM','Repair','Demount','Store','Resell','ReMFG','Recycle'] #could remove from loop
    nonvMFG_search = '|'.join(mod_nonvMFG) #create nonRE search
    mod_carbon_sum_nonvmfg = mod_carbon_scen_results.loc[:,mod_carbon_scen_results.columns.str.contains(nonvMFG_search)] #annual non mfging carbon
    scen_annual_carbon_mod = pd.concat([mod_mfg_carbon_total,mod_carbon_sum_nonvmfg], axis=1)
    scen_annual_carbon_mod[scen+'_Annual_Emit_mod_gCO2eq'] = scen_annual_carbon_mod.sum(axis=1)

    scenmatdc = pd.DataFrame()
    for mat in MATERIALS:
        print(mat)
        mat_carbon_scen_results = sim1.scenario[scen].material[mat].matdataOut_c.add_prefix(str(scen+'_'+mat+'_')) 
        
        #calculation for annual carbon emissions total (selecting to avoid double countings)
        mat_vmfg_total = mat_carbon_scen_results.filter(like='vMFG_total')
        mat_ce_recycle = mat_carbon_scen_results.filter(like='Recycle_e_p')
        mat_ce_remfg = mat_carbon_scen_results.filter(like='ReMFG_clean')
        mat_landfill = mat_carbon_scen_results.filter(like='landfill_total')
        mat_scen_annual_carbon = pd.concat([mat_vmfg_total,mat_ce_recycle,mat_ce_remfg,mat_landfill], axis=1)
        mat_scen_annual_carbon[scen+'_Annual_Emit_'+mat+'_gCO2eq'] = mat_scen_annual_carbon.sum(axis=1)
        
        scenmatdc = pd.concat([scenmatdc,mat_carbon_scen_results,
                               mat_scen_annual_carbon[scen+'_Annual_Emit_'+mat+'_gCO2eq']], axis=1) #group all material dc
    
    scen_carbon_results = pd.concat([mod_carbon_scen_results,scenmatdc], axis=1) #append mats to mod
    sim_carbon_results = pd.concat([sim_carbon_results, scen_carbon_results], axis=1) #append all scens "raw" data
    
    #calculate annual carbon emits with grouping by mod and mat
    scen_mats_annual_carbon = scenmatdc.filter(like='Annual_Emit')
    scen_mod_annual_carbon = scen_annual_carbon_mod.filter(like='Annual_Emit_mod')
    scen_annual_carbon = pd.concat([scen_mod_annual_carbon,scen_mats_annual_carbon], axis=1)
    scen_annual_carbon[scen+'_Annual_Emit_total_modmats_gCO2eq'] = scen_annual_carbon.sum(axis=1)
    sim_annual_carbon = pd.concat([sim_annual_carbon,scen_annual_carbon], axis=1)
    
    #FIX INDEX of dfs
sim_annual_carbon.index = pd.RangeIndex(start=2000,stop=2101,step=1)
sim_carbon_results.index = pd.RangeIndex(start=2000,stop=2101,step=1)
    
#return sim_carbon_results, sim_annual_carbon


# In[26]:


sim_carbon_results


# In[27]:


pvice_annual_carbon = sim_annual_carbon.filter(like='Annual_Emit').filter(like='PV_ICE')/1e12 #million tonnes
pvice_annual_carbon.index = pd.RangeIndex(start=2000,stop=2101,step=1)

colormats = ['#00bfbf','#ff7f0e','#1f77be','#2ca02c','#d62728','#9467BD','#8C564B','black'] #colors for material plots

plt.plot([],[],color=colormats[0], label=MATERIALS[0])
plt.plot([],[],color=colormats[1], label=MATERIALS[1])
plt.plot([],[],color=colormats[2], label=MATERIALS[2])
plt.plot([],[],color=colormats[3], label=MATERIALS[3])
plt.plot([],[],color=colormats[4], label=MATERIALS[4])
plt.plot([],[],color=colormats[5], label=MATERIALS[5])
plt.plot([],[],color=colormats[6], label=MATERIALS[6])
plt.plot([],[],color=colormats[7], label='module')


plt.stackplot(pvice_annual_carbon.index,
              pvice_annual_carbon['PV_ICE_Annual_Emit_glass_gCO2eq'], 
              pvice_annual_carbon['PV_ICE_Annual_Emit_silicon_gCO2eq'],
              pvice_annual_carbon['PV_ICE_Annual_Emit_silver_gCO2eq'], 
              pvice_annual_carbon['PV_ICE_Annual_Emit_aluminium_frames_gCO2eq'], 
              pvice_annual_carbon['PV_ICE_Annual_Emit_copper_gCO2eq'],
              pvice_annual_carbon['PV_ICE_Annual_Emit_encapsulant_gCO2eq'],
              pvice_annual_carbon['PV_ICE_Annual_Emit_backsheet_gCO2eq'],
              pvice_annual_carbon['PV_ICE_Annual_Emit_mod_gCO2eq'],
              colors = colormats)
plt.title('Carbon Emissions Annually by Module and Material Lifecycle')
plt.ylabel('GHG Emissions Annually from Lifecycle Mats and Mods\n[million metric tonnes CO2eq]')
plt.xlim(2000,2100)

handles, labels = plt.gca().get_legend_handles_labels()
#specify order of items in legend
#order = [1,2,0]
#add legend to plot
#plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])
plt.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1.4,1))

#plt.legend()
plt.show()


# In[31]:


colormats = ['#00bfbf','#ff7f0e','#1f77be','#2ca02c','#d62728','#9467BD','#8C564B','black'] #colors for material plots
for scen in scenarios:

    scen_annual_carbon = sim_annual_carbon.filter(like='Annual_Emit').filter(like=scen)/1e12 #million tonnes
    
    plt.plot([],[],color=colormats[0], label=MATERIALS[0])
    plt.plot([],[],color=colormats[1], label=MATERIALS[1])
    plt.plot([],[],color=colormats[2], label=MATERIALS[2])
    plt.plot([],[],color=colormats[3], label=MATERIALS[3])
    plt.plot([],[],color=colormats[4], label=MATERIALS[4])
    plt.plot([],[],color=colormats[5], label=MATERIALS[5])
    plt.plot([],[],color=colormats[6], label=MATERIALS[6])
    plt.plot([],[],color=colormats[7], label='module')


    plt.stackplot(scen_annual_carbon.index,
                  scen_annual_carbon[scen+'_Annual_Emit_glass_gCO2eq'], 
                  scen_annual_carbon[scen+'_Annual_Emit_silicon_gCO2eq'],
                  scen_annual_carbon[scen+'_Annual_Emit_silver_gCO2eq'], 
                  scen_annual_carbon[scen+'_Annual_Emit_aluminium_frames_gCO2eq'], 
                  scen_annual_carbon[scen+'_Annual_Emit_copper_gCO2eq'],
                  scen_annual_carbon[scen+'_Annual_Emit_encapsulant_gCO2eq'],
                  scen_annual_carbon[scen+'_Annual_Emit_backsheet_gCO2eq'],
                  scen_annual_carbon[scen+'_Annual_Emit_mod_gCO2eq'],
                  colors = colormats)
    plt.title(scen+':\nGHG Emissions Annually by Module and Material Lifecycle')
    plt.ylabel('GHG Emissions Annually from Lifecycle Mats and Mods\n[million metric tonnes CO2eq]')
    plt.xlim(2000,2100)

    handles, labels = plt.gca().get_legend_handles_labels()
#specify order of items in legend
#order = [1,2,0]
#add legend to plot
#plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])
    plt.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1.4,1))

#plt.legend()
    plt.show()


# In[57]:


sim_cumu_carbon = sim_annual_carbon.cumsum()
sim_cumu_carbon.loc[2100].filter(like='Annual_Emit_total_modmats')


# In[58]:


colormats = ['#00bfbf','#ff7f0e','#1f77be','#2ca02c','#d62728','#9467BD','#8C564B','black'] #colors for material plots
for scen in scenarios:

    scen_cumu_carbon = sim_cumu_carbon.filter(like='Annual_Emit').filter(like=scen)/1e12 #million tonnes
    
    plt.plot([],[],color=colormats[0], label=MATERIALS[0])
    plt.plot([],[],color=colormats[1], label=MATERIALS[1])
    plt.plot([],[],color=colormats[2], label=MATERIALS[2])
    plt.plot([],[],color=colormats[3], label=MATERIALS[3])
    plt.plot([],[],color=colormats[4], label=MATERIALS[4])
    plt.plot([],[],color=colormats[5], label=MATERIALS[5])
    plt.plot([],[],color=colormats[6], label=MATERIALS[6])
    plt.plot([],[],color=colormats[7], label='module')


    plt.stackplot(scen_cumu_carbon.index,
                  scen_cumu_carbon[scen+'_Annual_Emit_glass_gCO2eq'], 
                  scen_cumu_carbon[scen+'_Annual_Emit_silicon_gCO2eq'],
                  scen_cumu_carbon[scen+'_Annual_Emit_silver_gCO2eq'], 
                  scen_cumu_carbon[scen+'_Annual_Emit_aluminium_frames_gCO2eq'], 
                  scen_cumu_carbon[scen+'_Annual_Emit_copper_gCO2eq'],
                  scen_cumu_carbon[scen+'_Annual_Emit_encapsulant_gCO2eq'],
                  scen_cumu_carbon[scen+'_Annual_Emit_backsheet_gCO2eq'],
                  scen_cumu_carbon[scen+'_Annual_Emit_mod_gCO2eq'],
                  colors = colormats)
    plt.title(scen+':\nGHG Emissions Annually by Module and Material Lifecycle')
    plt.ylabel('GHG Emissions Annually from Lifecycle Mats and Mods\n[million metric tonnes CO2eq]')
    plt.xlim(2000,2100)
    plt.ylim(0,38000)

    handles, labels = plt.gca().get_legend_handles_labels()
#specify order of items in legend
#order = [1,2,0]
#add legend to plot
#plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])
    plt.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1.4,1))

#plt.legend()
    plt.show()


# In[ ]:





# In[ ]:





# In[ ]:


scen_cumu_carbon = scen_annual_carbon.cumsum()


# In[ ]:


scen_cumu_carbon.loc[55,'Annual_Emit_total_gCO2eq']/1e12


# In[ ]:


scen_annual_carbon.columns


# In[ ]:





# In[ ]:


#https://www.learnui.design/tools/data-color-picker.html#palette
#color pallette - modify here for all graphs below
colorpalette=['#000000', #PV ICE baseline
              '#595959', '#7F7F7F', '#A6A6A6', '#D9D9D9', #BAU, 4 grays, perc, shj, topcon, irena
              #'#067872','#0aa39e','#09d0cd','#00ffff', #realistic cases (4) teals, perc, shj, topcon, irena
              '#0579C1','#C00000','#FFC000', #extreme cases (3) long life, high eff, circular
                '#6E30A0','#00B3B5','#10C483', #ambitious modules (5) high eff+ long life, 50 yr perc, recycleSi, 
               '#97CB3F','#FF7E00' #circular perovskite+life, circular perovkiste+ high eff
                ] 

colormats = ['#00bfbf','#ff7f0e','#1f77be','#2ca02c','#d62728','#9467BD','#8C564B'] #colors for material plots       

import matplotlib as mpl #import matplotlib
from cycler import cycler #import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=colorpalette) #reset the default color palette of mpl

plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.figsize'] = (8, 6)

scennames_labels = ['PV_ICE','PERC','SHJ','TOPCon','Low\nQuality',
                         'Long-Lived','High Eff','Circular',
                        'High Eff\n+ Long-life','Long-Life\n+ Recycling',
                         'Recycled-Si\n+ Long-life','Circular\n+ Long-life',
                        'Circular\n+ High Eff'
                    ]  

scennames_labels_flat = ['PV_ICE','PERC','SHJ','TOPCon','Low Quality',
                         'Long-Lived','High Eff','Circular',
                        'High Eff + Long-life','Long-Life + Recycling',
                         'Recycled-Si + Long-life','Circular + Long-life',
                        'Circular + High Eff'
                    ] 

