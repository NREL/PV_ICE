#!/usr/bin/env python
# coding: utf-8

# # 6 - Sensitivity Analysis

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'SensitivityAnalysis')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


MATERIALS = ['glass','silver','silicon', 'copper','aluminium']
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'baseline_modules_mass_US.csv' 
MATERIALBASELINE = r'..\..\baselines\baseline_material_mass_'+MATERIAL+'.csv'


# In[3]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd


# In[4]:


# This information helps with debugging and getting support :)
import sys, platform
print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# In[5]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[6]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='baseline', massmodulefile=MODULEBASELINE)
r1.scenario['baseline'].addMaterial(MATERIAL, MATERIALBASELINE)


# ### Change Values:
# 

# In[7]:


## Change VAlues to 50:
'''
mat_virgin_eff	mat_massperm2	mat_MFG_eff	mat_MFG_scrap_Recycled	mat_MFG_scrap_Recycling_eff	mat_MFG_scrap_Recycled_into_HQ	mat_MFG_scrap_Recycled_into_HQ_Reused4MFG	mat_EOL_collected_Recycled	mat_EOL_Recycling_eff	mat_EOL_Recycled_into_HQ	mat_EOL_RecycledHQ_Reused4MFG
mod_MFG_eff	mod_EOL_collection_eff	mod_EOL_collected_recycled	mod_Repowering	mod_Repairing
mod_lifetime = 25
mod_reliability_t50 = 31
mod_reliability_t90 = 36
mod_degradation = 0.6
''';


# ### Load Scenarios and Parameters

# In[8]:


ss = pd.read_excel(r'..\..\..\tests\sensitivity_test.xlsx')
ss


# #### Create Scenarios

# In[9]:


for i in range (0, len(ss)):
    stage = ss['stage'][i]
    stage_highname = stage+'_high'
    stage_lowname = stage+'_low'
    
    if ss['Database'][i] == 'material':

        if ss['Modification'][i] == 'single':

            # Create Scenarios
            r1.createScenario(name=stage_highname, massmodulefile=MODULEBASELINE)
            r1.scenario[stage_highname].addMaterial(MATERIAL, massmatfile=MATERIALBASELINE)
            r1.createScenario(name=stage_lowname, massmodulefile=MODULEBASELINE)
            r1.scenario[stage_lowname].addMaterial(MATERIAL, massmatfile=MATERIALBASELINE)

            # Modify Values Absolute
            if ss['AbsRel'][i] == 'abs':
                # Modify Values High
                r1.scenario[stage_highname].material[MATERIAL].matdataIn_m[ss['variables'][i]] = r1.scenario[stage_highname].material[MATERIAL].matdataIn_m[ss['variables'][i]] + ss['High'][i]
                r1.scenario[stage_highname].material[MATERIAL].matdataIn_m[ss['variables'][i]][r1.scenario[stage_highname].material[MATERIAL].matdataIn_m[ss['variables'][i]]>100.0] =100.0
                # Modify Values Low
                r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m[ss['variables'][i]] = r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m[ss['variables'][i]] + ss['Low'][i]
                r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m[ss['variables'][i]][r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m[ss['variables'][i]]<0.0] = 0.0

            # Modify Values Relative
            if ss['AbsRel'][i] == 'rel':
                # Modify Values High
                high_change = 1+ss['High'][i]/100.0
                low_change = 1+ss['Low'][i]/100.0
                r1.scenario[stage_highname].material[MATERIAL].matdataIn_m = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].matdataIn_m, 
                             stage=ss['variables'][i], improvement=high_change, start_year=0)
                # Modify Values Low
                r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m, 
                             stage=ss['variables'][i], improvement=low_change, start_year=0)
          
        # If multiple, assumed all modifications are ABSOLUTE
        if ss['Modification'][i] == 'multiple':
            varmods = [x.strip() for x in ss['variables'][i].split(',')]
            
            # Create Scenarios
            r1.createScenario(name=stage_highname, massmodulefile=MODULEBASELINE)
            r1.scenario[stage_highname].addMaterial(MATERIAL, massmatfile=MATERIALBASELINE)
            r1.createScenario(name=stage_lowname, massmodulefile=MODULEBASELINE)
            r1.scenario[stage_lowname].addMaterial(MATERIAL, massmatfile=MATERIALBASELINE)
            
            for j in range(0, len(varmods)):
                # Modify Values High
                r1.scenario[stage_highname].material[MATERIAL].matdataIn_m[varmods[j]] = r1.scenario[stage_highname].material[MATERIAL].matdataIn_m[varmods[j]] + ss['High'][i] 
                r1.scenario[stage_highname].material[MATERIAL].matdataIn_m[varmods[j]][r1.scenario[stage_highname].material[MATERIAL].matdataIn_m[varmods[j]]>100.0] =100.0
                # Modify Values Low
                r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m[varmods[j]] = r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m[varmods[j]] + ss['Low'][i]
                r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m[varmods[j]][r1.scenario[stage_lowname].material[MATERIAL].matdataIn_m[varmods[j]]<0.0] = 0.0

        
    if ss['Database'][i] == 'module':
        
        
        if ss['Modification'][i] == 'single':

            # Create Scenarios
            r1.createScenario(name=stage_highname, massmodulefile=MODULEBASELINE)
            r1.scenario[stage_highname].addMaterial(MATERIAL, massmatfile=MATERIALBASELINE)
            r1.createScenario(name=stage_lowname, massmodulefile=MODULEBASELINE)
            r1.scenario[stage_lowname].addMaterial(MATERIAL, massmatfile=MATERIALBASELINE) 
            # Modify Values Absolute
            if ss['AbsRel'][i] == 'abs':


                r1.scenario[stage_highname].dataIn_m[ss['variables'][i]] = r1.scenario[stage_highname].dataIn_m[ss['variables'][i]] + ss['High'][i]
                r1.scenario[stage_highname].dataIn_m[ss['variables'][i]][r1.scenario[stage_highname].dataIn_m[ss['variables'][i]]>100.0] =100.0


                r1.scenario[stage_lowname].dataIn_m[ss['variables'][i]] = r1.scenario[stage_lowname].dataIn_m[ss['variables'][i]] + ss['Low'][i]
                r1.scenario[stage_lowname].dataIn_m[ss['variables'][i]][r1.scenario[stage_lowname].dataIn_m[ss['variables'][i]]<0.0] = 0.0

            # Modify Values Relative
            if ss['AbsRel'][i] == 'rel':
                high_change = 1+ss['High'][i]/100.0
                low_change = 1+ss['Low'][i]/100.0
                r1.scenario[stage_highname].dataIn_m = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].dataIn_m, 
                                                 stage=ss['variables'][i], improvement=high_change, start_year=0)
                r1.scenario[stage_lowname].dataIn_m = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].dataIn_m, 
                                                 stage=ss['variables'][i], improvement=low_change, start_year=0)
        
        # If multiple, assumed all modifications are ABSOLUTE
        if ss['Modification'][i] == 'multiple':
            varmods = [x.strip() for x in ss['variables'][i].split(',')]

            r1.createScenario(name=stage_highname, massmodulefile=MODULEBASELINE)
            r1.scenario[stage_highname].addMaterial(MATERIAL, massmatfile=MATERIALBASELINE)
            r1.createScenario(name=stage_lowname, massmodulefile=MODULEBASELINE)
            r1.scenario[stage_lowname].addMaterial(MATERIAL, massmatfile=MATERIALBASELINE)
            
            for j in range(0, len(varmods)):
                r1.scenario[stage_highname].dataIn_m[varmods[j]] = r1.scenario[stage_highname].dataIn_m[varmods[j]] + ss['High'][i] 
                r1.scenario[stage_highname].dataIn_m[varmods[j]][r1.scenario[stage_highname].dataIn_m[varmods[j]]>100.0] =100.0

                r1.scenario[stage_lowname].dataIn_m[varmods[j]] = r1.scenario[stage_lowname].dataIn_m[varmods[j]] + ss['Low'][i]
                r1.scenario[stage_lowname].dataIn_m[varmods[j]][r1.scenario[stage_lowname].dataIn_m[varmods[j]]<0.0] = 0.0

        


# # MASS FLOWS

# In[10]:


r1.calculateMassFlow()


# In[11]:


r1.scenario['mat_massperm2_high'].material['glass'].matdataOut_m.head()


# In[12]:


scenarios = list(r1.scenario.keys())
scenarios


# #### Compile Changes

# In[15]:


virginStock_Changes = []
waste_Changes = []
installedCapacity_Changes = []
virginStockRAW_Changes = []

virgin_keyword = 'mat_Virgin_Stock'
waste_keyword = 'mat_Total_Landfilled'
installs_keyword = 'Effective_Capacity_[W]'
viring_raw_keyword = 'mat_Virgin_Stock_Raw'

virginStock_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].matdataOut_m[virgin_keyword].sum()
virginStockRAW_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].matdataOut_m[viring_raw_keyword].sum()

# Installed Capacity is already cumulative so no need to sum or cumsum.
waste_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].matdataOut_m[waste_keyword].sum()
installedCapacity_baselined_2050 = r1.scenario['baseline'].dataOut_m[installs_keyword].iloc[-1]

for i in range (1, len(scenarios)):
    stage_name = scenarios[i]
    virginStock_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].matdataOut_m[virgin_keyword].sum()/virginStock_baseline_cum2050,5)-100)
    virginStockRAW_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].matdataOut_m[viring_raw_keyword].sum()/virginStockRAW_baseline_cum2050,5)-100)

    waste_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].matdataOut_m[waste_keyword].sum()/waste_baseline_cum2050,5)-100)
    installedCapacity_Changes.append(round(100*r1.scenario[stage_name].dataOut_m[installs_keyword].iloc[-1]/installedCapacity_baselined_2050,5)-100)


# In[16]:


stages = scenarios[1::] # removing baseline as we want a dataframe with only changes


# In[17]:


df2 = pd.DataFrame(list(zip(virginStock_Changes, virginStockRAW_Changes, waste_Changes, installedCapacity_Changes)), 
               columns=['Virgin Needs Change', 'Virgin Stock Raw Change', 'Waste Change', 'InstalledCapacity Change'],index=stages) 


# In[18]:


variables_description = {'mat_virgin_eff': "Material Virgin Efficiency",
    'mat_massperm2': "Mass per m2",
    'mat_MFG_eff': "Efficiency of Material Use during Module Manufacturing",
    'mat_MFG_scrap_Recycled': "% of Material Scrap from Manufacturing that undergoes Recycling",
    'mat_MFG_scrap_Recycling_eff': "Recycling Efficiency of the Material Scrap",
    'mat_MFG_scrap_Recycling_eff': "% of Recycled Material Scrap that is high quality",
    'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG': "% of high quality Recycled Material Scrap reused for manufacturing",
    'new_Installed_Capacity_[MW]': "New Installed Capacity",
    'mod_eff': "Module Efficiency",
    'mod_EOL_collection_eff': "Collection Efficiency of EoL Modules",
    'mod_EOL_collected_recycled': "% of collected modules that are recycled",
    'mod_Repowering': "% of EOL modules that are repowered",
    'mod_Repairing' : "% of failed modules that undergo repair",
    'mat_EOL_collected_Recycled': "% of times material is chosen to be recycled",
    'mat_EOL_Recycling_eff': "Efficiency of material recycling",
    'mat_EOL_Recycled_into_HQ': "Fraction of recycled material that is high quality",
    'mat_EOL_RecycledHQ_Reused4MFG': "Fraction of high quality recycled material that is reused for manufacturing",
    'EOL_CE_Pathways': "Overall improvement on EoL Circularity Pathways",
    'Reliability_and_CE_Pathways': "Overall improvement on Eol Circularity Pathways + Reliability and Lifetime",
    'mat_EOL_Recycling_Overall_Improvement': "Overall Improvement on EoL Recycling Loop"}


# In[19]:


df2_Pos = df2[['high' in s for s in df2.index]].copy()
df2_Pos.index = df2_Pos.index.str.replace("_high", "")

col_verbose = []

for i in range (0, len(df2_Pos)):
    if df2_Pos.index[i] in variables_description:
        col_verbose.append(variables_description[df2_Pos.index[i]])
    else:
        col_verbose.append("")
        
df2_Pos['Description'] = col_verbose     
df2_Pos = df2_Pos.reset_index()
df2_Pos = df2_Pos.rename(columns={'index':'variable'})
df2_Pos


# In[20]:


df2_Neg = df2[['low' in s for s in df2.index]].copy()
df2_Neg.index = df2_Neg.index.str.replace("_low", "")

col_verbose = []

for i in range (0, len(df2_Neg)):
    if df2_Neg.index[i] in variables_description:
        col_verbose.append(variables_description[df2_Neg.index[i]])
    else:
        col_verbose.append("")

df2_Neg['Description'] = col_verbose
df2_Neg = df2_Neg.reset_index()
df2_Neg = df2_Neg.rename(columns={'index':'variable'})
df2_Neg


# ### Optional: Print Values for a Senki Diagram, 1 year

# https://observablehq.com/@mbostock/flow-o-matic
# 
# The below code has not been updated for the latest variable names yet.

# In[28]:


'''
mat_UsedSuccessfullyinModuleManufacturing = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_UsedSuccessfullyinModuleManufacturing'].sum()
mat_MFG_Scrap = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_MFG_Scrap'].sum()
normvalue = (mat_UsedSuccessfullyinModuleManufacturing+mat_MFG_Scrap)/100

mat_UsedSuccessfullyinModuleManufacturing = mat_UsedSuccessfullyinModuleManufacturing/normvalue
mat_MFG_Scrap = mat_MFG_Scrap/normvalue
mat_MFG_Scrap_Sentto_Recycling = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_MFG_Scrap_Sentto_Recycling'].sum()/normvalue
mat_MFG_Scrap_Landfilled = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_MFG_Scrap_Landfilled'].sum()/normvalue
mat_MFG_Scrap_Recycled_Successfully = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_MFG_Scrap_Recycled_Successfully'].sum()/normvalue
mat_MFG_Scrap_Recycled_Losses_Landfilled = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_MFG_Scrap_Recycled_Losses_Landfilled'].sum()/normvalue
mat_MFG_Recycled_into_HQ = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_MFG_Recycled_into_HQ'].sum()/normvalue
mat_MFG_Recycled_into_OQ = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_MFG_Recycled_into_OQ'].sum()/normvalue
mat_MFG_Recycled_HQ_into_MFG = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_MFG_Recycled_HQ_into_MFG'].sum()/normvalue
mat_MFG_Recycled_HQ_into_OU = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_MFG_Recycled_HQ_into_OU'].sum()/normvalue


# UPDATE NAMES HERE:
mat_modules_NotCollected = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_L0'].sum()/normvalue
#mat_EOL_Collected = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_modules_Collected'].sum()/normvalue
#mat_still_Installed = mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected-mat_EOL_Collected
#mat_modules_Recycled = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_modules_Recycled'].sum()/normvalue

mat_EOL_collected_Recycled = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_EOL_collected_Recycled'].sum()/normvalue
mat_EOL_collected_notRecycled = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_modules_NotRecycled'].sum()/normvalue
mat_EOL_NotRecycled_Landfilled = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_EOL_NotRecycled_Landfilled'].sum()/normvalue
mat_EOL_sento_Recycling = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_EOL_sento_Recycling'].sum()/normvalue
mat_EOL_Recycled = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_EOL_Recycled'].sum()/normvalue
mat_EOL_Recycled_Losses_Landfilled = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_EOL_Recycled_Losses_Landfilled'].sum()/normvalue
mat_EOL_Recycled_2_HQ = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_EOL_Recycled_2_HQ'].sum()/normvalue
mat_EOL_Recycled_2_OQ = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_EOL_Recycled_2_OQ'].sum()/normvalue
mat_EoL_Recycled_HQ_into_MFG = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_EoL_Recycled_HQ_into_MFG'].sum()/normvalue
mat_EOL_Recycled_HQ_into_OU = r1.scenario['baseline'].material[MATERIAL].matdataOut_m['mat_EOL_Recycled_HQ_into_OU'].sum()/normvalue

''';


# In[30]:


'''print('Virgin Stock,Modules,',mat_UsedSuccessfullyinModuleManufacturing)

print('Modules, Installed Capacity,',mat_still_Installed)
print('Modules,EOL Not Collected,',mat_modules_NotCollected)
print('EOL Not Collected,Waste,',mat_modules_NotCollected)
print('Modules,EOL Collected,',mat_EOL_Collected)

print('EOL Collected,Waste,',mat_EOL_NotRecycled_Landfilled) # Material not recycled
print('EOL Collected,Recycled,',mat_modules_Recycled, ', #da4f81')
print('Recycled,Succesful,', mat_EOL_Recycled, ', #da4f81')
print('Recycled,Waste,', mat_EOL_collected_notRecycled+mat_EOL_Recycled_Losses_Landfilled)

print('Succesful,Closed Loop,',mat_EoL_Recycled_HQ_into_MFG, ', #da4f81')
print('Succesful,Open Loop,',mat_EOL_Recycled_2_OQ+mat_EOL_Recycled_HQ_into_OU)

print('Virgin Stock,Manufacturing Scrap,',mat_MFG_Scrap)
print('Manufacturing Scrap,Recycled,',mat_MFG_Scrap_Sentto_Recycling, ', #da4f81')
print('Manufacturing Scrap,Waste,',mat_MFG_Scrap_Landfilled)
print('Recycled,Succesful,',mat_MFG_Scrap_Recycled_Successfully, ', #da4f81')
print('Recycled,Waste,',mat_MFG_Scrap_Recycled_Losses_Landfilled)
print('Succesful,Closed Loop,',mat_MFG_Recycled_HQ_into_MFG, ', #da4f81')
print('Succesful,Open Loop,',mat_MFG_Recycled_into_OQ+mat_MFG_Recycled_HQ_into_OU)
''';


# In[32]:


# Senki with more detail:
'''
print('Virgin Stock,Modules,',mat_UsedSuccessfullyinModuleManufacturing)

print('Modules, Installed Capacity,',mat_still_Installed)
print('Modules,EOL Not Collected,',mat_modules_NotCollected)
print('EOL Not Collected,Waste,',mat_modules_NotCollected)
print('Modules,EOL Collected,',mat_EOL_Collected)

print('EOL Collected,Waste,',mat_EOL_NotRecycled_Landfilled) # Material not recycled
print('EOL Collected,Sent to Recycling,',mat_modules_Recycled, ', #da4f81')
print('Sent to Recycling,Material Recycled,', mat_EOL_sento_Recycling, ', #da4f81')

print('Material Recycled,Recycled,',mat_EOL_Recycled, ', #da4f81')
print('Material Recycled,Waste,',mat_EOL_Recycled_Losses_Landfilled)

print('Recycled,HQ,',mat_EOL_Recycled_2_HQ, ', #da4f81')
print('Recycled,OQ,',mat_EOL_Recycled_2_OQ)
print('HQ,HQ into Mfg,',mat_EoL_Recycled_HQ_into_MFG, ', #da4f81')
print('HQ,HQ Other Uses,',mat_EOL_Recycled_HQ_into_OU)

print('Virgin Stock,Manufacturing Scrap,',mat_MFG_Scrap)
print('Manufacturing Scrap,Sent to Recycling,',mat_MFG_Scrap_Sentto_Recycling, ', #da4f81')
print('Manufacturing Scrap,Waste,',mat_MFG_Scrap_Landfilled)
print('Sent to Recycling,Recycled,',mat_MFG_Scrap_Recycled_Successfully, ', #da4f81')
print('Sent to Recycling,Waste,',mat_MFG_Scrap_Recycled_Losses_Landfilled)
print('Recycled,HQ,',mat_MFG_Recycled_into_HQ, ', #da4f81')
print('Recycled,OQ,',mat_MFG_Recycled_into_OQ)
print('HQ,HQ into Mfg,',mat_MFG_Recycled_HQ_into_MFG, ', #da4f81')
print('HQ,HQ Other Uses,',mat_MFG_Recycled_HQ_into_OU)
''';


# # Modifing the installed capacity to stay fixed at BASELINE
# Needs to run each year becuase it needs to calculate the acumulated installs and deads.

# In[ ]:


Diff_Installment = []
for i in range (0, len(r1.scenario['baseline'].dataIn_m)):
    for jj in range (1, len(list(r1.scenario.keys()))):
        scen = list(r1.scenario.keys())[jj]
        Diff_Installment = ( (r1.scenario['baseline'].dataOut_m['Effective_Capacity_[W]'][i] - 
                             r1.scenario[scen].dataOut_m['Effective_Capacity_[W]'][i])/1000000 )  # MWATTS
        r1.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][i] += Diff_Installment
    r1.calculateMassFlow()
mat


# #### Compile Changes

# In[ ]:


virginStock_Changes = []
waste_Changes = []
installedCapacity_Changes = []
virginStockRAW_Changes = []

virgin_keyword = 'mat_Virgin_Stock'
waste_keyword = 'mat_Total_Landfilled'
installs_keyword = 'Effective_Capacity_[W]'
viring_raw_keyword = 'mat_Virgin_Stock_Raw'

virginStock_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].matdataOut_m[virgin_keyword].sum()
virginStockRAW_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].matdataOut_m[viring_raw_keyword].sum()

# Installed Capacity is already cumulative so no need to sum or cumsum.
waste_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].matdataOut_m[waste_keyword].sum()
installedCapacity_baselined_2050 = r1.scenario['baseline'].dataOut_m[installs_keyword].iloc[-1]

for i in range (1, len(scenarios)):
    stage_name = scenarios[i]
    virginStock_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].matdataOut_m[virgin_keyword].sum()/virginStock_baseline_cum2050,5)-100)
    virginStockRAW_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].matdataOut_m[viring_raw_keyword].sum()/virginStockRAW_baseline_cum2050,5)-100)

    waste_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].matdataOut_m[waste_keyword].sum()/waste_baseline_cum2050,5)-100)
    installedCapacity_Changes.append(round(100*r1.scenario[stage_name].dataOut_m[installs_keyword].iloc[-1]/installedCapacity_baselined_2050,5)-100)


# In[ ]:


stages = scenarios[1::] # removing baseline as we want a dataframe with only changes


# In[ ]:


df = pd.DataFrame(list(zip(virginStock_Changes, virginStockRAW_Changes, waste_Changes, installedCapacity_Changes)), 
               columns=['Virgin Needs Change', 'Virgin Stock Raw Change', 'Waste Change', 'InstalledCapacity Change'],index=stages) 


# #### Present Results

# In[ ]:


df_Pos = df[['high' in s for s in df.index]].copy()
df_Pos.index = df_Pos.index.str.replace("_high", "")

col_verbose = []

for i in range (0, len(df_Pos)):
    if df_Pos.index[i] in variables_description:
        col_verbose.append(variables_description[df_Pos.index[i]])
    else:
        col_verbose.append("")
        
df_Pos['Description'] = col_verbose     
df_Pos = df_Pos.reset_index()
df_Pos = df_Pos.rename(columns={'index':'variable'})


# In[ ]:


df_Neg = df[['low' in s for s in df.index]].copy()
df_Neg.index = df_Neg.index.str.replace("_low", "")

col_verbose = []

for i in range (0, len(df_Neg)):
    if df_Neg.index[i] in variables_description:
        col_verbose.append(variables_description[df_Neg.index[i]])
    else:
        col_verbose.append("")

df_Neg['Description'] = col_verbose
df_Neg = df_Neg.reset_index()
df_Neg = df_Neg.rename(columns={'index':'variable'})


# In[ ]:


print("Keeping Installs, the modifications to Virgin Needs, Virgin STock and Waste")
df_Pos[df_Pos['InstalledCapacity Change']!=0.000]


# In[ ]:


print("Keeping Installs, the modifications to Virgin Needs, Virgin STock and Waste")
df_Neg[df_Neg['InstalledCapacity Change']!=0.000]


# In[ ]:




