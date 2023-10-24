#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os # Creates and removes a directory (folder), fetch its contents, change and identify the current directory
from pathlib import Path
import PV_ICE # Load PV_ICE package

print("Successfully imported PV_ICE, version ", PV_ICE.__version__)

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'test') # Path to the simulation folder.

baselinesfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')  # Path to baselines and data.

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)
print ("Your baselines are stored in %s" % baselinesfolder)

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# In[ ]:


r1 = PV_ICE.Simulation.load_Simpickle(filename=r'C:\Users\sayala\Documents\GitHub\PV_ICE\PV_ICE\TEMP\test\Simulation1.pkl')


# In[10]:


import pandas as pd
import numpy as np


# In[2]:


from os.path import normpath, basename
pathstr = r'C:\Users\sayala\Documents\GitHub\PV_ICE\PV_ICE\TEMP\test'

name = basename(normpath(pathstr))

inputfiles = os.listdir(os.path.join(pathstr, 'input'))


# In[8]:


scenarios = [s[:-13] for s in inputfiles if "_dataIn_m.csv" in s]

scen = len(scenarios[0]) + 1 # ('Adding 1 for the underscore')
materials = [s[scen:-16] for s in inputfiles if "_matdataIn_m.csv" in s]
#materials = [s[scen:] for s in materials if scenarios[0] in s]
materials = list(set(materials))

if len(materials)%len(a) != 0:
    print("there might be an issue with the number of materials saved. Perhaps, tell silvana.")
    
for scen in scenarios:
    filee = scen + '_dataIn_m.csv'
    scenfile = os.path.join(pathstr, 'input', filee)
    with open(scenfile) as fd:
        headers = [next(fd) for i in range(2) ]
        cols = headers[0].strip().split(',')
        meta = headers[1].strip().split(',')

        df = pd.read_csv(fd, sep=',', names=cols)
        df2 = df.drop(df.columns[0],axis=1)
        
        cols = cols[1:] # removing the first empty item
        meta = meta[1:]
        metadict = {cols[i]: meta[i] for i in range(len(cols))}
        for mat in materials:
            


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='base', massmodulefile=r'..\..\baselines\baseline_modules_mass_US.csv', energymodulefile=r'..\..\baselines\baseline_modules_energy.csv')
r1.scenario['base'].addMaterials(['glass', 'silicon'])

r1.createScenario(name='pvsk', massmodulefile=r'..\..\baselines\baseline_modules_mass_US.csv', energymodulefile=r'..\..\baselines\baseline_modules_energy.csv')
r1.scenario['pvsk'].addMaterials(['glass', 'silicon'])


# In[ ]:


r1.scenario['pvsk'].dataIn_m['mod_reliability_t50'] = 10
r1.scenario['pvsk'].dataIn_m['mod_reliability_t90'] = 12
r1.scenario['pvsk'].dataIn_m['mod_lifetime'] = 15


# In[ ]:


r1.calculateFlows()


# In[ ]:


r1.pickle_Sim()


# In[ ]:


USyearly, UScum = r1.aggregateResults()


# In[ ]:


r1.saveSimulation()


# In[ ]:




