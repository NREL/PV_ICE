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


# In[10]:


df = pd.read_csv(MODULEBASELINE_High)
df.set_index(['Type','State','year'], inplace=True)
df.head()


# In[18]:


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


# In[12]:


ict


# # DO SIMULATIONS

# In[13]:


Sims=['base','LowREHighElec']


# In[14]:


baselineinstalls = os.path.join(testfolder, 'baselines')
onlyfiles = [f for f in os.listdir(baselineinstalls)]


# In[15]:


sim1 = [f for f in onlyfiles if f.startswith(Sims[0])]
sim2 = [f for f in onlyfiles if f.startswith(Sims[1])]


# In[16]:


STATEs = [i.split('_', 4)[3] for i in sim1]
STATEs = [i.split('.', 1)[0] for i in STATEs]
Type = [i.split('_', 4)[1] for i in sim1]


# In[ ]:





# In[17]:


#for ii in range (0, 1): #len(scenarios):
i = 0
r1 = PV_ICE.Simulation(name=Sims[i], path=testfolder)

for jj in range (0, len(sim1)): 
    filetitle = sim1[jj]
    filetitle = os.path.join(testfolder, 'baselines', filetitle) 
    scen = Type[jj]+'_'+STATEs[jj]
    r1.createScenario(name=scen, file=filetitle)
    r1.scenario[scen].addMaterial('glass', file=r'materialsubsets\baseline_material_glass_Reeds.csv')
    r1.scenario[scen].addMaterial('silicon', file=r'materialsubsets\baseline_material_silicon_Reeds.csv')
    r1.scenario[scen].addMaterial('silver', file=r'materialsubsets\baseline_material_silver_Reeds.csv')
    r1.scenario[scen].addMaterial('copper', file=r'materialsubsets\baseline_material_copper_Reeds.csv')
    r1.scenario[scen].addMaterial('aluminum', file=r'materialsubsets\baseline_material_aluminium_Reeds.csv')


i = 1
r2 = PV_ICE.Simulation(name=Sims[i], path=testfolder)

for jj in range (0, len(STATEs)): 
    filetitle = sim2[jj]
    filetitle = os.path.join(testfolder, 'baselines', filetitle)    
    scen = Type[jj]+'_'+STATEs[jj]
    r2.createScenario(name=scen, file=filetitle)
    r2.scenario[scen].addMaterial('glass', file=r'materialsubsets\baseline_material_glass_Reeds.csv')
    r2.scenario[scen].addMaterial('silicon', file=r'materialsubsets\baseline_material_silicon_Reeds.csv')
    r2.scenario[scen].addMaterial('silver', file=r'materialsubsets\baseline_material_silver_Reeds.csv')
    r2.scenario[scen].addMaterial('copper', file=r'materialsubsets\baseline_material_copper_Reeds.csv')
    r2.scenario[scen].addMaterial('aluminum', file=r'materialsubsets\baseline_material_aluminium_Reeds.csv')


# In[41]:


IRENA= False
PERFECTMFG = True

mats = ['glass', 'silicon','silver','copper','aluminum']

ELorRL = 'EL'
if IRENA:
    if ELorRL == 'RL':
        weibullInputParams = {'alpha': 5.3759, 'beta':30}  # Regular-loss scenario IRENA
    if ELorRL == 'EL':
        weibullInputParams = {'alpha': 2.49, 'beta':30}  # Regular-loss scenario IRENA
    
    if PERFECTMFG:
        for jj in range (0, len(r1.scenario.keys())):
            scen = Type[jj]+'_'+STATEs[jj]
            r1.scenario[scen].data['mod_lifetime'] = 40
            r1.scenario[scen].data['mod_MFG_eff'] = 100.0
            r2.scenario[scen].data['mod_lifetime'] = 40
            r2.scenario[scen].data['mod_MFG_eff'] = 100.0

            for kk in range(0, len(mats)):
                mat = mats[kk]
                r1.scenario[scen].material[mat].materialdata['mat_MFG_eff'] = 100.0    
                r2.scenario[scen].material[mat].materialdata['mat_MFG_eff'] = 100.0    

    
    r1.calculateMassFlow(weibullInputParams=weibullInputParams)
    r2.calculateMassFlow(weibullInputParams=weibullInputParams)
    title_Method = 'Irena_'+ELorRL
else:
    r1.calculateMassFlow()
    r2.calculateMassFlow()
    title_Method = 'PVICE'


# # OPEN EI

# In[42]:


kk=0
SFScenarios = [r1, r2]
SFScenarios[kk].name


# In[43]:


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
                    scen = Type[zz]+'_'+STATEs[zz]
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
        foo['@scenario|Electric Futures'] = SFScenarios[kk].name 
        foo['@filter|Install Type'] = Type[zz]
        foo['@timeseries|Year'] = SFScenarios[kk].scenario[scen].data.year

        scenariolist = scenariolist.append(foo)   

cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
cols = [scenariolist.columns[-1]] + [col for col in scenariolist if col != scenariolist.columns[-1]]
scenariolist = scenariolist[cols]
#scenariolist = scenariolist/1000000 # Converting to Metric Tons
#scenariolist = scenariolist.applymap(lambda x: round(x, N - int(np.floor(np.log10(abs(x))))))
#scenariolist = scenariolist.applymap(lambda x: int(x))
scenariolist.to_csv('OPEN EI '+title_Method+' ELECTRIF FUTURES.csv', index=False)

print("Done")


# In[ ]:




