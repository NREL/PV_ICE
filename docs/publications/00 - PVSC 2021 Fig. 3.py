#!/usr/bin/env python
# coding: utf-8

# # PVSC 2021 Fig. 3

# In[1]:


import PV_ICE
import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[2]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

print ("Your simulation will be stored in %s" % testfolder)


# In[3]:


years = list(range(2009,2051))


# In[ ]:


USyearly = pd.read_csv(os.path.join(testfolder,'PVSC_USYearly_DataforPlot.csv'))


# In[21]:


# USyearly.to_csv('PVSC_USYearly_DataforPlot.csv')



plt.rcParams.update({'font.size': 8})
plt.rcParams['figure.figsize'] = (12, 8)
    
keywords=['VirginStock_', 'Waste_']
SFScenarios = ['Reference.Mod', '95-by-35.Adv', '95-by-35_Elec.Adv_DR']
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminum']

    
fig, axs = plt.subplots(2,1, figsize=(5, 5), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .6, wspace=.001)
fig.subplots_adjust(hspace = .3, wspace=.001)

axs = axs.ravel()
i = 0

### PLOT 1

# Loop over Keywords
ii=0
keyw = keywords[ii]
# Loop over SF Scenarios
kk=0

obj = SFScenarios[kk]
axs[i].yaxis.grid()
axs[i].axvspan(2000, 2018, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
axs[i].plot([],[],color='c', label='glass', linewidth=5)
axs[i].plot([],[],color='k', label='silicon', linewidth=5)
axs[i].plot([],[],color='m', label='silver', linewidth=5)
axs[i].plot([],[],color='r', label='copper', linewidth=5)
axs[i].plot([],[],color='g', label='aluminum', linewidth=5)

axs[i].stackplot(years, USyearly[keyw+materials[0]+'_'+SFScenarios[0]], 
                                                  USyearly[keyw+materials[1]+'_'+SFScenarios[0]], 
                                                  USyearly[keyw+materials[2]+'_'+SFScenarios[0]], 
                                                  USyearly[keyw+materials[3]+'_'+SFScenarios[0]], 
                                                  USyearly[keyw+materials[4]+'_'+SFScenarios[0]], 
                                                  colors=['c','k','m','r', 'g'])
#axs[i].ylabel('Mass [Tons]')
axs[i].set_xlim([2010, 2050])
#axs[i].set_title(keyw+ ' ' + obj.name)
#axs[i].legend(materials)

i += 1 

### PLOT 2

ii=1
keyw = keywords[ii]
# Loop over SF Scenarios
kk=0

obj = SFScenarios[kk]
axs[i].yaxis.grid()
axs[i].axvspan(2000, 2018, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
axs[i].plot([],[],color='c', label='glass', linewidth=5)
axs[i].plot([],[],color='k', label='silicon', linewidth=5)
axs[i].plot([],[],color='m', label='silver', linewidth=5)
axs[i].plot([],[],color='r', label='copper', linewidth=5)
axs[i].plot([],[],color='g', label='aluminum', linewidth=5)

axs[i].stackplot(years, USyearly[keyw+materials[0]+'_'+SFScenarios[0]]*907185, 
                                                  USyearly[keyw+materials[1]+'_'+SFScenarios[0]]*907185, 
                                                  USyearly[keyw+materials[2]+'_'+SFScenarios[0]]*907185, 
                                                  USyearly[keyw+materials[3]+'_'+SFScenarios[0]]*907185, 
                                                  USyearly[keyw+materials[4]+'_'+SFScenarios[0]]*907185, 
                                                  colors=['c','k','m','r', 'g'])
#axs[i].ylabel('Mass [Tons]')
axs[i].set_xlim([2010, 2050])
#axs[i].set_title(keyw+ ' ' + obj.name)
#axs[i].legend(materials)

i += 1 


axs[0].set_ylim([0, 2e7])
axs[1].set_ylim([0, 5e6])
axs[0].set_title("Virgin Stock Needs")
axs[1].set_title("Waste")
        
axs[0].set_ylabel('Mass [Tons]')
axs[1].set_ylabel('Mass [Tons]')
axs[1].legend(materials)

fig.savefig(os.path.join(testfolder,'testplot.png'), dpi=600)

