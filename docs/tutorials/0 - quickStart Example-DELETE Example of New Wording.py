#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


import PV_ICE
PV_ICE.__version__


# In[ ]:


addMaterials(['glass', 'everything']) broken

for mat in materiallist:
    addMaterial('glass')


# In[12]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='standard', massmodulefile=r'..\baselines\baseline_modules_mass_US.csv') # can also be file
r1.scenario['standard'].addEnergytoModule(energymodulefile=r'..\baselines\baseline_modules_energy.csv')
r1.scenario['standard'].addMaterial('glass', massmatfile =r'..\baselines\baseline_material_mass_glass.csv') # can also be file
r1.scenario['standard'].material['glass'].addEnergytoMaterial(energymatfile=r'..\baselines\baseline_material_energy_glass.csv')


# In[4]:


r1.calculateMassFlow()


# In[15]:


r1.calculateEnergyFlow()


# In[14]:


r1.calculateFlows()


# In[5]:


r1.scenario['standard'].dataIn_m.keys()


# In[6]:


list(r1.scenario['standard'].dataOut_m.keys())


# In[16]:


list(r1.scenario['standard'].dataOut_e.keys())


# In[19]:


list(r1.scenario['standard'].material['glass'].matdataIn_m.keys())


# In[17]:


list(r1.scenario['standard'].material['glass'].matdataOut_m.keys())


# In[20]:


list(r1.scenario['standard'].material['glass'].matdataIn_e.keys())


# In[18]:


list(r1.scenario['standard'].material['glass'].matdataOut_e.keys())


# In[11]:


list(r1.scenario['standard'].material['glass'].__dict__)


# In[21]:


r1.scenario['standard'].material['glass'].massmatfile

