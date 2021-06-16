#!/usr/bin/env python
# coding: utf-8

# # PVSC 2021 Paper: by STATES
# ### Electrification Futures BASE Installations, 
# ### with Module Composition Scenarios for 'TODAY' and 'Bifacial Projection';
# ### Just PV ICE Reliability Approach, no Bifaciality Factor Assumptions
# 
# 
# SUMMARY OF OBJECTS:
# r1 - Today. scenarios: STATES
# r2 - Bifacial Projection. scenarios: STATES
# 
# 

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'PVSC')

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


MATERIALS = ['glass','silver','silicon', 'copper','aluminium_frames']
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'..\..\baselines\LiteratureProjections\EF-CapacityByState-basecase.csv'
## COMMENTED OUT BECAUSE WE ARE NOT DOING THE "HIGH ELECTRIFICATION SCENARIO¶
#MODULEBASELINE_High = r'..\..\baselines\LiteratureProjections\EF-CapacityByState-LowREHighElec.csv'
MODULEBASELINE_OtherParams = r'..\..\baselines\LiteratureProjections\baseline_modules_US_NREL_Energy_Futures_2021_basecase.csv'


# In[3]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# In[4]:


PV_ICE.__version__


# In[5]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# # Loading Module Baseline. 
# ## Will be used later to populate all the columsn otehr than 'new_Installed_Capacity_[MW]' which will be supplied by the REEDS model

# In[6]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='US', file=MODULEBASELINE_OtherParams)
baseline = r1.scenario['US'].data
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]'])
baseline.set_index('year', inplace=True)
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual
baseline.head()


# ## Important: STATE DATA STARTS ON 2018, so dropping columns for making the baselines

# In[7]:


baseline = baseline.iloc[23:]


# ## MERGE Baseline with States Instals

# In[8]:


df = pd.read_csv(MODULEBASELINE)
df.set_index(['Type','State','year'], inplace=True)
df.head()


# In[9]:


for ii in range (len(df.unstack(level=2))):   
    STATE = df.unstack(level=2).iloc[ii].name[1]
    SCEN = df.unstack(level=2).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = 'base_'+SCEN+'_'+STATE +'.csv'
    filetitle = os.path.join(testfolder, 'STATES', filetitle)
    A = df.unstack(level=2).iloc[ii]
    A = A.droplevel(level=0)
    A.name = 'new_Installed_Capacity_[MW]'
    A = pd.DataFrame(A)
    A.index=pd.PeriodIndex(A.index, freq='A')
    A = pd.DataFrame(A)
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] # 0.85 marketshares['Si'] already included
    # Add other columns
    A = pd.concat([A, baseline.reindex(A.index)], axis=1)
    
    
    header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,"    "mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,"    "mod_Repowering,mod_Repairing\n"    "year,MW,%,years,years,%,years,%,%,%,%,%\n"

    with open(filetitle, 'w', newline='') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
        for line in header:
            ict.write(line)

        #    savedata.to_csv(ict, index=False)
        A.to_csv(ict, header=False)


# #### COMMENTED OUT BECAUSE WE ARE NOT DOING THE "HIGH ELECTRIFICATION SCENARIO

# In[10]:


## COMMENTED OUT BECAUSE WE ARE NOT DOING THE "HIGH ELECTRIFICATION SCENARIO
"""
df = pd.read_csv(MODULEBASELINE_High)
df.set_index(['Type','State','year'], inplace=True)
df.head()

for ii in range (len(df.unstack(level=2))):   
    STATE = df.unstack(level=2).iloc[ii].name[1]
    SCEN = df.unstack(level=2).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = 'LowREHighElec_'+SCEN+'_'+STATE +'.csv'
    filetitle = os.path.join(testfolder, 'STATEs', filetitle)
    A = df.unstack(level=2).iloc[ii]
    A = A.droplevel(level=0)
    A.name = 'new_Installed_Capacity_[MW]'
    A = pd.DataFrame(A)
    A.index=pd.PeriodIndex(A.index, freq='A')
    A = pd.DataFrame(A)
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] # 0.85 marketshares['Si'] already included

    # Add other columns
    A = pd.concat([A, baseline.reindex(A.index)], axis=1)
    
    
    header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,"\
    "mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,"\
    "mod_Repowering,mod_Repairing\n"\
    "year,MW,%,years,years,%,years,%,%,%,%,%\n"

    with open(filetitle, 'w', newline='') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
        for line in header:
            ict.write(line)

        #    savedata.to_csv(ict, index=False)
        A.to_csv(ict, header=False)
"""
pass


# # DO SIMULATIONS

# In[11]:


#### Not really doing anything with Sims 'LowReHighElec' at the moment
Sims=['base','LowREHighElec']


# In[12]:


baselineinstalls = os.path.join(testfolder, 'STATEs')
onlyfiles = [f for f in os.listdir(baselineinstalls)]


# In[13]:


sim1 = [f for f in onlyfiles if f.startswith(Sims[0])]
## Not really doing anything with Sims 'LowReHighElec' at the moment
#sim2 = [f for f in onlyfiles if f.startswith(Sims[1])]
sim1[2]


# #### Get List of States

# In[14]:


STATEs = [i.split('_', 4)[2] for i in sim1]
STATEs = [i.split('.', 1)[0] for i in STATEs]


# In[15]:


MATERIALS = ['glass','aluminium_frames','silver','silicon', 'copper']


# In[16]:


MATERIALBASELINE_GLASS_TODAY = r'..\..\baselines\baseline_material_glass_hold2020.csv'
MATERIALBASELINE_ALFrames_TODAY = r'..\..\baselines\baseline_material_aluminium_frames_hold2020.csv'
MATERIALBASELINE_GLASS_BIFACIALPROJECTION = r'..\..\baselines\baseline_material_glass_bifacialTrend.csv'
MATERIALBASELINE_ALFrames_BIFACIALPROJECTION = r'..\..\baselines\baseline_material_aluminium_frames_bifacialTrend.csv'


# TODAY
r1 = PV_ICE.Simulation(name='Today', path=testfolder)

for jj in range (0, len(STATEs)): 
    filetitle = sim1[jj]
    filetitle = os.path.join(testfolder, 'STATEs', filetitle) 
    scen = STATEs[jj]
    r1.createScenario(name=scen, file=filetitle)
    r1.scenario[scen].addMaterial('glass', file=MATERIALBASELINE_GLASS_TODAY)
    r1.scenario[scen].material['glass'].materialdata = r1.scenario[scen].material['glass'].materialdata.iloc[23:].reset_index(drop=True)
    
    r1.scenario[scen].material['glass'].materialdata = r1.scenario[scen].material['glass'].materialdata
    r1.scenario[scen].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_TODAY)
    r1.scenario[scen].material['aluminium_frames'].materialdata = r1.scenario[scen].material['aluminium_frames'].materialdata.iloc[23:].reset_index(drop=True)
    
    for mat in range (2, len(MATERIALS)):
        MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
        r1.scenario[scen].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)
        r1.scenario[scen].material[MATERIALS[mat]].materialdata = r1.scenario[scen].material[MATERIALS[mat]].materialdata.iloc[23:].reset_index(drop=True)

# Bifacial Projection
r2 = PV_ICE.Simulation(name='Bifacial', path=testfolder)

for jj in range (0, len(STATEs)): 
    filetitle = sim1[jj]
    filetitle = os.path.join(testfolder, 'STATEs', filetitle) 
    scen = STATEs[jj]
    r2.createScenario(name=scen, file=filetitle)
    r2.scenario[scen].addMaterial('glass', file=MATERIALBASELINE_GLASS_BIFACIALPROJECTION)
    r2.scenario[scen].material['glass'].materialdata = r2.scenario[scen].material['glass'].materialdata.iloc[23:].reset_index(drop=True)
    
    r2.scenario[scen].material['glass'].materialdata = r2.scenario[scen].material['glass'].materialdata
    r2.scenario[scen].addMaterial('aluminium_frames', file=MATERIALBASELINE_ALFrames_BIFACIALPROJECTION)
    r2.scenario[scen].material['aluminium_frames'].materialdata = r2.scenario[scen].material['aluminium_frames'].materialdata.iloc[23:].reset_index(drop=True)
    
    for mat in range (2, len(MATERIALS)):
        MATERIALBASELINE=r'..\..\baselines\baseline_material_'+MATERIALS[mat]+'.csv'
        r2.scenario[scen].addMaterial(MATERIALS[mat], file=MATERIALBASELINE)
        r2.scenario[scen].material[MATERIALS[mat]].materialdata = r2.scenario[scen].material[MATERIALS[mat]].materialdata.iloc[23:].reset_index(drop=True)


# In[17]:


r1.calculateMassFlow()
r2.calculateMassFlow()


# # OPEN EI

# In[18]:


SFScenarios = [r1, r2]
SFScenarios[0].name


# In[19]:


# WORK ON THIS FOIR OPENEI

keyw=['mat_Virgin_Stock','mat_Total_EOL_Landfilled','mat_Total_MFG_Landfilled', 'mat_Total_Landfilled', 
      'new_Installed_Capacity_[MW]','Installed_Capacity_[W]']
keywprint = ['VirginMaterialDemand','EOLMaterial', 'ManufacturingScrap','ManufacturingScrapAndEOLMaterial',
             'NewInstalledCapacity','InstalledCapacity'] 
keywunits = ['MetricTonnes', 'MetricTonnes', 'MetricTonnes', 'MetricTonnes', 
            'MW','MW']
keywdcumneed = [True,True,True,True,
                True,False]
keywdlevel = ['material','material','material','material',
             'module','module']
keywscale = [1000000, 1000000, 1000000, 1000000,
            1,1e6]
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminum']
materials = ['glass','aluminium_frames','silver','silicon', 'copper']

# Loop over SF Scenarios

scenariolist = pd.DataFrame()
for kk in range(0, len(SFScenarios)):
    # Loop over Materials
    
    for zz in range (0, len(STATEs)):

        foo = pd.DataFrame()
        for jj in range (0, len(keyw)):

            if keywdlevel[jj] == 'material':
                for ii in range (0, len(materials)):    
                    scen = STATEs[zz]
                    sentit = '@value|'+keywprint[jj]+'|'+materials[ii].capitalize() +'#'+keywunits[jj]
                    foo[sentit] = SFScenarios[kk].scenario[scen].material[materials[ii]].materialdata[keyw[jj]]/keywscale[jj] 
            
                if keywdcumneed[jj]:
                    for ii in range (0, len(materials)):    
                        sentit = '@value|Cumulative'+keywprint[jj]+'|'+materials[ii].capitalize() +'#'+keywunits[jj]
                        foo[sentit] = SFScenarios[kk].scenario[scen].material[materials[ii]].materialdata[keyw[jj]].cumsum()/keywscale[jj] 

            else:
                sentit = '@value|'+keywprint[jj]+'|'+'PV' +'#'+keywunits[jj]
                #sentit = '@value|'+keywprint[jj]+'#'+keywunits[jj]
                foo[sentit] = SFScenarios[kk].scenario[scen].data[keyw[jj]]/keywscale[jj] 

                if keywdcumneed[jj]:
                    sentit = '@value|Cumulative'+keywprint[jj]+'|'+'PV' +'#'+keywunits[jj]
                    foo[sentit] = SFScenarios[kk].scenario[scen].data[keyw[jj]].cumsum()/keywscale[jj] 
                  

        foo['@states'] = STATEs[zz]
        foo['@scenario|Module Composition Scenario'] = SFScenarios[kk].name 
#        foo['@filter|Install'] = Type[zz]
        foo['@timeseries|Year'] = SFScenarios[kk].scenario[scen].data.year

        scenariolist = scenariolist.append(foo)   

cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
#cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
#scenariolist = scenariolist[cols]
#scenariolist = scenariolist/1000000 # Converting to Metric Tons
#scenariolist = scenariolist.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
#scenariolist = scenariolist.applymap(lambda x: int(x))
scenariolist.to_csv('OPEN EI 1 - STATE - PVSC 2021 PV ICE Today and Bifacial Projection All columns.csv', index=False)

print("Done")


# In[20]:


scenariolist.head(5)


# In[21]:


#scenariolist.keys()


# ### Save REDUCED CSV
# ###### Just Capacity & Module EOL Waste Columns

# In[22]:


csvtitle = 'OPEN EI 2 - STATE - PVSC 2021 PV ICE Today and Bifacial Projection Selected Columns.csv'
colNames = scenariolist.columns[scenariolist.columns.str.contains('CumulativeEOLMaterial')] 
print(colNames)
scenariolist['@value|CumulativeEOLMaterial|Module#MetricTonnes'] = scenariolist[colNames].sum(axis=1)
foo = scenariolist[['@states', '@scenario|Module Composition Scenario', '@timeseries|Year', 
                    '@value|NewInstalledCapacity|PV#MW', '@value|CumulativeNewInstalledCapacity|PV#MW', 
                    '@value|InstalledCapacity|PV#MW',
                   '@value|CumulativeEOLMaterial|Module#MetricTonnes']]
foo.to_csv(csvtitle, index=False)
foo.head(5)


# In[ ]:




