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


#https://www.learnui.design/tools/data-color-picker.html#palette
#color pallette - modify here for all graphs below
colorpalette=['#000000', #PV ICE baseline
              '#595959', '#7F7F7F', '#A6A6A6', '#D9D9D9', #BAU, 4 grays, perc, shj, topcon, irena
              #'#067872','#0aa39e','#09d0cd','#00ffff', #realistic cases (4) teals, perc, shj, topcon, irena
              '#0579C1','#C00000','#FFC000', #extreme cases (3) long life, high eff, circular
                '#6E30A0','#00B3B5','#10C483', #ambitious modules (5) high eff+ long life, 50 yr perc, recycleSi, 
               '#97CB3F','#FF7E00' #circular perovskite+life, circular perovkiste+ high eff
                ] 

colormats = ['#00bfbf','#ff7f0e','#1f77be','#2ca02c','#d62728','#9467BD','#8C564B', 'black'] #colors for material plots       

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


# In[5]:


MATERIALS = ['glass', 'silicon', 'silver', 'aluminium_frames', 'copper', 'encapsulant', 'backsheet']
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[6]:


#load in the simulation from Energy Analysis journal
sim1 = PV_ICE.Simulation.load_Simpickle(filename=r'C:\Users\hmirletz\Documents\GitHub\PV_ICE\PV_ICE\TEMP\EnergyAnalysis\sim1.pkl')


# sim1.calculateCarbonFlows()

# sim1.scenario['r_PERC'].dataOut_c

# In[7]:


sim1.scenario['r_PERC'].dataOut_m


# ## Project grid forward to 100% re in 2050
# To parallel the PV deployment, we will assume that we globally hit 100% RE in 2050 with the 75 TW of PV. As such, we need to change the future projection of marketshares of the different country grids.
# 
# One scenario with decarb grid, one scenario with decarb grid and heat
# 
# Estimating that 60-70% generation will be from Solar, 30-40% from wind, and any remainder from "other renewables"

# In[8]:


countrygridmix = pd.read_csv(os.path.join(carbonfolder,'baseline_countrygridmix.csv'), index_col='year')
gridsources = ['Bioenergy','Hydro','Nuclear','OtherFossil','OtherRenewables','Solar','Wind']
nonRE = ['Coal','Gas','OtherFossil','Nuclear','Bioenergy']


# In[9]:


countrygridmix.loc[2023:,:]=np.nan #delete 2023 to 2050
nonRE_search = '|'.join(nonRE) #create nonRE search
countrygridmix.loc[2050, countrygridmix.columns.str.contains(nonRE_search)] = 0.0 #set all nonRE to 0 in 2050


# In[10]:


countrygridmix.loc[2050, countrygridmix.columns.str.contains('Solar')] = 63.0
countrygridmix.loc[2050, countrygridmix.columns.str.contains('Wind')] = 33.0
countrygridmix.loc[2050, countrygridmix.columns.str.contains('Hydro')] = 3.0
countrygridmix.loc[2050, countrygridmix.columns.str.contains('OtherRenewables')] = 1.0
#numbers derived from leading scenario electricity generation Breyer et al 2022 scenarios (EU focused)


# In[11]:


countrygridmix_100RE2050 = countrygridmix.interpolate() #linearly interpolate between 2022 and 2050


# In[12]:


apnd_idx = pd.RangeIndex(start=2051,stop=2101,step=1) #create temp df
apnd_df = pd.DataFrame(columns=countrygridmix_100RE2050.columns, index=apnd_idx )
countrygridmix_100RE20502100 = pd.concat([countrygridmix_100RE2050.loc[2000:],apnd_df], axis=0) #extend through 2100
countrygridmix_100RE20502100.ffill(inplace=True) #propogate 2050 values through 2100


# In[13]:


countrygridmix_100RE20502100.loc[2050]


# This is a simple projection, assumes all countries have same ratio of PV and wind (which we know can't be true). Update in future with country specific projections.

# In[14]:


pd.read_csv(os.path.join(carbonfolder,'baseline_electricityemissionfactors.csv'), index_col=[0])


# In[15]:


sim1.calculateCarbonFlows(countrygridmixes=countrygridmix_100RE20502100)


# In[ ]:





# # Carbon Analysis
# this will become the aggregate carbon results function

# In[16]:


scenarios = sim1.scenario


# In[17]:


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


# In[18]:


sim_carbon_results


# # Cabon Emissions by material or module

# In[19]:


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


# In[20]:


sim_cumu_carbon = sim_annual_carbon.cumsum()
maxy = round(sim_cumu_carbon.loc[2100].filter(like='Annual_Emit_total_modmats').max()/1e12,-3)
sim_cumu_carbon.loc[2100].filter(like='Annual_Emit_total_modmats')


# In[21]:


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
    plt.ylim(0,maxy)

    handles, labels = plt.gca().get_legend_handles_labels()
#specify order of items in legend
#order = [1,2,0]
#add legend to plot
#plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])
    plt.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1.4,1))

#plt.legend()
    plt.show()


# In[22]:


sim_cumu_carbon


# In[23]:


#create a df from which to do a bar chart of 2100 emissions by mat/mod
mats_emit_2100 = pd.DataFrame() #index=scennames_labels_flat
for mat in MATERIALS:
    mat_emit_2100 = pd.Series(sim_cumu_carbon.loc[2100].filter(like=mat).values)
    mats_emit_2100 = pd.concat([mats_emit_2100, mat_emit_2100], axis=1)

mats_emit_2100
mats_emit_2100.columns = MATERIALS
modmats_emit_2100 = pd.concat([mats_emit_2100,pd.Series(sim_cumu_carbon.loc[2100].filter(like='mod_').values)], axis=1)
modmats_emit_2100.index = scennames_labels_flat
modmats_emit_2100.rename(columns={0:'module'}, inplace=True)
modmats_emit_2100_megatonne = modmats_emit_2100/1e12
modmats_emit_2100_megatonne


# In[24]:


fig_cumuemit_modmat, (ax0,ax2,ax3) = plt.subplots(1,3,figsize=(15,8), sharey=True, 
                                      gridspec_kw={'wspace': 0, 'width_ratios': [1.5,1,1.5]})
#BAU
ax0.bar(scennames_labels[0:5], modmats_emit_2100_megatonne[0:5]['glass'], color=colormats[0])
ax0.bar(scennames_labels[0:5], modmats_emit_2100_megatonne[0:5]['silicon'],
        bottom=modmats_emit_2100_megatonne[0:5]['glass'], color=colormats[1])
ax0.bar(scennames_labels[0:5], modmats_emit_2100_megatonne[0:5]['silver'],
       bottom=modmats_emit_2100_megatonne.iloc[0:5,0:2].sum(axis=1), color=colormats[2])
ax0.bar(scennames_labels[0:5], modmats_emit_2100_megatonne[0:5]['aluminium_frames'],
       bottom=modmats_emit_2100_megatonne.iloc[0:5,0:3].sum(axis=1), color=colormats[3])
ax0.bar(scennames_labels[0:5], modmats_emit_2100_megatonne[0:5]['copper'],
       bottom=modmats_emit_2100_megatonne.iloc[0:5,0:4].sum(axis=1), color=colormats[4])
ax0.bar(scennames_labels[0:5], modmats_emit_2100_megatonne[0:5]['encapsulant'],
       bottom=modmats_emit_2100_megatonne.iloc[0:5,0:5].sum(axis=1), color=colormats[5])
ax0.bar(scennames_labels[0:5], modmats_emit_2100_megatonne[0:5]['backsheet'],
       bottom=modmats_emit_2100_megatonne.iloc[0:5,0:6].sum(axis=1), color=colormats[6])
ax0.bar(scennames_labels[0:5], modmats_emit_2100_megatonne[0:5]['module'],
       bottom=modmats_emit_2100_megatonne.iloc[0:5,0:7].sum(axis=1), color='black')

ax0.set_ylim(0,31000)
ax0.set_ylabel('Cumulative Carbon Emissions\n[million metric tonnes CO2eq]', fontsize=20)
ax0.set_title('Baseline', fontsize=14)
ax0.set_xticklabels(labels=scennames_labels[0:5], rotation=45)
ax0.grid(axis='y', color='0.9', ls='--') 
ax0.set_axisbelow(True)

#Extreme
ax2.bar(scennames_labels[5:8], modmats_emit_2100_megatonne[5:8]['glass'], color=colormats[0])
ax2.bar(scennames_labels[5:8], modmats_emit_2100_megatonne[5:8]['silicon'],
        bottom=modmats_emit_2100_megatonne[5:8]['glass'], color=colormats[1])
ax2.bar(scennames_labels[5:8], modmats_emit_2100_megatonne[5:8]['silver'],
       bottom=modmats_emit_2100_megatonne.iloc[5:8,0:2].sum(axis=1), color=colormats[2])
ax2.bar(scennames_labels[5:8], modmats_emit_2100_megatonne[5:8]['aluminium_frames'],
       bottom=modmats_emit_2100_megatonne.iloc[5:8,0:3].sum(axis=1), color=colormats[3])
ax2.bar(scennames_labels[5:8], modmats_emit_2100_megatonne[5:8]['copper'],
       bottom=modmats_emit_2100_megatonne.iloc[5:8,0:4].sum(axis=1), color=colormats[4])
ax2.bar(scennames_labels[5:8], modmats_emit_2100_megatonne[5:8]['encapsulant'],
       bottom=modmats_emit_2100_megatonne.iloc[5:8,0:5].sum(axis=1), color=colormats[5])
ax2.bar(scennames_labels[5:8], modmats_emit_2100_megatonne[5:8]['backsheet'],
       bottom=modmats_emit_2100_megatonne.iloc[5:8,0:6].sum(axis=1), color=colormats[6])
ax2.bar(scennames_labels[5:8], modmats_emit_2100_megatonne[5:8]['module'],
       bottom=modmats_emit_2100_megatonne.iloc[5:8,0:7].sum(axis=1), color='black')

ax2.set_title('Extreme', fontsize=14)
ax2.set_xticklabels(labels=scennames_labels[5:8], rotation=45)
ax2.grid(axis='y', color='0.9', ls='--') 
ax2.set_axisbelow(True)

#Ambitious
ax3.bar(scennames_labels[8:], modmats_emit_2100_megatonne[8:]['glass'], color=colormats[0])
ax3.bar(scennames_labels[8:], modmats_emit_2100_megatonne[8:]['silicon'],
        bottom=modmats_emit_2100_megatonne[8:]['glass'], color=colormats[1])
ax3.bar(scennames_labels[8:], modmats_emit_2100_megatonne[8:]['silver'],
       bottom=modmats_emit_2100_megatonne.iloc[8:,0:2].sum(axis=1), color=colormats[2])
ax3.bar(scennames_labels[8:], modmats_emit_2100_megatonne[8:]['aluminium_frames'],
       bottom=modmats_emit_2100_megatonne.iloc[8:,0:3].sum(axis=1), color=colormats[3])
ax3.bar(scennames_labels[8:], modmats_emit_2100_megatonne[8:]['copper'],
       bottom=modmats_emit_2100_megatonne.iloc[8:,0:4].sum(axis=1), color=colormats[4])
ax3.bar(scennames_labels[8:], modmats_emit_2100_megatonne[8:]['encapsulant'],
       bottom=modmats_emit_2100_megatonne.iloc[8:,0:5].sum(axis=1), color=colormats[5])
ax3.bar(scennames_labels[8:], modmats_emit_2100_megatonne[8:]['backsheet'],
       bottom=modmats_emit_2100_megatonne.iloc[8:,0:6].sum(axis=1), color=colormats[6])
ax3.bar(scennames_labels[8:], modmats_emit_2100_megatonne[8:]['module'],
       bottom=modmats_emit_2100_megatonne.iloc[8:,0:7].sum(axis=1), color='black')


ax3.set_title('Ambitious', fontsize=14)
ax3.set_xticklabels(labels=scennames_labels[8:], rotation=45)
ax3.grid(axis='y', color='0.9', ls='--') 
ax3.set_axisbelow(True)

#overall fig

fig_cumuemit_modmat.suptitle('Cumulative Emisisons in 2100 by material', fontsize=24)
plt.show()

#fig_cumuemit_modmat.savefig('energyresults-energyBalance.png', dpi=300, bbox_inches='tight')


# # Cumulative Carbon in 2050 and 2100

# In[25]:


#mins in 2050 and 2100
cumu_carbon_2050 = sim_cumu_carbon.loc[2050].filter(like='Annual_Emit_total_modmats')/1e12
cumu_carbon_2100 = sim_cumu_carbon.loc[2100].filter(like='Annual_Emit_total_modmats')/1e12
cumu_carbon_rankings_crittime = pd.concat([cumu_carbon_2050,cumu_carbon_2100], axis=1)
cumu_carbon_rankings_crittime.index = scennames_labels_flat
cumu_carbon_rankings_crittime


# In[26]:


cumu_carbon_rankings_crittime_plot = cumu_carbon_rankings_crittime.copy()
cumu_carbon_rankings_crittime_plot['diff'] = cumu_carbon_rankings_crittime[2100]-cumu_carbon_rankings_crittime[2050]


# In[27]:



fig_cumulativeemit, (ax0,ax2,ax3) = plt.subplots(1,3,figsize=(15,8), sharey=True, 
                                      gridspec_kw={'wspace': 0, 'width_ratios': [1.5,1,1.5]})
#BAU
ax0.bar(cumu_carbon_rankings_crittime_plot.index[0:5], cumu_carbon_rankings_crittime_plot[2050].iloc[0:5],
        tick_label=scennames_labels[0:5], color=colorpalette[0:5], alpha = 0.7, edgecolor='white')
ax0.bar(cumu_carbon_rankings_crittime_plot.index[0:5], cumu_carbon_rankings_crittime_plot['diff'].iloc[0:5],
        bottom=cumu_carbon_rankings_crittime_plot[2050].iloc[0:5],
        tick_label=scennames_labels[0:5], color=colorpalette[0:5])
ax0.set_ylim(0,31000)
ax0.set_ylabel('Cumulative Carbon Emissions\n[million metric tonnes CO2eq]', fontsize=20)
ax0.set_title('Baseline', fontsize=14)
ax0.set_xticklabels(labels=scennames_labels[0:5], rotation=45)
ax0.grid(axis='y', color='0.9', ls='--') 
ax0.set_axisbelow(True)

#Extreme
ax2.bar(cumu_carbon_rankings_crittime_plot.index[5:8], cumu_carbon_rankings_crittime_plot[2050].iloc[5:8],
        tick_label=scennames_labels[5:8], color=colorpalette[5:8], alpha = 0.7, edgecolor='white')
ax2.bar(cumu_carbon_rankings_crittime_plot.index[5:8], cumu_carbon_rankings_crittime_plot['diff'].iloc[5:8],
        bottom=cumu_carbon_rankings_crittime_plot[2050].iloc[5:8],
        tick_label=scennames_labels[5:8], color=colorpalette[5:8])
ax2.set_title('Extreme', fontsize=14)
ax2.set_xticklabels(labels=scennames_labels[5:8], rotation=45)
ax2.grid(axis='y', color='0.9', ls='--') 
ax2.set_axisbelow(True)

#Ambitious
ax3.bar(cumu_carbon_rankings_crittime_plot.index[8:], cumu_carbon_rankings_crittime_plot[2050].iloc[8:],
        tick_label=scennames_labels[8:], color=colorpalette[8:], hatch='x', edgecolor='white', alpha=0.7)
ax3.bar(cumu_carbon_rankings_crittime_plot.index[8:], cumu_carbon_rankings_crittime_plot['diff'].iloc[8:],
        bottom=cumu_carbon_rankings_crittime_plot[2050].iloc[8:],
        tick_label=scennames_labels[8:], color=colorpalette[8:], hatch='x', edgecolor='white')
ax3.set_title('Ambitious', fontsize=14)
ax3.set_xticklabels(labels=scennames_labels[8:], rotation=45)
ax3.grid(axis='y', color='0.9', ls='--') 
ax3.set_axisbelow(True)

#overall fig

fig_cumulativeemit.suptitle('Cumulative Emisisons in 2050, 2100', fontsize=24)
plt.show()

#fig_eBalance.savefig('energyresults-energyBalance.png', dpi=300, bbox_inches='tight')


# # 

# # Emissions by electricity vs fuels vs process
# ## Process emission summing
#  This only happens on the material files

# In[47]:


process_emissions = pd.DataFrame()
for scen in scenarios:
    scen_p_totrim = sim_carbon_results.filter(like=scen).filter(like='_p_')
    exclude_p_sums = ['_HQ_p_','_LQ_p_','_e_p_']
    exclude_p_sums_search = '|'.join(exclude_p_sums)
    scen_p = scen_p_totrim.loc[:,~scen_p_totrim.columns.str.contains(exclude_p_sums_search)]
    scen_p_sum = scen_p.sum(axis=1)
    process_emissions = pd.concat([process_emissions,scen_p_sum], axis=1)


# In[49]:


process_emissions.columns = scennames_labels_flat
process_emissions


# ## Fuel Emissions
# This is capturing steam and heating fuel

# In[54]:


fuel_emissions = pd.DataFrame()
for scen in scenarios:
    scen_f = sim_carbon_results.filter(like=scen).filter(like='_fuel_')
    scen_f_sum = scen_f.sum(axis=1)
    fuel_emissions = pd.concat([fuel_emissions,scen_f_sum], axis=1)
    
fuel_emissions.columns = scennames_labels_flat


# In[55]:


fuel_emissions


# ## Electricity Emissions
# both module and material level elec.

# In[76]:



for scen in scenarios:
    scen_mod_elec = sim_annual_carbon.filter(like=scen).filter(like='Annual_Emit_mod') #module elec lifecycle energy
    
    mat_eleckey = ['Global_vmfg_elec','landfill_elec','ReMFG_clean','Recycled_LQ','Recycled_HQ_elec']
    mat_elecs_search = '|'.join(mat_eleckey)
    scen_mat_elecs = sim_carbon_results.loc[:,sim_carbon_results.columns.str.contains(mat_elecs_search)].filter(like=scen)
    
    #sum them together by scen


# In[77]:


scen_mat_elecs


# In[ ]:





# In[ ]:





# In[ ]:




