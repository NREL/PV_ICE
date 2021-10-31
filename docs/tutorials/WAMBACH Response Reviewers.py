#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'ElectricFutures')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[2]:


PV_ICE.__version__


# In[3]:


MATERIALS = ['WAMBACH']
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'C:\Users\Silvana\Documents\GitHub\PRIVATE_Wambach_US_INSTALLS_2020.csv'
#MODULEBASELINE = r'\..\..\PRIVATE_Wambach_US_INSTALLS_2020.csv'


# In[4]:


r1 = PV_ICE.Simulation(name='PV_ICE', path=testfolder)
r1.createScenario(name='base', file=MODULEBASELINE)
r1.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r1.scenMod_IRENIFY('base', ELorRL = 'EL' )

r1b = PV_ICE.Simulation(name='PV_ICE', path=testfolder)
r1b.createScenario(name='base', file=MODULEBASELINE)
r1b.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r1b.scenMod_IRENIFY('base', ELorRL = 'EL' )
r1c = PV_ICE.Simulation(name='PV_ICE', path=testfolder)
r1c.createScenario(name='base', file=MODULEBASELINE)
r1c.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r1c.scenMod_IRENIFY('base', ELorRL = 'EL' )


# In[5]:


r1.calculateMassFlow(m1=True)
r1b.calculateMassFlow(m2=True)
r1c.calculateMassFlow(m3=True)


# In[7]:


pvice_Usyearly1, pvice_Uscum1 = r1.aggregateResults()
pvice_Usyearly1b, pvice_Uscum1b = r1b.aggregateResults()
pvice_Usyearly1c, pvice_Uscum1c = r1c.aggregateResults()

pvice_Usyearly1 *= 1000000
pvice_Uscum1 *= 1000000
pvice_Usyearly1b *= 1000000
pvice_Uscum1b *= 1000000
pvice_Usyearly1c *= 1000000
pvice_Uscum1c *= 1000000



# In[8]:


pvice_Usyearly1.keys()


# In[9]:


PV_ICE.main.weibull_pdf_vis(2.4928, 30, xlim=40)


# In[10]:


PV_ICE.main.weibull_cdf_vis(2.4928, 30, xlim=40)


# In[11]:


foo = r1.scenario['base'].data
plt.plot(foo.ix[0,'EOL_on_Year_0':'EOL_on_Year_39'])
#plt.plot(r1.scenario['base'].data['EOL_on_Year_30']


# In[12]:


foo = r1b.scenario['base'].data
plt.plot(foo.ix[0,'EOL_on_Year_0':'EOL_on_Year_39'])
#plt.plot(r1.scenario['base'].data['EOL_on_Year_30']


# In[13]:


foo = r1c.scenario['base'].data
plt.plot(foo.ix[0,'EOL_on_Year_0':'EOL_on_Year_39'])
#plt.plot(r1.scenario['base'].data['EOL_on_Year_30']
max(foo.ix[0,'EOL_on_Year_0':'EOL_on_Year_39'])


# In[14]:


pvice_Uscum1['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'].head()


# In[15]:


pvice_Uscum1c['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'].tail()


# In[16]:


wambachResults = [2019 66,335
2020	92,362
2021	126,148
2022	169,008
2023	224,393
2024	293,597
2025	378,725
2026	481,696
2027	604,955
2028	749,954
2029	919,283
2030	1,116,586


# In[17]:


import matplotlib.pyplot as plt


# # R1: EL
# # R2: RL
# # R3: PV ICE

# In[18]:


r1 = PV_ICE.Simulation(name='PV_ICE', path=testfolder)
r1.createScenario(name='IrenaEL', file=MODULEBASELINE)
r1.createScenario(name='IrenaRL', file=MODULEBASELINE)
r1.createScenario(name='base', file=MODULEBASELINE)
r1.scenario['IrenaEL'].addMaterials(MATERIALS, r'..\..\baselines')
r1.scenMod_IRENIFY('IrenaEL', ELorRL = 'EL' )
r1.scenario['IrenaRL'].addMaterials(MATERIALS, r'..\..\baselines')
r1.scenMod_IRENIFY('IrenaRL', ELorRL = 'RL' )
r1.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')

r1.calculateMassFlow(m3=True)

pvice_Usyearly1, pvice_Uscum1 = r1.aggregateResults()

pvice_Usyearly1 *= 1000000
pvice_Uscum1 *= 1000000

#USCum = pd.concat([pvice_Uscum1, pvice_Uscum2, pvice_Uscum3], axis=1)
#USYearly = pd.concat([pvice_Usyearly1, pvice_Usyearly2, pvice_Usyearly3], axis=1)

pvice_Uscum1.to_csv('pvice_USCum_WAMBACH.csv')
pvice_Usyearly1.to_csv('pvice_USYearly_WAMBACH.csv')


# In[19]:


r1.scenario['IrenaEL'].data['WeibullParams'].tail()


# In[20]:


r1.scenario['IrenaRL'].data['WeibullParams'].tail()


# In[21]:


r1.scenario['base'].data['WeibullParams'].tail()


# In[22]:


'''
r1.createScenario(name='base', file=MODULEBASELINE)
r1.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r1.scenMod_IRENIFY('base', ELorRL = 'EL' )

r2 = PV_ICE.Simulation(name='PV_ICE', path=testfolder)
r2.createScenario(name='base', file=MODULEBASELINE)
r2.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r2.scenMod_IRENIFY('base', ELorRL = 'RL' )

r3 = PV_ICE.Simulation(name='PV_ICE', path=testfolder)
r3.createScenario(name='base', file=MODULEBASELINE)
r3.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')


r1.calculateMassFlow(m3=True)
r2.calculateMassFlow(m3=True)
r3.calculateMassFlow(m3=True)

scenarios = ['base']

pvice_Usyearly1, pvice_Uscum1 = r1.aggregateResults()
pvice_Usyearly2, pvice_Uscum2 = r2.aggregateResults()
pvice_Usyearly3, pvice_Uscum3 = r3.aggregateResults()

pvice_Usyearly1 *= 1000000
pvice_Uscum1 *= 1000000
pvice_Usyearly2 *= 1000000
pvice_Uscum2 *= 1000000
pvice_Usyearly3 *= 1000000
pvice_Uscum3 *= 1000000

USCum = pd.concat([pvice_Uscum1, pvice_Uscum2, pvice_Uscum3], axis=1)
USYearly = pd.concat([pvice_Usyearly1, pvice_Usyearly2, pvice_Usyearly3], axis=1)

USCum.to_csv('pvice_USCum_WAMBACH.csv')
USYearly.to_csv('pvice_USYearly_WAMBACH.csv')


''';


# In[24]:


r1.plotMetricResults()


# In[ ]:





# In[ ]:


plt.plot(pvice_Usyearly1['VirginStock_Module_PV_ICE_base_[Tonnes]'])
plt.plot(pvice_Usyearly2['VirginStock_WAMBACH_PV_ICE_base_[Tonnes]'])
plt.plot(pvice_Usyearly3['VirginStock_WAMBACH_PV_ICE_base_[Tonnes]'])
plt.ylabel('Metric Tonnes')


# In[ ]:


plt.plot(pvice_Usyearly1['WasteMFG_WAMBACH_PV_ICE_base_[Tonnes]'])
plt.plot(pvice_Usyearly2['WasteMFG_WAMBACH_PV_ICE_base_[Tonnes]'])
plt.plot(pvice_Usyearly3['WasteMFG_WAMBACH_PV_ICE_base_[Tonnes]'])
plt.ylabel('Metric Tonnes')


# In[ ]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (12, 5)


# In[ ]:


fig, (a0,a1,a2,a3) = plt.subplots(1,4, figsize=(20, 6), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .2, wspace=.4)

a0.plot(pvice_Usyearly1['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='EL')
a0.plot(pvice_Usyearly2['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='RL')
a0.plot(pvice_Usyearly3['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='PV_ICE')
a0.legend()
#a0.set_yscale('log')
a0.set_title('Yearly')
a0.set_ylabel('EOL Waste [Metric Tonnes]')

a1.plot(pvice_Usyearly1['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='EL')
a1.plot(pvice_Usyearly2['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='RL')
a1.plot(pvice_Usyearly3['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='PV_ICE')
a1.legend()
a1.set_yscale('log')
a1.set_title('Yearly LOG')
a1.set_ylabel('EOL Waste [Metric Tonnes]')


a2.plot(pvice_Uscum1['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='EL')
a2.plot(pvice_Uscum2['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='RL')
a2.plot(pvice_Uscum3['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='PV_ICE')
a2.legend()
a2.set_title('Cumulative')
a2.set_ylabel('EOL Waste [Metric Tonnes]')


a3.plot(pvice_Uscum1['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='EL')
a3.plot(pvice_Uscum2['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='RL')
a3.plot(pvice_Uscum3['WasteAll_WAMBACH_PV_ICE_base_[Tonnes]'], label='PV_ICE')
a3.legend()
a3.set_title('Cumulative LOG')
a3.set_yscale('log')
a3.set_ylabel('EOL Waste [Metric Tonnes]')


# In[ ]:





# In[ ]:





# In[ ]:


foo.ix[0,'EOL_on_Year_0':'EOL_on_Year_30']


# In[ ]:





# In[ ]:


pvice_Usyearly1c['WasteAll_Module_PV_ICE_base_[Tonnes]'].head()


# In[ ]:


fig, ax = 
WasteAll_WAMBACH_PV_ICE_base_


# In[ ]:




