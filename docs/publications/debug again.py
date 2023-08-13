#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'EnergyAnalysis'/'Sensitivity')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
altBaselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'Energy_CellModuleTechCompare')

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


timeshift = 2022-1995


# In[6]:


#load in a baseline and materials for modification
sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)

sim1.createScenario(name='PV_ICE', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim1.scenario['PV_ICE'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# In[7]:


sim1.createScenario(name='eff_high', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim1.scenario['eff_high'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
sim1.modifyScenario('eff_high', 'mod_eff', 
                    sim1.scenario['PV_ICE'].dataIn_m.loc[timeshift:,'mod_eff']+5, start_year=2022) #

#-------------------------------------------------------------------------------------------------------

sim1.createScenario(name='eff_high_bifi', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim1.scenario['eff_high_bifi'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
sim1.modifyScenario('eff_high_bifi', 'mod_eff', 
                    sim1.scenario['PV_ICE'].dataIn_m.loc[timeshift:,'mod_eff']+5, start_year=2022) #

#------------------------------------------------------------------------------------------------------

sim1.createScenario(name='eff_low', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim1.scenario['eff_low'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
sim1.modifyScenario('eff_low', 'mod_eff', 
                    sim1.scenario['PV_ICE'].dataIn_m.loc[timeshift:,'mod_eff']-5, start_year=2022) #


# In[ ]:





# In[8]:


sim1.calculateFlows()


# In[ ]:





# In[9]:


allenergy, energyGen, energy_demands = sim1.aggregateEnergyResults()


# In[ ]:





# In[ ]:





# scenarios = sim1.scenario.keys()

# allenergy = pd.DataFrame()
# energyGen = pd.DataFrame()
# energyFuel = pd.DataFrame()
# energyDemands = pd.DataFrame()
# energyDemands_all = pd.DataFrame()
# 
# for scen in scenarios:
#     energy_mod_scen = sim1.scenario[scen].dataOut_e.add_prefix(str(scen+'_')) #extract and label de module (10)
#     print(energy_mod_scen.columns)
#     
#     scenmatde = pd.DataFrame() #wipe and initialize material energy df
#     
#     for mat in MATERIALS:
#         energy_mat_scen = sim1.scenario[scen].material[mat].matdataOut_e.add_prefix(str(scen+'_'+mat+'_')) #extract and label de material
#         print(energy_mat_scen.columns)
#         scenmatde = pd.concat([scenmatde,energy_mat_scen], axis=1) #group all material de (84)
#     scende = pd.concat([energy_mod_scen,scenmatde], axis=1) #group single scenario de (module and materials) (94)
#     
#     scende_gen = scende.filter(like='e_out_annual')# create df of energy generation
#     scende_fuels = scende.filter(like='_fuel')# create df of fuel
#     
#     scende_filter1 = scende.loc[:,~scende.columns.isin(scende_gen.columns)] #select all columns that are NOT energy generation
#     scende_demands = scende_filter1.loc[:,~scende_filter1.columns.isin(scende_fuels.columns)] #select all columns that are NOT fuel (this avoids double counting)
#     colname = str(scen+'_e_demand_total') #create column name
#     scende_demands.loc[:,colname] = scende_demands.sum(axis=1) #sums module and material energy demands
#     
#     allenergy = pd.concat([allenergy, scende], axis=1) #collect all scenarios de (excludes demand sum)
#     energyDemands = pd.concat([energyDemands,scende_demands], axis=1) #collect energy demands (includes demand sum column)
#     energyGen = pd.concat([energyGen, scende_gen], axis=1) #collect all scenarios energy generation
#     energyFuel = pd.concat([energyFuel, scende_fuels], axis=1) #collect all scenarios fuel energy demands
#     energyDemands_all = pd.concat([energyDemands_all, scende_demands, scende_fuels])
# 
# #Fix the index to be years
# allenergy.index = sim1.scenario[scen].dataIn_e['year']

# In[20]:


allenergy.filter(like='demand_total')


# In[12]:


energyGen


# In[17]:


energy_demands.columns#.filter(like='demand_total')


# In[ ]:


scenarios


#     def aggregateEnergyResults(self, scenarios=None, materials=None):
#         if scenarios is None:
#             scenarios = list(self.scenario.keys())
#         else:
#             if isinstance(scenarios, str):
#                 scenarios = [scenarios]
# 
#         if materials is None:
#             materials = list(self.scenario[scenarios[0]].material.keys())
#         else:
#             if isinstance(materials, str):
#                 materials = [materials]
# 
# 
#         energy_demands_keys = [mfg_energies,mfg_recycle_energies_LQ,mfg_recycle_energies_HQ,use_energies,eol_energies,eol_remfg_energies,eol_recycle_energies_LQ,eol_recycle_energies_HQ]
#         energy_demands_flat = list(itertools.chain(*energy_demands_keys))
#         
#         
#         allenergy = pd.DataFrame()
#         energyGen = pd.DataFrame()
#         energyFuel = pd.DataFrame()
#         energy_mat = pd.DataFrame()
#         energy_demands = pd.DataFrame()
#         energy_mod = pd.DataFrame()
#         scenmatde = pd.DataFrame()
# 
#         for scen in scenarios:
#             # add the scen name as a prefix \
#             
#             energy_mod = self.scenario[scen].dataOut_e.add_prefix(str(scen+'_'))
#             #concat into one large df
#             #energy_mod = pd.concat([energy_mod, scende], axis=1)
#             
#             #material level energy
#             for mat in materials:
#                 # add the scen name as a prefix 
#                 
#                 energy_mat = self.scenario[scen].material[mat].matdataOut_e.add_prefix(str(scen+'_'+mat+'_'))
#                 scenmatde = pd.concat([scenmatde,energy_mat], axis=1)
#                 #concat into one large df
#                 #energy_mat = pd.concat([energy_mat, scenmatde], axis=1)
#             
#             #compile module and material energies into one df
#             allenergy_scen = pd.concat([energy_mod,scenmatde], axis=1) #df of mod and mat energy for scenario
#             
#             #select df to sum the total demand
#             energyGen_scen = allenergy_scen.filter(like='e_out_annual') #select all columns of energy generation
#             energyFuel_scen = allenergy_scen.filter(like='_fuel') #select all columns of fuel attributable
#             energy_demands_1 = allenergy_scen.loc[:,~allenergy_scen.columns.isin(energyGen_scen.columns)] #select all columns that are NOT energy generation, i.e. demands
#             energy_demands_scen = energy_demands_1.loc[:,~energy_demands_1.columns.isin(energyFuel_scen.columns)] #select all columns that are NOT fuel (this avoids double counting)
#             colname = str(scen+'_e_demand_total')
#             energy_demands_scen.loc[:,colname] = energy_demands_scen.sum(axis=1) 
#             
#             allenergy = pd.concat([allenergy,allenergy_scen], axis=1)
#             energyGen = pd.concat([energyGen,energyGen_scen], axis=1)
#             energyFuel = pd.concat([energyFuel,energyFuel_scen], axis=1)
#             energy_demands = pd.concat([energy_demands,energy_demands_scen], axis=1)
#         
#         
#         #Fix the index to be years
#         allenergy.index = self.scenario[scen].dataIn_e['year']
#         energyGen.index = self.scenario[scen].dataIn_e['year']
#         energyFuel.index = self.scenario[scen].dataIn_e['year']
#         energy_demands.index = self.scenario[scen].dataIn_e['year']
#                 
#         energy_demands = pd.concat([energy_demands,energyFuel], axis=1) #append fuel energy columns back onto energy demands
#                 
#         return allenergy, energyGen, energy_demands #note, all these are annual

# In[ ]:





# In[ ]:




