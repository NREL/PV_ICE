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

# ## Simulation Descriptions:
# - r1: For all 10 scenarios, the recycle ('mod_EOL_collection_eff'), reuse (mod_reuse), and repair (mod_Repair) rates are modified with outputs from ABM. Percent of collected modules & materials that are recycled ('mod_EOL_collected_recycled' & 'mat_EOL_collected_recycled') is set to 100 (i.e. it is assumed all collected modules are sent to recycling). Weibull parameters and lifetime is set to Irena Regular Loss values for all ABM scenarios (not PV ICE bsaeline). For the better_lifetime scenario, an improved lifetime, t50, t90 values are set (based on what was used in ABM). All other values are set to PV ICE defaults. 
# - r2: For all scenarios, the same modifications as in r1 are made. Additionally, the recycling efficiency ('mat_EOL_Recycling_eff') are replaced with with FRELP recovery rates for all scenarios. 'mat_EOL_Recycled_into_HQ' is set to 100. 'mat_EOL_RecycledHQ_Reused4MFG' is also set to 100. 
# - r3A-r3D: For 3 select scenarios, the same parameters are modified as in r2. The Weibull shape parameters are changed based on Henry Hieslmair's parameters for the 4 reliability bins -- r3A is the A reliability bin (most reliable module), etc. 
# - r4: For all scenarios, the same parameter modifications are made as in r2. The new installs are decreased, accounting for the higher installed capacity in each scenario. Installed capacity for all scenario come out to the ABM baseline. But, less new installs need to happen each year for some scenarios as more modules are being reused, repaired, etc. 
# - r4A-r4D: For 3 select scenarios, the same parameters are modified as in r3A-r3D. The new installs needed are calculated and modified to account for the increased installed capacity as in r4. 
# 

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
#Henry Hieslmair gives four classes of reliability bins: A, B, C, D; with A being most reliable, D being least reliable
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
weibullInputParamsA = {'alpha': 2.810, 'beta': 100.238} #most reliable
weibullInputParamsB = {'alpha': 3.841, 'beta': 57.491}
weibullInputParamsC = {'alpha': 4.602, 'beta': 40.767}
weibullInputParamsD = {'alpha': 5.692, 'beta': 29.697} #least reliable


# In[6]:


#cleaning up ABM outputs
ABM_SCENARIOS = SCENARIOS[1:] 
#reading in cumulative mass file
ABM_outputs_mass_cum = pd.read_csv(r'..\baselines\ABM\ABM_outputs_mass_cumulative.csv')
file_scenario_names = ABM_outputs_mass_cum['Scenario'].unique().tolist()
ABM_outputs_mass_cum = ABM_outputs_mass_cum.replace(file_scenario_names, ABM_SCENARIOS)
ABM_outputs_mass_cum = ABM_outputs_mass_cum.rename(columns = {'Mass of PV materials repaired (million tonnes)': 'Repaired',
                                  'Mass of PV materials reused (million tonnes)':'Reused',
                                  'Mass of PV materials recycled (million tonnes)':'Recycled',
                                  'Mass of PV materials landfilled (million tonnes)':'Landfilled',
                                  'Mass of PV materials stored (million tonnes)':'Stored'})

#convert from million metric tonnes to metric tonnes for comparison
ABM_outputs_mass_cum['Repaired'] = ABM_outputs_mass_cum['Repaired'] * 1000000
ABM_outputs_mass_cum['Reused'] = ABM_outputs_mass_cum['Reused'] * 1000000
ABM_outputs_mass_cum['Recycled'] = ABM_outputs_mass_cum['Recycled'] * 1000000
ABM_outputs_mass_cum['Landfilled'] = ABM_outputs_mass_cum['Landfilled'] * 1000000
ABM_outputs_mass_cum['Stored'] = ABM_outputs_mass_cum['Stored'] * 1000000

#change ABM_outputs_mass_cum cumulatives to yearly
ABM_outputs_mass_yearly = ABM_outputs_mass_cum.copy()

mass_diff = ABM_outputs_mass_cum.groupby('Scenario').diff().fillna(0).astype(int)
colnames = ['Repaired', 'Reused','Recycled','Landfilled','Stored']
for col in colnames:
    ABM_outputs_mass_yearly[col] = mass_diff[col]

#create a waste column
ABM_outputs_mass_cum['Waste'] = ABM_outputs_mass_cum['Landfilled'] + ABM_outputs_mass_cum['Stored']
ABM_outputs_mass_yearly['Waste'] = ABM_outputs_mass_yearly['Landfilled'] + ABM_outputs_mass_yearly['Stored']


#change ABM_outputs_mass_yearly to mass fractions and call new df ABM_outputs_mass_fraction_yearly
ABM_outputs_mass_fraction_yearly = ABM_outputs_mass_yearly.copy()
ABM_outputs_mass_fraction_yearly['Total'] = ABM_outputs_mass_fraction_yearly['Repaired'] + ABM_outputs_mass_fraction_yearly['Reused'] + ABM_outputs_mass_fraction_yearly['Recycled'] + ABM_outputs_mass_fraction_yearly['Landfilled'] + ABM_outputs_mass_fraction_yearly['Stored']
ABM_outputs_mass_fraction_yearly['mass_fraction_PV_materials_repaired_milliontonnes'] = ABM_outputs_mass_fraction_yearly['Repaired']/ABM_outputs_mass_fraction_yearly['Total']
ABM_outputs_mass_fraction_yearly['mass_fraction_PV_materials_reused_milliontonnes'] = ABM_outputs_mass_fraction_yearly['Reused']/ABM_outputs_mass_fraction_yearly['Total']
ABM_outputs_mass_fraction_yearly['mass_fraction_PV_materials_recycled_milliontonnes'] = ABM_outputs_mass_fraction_yearly['Recycled']/ABM_outputs_mass_fraction_yearly['Total']
ABM_outputs_mass_fraction_yearly['mass_fraction_PV_materials_landfilled_milliontonnes'] = ABM_outputs_mass_fraction_yearly['Landfilled']/ABM_outputs_mass_fraction_yearly['Total']
ABM_outputs_mass_fraction_yearly['mass_fraction_PV_materials_stored_milliontonnes'] = ABM_outputs_mass_fraction_yearly['Stored']/ABM_outputs_mass_fraction_yearly['Total']
#replace NaNs with 0s
ABM_outputs_mass_fraction_yearly = ABM_outputs_mass_fraction_yearly.replace(np.nan, 0)

#drop mass cols
ABM_outputs_mass_fraction_yearly = ABM_outputs_mass_fraction_yearly.drop(columns = ['Repaired', 'Reused','Recycled','Landfilled','Stored','Total','Waste'])

#rename ABM_outputs_mass_fraction_yearly to ABM_outputs to use for simulations
ABM_outputs = ABM_outputs_mass_fraction_yearly.copy()


# ## Modify parameters: Simulation 1 (r1), same installs for all scenarios: what is the effect of different reuse, recycle, and repair rates?

# In[7]:


#modify values of each scenario 2-10 based on ABM outputs
#first, set 'mod_EOL_collected_recycled' to 100% in scenarios 2-10 for years 2022 on (assume all collected modules are recycled)
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


# In[8]:


#next, modify 3 additional inputs for each scenario 2-10, with values depending on the scenario, coming from ABM outputs
MODIFIED_MODULE_BASELINES = ['mod_Repair','mod_Reuse','mod_EOL_collection_eff']
len(r1.scenario['landfill_ban'].data['mod_Reuse']) #all inputs have 56 rows
#keep first 27 rows corresponding to 1995-2021 values


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


#also change mod_lifetime = 40 for all years to agree with Irena RL
for myscenario in ABM_SCENARIOS:
    r1.scenario[myscenario].data['mod_lifetime'] = 40


# In[11]:


#use electrification futures base new installs
electric_module_baseline = pd.read_csv(r'..\baselines\ElectrificationFutures_2021\baseline_modules_US_NREL_Electrification_Futures_2021_basecase.csv')
electric_new_installs = electric_module_baseline['new_Installed_Capacity_[MW]'][1:].reset_index(drop=True).astype(float)
for myscenario in SCENARIOS:
    r1.scenario[myscenario].data['new_Installed_Capacity_[MW]'] = electric_new_installs


# ### Modify better_lifetime scenario reliability inputs: mod_lifetime, mod_reliability_t50, & mod_reliability_t90

# In[12]:


def lifetime_line(year):
    """"
    This function takes in a year and outputs the module lifetime based on scenario e) in ABM.
    Inputs
    year = desired year
    """
    m = (60-15.9)/(2050-2000)
    y = m*(year-2000) + 15.9
    return(y)


# In[13]:


#create list of mod_lifetime values based on linear regression
years = list(range(2022,2051)) #ONLY WANT to modify 2022 ONWARD
mod_lifetimes_list = []
for myyear in years:
    mod_lifetimes_list += [lifetime_line(myyear)]


# In[14]:


mod_lifetimes_df = pd.DataFrame()


# In[15]:


mod_lifetimes_df['year'] = years
mod_lifetimes_df['mod_lifetime'] = mod_lifetimes_list


# In[16]:


#changing mod_lifetime in scenario e) better_lifetime
new_mod_lifetime = list(r1.scenario[myscenario].data['mod_lifetime'][0:27].values) + mod_lifetimes_list
r1.scenario['better_lifetime'].data['mod_lifetime'] = new_mod_lifetime


# In[17]:


#create linear regression for mod_reliability_t50 & mod_reliability_t90 vs. mod_lifetime 
#to estimate t50 and t90 values to input for improved lifetime scenario
reliability_baselines = pd.DataFrame()
reliability_baselines['mod_lifetime'] = r1.scenario['standard_PVICE'].data['mod_lifetime']
reliability_baselines['mod_reliability_t50'] = r1.scenario['standard_PVICE'].data['mod_reliability_t50']
reliability_baselines['mod_reliability_t90'] = r1.scenario['standard_PVICE'].data['mod_reliability_t90']


# In[18]:


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


# In[19]:


#changing mod_reliability_t50 & mod_reliability_t90 in scenario e) better_lifetime
new_mod_t50 = list(r1.scenario[myscenario].data['mod_reliability_t50'][0:27].values) + better_lifetime_t50_list
r1.scenario['better_lifetime'].data['mod_reliability_t50'] = new_mod_t50

new_mod_t90 = list(r1.scenario[myscenario].data['mod_reliability_t90'][0:27].values) + better_lifetime_t90_list
r1.scenario['better_lifetime'].data['mod_reliability_t90'] = new_mod_t90


# ## Modify parameters: Simulation 2 (r2), same installs for all scenarios: what is effect of different reuse, recycle, and repair rates when recycling efficiency is improved?

# In[20]:


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
    
#also change mod_lifetime = 40 for all years to agree with Irena RL
for myscenario in ABM_SCENARIOS:
    r2.scenario[myscenario].data['mod_lifetime'] = 40
    
r2.scenario['better_lifetime'].data['mod_lifetime'] = new_mod_lifetime
r2.scenario['better_lifetime'].data['mod_reliability_t50'] = new_mod_t50
r2.scenario['better_lifetime'].data['mod_reliability_t90'] = new_mod_t90


# In[21]:


#FRELP recovery rates and qualities
frelp_results = pd.DataFrame()
frelp_results['mat'] = ['silver','copper','aluminium_frames','silicon','glass']
frelp_results['recovery_rate'] = [94,97,99.4,97,98]
frelp_results['mat_recycled_into_HQ'] = [100,100,100,100,100] #########MODIFY THIS BASED ON RESEARCH VALUES!


# In[22]:


frelp_results


# In[23]:


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


# In[24]:


#use electrification futures base new installs
for myscenario in SCENARIOS:
    r2.scenario[myscenario].data['new_Installed_Capacity_[MW]'] = electric_new_installs


# ## Modify parameters: Simulation 3 (r3), same installs for some scenarios: what is the effect of module reliability when recycle rates, reuse rates, repair rates, and recycling efficiencies changed for select scenarios with different repair bins?

# In[25]:


#Figure out which scenarios to include
#ABM_outputs.groupby('Scenario').sum()['mass_fraction_PV_materials_repaired_milliontonnes'].sort_values()
#calculate scenarios with highest repair rates: better lifetime, better learning, julien’s baseline, landfill ban
#only do better learning, julien’s baseline, landfill ban as better lifetime already had different reliability


# In[26]:


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
            
#also change mod_lifetime = 40 for all years to agree with Irena RL
for myr3simulation in r3_simulations:
    for myscenario in REPAIR_SCENARIOS:
        myr3simulation.scenario[myscenario].data['mod_lifetime'] = 40
    


# In[27]:


#modify shape parameters (overrides t50 and t90 baselines) -- values from Henry Hieslmair
weibullInputParamsA = {'alpha': 2.810, 'beta': 100.238} 
weibullInputParamsB = {'alpha': 3.841, 'beta': 57.491}
weibullInputParamsC = {'alpha': 4.602, 'beta': 40.767}
weibullInputParamsD = {'alpha': 5.692, 'beta': 29.697}


# In[28]:


#use electrification futures base new installs
for myr3simulation in r3_simulations:
    for myscenario in REPAIR_SCENARIOS:
        myr3simulation.scenario[myscenario].data['new_Installed_Capacity_[MW]'] = electric_new_installs


# ## Modify parameters: Simulation 4 (r4), change new installs due to increased installed capacity for all scenarios: what is effect of accounting for fewer installs for all scenarios on virgin material demand vs. r2? what is the effect on cumulative new installs and yearly virgin material demand for different repair bins?

# In[29]:


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

#also change mod_lifetime = 40 for all years to agree with Irena RL
for myscenario in ABM_SCENARIOS:
    r4.scenario[myscenario].data['mod_lifetime'] = 40  

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


# In[30]:


#use electrification futures base new installs
for myscenario in SCENARIOS:
    r4.scenario[myscenario].data['new_Installed_Capacity_[MW]'] = electric_new_installs


# In[31]:


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
            
#also change mod_lifetime = 40 for all years to agree with Irena RL
for myr4simulation in r4_simulations:
    for myscenario in REPAIR_SCENARIOS:
        myr4simulation.scenario[myscenario].data['mod_lifetime'] = 40


# In[32]:


#use electrification futures base new installs
for myr4simulation in r4_simulations:
    for myscenario in REPAIR_SCENARIOS:
        myr4simulation.scenario[myscenario].data['new_Installed_Capacity_[MW]'] = electric_new_installs


# ## Run Mass Flow Calculations

# In[33]:


r1.calculateMassFlow(weibullInputParams= weibull_IrenaRL)
r2.calculateMassFlow(weibullInputParams= weibull_IrenaRL)
r3A.calculateMassFlow(weibullInputParams= weibullInputParamsA)
r3B.calculateMassFlow(weibullInputParams= weibullInputParamsB)
r3C.calculateMassFlow(weibullInputParams= weibullInputParamsC)
r3D.calculateMassFlow(weibullInputParams= weibullInputParamsD)
#r4.calculateMassFlow(weibullInputParams= weibull_IrenaRL)
r4A.calculateMassFlow(weibullInputParams= weibullInputParamsA)
r4B.calculateMassFlow(weibullInputParams= weibullInputParamsB)
r4C.calculateMassFlow(weibullInputParams= weibullInputParamsC)
r4D.calculateMassFlow(weibullInputParams= weibullInputParamsD)


# In[34]:


#Under_Installment = []
#scenarios = ['standard_PVICE','landfill_ban','high_mat_recovery_cheap_recycling','cheap_recycling','high_landfill_costs','better_lifetime','better_learning','reuse_warranties','seeding_reuse','juliens_baseline']
#for i in range (0, len(r4.scenario['juliens_baseline'].data)): #runs for each year
#    for myscenario in scenarios[1:9]:
#        Under_Installment = ( (r4.scenario['juliens_baseline'].data['Installed_Capacity_[W]'][i] - 
#                         r4.scenario[myscenario].data['Installed_Capacity_[W]'][i])/1000000 )  # MWATTS
#        r4.scenario[myscenario].data['new_Installed_Capacity_[MW]'][i] += Under_Installment
#    r4.calculateMassFlow(weibullInputParams= weibull_IrenaRL)


# # Silvana please look here:

# In[35]:


#####SILVANA PLEASE DOUBLE CHECK THIS##################################################
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

# In[36]:


USyearly=pd.DataFrame()


# In[37]:


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


# In[38]:


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


# In[39]:


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


# In[40]:


keyword='mat_EoL_Recycled_HQ_into_MFG'
r1_r2 = [r1,r2]

for mysimulation in r1_r2:
    for jj in range(0, len(mysimulation.scenario)): #goes from 0 to 9
        case = list(mysimulation.scenario.keys())[jj]
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["EOL_Recycled_HQ_into_MFG_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
        filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_HQ_into_MFG') and col.endswith(mysimulation.name+'_'+case)) ]
        USyearly['EOL_Recycled_HQ_into_MFG_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[41]:


keyword='mat_EOL_Recycled_HQ_into_OU'

for mysimulation in r1_r2:
    for jj in range(0, len(mysimulation.scenario)): #goes from 0 to 9
        case = list(mysimulation.scenario.keys())[jj]
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["EOL_Recycled_HQ_into_OU_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
        filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_HQ_into_OU') and col.endswith(mysimulation.name+'_'+case)) ]
        USyearly['EOL_Recycled_HQ_into_OU_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[42]:


keyword='mat_EOL_Recycled_2_OQ'

for mysimulation in r1_r2:
    for jj in range(0, len(mysimulation.scenario)): #goes from 0 to 9
        case = list(mysimulation.scenario.keys())[jj]
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["EOL_Recycled_2_OQ_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
        filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_2_OQ') and col.endswith(mysimulation.name+'_'+case)) ]
        USyearly['EOL_Recycled_2_OQ_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[43]:


USyearly = USyearly/1000000  #Convert to metric tonnes
#907185 -- this is for US tons


# In[44]:


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


# In[45]:


UScum = USyearly.copy()
UScum = UScum.cumsum()


# In[46]:


keyword='Installed_Capacity_[W]'

for mysimulation in SIMULATIONS:
    for i in range(0, len(mysimulation.scenario)):
        case = list(mysimulation.scenario.keys())[i]
        foo = mysimulation.scenario[case].data[keyword]
        foo = foo.to_frame(name=keyword)
        UScum["Capacity_"+mysimulation.name+'_'+case] = foo[keyword].values/1000000 #change to MW


# In[47]:


USyearly.index = r1.scenario['standard_PVICE'].data['year']
UScum.index = r1.scenario['standard_PVICE'].data['year']


# In[48]:


USyearly.to_csv('ABM_Yearly_Results.csv')
UScum.to_csv('ABM_Cumulative_Results.csv')


# ### Plotting with USyearly and UScum data frames: r1

# In[49]:


filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation1'))]
df = UScum[filter_col]
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
fig1.update_layout(title_text='Simulation 1: Cumulative Virgin Material Demand', title_x=0.2)
fig1.show()


# In[50]:


# average cumulative virgin material demand for later simulation 2 comparison
filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation1'))]
df = UScum[filter_col]
pretty_scenarios = ['PV ICE Baseline','Landfill Ban','High material recovery and Lower recycling costs','Lower recycling costs','Higher landfill costs','Improved lifetime','Improved learning effect','Reuse warranties','Seeding reuse','ABM Baseline']
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]

df_avg_r1_virgin_material_demand_cum = df.groupby(['year']).mean()
df_avg_r1_virgin_material_demand_cum['year'] = list(range(2020,2051))
df_avg_r1_virgin_material_demand_cum['variable'] = 'Average Cumulative Virgin Material Demand from Simulation 1'


# In[51]:


#cumulative at 2050 results for Virgin Material Demand
filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation1'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin([2050])]
df = df.sort_values('value')
df = df.rename(columns={'variable':'Scenario','value':'Cumulative Virgin Material Demand at 2050 [metric tonnes]'})
df = df.round(0)
df.to_csv('r1 cumulative at 2050 virgin material demand.csv')

df_avg = pd.DataFrame()
df_avg['Cumulative Virgin Material Demand at 2050 [metric tonnes]'] = [df['Cumulative Virgin Material Demand at 2050 [metric tonnes]'].mean()]
df_avg['high'] = [df['Cumulative Virgin Material Demand at 2050 [metric tonnes]'].max()]
df_avg['low'] = [df['Cumulative Virgin Material Demand at 2050 [metric tonnes]'].min()]
df_avg['year'] = [2050]

#calculate max and min relative to average
bigger_range = max(df_avg['high'][0] - df_avg['Cumulative Virgin Material Demand at 2050 [metric tonnes]'][0],abs(df_avg['low'][0] - df_avg['Cumulative Virgin Material Demand at 2050 [metric tonnes]'][0]))
percent_diff = (bigger_range/df_avg['Cumulative Virgin Material Demand at 2050 [metric tonnes]'][0]*100).round(1)

fig1 = px.bar(df_avg, x='year', y='Cumulative Virgin Material Demand at 2050 [metric tonnes]', labels={
    'Cumulative Virgin Material Demand at 2050 [metric tonnes]':'Material Demand [metric tonnes]',
                     "year": ""}, width=500, height=500)
fig1.update_layout(title_text='Simulation 1: Cumulative Virgin Material Demand at 2050', title_x=0.5)
fig1.add_annotation(dict(font=dict(color='black',size=20),
                                        x=0.4,
                                        y=1.05,
                                        showarrow=False,
                                        text='+/- ' + str(percent_diff) + '%',
                                        textangle=0,
                                        xanchor='left',
                                        xref="paper",
                                        yref="paper"))
for data in fig1.data:
    data["width"] = 0.15 #Change this value for bar widths
fig1.update_xaxes(type='category')
fig1.show()


# In[214]:


#graph recycled material stacked bar chart cumulative at 2050
filter_col = [col for col in UScum if (col.startswith(('EOL_Recycled_HQ_into_MFG_Module_ABM_Simulation1','EOL_Recycled_HQ_into_OU_Module_ABM_Simulation1','EOL_Recycled_2_OQ_Module_ABM_Simulation1')))]
df = UScum[filter_col]
df['year'] = list(range(1995,2051))
df = df[df.year.isin([2050])]
df = df.melt(id_vars = 'year')
df = df.drop(columns = ['year'])
df['Scenario'] = pretty_scenarios * 3
df['Recycled Material Type'] = ['HQ Closed Loop'] * 10 + ['HQ Open Loop'] * 10 + ['OQ Open Loop'] * 10
fig1 = px.bar(df, x="Scenario", y="value", color="Recycled Material Type", title="Simulation 1: Cumulative Recycled Material at 2050",
             labels={'value':'Recycled Material [metric tonnes]'})
fig1.update_layout(title_x=0.2)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.78
))
fig1.show()


# In[53]:


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


# In[54]:


filter_col = [col for col in UScum if (col.startswith('Waste_Module_ABM_Simulation1'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'variable', labels={
                     "year": "Year",
                     "value": "Waste [metric tonnes]",
                    "variable" :"Scenario"
                 })
fig1.update_layout(title_text='Simulation 1: Cumulative Waste', title_x=0.25)
fig1.show()


# In[55]:


# comparing to Julien's: making a cumulative at 2050 df for r1
ABM_outputs_mass_cum_2050 = ABM_outputs_mass_cum[ABM_outputs_mass_cum.Year.isin([2050])]
ABM_outputs_mass_cum_2050 = ABM_outputs_mass_cum_2050.replace(ABM_SCENARIOS, pretty_scenarios[1:])
ABM_outputs_mass_cum_2050 = ABM_outputs_mass_cum_2050.rename(columns = {'Waste':'Cumulative Waste at 2050 ABM [metric tonnes]'})

filter_col = [col for col in UScum if (col.startswith('Waste_Module_ABM_Simulation1'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin([2050])]
df = df.rename(columns = {'variable':'Scenario',
                   'value':'Cumulative Waste at 2050 PV ICE [metric tonnes]'})
df['Cumulative Waste at 2050 ABM [metric tonnes]'] = [0] + list(ABM_outputs_mass_cum_2050['Cumulative Waste at 2050 ABM [metric tonnes]'].values)
df = df.drop(columns = ['year'])
df['Cumulative Waste at 2050 PV ICE [million metric tonnes]'] = df['Cumulative Waste at 2050 PV ICE [metric tonnes]'].round(0)/1000000
df['Cumulative Waste at 2050 ABM [million metric tonnes]'] = df['Cumulative Waste at 2050 ABM [metric tonnes]']/1000000

df.to_csv("r1_cum_waste_2050_ABM_comparison.csv")


# In[56]:


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


# In[57]:


df_2050 = df[df.year.isin([2050])]
df_avg = pd.DataFrame()
df_avg['Installed Capacity at 2050 [MW]'] = [df_2050['value'].mean()]
df_avg['high'] = [df_2050['value'].max()]
df_avg['low'] = [df_2050['value'].min()]
df_avg['year'] = [2050]
print( "The installed capacity at 2050 for all scenarios is approx. " + str(df_avg['Installed Capacity at 2050 [MW]'][0]) + ' MW.')

#calculate max and min relative to average
bigger_range = max(df_avg['high'][0] - df_avg['Installed Capacity at 2050 [MW]'][0],abs(df_avg['low'][0] - df_avg['Installed Capacity at 2050 [MW]'][0]))
percent_diff = (bigger_range/df_avg['Installed Capacity at 2050 [MW]'][0]*100).round(1)
print("The percent difference that this is off by depending on the scenario is +/- " + str(percent_diff) + ' %.')


# ### Plotting with USyearly and UScum data frames: r2

# In[98]:


#simulation 2 lines
filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation2'))]
df2 = UScum[filter_col]
df2 = df2.set_axis(pretty_scenarios, axis=1)
df2['year'] = list(range(1995,2051))
df2 = df2.melt(id_vars = 'year')
df2 = df2[df2.year.isin(list(range(2020,2051)))]

#simulation 1 average
s1_avg = list(df_avg_r1_virgin_material_demand_cum["value"][:].values)

fig = go.Figure()

for myscenario in pretty_scenarios:
    y_values = list(df2[df2.variable.isin([myscenario])].loc[:,'value'].values)
    fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=y_values,
                    mode='lines',
                    name='S2 '+ myscenario))
    
fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=s1_avg,
                    mode='markers',
                    name='S1 Average',
                        marker_color = 'black'))


fig.update_layout(title_text='Cumulative Virgin Material Demand: Simulations 1 and 2', title_x=0.1, 
                 xaxis_title="Time",
    yaxis_title="Material Demand [metric tonnes]",
    legend_title="Scenario")
fig.show()


# In[58]:


filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation2'))]
df = UScum[filter_col]
s2_scenarios = ['S2 PV ICE Baseline','S2 Landfill Ban','S2 High material recovery and Lower recycling costs','S2 Lower recycling costs','S2 Higher landfill costs','S2 Improved lifetime','S2 Improved learning effect','S2 Reuse warranties','S2 Seeding reuse','S2 ABM Baseline']
df = df.set_axis(s2_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df[df.year.isin(list(range(2020,2051)))]

##include average line from simulation 1 yearly virgin material demand
df["S1 Average"] = list(df_avg_r1_virgin_material_demand_cum["value"][:].values)
cols = s2_scenarios + ["S1 Average"]

fig1 = px.line(df, x='year', y = cols, labels = {
            'variable':'Scenario',
            'value':'Virgin Material Demand [metric tonnes]',
            'year':'Year'},
              color_discrete_map={
                "S1 Average": "black"},
              line_dash_map={
                  "S1 Average": "dash" #get this dashed line to work
              })
fig1.update_layout(title_text='Cumulative Virgin Material Demand: Simulations 1 and 2', title_x=0.1)
fig1.show()


# In[59]:


#cumulative at 2050 results for Virgin Material Demand
filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation2'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin([2050])]
df.sort_values('value')


# In[213]:


#graph recycled material stacked bar chart cumulative at 2050
filter_col = [col for col in UScum if (col.startswith(('EOL_Recycled_HQ_into_MFG_Module_ABM_Simulation2','EOL_Recycled_HQ_into_OU_Module_ABM_Simulation2','EOL_Recycled_2_OQ_Module_ABM_Simulation2')))]
df = UScum[filter_col]
df['year'] = list(range(1995,2051))
df = df[df.year.isin([2050])]
df = df.melt(id_vars = 'year')
df = df.drop(columns = ['year'])
df['Scenario'] = pretty_scenarios * 3
df['Recycled Material Type'] = ['HQ Closed Loop'] * 10 + ['HQ Open Loop'] * 10 + ['OQ Open Loop'] * 10
fig1 = px.bar(df, x="Scenario", y="value", color="Recycled Material Type", title="Simulation 2: Cumulative Recycled Material at 2050",
             labels={'value':'Recycled Material [metric tonnes]'})
fig1.update_layout(title_x=0.2)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.78
))
fig1.show()


# In[212]:


#add above graph to recycled material bar chart from simulation 1
#simulation 1 trace
filter_col = [col for col in UScum if (col.startswith(('EOL_Recycled_HQ_into_MFG_Module_ABM_Simulation1','EOL_Recycled_HQ_into_OU_Module_ABM_Simulation1','EOL_Recycled_2_OQ_Module_ABM_Simulation1')))]
df = UScum[filter_col]
df['year'] = list(range(1995,2051))
df = df[df.year.isin([2050])]
df = df.melt(id_vars = 'year')
df = df.drop(columns = ['year'])
df['Scenario'] = pretty_scenarios * 3
df['Recycled_Material_Type'] = ['HQ Closed Loop'] * 10 + ['HQ Open Loop'] * 10 + ['OQ Open Loop'] * 10

hq_closed = list(df[df.Recycled_Material_Type.isin(["HQ Closed Loop"])].loc[:,'value'].values)
hq_open = list(df[df.Recycled_Material_Type.isin(["HQ Open Loop"])].loc[:,'value'].values)
oq_open = list(df[df.Recycled_Material_Type.isin(["OQ Open Loop"])].loc[:,'value'].values)

#simulation 2 trace
filter_col = [col for col in UScum if (col.startswith(('EOL_Recycled_HQ_into_MFG_Module_ABM_Simulation2','EOL_Recycled_HQ_into_OU_Module_ABM_Simulation2','EOL_Recycled_2_OQ_Module_ABM_Simulation2')))]
df2 = UScum[filter_col]
df2['year'] = list(range(1995,2051))
df2 = df2[df2.year.isin([2050])]
df2 = df2.melt(id_vars = 'year')
df2 = df2.drop(columns = ['year'])
df2['Scenario'] = pretty_scenarios * 3
df2['Recycled_Material_Type'] = ['HQ Closed Loop'] * 10 + ['HQ Open Loop'] * 10 + ['OQ Open Loop'] * 10

hq_closed_sim2 = list(df2[df2.Recycled_Material_Type.isin(["HQ Closed Loop"])].loc[:,'value'].values)


fig = go.Figure(data=[
    go.Bar(name='HQ Closed Loop S1', x=pretty_scenarios, y=hq_closed), 
    go.Bar(name='HQ Open Loop S1', x=pretty_scenarios, y=hq_open),
    go.Bar(name='OQ Open Loop S1', x=pretty_scenarios, y=oq_open)
])

fig.add_trace(go.Scatter(x=pretty_scenarios, y=hq_closed_sim2,
                    mode='markers',
                    name='HQ Closed Loop S2'))


# Change the bar mode
fig.update_layout(barmode='stack', title_text = 'Cumulative Recycled Material at 2050: Simulations 1 and 2',
                 title_x = 0.4, xaxis_title="Scenario",
    yaxis_title="Recycled Material [metric tonnes]",
    legend_title="Recycled Material Type")
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.78
))
fig.show()


# In[204]:


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
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.show()


# In[206]:


#use max and min lines from simulation 1 for simulation 2 yearly waste

#simulation 2 lines
filter_col = [col for col in USyearly if (col.startswith('Waste_Module_ABM_Simulation2'))]
df2 = USyearly[filter_col]
df2 = df2.set_axis(pretty_scenarios, axis=1)
df2['year'] = list(range(1995,2051))
df2 = df2.melt(id_vars = 'year')
df2 = df2[df2.year.isin(list(range(2020,2051)))]

#simulation 1 lines
filter_col = [col for col in USyearly if (col.startswith('Waste_Module_ABM_Simulation1'))]
df1 = USyearly[filter_col]
df1 = df1.set_axis(pretty_scenarios, axis=1)
df1['year'] = list(range(1995,2051))
df1 = df1.melt(id_vars = 'year')
df1 = df1[df1.year.isin(list(range(2020,2051)))]
s1_landfill_ban = list(df1[df1.variable.isin(['Landfill Ban'])].loc[:,'value'].values) #max value from sim 1
s1_reuse_warranties = list(df1[df1.variable.isin(['Reuse warranties'])].loc[:,'value'].values) #min value from sim 1
s1_abm_baseline = list(df1[df1.variable.isin(['ABM Baseline'])].loc[:,'value'].values) #abm baseline from sim 1

fig = go.Figure()

for myscenario in pretty_scenarios:
    y_values = list(df2[df2.variable.isin([myscenario])].loc[:,'value'].values)
    fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=y_values,
                    mode='lines',
                    name='S2 '+ myscenario))
    
fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=s1_landfill_ban,
                    mode='markers',
                    name='S1 Landfill Ban'))
fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=s1_reuse_warranties,
                    mode='markers',
                    name='S1 Reuse Warranties'))
fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=s1_abm_baseline,
                    mode='markers',
                    name='S1 ABM Baseline'))


fig.update_layout(title_text='Yearly Waste: Simulations 1 and 2', title_x=0.2, 
                 xaxis_title="Time",
    yaxis_title="Waste [metric tonnes]",
    legend_title="Scenario")
fig.show()


# In[65]:


#cumulative at 2050 results for Waste
filter_col = [col for col in UScum if (col.startswith('Waste_Module_ABM_Simulation2'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin([2050])]
df.sort_values('value')


# In[203]:


#cumulative waste at 2050 bar chart sim 1 vs. sim 2
x_labels = [pretty_scenarios[1]] + ['High material recovery /nand lower recycling costs'] + pretty_scenarios[3:5]

#simulation 1 trace
filter_col = [col for col in UScum if (col.startswith('Waste_Module_ABM_Simulation1'))]
df = UScum[filter_col]
df['year'] = list(range(1995,2051))
df = df[df.year.isin([2050])]
df = df.melt(id_vars = 'year')
df = df.drop(columns = ['year'])
df['Scenario'] = pretty_scenarios
df = df[df.Scenario.isin(pretty_scenarios[1:5])]

s1_waste = list(df.loc[:,'value'].values)
                                       
#simulation 2 trace
filter_col = [col for col in UScum if (col.startswith('Waste_Module_ABM_Simulation2'))]
df2 = UScum[filter_col]
df2['year'] = list(range(1995,2051))
df2 = df2[df2.year.isin([2050])]
df2 = df2.melt(id_vars = 'year')
df2 = df2.drop(columns = ['year'])
df2['Scenario'] = pretty_scenarios
df2 = df2[df2.Scenario.isin(pretty_scenarios[1:5])]

s2_waste = list(df2.loc[:,'value'].values)


fig = go.Figure(data=[
    go.Bar(name='S1', x=x_labels, y=s1_waste, width = [0.5,0.5,0.5,0.5])
])

fig.add_trace(go.Scatter(x=x_labels, y=s2_waste,
                    mode='markers',
                    name='S2', 
                    marker=dict(size=[30, 30, 30, 30])))


# Change the bar mode
fig.update_layout(title_text = 'Cumulative Waste at 2050: Simulations 1 and 2',
                 title_x = 0.5, xaxis_title="Scenario",
    yaxis_title="Waste [metric tonnes]",
    legend_title="Simulation", width = 1000, height = 600)
fig.update_xaxes(tickangle=20)
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig.show()


# ### Plotting with USyearly and UScum data frames: r3

# In[190]:


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
df['reliability_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'reliability_bin', facet_col = 'scenario', labels={
                     "year": "Year",
                     "value": "Cumulative Waste [metric tonnes]",
                    "reliability_bin":"Reliability Bin"
                })
fig1.update_layout(title_text='Simulation 3: Cumulative Waste for Different Reliability Bins', title_x=0.5)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
fig1.update_xaxes(tickangle=-45)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.show()


# In[191]:


filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation3'))]
df = UScum[filter_col]
#pretty_repair_scenarios = ['Improved Learning Effect', 'ABM Baseline', 'Landfill Ban']
#df = df.set_axis(pretty_repair_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
scenario_splices = []
for i in range(0,len(df['variable'])):
    scenario_splices += [df.loc[i,'variable'][36:]]
quality_splices = []
for i in range(0,len(df['variable'])):
    quality_splices += [df.loc[i,'variable'][34]]
df['scenario'] = scenario_splices
df['reliability_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'reliability_bin', facet_col = 'scenario', labels={
                     "year": "Year",
                     "value": "Cumulative Virgin Material Demand [metric tonnes]",
                    "reliability_bin":"Reliability Bin"
                })
fig1.update_layout(title_text='Simulation 3: Cumulative Virgin Material Demand for Different Reliability Bins', title_x=0.5)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
fig1.update_xaxes(tickangle=-45)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.show()


# In[124]:


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
df['reliability_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
df


# In[192]:


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
df['reliability_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
df = df[df.scenario.isin(['juliens_baseline'])]
fig1 = px.line(df, x='year', y='value', color = 'reliability_bin', labels={
                     "year": "Year",
                     "value": "Installed Capacity [MW]",
                    "reliability_bin":"Reliability Bin"
                })
fig1.update_layout(title_text='Simulation 3: ABM Baseline Installed Capacity for Different Reliability Bins', title_x=0.45)
#fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
#fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
#fig1.update_xaxes(tickangle=-45)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.show()


# ### Plotting with USyearly and UScum data frames: r4

# # Silvana please look here:

# In[245]:


#############################SILVANA PLEASE LOOK HERE

filter_col = [col for col in UScum if (col.startswith(('Capacity_ABM_Simulation4A','Capacity_ABM_Simulation4B','Capacity_ABM_Simulation4C','Capacity_ABM_Simulation4D')))]

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
df['reliability_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
df = df[df.scenario.isin(['juliens_baseline'])]
fig1 = px.line(df, x='year', y='value', color = 'reliability_bin', labels={
                     "year": "Year",
                     "value": "Installed Capacity [MW]",
                    "reliability_bin":"Reliability Bin"
                })
fig1.update_layout(title_text='Simulation 4: ABM Baseline Installed Capacity for Different Reliability Bins', title_x=0.45)
#fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
#fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
#fig1.update_xaxes(tickangle=-45)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.show()


# In[244]:


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
df['reliability_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'reliability_bin', facet_col = 'scenario', labels={
                     "year": "Year",
                     "value": "Cumulative Waste [metric tonnes]",
                    "reliability_bin":"Reliability Bin"
                })
fig1.update_layout(title_text='Simulation 4: Cumulative New Installs for Different Reliability Bins with Fewer New Installs', title_x=0.5)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
fig1.update_xaxes(tickangle=-45)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.show()


# In[196]:


filter_col = [col for col in UScum if (col.startswith(('VirginStock_Module_ABM_Simulation4A','VirginStock_Module_ABM_Simulation4B','VirginStock_Module_ABM_Simulation4C','VirginStock_Module_ABM_Simulation4D')))]
df = UScum[filter_col]
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
scenario_splices = []
for i in range(0,len(df['variable'])):
    scenario_splices += [df.loc[i,'variable'][36:]]
quality_splices = []
for i in range(0,len(df['variable'])):
    quality_splices += [df.loc[i,'variable'][34]]
df['scenario'] = scenario_splices
df['reliability_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]
fig1 = px.line(df, x='year', y='value', color = 'reliability_bin', facet_col = 'scenario', labels={
                     "year": "Year",
                     "value": "Material Demand [metric tonnes]",
                    "reliability_bin":"Reliability Bin"
                })
fig1.update_layout(title_text='Simulation 4: Cumulative Virgin Material Demand for Different Reliability Bins with Fewer New Installs', title_x=0.5)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved Learning Effect")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM Baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill Ban")))
fig1.update_xaxes(tickangle=-45)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.show()


# ## Graphing ABM outputs

# In[195]:


df = ABM_outputs.rename(columns={'mass_fraction_PV_materials_repaired_milliontonnes':'Repaired',
                                'mass_fraction_PV_materials_reused_milliontonnes':'Reused',
                                'mass_fraction_PV_materials_recycled_milliontonnes':'Recycled',
                                'mass_fraction_PV_materials_landfilled_milliontonnes':'Landfilled',
                                'mass_fraction_PV_materials_stored_milliontonnes':'Stored'})
df['Scenario'] = [pretty_scenarios[1]] * 31 + [pretty_scenarios[2]] * 31 + [pretty_scenarios[3]] * 31 + [pretty_scenarios[4]] * 31 + [pretty_scenarios[5]] * 31 + [pretty_scenarios[6]] * 31 + [pretty_scenarios[7]] * 31 + [pretty_scenarios[8]] * 31 + [pretty_scenarios[9]] * 31
df = df.melt(id_vars = ('Year','Scenario'))
fig1 = px.bar(df, x="Year", y="value", color="variable", title="ABM Outputs: Yearly Mass Fraction of Material in EOL Pathways",
             labels={'value':'Mass Fraction',
                    'variable':'EOL Pathway'}, 
              facet_col = 'Scenario',
             facet_col_wrap=3, width = 1200, height = 1000)
fig1.update_layout(title_x=0.5)
fig1.update_xaxes(tickangle=-45)
fig1.show()


# In[76]:


file_scenario_names = ABM_outputs_mass_yearly['Scenario'].unique().tolist()
ABM_outputs_mass_yearly = ABM_outputs_mass_yearly.replace(file_scenario_names, pretty_scenarios[1:])
fig1 = px.line(ABM_outputs_mass_yearly, x='Year', y='Waste', color = 'Scenario',
              labels = {'Waste':'Waste [metric tonnes]'})
fig1.update_layout(title_text='ABM Outputs: Yearly Waste', title_x=0.2)
fig1.show()


# In[77]:


file_scenario_names = ABM_outputs_mass_cum['Scenario'].unique().tolist()
ABM_outputs_mass_cum = ABM_outputs_mass_cum.replace(file_scenario_names, pretty_scenarios[1:])
fig1 = px.line(ABM_outputs_mass_cum, x='Year', y='Waste', color = 'Scenario',
              labels = {'Waste':'Waste [metric tonnes]'})
fig1.update_layout(title_text='ABM Outputs: Cumulative Waste', title_x=0.2)
fig1.show()


# In[236]:


##graphing ABM inputs: yearly new installs
ABM_input_cum_installs = pd.read_csv(r'..\baselines\ABM\abm_input_cum_capacity.csv')

#undo cumsum to get yearly new installs
#change ABM_outputs_mass_cum cumulatives to yearly
ABM_input_yearly_installs = ABM_input_cum_installs.copy()
installs_diff = ABM_input_cum_installs.diff().fillna(0).astype(int)
ABM_input_yearly_installs['Yearly New Installs [MW]'] = installs_diff['Cumulative_PV_capacity_MW']
ABM_input_yearly_installs


# In[240]:


fig = go.Figure()

abm_y_values = list(ABM_input_yearly_installs['Yearly New Installs [MW]'].values)
ef_y_values = list(r2.scenario['landfill_ban'].data["new_Installed_Capacity_[MW]"].values)
    
fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=abm_y_values,
                    mode='lines',
                    name='ABM New Installs'))

fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=ef_y_values,
                    mode='lines',
                    name='Electrification Futures New Installs'))

fig.update_layout(title_text='Yearly New Installs', title_x=0.3, 
                 xaxis_title="Time",
    yaxis_title="Yearly New Installs [MW]",
    legend_title="Model")
fig.show()


# In[ ]:





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

