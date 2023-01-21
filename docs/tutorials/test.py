#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PV_ICE


# In[2]:


import matplotlib.pyplot as plt
import os,sys
from pathlib import Path


# In[3]:


PV_ICE.__version__


# In[4]:


modulefile_m = r'C:\Users\hmirletz\Documents\GitHub\PV_ICE\tests\baseline_modules_test_3.csv'
materialfile_m = r'C:\Users\hmirletz\Documents\GitHub\PV_ICE\tests\baseline_material_test_3.csv'
testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')


# In[5]:


sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)
sim1.createScenario(name='scen1', massmodulefile=modulefile_m)
sim1.scenario['scen1'].addMaterial('mat1', massmatfile=materialfile_m)


# In[6]:


sim1.calculateMassFlow()


# In[7]:


year, cum = sim1.aggregateResults()


# In[8]:


# TO DO: Add HQ MF OU to aggregateResults 


# In[9]:


sim1.scenario['scen1'].material['mat1'].matdataOut_m.keys()


# In[10]:


plt.plot(sim1.scenario['scen1'].material['mat1'].matdataOut_m['mat_recycled_PG4'])


# In[11]:


plt.plot(sim1.scenario['scen1'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_OU'])


# In[12]:


year.keys()


# In[13]:


plt.plot(year['VirginStock_mat1_sim1_scen1_[Tonnes]'])


# In[14]:


plt.plot(year['ActiveCapacity_sim1_scen1_[MW]'])


# In[15]:


sim1.plotMetricResults()


# In[16]:


sim1.createScenario(name='scen2', massmodulefile=modulefile_m)
sim1.scenario['scen2'].addMaterial('mat1', massmatfile=materialfile_m)


# In[17]:


# sim1.scenario['scen2'].perfectRecycling()
#'mat_EOL_RecycledHQ_Reused4MFG'

sim1.modifyScenario('scen2', 'mod_EOL_pg3_reMFG', 100, start_year=2000) #all modules attempt remfg
sim1.modifyScenario('scen2', 'mod_EOL_sp_reMFG_recycle', 100, start_year=2000) # recycle if can't remfg
sim1.modifyScenario('scen2', 'mod_EOL_pb3_reMFG', 100, start_year=2000) # remfg bad mods too
sim1.modifyScenario('scen2', 'mod_EOL_reMFG_yield', 100, start_year=2000) # REMFG YIELD 98%

#set all other paths to 0
sim1.modifyScenario('scen2', 'mod_EOL_pg0_resell', 0.0, start_year=2000) # 
sim1.modifyScenario('scen2', 'mod_EOL_pg1_landfill', 0.0, start_year=2000) # 
sim1.modifyScenario('scen2', 'mod_EOL_pg2_stored', 0.0, start_year=2000) #
sim1.modifyScenario('scen2', 'mod_EOL_pg4_recycled', 0.0, start_year=2000) # 
sim1.modifyScenario('scen2', 'mod_EOL_pb1_landfill', 0.0, start_year=2000) # 
sim1.modifyScenario('scen2', 'mod_EOL_pb2_stored', 0.0, start_year=2000) # 
sim1.modifyScenario('scen2', 'mod_EOL_pb4_recycled', 0.0, start_year=2000) # 
sim1.modifyScenario('scen2', 'mod_Repair', 0.0, start_year=2000) #
sim1.modifyScenario('scen2', 'mod_MerchantTail', 0.0, start_year=2000) #

sim1.scenario['scen2'].modifyMaterials('mat1', 'mat_PG3_ReMFG_target', 100.0, start_year=2000) #send to recycle
sim1.scenario['scen2'].modifyMaterials('mat1', 'mat_ReMFG_yield', 100.0, start_year=2000) #99% yeild
sim1.scenario['scen2'].modifyMaterials('mat1', 'mat_PG4_Recycling_target', 0.0, start_year=2000) #99% yeild


# In[18]:


sim1.calculateMassFlow()


# In[19]:


year, cum = sim1.aggregateResults()


# In[20]:


# TO DO: Add HQ MF OU to aggregateResults 


# In[21]:


sim1.scenario['scen1'].material['mat1'].matdataOut_m.keys()


# In[22]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_recycled_PG4'])


# In[23]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_OU'])


# In[24]:


year['VirginStock_mat1_sim1_scen1_[Tonnes]'].sum()


# In[25]:


year['VirginStock_mat1_sim1_scen2_[Tonnes]'].sum()


# In[26]:


sim1.scenario['scen1'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_OU'].sum()


# In[27]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG'])


# In[28]:


sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG'].sum()


# In[29]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT'], label='What actually got used in reMFG')
plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG'], label='What got Sent in reMFG')
plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG']
         -
         sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT'], label='What did not got used in reMFG')
plt.legend()

(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG']
         -
         sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT']).sum()


# In[30]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT'])


# In[31]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT'])


# In[32]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG'])


# In[33]:


year.keys()


# In[34]:


plt.plot(year['VirginStock_mat1_sim1_scen1_[Tonnes]'])
plt.plot(year['VirginStock_mat1_sim1_scen2_[Tonnes]'])


# In[35]:


plt.plot(year['ActiveCapacity_sim1_scen2_[MW]'])


# In[36]:


sim1.plotMetricResults()


# In[37]:


#sim1.scenario['scen2'].scenMod_perfectRecycling()

