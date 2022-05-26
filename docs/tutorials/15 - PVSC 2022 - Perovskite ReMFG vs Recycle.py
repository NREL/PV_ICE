#!/usr/bin/env python
# coding: utf-8

# # PVSC 2022 Perovskite ReMFG vs Recycling: a mass and energy analysis

# This journal documents the analysis conducted for PVSC 2022 Mirletz et al conference presentation. It constitutes an initial demonstration of the energy flows of the PV ICE tool.
# 
# The comparison will be between a 100% remanfactured module and a 100% recycled module.

# In[1]:


import os
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP'/'PVSC2022-Eflows')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[2]:


PV_ICE.__version__


# ## Add Scenarios and Materials
# 
# We wil create 3 scenarios:
# 1. baseline linear economy for glass-glass module
# 2. 100% reMFG the glass
# 3. 100% recycle the glass
# 
# These three scenarios will have the following assumptions:
# 
# 0. All Scenarios
#     - no circularity in MFG scrap
# 1. Linear economy
#     - no reMFG or recycling
# 2. 100% ReMFG
#     - all EoL goes to reMFG, no recycling
#     - yields are: 99%
# 3. 100% Recycle LQ
#    - all EoL goes to recycling, mix open and closed-loop
#    - yields are: 40%*15%
# 4. 100% Recycle HQ
#    - all EOL goes to recycling closed-loop
#    - yields are 99%

# In[3]:


cwd=os.getcwd()
print(os.getcwd())


# In[4]:


MATERIALS = ['glass']#,'aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
MATERIAL = MATERIALS[0]
#moduleFile_recycle = r'..\..\baselines\perovskite_modules_US_recycle.csv'
#moduleFile_reMFG = r'..\..\baselines\perovskite_modules_US_reMFG.csv'
moduleFile= r'..\..\baselines\perovskite_modules_US_linear.csv'


# In[5]:


r1 = PV_ICE.Simulation(name='perovskite_energies', path=testfolder)

scenarios = ['perovskite_linear', 'perovskite_reMFG', 'perovskite_recycle', 'perovskite_recycle_perfect']

for scen in scenarios: 

    r1.createScenario(name=scen, file=moduleFile)
    for mat in range (0, len(MATERIALS)):
        MATERIALBASELINE = r'..\..\baselines\perovskite_material_'+MATERIALS[mat]+'.csv'
        r1.scenario[scen].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)


# ### Modify the scenarios to match assumptions

# In[6]:


r1.scenario['perovskite_linear'].data.keys()


# In[7]:


r1.scenario['perovskite_linear'].material['glass'].materialdata.keys()


# In[8]:


#linear
r1.modifyScenario('perovskite_linear', 'mod_Repair', 0.0) #this removes all weibull failures from field immediately
r1.modifyScenario('perovskite_linear', 'mod_MerchantTail', 0.0) # this prevents extended use
r1.modifyScenario('perovskite_linear', 'mod_EOL_collection_eff', 0.0) #this sends everytyhing to landfill


# In[9]:


#reMFG
#Module
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_collection_eff', 100.0) #this collects everything
    #path good
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_pg0_resell', 0.0) #
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_pg1_landfill', 0.0) #
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_pg2_stored', 0.0) #

r1.modifyScenario('perovskite_reMFG', 'mod_EOL_pg3_reMFG', 100.0) #send all to remfg
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_reMFG_yield', 100.0) #100% yield of remfg

r1.modifyScenario('perovskite_reMFG', 'mod_EOL_pg4_recycled', 0.0) #
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_sp_reMFG_recycle', 0.0) #
    #path bad
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_pb1_landfill', 0.0) #
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_pb2_stored', 0.0) #
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_pb3_reMFG', 100.0) #sends all "bad" modules to remfg, uses same yield above
r1.modifyScenario('perovskite_reMFG', 'mod_EOL_pb4_recycled', 0.0) #

#material
r1.scenario['perovskite_reMFG'].modifyMaterials('glass', 'mat_PG3_ReMFG_target', 100.0) #send all to remfg
r1.scenario['perovskite_reMFG'].modifyMaterials('glass', 'mat_PG4_Recycling_target', 0.0) #send none to recycle
r1.scenario['perovskite_reMFG'].modifyMaterials('glass', 'mat_ReMFG_yield', 99.0) #already set to 99, in case change


# In[10]:


#recycle
#module
r1.modifyScenario('perovskite_recycle', 'mod_EOL_collection_eff', 100.0) #this collects everything
    #path good
r1.modifyScenario('perovskite_recycle', 'mod_EOL_pg0_resell', 0.0) #
r1.modifyScenario('perovskite_recycle', 'mod_EOL_pg1_landfill', 0.0) #
r1.modifyScenario('perovskite_recycle', 'mod_EOL_pg2_stored', 0.0) #
r1.modifyScenario('perovskite_recycle', 'mod_EOL_pg3_reMFG', 0.0) #
r1.modifyScenario('perovskite_recycle', 'mod_EOL_reMFG_yield', 0.0) #

r1.modifyScenario('perovskite_recycle', 'mod_EOL_pg4_recycled', 100.0) #send all to recycle
r1.modifyScenario('perovskite_recycle', 'mod_EOL_sp_reMFG_recycle', 0.0) #
    #path bad
r1.modifyScenario('perovskite_recycle', 'mod_EOL_pb1_landfill', 0.0) #
r1.modifyScenario('perovskite_recycle', 'mod_EOL_pb2_stored', 0.0) #
r1.modifyScenario('perovskite_recycle', 'mod_EOL_pb3_reMFG', 0.0) #
r1.modifyScenario('perovskite_recycle', 'mod_EOL_pb4_recycled', 100.0) #send all to recycle

#material
r1.scenario['perovskite_recycle'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled', 100.0) #send all mfg scrap to recycle
r1.scenario['perovskite_recycle'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0) #all hq closed-loop
r1.scenario['perovskite_recycle'].modifyMaterials('glass', 'mat_PG3_ReMFG_target', 0.0) #send none to remfg
r1.scenario['perovskite_recycle'].modifyMaterials('glass', 'mat_PG4_Recycling_target', 100.0) #send all to recycle
r1.scenario['perovskite_recycle'].modifyMaterials('glass', 'mat_EOL_RecycledHQ_Reused4MFG', 100.0) #closed-loop
r1.scenario['perovskite_recycle'].modifyMaterials('glass', 'mat_EOL_Recycled_into_HQ', 15.0) #HQ??
r1.scenario['perovskite_recycle'].modifyMaterials('glass', 'mat_Recycling_yield', 40.0) #yield??


# In[11]:


#recycle_perfect
#module
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_collection_eff', 100.0) #this collects everything
    #path good
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_pg0_resell', 0.0) #
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_pg1_landfill', 0.0) #
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_pg2_stored', 0.0) #
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_pg3_reMFG', 0.0) #
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_reMFG_yield', 0.0) #

r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_pg4_recycled', 100.0) #send all to recycle
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_sp_reMFG_recycle', 0.0) #
    #path bad
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_pb1_landfill', 0.0) #
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_pb2_stored', 0.0) #
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_pb3_reMFG', 0.0) #
r1.modifyScenario('perovskite_recycle_perfect', 'mod_EOL_pb4_recycled', 100.0) #send all to recycle

#material
r1.scenario['perovskite_recycle_perfect'].modifyMaterials('glass', 'mat_MFG_scrap_Recycling_eff', 99.0) #send all mfg scrap to recycle
r1.scenario['perovskite_recycle_perfect'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ', 100.0) #send all mfg scrap to recycle
r1.scenario['perovskite_recycle_perfect'].modifyMaterials('glass', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG', 100.0) #send all mfg scrap to recycle

r1.scenario['perovskite_recycle_perfect'].modifyMaterials('glass', 'mat_PG3_ReMFG_target', 0.0) #send none to remfg
r1.scenario['perovskite_recycle_perfect'].modifyMaterials('glass', 'mat_PG4_Recycling_target', 100.0) #send all to recycle
r1.scenario['perovskite_recycle_perfect'].modifyMaterials('glass', 'mat_Recycling_yield', 99.0) #yield
r1.scenario['perovskite_recycle_perfect'].modifyMaterials('glass', 'mat_EOL_Recycled_into_HQ', 100.0) #HQ
r1.scenario['perovskite_recycle_perfect'].modifyMaterials('glass', 'mat_EOL_RecycledHQ_Reused4MFG', 100.0) #closed-loop


# In[12]:


r1.scenario['perovskite_recycle'].material['glass'].materialdata.keys()


# ## Run the Mass Flow Calculations on All Scenarios and Materials

# In[13]:


r1.calculateMassFlow()


# In[14]:


r1.plotScenariosComparison('Installed_Capacity_[W]')


# In[15]:


r1.plotScenariosComparison('Yearly_Sum_Power_disposed')


# In[16]:


mass_agg_yearly, mass_agg_sums = r1.aggregateResults()


# # Energy Flows
# 
# First read in the energy files. Point at a path, then use the PV ICE colde to handle the meta data. Energy values for modules are in kWh/m2 and for materials are in kWh/kg. To ensure unit matching, we will divide the input by 1000 to convert kg to g.

# In[17]:


matEfile_glass = str(Path().resolve().parent.parent / 'baselines'/'perovskite_energy_material_glass.csv')

modEfile = str(Path().resolve().parent.parent / 'baselines'/'perovskite_energy_modules.csv')


# In[18]:


# Material energy file
file = matEfile_glass
csvdata = open(str(file), 'r', encoding="UTF-8")
csvdata = open(str(file), 'r', encoding="UTF-8-sig")
firstline = csvdata.readline()
secondline = csvdata.readline()

head = firstline.rstrip('\n').split(",")
meta = dict(zip(head, secondline.rstrip('\n').split(",")))

data = pd.read_csv(csvdata, names=head)
data.loc[:, data.columns != 'year'] = data.loc[:, data.columns != 'year'].astype(float)/1000 
#Divide by 1000 go get kg to g
# THIS IS A TEMP FIX
matEfile_glass_simple = data.copy()


# In[19]:


#module energy file
file = modEfile
csvdata = open(str(file), 'r', encoding="UTF-8")
csvdata = open(str(file), 'r', encoding="UTF-8-sig")
firstline = csvdata.readline()
secondline = csvdata.readline()

head = firstline.rstrip('\n').split(",")
meta = dict(zip(head, secondline.rstrip('\n').split(",")))

data = pd.read_csv(csvdata, names=head)
data.loc[:, data.columns != 'year'] = data.loc[:, data.columns != 'year'].astype(float)
modEfile_simple = data.copy()


# Now run the energy calculation. Currently this is not a class, just a function that will return a dataframe. Each scenario will need to be run seperately, and read in the perovskite energy files. The results are like the aggregate mass results function in that an annual and a cumulative dataframe are returned.

# In[20]:


r1_e_linear, r1_e_linear_cum = r1.calculateEnergyFlow(scenarios='perovskite_linear', materials='glass', modEnergy=modEfile_simple, matEnergy=matEfile_glass_simple)
r1_e_reMFG, r1_e_reMFG_cum = r1.calculateEnergyFlow(scenarios='perovskite_reMFG', materials='glass', modEnergy=modEfile_simple, matEnergy=matEfile_glass_simple)
r1_e_reCYCLE, r1_e_reCYCLE_cum = r1.calculateEnergyFlow(scenarios='perovskite_recycle', materials='glass', modEnergy=modEfile_simple, matEnergy=matEfile_glass_simple)
r1_e_reCYCLE_perfs, r1_e_reCYCLE_perfs_cum = r1.calculateEnergyFlow(scenarios='perovskite_recycle_perfect', materials='glass', modEnergy=modEfile_simple, matEnergy=matEfile_glass_simple)


# # Energy Analysis

# In[21]:


r1_e_linear.index = modEfile_simple['year']
r1_e_reMFG.index = modEfile_simple['year']
r1_e_reCYCLE.index = modEfile_simple['year']
r1_e_reCYCLE_perfs.index = modEfile_simple['year']


# In[22]:


r1_e_linear.keys()


# In[23]:


for key in r1_e_linear.keys():
    plt.plot(r1_e_linear.index, r1_e_linear[key], marker='s', ms=12, label='linear')
    plt.plot(r1_e_reMFG.index, r1_e_reMFG[key], marker='^', ms=12, label='reMFG')
    plt.plot(r1_e_reCYCLE.index, r1_e_reCYCLE[key], marker='o',ms=10, label='reCYCLE')
    plt.plot(r1_e_reCYCLE_perfs.index, r1_e_reCYCLE_perfs[key], marker='X', color='purple', label='reCYCLE_perfect')
    plt.legend()
    plt.title(str(key))
    plt.show()


# The negative values are a product of the 15 year lifetime, and suddenly providing more material than necessary in a mfging year. Ideally, we would address this through storage for next year offsetting - to be developed. These negative values can be exacerbated by deployment curves.

# ### E_in

# In[24]:


energy_annual = pd.concat([r1_e_linear, r1_e_reMFG, r1_e_reCYCLE, r1_e_reCYCLE_perfs], axis=1, 
                          keys=['perovskite_linear', 'perovskite_reMFG', 'perovskite_recycle', 'perovskite_recycle_perfect'])
#this is a multiindex column, and filter doesn't work with it
energy_annual.to_csv('energyyearly_flatdeploy.csv')

energy_sums = pd.concat([r1_e_linear_cum, r1_e_reMFG_cum, r1_e_reCYCLE_cum, r1_e_reCYCLE_perfs_cum], axis=1)
energy_sums.to_csv('energysums_flatdeploy.csv')


# In[25]:


#categorize the energy in values into lifecycle stages
mfg_energies = ['mod_MFG','mat_extraction','mat_MFG_virgin']
mfg_recycle_energies_LQ = ['mat_MFGScrap_LQ'] #LQ and HQ are separate becuase LQ is only LQ
mfg_recycle_energies_HQ = ['mat_MFGScrap_HQ'] #and HQ material is E_LQ + E_HQ
use_energies = ['mod_install','mod_OandM','mod_Repair']
eol_energies = ['mat_landfill','mod_Demount','mod_Store','mod_Resell_Certify']
eol_remfg_energies = ['mod_ReMFG_Disassmbly','mat_EoL_ReMFG_clean']
eol_recycle_energies_LQ = ['mod_Recycle_Crush','mat_Recycled_LQ']
eol_recycle_energies_HQ = ['mod_Recycle_Crush','mat_Recycled_HQ']


# In[26]:


#example filtering
energy_sums.filter(items=mfg_energies, axis=0).filter(regex='recycle$')


# In[27]:


#energy in for the linear system (includes LQ and HQ recycling, which might not be right)
e_in_mfg_linear = energy_sums.filter(items=mfg_energies, axis=0).filter(like='linear').sum()
e_in_use_linear = energy_sums.filter(items=use_energies, axis=0).filter(like='linear').sum()
e_in_eol_linear = energy_sums.filter(items=eol_energies, axis=0).filter(like='linear').sum()

e_in_linear_tab = pd.concat([e_in_mfg_linear,e_in_use_linear,e_in_eol_linear], axis=1)
e_in_linear_tab.columns = ['mfg','use','eol']

e_in_linear = e_in_mfg_linear + e_in_use_linear + e_in_eol_linear
print('Energy_in for the linear perovskite is ' + str(round(e_in_linear[0],2)) + ' kWh.')


# In[28]:


#energy in for reMFG
e_in_mfg_remfg = energy_sums.filter(items=mfg_energies, axis=0).filter(like='reMFG').sum()
e_in_use_remfg = energy_sums.filter(items=use_energies, axis=0).filter(like='reMFG').sum()
e_in_eol_remfg = energy_sums.filter(items=eol_energies, axis=0).filter(like='reMFG').sum()
e_in_remfg_remfg = energy_sums.filter(items=eol_remfg_energies, axis=0).filter(like='reMFG').sum()

e_in_remfg_tab = pd.concat([e_in_mfg_remfg, e_in_use_remfg, e_in_eol_remfg, e_in_remfg_remfg], axis=1)
e_in_remfg_tab.columns = ['mfg','use','eol','remfg']

e_in_remfg = e_in_mfg_remfg + e_in_use_remfg + e_in_eol_remfg + e_in_remfg_remfg
print('Energy_in for the remanufactured perovskite is ' + str(round(e_in_remfg[0],2)) +' kWh.')


# In[29]:


#energy in for recycle
e_in_mfg_recycle = energy_sums.filter(items=mfg_energies, axis=0).filter(regex='recycle$').sum()
e_in_mfgscrap_recycle = energy_sums.filter(items=mfg_recycle_energies_LQ, axis=0).filter(regex='recycle$').sum()
e_in_use_recycle = energy_sums.filter(items=use_energies, axis=0).filter(regex='recycle$').sum()
e_in_eol_recycle = energy_sums.filter(items=eol_energies, axis=0).filter(regex='recycle$').sum()
e_in_recycle_recycle = energy_sums.filter(items=eol_recycle_energies_LQ, axis=0).filter(regex='recycle$').sum()

e_in_recycle_tab = pd.concat([e_in_mfg_recycle, e_in_mfgscrap_recycle, e_in_use_recycle,
                              e_in_eol_recycle, e_in_recycle_recycle], axis=1)
e_in_recycle_tab.columns = ['mfg','mfgscrap','use','eol','eolrecycle']

e_in_recycle = e_in_mfg_recycle + e_in_mfgscrap_recycle + e_in_use_recycle + e_in_eol_recycle + e_in_recycle_recycle
print('Energy_in for recycled perovkiste is ' + str(round(e_in_recycle[0],2)) +' kWh.')


# In[30]:


#energy in for recycle_perfect
e_in_mfg_recycle_p = energy_sums.filter(items=mfg_energies, axis=0).filter(like='recycle_perfect').sum()
e_in_mfgscrap_recycle_p = energy_sums.filter(items=mfg_recycle_energies_HQ, axis=0).filter(like='recycle_perfect').sum()
e_in_use_recycle_p = energy_sums.filter(items=use_energies, axis=0).filter(like='recycle_perfect').sum()
e_in_eol_recycle_p = energy_sums.filter(items=eol_energies, axis=0).filter(like='recycle_perfect').sum()
e_in_recycle_recycle_p = energy_sums.filter(items=eol_recycle_energies_HQ, axis=0).filter(like='recycle_perfect').sum()

e_in_recycle_p_tab = pd.concat([e_in_mfg_recycle_p, e_in_mfgscrap_recycle_p, e_in_use_recycle_p,
                                e_in_eol_recycle_p, e_in_recycle_recycle_p], axis=1)
e_in_recycle_p_tab.columns = ['mfg','mfgscrap','use','eol','eolrecycle']

e_in_recycle_p = e_in_mfg_recycle_p + e_in_mfgscrap_recycle_p + e_in_use_recycle_p + e_in_eol_recycle_p + e_in_recycle_recycle_p
print('Energy_in for the perfect recycled perovkiste is ' + str(round(e_in_recycle_p[0],2)) +' kWh.')


# In[31]:


e_in_cat_tab = pd.concat([e_in_linear_tab, e_in_remfg_tab, e_in_recycle_tab, e_in_recycle_p_tab] )
e_in_cat_tab.to_csv('energy_in_by_category.csv') 


# In[32]:


e_in = pd.DataFrame(pd.concat([e_in_linear, e_in_remfg, e_in_recycle, e_in_recycle_p]), columns=['E_in_MWh'])
e_in/e_in.iloc[0]


# ### E_out
# Create an approximation of energy generated each year using hours of sunlight per year

# In[89]:


#Generation = Insolation * Power/Irradience * time
# We are assuming Insolation = 5 kWh/m2-day
active_capacity = mass_agg_yearly.filter(like='ActiveCapacity').filter(like='linear') #MW
active_capacity_W = active_capacity*1e6 # MW to W
active_Wh = (active_capacity_W/1000)*5000*365 # divide by irradience * insolation * time
#OR do this using a kWh/Kw factor from somewhere like ATB
e_out = active_Wh.sum() #lifecycle cumulative energy generated by all cohorts
print('Cumulative lifetime energy from all cohorts (accounting for degradation) is '+
     str(round(e_out[0],2)/1e6) + ' MWh.')


# In[90]:


#Compare to new e_out calc
e_out_annu_linear = r1_e_linear.filter(like='e_out')
e_out_annu_remfg = r1_e_reMFG.filter(like='e_out')
e_out_annu_recycle = r1_e_reCYCLE.filter(like='e_out')
e_out_annu_recycle_p = r1_e_reCYCLE_perfs.filter(like='e_out')

plt.plot(e_out_annu_linear, label='linear')
plt.plot(e_out_annu_remfg, label='remfg')
plt.plot(e_out_annu_recycle, label='recycle')
plt.plot(e_out_annu_recycle_p, label='recycle_p')
#sanity check they are all the same


# In[91]:


print(r1_e_linear_cum['perovskite_linear']['e_out_annual_[Wh]'])
e_out[0]


# ## EROI

# In[35]:


#EROI = Eout/Ein (note this is not a true eroi because it is missing embedded energy of process materials)
eroi = e_out[0]/e_in
eroi.columns = ['EROI']
eroi


# In[ ]:





# In[36]:


plt.plot(active_kWh, label = 'Energy generated [Wh]')
plt.plot(energy_annual['perovskite_linear']['mod_MFG'], label='perovskite_linear mod mfg [kWh]')
plt.plot(energy_annual['perovskite_reMFG']['mod_MFG'], label='perovskite_reMFG mod mfg [kWh]')
plt.plot(energy_annual['perovskite_recycle_perfect']['mod_MFG'], label='perovskite_recycle mod mfg [kWh]')
plt.legend()


# In[37]:


plt.plot(active_kWh, label = 'Energy generated [kWh]')
plt.plot(energy_annual['perovskite_linear']['mat_MFG_virgin'], label='perovskite_linear mod mfg [kWh]')
plt.plot(energy_annual['perovskite_reMFG']['mat_MFG_virgin'], label='perovskite_reMFG mod mfg [kWh]')
plt.plot(energy_annual['perovskite_recycle']['mat_MFG_virgin'], label='perovskite_recycle mod mfg [kWh]')
plt.plot(energy_annual['perovskite_recycle_perfect']['mat_MFG_virgin'], label='perovskite_recycle mod mfg [kWh]')
plt.legend()


# # Calculations for file prep (module and glass)
# 
# ### Module
# We are doing a case study comparing recycling versus remanufacturing the glass for a perovskite module. The assumption is that the perovskite module lasts for 15 years, with weibull parameters that fail 10% of the modules before year 15, and a power degradation such that the module is at 80% of nameplate power at year 15. See the Lifetime vs Recycling journal for calculation of weibull parameters and degradation rates.
# 
# ### Glass
# The assumption is that a perovskite module will be a glass-glass package. Modern c-Si glass-glass (35% marketshare) bifacial modules (27% marketshare) are most likely 2.5mm front glass (28% marketshare) and 2.5 mm back glass (95% marketshare) [ITRPV 2022]. Therefore, we will assume a perovskite glass glass module will use 2 sheets of glass that are 2.5 mm thick.
# 

# In[38]:


density_glass = 2500*1000 # g/m^3    
glass_thickness = 2.5/1e3 #m
mass_glass = 2*glass_thickness*density_glass
print('The mass of glass per module area for a perovskite glass-glass package is assumed to be '+
     str(mass_glass) + ' g/m^2.')


# ## Energy flows (module and glass)
# 
# ### Module
# We will assume that a perovskite module is disassemble-able or openable with either a laser applied to a vacuum edge seal OR with a hot knife. Laser edge seal can be done with a 16 W laser. 
# 
# The hot knife procedure with EVA heats the blade to 300 C (https://www.npcgroup.net/eng/solarpower/reuse-recycle/dismantling#comp) and is currently only used on glass-backsheet modules. The NPC website indicates that cycle time is 60 seconds for one 6x10 cell module. Small commercially availble hot knives can achieve greater than 300C drawing less than 150W. We will assume worst case scenario; hot knife for 60 seconds at 150 W

# In[39]:


e_hotknife_tot = 150*60*(1/3600)*(1/1000) # 150 W * 60 s = W*s *(hr/s)*(kW/W)
area_mod = 1.090*2.100 #m
e_hotknife = e_hotknife_tot/area_mod # E/module to E/m2
print('Energy for hot knife separation is '+ str(round(e_hotknife, 4))+' kWh/m2. This will be used as energy of module reMFG Disassembly')


# ### Glass
# The process to remove the perovskite from the glass is relatively simple regardless of architecture (all back contact or stack). A dunk in a water-based solvent at room temperature can remove the perovskite layer, and simple heating/baking or UV+Ozone steps should round out the cleaning preparation for a new perovskite deposition. 
# 
# Using Rodriguez-Garcia G, Aydin E, De Wolf S, Carlson B, Kellar J, Celik I. Life Cycle Assessment of Coated-Glass Recovery from Perovskite Solar Cells. ACS Sustainable Chem Eng [Internet]. 2021 Nov 3 [cited 2021 Nov 8]; Available from: https://doi.org/10.1021/acssuschemeng.1c05029, we will assume a room temperature water bath with sonication, a heating/drying/baking step, and a UV+Ozone step.
# 

# In[40]:


e_sonicate = 4  #kWh/m2 ultrasonication
e_uvozone = 3.57  #kWh/m2 ozone+UV
e_bake = 0.06  #kWh/m2 hot plate drying
e_glassreMFG_area = e_sonicate+e_uvozone+e_bake
e_glass_reMFG_mass = e_glassreMFG_area/(mass_glass/1000) #kWh/m2 *m2/g

print('Energy to remanufacture the glass (material energy only) is ' + str(round(e_glass_reMFG_mass, 2)) + 'kWh/kg')


# ## Modify Solar Futures Deployment Curve
# 
# ReEDS deployment curve for solar futures is a complex deployment, which will obfuscate the results of our energy flows. To mitage that, we will develop an exponential decay deployment curve to meet the targets as layed out by Solar Futures, namely, 1.6 TW in 2050. If we can also hit 1.0 TW in 2035, that is bonus

# In[ ]:





# In[41]:


# Import curve fitting package from scipy
from scipy.optimize import curve_fit
# Function to calculate the power-law with constants a and b
def power_law(x, a, b):
    return a*np.power(x, b)


# In[42]:


#generate a dataset for deployment between 2023 and 2050
deployed_2022 =  100000# y value in MW of already deployed PV
x_vals = pd.Series(range(2021,2051)) # x values

#exponential decay function
y_dummy = power_law(x_vals-2021, deployed_2022, 0.85) 
#play around with the exponential until y_dummy[31] hits 1.7 TW (DC)

print(str(y_dummy[14]/1e6) + ' TW in 2035')
print(str(y_dummy[29]/1e6) + ' TW in 2050')
plt.plot(y_dummy)


# In[43]:


#dataframe the cumulative deployements
deployments = pd.DataFrame()
deployments['CumulativeDeploy[MW]'] = y_dummy
deployments.index = x_vals


# In[44]:


#take the annual difference to de-cumulate
deployments['AnnualDeploy[MW]'] = deployments['CumulativeDeploy[MW]']-deployments['CumulativeDeploy[MW]'].shift(1).fillna(0)
plt.plot(deployments)
plt.legend(deployments.columns)


# In[45]:


plt.plot(deployments['AnnualDeploy[MW]'])
plt.title('Annual Deployments Meeting 1.7 TW in 2050')
plt.ylabel('Annual Deploy [MW]')


# In[46]:


reversedeploy = deployments['AnnualDeploy[MW]'].iloc[::-1] #save off reverse deploy as series
reversedeploy.index = deployments.index #reapply the index to put back into df
deployments['AnnualDeploy_rev[MW]'] = reversedeploy #add to df
deployments['CumulativeReverse[MW]'] = deployments['AnnualDeploy_rev[MW]'].cumsum()


# In[47]:


print(str(deployments['CumulativeReverse[MW]'][2035]/1e6) + ' TW in 2035')
print(str(deployments['CumulativeReverse[MW]'][2050]/1e6) + ' TW in 2055')


# In[48]:


plt.plot(deployments['AnnualDeploy_rev[MW]'])
plt.title('Annual Deployments Meeting 1.7 TW in 2050')
plt.ylabel('Annual Deploy [MW]')


# In[49]:


deployments.to_csv('alternatedeployment.csv')


# In[ ]:




