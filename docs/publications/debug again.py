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


mod_circ_vars = ['mod_EOL_pg4_recycled', 'mod_EOL_pb4_recycled']

mod_alt_paths = ['mod_EOL_pg0_resell','mod_EOL_pg1_landfill','mod_EOL_pg2_stored','mod_EOL_pg3_reMFG',
                 'mod_EOL_reMFG_yield','mod_EOL_sp_reMFG_recycle',
                 'mod_EOL_pb1_landfill','mod_EOL_pb2_stored','mod_EOL_pb3_reMFG']

mat_circ_vars = ['mat_MFG_scrap_Recycled', 'mat_MFG_scrap_Recycling_eff', 'mat_MFG_scrap_Recycled_into_HQ',
                 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG',
                 
                 'mat_PG4_Recycling_target', 'mat_Recycling_yield',
                 'mat_EOL_Recycled_into_HQ', 'mat_EOL_RecycledHQ_Reused4MFG']

#mat_mfgscrap = ['mat_MFG_scrap_Recycled', 'mat_MFG_scrap_Recycling_eff', 'mat_MFG_scrap_Recycled_into_HQ',
#                 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG']

#path control variables are:
# 'mat_PG4_Recycling_target'
# 'mat_MFG_scrap_Recycled'
# 'mod_EOL_pg4_recycled'


# In[8]:


sim1.createScenario(name='circ_high', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim1.scenario['circ_high'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
for var in range(0,len(mod_alt_paths)):
    sim1.modifyScenario('circ_high', mod_alt_paths[var], 0.0, start_year=2022) #set non recycle to 0   

sim1.modifyScenario('circ_high', 'mod_EOL_collection_eff',100.0, start_year=2022) #collect everything
    
for var in range(0,len(mod_circ_vars)):
    sim1.modifyScenario('circ_high', mod_circ_vars[var], 100.0, start_year=2022) #set recycle paths to 100%

for mat in range (0, len(MATERIALS)):
    for mvar in range(0,len(mat_circ_vars)):
        sim1.scenario['circ_high'].modifyMaterials(MATERIALS[mat], mat_circ_vars[mvar],100.0, start_year=2022) #
        sim1.scenario['circ_high'].modifyMaterials(MATERIALS[mat], 'mat_MFG_scrap_Recycled',100.0, start_year=2022) #


# In[9]:


sim1.createScenario(name='circ_mid', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim1.scenario['circ_mid'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
for var in range(0,len(mod_alt_paths)):
    sim1.modifyScenario('circ_mid', mod_alt_paths[var], 0.0, start_year=2022) #set non recycle to 0   

sim1.modifyScenario('circ_mid', 'mod_EOL_collection_eff',100.0, start_year=2022) #collect everything
sim1.modifyScenario('circ_mid','mod_EOL_pb1_landfill',100.0,start_year=2022) #landfill up just in case
sim1.modifyScenario('circ_mid','mod_EOL_pg1_landfill',100.0,start_year=2022)
    
for var in range(0,len(mod_circ_vars)):
    sim1.modifyScenario('circ_mid', mod_circ_vars[var], 25.0, start_year=2022) #set recycle paths to 25%

for mat in range (0, len(MATERIALS)):
    for mvar in range(0,len(mat_circ_vars)):
        sim1.scenario['circ_mid'].modifyMaterials(MATERIALS[mat], mat_circ_vars[mvar],100.0, start_year=2022) #
        sim1.scenario['circ_mid'].modifyMaterials(MATERIALS[mat], 'mat_MFG_scrap_Recycled',25.0, start_year=2022) #


# In[10]:


sim1.createScenario(name='circ_low', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim1.scenario['circ_low'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
#sim1.scenMod_noCircularity(scenarios='circ_low') #sets all years to 0
    
for var in range(0,len(mod_circ_vars)):
    sim1.modifyScenario('circ_low', mod_circ_vars[var],0.0, start_year=2022) #set recycle to 0
    
for var in range(0,len(mod_alt_paths)):
    sim1.modifyScenario('circ_low', mod_alt_paths[var], 0.0, start_year=2022) #set non recycle to 0   

sim1.modifyScenario('circ_low', 'mod_EOL_collection_eff',0.0, start_year=2022) #collect nothing

sim1.modifyScenario('circ_low','mod_EOL_pb1_landfill',100.0,start_year=2022) #landfill up just in case
sim1.modifyScenario('circ_low','mod_EOL_pg1_landfill',100.0,start_year=2022)

for mat in range (0, len(MATERIALS)):
    for mvar in range(0,len(mat_circ_vars)):
        sim1.scenario['circ_low'].modifyMaterials(MATERIALS[mat], mat_circ_vars[mvar],0.0, start_year=2022) #


# In[11]:


global_projection = pd.read_csv(os.path.join(supportMatfolder,'output-globalInstallsProjection.csv'), index_col=0)


# In[12]:


#trim to start in 2000, this trims module and materials
#had to specify and end year, cannot use to extend
sim1.trim_Years(startYear=2000, endYear=2100)


# In[13]:


#deployment projection for all scenarios
sim1.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', 
                    value= global_projection['World_annual_[MWdc]'], start_year=2000)


# In[ ]:





# In[14]:


sim1.calculateFlows()


# In[15]:



for row in range (0,len(sim1.scenario['PV_ICE'].dataIn_m)): #loop over length of years
    print(row)
    for scen in sim1.scenario.keys(): #loop over scenarios
        print(scen)
        Under_Installment = global_projection.iloc[row,0] - ((sim1.scenario[scen].dataOut_m['Effective_Capacity_[W]'][row])/1e6)  # MWATTS
        sim1.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][row] += Under_Installment #overwrite new installed
        #UnderInstall_df.loc[row,scen] = Under_Installment #save the underinstallment as df
        #calculate flows for that scenario with it's bifi factor and modified weibull
        sim1.calculateMassFlow(scenarios=[scen])#, bifacialityfactors=bifiPathDict[scen])

sim1.calculateEnergyFlow()


# In[16]:


cc_yearly, cc_cumu = sim1.aggregateResults() #have to do this to get auto plots


# In[17]:


allenergy, energyGen, energy_demands = sim1.aggregateEnergyResults()


# In[18]:


scennames_labels = sim1.scenario.keys()


# In[46]:


circ_high_p4 = sim1.scenario['circ_high'].dataOut_m['P4_recycled']
circ_mid_p4 = sim1.scenario['circ_mid'].dataOut_m['P4_recycled']
circ_mid_L0 = sim1.scenario['circ_mid'].dataOut_m['EOL_Landfill0']
circ_low_p4 = sim1.scenario['circ_low'].dataOut_m['P4_recycled']
circ_low_p0 = sim1.scenario['circ_low'].dataOut_m['EOL_Landfill0']


#plt.plot(circ_high_p4, label='high')
plt.plot(circ_mid_p4, label='mid')
plt.plot(circ_mid_L0, label='mid,Landfill0')
#plt.plot(circ_low_p4, label='low,P4')
#plt.plot(circ_low_p0, ls='--', label='low,Landfill0')
plt.legend()
plt.ylabel('Mass')


# In[20]:


sim1.scenario['circ_mid'].dataOut_m.filter(like='Landfill')


# In[21]:


circ_high_modcrushe = sim1.scenario['circ_high'].dataOut_e['mod_Recycle_Crush']
circ_mid_modcrushe = sim1.scenario['circ_mid'].dataOut_e['mod_Recycle_Crush']
circ_low_modcrushe = sim1.scenario['circ_low'].dataOut_e['mod_Recycle_Crush']


plt.plot(circ_high_modcrushe)
plt.plot(circ_mid_modcrushe)
plt.plot(circ_low_modcrushe)


# In[45]:


circ_high_matRHQ_e = sim1.scenario['circ_high'].material['glass'].matdataOut_e['mat_Recycled_HQ']
circ_mid_matRHQ_e = sim1.scenario['circ_mid'].material['glass'].matdataOut_e['mat_Recycled_HQ']
circ_low_matRHQ_e = sim1.scenario['circ_low'].material['glass'].matdataOut_e['mat_Recycled_HQ']

plt.plot(circ_high_matRHQ_e, label='high')
plt.plot(circ_mid_matRHQ_e, label='mid')
plt.plot(circ_low_matRHQ_e, label='low')
plt.legend()
plt.ylabel('HQ Recycling Energy [Wh]')


# In[23]:


plt.rcParams['figure.figsize'] = (12, 6)


# In[24]:


glass_mfgscrap_e = allenergy.filter(like='glass').filter(regex='MFGScrap_HQ$')
glass_mfgscrap_e.plot.bar()


# In[25]:


glass_virgin_e = allenergy.filter(like='glass').filter(regex='MFG_virgin$')


# In[26]:


glass_virgin_e.plot.bar()


# In[ ]:





# In[40]:


for scens in glass_virgin_e:
    plt.bar(glass_virgin_e.index, glass_virgin_e.loc[:,scens], label=scens)

plt.legend()


# In[ ]:





# In[ ]:





# In[24]:


e_annual_sumDemands = energy_demands.filter(like='demand_total')
e_annual_sumDemands_cumu = e_annual_sumDemands.cumsum()
cumu_e_demands = e_annual_sumDemands_cumu.loc[2100]
cumu_e_demands.index= scennames_labels

plt.bar(scennames_labels, cumu_e_demands/1e12)
plt.title('Cumulative Lifecycle Energy Demands')
plt.ylabel('Cumulative Energy Demands\n[TWh]')


# In[25]:


cumu_e_demands


# # SIMPLE GLASS ENERGY TEST

# In[27]:


MATERIAL = ['glass']#, 'silicon', 'silver', 'aluminium_frames', 'copper', 'encapsulant', 'backsheet']
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[28]:


density_glass = 2500*1000 # g/m^3 
glassperm2 = (2.5/1000)* 2 * density_glass


# In[29]:


#load in a baseline and materials for modification
sim2 = PV_ICE.Simulation(name='sim2', path=testfolder)

sim2.createScenario(name='PV_ICE', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIAL)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim2.scenario['PV_ICE'].addMaterial(MATERIAL[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
sim2.scenario['PV_ICE'].modifyMaterials('glass', 'mat_massperm2', glassperm2, start_year=2020)


# In[ ]:





# In[30]:


mod_circ_vars = ['mod_EOL_pg4_recycled', 'mod_EOL_pb4_recycled']

mod_alt_paths = ['mod_EOL_pg0_resell','mod_EOL_pg1_landfill','mod_EOL_pg2_stored','mod_EOL_pg3_reMFG',
                 'mod_EOL_reMFG_yield','mod_EOL_sp_reMFG_recycle',
                 'mod_EOL_pb1_landfill','mod_EOL_pb2_stored','mod_EOL_pb3_reMFG']

mat_circ_vars = ['mat_MFG_scrap_Recycled', 'mat_MFG_scrap_Recycling_eff', 'mat_MFG_scrap_Recycled_into_HQ',
                 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG',
                 
                 'mat_PG4_Recycling_target', 'mat_Recycling_yield',
                 'mat_EOL_Recycled_into_HQ', 'mat_EOL_RecycledHQ_Reused4MFG']

mat_mfgscrap = ['mat_MFG_scrap_Recycled', 'mat_MFG_scrap_Recycling_eff', 'mat_MFG_scrap_Recycled_into_HQ',
                 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG']

#path control variables are:
# 'mat_PG4_Recycling_target'
# 'mat_MFG_scrap_Recycled'
# 'mod_EOL_pg4_recycled'


# In[31]:


sim2.createScenario(name='nomfgscrap', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIAL)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim2.scenario['nomfgscrap'].addMaterial(MATERIAL[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
sim2.scenario['nomfgscrap'].modifyMaterials('glass', 'mat_massperm2', glassperm2, start_year=2020)

#sim2.modifyScenario(scenname, 'mod_EOL_collection_eff',100.0, start_year=2022) #

for var in range(0,len(mod_circ_vars)):
    sim2.modifyScenario('nomfgscrap', mod_circ_vars[var], 0.0, start_year=2020) #set EoL recycle to 0
    
for var in range(0,len(mod_alt_paths)):
    sim2.modifyScenario('nomfgscrap', mod_alt_paths[var], 0.0, start_year=2020) #set non recycle to 0
    
for var in range(0,len(mat_circ_vars)):
    sim2.modifyScenario('nomfgscrap', mat_circ_vars[var], 0.0, start_year=2020) #set mat recycle to 0


# In[32]:


sim2.createScenario(name='lqmfgscrap', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIAL)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim2.scenario['lqmfgscrap'].addMaterial(MATERIAL[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
sim2.scenario['lqmfgscrap'].modifyMaterials('glass', 'mat_massperm2', glassperm2)

#sim2.modifyScenario(scenname, 'mod_EOL_collection_eff',100.0, start_year=2022) #

for var in range(0,len(mod_circ_vars)):
    sim2.modifyScenario('lqmfgscrap', mod_circ_vars[var], 0.0, start_year=2020) #set EoL recycle to 0
    
for var in range(0,len(mod_alt_paths)):
    sim2.modifyScenario('lqmfgscrap', mod_alt_paths[var], 0.0, start_year=2020) #set non recycle EoL to 0
    
for var in range(0,len(mat_circ_vars)):
    sim2.modifyScenario('lqmfgscrap', mat_circ_vars[var], 0.0, start_year=2020) #set mat recycle to 0

sim2.modifyScenario('lqmfgscrap', 'mat_MFG_scrap_Recycled', 100.0, start_year=2020) # recycle all mfgscrap
sim2.modifyScenario('lqmfgscrap', 'mat_MFG_scrap_Recycling_eff', 100.0, start_year=2020) # 100 yield
sim2.modifyScenario('lqmfgscrap', 'mat_MFG_scrap_Recycled_into_HQ', 0.0, start_year=2020) # all LQ
sim2.modifyScenario('lqmfgscrap', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 0.0, start_year=2020) # all LQ


# In[33]:


sim2.createScenario(name='CLHQmfgscrap', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIAL)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim2.scenario['CLHQmfgscrap'].addMaterial(MATERIAL[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
sim2.scenario['CLHQmfgscrap'].modifyMaterials('glass', 'mat_massperm2', glassperm2)

#sim2.modifyScenario(scenname, 'mod_EOL_collection_eff',100.0, start_year=2022) #

for var in range(0,len(mod_circ_vars)):
    sim2.modifyScenario('CLHQmfgscrap', mod_circ_vars[var], 0.0, start_year=2020) #set EoL recycle to 0
    
for var in range(0,len(mod_alt_paths)):
    sim2.modifyScenario('CLHQmfgscrap', mod_alt_paths[var], 0.0, start_year=2020) #set non recycle EoL to 0
    
for var in range(0,len(mat_circ_vars)):
    sim2.modifyScenario('CLHQmfgscrap', mat_circ_vars[var], 0.0, start_year=2020) #set mat recycle to 0

sim2.modifyScenario('CLHQmfgscrap', 'mat_MFG_scrap_Recycled', 100.0, start_year=2020) # recycle all mfgscrap
sim2.modifyScenario('CLHQmfgscrap', 'mat_MFG_scrap_Recycling_eff', 100.0, start_year=2020) # 100 yield
sim2.modifyScenario('CLHQmfgscrap', 'mat_MFG_scrap_Recycled_into_HQ', 100.0, start_year=2020) # all HQ
sim2.modifyScenario('CLHQmfgscrap', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0, start_year=2020) # all CL


# In[34]:


sim2.createScenario(name='OLHQmfgscrap', massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
for mat in range (0, len(MATERIAL)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
    matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
    sim2.scenario['OLHQmfgscrap'].addMaterial(MATERIAL[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)
    
sim2.scenario['OLHQmfgscrap'].modifyMaterials('glass', 'mat_massperm2', glassperm2)

#sim2.modifyScenario(scenname, 'mod_EOL_collection_eff',100.0, start_year=2022) #

for var in range(0,len(mod_circ_vars)):
    sim2.modifyScenario('OLHQmfgscrap', mod_circ_vars[var], 0.0, start_year=2020) #set EoL recycle to 0
    
for var in range(0,len(mod_alt_paths)):
    sim2.modifyScenario('OLHQmfgscrap', mod_alt_paths[var], 0.0, start_year=2020) #set non recycle EoL to 0
    
for var in range(0,len(mat_circ_vars)):
    sim2.modifyScenario('OLHQmfgscrap', mat_circ_vars[var], 0.0, start_year=2020) #set mat recycle to 0

sim2.modifyScenario('OLHQmfgscrap', 'mat_MFG_scrap_Recycled', 100.0, start_year=2020) # recycle all mfgscrap
sim2.modifyScenario('OLHQmfgscrap', 'mat_MFG_scrap_Recycling_eff', 100.0, start_year=2020) # 100 yield
sim2.modifyScenario('OLHQmfgscrap', 'mat_MFG_scrap_Recycled_into_HQ', 100.0, start_year=2020) # all HQ
sim2.modifyScenario('OLHQmfgscrap', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 0.0, start_year=2020) # all OL


# In[35]:


sim2.trim_Years(startYear=2020, endYear=2050)


# In[36]:


#identical deploy 10 MW
sim2.modifyScenario(scenarios=None,stage='new_Installed_Capacity_[MW]', value= 10.0, start_year=2020)


# In[37]:


sim2.calculateFlows()


# In[38]:


cc_yearly2, cc_cumu2 = sim2.aggregateResults()
allenergy2, energyGen2, energy_demands2 = sim2.aggregateEnergyResults()


# In[39]:


sim2.scenario['lqmfgscrap'].dataIn_m


# In[40]:


glass_mfgvirgin_e = allenergy2.filter(like='glass').filter(regex='MFG_virgin$')
plt.plot(glass_mfgvirgin_e)
plt.legend(glass_mfgvirgin_e.columns)


# In[41]:


allenergy2.filter(like='glass').filter(regex='MFGScrap')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




