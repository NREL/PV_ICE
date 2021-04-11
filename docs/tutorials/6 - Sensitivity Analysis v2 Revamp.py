#!/usr/bin/env python
# coding: utf-8

# # 6 - Sensitivity Analysis v2

# In[1]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


MATERIALS = ['glass','silver','silicon', 'copper','aluminium']
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'..\baselines\baseline_modules_US.csv' 
MATERIALBASELINE = r'..\baselines\baseline_material_'+MATERIAL+'.csv'


# In[3]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd


# In[4]:


PV_ICE.__version__


# In[5]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[6]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='baseline', file=MODULEBASELINE)
r1.scenario['baseline'].addMaterial(MATERIAL, file=MATERIALBASELINE)


# ### Change VAlues to 50:
# 

# In[7]:


## Change VAlues to 50:
'''
mat_virgin_eff	mat_massperm2	mat_MFG_eff	mat_MFG_scrap_Recycled	mat_MFG_scrap_Recycling_eff	mat_MFG_scrap_Recycled_into_HQ	mat_MFG_scrap_Recycled_into_HQ_Reused4MFG	mat_EOL_collected_Recycled	mat_EOL_Recycling_eff	mat_EOL_Recycled_into_HQ	mat_EOL_RecycledHQ_Reused4MFG
mod_MFG_eff	mod_EOL_collection_eff	mod_EOL_collected_recycled	mod_Repowering	mod_Repairing
mod_lifetime = 25
mod_reliability_t50 = 31
mod_reliability_t90 = 36
od_degradation = 0.6
''';


# ### Load Scenarios and Parameters

# In[8]:


ss = pd.read_excel(r'..\..\tests\sensitivity_test.xlsx')
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
            r1.createScenario(name=stage_highname, file=MODULEBASELINE)
            r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
            r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)

            # Modify Values Absolute
            if ss['AbsRel'][i] == 'abs':
                # Modify Values High
                r1.scenario[stage_highname].material[MATERIAL].materialdata[ss['variables'][i]] = r1.scenario[stage_highname].material[MATERIAL].materialdata[ss['variables'][i]] + ss['High'][i]
                r1.scenario[stage_highname].material[MATERIAL].materialdata[ss['variables'][i]][r1.scenario[stage_highname].material[MATERIAL].materialdata[ss['variables'][i]]>100.0] =100.0
                # Modify Values Low
                r1.scenario[stage_lowname].material[MATERIAL].materialdata[ss['variables'][i]] = r1.scenario[stage_lowname].material[MATERIAL].materialdata[ss['variables'][i]] + ss['Low'][i]
                r1.scenario[stage_lowname].material[MATERIAL].materialdata[ss['variables'][i]][r1.scenario[stage_lowname].material[MATERIAL].materialdata[ss['variables'][i]]<0.0] = 0.0

            # Modify Values Relative
            if ss['AbsRel'][i] == 'rel':
                # Modify Values High
                high_change = 1+ss['High'][i]/100.0
                low_change = 1+ss['Low'][i]/100.0
                r1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=ss['variables'][i], improvement=high_change, start_year=0)
                # Modify Values Low
                r1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=ss['variables'][i], improvement=low_change, start_year=0)
          
        # If multiple, assumed all modifications are ABSOLUTE
        if ss['Modification'][i] == 'multiple':
            varmods = [x.strip() for x in ss['variables'][i].split(',')]
            
            # Create Scenarios
            r1.createScenario(name=stage_highname, file=MODULEBASELINE)
            r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
            r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            
            for j in range(0, len(varmods)):
                # Modify Values High
                r1.scenario[stage_highname].material[MATERIAL].materialdata[varmods[j]] = r1.scenario[stage_highname].material[MATERIAL].materialdata[varmods[j]] + ss['High'][i] 
                r1.scenario[stage_highname].material[MATERIAL].materialdata[varmods[j]][r1.scenario[stage_highname].material[MATERIAL].materialdata[varmods[j]]>100.0] =100.0
                # Modify Values Low
                r1.scenario[stage_lowname].material[MATERIAL].materialdata[varmods[j]] = r1.scenario[stage_lowname].material[MATERIAL].materialdata[varmods[j]] + ss['Low'][i]
                r1.scenario[stage_lowname].material[MATERIAL].materialdata[varmods[j]][r1.scenario[stage_lowname].material[MATERIAL].materialdata[varmods[j]]<0.0] = 0.0

        
    if ss['Database'][i] == 'module':
        
        
        if ss['Modification'][i] == 'single':

            # Create Scenarios
            r1.createScenario(name=stage_highname, file=MODULEBASELINE)
            r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
            r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE) 
            # Modify Values Absolute
            if ss['AbsRel'][i] == 'abs':


                r1.scenario[stage_highname].data[ss['variables'][i]] = r1.scenario[stage_highname].data[ss['variables'][i]] + ss['High'][i]
                r1.scenario[stage_highname].data[ss['variables'][i]][r1.scenario[stage_highname].data[ss['variables'][i]]>100.0] =100.0


                r1.scenario[stage_lowname].data[ss['variables'][i]] = r1.scenario[stage_lowname].data[ss['variables'][i]] + ss['Low'][i]
                r1.scenario[stage_lowname].data[ss['variables'][i]][r1.scenario[stage_lowname].data[ss['variables'][i]]<0.0] = 0.0

            # Modify Values Relative
            if ss['AbsRel'][i] == 'rel':
                high_change = 1+ss['High'][i]/100.0
                low_change = 1+ss['Low'][i]/100.0
                r1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_highname].data, 
                                                 stage=ss['variables'][i], improvement=high_change, start_year=0)
                r1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(r1.scenario[stage_lowname].data, 
                                                 stage=ss['variables'][i], improvement=low_change, start_year=0)
        
        # If multiple, assumed all modifications are ABSOLUTE
        if ss['Modification'][i] == 'multiple':
            varmods = [x.strip() for x in ss['variables'][i].split(',')]

            r1.createScenario(name=stage_highname, file=MODULEBASELINE)
            r1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            r1.createScenario(name=stage_lowname, file=MODULEBASELINE)
            r1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            
            for j in range(0, len(varmods)):
                r1.scenario[stage_highname].data[varmods[j]] = r1.scenario[stage_highname].data[varmods[j]] + ss['High'][i] 
                r1.scenario[stage_highname].data[varmods[j]][r1.scenario[stage_highname].data[varmods[j]]>100.0] =100.0

                r1.scenario[stage_lowname].data[varmods[j]] = r1.scenario[stage_lowname].data[varmods[j]] + ss['Low'][i]
                r1.scenario[stage_lowname].data[varmods[j]][r1.scenario[stage_lowname].data[varmods[j]]<0.0] = 0.0

        


# # MASS FLOWS

# In[10]:


r1.calculateMassFlow()


# In[11]:


r1.scenario['baseline'].material['glass'].materialdata.head()


# In[12]:


r1.scenario['mat_massperm2_high'].material['glass'].materialdata.head()


# In[13]:


scenarios = list(r1.scenario.keys())
scenarios


# #### Compile Changes

# In[14]:


virginStock_Changes = []
waste_Changes = []
installedCapacity_Changes = []
virginStockRAW_Changes = []

virgin_keyword = 'mat_Virgin_Stock'
waste_keyword = 'mat_Total_Landfilled'
installs_keyword = 'Installed_Capacity_[W]'
viring_raw_keyword = 'mat_Virgin_Stock_Raw'

virginStock_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].materialdata[virgin_keyword].sum()
virginStockRAW_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].materialdata[viring_raw_keyword].sum()

# Installed Capacity is already cumulative so no need to sum or cumsum.
waste_baseline_cum2050 = r1.scenario['baseline'].material[MATERIAL].materialdata[waste_keyword].sum()
installedCapacity_baselined_2050 = r1.scenario['baseline'].data[installs_keyword].iloc[-1]

for i in range (1, len(scenarios)):
    stage_name = scenarios[i]
    virginStock_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].materialdata[virgin_keyword].sum()/virginStock_baseline_cum2050,5)-100)
    virginStockRAW_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].materialdata[viring_raw_keyword].sum()/virginStockRAW_baseline_cum2050,5)-100)

    waste_Changes.append(round(100*r1.scenario[stage_name].material[MATERIAL].materialdata[waste_keyword].sum()/waste_baseline_cum2050,5)-100)
    installedCapacity_Changes.append(round(100*r1.scenario[stage_name].data[installs_keyword].iloc[-1]/installedCapacity_baselined_2050,5)-100)


# In[15]:


stages = scenarios[1::] # removing baseline as we want a dataframe with only changes


# In[16]:


df = pd.DataFrame(list(zip(virginStock_Changes, virginStockRAW_Changes, waste_Changes, installedCapacity_Changes)), 
               columns=['Virgin Needs Change', 'Virgin Stock Raw Change', 'Waste Change', 'InstalledCapacity Change'],index=stages) 


# In[17]:


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


# In[18]:


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
df_Pos


# In[19]:


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
df_Neg


# # Print Values for a Senki Diagram, 1 year

# https://observablehq.com/@mbostock/flow-o-matic

# In[20]:


r1.scenario['baseline'].data.keys()


# In[21]:


r1.scenario['baseline'].material[MATERIAL].materialdata.keys()


# In[23]:


mat_UsedSuccessfullyinModuleManufacturing = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_UsedSuccessfullyinModuleManufacturing'].sum()
mat_MFG_Scrap = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap'].sum()
mat_MFG_Scrap_Sentto_Recycling = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap_Sentto_Recycling'].sum()
mat_MFG_Scrap_Landfilled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap_Landfilled'].sum()
mat_MFG_Scrap_Recycled_Successfully = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap_Recycled_Successfully'].sum()
mat_MFG_Scrap_Recycled_Losses_Landfilled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Scrap_Recycled_Losses_Landfilled'].sum()
mat_MFG_Recycled_into_HQ = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Recycled_into_HQ'].sum()
mat_MFG_Recycled_into_OQ = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Recycled_into_OQ'].sum()
mat_MFG_Recycled_HQ_into_MFG = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Recycled_HQ_into_MFG'].sum()
mat_MFG_Recycled_HQ_into_OU = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_Recycled_HQ_into_OU'].sum()


mat_modules_NotCollected = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_modules_NotCollected'].sum()
mat_EOL_Collected = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_modules_NotCollected'].sum()
mat_still_Installed = mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected-mat_EOL_Collected

mat_EOL_collected_Recycled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_collected_Recycled'].sum()
mat_EOL_collected_notRecycled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_modules_NotRecycled'].sum()
mat_EOL_NotRecycled_Landfilled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_NotRecycled_Landfilled'].sum()
mat_EOL_Recycled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled'].sum()
mat_EOL_Recycled_Losses_Landfilled = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled_Losses_Landfilled'].sum()
mat_EOL_Recycled_2_HQ = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled_2_HQ'].sum()
mat_EOL_Recycled_2_OQ = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled_2_OQ'].sum()
mat_EoL_Recycled_HQ_into_MFG = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EoL_Recycled_HQ_into_MFG'].sum()
mat_EOL_Recycled_HQ_into_OU = r1.scenario['baseline'].material[MATERIAL].materialdata['mat_EOL_Recycled_HQ_into_OU'].sum()


# mat_Virgin_Stock, mat_UsedSuccessfullyinModuleManufacturing
# mat_Virgin_Stock, mat_MFG_Scrap
# mat_MFG_Scrap, mat_MFG_Scrap_Sentto_Recycling
# mat_MFG_Scrap, mat_MFG_Scrap_Landfilled
# mat_MFG_Scrap_Sentto_Recycling, mat_MFG_Scrap_Recycled_Successfully
# mat_MFG_Scrap_Sentto_Recycling, mat_MFG_Scrap_Recycled_Losses_Landfilled
# mat_MFG_Scrap_Recycled_Successfully, mat_MFG_Recycled_into_HQ
# mat_MFG_Scrap_Recycled_Successfully, mat_MFG_Recycled_into_OQ
# mat_MFG_Recycled_into_HQ, mat_MFG_Recycled_HQ_into_MFG
# mat_MFG_Recycled_into_HQ, mat_MFG_Recycled_HQ_into_OU
# 
# mat_UsedSuccessfullyinModuleManufacturing, mat_modules_NotCollected
# mat_UsedSuccessfullyinModuleManufacturing, (mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected) # mat collected
# (mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected), mat_EOL_collected_Recycled
# (mat_UsedSuccessfullyinModuleManufacturing-mat_modules_NotCollected), mat_EOL_NotRecycled_Landfilled
# mat_EOL_collected_Recycled, mat_EOL_Recycled
# mat_EOL_collected_Recycled, mat_EOL_Recycled_Losses_Landfilled
# mat_EOL_Recycled, mat_EOL_Recycled_2_HQ
# mat_EOL_Recycled, mat_EOL_Recycled_2_OQ
# mat_EOL_Recycled_2_HQ, mat_EoL_Recycled_HQ_into_MFG
# mat_EOL_Recycled_2_HQ, mat_EOL_Recycled_HQ_into_OU
# 

# In[ ]:





# In[ ]:





# In[29]:


print('Virgin Stock,Modules,',mat_UsedSuccessfullyinModuleManufacturing)
print('Virgin Stock,Manufacturing Scrap,',mat_MFG_Scrap)
print('Manufacturing Scrap,Sent to Recycling,',mat_MFG_Scrap_Sentto_Recycling)
print('Manufacturing Scrap,Waste,',mat_MFG_Scrap_Landfilled)
print('Sent to Recycling,Recycled,',mat_MFG_Scrap_Recycled_Successfully)
print('Sent to Recycling,Waste,',mat_MFG_Scrap_Recycled_Losses_Landfilled)
print('Recycled,HQ,',mat_MFG_Recycled_into_HQ)
print('Recycled,OQ,',mat_MFG_Recycled_into_OQ)
print('HQ,HQ_Mfg,',mat_MFG_Recycled_HQ_into_MFG)
print('HQ,HQ Other Uses,',mat_MFG_Recycled_HQ_into_OU)

print('Modules,still_installed,',mat_still_Installed)
print('Modules,mat_modules_NotCollected,',mat_modules_NotCollected)
print('mat_modules_NotCollected,Waste,',mat_modules_NotCollected)
print('Modules,EOL Collected,',mat_EOL_Collected)
print('EOL Collected,Sent to Recycling,',mat_EOL_collected_Recycled)
print('EOL Collected,Waste,',mat_EOL_NotRecycled_Landfilled) # Material not recycled
print('Sent to Recycling,Recycled,',mat_EOL_Recycled)
print('Sent to Recycling,Waste,',mat_EOL_Recycled_Losses_Landfilled)

print('Recycled,HQ,',mat_EOL_Recycled_2_HQ)
print('Recycled,OQ,',mat_EOL_Recycled_2_OQ)
print('HQ,HQ_Mfg,',mat_EoL_Recycled_HQ_into_MFG)
print('HQ,HQ Other Uses,',mat_EOL_Recycled_HQ_into_OU)


# In[ ]:


print('Virgin Stock,Modules,',mat_UsedSuccessfullyinModuleManufacturing)
print('Virgin Stock,Manufacturing Scrap,',mat_MFG_Scrap)
print('Manufacturing Scrap,Sent to Recycling,',mat_MFG_Scrap_Sentto_Recycling)
print('Manufacturing Scrap,Waste,',mat_MFG_Scrap_Landfilled)
print('Sent to Recycling,Recycled,',mat_MFG_Scrap_Recycled_Successfully)
print('Sent to Recycling,Waste,',mat_MFG_Scrap_Recycled_Losses_Landfilled)
print('Recycled,HQ,',mat_MFG_Recycled_into_HQ)
print('Recycled,OQ,',mat_MFG_Recycled_into_OQ)
print('HQ,HQ_Mfg,',mat_MFG_Recycled_HQ_into_MFG)
print('HQ,HQ Other Uses,',mat_MFG_Recycled_HQ_into_OU)

print('Modules,mat_modules_NotCollected,',mat_modules_NotCollected)
print('Modules,EOL Collected,',mat_EOL_Collected)
print('EOL Collected,Sent to Recycling,',mat_EOL_collected_Recycled)
print('EOL Collected,Waste,',mat_EOL_NotRecycled_Landfilled)
print('Sent to Recycling,Recycled,',mat_EOL_Recycled)
print('Sent to Recycling,Waste,',mat_EOL_Recycled_Losses_Landfilled)
print('Recycled,HQ,',mat_EOL_Recycled_2_HQ)
print('Recycled,OQ,',mat_EOL_Recycled_2_OQ)
print('HQ,HQ_Mfg,',mat_EoL_Recycled_HQ_into_MFG)
print('HQ,HQ Other Uses,',mat_EOL_Recycled_HQ_into_OU)


# In[ ]:


print('Virgin Stock,Modules,',mat_UsedSuccessfullyinModuleManufacturing)
print('Virgin Stock,Manufacturing Scrap,',mat_MFG_Scrap)
print('Manufacturing Scrap,Sent to Recycling,',mat_MFG_Scrap_Sentto_Recycling)
print('Manufacturing Scrap,Waste,',mat_MFG_Scrap_Landfilled)
print('Sent to Recycling,Recycled,',mat_MFG_Scrap_Recycled_Successfully)
print('Sent to Recycling,Waste,',mat_MFG_Scrap_Recycled_Losses_Landfilled)
print('Recycled,HQ,',mat_MFG_Recycled_into_HQ)
print('Recycled,OQ,',mat_MFG_Recycled_into_OQ)
print('HQ,HQ_Mfg,',mat_MFG_Recycled_HQ_into_MFG)
print('HQ,HQ Other Uses,',mat_MFG_Recycled_HQ_into_OU)

print('Modules,mat_modules_NotCollected,',mat_modules_NotCollected)
print('Modules,EOL Collected,',mat_EOL_Collected)
print('EOL Collected,Sent to Recycling,',mat_EOL_collected_Recycled)
print('EOL Collected,Waste,',mat_EOL_NotRecycled_Landfilled)
print('Sent to Recycling,Recycled,',mat_EOL_Recycled)
print('Sent to Recycling,Waste,',mat_EOL_Recycled_Losses_Landfilled)
print('Recycled,HQ,',mat_EOL_Recycled_2_HQ)
print('Recycled,OQ,',mat_EOL_Recycled_2_OQ)
print('HQ,HQ_Mfg,',mat_EoL_Recycled_HQ_into_MFG)
print('HQ,HQ Other Uses,',mat_EOL_Recycled_HQ_into_OU)


# In[ ]:


# Material Baseline Mod. Results
"""
resultkeyword = 'mat_Virgin_Stock'
print("Baseline Cum Value 2050 ", resultkeyword, ": ", r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum())
print("High Eff ", stage, resultkeyword, ": ", int(100*r1.scenario[stage_highname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
print("Low Eff", stage, resultkeyword, ": ", int(100*r1.scenario[stage_lowname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))

resultkeyword = 'mat_Total_Landfilled'
print("Baseline Cum Value 2050 ", resultkeyword, ": ", r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum())
print("High Eff ", stage, resultkeyword, ": ", int(100*r1.scenario[stage_highname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
print("Low Eff", stage, resultkeyword, ": ", int(100*r1.scenario[stage_lowname].material[MATERIAL].materialdata[resultkeyword].sum()/r1.scenario['baseline'].material[MATERIAL].materialdata[resultkeyword].sum()))
r""";


# In[ ]:


"""
fig, ax1 = plt.subplots()
ax1.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Total_Landfilled']/r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Total_Landfilled'], label='base eff')
ax1.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline_HighMatManufEff'].material[MATERIAL].materialdata['mat_Total_Landfilled']/r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Total_Landfilled'], label='high eff')
ax1.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline_lowMatManufEff'].material[MATERIAL].materialdata['mat_Total_Landfilled']/r1.scenario['baseline'].material[MATERIAL].materialdata['mat_Total_Landfilled'], label='low eff')

ax2 = ax1.twinx()
ax2.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline'].material[MATERIAL].materialdata['mat_MFG_eff'], '.')
ax2.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline_HighMatManufEff'].material[MATERIAL].materialdata['mat_MFG_eff'], '.')
ax2.plot(r1.scenario['baseline'].data.year, r1.scenario['baseline_lowMatManufEff'].material[MATERIAL].materialdata['mat_MFG_eff'], '.')
ax1.legend()
""";


# In[ ]:





# In[ ]:





# In[ ]:




