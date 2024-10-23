#!/usr/bin/env python
# coding: utf-8

# # MassFlows Calculations

# ## 1. Initial setup

# In[1]:


import PV_ICE
import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
from pathlib import Path


# In[2]:


testfolder = os.path.join('TEMP')
print ("Your simulation will be stored in %s" % testfolder)


# In[3]:


baselinesFolder = Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines'
baselinesFolder


# ### Reading GIS inputs

# In[4]:


GISfile = os.path.join(baselinesFolder, 'SupportingMaterial','gis_centroid_n.csv')
GIS = pd.read_csv(GISfile)
GIS = GIS.set_index('id')


# ## 2. Load PCA baselines, create the 2 Scenarios and assign baselines
# 
# Keeping track of each scenario as its own PV ICE Object.

# Select the method folder you want to run (uncomment your choice). There are three choices:
# 1. Method 1: Uses the raw regionalized capacity by ReEEDS, this creates a very uneven peak of wastes.
# 2. Method 2: Uses ordered wastes between 2021 to 2035 and 2046 to 2050. Still creates unrealistic peaks.
# 3. Method 3: Uses the cummulative capacity between 2021 to 2035 and 2034 to 2050 to create a logarithmic growth of waste (this method is being tested, not validated yet, and subjected to ongoing changes).

# In[5]:


projectionmethod = 'Method1'


# ### Scenario creation

# In[6]:


SFscenarioname = '95-by-35_Elec.Adv_DR'
SFscenarios = ['95-by-35_Elec.Adv_DR_cSi' , '95-by-35_Elec.Adv_DR_CdTe']


# In[7]:


i = 0
r1 = PV_ICE.Simulation(name=SFscenarioname, path=testfolder)


# In[8]:


filetitle = SFscenarios[i]+'.csv'
filetitle = os.path.join('USA', filetitle)    
energyfiletitle = os.path.join(baselinesFolder, 'baseline_modules_energy.csv')
r1.createScenario(name='cSi', massmodulefile=filetitle, energymodulefile=energyfiletitle)
r1.scenario['cSi'].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant', 'backsheet'], )


# In[9]:


filetitle = SFscenarios[i+1]+'.csv'
filetitle = os.path.join('USA', filetitle)    
energyfiletitle = os.path.join(baselinesFolder, 'baseline_modules_energy_CdTe.csv')
r1.createScenario(name='CdTe', massmodulefile=filetitle, energymodulefile=energyfiletitle)
r1.scenario['CdTe'].addMaterials(['glass_cdte', 'cadmium', 'tellurium', 'copper_cdte', 'aluminium_frames_cdte', 'encapsulant_cdte'], )


# In[10]:


r1.scenario['CdTe'].material['glass_cdte'].addEnergytoMaterial(energymatfile=os.path.join(baselinesFolder, 'baseline_material_energy_'+'glass'+'.csv'))
r1.scenario['CdTe'].material['copper_cdte'].addEnergytoMaterial(energymatfile=os.path.join(baselinesFolder, 'baseline_material_energy_'+'copper'+'.csv'))
r1.scenario['CdTe'].material['aluminium_frames_cdte'].addEnergytoMaterial(energymatfile=os.path.join(baselinesFolder, 'baseline_material_energy_'+'aluminium_frames'+'.csv'))
r1.scenario['CdTe'].material['encapsulant_cdte'].addEnergytoMaterial(energymatfile=os.path.join(baselinesFolder, 'baseline_material_energy_'+'encapsulant'+'.csv'))


# In[11]:


r1.trim_Years(startYear=2010, endYear=2050)


# ### Set characteristics for Manufacturing 
# IF only EoL needed, set manufacturing waste to 0 by running PercetManufacturing() modifying scenario function

# In[12]:


PERFECTMFG = True
# Set to false if I want to see how much goes to mnf waste
if PERFECTMFG:
    r1.scenMod_PerfectManufacturing()
    title_Method = 'PVICE_PerfectMFG'
else:
    title_Method = 'PVICE'


# ## 3. Calculate Mass Flow

# In[13]:


r1.calculateMassFlow()


# ## 4. Aggregate & Save Data

# In[16]:


r1.aggregateResults()


# In[20]:


r1.USyearly.to_csv('USyearly.csv')
r1.UScum.to_csv('UScum.csv')

