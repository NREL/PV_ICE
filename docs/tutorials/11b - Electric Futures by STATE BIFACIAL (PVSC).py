#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'ElectricFutures')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


MATERIALS = ['glass','silver','silicon', 'copper','aluminium_frames']
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'..\..\baselines\LiteratureProjections\EF-CapacityByState-basecase.csv'
MODULEBASELINE_High = r'..\..\baselines\LiteratureProjections\EF-CapacityByState-LowREHighElec.csv'


# In[3]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# In[4]:


PV_ICE.__version__


# ### Loading Module Baseline. Will be used later to populate all the columsn otehr than 'new_Installed_Capacity_[MW]' which will be supplied by the REEDS model

# In[5]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='US', file=r'..\..\baselines\ReedsSubset\baseline_modules_US_Reeds_EF.csv')
baseline = r1.scenario['US'].data
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]'])
baseline.set_index('year', inplace=True)
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual
baseline.head()


# In[6]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[7]:


df = pd.read_csv(MODULEBASELINE)
df.set_index(['Type','State','year'], inplace=True)
df.head()


# In[8]:


for ii in range (len(df.unstack(level=2))):   
    STATE = df.unstack(level=2).iloc[ii].name[1]
    SCEN = df.unstack(level=2).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = 'base_'+SCEN+'_'+STATE +'.csv'
    filetitle = os.path.join(testfolder, 'baselines', filetitle)
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


# In[9]:


df = pd.read_csv(MODULEBASELINE_High)
df.set_index(['Type','State','year'], inplace=True)
df.head()


# In[10]:


for ii in range (len(df.unstack(level=2))):   
    STATE = df.unstack(level=2).iloc[ii].name[1]
    SCEN = df.unstack(level=2).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = 'LowREHighElec_'+SCEN+'_'+STATE +'.csv'
    filetitle = os.path.join(testfolder, 'baselines', filetitle)
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


# In[11]:


ict


# # DO SIMULATIONS

# In[12]:


Sims=['base','LowREHighElec']


# In[13]:


baselineinstalls = os.path.join(testfolder, 'baselines')
onlyfiles = [f for f in os.listdir(baselineinstalls)]


# In[ ]:





# In[14]:


sim1 = [f for f in onlyfiles if f.startswith(Sims[0])]
sim2 = [f for f in onlyfiles if f.startswith(Sims[1])]


# In[24]:


STATEs = [i.split('_', 4)[2] for i in sim1]
STATEs = [i.split('.', 1)[0] for i in STATEs]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[30]:


testfolder


# In[33]:


#for ii in range (0, 1): #len(scenarios):
i = 0
r1 = PV_ICE.Simulation(name='Today', path=testfolder)

MATERIALBASELINE_GLASS = r'materialsubsets\baseline_material_glass_hold2020.csv'
MATERIALBASELINE_ALFrames = r'materialsubsets\baseline_material_aluminium_frames_hold2020.csv'


for jj in range (0, len(STATEs)): 
    filetitle = sim1[jj]
    filetitle = os.path.join(testfolder, 'baselines', filetitle) 
    scen = STATEs[jj]
    r1.createScenario(name=scen, file=filetitle)
    r1.scenario[scen].addMaterial('glass', file=MATERIALBASELINE_GLASS)
    r1.scenario[scen].addMaterial('aluminum', file=MATERIALBASELINE_ALFrames)
    r1.scenario[scen].addMaterial('silicon', file=r'materialsubsets\baseline_material_silicon_Reeds.csv')
    r1.scenario[scen].addMaterial('silver', file=r'materialsubsets\baseline_material_silver_Reeds.csv')
    r1.scenario[scen].addMaterial('copper', file=r'materialsubsets\baseline_material_copper_Reeds.csv')


i = 1
r2 = PV_ICE.Simulation(name='Bifacial', path=testfolder)

MATERIALBASELINE_GLASS = r'materialsubsets\baseline_material_glass_bifacialTrend.csv'
MATERIALBASELINE_ALFrames = r'materialsubsets\baseline_material_aluminium_frames_bifacialTrend.csv'


for jj in range (0, len(STATEs)): 
    filetitle = sim2[jj]
    filetitle = os.path.join(testfolder, 'baselines', filetitle)    
    scen = STATEs[jj]
    r2.createScenario(name=scen, file=filetitle)
    r2.scenario[scen].addMaterial('glass', file=MATERIALBASELINE_GLASS)
    r2.scenario[scen].addMaterial('aluminum', file=MATERIALBASELINE_ALFrames)
    r2.scenario[scen].addMaterial('silicon', file=r'materialsubsets\baseline_material_silicon_Reeds.csv')
    r2.scenario[scen].addMaterial('silver', file=r'materialsubsets\baseline_material_silver_Reeds.csv')
    r2.scenario[scen].addMaterial('copper', file=r'materialsubsets\baseline_material_copper_Reeds.csv')


# In[36]:


r1.calculateMassFlow()
r2.calculateMassFlow()


# # OPEN EI

# In[37]:


kk=0
SFScenarios = [r1, r2]
SFScenarios[kk].name


# In[42]:


r1.name


# In[57]:


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
scenariolist.to_csv('OPEN EI PVSC by State ELECTRIF FUTURES.csv', index=False)

print("Done")


# In[58]:


scenariolist


# In[62]:


# OpenEI 1 - Cumulative EOL by State, Module
csvtitle = 'OPENEI 1 - Cumulative EOL Module Material, by State.csv'
colNames = scenariolist.columns[scenariolist.columns.str.contains('CumulativeEOLMaterial')] 

scenariolist['@value|CumulativeEOLMaterial|Module#MetricTonnes'] = scenariolist[colNames].sum(axis=1)
foo = scenariolist[['@states', '@scenario|Module Composition Scenario', '@timeseries|Year', 
                    '@value|CumulativeEOLMaterial|Module#MetricTonnes']]
foo.to_csv(csvtitle, index=False)


# In[64]:





# In[59]:


scenariolist.keys()


# In[ ]:


'@value|CumulativeEOLMaterial|Glass#MetricTonnes',
     '@value|CumulativeEOLMaterial|Silicon#MetricTonnes',
     '@value|CumulativeEOLMaterial|Silver#MetricTonnes',
     '@value|CumulativeEOLMaterial|Copper#MetricTonnes',
     '@value|CumulativeEOLMaterial|Aluminum#MetricTonnes'

