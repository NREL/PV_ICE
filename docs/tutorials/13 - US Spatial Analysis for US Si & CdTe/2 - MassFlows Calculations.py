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


testfolder = os.path.join(os.getcwd(), 'TEMP')
print ("Your simulation will be stored in %s" % testfolder)


# In[3]:


baselinesFolder = Path().resolve().parent.parent.parent / 'PV_ICE' / 'baselines'
baselinesFolder


# ### Reading GIS inputs

# In[5]:


from geopy.geocoders import Nominatim
from geopy.point import Point
# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")


# In[6]:


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

# In[7]:


projectionmethod = 'Method1'


# ### Scenario creation

# In[8]:


reedsFile = os.path.join(baselinesFolder, 'SupportingMaterial','December Core Scenarios ReEDS Outputs Solar Futures v3a.xlsx')
print ("Input file is stored in %s" % reedsFile)
REEDSInput = pd.read_excel(reedsFile, sheet_name="new installs PV")
rawdf = REEDSInput.copy()
rawdf.drop(columns=['State'], inplace=True)
rawdf.drop(columns=['Tech'], inplace=True) #tech=pvtotal from "new installs PV sheet", so can drop
rawdf.set_index(['Scenario','Year','PCA'], inplace=True)
PCAs = list(rawdf.unstack(level=2).iloc[0].unstack(level=0).index.unique())


# In[9]:


SFscenarios = ['95-by-35_Elec.Adv_DR_cSi', '95-by-35_Elec.Adv_DR_CdTe']


# In[10]:


i = 0
r1 = PV_ICE.Simulation(name=SFscenarios[i], path=testfolder)


# In[11]:


jj=0


# In[12]:


filetitle = SFscenarios[i]+'_'+PCAs[jj]+'.csv'
filetitle = os.path.join(testfolder, f'PCAs_{projectionmethod}', filetitle)    # Change this number to the simulation you want to run
r1.createScenario(name=PCAs[jj], massmodulefile=filetitle)
r1.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant', 'backsheet'], )
r1.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
r1.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long


# In[13]:


#for ii in range (0, 1): #len(scenarios):
i = 0
r1 = PV_ICE.Simulation(name=SFscenarios[i], path=testfolder)

for jj in range (0, len(PCAs)): 
    filetitle = SFscenarios[i]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, f'PCAs_{projectionmethod}', filetitle)    # Change this number to the simulation you want to run
    r1.createScenario(name=PCAs[jj], massmodulefile=filetitle, energymodulefile='baseline_modules_energy.csv')
    r1.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant', 'backsheet'])
    r1.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r1.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long

r1.trim_Years(startYear=2010, endYear=2050)


# In[14]:


i = 1
r2 = PV_ICE.Simulation(name=SFscenarios[i], path=testfolder)

for jj in range (0, len(PCAs)): 
    filetitle = SFscenarios[i]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, f'PCAs_{projectionmethod}', filetitle)        
    r2.createScenario(name=PCAs[jj], massmodulefile=filetitle, energymodulefile='baseline_modules_energy.csv')
    r2.scenario[PCAs[jj]].addMaterials(['cadmium', 'tellurium', 'glass_cdte', 'aluminium_frames_cdte', 'encapsulant_cdte', 'copper_cdte'])
    r2.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r2.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long

r2.trim_Years(startYear=2010, endYear=2050)


# ### Set characteristics for Manufacturing 
# IF only EoL needed, set manufacturing waste to 0 by running PercetManufacturing() modifying scenario function

# In[15]:


PERFECTMFG = True
# Set to false if I want to see how much goes to mnf waste
if PERFECTMFG:
    r1.scenMod_PerfectManufacturing()
    r2.scenMod_PerfectManufacturing()
    title_Method = 'PVICE_PerfectMFG'
else:
    title_Method = 'PVICE'


# ## 3. Calculate Mass Flow

# In[16]:


r1.calculateMassFlow()


# In[17]:


r2.calculateMassFlow()


# In[18]:


print("PCAs:", r1.scenario.keys())
print("Module Keys:", r1.scenario[PCAs[jj]].dataIn_m.keys())
print("Material Keys: ", r1.scenario[PCAs[jj]].material['glass'].matdataIn_m.keys())


# In[19]:


"""
r1.plotScenariosComparison(keyword='Cumulative_Area_disposedby_Failure')
r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_Total_Landfilled')
r1.scenario['p1'].dataIn_m.head(21)
r2.scenario['p1'].dataIn_m.head(21)
r3.scenario['p1'].dataIn_m.head(21)
"""
pass


# ## 4. Aggregate & Save Data

# In[20]:


r1.aggregateResults()
r2.aggregateResults()


# In[21]:


datay = r1.USyearly
datac = r1.UScum


# In[22]:


datay_CdTe = r2.USyearly
datac_CdTe = r2.UScum


# ### Get the EOL waste

# In[23]:


filter_colc = [col for col in datay if col.startswith('WasteEOL')]
datay[filter_colc].to_csv(f'PVICE_PCA_cSi_WasteEOL_{projectionmethod}.csv')
filter_colc = [col for col in datay_CdTe if col.startswith('WasteEOL')]
datay_CdTe[filter_colc].to_csv(f'PVICE_PCA_CdTe_WasteEOL_{projectionmethod}.csv')


# ### Get the Virgin materials

# In[24]:


filter_colc = [col for col in datay if col.startswith('VirginStock')]
datay[filter_colc].to_csv(f'PVICE_PCA_cSi_VirginStock_{projectionmethod}.csv')
filter_colc = [col for col in datay_CdTe if col.startswith('VirginStock')]
datay_CdTe[filter_colc].to_csv(f'PVICE_PCA_CdTe_VirginStock_{projectionmethod}.csv')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




