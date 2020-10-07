# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:43:40 2020

@author: Silvana
"""


file = r'C:\Users\Silvana\Documents\GitHub\CircularEconomy-MassFlowCalculator\PV_DEMICE\baselines\baseline_modules_US.csv'
fileglass = r'C:\Users\Silvana\Documents\GitHub\CircularEconomy-MassFlowCalculator\PV_DEMICE\baselines\baseline_material_glass.csv'
r1 = Simulation()
r1.createScenario('standard', file=file)
r1.scenario['standard'].addMaterial('glass', fileglass )

r1.scenario['standard'].addMaterial('limestone', fileglass )
r1.scenario['standard'].material['limestone'].materialdata['mat_virgin_eff'] = 30.0
r1.scenario['standard'].material['limestone'].materialdata['mat_EOL_collected_Recycled'] = 40.0
r1.scenario['standard'].material['limestone'].materialdata['mat_massperm2'] = 4


r1.createScenario('decadence', file=file)

r1.scenario['decadence'].addMaterial('glass', fileglass )
r1.scenario['decadence'].data['mod_lifetime'] = 35
r1.scenario['decadence'].material['glass'].materialdata['mat_virgin_eff'] = 70.0

r1.scenario['decadence'].addMaterial('limestone', fileglass )
r1.scenario['decadence'].material['limestone'].materialdata['mat_virgin_eff'] = 80.0
r1.scenario['decadence'].material['limestone'].materialdata['mat_EOL_collected_Recycled'] = 100.0
r1.scenario['decadence'].material['limestone'].materialdata['mat_massperm2'] = 22

# In[2]:

r1.calculateMassFlow()

# In[3]:
r1.plotScenariosComparison(keyword='Cumulative_Area_disposedby_Failure')
r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_EoL_Recycled_into_HQ')


# In[3]:
Index(['', ' '', '',
       '', 'mod_degradation', '', '',
       '', 'mod_EOL_collected_recycled',
       'mod_Repowering', 'mod_Repairing', 

      
      
  Index(['year', 'mat_virgin_eff', 'mat_massperm2', 'material_MFG_eff',
       'mat_MFG_scrap_recycled', 'mat_MFG_scrap_recycling_eff',
       'mat_MFG_scrap_Recycled_into_HQ',
       'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG',
       'mat_EOL_collected_Recycled', 'mat_EOL_Recycling_eff',
       'mat_EOL_Recycled_into_HQ', 'mat_EOL_RecycledHQ_Reused4MFG',
       'mat_modules_NotRecycled', 'mat_modules_NotCollected',
       'mat_EOL_sento_Recycling', 'mat_EOL_NotRecycled_Landfilled',
       'mat_EOL_Recycled', 'mat_EOL_Recycled_Losses_Landfilled',
       'mat_EoL_Recycled_into_HQ', 'mat_EoL_Recycled_into_OQ',
       'mat_EoL_Recycled_HQ_into_MFG', 'mat_EOL_Recycled_HQ_into_OU',
       'mat_Manufactured', 'mat_Manufacturing_Input', 'mat_MFG_Scrap',
       'mat_MFG_Scrap_Sentto_Recycling', 'mat_MFG_Scrap_Landfilled',
       'mat_MFG_Scrap_Recycled', 'mat_MFG_Scrap_Recycled_Losses_Landfilled',
       'mat_MFG_Recycled_into_HQ', 'mat_MFG_Recycled_into_OQ',
       'mat_MFG_Recycled_HQ_into_MFG', 'mat_MFG_Recycled_HQ_into_OU',
       'mat_Virgin_Stock', 'mat_Total_EoL_Landfilled',
       'mat_Total_MFG_Landfilled', 'mat_Total_Landfilled',
       'mat_Total_Recycled_OU'],
        
# In[4]:
    
    
keyword = 'Cumulative_Active_Area'
plt.figure()
scen=['standard','decadence']
i=0
for i in range 
plt.plot(r1.scenario[scen[i]].data['year'],r1.scenario[scen[i]].data[keyword], label=scen[i])
plt.legend()
plt.xlabel('Year')
plt.title(keyword.replace('_', " "))
pltylabel('')