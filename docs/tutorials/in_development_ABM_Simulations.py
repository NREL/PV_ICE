#!/usr/bin/env python
# coding: utf-8

# # Inputting ABM outputs into PV ICE 

# ## Import libraries and create test folder

# In[1]:


import PV_ICE
import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from itertools import chain
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px


# In[2]:


testfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'TEMP')
baselinesfolder =  str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)
print(baselinesfolder)


# ## Create initial simulations

# In[3]:


#create simulations
r1 = PV_ICE.Simulation(name='ABM_Simulation1', path=testfolder)
r2 = PV_ICE.Simulation(name='ABM_Simulation2', path=testfolder)
r3A = PV_ICE.Simulation(name='ABM_Simulation3A', path=testfolder)
r3B = PV_ICE.Simulation(name='ABM_Simulation3B', path=testfolder)
r3C = PV_ICE.Simulation(name='ABM_Simulation3C', path=testfolder)
r3D = PV_ICE.Simulation(name='ABM_Simulation3D', path=testfolder)
r4 = PV_ICE.Simulation(name='ABM_Simulation4', path=testfolder)
r4A = PV_ICE.Simulation(name='ABM_Simulation4A', path=testfolder)
r4B = PV_ICE.Simulation(name='ABM_Simulation4B', path=testfolder)
r4C = PV_ICE.Simulation(name='ABM_Simulation4C', path=testfolder)
r4D = PV_ICE.Simulation(name='ABM_Simulation4D', path=testfolder)

#create 10 scenarios in each simulation: 1st is standard in PV ICE, 2-10 are scenarios a-i in ABM
SIMULATIONS = [r1,r2,r4]
SCENARIOS = ['standard_PVICE','landfill_ban','high_mat_recovery_cheap_recycling','cheap_recycling','high_landfill_costs','better_lifetime','better_learning','reuse_warranties','seeding_reuse','juliens_baseline']
for mysimulation in SIMULATIONS: 
    for myscenario in SCENARIOS:
        mysimulation.createScenario(name=myscenario, file=r'..\baselines\baseline_modules_US.csv')
        mysimulation.scenario[myscenario].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
        mysimulation.scenario[myscenario].addMaterial('aluminium_frames', file=r'..\baselines\baseline_material_aluminium_frames.csv')
        mysimulation.scenario[myscenario].addMaterial('silver', file=r'..\baselines\baseline_material_silver.csv')
        mysimulation.scenario[myscenario].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')
        mysimulation.scenario[myscenario].addMaterial('copper', file=r'..\baselines\baseline_material_copper.csv')

#create r3 for select scenarios: split up into 4 separate simulations: r3A, r3B, r3C, r3D
#Henry Hieslmair gives four classes of repair bins: A, B, C, D; with A being lowest quality, D being highest quality
REPAIR_SCENARIOS = ['better_learning', 'juliens_baseline', 'landfill_ban']
r3_simulations = [r3A, r3B, r3C, r3D]
for myr3simulation in r3_simulations:
    for myscenario in REPAIR_SCENARIOS:
        scenario_name = myscenario
        myr3simulation.createScenario(name=myscenario, file=r'..\baselines\baseline_modules_US.csv')
        myr3simulation.scenario[myscenario].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
        myr3simulation.scenario[myscenario].addMaterial('aluminium_frames', file=r'..\baselines\baseline_material_aluminium_frames.csv')
        myr3simulation.scenario[myscenario].addMaterial('silver', file=r'..\baselines\baseline_material_silver.csv')
        myr3simulation.scenario[myscenario].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')
        myr3simulation.scenario[myscenario].addMaterial('copper', file=r'..\baselines\baseline_material_copper.csv')
        
#create r4 for select scenarios: r4A, r4B, r4C, r4D
REPAIR_SCENARIOS = ['better_learning', 'juliens_baseline', 'landfill_ban']
r4_simulations = [r4A, r4B, r4C, r4D]
for myr4simulation in r4_simulations:
    for myscenario in REPAIR_SCENARIOS:
        scenario_name = myscenario
        myr4simulation.createScenario(name=myscenario, file=r'..\baselines\baseline_modules_US.csv')
        myr4simulation.scenario[myscenario].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
        myr4simulation.scenario[myscenario].addMaterial('aluminium_frames', file=r'..\baselines\baseline_material_aluminium_frames.csv')
        myr4simulation.scenario[myscenario].addMaterial('silver', file=r'..\baselines\baseline_material_silver.csv')
        myr4simulation.scenario[myscenario].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')
        myr4simulation.scenario[myscenario].addMaterial('copper', file=r'..\baselines\baseline_material_copper.csv')


# In[4]:


#Irena RL Weibull Parameters to use for r1, r2, r4
weibull_IrenaRL = {'alpha': 5.3759, 'beta': 30}


# In[5]:


#Henry Hieslmair Weibull Parameters to use for r3A, r3B, r3C, r3D, r4A, r4B, r4C, r4D
weibullInputParamsA = {'alpha': 2.810, 'beta': 100.238} 
weibullInputParamsB = {'alpha': 3.841, 'beta': 57.491}
weibullInputParamsC = {'alpha': 4.602, 'beta': 40.767}
weibullInputParamsD = {'alpha': 5.692, 'beta': 29.697}


# ## Modify parameters: Simulation 1 (r1), same installs for all scenarios: what is the effect of different reuse, recycle, and repair rates?

# In[6]:


#modify values of each scenario 2-10 based on ABM outputs
#first, set 'mod_EOL_collected_recycled' to 100% in scenarios 2-10 for years 2022 on (assume all collected modules are recycled)
ABM_SCENARIOS = SCENARIOS[1:] 
past_years_collected_recycled = [r1.scenario['standard_PVICE'].data['mod_EOL_collected_recycled'][0]]*(2022-1995)
new_collected_recycled = [100]*(2050-2021)
#create new list to replace 'mod_EOL_collected_recycled' with, with 1995-2021 original baseline module values, and 2022-2050 at 100%
new_mod_recycled = past_years_collected_recycled + new_collected_recycled
for myscenario in ABM_SCENARIOS:
    r1.scenario[myscenario].data['mod_EOL_collected_recycled'] = new_mod_recycled
    
#next, set 'mat_EOL_collected_Recycled' to 100% for each material in scenarios 2-10 for years 2022 on (assume all collected materials are recycled)
MATERIALS = ['glass','aluminium_frames','silver','silicon','copper']
for mymaterial in MATERIALS:
    past_years_collected_recycled = [r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_collected_Recycled'][0]]*(2022-1995)
    new_collected_recycled = [100]*(2050-2021)
    #create new list to replace 'mat_EOL_collected_Recycled' with, with 1995-2021 original baseline module values, and 2022-2050 at 100%
    new_mat_recycled = past_years_collected_recycled + new_collected_recycled
    for myscenario in ABM_SCENARIOS:
        r1.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_collected_Recycled'] = new_mat_recycled


# In[7]:


#next, modify 3 additional inputs for each scenario 2-10, with values depending on the scenario, coming from ABM outputs
MODIFIED_MODULE_BASELINES = ['mod_Repair','mod_Reuse','mod_EOL_collection_eff']
len(r1.scenario['landfill_ban'].data['mod_Reuse']) #all inputs have 56 rows
#keep first 27 rows corresponding to 1995-2021 values
ABM_outputs = pd.read_csv(r'..\baselines\ABM\abm_outputs_mass_fractions.csv')


# In[8]:


#ABM_outputs
#change scenario names to names from ABM_SCENARIOS
file_scenario_names = ABM_outputs['Scenario'].unique().tolist()
ABM_outputs = ABM_outputs.replace(file_scenario_names, ABM_SCENARIOS)


# In[9]:


#changing repair, eol collection eff, and reuse module baselines for all ABM scenarios
for myscenario in ABM_SCENARIOS:
    frames1 = []
    frames2 = []
    frames3 = []
    new_outputs = []
    scenario_filter = []
    new_mod_Repairing = []
    new_mod_Recycling = []
    new_mod_Reuse = []
    scenario_filter = 'Scenario == ' + '\"' + myscenario + '\"'
    new_outputs = ABM_outputs.query(scenario_filter)
    #replace repairing baselines
    repairs = new_outputs.loc[:,'mass_fraction_PV_materials_repaired_milliontonnes']*100
    repairs.index = list(range(31))
    frames1 = [r1.scenario[myscenario].data['mod_Repair'][0:27],repairs[2:]]
    new_mod_Repairing = pd.concat(frames1)
    r1.scenario[myscenario].data['mod_Repair'] = new_mod_Repairing.values
    #replace recycling baselines
    recycled = new_outputs.loc[:,'mass_fraction_PV_materials_recycled_milliontonnes']*100
    if myscenario == 'high_mat_recovery_cheap_recycling':
        recycles = recycled/0.96 #reflects higher material recovery rate (must change as ABM gives effective recycling rate)
    else:
        recycles = recycled/0.80 #must change as ABM gives effective recycling rate
    recycles.index = list(range(31))
    frames2 = [r1.scenario[myscenario].data['mod_EOL_collection_eff'][0:27],recycles[2:]]
    new_mod_Recycling = pd.concat(frames2)
    r1.scenario[myscenario].data['mod_EOL_collection_eff'] = new_mod_Recycling.values
    #replace reuse baselines
    reuses = new_outputs.loc[:,'mass_fraction_PV_materials_reused_milliontonnes']*100
    reuses.index = list(range(31))
    frames3 = [r1.scenario[myscenario].data['mod_Reuse'][0:27],reuses[2:]]
    new_mod_Reuse = pd.concat(frames3)
    r1.scenario[myscenario].data['mod_Reuse'] = new_mod_Reuse.values


# In[10]:


#also change mod_lifetime = 40 to agree with Irena RL
for myscenario in ABM_SCENARIOS:
    old_lifetime = list(r1.scenario[myscenario].data['mod_lifetime'][0:27])
    irena_lifetime = [40] * (2050-2021)
    r1.scenario[myscenario].data['mod_lifetime'] = old_lifetime + irena_lifetime


# ### Modify better_lifetime scenario reliability inputs: mod_lifetime, mod_reliability_t50, & mod_reliability_t90

# In[11]:


def lifetime_line(year):
    """"
    This function takes in a year and outputs the module lifetime based on scenario e) in ABM.
    Inputs
    year = desired year
    """
    m = (60-15.9)/(2050-2000)
    y = m*(year-2000) + 15.9
    return(y)


# In[12]:


#create list of mod_lifetime values based on linear regression
years = list(range(2022,2051)) #ONLY WANT to modify 2022 ONWARD
mod_lifetimes_list = []
for myyear in years:
    mod_lifetimes_list += [lifetime_line(myyear)]


# In[13]:


mod_lifetimes_df = pd.DataFrame()


# In[14]:


mod_lifetimes_df['year'] = years
mod_lifetimes_df['mod_lifetime'] = mod_lifetimes_list


# In[15]:


#changing mod_lifetime in scenario e) better_lifetime
new_mod_lifetime = list(r1.scenario[myscenario].data['mod_lifetime'][0:27].values) + mod_lifetimes_list
r1.scenario['better_lifetime'].data['mod_lifetime'] = new_mod_lifetime


# In[16]:


#create linear regression for mod_reliability_t50 & mod_reliability_t90 vs. mod_lifetime 
#to estimate t50 and t90 values to input for improved lifetime scenario
reliability_baselines = pd.DataFrame()
reliability_baselines['mod_lifetime'] = r1.scenario['standard_PVICE'].data['mod_lifetime']
reliability_baselines['mod_reliability_t50'] = r1.scenario['standard_PVICE'].data['mod_reliability_t50']
reliability_baselines['mod_reliability_t90'] = r1.scenario['standard_PVICE'].data['mod_reliability_t90']


# In[17]:


X_lifetime = reliability_baselines.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
Y1_t50 = reliability_baselines.iloc[:, 1].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
Y2_t90 = reliability_baselines.iloc[:, 2].values.reshape(-1, 1)
better_lifetimes = np.array(mod_lifetimes_list).reshape(-1,1)

linear_regressor_Y1 = LinearRegression()
linear_regressor_Y1.fit(X_lifetime, Y1_t50)  # perform linear regression
better_lifetime_t50_list = linear_regressor_Y1.predict(better_lifetimes).tolist()  # make predictions based on improved lifetime values
better_lifetime_t50_list = list(chain(*better_lifetime_t50_list)) #unnest list

linear_regressor_Y2 = LinearRegression() 
linear_regressor_Y2.fit(X_lifetime, Y2_t90)
better_lifetime_t90_list = linear_regressor_Y2.predict(better_lifetimes).tolist()
better_lifetime_t90_list = list(chain(*better_lifetime_t90_list)) #unnest list


# In[18]:


#changing mod_reliability_t50 & mod_reliability_t90 in scenario e) better_lifetime
new_mod_t50 = list(r1.scenario[myscenario].data['mod_reliability_t50'][0:27].values) + better_lifetime_t50_list
r1.scenario['better_lifetime'].data['mod_reliability_t50'] = new_mod_t50

new_mod_t90 = list(r1.scenario[myscenario].data['mod_reliability_t90'][0:27].values) + better_lifetime_t90_list
r1.scenario['better_lifetime'].data['mod_reliability_t90'] = new_mod_t90


# ## Modify parameters: Simulation 2 (r2), same installs for all scenarios: what is effect of different reuse, recycle, and repair rates when recycling efficiency is improved?

# In[19]:


#copy same parameter modifications for r2 as in r1
for myscenario in ABM_SCENARIOS:
    r2.scenario[myscenario].data['mod_EOL_collected_recycled'] = new_mod_recycled
for mymaterial in MATERIALS:
    past_years_collected_recycled = [r2.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_collected_Recycled'][0]]*(2022-1995)
    new_collected_recycled = [100]*(2050-2021)
    new_mat_recycled = past_years_collected_recycled + new_collected_recycled
    for myscenario in ABM_SCENARIOS:
        r2.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_collected_Recycled'] = new_mat_recycled
for myscenario in ABM_SCENARIOS:
    frames1 = []
    frames2 = []
    frames3 = []
    new_outputs = []
    scenario_filter = []
    new_mod_Repairing = []
    new_mod_Recycling = []
    new_mod_Reuse = []
    scenario_filter = 'Scenario == ' + '\"' + myscenario + '\"'
    new_outputs = ABM_outputs.query(scenario_filter)
    #replace repairing baselines
    repairs = new_outputs.loc[:,'mass_fraction_PV_materials_repaired_milliontonnes']*100
    repairs.index = list(range(31))
    frames1 = [r2.scenario[myscenario].data['mod_Repair'][0:27],repairs[2:]]
    new_mod_Repairing = pd.concat(frames1)
    r2.scenario[myscenario].data['mod_Repair'] = new_mod_Repairing.values
    #replace recycling baselines
    recycled = new_outputs.loc[:,'mass_fraction_PV_materials_recycled_milliontonnes']*100
    if myscenario == 'high_mat_recovery_cheap_recycling':
        recycles = recycled/0.96 #reflects higher material recovery rate (must change as ABM gives effective recycling rate)
    else:
        recycles = recycled/0.80 #must change as ABM gives effective recycling rate
    recycles.index = list(range(31))
    frames2 = [r2.scenario[myscenario].data['mod_EOL_collection_eff'][0:27],recycles[2:]]
    new_mod_Recycling = pd.concat(frames2)
    r2.scenario[myscenario].data['mod_EOL_collection_eff'] = new_mod_Recycling.values
    #replace reuse baselines
    reuses = new_outputs.loc[:,'mass_fraction_PV_materials_reused_milliontonnes']*100
    reuses.index = list(range(31))
    frames3 = [r2.scenario[myscenario].data['mod_Reuse'][0:27],reuses[2:]]
    new_mod_Reuse = pd.concat(frames3)
    r2.scenario[myscenario].data['mod_Reuse'] = new_mod_Reuse.values
    
#also change mod_lifetime = 40 to agree with Irena RL
for myscenario in ABM_SCENARIOS:
    old_lifetime = list(r2.scenario[myscenario].data['mod_lifetime'][0:27])
    irena_lifetime = [40] * (2050-2021)
    r2.scenario[myscenario].data['mod_lifetime'] = old_lifetime + irena_lifetime
    
r2.scenario['better_lifetime'].data['mod_lifetime'] = new_mod_lifetime
r2.scenario['better_lifetime'].data['mod_reliability_t50'] = new_mod_t50
r2.scenario['better_lifetime'].data['mod_reliability_t90'] = new_mod_t90


# In[20]:


#FRELP recovery rates and qualities
frelp_results = pd.DataFrame()
frelp_results['mat'] = ['silver','copper','aluminium_frames','silicon','glass']
frelp_results['recovery_rate'] = [94,97,99.4,97,98]
frelp_results['mat_recycled_into_HQ'] = [100,100,100,100,100] #########MODIFY THIS BASED ON RESEARCH VALUES!


# In[21]:


frelp_results


# In[22]:


#Modify 'mat_EOL_Recycling_eff', 'mat_EOL_Recycled_into_HQ', 'mat_EOL_RecycledHQ_Reused4MFG' 
new_HQ4MFG = [100]*(2050-2021)
for mymaterial in MATERIALS: 
    #modifying 'mat_EOL_Recycling_eff'
    past_recycling_eff = [r2.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_Recycling_eff'][0]]*(2022-1995)
    new_recycling_eff = frelp_results[frelp_results.mat.isin([mymaterial])]['recovery_rate'].values.tolist()*(2050-2021)
    new_mat_EOL_recycling_eff = past_recycling_eff + new_recycling_eff
    #modifiying 'mat_EOL_Recycled_into_HQ'
    past_HQ_recycling = [r2.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_Recycled_into_HQ'][0]]*(2022-1995)
    new_HQ_recycling = frelp_results[frelp_results.mat.isin([mymaterial])]['mat_recycled_into_HQ'].values.tolist()*(2050-2021)
    new_mat_EOL_recycled_into_HQ = past_HQ_recycling + new_HQ_recycling
    #modifying 'mat_EOL_RecycledHQ_Reused4MFG' 
    past_HQ4MFG = list(r2.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_RecycledHQ_Reused4MFG'][0:27].values)
    new_recycledHQ_reused4MFG = past_HQ4MFG + new_HQ4MFG
    for myscenario in ABM_SCENARIOS:
        r2.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_Recycling_eff'] = new_mat_EOL_recycling_eff
        r2.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_Recycled_into_HQ'] = new_mat_EOL_recycled_into_HQ
        r2.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_RecycledHQ_Reused4MFG'] = new_recycledHQ_reused4MFG


# ## Modify parameters: Simulation 3 (r3), same installs for some scenarios: what is the effect of module reliability when recycle rates, reuse rates, repair rates, and recycling efficiencies changed for select scenarios with different repair bins?

# In[23]:


#Figure out which scenarios to include
#ABM_outputs.groupby('Scenario').sum()['mass_fraction_PV_materials_repaired_milliontonnes'].sort_values()
#calculate scenarios with highest repair rates: better lifetime, better learning, julien’s baseline, landfill ban
#only do better learning, julien’s baseline, landfill ban as better lifetime already had different reliability


# In[24]:


#copy same parameter modifications for each r3 simulation as in r2
new_HQ4MFG = [100]*(2050-2021)
for myr3simulation in r3_simulations:
    for myscenario in REPAIR_SCENARIOS:
        myr3simulation.scenario[myscenario].data['mod_EOL_collected_recycled'] = new_mod_recycled
    for mymaterial in MATERIALS:
        past_years_collected_recycled = [r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_collected_Recycled'][0]]*(2022-1995)
        new_collected_recycled = [100]*(2050-2021)
        #create new list to replace 'mod_EOL_collected_Recycled' with, with 1995-2021 original baseline module values, and 2022-2050 at 100%
        new_mat_recycled = past_years_collected_recycled + new_collected_recycled
        for myscenario in REPAIR_SCENARIOS:
            myr3simulation.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_collected_Recycled'] = new_mat_recycled
    for myscenario in REPAIR_SCENARIOS:
        frames1 = []
        frames2 = []
        frames3 = []
        new_outputs = []
        scenario_filter = []
        new_mod_Repairing = []
        new_mod_Recycling = []
        new_mod_Reuse = []
        scenario_filter = 'Scenario == ' + '\"' + myscenario + '\"'
        new_outputs = ABM_outputs.query(scenario_filter)
        #replace repairing baselines
        repairs = new_outputs.loc[:,'mass_fraction_PV_materials_repaired_milliontonnes']*100
        repairs.index = list(range(31))
        frames1 = [myr3simulation.scenario[myscenario].data['mod_Repair'][0:27],repairs[2:]]
        new_mod_Repairing = pd.concat(frames1)
        myr3simulation.scenario[myscenario].data['mod_Repair'] = new_mod_Repairing.values
        #replace recycling baselines
        recycled = new_outputs.loc[:,'mass_fraction_PV_materials_recycled_milliontonnes']*100
        if myscenario == 'high_mat_recovery_cheap_recycling':
            recycles = recycled/0.96 #reflects higher material recovery rate (must change as ABM gives effective recycling rate)
        else:
            recycles = recycled/0.80 #must change as ABM gives effective recycling rate
        recycles.index = list(range(31))
        frames2 = [myr3simulation.scenario[myscenario].data['mod_EOL_collection_eff'][0:27],recycles[2:]]
        new_mod_Recycling = pd.concat(frames2)
        myr3simulation.scenario[myscenario].data['mod_EOL_collection_eff'] = new_mod_Recycling.values
        #replace reuse baselines
        reuses = new_outputs.loc[:,'mass_fraction_PV_materials_reused_milliontonnes']*100
        reuses.index = list(range(31))
        frames3 = [myr3simulation.scenario[myscenario].data['mod_Reuse'][0:27],reuses[2:]]
        new_mod_Reuse = pd.concat(frames3)
        myr3simulation.scenario[myscenario].data['mod_Reuse'] = new_mod_Reuse.values
    for mymaterial in MATERIALS: 
        #modifying 'mat_EOL_Recycling_eff'
        past_recycling_eff = [r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_Recycling_eff'][0]]*(2022-1995)
        new_recycling_eff = frelp_results[frelp_results.mat.isin([mymaterial])]['recovery_rate'].values.tolist()*(2050-2021)
        new_mat_EOL_recycling_eff = past_recycling_eff + new_recycling_eff
        #modifiying 'mat_EOL_Recycled_into_HQ'
        past_HQ_recycling = [r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_Recycled_into_HQ'][0]]*(2022-1995)
        new_HQ_recycling = frelp_results[frelp_results.mat.isin([mymaterial])]['mat_recycled_into_HQ'].values.tolist()*(2050-2021)
        new_mat_EOL_recycled_into_HQ = past_HQ_recycling + new_HQ_recycling
        #modifying 'mat_EOL_RecycledHQ_Reused4MFG' 
        past_HQ4MFG = list(r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_RecycledHQ_Reused4MFG'][0:27].values)
        new_recycledHQ_reused4MFG = past_HQ4MFG + new_HQ4MFG
        for myscenario in REPAIR_SCENARIOS:
            myr3simulation.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_Recycling_eff'] = new_mat_EOL_recycling_eff
            myr3simulation.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_Recycled_into_HQ'] = new_mat_EOL_recycled_into_HQ
            myr3simulation.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_RecycledHQ_Reused4MFG'] = new_recycledHQ_reused4MFG
            
#also change mod_lifetime = 40 to agree with Irena RL
for myr3simulation in r3_simulations:
    for myscenario in REPAIR_SCENARIOS:
        old_lifetime = list(myr3simulation.scenario[myscenario].data['mod_lifetime'][0:27])
        irena_lifetime = [40] * (2050-2021)
        myr3simulation.scenario[myscenario].data['mod_lifetime'] = old_lifetime + irena_lifetime
    


# In[25]:


#modify shape parameters (overrides t50 and t90 baselines) -- values from Henry Hieslmair
weibullInputParamsA = {'alpha': 2.810, 'beta': 100.238} 
weibullInputParamsB = {'alpha': 3.841, 'beta': 57.491}
weibullInputParamsC = {'alpha': 4.602, 'beta': 40.767}
weibullInputParamsD = {'alpha': 5.692, 'beta': 29.697}


# ## Modify parameters: Simulation 4 (r4), change new installs due to increased installed capacity for all scenarios: what is effect of accounting for fewer installs for all scenarios on virgin material demand vs. r2? what is the effect on cumulative new installs and yearly virgin material demand for different repair bins?

# In[26]:


#modify parameters for r4
#copy same parameter modifications for r4 as in r2
for myscenario in ABM_SCENARIOS:
    r4.scenario[myscenario].data['mod_EOL_collected_recycled'] = new_mod_recycled
for mymaterial in MATERIALS:
    past_years_collected_recycled = [r4.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_collected_Recycled'][0]]*(2022-1995)
    new_collected_recycled = [100]*(2050-2021)
    #create new list to replace 'mod_EOL_collected_Recycled' with, with 1995-2021 original baseline module values, and 2022-2050 at 100%
    new_mat_recycled = past_years_collected_recycled + new_collected_recycled
    for myscenario in ABM_SCENARIOS:
        r4.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_collected_Recycled'] = new_mat_recycled
for myscenario in ABM_SCENARIOS:
    frames1 = []
    frames2 = []
    frames3 = []
    new_outputs = []
    scenario_filter = []
    new_mod_Repairing = []
    new_mod_Recycling = []
    new_mod_Reuse = []
    scenario_filter = 'Scenario == ' + '\"' + myscenario + '\"'
    new_outputs = ABM_outputs.query(scenario_filter)
    #replace repairing baselines
    repairs = new_outputs.loc[:,'mass_fraction_PV_materials_repaired_milliontonnes']*100
    repairs.index = list(range(31))
    frames1 = [r4.scenario[myscenario].data['mod_Repair'][0:27],repairs[2:]]
    new_mod_Repairing = pd.concat(frames1)
    r4.scenario[myscenario].data['mod_Repair'] = new_mod_Repairing.values
    #replace recycling baselines
    recycled = new_outputs.loc[:,'mass_fraction_PV_materials_recycled_milliontonnes']*100
    if myscenario == 'high_mat_recovery_cheap_recycling':
        recycles = recycled/0.96 #reflects higher material recovery rate (must change as ABM gives effective recycling rate)
    else:
        recycles = recycled/0.80 #must change as ABM gives effective recycling rate
    recycles.index = list(range(31))
    frames2 = [r4.scenario[myscenario].data['mod_EOL_collection_eff'][0:27],recycles[2:]]
    new_mod_Recycling = pd.concat(frames2)
    r4.scenario[myscenario].data['mod_EOL_collection_eff'] = new_mod_Recycling.values
    #replace reuse baselines
    reuses = new_outputs.loc[:,'mass_fraction_PV_materials_reused_milliontonnes']*100
    reuses.index = list(range(31))
    frames3 = [r4.scenario[myscenario].data['mod_Reuse'][0:27],reuses[2:]]
    new_mod_Reuse = pd.concat(frames3)
    r4.scenario[myscenario].data['mod_Reuse'] = new_mod_Reuse.values

#also change mod_lifetime = 40 to agree with Irena RL
for myscenario in ABM_SCENARIOS:
    old_lifetime = list(r4.scenario[myscenario].data['mod_lifetime'][0:27])
    irena_lifetime = [40] * (2050-2021)
    r4.scenario[myscenario].data['mod_lifetime'] = old_lifetime + irena_lifetime    

r4.scenario['better_lifetime'].data['mod_lifetime'] = new_mod_lifetime
r4.scenario['better_lifetime'].data['mod_reliability_t50'] = new_mod_t50
r4.scenario['better_lifetime'].data['mod_reliability_t90'] = new_mod_t90

new_HQ4MFG = [100]*(2050-2021)
for mymaterial in MATERIALS: 
    #modifying 'mat_EOL_Recycling_eff'
    past_recycling_eff = [r4.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_Recycling_eff'][0]]*(2022-1995)
    new_recycling_eff = frelp_results[frelp_results.mat.isin([mymaterial])]['recovery_rate'].values.tolist()*(2050-2021)
    new_mat_EOL_recycling_eff = past_recycling_eff + new_recycling_eff
    #modifiying 'mat_EOL_Recycled_into_HQ'
    past_HQ_recycling = [r4.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_Recycled_into_HQ'][0]]*(2022-1995)
    new_HQ_recycling = frelp_results[frelp_results.mat.isin([mymaterial])]['mat_recycled_into_HQ'].values.tolist()*(2050-2021)
    new_mat_EOL_recycled_into_HQ = past_HQ_recycling + new_HQ_recycling
    #modifying 'mat_EOL_RecycledHQ_Reused4MFG' 
    past_HQ4MFG = list(r4.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_RecycledHQ_Reused4MFG'][0:27].values)
    new_recycledHQ_reused4MFG = past_HQ4MFG + new_HQ4MFG
    for myscenario in ABM_SCENARIOS:
        r4.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_Recycling_eff'] = new_mat_EOL_recycling_eff
        r4.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_Recycled_into_HQ'] = new_mat_EOL_recycled_into_HQ
        r4.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_RecycledHQ_Reused4MFG'] = new_recycledHQ_reused4MFG


# In[27]:


#modify parameters for r4A, r4B, r4C, r4D (same as r3 modifications)
new_HQ4MFG = [100]*(2050-2021)
for myr4simulation in r4_simulations:
    for myscenario in REPAIR_SCENARIOS:
        myr4simulation.scenario[myscenario].data['mod_EOL_collected_recycled'] = new_mod_recycled
    for mymaterial in MATERIALS:
        past_years_collected_recycled = [r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_collected_Recycled'][0]]*(2022-1995)
        new_collected_recycled = [100]*(2050-2021)
        #create new list to replace 'mod_EOL_collected_Recycled' with, with 1995-2021 original baseline module values, and 2022-2050 at 100%
        new_mat_recycled = past_years_collected_recycled + new_collected_recycled
        for myscenario in REPAIR_SCENARIOS:
            myr4simulation.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_collected_Recycled'] = new_mat_recycled
    for myscenario in REPAIR_SCENARIOS:
        frames1 = []
        frames2 = []
        frames3 = []
        new_outputs = []
        scenario_filter = []
        new_mod_Repairing = []
        new_mod_Recycling = []
        new_mod_Reuse = []
        scenario_filter = 'Scenario == ' + '\"' + myscenario + '\"'
        new_outputs = ABM_outputs.query(scenario_filter)
        #replace repairing baselines
        repairs = new_outputs.loc[:,'mass_fraction_PV_materials_repaired_milliontonnes']*100
        repairs.index = list(range(31))
        frames1 = [myr4simulation.scenario[myscenario].data['mod_Repair'][0:27],repairs[2:]]
        new_mod_Repairing = pd.concat(frames1)
        myr4simulation.scenario[myscenario].data['mod_Repair'] = new_mod_Repairing.values
        #replace recycling baselines
        recycled = new_outputs.loc[:,'mass_fraction_PV_materials_recycled_milliontonnes']*100
        if myscenario == 'high_mat_recovery_cheap_recycling':
            recycles = recycled/0.96 #reflects higher material recovery rate (must change as ABM gives effective recycling rate)
        else:
            recycles = recycled/0.80 #must change as ABM gives effective recycling rate
        recycles.index = list(range(31))
        frames2 = [myr4simulation.scenario[myscenario].data['mod_EOL_collection_eff'][0:27],recycles[2:]]
        new_mod_Recycling = pd.concat(frames2)
        myr4simulation.scenario[myscenario].data['mod_EOL_collection_eff'] = new_mod_Recycling.values
        #replace reuse baselines
        reuses = new_outputs.loc[:,'mass_fraction_PV_materials_reused_milliontonnes']*100
        reuses.index = list(range(31))
        frames3 = [myr4simulation.scenario[myscenario].data['mod_Reuse'][0:27],reuses[2:]]
        new_mod_Reuse = pd.concat(frames3)
        myr4simulation.scenario[myscenario].data['mod_Reuse'] = new_mod_Reuse.values
    for mymaterial in MATERIALS: 
        #modifying 'mat_EOL_Recycling_eff'
        past_recycling_eff = [r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_Recycling_eff'][0]]*(2022-1995)
        new_recycling_eff = frelp_results[frelp_results.mat.isin([mymaterial])]['recovery_rate'].values.tolist()*(2050-2021)
        new_mat_EOL_recycling_eff = past_recycling_eff + new_recycling_eff
        #modifiying 'mat_EOL_Recycled_into_HQ'
        past_HQ_recycling = [r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_Recycled_into_HQ'][0]]*(2022-1995)
        new_HQ_recycling = frelp_results[frelp_results.mat.isin([mymaterial])]['mat_recycled_into_HQ'].values.tolist()*(2050-2021)
        new_mat_EOL_recycled_into_HQ = past_HQ_recycling + new_HQ_recycling
        #modifying 'mat_EOL_RecycledHQ_Reused4MFG' 
        past_HQ4MFG = list(r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_RecycledHQ_Reused4MFG'][0:27].values)
        new_recycledHQ_reused4MFG = past_HQ4MFG + new_HQ4MFG
        for myscenario in REPAIR_SCENARIOS:
            myr4simulation.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_Recycling_eff'] = new_mat_EOL_recycling_eff
            myr4simulation.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_Recycled_into_HQ'] = new_mat_EOL_recycled_into_HQ
            myr4simulation.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_RecycledHQ_Reused4MFG'] = new_recycledHQ_reused4MFG
            
#also change mod_lifetime = 40 to agree with Irena RL
for myr4simulation in r4_simulations:
    for myscenario in REPAIR_SCENARIOS:
        old_lifetime = list(myr4simulation.scenario[myscenario].data['mod_lifetime'][0:27])
        irena_lifetime = [40] * (2050-2021)
        myr4simulation.scenario[myscenario].data['mod_lifetime'] = old_lifetime + irena_lifetime


# ## Run Mass Flow Calculations

# In[35]:


r1.calculateMassFlow(weibullInputParams= weibull_IrenaRL)
r2.calculateMassFlow(weibullInputParams= weibull_IrenaRL)
r3A.calculateMassFlow(weibullInputParams= weibullInputParamsA)
r3B.calculateMassFlow(weibullInputParams= weibullInputParamsB)
r3C.calculateMassFlow(weibullInputParams= weibullInputParamsC)
r3D.calculateMassFlow(weibullInputParams= weibullInputParamsD)
r4.calculateMassFlow(weibullInputParams= weibull_IrenaRL)
r4A.calculateMassFlow(weibullInputParams= weibullInputParamsA)
r4B.calculateMassFlow(weibullInputParams= weibullInputParamsB)
r4C.calculateMassFlow(weibullInputParams= weibullInputParamsC)
r4D.calculateMassFlow(weibullInputParams= weibullInputParamsD)


# In[36]:


Under_Installment = []
scenarios = ['standard_PVICE','landfill_ban','high_mat_recovery_cheap_recycling','cheap_recycling','high_landfill_costs','better_lifetime','better_learning','reuse_warranties','seeding_reuse','juliens_baseline']
for i in range (0, len(r4.scenario['juliens_baseline'].data)): #runs for each year
    for myscenario in scenarios[1:9]:
        Under_Installment = ( (r4.scenario['juliens_baseline'].data['Installed_Capacity_[W]'][i] - 
                         r4.scenario[myscenario].data['Installed_Capacity_[W]'][i])/1000000 )  # MWATTS
        r4.scenario[myscenario].data['new_Installed_Capacity_[MW]'][i] += Under_Installment
    r4.calculateMassFlow(weibullInputParams= weibull_IrenaRL)


# In[37]:


Under_Installment = []
weibullparams = [weibullInputParamsA, weibullInputParamsB, weibullInputParamsC, weibullInputParamsD]
for myr4simulation in r4_simulations:
    myweibullparams = weibullparams[r4_simulations.index(myr4simulation)]
    for i in range (0, len(myr4simulation.scenario['juliens_baseline'].data)): #runs for each year
        for myscenario in REPAIR_SCENARIOS:
            Under_Installment = ((myr4simulation.scenario['juliens_baseline'].data['Installed_Capacity_[W]'][i] - 
                             myr4simulation.scenario[myscenario].data['Installed_Capacity_[W]'][i])/1000000 )  # MWATTS
            myr4simulation.scenario[myscenario].data['new_Installed_Capacity_[MW]'][i] += Under_Installment
        myr4simulation.calculateMassFlow(weibullInputParams= myweibullparams)


# ## Creating a summary of results in a new data frame

# In[38]:


USyearly=pd.DataFrame()


# In[39]:


keyword='mat_Virgin_Stock'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']
SIMULATIONS = [r1,r2, r3A, r3B, r3C, r3D, r4, r4A, r4B, r4C, r4D]

# Loop over Simulations
for mysimulation in SIMULATIONS:
    for jj in range(0, len(mysimulation.scenario)): # Loop over Scenarios
        case = list(mysimulation.scenario.keys())[jj] # case gives scenario name
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["VirginStock_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
        filter_col = [col for col in USyearly if (col.startswith('VirginStock') and col.endswith(mysimulation.name+'_'+case)) ]
        USyearly['VirginStock_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[40]:


keyword='mat_Total_Landfilled'

for mysimulation in SIMULATIONS:
    for jj in range(0, len(mysimulation.scenario)): #goes from 0 to 9
        case = list(mysimulation.scenario.keys())[jj]
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["Waste_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
        filter_col = [col for col in USyearly if (col.startswith('Waste') and col.endswith(mysimulation.name+'_'+case)) ]
        USyearly['Waste_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[41]:


keyword='mat_Total_EOL_Landfilled'

for mysimulation in SIMULATIONS:
    for jj in range(0, len(mysimulation.scenario)): #goes from 0 to 9
        case = list(mysimulation.scenario.keys())[jj]
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["Waste_EOL_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
        filter_col = [col for col in USyearly if (col.startswith('Waste_EOL') and col.endswith(mysimulation.name+'_'+case)) ]
        USyearly['Waste_EOL_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[42]:


USyearly = USyearly/1000000  #Convert to metric tonnes
#907185 -- this is for US tons


# In[43]:


keyword='new_Installed_Capacity_[MW]'

#for simulations r1 through r4
for mysimulation in SIMULATIONS[0:7]:
    newcolname = keyword+'_'+mysimulation.name 
    if newcolname in USyearly:
        USyearly[newcolname] = USyearly[newcolname]+mysimulation.scenario[list(mysimulation.scenario.keys())[0]].data[keyword]
    else:
        USyearly[keyword+'_'+mysimulation.name] = mysimulation.scenario[list(mysimulation.scenario.keys())[0]].data[keyword]

#for simulations r4A through r4D
#this is not working for some reason...
for mysimulation in SIMULATIONS[7:]:
    for myscenario in REPAIR_SCENARIOS:
        newcolname = keyword+'_'+mysimulation.name+'_'+myscenario
        if newcolname in USyearly:
            USyearly[newcolname] = USyearly[newcolname]+mysimulation.scenario[myscenario].data[keyword]
        else:
            USyearly[newcolname] = mysimulation.scenario[myscenario].data[keyword]


# In[44]:


UScum = USyearly.copy()
UScum = UScum.cumsum()


# In[45]:


keyword='Installed_Capacity_[W]'

for mysimulation in SIMULATIONS:
    for i in range(0, len(mysimulation.scenario)):
        case = list(mysimulation.scenario.keys())[i]
        foo = mysimulation.scenario[case].data[keyword]
        foo = foo.to_frame(name=keyword)
        UScum["Capacity_"+mysimulation.name+'_'+case] = foo[keyword].values/1000000 #change to MW


# In[46]:


USyearly.index = r1.scenario['standard_PVICE'].data['year']
UScum.index = r1.scenario['standard_PVICE'].data['year']


# In[47]:


USyearly.to_csv('ABM_Yearly_Results.csv')
UScum.to_csv('ABM_Cumulative_Results.csv')


# ### Plotting with USyearly and UScum data frames: r1

# In[48]:


filter_col = [col for col in USyearly if (col.startswith('VirginStock_Module_ABM_Simulation1'))]
df = USyearly[filter_col]
pretty_scenarios = ['PV ICE Baseline','Landfill Ban','High material recovery and Lower recycling costs','Lower recycling costs','Higher landfill costs','Improved lifetime','Improved learning effect','Reuse warranties','Seeding reuse','ABM Baseline']
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'variable', labels={
                     "year": "Year",
                     "value": "Virgin Material Demand [metric tonnes]",
                    "variable" :"Scenario"
                 })
fig1.update_layout(title_text='Simulation 1: Yearly Virgin Material Demand', title_x=0.2)
fig1.show()


# In[49]:


filter_col = [col for col in USyearly if (col.startswith('Waste_Module_ABM_Simulation1'))]
df = USyearly[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'variable', labels={
                     "year": "Year",
                     "value": "Waste [metric tonnes]",
                    "variable" :"Scenario"
                 })
fig1.update_layout(title_text='Simulation 1: Yearly Waste', title_x=0.25)
fig1.show()


# In[50]:


filter_col = [col for col in UScum if (col.startswith('Capacity_ABM_Simulation1'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'variable', labels={
                     "year": "Year",
                     "value": "Installed Capacity [MW]",
                    "variable" :"Scenario"
                 })
fig1.update_layout(title_text='Simulation 1: Installed Capacity', title_x=0.2)
fig1.show()


# ### Plotting with USyearly and UScum data frames: r2

# In[51]:


filter_col = [col for col in USyearly if (col.startswith('VirginStock_Module_ABM_Simulation2'))]
df = USyearly[filter_col]
pretty_scenarios = ['PV ICE Baseline','Landfill Ban','High material recovery and Lower recycling costs','Lower recycling costs','Higher landfill costs','Improved lifetime','Improved learning effect','Reuse warranties','Seeding reuse','ABM Baseline']
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'variable', labels={
                     "year": "Year",
                     "value": "Virgin Material Demand [metric tonnes]",
                    "variable" :"Scenario"
                 })
fig1.update_layout(title_text='Simulation 2: Yearly Virgin Material Demand', title_x=0.2)
fig1.show()


# In[52]:


#cumulative at 2050 results for Virgin Material Demand
filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation2'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin([2050])]
df.sort_values('value')


# In[53]:


filter_col = [col for col in USyearly if (col.startswith('Waste_Module_ABM_Simulation2'))]
df = USyearly[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'variable', labels={
                     "year": "Year",
                     "value": "Waste [metric tonnes]",
                    "variable" :"Scenario"
                 })
fig1.update_layout(title_text='Simulation 2: Yearly Waste', title_x=0.25)
fig1.show()


# In[54]:


#cumulative at 2050 results for Waste
filter_col = [col for col in UScum if (col.startswith('Waste_Module_ABM_Simulation2'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin([2050])]
df.sort_values('value')


# ### Plotting with USyearly and UScum data frames: r3

# In[55]:


filter_col = [col for col in UScum if (col.startswith('Waste_Module_ABM_Simulation3'))]
df = UScum[filter_col]
#pretty_repair_scenarios = ['Improved Learning Effect', 'ABM Baseline', 'Landfill Ban']
#df = df.set_axis(pretty_repair_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
scenario_splices = []
for i in range(0,len(df['variable'])):
    scenario_splices += [df.loc[i,'variable'][30:]]
quality_splices = []
for i in range(0,len(df['variable'])):
    quality_splices += [df.loc[i,'variable'][28]]
df['scenario'] = scenario_splices
df['repair_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'repair_bin', facet_col = 'scenario', labels={
                     "year": "Year",
                     "value": "Cumulative Waste [metric tonnes]",
                    "repair_bin":"Repair Bin"
                })
fig1.update_layout(title_text='Simulation 3: Cumulative Waste for Different Repair Bins', title_x=0.5)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
fig1.update_xaxes(tickangle=-45)
fig1.show()


# In[56]:


filter_col = [col for col in UScum if (col.startswith('Capacity_ABM_Simulation3'))]
df = UScum[filter_col]
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
scenario_splices = []
for i in range(0,len(df['variable'])):
    scenario_splices += [df.loc[i,'variable'][26:]]
quality_splices = []
for i in range(0,len(df['variable'])):
    quality_splices += [df.loc[i,'variable'][24]]
df['scenario'] = scenario_splices
df['repair_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'repair_bin', facet_col = 'scenario', labels={
                     "year": "Year",
                     "value": "Installed Capacity [MW]",
                    "repair_bin":"Repair Bin"
                })
fig1.update_layout(title_text='Simulation 3: Installed Capacity for Different Repair Bins', title_x=0.5)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
fig1.update_xaxes(tickangle=-45)
fig1.show()


# ### Plotting with USyearly and UScum data frames: r4

# In[57]:


filter_col = [col for col in USyearly if (col.startswith('VirginStock_Module_ABM_Simulation4_'))]
df = USyearly[filter_col]
pretty_scenarios = ['PV ICE Baseline','Landfill Ban','High material recovery and Lower recycling costs','Lower recycling costs','Higher landfill costs','Improved lifetime','Improved learning effect','Reuse warranties','Seeding reuse','ABM Baseline']
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'variable', labels={
                     "year": "Year",
                     "value": "Virgin Material Demand [metric tonnes]",
                    "variable" :"Scenario"
                 })
fig1.update_layout(title_text='Simulation 4: Yearly Virgin Material Demand with Fewer New Installs', title_x=0.07)
fig1.show()


# In[58]:


#cumulative at 2050 results for Virgin Material Demand
filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation4_'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin([2050])]
df.sort_values('value')


# In[59]:


filter_col = [col for col in UScum if (col.startswith(('new_Installed_Capacity_[MW]_ABM_Simulation4A','new_Installed_Capacity_[MW]_ABM_Simulation4B','new_Installed_Capacity_[MW]_ABM_Simulation4C','new_Installed_Capacity_[MW]_ABM_Simulation4D')))]
df = UScum[filter_col]
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
scenario_splices = []
for i in range(0,len(df['variable'])):
    scenario_splices += [df.loc[i,'variable'][45:]]
quality_splices = []
for i in range(0,len(df['variable'])):
    quality_splices += [df.loc[i,'variable'][43]]
df['scenario'] = scenario_splices
df['repair_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'repair_bin', facet_col = 'scenario', labels={
                     "year": "Year",
                     "value": "Cumulative Waste [metric tonnes]",
                    "repair_bin":"Repair Bin"
                })
fig1.update_layout(title_text='Simulation 4: Cumulative New Installs for Different Repair Bins with Fewer New Installs', title_x=0.5)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
fig1.update_xaxes(tickangle=-45)
fig1.show()


# In[60]:


filter_col = [col for col in USyearly if (col.startswith(('VirginStock_Module_ABM_Simulation4A','VirginStock_Module_ABM_Simulation4B','VirginStock_Module_ABM_Simulation4C','VirginStock_Module_ABM_Simulation4D')))]
df = USyearly[filter_col]
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
scenario_splices = []
for i in range(0,len(df['variable'])):
    scenario_splices += [df.loc[i,'variable'][36:]]
quality_splices = []
for i in range(0,len(df['variable'])):
    quality_splices += [df.loc[i,'variable'][34]]
df['scenario'] = scenario_splices
df['repair_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'repair_bin', facet_col = 'scenario', labels={
                     "year": "Year",
                     "value": "Yearly Virgin Material Demand [metric tonnes]",
                    "repair_bin":"Repair Bin"
                })
fig1.update_layout(title_text='Simulation 4: Yearly Virgin Material Demand for Different Repair Bins with Fewer New Installs', title_x=0.5)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
fig1.update_xaxes(tickangle=-45)
fig1.show()


# ## Clean up results for OpenEI export

# ### Yearly Results

# In[ ]:


yearly_scenario_comparison = pd.DataFrame()


# In[ ]:


#use scenarios as values
years = USyearly.index
yearly_scenario_comparison['@timeseries|Year'] = list(years)


# In[ ]:


scenarios = ['standard_PVICE','landfill_ban','high_mat_recovery_cheap_recycling','cheap_recycling','high_landfill_costs','better_lifetime','better_learning','reuse_warranties','seeding_reuse','juliens_baseline']
pretty_scenarios = ['PV ICE Baseline','Landfill Ban','High material recovery and Lower recycling costs','Lower recycling costs','Higher landfill costs','Improved lifetime','Improved learning effect','Reuse warranties','Seeding reuse','ABM Baseline']

#virgin material demand columns
for myscenario in scenarios:
    better_scenario_name = pretty_scenarios[scenarios.index(myscenario)]
    virgin_material_demand = USyearly['VirginStock_glass_ABM_Simulation_' + myscenario] + USyearly['VirginStock_aluminium_frames_ABM_Simulation_' + myscenario] + USyearly['VirginStock_silver_ABM_Simulation_' + myscenario] + USyearly['VirginStock_silicon_ABM_Simulation_' + myscenario] + USyearly['VirginStock_copper_ABM_Simulation_' + myscenario]
    yearly_scenario_comparison['@value|TotalVirginMaterialDemand|' + better_scenario_name + '#MetricTonnes'] = list(virgin_material_demand.values)
    


# In[ ]:


#EOL material columns
for myscenario in scenarios:
    better_scenario_name = pretty_scenarios[scenarios.index(myscenario)]
    total_eol_material = USyearly['Waste_EOL_glass_ABM_Simulation_' + myscenario] + USyearly['Waste_EOL_aluminium_frames_ABM_Simulation_' + myscenario] + USyearly['Waste_EOL_silver_ABM_Simulation_' + myscenario] + USyearly['Waste_EOL_silicon_ABM_Simulation_' + myscenario] + USyearly['Waste_EOL_copper_ABM_Simulation_' + myscenario]
    yearly_scenario_comparison['@value|TotalEOLMaterial|' + better_scenario_name + '#MetricTonnes'] = list(total_eol_material.values)


# In[ ]:


yearly_scenario_comparison.to_csv('ABM_Yearly, with Scenario Comparison, Materials Summed.csv')


# ### Cumulative Results

# In[ ]:


cumulative_ABM = pd.DataFrame()


# In[ ]:


scenarios = ['standard_PVICE','landfill_ban','high_mat_recovery_cheap_recycling','cheap_recycling','high_landfill_costs','better_lifetime','better_learning','reuse_warranties','seeding_reuse','juliens_baseline']
pretty_scenarios = ['PV ICE Baseline','Landfill Ban','High material recovery and Lower recycling costs','Lower recycling costs','Higher landfill costs','Improved lifetime','Improved learning effect','Reuse warranties','Seeding reuse','ABM Baseline']
list1 = []
for myscenario in pretty_scenarios: 
    list1 += [myscenario] * (2050-1994)
cumulative_ABM['@scenario|Intervention Scenario'] = list1


# In[ ]:


years = USyearly.index
cumulative_ABM['@timeseries|Year'] = list(years) * 10


# In[ ]:


#Virgin Material Demand Columns
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    virgin_material_demand = []
    for myscenario in scenarios: 
        virgin_material_demand += list(UScum['VirginStock_'+ mymaterial + '_ABM_Simulation_'+ myscenario].values)
    cumulative_ABM['@value|VirginMaterialDemand|' + better_material_name + '#MetricTonnes'] = virgin_material_demand


# In[ ]:


#EOL Material Columns
materials = ['glass','aluminium_frames','silver','silicon','copper']
pretty_materials = ['Glass','AluminiumFrames','Silver','Silicon','Copper']
for mymaterial in materials:
    better_material_name = pretty_materials[materials.index(mymaterial)]
    eol_material = []
    for myscenario in scenarios: 
        eol_material += list(UScum['Waste_EOL_'+ mymaterial + '_ABM_Simulation_'+ myscenario].values)
    cumulative_ABM['@value|EOLMaterial|' + better_material_name + '#MetricTonnes'] = eol_material


# In[ ]:


#filter for decade increments
df_new = cumulative_ABM.rename(columns={'@timeseries|Year':'year'})
cumulative_ABM = cumulative_ABM[df_new.year.isin([2020, 2030,2040,2050])]
cumulative_ABM = cumulative_ABM.rename(columns={'year':'@timeseries|Year'})


# In[ ]:


cumulative_ABM.to_csv('ABM_Cumulative with Decade Increments.csv')


# In[ ]:


#create a cumulative at 2050 file
cumulative_ABM_2050 = pd.DataFrame()


# In[ ]:


cumulative_ABM_2050["@scenario|PVICEOutput"] = ['Virgin Material Demand MT','EOL Material MT','Installed Capacity MW']


# In[ ]:


cumulative_ABM_2050["@timeseries|Year"] = [2050,2050,2050]


# In[ ]:


UScum2050 = UScum.iloc[-1:]
scenarios = ['standard_PVICE','landfill_ban','high_mat_recovery_cheap_recycling','cheap_recycling','high_landfill_costs','better_lifetime','better_learning','reuse_warranties','seeding_reuse','juliens_baseline']
pretty_scenarios = ['PV ICE Baseline','Landfill Ban','High material recovery and Lower recycling costs','Lower recycling costs','Higher landfill costs','Improved lifetime','Improved learning effect','Reuse warranties','Seeding reuse','ABM Baseline']
list1 = []
for myscenario in scenarios: 
    better_scenario_name = pretty_scenarios[scenarios.index(myscenario)]
    virgin_material_demand = [UScum2050['VirginStock_Module_ABM_Simulation_' + myscenario].values] #MT
    eol_material = [UScum2050['Waste_EOL_Module_ABM_Simulation_' + myscenario].values] #MT
    installed_capacity = [UScum2050['Capacity_ABM_Simulation_' + myscenario].values/1000000] #MW
    cumulative_ABM_2050['@value|InterventionScenario|'+better_scenario_name+'#Units'] = virgin_material_demand + eol_material + installed_capacity


# In[ ]:


cumulative_ABM_2050 = cumulative_ABM_2050.applymap(str)
colnames = list(cumulative_ABM_2050.columns)[1:]
for col in colnames:
    cumulative_ABM_2050[col] = cumulative_ABM_2050[col].str.strip('[]')


# In[ ]:


cumulative_ABM_2050.to_csv('ABM_cumulative_at_2050_toOPENEI.csv')


# In[ ]:


#Create installed capacity CSV
installed_capacity = pd.DataFrame()


# In[ ]:


years = USyearly.index
installed_capacity['@timeseries|Year'] = years


# In[ ]:


scenarios = ['standard_PVICE','landfill_ban','high_mat_recovery_cheap_recycling','cheap_recycling','high_landfill_costs','better_lifetime','better_learning','reuse_warranties','seeding_reuse','juliens_baseline']
pretty_scenarios = ['PV ICE Baseline','Landfill Ban','High material recovery and Lower recycling costs','Lower recycling costs','Higher landfill costs','Improved lifetime','Improved learning effect','Reuse warranties','Seeding reuse','ABM Baseline']
for myscenario in scenarios:
    capacity = UScum['Capacity_ABM_Simulation_'+ myscenario]
    better_scenario_name = pretty_scenarios[scenarios.index(myscenario)]
    installed_capacity['@value|InstalledCapacity|' + better_scenario_name + '#MW'] = list(capacity.values/1000000) #convert from W to MW


# In[ ]:


installed_capacity.to_csv('ABM_installed_capacity.csv')


# ### Calculating Number of Less Installs Needed For Each Scenario

# In[ ]:


Under_Installment = []
scenarios = ['standard_PVICE','landfill_ban','high_mat_recovery_cheap_recycling','cheap_recycling','high_landfill_costs','better_lifetime','better_learning','reuse_warranties','seeding_reuse','juliens_baseline']
for i in range (0, len(r1.scenario['juliens_baseline'].data)): #runs for each year
    for myscenario in scenarios[1:9]:
        Under_Installment = ( (r1.scenario['juliens_baseline'].data['Installed_Capacity_[W]'][i] - 
                         r1.scenario[myscenario].data['Installed_Capacity_[W]'][i])/1000000 )  # MWATTS
        r1.scenario[myscenario].data['new_Installed_Capacity_[MW]'][i] += Under_Installment
    r1.calculateMassFlow()


# In[ ]:


# Compare cumulative virgin material needs by 2050
USyearly_fewerinstalls=pd.DataFrame()


# In[ ]:


keyword='mat_Virgin_Stock'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']

# Loop over Scenarios
for jj in range(0, len(r1.scenario)): #goes from 0 to 9
    case = list(r1.scenario.keys())[jj] #case gives scenario name
    for ii in range (0, len(materials)):    
        material = materials[ii]
        foo = r1.scenario[case].material[material].materialdata[keyword].copy()
        foo = foo.to_frame(name=material)
        USyearly_fewerinstalls["VirginStock_"+material+'_'+r1.name+'_'+case] = foo[material]
    filter_col = [col for col in USyearly_fewerinstalls if (col.startswith('VirginStock') and col.endswith(r1.name+'_'+case)) ]
    USyearly_fewerinstalls['VirginStock_Module_'+r1.name+'_'+case] = USyearly_fewerinstalls[filter_col].sum(axis=1)


# In[ ]:


keyword='mat_Total_Landfilled'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']

# Loop over Scenarios
for jj in range(0, len(r1.scenario)): #goes from 0 to 9
    case = list(r1.scenario.keys())[jj]
    for ii in range (0, len(materials)):    
        material = materials[ii]
        foo = r1.scenario[case].material[material].materialdata[keyword].copy()
        foo = foo.to_frame(name=material)
        USyearly_fewerinstalls["Waste_"+material+'_'+r1.name+'_'+case] = foo[material]
    filter_col = [col for col in USyearly_fewerinstalls if (col.startswith('Waste') and col.endswith(r1.name+'_'+case)) ]
    USyearly_fewerinstalls['Waste_Module_'+r1.name+'_'+case] = USyearly_fewerinstalls[filter_col].sum(axis=1)


# In[ ]:


keyword='mat_Total_EOL_Landfilled'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']

# Loop over Scenarios
for jj in range(0, len(r1.scenario)): #goes from 0 to 9
    case = list(r1.scenario.keys())[jj]
    for ii in range (0, len(materials)):    
        material = materials[ii]
        foo = r1.scenario[case].material[material].materialdata[keyword].copy()
        foo = foo.to_frame(name=material)
        USyearly_fewerinstalls["Waste_EOL_"+material+'_'+r1.name+'_'+case] = foo[material]
    filter_col = [col for col in USyearly_fewerinstalls if (col.startswith('Waste_EOL') and col.endswith(r1.name+'_'+case)) ]
    USyearly_fewerinstalls['Waste_EOL_Module_'+r1.name+'_'+case] = USyearly_fewerinstalls[filter_col].sum(axis=1)


# In[ ]:


USyearly_fewerinstalls = USyearly_fewerinstalls/1000000  #Convert to metric tonnes


# In[ ]:


keyword='new_Installed_Capacity_[MW]'

newcolname = keyword+'_'+r1.name
    
if newcolname in USyearly_fewerinstalls:
    USyearly_fewerinstalls[newcolname] = USyearly_fewerinstalls[newcolname]+r1.scenario[list(r1.scenario.keys())[0]].data[keyword]
else:
    USyearly_fewerinstalls[keyword+'_'+r1.name] = r1.scenario[list(r1.scenario.keys())[0]].data[keyword]


# In[ ]:


UScum_fewerinstalls = USyearly_fewerinstalls.copy()
UScum_fewerinstalls = UScum_fewerinstalls.cumsum()


# In[ ]:


keyword='Installed_Capacity_[W]'

# Loop over Scenarios
for i in range(0, len(r1.scenario)):
    case = list(r1.scenario.keys())[i]
    foo = r1.scenario[case].data[keyword]
    foo = foo.to_frame(name=keyword)
    UScum_fewerinstalls["Capacity_"+r1.name+'_'+case] = foo[keyword].values #this needs to be .values
    ########SHOULD THIS BE CHANGED TO BE IN MW?


# In[ ]:


USyearly_fewerinstalls.index = r1.scenario['standard_PVICE'].data['year']
UScum_fewerinstalls.index = r1.scenario['standard_PVICE'].data['year']


# In[ ]:


USyearly_fewerinstalls.to_csv('ABM_Yearly_Results_Fewer_Installs.csv')
UScum_fewerinstalls.to_csv('ABM_Cumulative_Results_Fewer_Installs.csv')


# In[ ]:


#Other Results for UScum_fewerinstalls:
cum_Waste = [] #metric tonnes
cum_EOL_Waste = [] #metric tonnes
cum_VirginNeeds = [] #metric tonnes
cum_InstalledCapacity = [] #MW
cum_NewInstalls = [] #W

for ii in range (0, len(r1.scenario.keys())): #0 to 9
    # Cumulative for all materials (not just glass) at 2050
    scen = list(r1.scenario.keys())[ii]
    cum_Waste.append(UScum_fewerinstalls['Waste_Module_ABM_Simulation_' + scen][2050])
    cum_EOL_Waste.append(UScum_fewerinstalls['Waste_EOL_Module_ABM_Simulation_' + scen][2050])
    cum_VirginNeeds.append((UScum_fewerinstalls['VirginStock_Module_ABM_Simulation_' + scen][2050]))
    cum_NewInstalls.append(r1.scenario[scen].data['new_Installed_Capacity_[MW]'].sum())
    cum_InstalledCapacity.append(r1.scenario[scen].data['Installed_Capacity_[W]'].iloc[-1])

df = pd.DataFrame(list(zip(list(r1.scenario.keys()), cum_Waste, cum_EOL_Waste, cum_VirginNeeds, cum_NewInstalls, cum_InstalledCapacity)),
               columns =['scenarios','cum_Waste', 'cum_EOL_Waste', 'cum_VirginNeeds', 'cum_NewInstalls', 'cum_InstalledCapacity'])


# In[ ]:


#Best interventions to minimize cum_Waste: 
#better learning, reuse warranties, high material recovery and cheap recycling, better lifetime
df.sort_values('cum_Waste') 


# In[ ]:


#Best interventions to minimize cum_EOL_Waste: 
#better learning, reuse warranties, high material recovery and cheap recycling, better lifetime
df.sort_values('cum_EOL_Waste') 


# In[ ]:


#Best interventions to minimize cum_VirginNeeds:
#better_learning, reuse_warranties, high_mat_recovery_cheap_recycling, better_lifetime
df.sort_values('cum_VirginNeeds')


# In[ ]:


#Best interventions to minimize cum_NewInstalls:
#better lifetime, standard PVICE, ABM baseline, landfill ban
df.sort_values('cum_NewInstalls')


# In[ ]:


#Looking in terms of percentages
df[['cum_Waste', 'cum_EOL_Waste', 'cum_VirginNeeds', 'cum_NewInstalls', 'cum_InstalledCapacity']] = df[['cum_Waste','cum_EOL_Waste', 'cum_VirginNeeds', 'cum_NewInstalls', 'cum_InstalledCapacity']]*100/df[['cum_Waste', 'cum_EOL_Waste','cum_VirginNeeds', 'cum_NewInstalls', 'cum_InstalledCapacity']].iloc[9] -100


# In[ ]:


## Experimenting with Plotly


# In[ ]:


fig1 = px.bar(df, x='scenarios', y='cum_Waste', labels={
                     "cum_Waste": "Cumulative Waste Percent Difference",
                     "scenarios": "Scenario"
                 })
fig1.update_layout(title_text='Cumulative Waste Percent Difference from Baseline at 2050', title_x=0.5)
fig1.show()


# In[ ]:


fig = px.bar(df, x='scenarios', y='cum_VirginNeeds')
fig.show()


# In[ ]:


percent_diff = df.melt(id_vars = 'scenarios')
percent_diff = percent_diff.rename(columns={'value': 'percent_difference_from_baseline'})


# In[ ]:


px.scatter(percent_diff, x = 'scenarios', y = 'percent_difference_from_baseline',color = 'variable', title = 'Percent Difference from Baseline at 2050',
          labels={
                     "percent_difference_from_baseline": "Percent Difference from Baseline at 2050",
                     "scenarios": "Scenario"
                 })

