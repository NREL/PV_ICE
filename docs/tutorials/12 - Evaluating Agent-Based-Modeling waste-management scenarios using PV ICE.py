#!/usr/bin/env python
# coding: utf-8

# # 12 - Evaluating material circular efficacy of ABM waste-management scenarios using PV ICE

# This Jupyter journal uses results from Walzberg et al.'s PV ABM and inputs them into PV ICE, exploring the effect of increasing CE EoL pathway rates, recycling efficiency, and module reliability. The results of this journals were published on 
# 
# > <b> Acadia Hegedus, Silvana Ovaitt, Julien Walzberg, Heather Mirletz, Teresa Barnes. <i> Evaluating material circular efficacy of waste-management scenarios using PV ICE (PV in hte Circular Economy) tool</i>. NREL Student Intern Symposium, 2021.<b>
# 
# Steps include: 
# <ol>
#     <li> <a href='#step1'> Import libraries and create test folder for simulations </a> </li>
#     <li> <a href='#step2'> Create simulations and scenarios </a> </li>
#     <li> <a href='#step3'> Modify parameters </a> </li>
#     <ol>
#         <li> <a href='#step4'> Current Recovery (S1) </a> </li>
#         <li> <a href='#step5'> Ideal Recovery (S2) </a> </li>
#         <li> <a href='#step6'> Reliability Same New Installs (S3) </a> </li>
#         <li> <a href='#step7'> Reliability Maintaining Capacity (S4) </a> </li>
#     </ol>
#     <li> <a href='#step8'> Run mass flow calculations </a> </li>
#     <li> <a href='#step9'> Compile results </a> </li>
#     <li> <a href='#step10'> Plotting results </a> </li>
#     <li> <a href='#step11'> Graphing ABM outputs </a> </li>
#     <li> <a href='#step12'> Results validation </a> </li>
# </ol>

# ## Simulation Descriptions:
# - r1: For all 10 scenarios, the recycle ('mod_EOL_collection_eff'), reuse (mod_reuse), and repair (mod_Repair) rates are modified with outputs from ABM. Percent of collected modules & materials that are recycled ('mod_EOL_collected_recycled' & 'mat_EOL_collected_recycled') is set to 100 (i.e. it is assumed all collected modules are sent to recycling). Weibull parameters and lifetime is set to Irena Regular Loss values for all ABM scenarios (not PV ICE baseline). For the better_lifetime scenario, an improved lifetime, t50, t90 values are set (based on what was used in ABM) in a separate simulation called r1_better_lifetime. All other values are set to PV ICE defaults. 
# - r2: For all scenarios, the same modifications as in r1 are made. r2_better_lifetime has improved lifetime and reliability inputs as in r1_better_lifetime. Additionally, the recycling efficiency ('mat_EOL_Recycling_eff') are replaced with with FRELP recovery rates for all scenarios. 'mat_EOL_Recycled_into_HQ' is set to 100. 'mat_EOL_RecycledHQ_Reused4MFG' is also set to 100. 
# - r3A-r3D: For 3 select scenarios, the same parameters are modified as in r2. The Weibull shape parameters are changed based on Henry Hieslmair's parameters for the 4 reliability bins -- r3A is the A reliability bin (most reliable module), etc. 
# - r4A-r4D: For 3 select scenarios, the same parameters are modified as in r3A-r3D. The new installs needed are calculated and modified to account for the increased installed capacity as in r4. 
# 

# <a id='step1'></a>

# ## 1. Import libraries and create test folder for simulations

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


# <a id='step2'></a>

# ## 2. Create simulations and scenarios

# In[3]:


#create simulations
r1 = PV_ICE.Simulation(name='ABM_Simulation1', path=testfolder)
r1_better_lifetime = PV_ICE.Simulation(name='ABM_Simulation1BL', path=testfolder) #use this to eventually overwrite better_lifetime results in r1
r2 = PV_ICE.Simulation(name='ABM_Simulation2', path=testfolder)
r2_better_lifetime = PV_ICE.Simulation(name='ABM_Simulation2BL', path=testfolder) #use this to eventually overwrite better_lifetime results in r2
r3A = PV_ICE.Simulation(name='ABM_Simulation3A', path=testfolder)
r3B = PV_ICE.Simulation(name='ABM_Simulation3B', path=testfolder)
r3C = PV_ICE.Simulation(name='ABM_Simulation3C', path=testfolder)
r3D = PV_ICE.Simulation(name='ABM_Simulation3D', path=testfolder)
r4A = PV_ICE.Simulation(name='ABM_Simulation4A', path=testfolder)
r4B = PV_ICE.Simulation(name='ABM_Simulation4B', path=testfolder)
r4C = PV_ICE.Simulation(name='ABM_Simulation4C', path=testfolder)
r4D = PV_ICE.Simulation(name='ABM_Simulation4D', path=testfolder)

#create 10 scenarios in each simulation: 1st is standard in PV ICE, 2-10 are scenarios a-i in ABM
SIMULATIONS = [r1,r2]
SCENARIOS = ['standard_PVICE','landfill_ban','high_mat_recovery_cheap_recycling','cheap_recycling','high_landfill_costs','better_lifetime','better_learning','reuse_warranties','seeding_reuse','juliens_baseline']
for mysimulation in SIMULATIONS: 
    for myscenario in SCENARIOS:
        mysimulation.createScenario(name=myscenario, file=r'..\baselines\baseline_modules_US.csv')
        mysimulation.scenario[myscenario].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
        mysimulation.scenario[myscenario].addMaterial('aluminium_frames', file=r'..\baselines\baseline_material_aluminium_frames.csv')
        mysimulation.scenario[myscenario].addMaterial('silver', file=r'..\baselines\baseline_material_silver.csv')
        mysimulation.scenario[myscenario].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')
        mysimulation.scenario[myscenario].addMaterial('copper', file=r'..\baselines\baseline_material_copper.csv')

#create separate better_lifetime simulation with one scenario so that t50, t90, and lifetime modifications do not get overwritten
BETTER_LIFETIME_SIMULATIONS = [r1_better_lifetime, r2_better_lifetime]
for mysimulation in BETTER_LIFETIME_SIMULATIONS: 
    mysimulation.createScenario(name='better_lifetime', file=r'..\baselines\baseline_modules_US.csv')
    mysimulation.scenario['better_lifetime'].addMaterial('glass', file=r'..\baselines\baseline_material_glass.csv')
    mysimulation.scenario['better_lifetime'].addMaterial('aluminium_frames', file=r'..\baselines\baseline_material_aluminium_frames.csv')
    mysimulation.scenario['better_lifetime'].addMaterial('silver', file=r'..\baselines\baseline_material_silver.csv')
    mysimulation.scenario['better_lifetime'].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon.csv')
    mysimulation.scenario['better_lifetime'].addMaterial('copper', file=r'..\baselines\baseline_material_copper.csv')
    

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


#Irena RL Weibull Parameters to use for r1, r2
#overrides t50 and t90 inputs
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


# <a id='step3'></a>

# ## Modify Parameters

# <a id='step4'></a>

# ### Current Recovery (r1) 
# What is the effect of different reuse, recycle, and repair rates using PV ICE default recycling values?

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


# #### For r1_better_lifetime, modify same parameters as above, while also modifying scenario reliability inputs: mod_lifetime, mod_reliability_t50, & mod_reliability_t90

# In[12]:


#modify same values as in r1_better_lifetime simulation
past_years_collected_recycled = [r1_better_lifetime.scenario['better_lifetime'].data['mod_EOL_collected_recycled'][0]]*(2022-1995)
new_collected_recycled = [100]*(2050-2021)
#create new list to replace 'mod_EOL_collected_recycled' with, with 1995-2021 original baseline module values, and 2022-2050 at 100%
new_mod_recycled = past_years_collected_recycled + new_collected_recycled
r1_better_lifetime.scenario['better_lifetime'].data['mod_EOL_collected_recycled'] = new_mod_recycled
    
#next, set 'mat_EOL_collected_Recycled' to 100% for each material in scenarios 2-10 for years 2022 on (assume all collected materials are recycled)
MATERIALS = ['glass','aluminium_frames','silver','silicon','copper']
for mymaterial in MATERIALS:
    past_years_collected_recycled = [r1_better_lifetime.scenario['better_lifetime'].material[mymaterial].materialdata['mat_EOL_collected_Recycled'][0]]*(2022-1995)
    new_collected_recycled = [100]*(2050-2021)
    #create new list to replace 'mat_EOL_collected_Recycled' with, with 1995-2021 original baseline module values, and 2022-2050 at 100%
    new_mat_recycled = past_years_collected_recycled + new_collected_recycled
    r1_better_lifetime.scenario['better_lifetime'].material[mymaterial].materialdata['mat_EOL_collected_Recycled'] = new_mat_recycled
    
#change reuse, repair, and recycle rates
scenario_filter = 'Scenario == ' + '\"' + 'better_lifetime' + '\"'
new_outputs = ABM_outputs.query(scenario_filter)
#replace repairing baselines
repairs = new_outputs.loc[:,'mass_fraction_PV_materials_repaired_milliontonnes']*100
repairs.index = list(range(31))
frames1 = [r1_better_lifetime.scenario['better_lifetime'].data['mod_Repair'][0:27],repairs[2:]]
new_mod_Repairing = pd.concat(frames1)
r1_better_lifetime.scenario['better_lifetime'].data['mod_Repair'] = new_mod_Repairing.values
#replace recycling baselines
recycled = new_outputs.loc[:,'mass_fraction_PV_materials_recycled_milliontonnes']*100
if 'better_lifetime' == 'high_mat_recovery_cheap_recycling':
    recycles = recycled/0.96 #reflects higher material recovery rate (must change as ABM gives effective recycling rate)
else:
    recycles = recycled/0.80 #must change as ABM gives effective recycling rate
recycles.index = list(range(31))
frames2 = [r1_better_lifetime.scenario['better_lifetime'].data['mod_EOL_collection_eff'][0:27],recycles[2:]]
new_mod_Recycling = pd.concat(frames2)
r1_better_lifetime.scenario['better_lifetime'].data['mod_EOL_collection_eff'] = new_mod_Recycling.values
#replace reuse baselines
reuses = new_outputs.loc[:,'mass_fraction_PV_materials_reused_milliontonnes']*100
reuses.index = list(range(31))
frames3 = [r1_better_lifetime.scenario['better_lifetime'].data['mod_Reuse'][0:27],reuses[2:]]
new_mod_Reuse = pd.concat(frames3)
r1_better_lifetime.scenario['better_lifetime'].data['mod_Reuse'] = new_mod_Reuse.values

#change new installs to EF
r1_better_lifetime.scenario['better_lifetime'].data['new_Installed_Capacity_[MW]'] = electric_new_installs


# In[13]:


#modify reliability for better_lifetime
def lifetime_line(year):
    """"
    This function takes in a year and outputs the module lifetime based on scenario e) in ABM.
    Inputs
    year = desired year
    """
    m = (60-15.9)/(2050-2000)
    y = m*(year-2000) + 15.9
    return(y)


# In[14]:


#create list of mod_lifetime values based on linear regression
years = list(range(2022,2051)) #ONLY WANT to modify 2022 ONWARD
mod_lifetimes_list = []
for myyear in years:
    mod_lifetimes_list += [lifetime_line(myyear)]


# In[15]:


mod_lifetimes_df = pd.DataFrame()


# In[16]:


mod_lifetimes_df['year'] = years
mod_lifetimes_df['mod_lifetime'] = mod_lifetimes_list


# In[17]:


#changing mod_lifetime in scenario e) better_lifetime
new_mod_lifetime = list(r1_better_lifetime.scenario['better_lifetime'].data['mod_lifetime'][0:27].values) + mod_lifetimes_list
r1_better_lifetime.scenario['better_lifetime'].data['mod_lifetime'] = new_mod_lifetime


# In[18]:


#create linear regression for mod_reliability_t50 & mod_reliability_t90 vs. mod_lifetime 
#to estimate t50 and t90 values to input for improved lifetime scenario
reliability_baselines = pd.DataFrame()
reliability_baselines['mod_lifetime'] = r1.scenario['standard_PVICE'].data['mod_lifetime']
reliability_baselines['mod_reliability_t50'] = r1.scenario['standard_PVICE'].data['mod_reliability_t50']
reliability_baselines['mod_reliability_t90'] = r1.scenario['standard_PVICE'].data['mod_reliability_t90']


# In[19]:


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


# In[20]:


#changing mod_reliability_t50 & mod_reliability_t90 in scenario e) better_lifetime
new_mod_t50 = list(r1.scenario['standard_PVICE'].data['mod_reliability_t50'][0:27].values) + better_lifetime_t50_list
r1_better_lifetime.scenario['better_lifetime'].data['mod_reliability_t50'] = new_mod_t50

new_mod_t90 = list(r1.scenario['standard_PVICE'].data['mod_reliability_t90'][0:27].values) + better_lifetime_t90_list
r1_better_lifetime.scenario['better_lifetime'].data['mod_reliability_t90'] = new_mod_t90


# <a id='step5'></a>

# ### Ideal Recovery (r2)
# What is the effect of different reuse, recycle, and repair rates when FRELP recycling efficiencies are used and all recycled material is closed-loop?

# In[21]:


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


# In[22]:


#FRELP recovery rates and qualities
frelp_results = pd.DataFrame()
frelp_results['mat'] = ['silver','copper','aluminium_frames','silicon','glass']
frelp_results['recovery_rate'] = [94,97,99.4,97,98]
frelp_results['mat_recycled_into_HQ'] = [100,100,100,100,100]


# In[23]:


frelp_results


# In[24]:


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


# In[25]:


#use electrification futures base new installs
for myscenario in SCENARIOS:
    r2.scenario[myscenario].data['new_Installed_Capacity_[MW]'] = electric_new_installs


# #### For r2_better_lifetime, modify same parameters as in r2, while also modifying scenario reliability inputs as in r1_better_lifetime: mod_lifetime, mod_reliability_t50, & mod_reliability_t90

# In[26]:


#modify same values as in r2_better_lifetime simulation
past_years_collected_recycled = [r2_better_lifetime.scenario['better_lifetime'].data['mod_EOL_collected_recycled'][0]]*(2022-1995)
new_collected_recycled = [100]*(2050-2021)
#create new list to replace 'mod_EOL_collected_recycled' with, with 1995-2021 original baseline module values, and 2022-2050 at 100%
new_mod_recycled = past_years_collected_recycled + new_collected_recycled
r2_better_lifetime.scenario['better_lifetime'].data['mod_EOL_collected_recycled'] = new_mod_recycled
    
#next, set 'mat_EOL_collected_Recycled' to 100% for each material in scenarios 2-10 for years 2022 on (assume all collected materials are recycled)
MATERIALS = ['glass','aluminium_frames','silver','silicon','copper']
for mymaterial in MATERIALS:
    past_years_collected_recycled = [r2_better_lifetime.scenario['better_lifetime'].material[mymaterial].materialdata['mat_EOL_collected_Recycled'][0]]*(2022-1995)
    new_collected_recycled = [100]*(2050-2021)
    #create new list to replace 'mat_EOL_collected_Recycled' with, with 1995-2021 original baseline module values, and 2022-2050 at 100%
    new_mat_recycled = past_years_collected_recycled + new_collected_recycled
    r2_better_lifetime.scenario['better_lifetime'].material[mymaterial].materialdata['mat_EOL_collected_Recycled'] = new_mat_recycled
    
#change reuse, repair, and recycle rates
scenario_filter = 'Scenario == ' + '\"' + 'better_lifetime' + '\"'
new_outputs = ABM_outputs.query(scenario_filter)
#replace repairing baselines
repairs = new_outputs.loc[:,'mass_fraction_PV_materials_repaired_milliontonnes']*100
repairs.index = list(range(31))
frames1 = [r2_better_lifetime.scenario['better_lifetime'].data['mod_Repair'][0:27],repairs[2:]]
new_mod_Repairing = pd.concat(frames1)
r2_better_lifetime.scenario['better_lifetime'].data['mod_Repair'] = new_mod_Repairing.values
#replace recycling baselines
recycled = new_outputs.loc[:,'mass_fraction_PV_materials_recycled_milliontonnes']*100
if 'better_lifetime' == 'high_mat_recovery_cheap_recycling':
    recycles = recycled/0.96 #reflects higher material recovery rate (must change as ABM gives effective recycling rate)
else:
    recycles = recycled/0.80 #must change as ABM gives effective recycling rate
recycles.index = list(range(31))
frames2 = [r2_better_lifetime.scenario['better_lifetime'].data['mod_EOL_collection_eff'][0:27],recycles[2:]]
new_mod_Recycling = pd.concat(frames2)
r2_better_lifetime.scenario['better_lifetime'].data['mod_EOL_collection_eff'] = new_mod_Recycling.values
#replace reuse baselines
reuses = new_outputs.loc[:,'mass_fraction_PV_materials_reused_milliontonnes']*100
reuses.index = list(range(31))
frames3 = [r2_better_lifetime.scenario['better_lifetime'].data['mod_Reuse'][0:27],reuses[2:]]
new_mod_Reuse = pd.concat(frames3)
r2_better_lifetime.scenario['better_lifetime'].data['mod_Reuse'] = new_mod_Reuse.values

#change new installs to EF
r2_better_lifetime.scenario['better_lifetime'].data['new_Installed_Capacity_[MW]'] = electric_new_installs

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
    r2_better_lifetime.scenario['better_lifetime'].material[mymaterial].materialdata['mat_EOL_Recycling_eff'] = new_mat_EOL_recycling_eff
    r2_better_lifetime.scenario['better_lifetime'].material[mymaterial].materialdata['mat_EOL_Recycled_into_HQ'] = new_mat_EOL_recycled_into_HQ
    r2_better_lifetime.scenario['better_lifetime'].material[mymaterial].materialdata['mat_EOL_RecycledHQ_Reused4MFG'] = new_recycledHQ_reused4MFG

#change reliability values as in r1_better_lifetime
r2_better_lifetime.scenario['better_lifetime'].data['mod_lifetime'] = new_mod_lifetime
r2_better_lifetime.scenario['better_lifetime'].data['mod_reliability_t50'] = new_mod_t50
r2_better_lifetime.scenario['better_lifetime'].data['mod_reliability_t90'] = new_mod_t90


# <a id='step6'></a>

# ### Reliability Same New Installs (r3)
# What is the effect of module reliability when recycle rates, reuse rates, repair rates, and recycling efficiencies are changed for select scenarios with different repair bins? Using the same new installs (from NREL's 2021 Electrification Futures Study) as inputs. 

# In[27]:


#Figure out which scenarios to include
#ABM_outputs.groupby('Scenario').sum()['mass_fraction_PV_materials_repaired_milliontonnes'].sort_values()
#calculate scenarios with highest repair rates: better lifetime, better learning, julien’s baseline, landfill ban
#only do better learning, julien’s baseline, landfill ban as better lifetime already had different reliability


# In[28]:


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
    


# In[29]:


#modify shape parameters (overrides t50 and t90 baselines) -- values from Henry Hieslmair
weibullInputParamsA = {'alpha': 2.810, 'beta': 100.238} 
weibullInputParamsB = {'alpha': 3.841, 'beta': 57.491}
weibullInputParamsC = {'alpha': 4.602, 'beta': 40.767}
weibullInputParamsD = {'alpha': 5.692, 'beta': 29.697}


# In[30]:


#use electrification futures base new installs
for myr3simulation in r3_simulations:
    for myscenario in REPAIR_SCENARIOS:
        myr3simulation.scenario[myscenario].data['new_Installed_Capacity_[MW]'] = electric_new_installs


# <a id='step7'></a>

# ### Reliability Maintaining Capacity (r4)
# What is the effect on cumulative new installs and yearly virgin material demand for different repair bins, when capacity is set for all repair bins at bin A's capacity?

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


# <a id='step8'></a>

# ## Run mass flow calculations

# In[33]:


r1.calculateMassFlow(weibullInputParams= weibull_IrenaRL)
r1_better_lifetime.calculateMassFlow() #do not override reliabilty inputs with IRENA RL
r2.calculateMassFlow(weibullInputParams= weibull_IrenaRL)
r2_better_lifetime.calculateMassFlow() #do not override reliabilty inputs with IRENA RL
r3A.calculateMassFlow(weibullInputParams= weibullInputParamsA)
r3B.calculateMassFlow(weibullInputParams= weibullInputParamsB)
r3C.calculateMassFlow(weibullInputParams= weibullInputParamsC)
r3D.calculateMassFlow(weibullInputParams= weibullInputParamsD)
r4A.calculateMassFlow(weibullInputParams= weibullInputParamsA)
r4B.calculateMassFlow(weibullInputParams= weibullInputParamsB)
r4C.calculateMassFlow(weibullInputParams= weibullInputParamsC)
r4D.calculateMassFlow(weibullInputParams= weibullInputParamsD)


# In[34]:


Under_Installment = []
weibullparams = [weibullInputParamsA, weibullInputParamsB, weibullInputParamsC, weibullInputParamsD]
for myr4simulation in r4_simulations:
    myweibullparams = weibullparams[r4_simulations.index(myr4simulation)]
    for i in range (0, len(myr4simulation.scenario['juliens_baseline'].data)): #runs for each year
        for myscenario in REPAIR_SCENARIOS:
            Under_Installment = ((r4_simulations[0].scenario[myscenario].data['Installed_Capacity_[W]'][i] - #have reliability bin A's installed capacity be matched within a given scenario -- this used to be myr4simulation.scenario['juliens_baseline'].data['Installed_Capacity_[W]'][i]
                             myr4simulation.scenario[myscenario].data['Installed_Capacity_[W]'][i])/1000000 )  # MWATTS
            myr4simulation.scenario[myscenario].data['new_Installed_Capacity_[MW]'][i] += Under_Installment
        myr4simulation.calculateMassFlow(weibullInputParams= myweibullparams)


# <a id='step9'></a>

# ## Compile results

# In[35]:


USyearly=pd.DataFrame()


# In[36]:


keyword='mat_Virgin_Stock'
materials = ['glass', 'aluminium_frames','silicon', 'silver', 'copper']
SIMULATIONS = [r1,r2, r3A, r3B, r3C, r3D, r4A, r4B, r4C, r4D]

# Loop over Simulations
for mysimulation in SIMULATIONS:
    for jj in range(0, len(mysimulation.scenario)): # Loop over Scenarios
        case = list(mysimulation.scenario.keys())[jj] # case gives scenario name
        
        if mysimulation == r1 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r1_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["VirginStock_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('VirginStock') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['VirginStock_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        elif mysimulation == r2 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r2_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["VirginStock_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('VirginStock') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['VirginStock_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)  
            
        else:
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["VirginStock_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('VirginStock') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['VirginStock_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[37]:


keyword='mat_Total_Landfilled'

for mysimulation in SIMULATIONS:
    for jj in range(0, len(mysimulation.scenario)): # Loop over Scenarios
        case = list(mysimulation.scenario.keys())[jj] # case gives scenario name
        
        if mysimulation == r1 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r1_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["Waste_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('Waste') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['Waste_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        elif mysimulation == r2 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r2_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["Waste_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('Waste') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['Waste_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        else:
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["Waste_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('Waste') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['Waste_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[38]:


keyword='mat_Total_EOL_Landfilled'

for mysimulation in SIMULATIONS:
    for jj in range(0, len(mysimulation.scenario)): # Loop over Scenarios
        case = list(mysimulation.scenario.keys())[jj] # case gives scenario name
        
        if mysimulation == r1 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r1_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["Waste_EOL_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('Waste_EOL') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['Waste_EOL_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        elif mysimulation == r2 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r2_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["Waste_EOL_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('Waste_EOL') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['Waste_EOL_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
        
        else:
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["Waste_EOL_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('Waste_EOL') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['Waste_EOL_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[39]:


keyword='mat_EoL_Recycled_HQ_into_MFG'
r1_r2 = [r1,r2]

for mysimulation in r1_r2:
    for jj in range(0, len(mysimulation.scenario)): # Loop over Scenarios
        case = list(mysimulation.scenario.keys())[jj] # case gives scenario name
        
        if mysimulation == r1 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r1_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["EOL_Recycled_HQ_into_MFG_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_HQ_into_MFG') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['EOL_Recycled_HQ_into_MFG_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        elif mysimulation == r2 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r2_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["EOL_Recycled_HQ_into_MFG_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_HQ_into_MFG') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['EOL_Recycled_HQ_into_MFG_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        else:
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["EOL_Recycled_HQ_into_MFG_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_HQ_into_MFG') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['EOL_Recycled_HQ_into_MFG_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[40]:


keyword='mat_EOL_Recycled_HQ_into_OU'

for mysimulation in r1_r2:
    for jj in range(0, len(mysimulation.scenario)): # Loop over Scenarios
        case = list(mysimulation.scenario.keys())[jj] # case gives scenario name
        
        if mysimulation == r1 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r1_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["EOL_Recycled_HQ_into_OU_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_HQ_into_OU') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['EOL_Recycled_HQ_into_OU_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        elif mysimulation == r2 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r2_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["EOL_Recycled_HQ_into_OU_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_HQ_into_OU') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['EOL_Recycled_HQ_into_OU_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        else:
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["EOL_Recycled_HQ_into_OU_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_HQ_into_OU') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['EOL_Recycled_HQ_into_OU_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[41]:


keyword='mat_EOL_Recycled_2_OQ'

for mysimulation in r1_r2:
    for jj in range(0, len(mysimulation.scenario)): # Loop over Scenarios
        case = list(mysimulation.scenario.keys())[jj] # case gives scenario name
        
        if mysimulation == r1 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r1_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["EOL_Recycled_2_OQ_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_2_OQ') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['EOL_Recycled_2_OQ_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        elif mysimulation == r2 and case == 'better_lifetime':
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = r2_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["EOL_Recycled_2_OQ_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_2_OQ') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['EOL_Recycled_2_OQ_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)
            
        else:
            for ii in range (0, len(materials)):    
                material = materials[ii]
                foo = mysimulation.scenario[case].material[material].materialdata[keyword].copy()
                foo = foo.to_frame(name=material)
                USyearly["EOL_Recycled_2_OQ_"+material+'_'+mysimulation.name+'_'+case] = foo[material]
            filter_col = [col for col in USyearly if (col.startswith('EOL_Recycled_2_OQ') and col.endswith(mysimulation.name+'_'+case)) ]
            USyearly['EOL_Recycled_2_OQ_Module_'+mysimulation.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# In[42]:


USyearly = USyearly/1000000  #Convert to metric tonnes
#907185 -- this is for US tons


# In[43]:


keyword='new_Installed_Capacity_[MW]'

#for simulations r1 through r3D
for mysimulation in SIMULATIONS[0:6]: 
    newcolname = keyword+'_'+mysimulation.name 
    if newcolname in USyearly:
        USyearly[newcolname] = USyearly[newcolname]+mysimulation.scenario[list(mysimulation.scenario.keys())[0]].data[keyword]
    else:
        USyearly[keyword+'_'+mysimulation.name] = mysimulation.scenario[list(mysimulation.scenario.keys())[0]].data[keyword]
        
#for simulations r4A through r4D
for mysimulation in SIMULATIONS[6:]:
    for myscenario in REPAIR_SCENARIOS:
        newcolname = keyword+'_'+mysimulation.name+'_'+myscenario
        if newcolname in USyearly:
            USyearly[newcolname] = USyearly[newcolname]+mysimulation.scenario[myscenario].data[keyword]
        else:
            USyearly[newcolname] = mysimulation.scenario[myscenario].data[keyword]


# In[44]:


keyword='Repaired_[W]'

#for simulations r3A through r3D
for mysimulation in SIMULATIONS[2:6]:
    for myscenario in REPAIR_SCENARIOS:
        newcolname = 'Repaired_[MW]'+'_'+mysimulation.name+'_'+myscenario
        if newcolname in USyearly:
            USyearly[newcolname] = USyearly[newcolname]+mysimulation.scenario[myscenario].data[keyword]/1000000 #change to MW
        else:
            USyearly[newcolname] = mysimulation.scenario[myscenario].data[keyword]/1000000 #change to MW


# In[45]:


keyword='Repaired_Area'

#for simulations r3A through r3D
for mysimulation in SIMULATIONS[2:6]:
    for myscenario in REPAIR_SCENARIOS:
        newcolname = keyword+'_'+mysimulation.name+'_'+myscenario
        if newcolname in USyearly:
            USyearly[newcolname] = USyearly[newcolname]+mysimulation.scenario[myscenario].data[keyword]
        else:
            USyearly[newcolname] = mysimulation.scenario[myscenario].data[keyword]


# In[46]:


UScum = USyearly.copy()
UScum = UScum.cumsum()


# In[47]:


keyword='Installed_Capacity_[W]'

for mysimulation in SIMULATIONS:
    for i in range(0, len(mysimulation.scenario)):
        case = list(mysimulation.scenario.keys())[i]
        if mysimulation == r1 and case == 'better_lifetime':
            foo = r1_better_lifetime.scenario[case].data[keyword]
            foo = foo.to_frame(name=keyword)
            UScum["Capacity_"+mysimulation.name+'_'+case] = foo[keyword].values/1000000 #change to MW
        elif mysimulation == r2 and case == 'better_lifetime':
            foo = r2_better_lifetime.scenario[case].data[keyword]
            foo = foo.to_frame(name=keyword)
            UScum["Capacity_"+mysimulation.name+'_'+case] = foo[keyword].values/1000000 #change to MW
        else:
            foo = mysimulation.scenario[case].data[keyword]
            foo = foo.to_frame(name=keyword)
            UScum["Capacity_"+mysimulation.name+'_'+case] = foo[keyword].values/1000000 #change to MW


# In[48]:


USyearly.index = r1.scenario['standard_PVICE'].data['year']
UScum.index = r1.scenario['standard_PVICE'].data['year']


# In[49]:


USyearly.to_csv('ABM_Yearly_Results.csv')
UScum.to_csv('ABM_Cumulative_Results.csv')


# <a id='step10'></a>

# ## Plotting results

# In[51]:


pretty_scenarios = ['PV ICE baseline','Landfill ban','High material recovery & <br> lower recycling costs','Lower recycling costs','Higher landfill costs','Improved lifetime','Improved learning effect','Reuse warranties','Seeding reuse','ABM baseline']


# In[146]:


filter_col = [col for col in UScum if (col.startswith('Capacity_ABM_Simulation1'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]
df = df[df.variable.isin(['ABM baseline','Improved lifetime'])]
df["variable"].replace({"ABM baseline": "All other scenarios"}, inplace=True)
fig1 = px.line(df, x='year', y='value', color = 'variable', labels={
                     "year": "Year",
                     "value": "Installed Capacity [MW]",
                    "variable" :"Scenario"
                 })
fig1.update_layout(#title_text='Simulations 1 & 2: Installed Capacity', title_x=0.5, #stays same for both simulation
height = 800, width = 1000)
fig1.update_layout(font=dict(size=25))
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
ef_values = list(r2.scenario['standard_PVICE'].data['new_Installed_Capacity_[MW]'].cumsum()[25:].values)
fig1.add_trace(go.Scatter(x=list(range(2020,2051)), y=ef_values,
                    mode='markers',
                    name='EF Cumulative New Installs',
                    marker_color = 'black')) 
fig1.show()


# In[150]:


filter_col = [col for col in UScum if (col.startswith('Capacity_ABM_Simulation1'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df_2050 = df[df.year.isin([2050])]
df_2050 = df_2050[df_2050.variable.isin(pretty_scenarios[0:5] + pretty_scenarios[6:])]
df_avg = pd.DataFrame()
df_avg['Installed Capacity at 2050 [MW]'] = [df_2050['value'].mean()]
df_avg['high'] = [df_2050['value'].max()]
df_avg['low'] = [df_2050['value'].min()]
df_avg['year'] = [2050]
print( "The installed capacity at 2050 for all scenarios except Improved lifetime is approx. " + str(df_avg['Installed Capacity at 2050 [MW]'][0]) + ' MW.')

#calculate max and min relative to average
bigger_range = max(df_avg['high'][0] - df_avg['Installed Capacity at 2050 [MW]'][0],abs(df_avg['low'][0] - df_avg['Installed Capacity at 2050 [MW]'][0]))
percent_diff = (bigger_range/df_avg['Installed Capacity at 2050 [MW]'][0]*100).round(1)
print("The percent difference that this is off by depending on the scenario is +/- " + str(percent_diff) + ' %.')


# In[152]:


# average cumulative virgin material demand for simulation 2 comparison
filter_col = [col for col in UScum if (col.startswith('VirginStock_Module_ABM_Simulation1'))]
df = UScum[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]

df_avg_r1_virgin_material_demand_cum = df.groupby(['year']).mean()
df_avg_r1_virgin_material_demand_cum['year'] = list(range(2020,2051))
df_avg_r1_virgin_material_demand_cum['variable'] = 'Average Cumulative Virgin Material Demand from Simulation 1'

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


fig.update_layout( #title_text='Simulations 1 & 2: Cumulative Virgin Material Demand', title_x=0.5, 
                 xaxis_title="Year",
    yaxis_title="Material Demand [metric tonnes]",
    legend_title="Scenario", height = 1100, width = 1000)
fig.update_layout(font=dict(size=25))
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig.update_yaxes(range=[0,66000000])
fig.show()


# In[153]:


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
    go.Bar(name='S1 HQ Closed Loop', x=pretty_scenarios, y=hq_closed), 
    go.Bar(name='S1 HQ Open Loop', x=pretty_scenarios, y=hq_open),
    go.Bar(name='S1 OQ Open Loop', x=pretty_scenarios, y=oq_open)
])

fig.add_trace(go.Scatter(x=pretty_scenarios, y=hq_closed_sim2,
                    mode='markers',
                    name='S2 HQ Closed Loop', 
                    marker=dict(size=[20, 20, 20, 20, 20, 20, 20, 20, 20, 20])))


# Change the bar mode
fig.update_layout(barmode='stack', #title_text = 'Simulations 1 & 2: Cumulative Recycled Material at 2050', title_x = 0.5, 
                  xaxis_title="Scenario",
    yaxis_title="Recycled Material [metric tonnes]",
    legend_title="Recycled Material Type")
fig.update_layout(font=dict(size=25), height = 1000, width = 1300)
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.68
))
fig.show()


# In[93]:


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
s1_landfill_ban = list(df1[df1.variable.isin(['Landfill ban'])].loc[:,'value'].values) #max value from sim 1
s1_reuse_warranties = list(df1[df1.variable.isin(['Reuse warranties'])].loc[:,'value'].values) #min value from sim 1
s1_abm_baseline = list(df1[df1.variable.isin(['ABM baseline'])].loc[:,'value'].values) #abm baseline from sim 1

fig = go.Figure()

for myscenario in pretty_scenarios:
    y_values = list(df2[df2.variable.isin([myscenario])].loc[:,'value'].values)
    fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=y_values,
                    mode='lines',
                    name='S2 '+ myscenario))
    
fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=s1_landfill_ban,
                    mode='markers',
                    name='S1 Landfill ban', 
                    marker_color='rgba(239, 85, 58, 1)',
                    marker=dict(size=13)))
fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=s1_reuse_warranties,
                    mode='markers',
                    name='S1 Reuse warranties',
                    marker_color='rgba(209, 240, 175, 1)',
                     marker=dict(size=13)))
fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=s1_abm_baseline,
                    mode='markers',
                    name= 'S1 ABM Baseline', 
                    marker_color='rgba(254, 230, 171, 1)',
                    marker=dict(size=13)))

fig.update_layout(#title_text='Simulations 1 & 2: Yearly Waste', title_x=0.5, 
                 xaxis_title="Year",
    yaxis_title="Waste [metric tonnes]",
    legend_title="Scenario")
fig.update_layout(font=dict(size=26), height = 1100, width = 1000)
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig.show()


# In[94]:


#cumulative waste at 2050 bar chart sim 1 vs. sim 2
x_labels = pretty_scenarios[1:5]

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
fig.update_layout(#title_text = 'Simulations 1 & 2: Cumulative Waste at 2050', title_x = 0.5, 
                  xaxis_title="Scenario",
    yaxis_title="Waste [metric tonnes]",
    legend_title="Simulation")
fig.update_xaxes(tickangle=18)
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig.update_layout(font=dict(size=23), height = 850, width = 800)
fig.show()


# In[100]:


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

#make bin labels more descriptive
df = df.reset_index()
new_reliability_bin = []
for i in range(0,len(df['reliability_bin'])):
    if df.loc[i,'reliability_bin'] == 'A':
        new_reliability_bin += ['S3A (most reliable)']
    elif df.loc[i,'reliability_bin'] == 'D':
        new_reliability_bin += ['S3D (least reliable)'] 
    elif df.loc[i,'reliability_bin'] == 'B':
        new_reliability_bin += ['S3B'] 
    elif df.loc[i,'reliability_bin'] == 'C':
        new_reliability_bin += ['S3C'] 
    else:
        new_reliability_bin += [df.loc[i,'reliability_bin']]
df['new_reliability_bin'] = new_reliability_bin

fig1 = px.line(df, x='year', y='value', color = 'new_reliability_bin', facet_col = 'scenario', 
               facet_col_spacing = 0.04, 
               labels={
                     "year": "Year",
                     "value": "Waste [metric tonnes]",
                    "new_reliability_bin":"Reliability Bin"
                },  color_discrete_sequence=px.colors.qualitative.Set1,
              category_orders={"scenario": ["juliens_baseline", "better_learning", "landfill_ban"]})
#fig1.update_layout(title_text='Simulation 3: Cumulative Waste for Different Reliability Bins', title_x=0.5)
fig1.update_layout(font=dict(size=20), height = 1000, width = 1000)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved learning effect")
                                            , font_size=27))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill ban")))
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.7
))
fig1.update_xaxes(tickangle=45)
fig1.show()


# In[104]:


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

#make bin labels more descriptive
df = df.reset_index()
new_reliability_bin = []
for i in range(0,len(df['reliability_bin'])):
    if df.loc[i,'reliability_bin'] == 'A':
        new_reliability_bin += ['S3A (most reliable)']
    elif df.loc[i,'reliability_bin'] == 'D':
        new_reliability_bin += ['S3D (least reliable)'] 
    elif df.loc[i,'reliability_bin'] == 'B':
        new_reliability_bin += ['S3B'] 
    elif df.loc[i,'reliability_bin'] == 'C':
        new_reliability_bin += ['S3C'] 
    else:
        new_reliability_bin += [df.loc[i,'reliability_bin']]
df['new_reliability_bin'] = new_reliability_bin

fig1 = px.line(df, x='year', y='value', color = 'new_reliability_bin', facet_col = 'scenario', 
               facet_col_spacing = 0.04, 
               labels={
                     "year": "Year",
                     "value": "Material Demand [metric tonnes]",
                    "new_reliability_bin":"Reliability Bin"
                },  color_discrete_sequence=px.colors.qualitative.Set1,
              category_orders={"scenario": ["juliens_baseline", "better_learning", "landfill_ban"]})
#fig1.update_layout(title_text='Simulation 3: Cumulative Virgin Material Demand for Different Reliability Bins', title_x=0.5)
fig1.update_layout(font=dict(size=18), height = 1000, width = 1000)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved learning effect")
                                           , font_size=27))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill ban")))
fig1.update_xaxes(tickangle=45)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.73
))
fig1.update_yaxes(range=[0,66000000])
fig1.show()


# In[181]:


#quantify difference across scenarios / bins for installed capacity S3
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
df = df[df.year.isin([2050])]

percent_diff = []
for mybin in ['A','B','C','D']:
    mydf = df[df.reliability_bin.isin([mybin])]
    better_learning_diff = list((mydf[mydf.scenario.isin(['better_learning'])]['value'].values - mydf[mydf.scenario.isin(['juliens_baseline'])]['value'].values)/ (mydf[mydf.scenario.isin(['juliens_baseline'])]['value'].values))
    landfill_ban_diff = list((mydf[mydf.scenario.isin(['juliens_baseline'])]['value'].values - mydf[mydf.scenario.isin(['landfill_ban'])]['value'].values)/ (mydf[mydf.scenario.isin(['juliens_baseline'])]['value'].values))
    percent_diff += better_learning_diff + [0] + landfill_ban_diff
    
df['percent_diff'] = percent_diff
print("The maximum percent difference for all bins and scenarios in S3 relative to ABM baseline installed capacity is " + str(df['percent_diff'].max() * 100) + "%")


# In[129]:


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
df = df[df.scenario.isin(['juliens_baseline'])] #show ABM baseline only

#make bin labels more descriptive
df = df.reset_index()
new_reliability_bin = []
for i in range(0,len(df['reliability_bin'])):
    if df.loc[i,'reliability_bin'] == 'A':
        new_reliability_bin += ['S3A (most reliable)']
    elif df.loc[i,'reliability_bin'] == 'D':
        new_reliability_bin += ['S3D (least reliable)'] 
    elif df.loc[i,'reliability_bin'] == 'B':
        new_reliability_bin += ['S3B'] 
    elif df.loc[i,'reliability_bin'] == 'C':
        new_reliability_bin += ['S3C'] 
    else:
        new_reliability_bin += [df.loc[i,'reliability_bin']]
df['new_reliability_bin'] = new_reliability_bin

fig1 = px.line(df, x='year', y='value', color = 'new_reliability_bin',labels={
                     "year": "Year",
                     "value": "Installed Capacity [MW]",
                    "new_reliability_bin":"Reliability Bin"
                },  color_discrete_sequence=px.colors.qualitative.Set1)
#fig1.update_layout(title_text='Simulation 3: Installed Capacity for Different Reliability Bins', title_x=0.47)
#fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved learning effect")))
#fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM baseline")))
#fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill ban")))
#fig1.update_xaxes(tickangle=-45)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.update_layout(font=dict(size=25), height = 800, width = 800)
ef_values = list(r2.scenario['standard_PVICE'].data['new_Installed_Capacity_[MW]'].cumsum()[25:].values)
fig1.add_trace(go.Scatter(x=list(range(2020,2051)), y=ef_values,
                    mode='markers',
                    name='EF Cumulative New Installs',
                    marker_color = 'black')) 
fig1.show()


# In[81]:


filter_col = [col for col in UScum if (col.startswith('Repaired_[MW]_ABM_Simulation3'))]
df = UScum[filter_col]
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
scenario_splices = []
for i in range(0,len(df['variable'])):
    scenario_splices += [df.loc[i,'variable'][31:]]
quality_splices = []
for i in range(0,len(df['variable'])):
    quality_splices += [df.loc[i,'variable'][29]]
df['scenario'] = scenario_splices
df['reliability_bin'] = quality_splices
df = df.drop("variable", axis=1)
df = df[df.year.isin(list(range(2020,2051)))]

#make bin labels more descriptive
df = df.reset_index()
new_reliability_bin = []
for i in range(0,len(df['reliability_bin'])):
    if df.loc[i,'reliability_bin'] == 'A':
        new_reliability_bin += ['S3A (most reliable)']
    elif df.loc[i,'reliability_bin'] == 'D':
        new_reliability_bin += ['S3D (least reliable)'] 
    elif df.loc[i,'reliability_bin'] == 'B':
        new_reliability_bin += ['S3B'] 
    elif df.loc[i,'reliability_bin'] == 'C':
        new_reliability_bin += ['S3C'] 
    else:
        new_reliability_bin += [df.loc[i,'reliability_bin']]
df['new_reliability_bin'] = new_reliability_bin

fig1 = px.line(df, x='year', y='value', color = 'new_reliability_bin', facet_col = 'scenario', 
               facet_col_spacing = 0.04, 
               labels={
                     "year": "Year",
                     "value": "Repairs [MW]",
                    "new_reliability_bin":"Reliability Bin"
                },  color_discrete_sequence=px.colors.qualitative.Set1,
              category_orders={"scenario": ["juliens_baseline", "better_learning", "landfill_ban"]})
#fig1.update_layout(title_text='Simulation 3: Cumulative Repairs for Different Reliability Bins', title_x=0.5)
fig1.update_layout(font=dict(size=20), height = 1000, width = 1000)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved learning effect")
                                            , font_size=27))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill ban")))
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.7
))
fig1.update_xaxes(tickangle=45)
fig1.show()


# In[105]:


#simulation 4 lines
filter_col = [col for col in UScum if (col.startswith(('new_Installed_Capacity_[MW]_ABM_Simulation4A_landfill_ban','new_Installed_Capacity_[MW]_ABM_Simulation4B_landfill_ban','new_Installed_Capacity_[MW]_ABM_Simulation4C_landfill_ban','new_Installed_Capacity_[MW]_ABM_Simulation4D_landfill_ban')))]
df4 = UScum[filter_col]
s4_traces = ['S4A (most reliable)','S4B','S4C','S4D (least reliable)']
df4 = df4.set_axis(s4_traces, axis=1)
df4['year'] = list(range(1995,2051))
df4 = df4.melt(id_vars = 'year')
df4 = df4[df4.year.isin(list(range(2020,2051)))]

#simulation 3A
filter_col = [col for col in UScum if (col.startswith('new_Installed_Capacity_[MW]_ABM_Simulation3A'))]
df3 = UScum[filter_col]
df3 = df3.set_axis(['S3A (most reliable)'], axis=1)
df3['year'] = list(range(1995,2051))
df3 = df3.melt(id_vars = 'year')
df3 = df3[df3.year.isin(list(range(2020,2051)))]

fig = go.Figure()

for mytrace in s4_traces:
    y_values = list(df4[df4.variable.isin([mytrace])].loc[:,'value'].values)
    fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=y_values,
                    mode='lines',
                    name=mytrace, marker_color = px.colors.qualitative.Set1[s4_traces.index(mytrace)]))   

y_values = list(df3.loc[:,'value'].values)
fig.add_trace(go.Scatter(x=list(range(2020,2051)), y=y_values,
                    mode='markers',
                    name='Electrification Futures Study',
                    marker_color = 'black')) 
    
fig.update_layout(#title_text='Simulations 3 & 4: Cumulative New Installs for Different Reliability Bins', title_x=0.5, 
                 xaxis_title="Year",
    yaxis_title="New Installs [metric tonnes]",
    legend_title="Scenario", height = 800, width = 1000)
fig.update_layout(font=dict(size=25))
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig.show()


# In[65]:


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

#make bin labels more descriptive
df = df.reset_index()
new_reliability_bin = []
for i in range(0,len(df['reliability_bin'])):
    if df.loc[i,'reliability_bin'] == 'A':
        new_reliability_bin += ['S4A (most reliable)']
    elif df.loc[i,'reliability_bin'] == 'D':
        new_reliability_bin += ['S4D (least reliable)'] 
    elif df.loc[i,'reliability_bin'] == 'B':
        new_reliability_bin += ['S4B'] 
    elif df.loc[i,'reliability_bin'] == 'C':
        new_reliability_bin += ['S4C'] 
    else:
        new_reliability_bin += [df.loc[i,'reliability_bin']]
df['new_reliability_bin'] = new_reliability_bin

fig1 = px.line(df, x='year', y='value', color = 'new_reliability_bin', facet_col = 'scenario', 
               facet_col_spacing = 0.04,
               labels={
                     "year": "Year",
                     "value": "Material Demand [metric tonnes]",
                    "new_reliability_bin":"Reliability Bin"
                },  color_discrete_sequence=px.colors.qualitative.Set1,
              category_orders={"scenario": ["juliens_baseline", "better_learning", "landfill_ban"]})
#fig1.update_layout(title_text='Simulation 4: Cumulative Virgin Material Demand for Different Reliability Bins with Fewer New Installs', title_x=0.5)
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=better_learning", "Improved learning effect"),
                                           font_size = 27))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=juliens_baseline", "ABM baseline")))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("scenario=landfill_ban", "Landfill ban")))
fig1.update_xaxes(tickangle=45)
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.7
))
fig1.update_layout(font=dict(size=20), height = 1000, width = 1000)
fig1.update_yaxes(range=[0,66000000])
fig1.show()


# <a id='step11'></a>

# ## Graphing ABM outputs

# In[67]:


df = ABM_outputs.rename(columns={'mass_fraction_PV_materials_repaired_milliontonnes':'Repaired',
                                'mass_fraction_PV_materials_reused_milliontonnes':'Reused',
                                'mass_fraction_PV_materials_recycled_milliontonnes':'Recycled',
                                'mass_fraction_PV_materials_landfilled_milliontonnes':'Landfilled',
                                'mass_fraction_PV_materials_stored_milliontonnes':'Stored'})
df['Scenario'] = [pretty_scenarios[1]] * 31 + [pretty_scenarios[2]] * 31 + [pretty_scenarios[3]] * 31 + [pretty_scenarios[4]] * 31 + [pretty_scenarios[5]] * 31 + [pretty_scenarios[6]] * 31 + [pretty_scenarios[7]] * 31 + [pretty_scenarios[8]] * 31 + [pretty_scenarios[9]] * 31
df = df.melt(id_vars = ('Year','Scenario'))
fig1 = px.bar(df, x="Year", y="value", color="variable", #title="ABM Outputs: Yearly Mass Fraction of Material in EOL Pathways",
             labels={'value':'Mass Fraction',
                    'variable':'EoL Pathway'}, 
              facet_col = 'Scenario',
             facet_col_wrap=3, width = 1200, height = 1000,
             category_orders={"Scenario": ["ABM baseline", "Improved learning effect", "Landfill ban","Lower recycling costs"]})
fig1.update_layout(title_x=0.5, title_y=0.98,font=dict(size=24))
fig1.update_xaxes(tickangle=45)
#make scenario annotations nicer
for myscenario in pretty_scenarios[1:]:    
    fig1.for_each_annotation(lambda a: a.update(text=a.text.replace("Scenario=" + myscenario, myscenario)))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace(pretty_scenarios[2], 'High material recovery<br> and lower recycling costs')))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace(pretty_scenarios[1], '<b>Landfill ban</b>')))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace(pretty_scenarios[9], '<b>ABM baseline</b>')))
fig1.for_each_annotation(lambda a: a.update(text=a.text.replace(pretty_scenarios[6], '<b>Improved learning effect</b>')))
fig1.show()


# In[68]:


# PV ICE baseline graphing (to compare to above graph)
pv_ice_baseline_eol_rates = pd.DataFrame()
pv_ice_baseline_eol_rates['Repaired'] = list(r1.scenario['standard_PVICE'].data['mod_Repair']/100)
pv_ice_baseline_eol_rates['Reused'] = list(r1.scenario['standard_PVICE'].data['mod_Reuse']/100)
pv_ice_baseline_eol_rates['Recycled'] = list(r1.scenario['standard_PVICE'].data['mod_EOL_collection_eff']/100 * r1.scenario['standard_PVICE'].data['mod_EOL_collected_recycled']/100)
pv_ice_baseline_eol_rates['Landfilled'] = 1 - (pv_ice_baseline_eol_rates['Repaired']+pv_ice_baseline_eol_rates['Reused']+pv_ice_baseline_eol_rates['Recycled'])
pv_ice_baseline_eol_rates['Year'] = list(range(1995,2051))
df = pv_ice_baseline_eol_rates.melt(id_vars = 'Year')
df = df[df.Year.isin([2020])]

fig1 = px.bar(df, x="Year", y="value", color="variable", #title="PV ICE Baseline: Yearly Mass Fraction of Material in EOL Pathways",
             labels={'value':'Mass Fraction',
                    'variable':'EoL Pathway',
                    'Year':'All Years'}, 
              width = 400, height = 500)
fig1.update_xaxes(showticklabels=False)
fig1.update_layout(title_x=0.5, title_y=0.98,font=dict(size=24))

for data in fig1.data:
    data["width"] = 0.20 #Change this value for bar widths
fig1.show()


# In[106]:


file_scenario_names = ABM_outputs_mass_cum['Scenario'].unique().tolist()
ABM_outputs_mass_cum = ABM_outputs_mass_cum.replace(file_scenario_names, pretty_scenarios[1:])
fig1 = px.line(ABM_outputs_mass_cum, x='Year', y='Waste', color = 'Scenario',
              labels = {'Waste':'Waste [metric tonnes]'})
fig1.update_layout(#title_text='ABM Outputs: Cumulative Waste', title_x=0.5,
                   height = 800, width = 1000)
fig1.update_layout(font=dict(size=25))
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.update_yaxes(range=[0,9000000])
fig1.show()


# <a id='step12'></a>

# ## Results validation

# In[82]:


##graphing ABM inputs: yearly new installs
ABM_input_cum_installs = pd.read_csv(r'..\baselines\ABM\abm_input_new_installs_cumulative.csv') #changed to MW from GW in excel

#undo cumsum to get yearly new installs
#add yearly installs col
ABM_input_new_installs = ABM_input_cum_installs.copy()
installs_diff = ABM_input_cum_installs.diff().fillna(0).astype(int)
installs_diff.loc[0,'Cumulative_New_Installs_[MW]'] = ABM_input_cum_installs.loc[0,'Cumulative_New_Installs_[MW]'] #get rid of first 0
ABM_input_new_installs['Yearly_New_Installs_[MW]'] = installs_diff['Cumulative_New_Installs_[MW]']


# In[87]:


fig = go.Figure()

abm_y_values = list(ABM_input_new_installs['Cumulative_New_Installs_[MW]'].values)
ef_y_values = list(r2.scenario['landfill_ban'].data['new_Installed_Capacity_[MW]'].cumsum()[5:].values) #only show 2000 onwards
    
fig.add_trace(go.Scatter(x=list(range(2000,2051)), y=abm_y_values,
                    mode='lines',
                    name='ABM'))

fig.add_trace(go.Scatter(x=list(range(2000,2051)), y=ef_y_values,
                    mode='lines',
                    name='Electrification Futures Study'))

fig.update_layout(#title_text='Cumulative New Installs by Source', title_x=0.5, 
                 xaxis_title="Year",
    yaxis_title="Cumulative New Installs [MW]",
    legend_title="Source",
                   height = 800, width = 1000)
fig.update_layout(font=dict(size=25))
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.98,
    xanchor="left",
    x=0.01
))
fig.show()


# #### Rerun r2 with Julien's new installs and recovery rates and see results

# In[107]:


#CHANGE NEW INSTALLS TO MATCH JULIENS
abm_new_installs = list(ABM_input_new_installs['Yearly_New_Installs_[MW]'].values) # yearly new installs 2020-2050
ef_new_installs = list(r2.scenario['landfill_ban'].data["new_Installed_Capacity_[MW]"][:5].values)
for myscenario in ABM_SCENARIOS: 
    r2.scenario[myscenario].data['new_Installed_Capacity_[MW]'] = ef_new_installs + abm_new_installs
r2_better_lifetime.scenario['better_lifetime'].data['new_Installed_Capacity_[MW]'] = ef_new_installs + abm_new_installs


# In[108]:


#CHANGE RECYCLING EFFICIENCIES TO MATCH JULIENS
regular_recovery_rate = pd.DataFrame() #recycling eff used in ABM for all scenarios except high material recovery that uses FRELP
regular_recovery_rate['mat'] = ['silver','copper','aluminium_frames','silicon','glass']
regular_recovery_rate['recovery_rate'] = [0,72,92,0,85]

regular_recovery_scenarios = [ABM_SCENARIOS[0]] + ABM_SCENARIOS[2:]
   
#Modify 'mat_EOL_Recycling_eff'
for mymaterial in MATERIALS: 
    past_recycling_eff = [r1.scenario['standard_PVICE'].material[mymaterial].materialdata['mat_EOL_Recycling_eff'][0]]*(2022-1995)
    new_recycling_eff = regular_recovery_rate[regular_recovery_rate.mat.isin([mymaterial])]['recovery_rate'].values.tolist()*(2050-2021)
    new_mat_EOL_recycling_eff = past_recycling_eff + new_recycling_eff
    for myscenario in regular_recovery_scenarios:
        r2.scenario[myscenario].material[mymaterial].materialdata['mat_EOL_Recycling_eff'] = new_mat_EOL_recycling_eff
    r2_better_lifetime.scenario['better_lifetime'].material[mymaterial].materialdata['mat_EOL_Recycling_eff'] = new_mat_EOL_recycling_eff


# In[109]:


r2.calculateMassFlow(weibullInputParams = weibull_IrenaRL)
r2_better_lifetime.calculateMassFlow()


# In[110]:


# create dataframe of results for WASTE only
USyearly_validation=pd.DataFrame()


# In[111]:


keyword='mat_Total_Landfilled'

for jj in range(0, len(r2.scenario)): # Loop over Scenarios
    case = list(r2.scenario.keys())[jj] # case gives scenario name
    if case == 'better_lifetime':
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = r2_better_lifetime.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly_validation["Waste_"+material+'_'+r2.name+'_'+case] = foo[material]
        filter_col = [col for col in USyearly_validation if (col.startswith('Waste') and col.endswith(r2.name+'_'+case)) ]
        USyearly_validation['Waste_Module_'+r2.name+'_'+case] = USyearly_validation[filter_col].sum(axis=1)
    else:
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = r2.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly_validation["Waste_"+material+'_'+r2.name+'_'+case] = foo[material]
        filter_col = [col for col in USyearly_validation if (col.startswith('Waste') and col.endswith(r2.name+'_'+case)) ]
        USyearly_validation['Waste_Module_'+r2.name+'_'+case] = USyearly_validation[filter_col].sum(axis=1)


# In[112]:


USyearly_validation = USyearly_validation/1000000  #Convert to metric tonnes
#907185 -- this is for US tons


# In[113]:


UScum_validation = USyearly_validation.copy()
UScum_validation = UScum_validation.cumsum()


# In[114]:


USyearly_validation.index = r1.scenario['standard_PVICE'].data['year']
UScum_validation.index = r1.scenario['standard_PVICE'].data['year']


# In[120]:


#Graphing Cumulative Waste
filter_col = [col for col in UScum_validation if (col.startswith('Waste_Module_ABM_Simulation2'))]
df = UScum_validation[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin(list(range(2020,2051)))]
df = df[df.variable.isin(pretty_scenarios[1:])]
fig1 = px.line(df, x='year', y='value', color = 'variable', labels={
                     "year": "Year",
                     "value": "Waste [metric tonnes]",
                    "variable" :"Scenario"
                 })
fig1.update_layout(#title_text='Simulation 2 Validation: Cumulative Waste', title_x=0.5,
                   height = 800, width = 1000)
fig1.update_layout(font=dict(size=25))
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig1.update_yaxes(range=[0,9000000])
fig1.show()


# In[116]:


#cumulative at 2050 results for Waste
filter_col = [col for col in UScum_validation if (col.startswith('Waste_Module_ABM_Simulation2'))]
df = UScum_validation[filter_col]
df = df.set_axis(pretty_scenarios, axis=1)
df['year'] = list(range(1995,2051))
df = df.melt(id_vars = 'year')
df = df[df.year.isin([2050])]
df = df[df.variable.isin(pretty_scenarios[1:])]
df['value'] = df['value']/1000000 #convert from metric tonnes to million metric tonnes
df.to_csv('s2_validation_cum_waste_results.csv')
cum_waste_validation = df.copy()


# In[117]:


#cum waste at 2050 comparison
cum_waste_validation = cum_waste_validation.rename(columns={"value": "S2 Cum Waste at 2050 with ABM New Installs"})
abm_waste_2050 = ABM_outputs_mass_cum[ABM_outputs_mass_cum.Year.isin([2050])]['Waste']/1000000
cum_waste_validation['ABM Cum Waste at 2050'] = list(abm_waste_2050.values)


# In[126]:


# graph cum waste at 2050 for PV ICE vs. ABM
fig = go.Figure()
fig.add_trace(go.Scatter(x=pretty_scenarios[1:], y=cum_waste_validation["S2 Cum Waste at 2050 with ABM New Installs"],
                    mode='markers',
                    name='PV ICE S2 with ABM New Installs <br> and Recovery Rates',
                        marker_color = 'black',
                        marker=dict(size=13))) 
fig.add_trace(go.Scatter(x=pretty_scenarios[1:], y=cum_waste_validation["ABM Cum Waste at 2050"],
                    mode='markers',
                    name='ABM (Landfilled + Stored)',
                        marker_color = 'red',
                         marker=dict(size=13))) 
    
fig.update_layout(#title_text='Cumulative Waste at 2050 Validation', title_x=0.5, 
                 xaxis_title="Year",
    yaxis_title="Waste [million metric tonnes]",
    legend_title="Scenario", height = 1000, width = 1000)
fig.update_layout(font=dict(size=22))
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig.show()


# In[ ]:




