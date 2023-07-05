#!/usr/bin/env python
# coding: utf-8

# # ReEDS Scenarios on PV ICE Tool

# To explore different scenarios for furture installation projections of PV (or any technology), ReEDS output data can be useful in providing standard scenarios. ReEDS installation projections from the Solar Futures DOE Report (2021) are used in this journal as input data to the PV ICE tool. 
# 
# Current sections include:
# 
# <ol>
#     <li> ### Reading a standard ReEDS output file and saving it in a PV ICE input format </li>
# <li>### Reading scenarios of interest and running PV ICE tool </li>
# <li>###Plotting </li>
# <li>### GeoPlotting.</li>
# </ol>
#     Notes:
#    
# Scenarios of Interest:
# 	the Ref.Mod, 
# o	95-by-35.Adv, and 
# o	95-by-35+Elec.Adv+DR ones
# 

# In[1]:


import PV_ICE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os,sys

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[2]:


PV_ICE.__version__


# In[3]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'PCA')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)

print ("Your simulation will be stored in %s" % testfolder)


# In[ ]:


SupportingMaterialFolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
BaselinesFolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')


# ### Reading REEDS original file to get list of SCENARIOs, PCAs, and STATEs 

# In[ ]:


reedsFile = os.path.join(SupportingMaterialFolder, 'December Core Scenarios ReEDS Outputs Solar Futures v3a.xlsx')
print ("Input file is stored in %s" % reedsFile)


# In[ ]:


rawdf = pd.read_excel(reedsFile,
                        sheet_name="new installs PV")
                        #index_col=[0,2,3]) #this casts scenario, PCA and State as levels
#now set year as an index in place
#rawdf.drop(columns=['State'], inplace=True)
rawdf.drop(columns=['Tech'], inplace=True)
rawdf.set_index(['Scenario','Year','PCA'], inplace=True)


# In[ ]:


scenarios = list(rawdf.index.get_level_values('Scenario').unique())
PCAs = list(rawdf.index.get_level_values('PCA').unique())
STATEs = list(rawdf.index.get_level_values('State').unique())


# ### Reading GIS inputs

# In[ ]:


GISfile = os.path.join(SupportingMaterialFolder, 'gis_centroid_n.csv')
GIS = pd.read_csv(GISfile)
GIS = GIS.set_index('id')


# In[ ]:


GIS.head()


# In[ ]:


GIS.loc['p1'].long


# # 1. Create ReEDS Scenarios BASELINE Files

# #### Loading Module Baseline. Will be used later to populate all the columsn otehr than 'new_Installed_Capacity_[MW]' which will be supplied by the REEDS model

# In[ ]:


import PV_ICE
r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='US', massmodulefile=r'..\baselines\baseline_modules_mass_US.csv')
r1.scenMod_noCircularity() # Reeds Solar Future Study had circularity paths set to 0
baseline = r1.scenario['US'].dataIn_m
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]'])
baseline.set_index('year', inplace=True)
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual
baseline.head()


# #### For each Scenario and for each PCA, combine with baseline and save as input file

# In[ ]:


# Set header dynamically


# In[ ]:


SupportingMaterialFolder


# In[ ]:





# In[ ]:


import csv

massmodulefile = os.path.join(BaselinesFolder, 'baseline_modules_mass_US.csv')

with open(massmodulefile, newline='') as f:
  reader = csv.reader(f)
  row1 = next(reader)  # gets the first line
  row2 = next(reader)  # gets the first line

row11 = 'year'
for x in row1[1:]:
    row11 = row11 + ',' + x 

row22 = 'year'
for x in row2[1:]:
    row22 = row22 + ',' + x 


# In[ ]:


row11


# In[ ]:


for ii in range (len(rawdf.unstack(level=1))):
    PCA = rawdf.unstack(level=1).iloc[ii].name[1]
    SCEN = rawdf.unstack(level=1).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = SCEN+'_'+PCA +'.csv'
    subtestfolder = os.path.join(testfolder, 'PCAs')
    if not os.path.exists(subtestfolder):
        os.makedirs(subtestfolder)
    filetitle = os.path.join(subtestfolder, filetitle)
    A = rawdf.unstack(level=1).iloc[ii]
    A = A.droplevel(level=0)
    A.name = 'new_Installed_Capacity_[MW]'
    A = pd.DataFrame(A)
    A.index=pd.PeriodIndex(A.index, freq='A')
    A = pd.DataFrame(A)
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 0.85
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 1000   # ReEDS file is in GW.
    # Add other columns
    A = pd.concat([A, baseline.reindex(A.index)], axis=1)
   
    header = row11 + '\n' + row22 + '\n'
    
    with open(filetitle, 'w', newline='') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
        for line in header:
            ict.write(line)

        #    savedata.to_csv(ict, index=False)
        A.to_csv(ict, header=False)


# ### Create Scenarios in PV_ICE

# #### Rename difficult characters from Scenarios Names

# In[ ]:


simulationname = scenarios
simulationname = [w.replace('+', '_') for w in simulationname]
simulationname


# #### Downselect to Solar Future scenarios of interest
# 
# Scenarios of Interest:
# <li> Ref.Mod
# <li> 95-by-35.Adv  
# <li> 95-by-35+Elec.Adv+DR 

# In[ ]:


SFscenarios = [simulationname[0], simulationname[4], simulationname[8]]
SFscenarios


# #### Create the 3 Scenarios and assign Baselines
# 
# Keeping track of each scenario as its own PV ICE Object.

# In[ ]:


#for ii in range (0, 1): #len(scenarios):
i = 0
r1 = PV_ICE.Simulation(name=SFscenarios[i], path=testfolder)

for jj in range (0, len(PCAs)): 
    filetitle = SFscenarios[i]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, 'PCAs', filetitle)    
    r1.createScenario(name=PCAs[jj], massmodulefile=filetitle)
    r1.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']) 
    r1.trim_Years(startYear=2010, endYear=2050)
    # All -- but these where not included in the Reeds initial study as we didnt have encapsulant or backsheet
    # r1.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant', 'backsheet'], baselinefolder=r'..\baselines')
    r1.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r1.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long

i = 1
r2 = PV_ICE.Simulation(name=SFscenarios[i], path=testfolder)

for jj in range (0, len(PCAs)): 
    filetitle = SFscenarios[i]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, 'PCAs', filetitle)        
    r2.createScenario(name=PCAs[jj], massmodulefile=filetitle)
    r2.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']) 
    r2.trim_Years(startYear=2010, endYear=2050)
    # All -- but these where not included in the Reeds initial study as we didnt have encapsulant or backsheet
    # r2.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant', 'backsheet'], baselinefolder=r'..\baselines')
    r2.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r2.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long

i = 2
r3 = PV_ICE.Simulation(name=SFscenarios[i], path=testfolder)
for jj in range (0, len(PCAs)): 
    filetitle = SFscenarios[i]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, 'PCAs', filetitle)        
    r3.createScenario(name=PCAs[jj], massmodulefile=filetitle)
    r3.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']) #
    r3.trim_Years(startYear=2010, endYear=2050)
    # All -- but these where not included in the Reeds initial study as we didnt have encapsulant or backsheet
    # r3.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant', 'backsheet'], baselinefolder=r'..\baselines')
    r3.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r3.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long


# # 2 Set characteristics of Recycling to SF values.

# In[ ]:


IRENA= False
PERFECTMFG = True

mats = ['glass', 'silicon','silver','copper','aluminum']

ELorRL = 'EL'
if IRENA:
    if ELorRL == 'RL':
        r1.scenMod_IRENIFY(ELorRL='RL')
        r2.scenMod_IRENIFY(ELorRL='RL')
        r3.scenMod_IRENIFY(ELorRL='RL')

    if ELorRL == 'EL':
        r1.scenMod_IRENIFY(ELorRL='EL')
        r2.scenMod_IRENIFY(ELorRL='EL')
        r3.scenMod_IRENIFY(ELorRL='EL')
    
    
    if PERFECTMFG:
        r1.scenMod_PerfectManufacturing()
        r2.scenMod_PerfectManufacturing()
        r3.scenMod_PerfectManufacturing()

    title_Method = 'Irena_'+ELorRL
else:
    title_Method = 'PVICE'


# #### Calculate Mass Flow

# In[ ]:


r1.calculateMassFlow()
r2.calculateMassFlow()
r3.calculateMassFlow()


# In[ ]:


print("PCAs:", r1.scenario.keys())
print("Module Keys:", r1.scenario[PCAs[jj]].dataIn_m.keys())
print("Material Keys: ", r1.scenario[PCAs[jj]].material['glass'].matdataIn_m.keys())


# In[ ]:


"""
r1.plotScenariosComparison(keyword='Cumulative_Area_disposedby_Failure')
r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_Total_Landfilled')
r1.scenario['p1'].dataIn_m.head(21)
r2.scenario['p1'].dataIn_m.head(21)
r3.scenario['p1'].dataIn_m.head(21)
"""
pass


# In[ ]:


USyearly1, UScum1 = r1.aggregateResults()
USyearly2, UScum2 = r2.aggregateResults()
USyearly3, UScum3 = r3.aggregateResults()


# In[ ]:


USyearly1.to_csv('USyearly_'+r1.name+'.csv')
UScum1.to_csv('UScum_'+r1.name+'.csv')
USyearly2.to_csv('USyearly_'+r2.name+'.csv')
UScum2.to_csv('UScum_'+r2.name+'.csv')
USyearly3.to_csv('USyearly_'+r3.name+'.csv')
UScum3.to_csv('UScum_'+r3.name+'.csv')


# # Manual Data Saving

# ### PCA vs. Cumulative Waste by 2050
# 

# In[ ]:


#for 3 significant numbers rounding
N = 2


# SFScenarios[kk].scenario[PCAs[zz]].data.year
# 
# Index 20 --> 2030
# 
# Index 30 --> 2040
# 
# Index 40 --> 2050

# In[ ]:


idx2030 = 20
idx2040 = 30
idx2050 = 40
print("index ", idx2030, " is year ", r1.scenario[PCAs[0]].dataIn_m['year'].iloc[idx2030])
print("index ", idx2040, " is year ", r1.scenario[PCAs[0]].dataIn_m['year'].iloc[idx2040])
print("index ", idx2050, " is year ", r1.scenario[PCAs[0]].dataIn_m['year'].iloc[idx2050])


# #### 1 - PCA Cumulative Virgin Needs by 2050

# In[ ]:


materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']


# In[ ]:


keyword='mat_Virgin_Stock'

SFScenarios = [r1, r2, r3]
# Loop over SF Scenarios

scenariolist = pd.DataFrame()
for kk in range(0, 3):
    # Loop over Materials
    
    materiallist = []
    for ii in range (0, len(materials)):    
        
        keywordsum = []
        for zz in range (0, len(PCAs)):
            keywordsum.append(SFScenarios[kk].scenario[PCAs[zz]].material[materials[ii]].matdataOut_m[keyword].sum())
    
        materiallist.append(keywordsum)
    df = pd.DataFrame (materiallist,columns=PCAs, index = materials)
    df = df.T
    df = df.add_prefix(SFScenarios[kk].name+'_')
    scenariolist = pd.concat([scenariolist , df], axis=1)

scenariolist = scenariolist/1000000 # Converting to Metric Tons
#scenariolist = scenariolist.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
#scenariolist = scenariolist.applymap(lambda x: int(x))
scenariolist.to_csv(title_Method+' 1 - PCA Cumulative2050 VirginMaterialNeeds_tons.csv')


# #### 2 - PCA Cumulative EoL Only Waste by 2050

# In[ ]:


keyword='mat_Total_EOL_Landfilled'

SFScenarios = [r1, r2, r3]
# Loop over SF Scenarios

scenariolist = pd.DataFrame()
for kk in range(0, 3):
    # Loop over Materials
    
    materiallist = []
    for ii in range (0, len(materials)):    
        
        keywordsum = []
        for zz in range (0, len(PCAs)):
            keywordsum.append(SFScenarios[kk].scenario[PCAs[zz]].material[materials[ii]].matdataOut_m[keyword].sum())
    
        materiallist.append(keywordsum)
    df = pd.DataFrame (materiallist,columns=PCAs, index = materials)
    df = df.T
    df = df.add_prefix(SFScenarios[kk].name+'_')
    scenariolist = pd.concat([scenariolist , df], axis=1)

scenariolist = scenariolist/1000000 # Converting to Metric Tons
#scenariolist = scenariolist.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
#scenariolist = scenariolist.applymap(lambda x: int(x))
scenariolist.to_csv(title_Method+' 2 - PCA Cumulative2050 Waste EOL_tons.csv')


# #### 3 - PCA Yearly Virgin Needs 2030 2040 2050

# In[ ]:


keyword='mat_Virgin_Stock'

SFScenarios = [r1, r2, r3]
# Loop over SF Scenarios

scenariolist = pd.DataFrame()
for kk in range(0, 3):
    # Loop over Materials
    materiallist = pd.DataFrame()

    for ii in range (0, len(materials)):    
        
        keywordsum2030 = []
        keywordsum2040 = []
        keywordsum2050 = []

        for zz in range (0, len(PCAs)):
            keywordsum2030.append(SFScenarios[kk].scenario[PCAs[zz]].material[materials[ii]].matdataOut_m[keyword][idx2030])
            keywordsum2040.append(SFScenarios[kk].scenario[PCAs[zz]].material[materials[ii]].matdataOut_m[keyword][idx2040])
            keywordsum2050.append(SFScenarios[kk].scenario[PCAs[zz]].material[materials[ii]].matdataOut_m[keyword][idx2050])
    
        yearlylist = pd.DataFrame([keywordsum2030, keywordsum2040, keywordsum2050], columns=PCAs, index = [2030, 2040, 2050])
        yearlylist = yearlylist.T
        yearlylist = yearlylist.add_prefix(materials[ii]+'_')
        materiallist = pd.concat([materiallist, yearlylist], axis=1)
    materiallist = materiallist.add_prefix(SFScenarios[kk].name+'_')
    scenariolist = pd.concat([scenariolist , materiallist], axis=1)

scenariolist = scenariolist/1000000   # Converting to Metric Tons
#scenariolist = scenariolist.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
#scenariolist = scenariolist.applymap(lambda x: int(x))
scenariolist.to_csv(title_Method+' 3 - PCA Yearly 2030 2040 2050 VirginMaterialNeeds_tons.csv')


# #### 4 - PCA Yearly EoL Waste 2030 2040 2050

# In[ ]:


keyword='mat_Total_Landfilled'

SFScenarios = [r1, r2, r3]
# Loop over SF Scenarios

scenariolist = pd.DataFrame()
for kk in range(0, 3):
    # Loop over Materials
    materiallist = pd.DataFrame()

    for ii in range (0, len(materials)):    
        
        keywordsum2030 = []
        keywordsum2040 = []
        keywordsum2050 = []

        for zz in range (0, len(PCAs)):
            keywordsum2030.append(SFScenarios[kk].scenario[PCAs[zz]].material[materials[ii]].matdataOut_m[keyword][idx2030])
            keywordsum2040.append(SFScenarios[kk].scenario[PCAs[zz]].material[materials[ii]].matdataOut_m[keyword][idx2040])
            keywordsum2050.append(SFScenarios[kk].scenario[PCAs[zz]].material[materials[ii]].matdataOut_m[keyword][idx2050])
    
        yearlylist = pd.DataFrame([keywordsum2030, keywordsum2040, keywordsum2050], columns=PCAs, index = [2030, 2040, 2050])
        yearlylist = yearlylist.T
        yearlylist = yearlylist.add_prefix(materials[ii]+'_')
        materiallist = pd.concat([materiallist, yearlylist], axis=1)
    materiallist = materiallist.add_prefix(SFScenarios[kk].name+'_')
    scenariolist = pd.concat([scenariolist , materiallist], axis=1)

scenariolist = scenariolist/1000000   # Converting to Metric Tonnes
#scenariolist = scenariolist.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
#scenariolist = scenariolist.applymap(lambda x: int(x))
scenariolist.to_csv(title_Method+' 4 - PCA Yearly 2030 2040 2050 Waste_EOL_tons.csv')

