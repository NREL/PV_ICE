#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PV_ICE


# In[2]:


import matplotlib.pyplot as plt


# In[3]:


PV_ICE.__version__


# In[4]:


modulefile_m = r'C:\Users\sayala\Documents\GitHub\PV_ICE\tests\baseline_modules_test_3.csv'
materialfile_m = r'C:\Users\sayala\Documents\GitHub\PV_ICE\tests\baseline_material_test_3.csv'
testfolder = 'TEMP'


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

sim1.scenMod_perfectRecycling(scenarios='scen2')


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


# In[37]:


year['VirginStock_mat1_sim1_scen1_[Tonnes]'].sum()


# In[38]:


year['VirginStock_mat1_sim1_scen2_[Tonnes]'].sum()


# In[34]:


sim1.scenario['scen1'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_OU'].sum()


# In[40]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG'])


# In[41]:


sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG'].sum()


# In[51]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT'], label='What actually got used in reMFG')
plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG'], label='What got Sent in reMFG')
plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG']
         -
         sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT'], label='What did not got used in reMFG')
plt.legend()

(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG']
         -
         sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT']).sum()


# In[43]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT'])


# In[ ]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_VAT'])


# In[24]:


plt.plot(sim1.scenario['scen2'].material['mat1'].matdataOut_m['mat_EOL_Recycled_HQ_into_MFG'])


# In[25]:


year.keys()


# In[28]:


plt.plot(year['VirginStock_mat1_sim1_scen1_[Tonnes]'])
plt.plot(year['VirginStock_mat1_sim1_scen2_[Tonnes]'])


# In[30]:


plt.plot(year['ActiveCapacity_sim1_scen2_[MW]'])


# In[31]:


sim1.plotMetricResults()


# In[ ]:


#sim1.scenario['scen2'].scenMod_perfectRecycling()

