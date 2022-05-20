#!/usr/bin/env python
# coding: utf-8

# # Energy Flows for PV ICE

# This journal documents and demonstrates the new Energy flows calculation capacity of PV ICE

# In[1]:


import os
from pathlib import Path
import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


PV_ICE.__version__


# ### Add Scenarios and Materials
# 

# In[3]:


cwd=os.getcwd()
print(os.getcwd())


# In[4]:


MATERIALS = ['glass']#,'aluminium_frames','silver','silicon', 'copper', 'encapsulant', 'backsheet']
MATERIAL = MATERIALS[0]
moduleFile_recycle = r'..\baselines\perovskite_modules_US_recycle.csv'
moduleFile_reMFG = r'..\baselines\perovskite_modules_US_reMFG.csv'


# In[5]:


r1 = PV_ICE.Simulation(name='perovskite_energies', path=testfolder)

r1.createScenario(name='perovskite_recycle', file=moduleFile_recycle)
for mat in range (0, len(MATERIALS)):
    MATERIALBASELINE = r'..\baselines\perovskite_material_'+MATERIALS[mat]+'.csv'
    r1.scenario['perovskite_recycle'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)

r1.createScenario(name='perovskite_reMFG', file=moduleFile_reMFG)
for mat in range (0, len(MATERIALS)):
    MATERIALBASELINE = r'..\baselines\perovskite_material_'+MATERIALS[mat]+'.csv'
    r1.scenario['perovskite_reMFG'].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)


# ### Set All Material Virgin, MFG, and circularity to 0
# 
# Do we want to do this?

# In[6]:


#r1.scenMod_noCircularity() # sets all module and material circular variables to 0, creating fully linear
#r1.scenMod_PerfectManufacturing() #sets all manufacturing values to 100% efficiency/yield
#check:
#r1.scenario['USHistory'].material['glass'].materialdata['mat_MFG_eff']


# ### Run the Mass Flow Calculations on All Scenarios and Materials

# In[7]:


r1.calculateMassFlow()


# ## Testing Energy Flows

# In[8]:


matEfile_glass = pd.read_csv(str(Path().resolve().parent.parent /'PV_ICE' / 'baselines'/'perovskite_energy_material_glass.csv'))

modEfile = pd.read_csv(str(Path().resolve().parent.parent /'PV_ICE' / 'baselines'/'perovskite_energy_modules.csv'))


# In[9]:


matEfile_glass_simple = matEfile_glass.drop(0)
modEfile_simple = modEfile.drop(0)


# In[10]:


r1.calculateEnergyFlow(modEnergy=modEfile_simple, matEnergy=matEfile_glass_simple)


# ###  Use internal plotting functions to plot results

# Pull out the keywords by printing the keys to the module data or the material data:
# 
#     print(r1.scenario.keys())
#     
#     print(r1.scenario['standard'].data.keys())
#     
#     print(r1.scenario['standard'].material['glass'].materialdata.keys())

# In[ ]:


#print(r1.scenario.keys())
print(r1.scenario['USHistory'].data.keys())
#print(r1.scenario['USHistory'].material['glass'].materialdata.keys())


# ### Run the Energy flow calculations for all scenarios and materials

# In[ ]:





# In[ ]:





# # Calculations for file prep (module and glass)
# 
# ### Module
# We are doing a case study comparing recycling versus remanufacturing the glass for a perovskite module. The assumption is that the perovskite module lasts for 15 years, with weibull parameters that fail 10% of the modules before year 15, and a power degradation such that the module is at 80% of nameplate power at year 15. See the Lifetime vs Recycling journal for calculation of weibull parameters and degradation rates.
# 
# ### Glass
# The assumption is that a perovskite module will be a glass-glass package. Modern c-Si glass-glass (35% marketshare) bifacial modules (27% marketshare) are most likely 2.5mm front glass (28% marketshare) and 2.5 mm back glass (95% marketshare) [ITRPV 2022]. Therefore, we will assume a perovskite glass glass module will use 2 sheets of glass that are 2.5 mm thick.
# 

# In[ ]:


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

# In[ ]:


e_hotknife_tot = 150*60*(1/3600)*(1/1000) # 150 W * 60 s = W*s *(hr/s)*(kW/W)
area_mod = 1.090*2.100 #m
e_hotknife = e_hotknife_tot/area_mod # E/module to E/m2
print('Energy for hot knife separation is '+ str(round(e_hotknife, 4))+' kWh/m2. This will be used as energy of module reMFG Disassembly')


# ### Glass
# The process to remove the perovskite from the glass is relatively simple regardless of architecture (all back contact or stack). A dunk in a water-based solvent at room temperature can remove the perovskite layer, and simple heating/baking or UV+Ozone steps should round out the cleaning preparation for a new perovskite deposition. 
# 
# Using Rodriguez-Garcia G, Aydin E, De Wolf S, Carlson B, Kellar J, Celik I. Life Cycle Assessment of Coated-Glass Recovery from Perovskite Solar Cells. ACS Sustainable Chem Eng [Internet]. 2021 Nov 3 [cited 2021 Nov 8]; Available from: https://doi.org/10.1021/acssuschemeng.1c05029, we will assume a room temperature water bath with sonication, a heating/drying/baking step, and a UV+Ozone step.
# 

# In[ ]:


e_sonicate = 4  #kWh/m2 ultrasonication
e_uvozone = 3.57  #kWh/m2 ozone+UV
e_bake = 0.06  #kWh/m2 hot plate drying
e_glassreMFG_area = e_sonicate+e_uvozone+e_bake
e_glass_reMFG_mass = e_glassreMFG_area/(mass_glass/1000) #kWh/m2 *m2/g

print('Energy to remanufacture the glass (material energy only) is ' + str(round(e_glass_reMFG_mass, 2)) + 'kWh/kg')


# In[ ]:




