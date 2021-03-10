#!/usr/bin/env python
# coding: utf-8

# # Baseline Plotting
# 
# This Journal supports the documentation of the baseline input files for the PV_ICE calculator by graphing all baseline inputs of modules and materials for all years. Currently, this includes:
# - USA module installs
# - Global module intalls
# 
# And materials such as:
# - glass
# - silicon
# - silver (preliminary)

# In[12]:


import PV_ICE
import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt


# In[13]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[14]:


testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder =  str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# ## Select Module Baseline and Material baseline to Plot:

# In[18]:


USBaseline = True

if USBaseline:
    MODULEBASELINE=r'..\baselines\baseline_modules_US.csv'
else:
    MODULEBASELINE=r'..\baselines\baseline_modules_WORLD.csv'

MATERIAL = 'glass' # Other options: silicon, silver, aluminum
MATERIALBASELINE=r'..\baselines\baseline_material_'+MATERIAL+'.csv'


# ## Create Simulation

# In[25]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='standard', file=os.path.join(baselinesfolder,  MODULEBASELINE))
r1.scenario['standard'].addMaterial(MATERIAL, file=MATERIALBASELINE)
r1.calculateMassFlow()


# #### Explore loaded Baselines

# In[26]:


r1.scenario['standard'].data.head()


# In[27]:


r1.scenario['standard'].material[MATERIAL].materialdata.head()


# #### Generate variable list of data and material data. 
# 
# This journal plots only baselines, not generated results so it's not all columns after running the mass flow

# In[89]:


keys = list(r1.scenario['standard'].metdata[0])
keys = keys[1::]
keys


# In[76]:


matkeys = list(r1.scenario['standard'].material[MATERIAL].materialmetdata)
matkeys = matkeys[1::]
matkeys


# ### Plot all keys

# In[82]:


prows=int(np.ceil((len(keys)+1)/3))

plt.rcParams.update({'font.size': 12})

fig, axs = plt.subplots(prows,3, figsize=(15, prows*5), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = 0.5, wspace=.4)
axs = axs.ravel()

for i in range(0, len(keys)):
    k = keys[i]
    axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data[k])
    axs[i].set_ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')   
    axs[i].axvspan(1995, 2018, facecolor='0.9', alpha=0.5)
    axs[i].axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
    axs[i].set_xlim(1995, 2050)

    
i +=1
axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_reliability_t50'])
axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_reliability_t90'])
axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_lifetime'])
axs[i].set_ylabel(k+' ['+r1.scenario['standard'].metdata[0]['mod_reliability_t50']+']')   
axs[i].axvspan(1995, 2018, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
axs[i].set_xlim(1995, 2050)

axs[i].set_xlim(1995, 2050)


# In[97]:


prows=int(np.ceil((len(matkeys)+1)/3))

plt.rcParams.update({'font.size': 12})

fig, axs = plt.subplots(prows,3, figsize=(15, prows*5), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = 0.5, wspace=.4)
axs = axs.ravel()

for i in range(0, len(matkeys)):
    k = matkeys[i]
    axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].material[MATERIAL].materialdata[k])
    axs[i].set_ylabel(k+' ['+r1.scenario['standard'].material[MATERIAL].materialmetdata[k]+']')   
    axs[i].axvspan(1995, 2018, facecolor='0.9', alpha=0.5)
    axs[i].axvspan(2018, 2050.5, facecolor='orange', alpha=0.1)
    axs[i].set_xlim(1995, 2050)


# ## Plot with Limits

# In[103]:


# absolutes
upperlimit = {'new_Installed_Capacity_[MW]': 5,    # relative
 'mod_eff': 3,                                     # absolute
 'mod_reliability_t50': 5,                         # absolute
 'mod_reliability_t90': 5,                         # absolute
 'mod_degradation': 2,                             # absolute
 'mod_lifetime': 5,                                # absolute
 'mod_MFG_eff': 5,                                 # absolute
 'mod_EOL_collection_eff': 10,                     # absolute
 'mod_EOL_collected_recycled': 10,                 # absolute
 'mod_Repowering': 10,                             #absolute
 'mod_Repairing':10}

# absolutes
lowerlimit = {'new_Installed_Capacity_[MW]': 5,        # relative
 'mod_eff': 3,                                     # absolute
 'mod_reliability_t50': 5,                         # absolute
 'mod_reliability_t90': 5,                         # absolute
 'mod_degradation': 2,                             # absolute
 'mod_lifetime': 5,                                # absolute
 'mod_MFG_eff': 5,                                 # absolute
 'mod_EOL_collection_eff': 10,                     # absolute
 'mod_EOL_collected_recycled': 10,                 # absolute
 'mod_Repowering': 10,                             #absolute
 'mod_Repairing':10}


# In[ ]:





# #### Reducing keys so that lifetime-related ones are plotted together

# In[117]:


keys = ['new_Installed_Capacity_[MW]',
 'mod_eff',
 'mod_degradation',
 'mod_MFG_eff',
 'mod_EOL_collection_eff',
 'mod_EOL_collected_recycled',
 'mod_Repowering',
 'mod_Repairing']


# In[118]:


(r1.scenario['standard'].data[k]+upperlimit[k]).clip(lower=0.0, upper=100.0)


# In[134]:


prows=int(np.ceil((len(keys)+1)/3))

plt.rcParams.update({'font.size': 12})

fig, axs = plt.subplots(prows,3, figsize=(15, prows*5), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = 0.5, wspace=.4)
axs = axs.ravel()

x = r1.scenario['standard'].data.year

# Installations
i = 0
k = keys[i]
base =  r1.scenario['standard'].data[k]
upperlim = base*(1+(upperlimit[k])/100)
lowerlim = base*(1-(lowerlimit[k])/100)
axs[i].axvspan(1995, 2020, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2020, 2050.5, facecolor='yellow', alpha=0.1)
axs[i].set_xlim(1995, 2050)
axs[i].plot(r1.scenario['standard'].data.year, base)
axs[i].fill_between(x, lowerlim, upperlim, color='g', lw=3, alpha=.3)
axs[i].set_yscale('log')
axs[i].set_ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')   


# Efficiency
i = 1
k = keys[i]
base =  r1.scenario['standard'].data[k]
upperlim = (base+upperlimit[k]).clip(lower=0.0, upper=100.0)
lowerlim = (base-lowerlimit[k]).clip(lower=0.0, upper=100.0)
axs[i].axvspan(1995, 2020, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2020, 2050.5, facecolor='yellow', alpha=0.1)
axs[i].plot(x, upperlim, label='upper')
axs[i].plot(x, base, label='base')
axs[i].plot(x, lowerlim, label='lower')
axs[i].fill_between(x, lowerlim, upperlim, color='g', lw=3, alpha=.3)
axs[i].set_ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')   
axs[i].set_xlim(1995, 2050)
axs[i].set_ylim(0.0, 40.0)
axs[i].legend()

# Degradation
i = 2
k = keys[i]
base =  r1.scenario['standard'].data[k]
upperlim = (base+upperlimit[k]).clip(lower=0.0, upper=100.0)
lowerlim = (base-lowerlimit[k]).clip(lower=0.0, upper=100.0)
axs[i].axvspan(1995, 2020, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2020, 2050.5, facecolor='yellow', alpha=0.1)
axs[i].plot(x, upperlim, label='upper')
axs[i].plot(x, base, label='base')
axs[i].plot(x, lowerlim, label='lower')
axs[i].fill_between(x, lowerlim, upperlim, color='g', lw=3, alpha=.3)
axs[i].set_ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')   
axs[i].set_xlim(1995, 2050)
axs[i].set_ylim(0.0, 5.0)
axs[i].legend()

    
for i in range(3, len(keys)):
    k = keys[i]
    base =  r1.scenario['standard'].data[k]
    upperlim = (base+upperlimit[k]).clip(lower=0.0, upper=100.0)
    lowerlim = (base-lowerlimit[k]).clip(lower=0.0, upper=100.0)
    axs[i].axvspan(1995, 2020, facecolor='0.9', alpha=0.5)
    axs[i].axvspan(2020, 2050.5, facecolor='yellow', alpha=0.1)
    axs[i].plot(x, upperlim, label='upper')
    axs[i].plot(x, base, label='base')
    axs[i].plot(x, lowerlim, label='lower')
    axs[i].fill_between(x, lowerlim, upperlim, color='g', lw=3, alpha=.3)
    axs[i].set_ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')   
    axs[i].set_xlim(1995, 2050)
    axs[i].set_ylim(0.0, 100.0)
    axs[i].legend()



    
i +=1
base =  r1.scenario['standard'].data[k]
upperlim = r1.scenario['standard'].data['mod_reliability_t90']+5
lowerlim = r1.scenario['standard'].data['mod_lifetime']-5
axs[i].fill_between(x, lowerlim, upperlim, color='g', lw=3, alpha=.3)
axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_reliability_t50'], label='t50')
axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_reliability_t90'], label='t90')
axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_lifetime'], label='project lifetime')
axs[i].set_ylabel(k+' ['+r1.scenario['standard'].metdata[0]['mod_reliability_t50']+']')   
axs[i].axvspan(1995, 2020, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2020, 2050.5, facecolor='yellow', alpha=0.1)
axs[i].set_xlim(1995, 2050)
axs[i].legend()
axs[i].set_xlim(1995, 2050)


# In[135]:


matkeys


# In[139]:


# absolutes
matupperlimit = {'mat_virgin_eff': 10,               # absolute
 'mat_massperm2': 10,                                # relative
 'mat_MFG_eff': 10,                                  # absolute
 'mat_MFG_scrap_Recycled': 10,                       # absolute
 'mat_MFG_scrap_Recycling_eff': 10,                  # absolute
 'mat_MFG_scrap_Recycled_into_HQ': 10,               # absolute
 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG': 10,    # absolute
 'mat_EOL_collected_Recycled': 10,                   # absolute
 'mat_EOL_Recycling_eff': 10,                        # absolute
 'mat_EOL_Recycled_into_HQ': 10,                     #absolute
 'mat_EOL_RecycledHQ_Reused4MFG':10}

# absolutes
matlowerlimit = {'mat_virgin_eff': 10,                  # absolute
 'mat_massperm2': 10,                                # relative
 'mat_MFG_eff': 10,                                  # absolute
 'mat_MFG_scrap_Recycled': 10,                       # absolute
 'mat_MFG_scrap_Recycling_eff': 10,                  # absolute
 'mat_MFG_scrap_Recycled_into_HQ': 10,               # absolute
 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG': 10,    # absolute
 'mat_EOL_collected_Recycled': 10,                   # absolute
 'mat_EOL_Recycling_eff': 10,                        # absolute
 'mat_EOL_Recycled_into_HQ': 10,                     #absolute
 'mat_EOL_RecycledHQ_Reused4MFG':10}


# In[143]:


base


# In[149]:


prows=int(np.ceil((len(matkeys)+1)/3))

plt.rcParams.update({'font.size': 12})

fig, axs = plt.subplots(prows,3, figsize=(15, prows*5), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = 0.5, wspace=.4)
axs = axs.ravel()

x = r1.scenario['standard'].data.year

# mat_virgin_eff
i = 0
k = matkeys[i]
base = r1.scenario['standard'].material[MATERIAL].materialdata[k]
upperlim = (base+matupperlimit[k]).clip(lower=0.0, upper=100.0)
lowerlim = (base-matlowerlimit[k]).clip(lower=0.0, upper=100.0)
axs[i].axvspan(1995, 2020, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2020, 2050.5, facecolor='orange', alpha=0.1)
axs[i].set_xlim(1995, 2050)
axs[i].fill_between(x, lowerlim, upperlim, color='g', lw=3, alpha=.3)
axs[i].plot(x, upperlim, label='upper')
axs[i].plot(x, base, label='base')
axs[i].plot(x, lowerlim, label='lower')
axs[i].set_ylabel(k+' ['+r1.scenario['standard'].material[MATERIAL].materialmetdata[k]+']')   
axs[i].set_ylim(0.0, 100.0)
axs[i].legend()


# mat_massperm2
i = 1
k = matkeys[i]
base = r1.scenario['standard'].material[MATERIAL].materialdata[k]
upperlim = base*(1+(matupperlimit[k])/100)
lowerlim = base*(1-(matlowerlimit[k])/100)
axs[i].axvspan(1995, 2020, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2020, 2050.5, facecolor='orange', alpha=0.1)
axs[i].fill_between(x, lowerlim, upperlim, color='g', lw=3, alpha=.3)
axs[i].plot(x, upperlim, label='upper')
axs[i].plot(x, base, label='base')
axs[i].plot(x, lowerlim, label='lower')
axs[i].set_ylabel(k+' ['+r1.scenario['standard'].material[MATERIAL].materialmetdata[k]+']')   
axs[i].set_xlim(1995, 2050)
#axs[i].set_ylim(0.0, 40.0)
axs[i].legend()

# mat_MFG_eff
i = 2
k = matkeys[i]
base = r1.scenario['standard'].material[MATERIAL].materialdata[k]
upperlim = (base+matupperlimit[k]).clip(lower=0.0, upper=100.0)
lowerlim = (base-matlowerlimit[k]).clip(lower=0.0, upper=100.0)
axs[i].axvspan(1995, 2020, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2020, 2050.5, facecolor='orange', alpha=0.1)
axs[i].fill_between(x, lowerlim, upperlim, color='g', lw=3, alpha=.3)
axs[i].plot(x, upperlim, label='upper')
axs[i].plot(x, base, label='base')
axs[i].plot(x, lowerlim, label='lower')
axs[i].set_ylabel(k+' ['+r1.scenario['standard'].material[MATERIAL].materialmetdata[k]+']')   
axs[i].set_xlim(1995, 2050)
axs[i].set_ylim(50.0, 100.0)
axs[i].legend()

    
for i in range(3, len(matkeys)):
    k = matkeys[i]
    base = r1.scenario['standard'].material[MATERIAL].materialdata[k]
    upperlim = (base+matupperlimit[k]).clip(lower=0.0, upper=100.0)
    lowerlim = (base-matlowerlimit[k]).clip(lower=0.0, upper=100.0)
    axs[i].axvspan(1995, 2020, facecolor='0.9', alpha=0.5)
    axs[i].axvspan(2020, 2050.5, facecolor='orange', alpha=0.1)
    axs[i].fill_between(x, lowerlim, upperlim, color='g', lw=3, alpha=.3)
    axs[i].plot(x, upperlim, label='upper')
    axs[i].plot(x, base, label='base')
    axs[i].plot(x, lowerlim, label='lower')
    axs[i].set_ylabel(k+' ['+r1.scenario['standard'].material[MATERIAL].materialmetdata[k]+']')   
    axs[i].set_xlim(1995, 2050)
    axs[i].set_ylim(0.0, 100.0)
    axs[i].legend()


# In[ ]:


plt.rcParams.update({'font.size': 10})
plt.rcParams['figure.figsize'] = (12, 8)
    
keywords=['VirginStock_']
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminum']

fig, axs = plt.subplots(1,1, figsize=(4, 6), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.2)
i = 0

obj = SFScenarios[2].name
# Loop over Keywords
ii = 0 
keyw = keywords[ii]
# Loop over SF Scenarios

# ROW 2, Aluminum and Silicon:        g-  4 aluminum k - 1 silicon   orange - 3 copper  gray - 2 silver
axs.plot(USyearly[keyw+materials[2]+'_'+SFScenarios[2].name]*100/mining2020_silver, 
         color = 'gray', linewidth=2.0, label='Silver')
axs.fill_between(USyearly.index, USyearly[keyw+materials[2]+'_'+SFScenarios[0].name]*100/mining2020_silver, USyearly[keyw+materials[2]+'_'+SFScenarios[2].name]*100/mining2020_silver,
                   color='gray', lw=3, alpha=.3)
    
axs.plot(USyearly[keyw+materials[1]+'_'+SFScenarios[2].name]*100/mining2020_silicon, 
         color = 'k', linewidth=2.0, label='Silicon')
axs.fill_between(USyearly.index, USyearly[keyw+materials[1]+'_'+SFScenarios[0].name]*100/mining2020_silicon, 
                                USyearly[keyw+materials[1]+'_'+SFScenarios[2].name]*100/mining2020_silicon,
                   color='k', lw=3, alpha=.5)

axs.plot(USyearly[keyw+materials[4]+'_'+SFScenarios[2].name]*100/mining2020_aluminum, 
         color = 'g', linewi


for i in range(1, len(keys)):
    k = keys[i]
    upperlim = r1.scenario['standard'].data[k]+upperlimit[k].clip(100)
    lowerlim = r1.scenario['standard'].data[k]-lowerlimit[k].clip(0)
    axs[i].plot(r1.scenario['standard'].data.year, upperlim)
    axs[i].plot(r1.scenario['standard'].data.year, lowerlim)
    axs[i].set_ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')   
    axs[i].axvspan(1995, 2018, facecolor='0.9', alpha=0.5)
    axs[i].axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
    axs[i].set_xlim(1995, 2050)


    
i +=1
axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_reliability_t50'])
axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_reliability_t90'])
axs[i].plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_lifetime'])
axs[i].set_ylabel(k+' ['+r1.scenario['standard'].metdata[0]['mod_reliability_t50']+']')   
axs[i].axvspan(1995, 2018, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
axs[i].set_xlim(1995, 2050)

axs[i].set_xlim(1995, 2050)dth=2.0, label='Aluminum')


axs.plot(USyearly[keyw+materials[3]+'_'+SFScenarios[2].name]*100/mining2020_copper, 
         color = 'orange', linewidth=2.0, label='Copper')

axs.fill_between(USyearly.index, USyearly[keyw+materials[3]+'_'+SFScenarios[0].name]*100/mining2020_copper, 
                                USyearly[keyw+materials[3]+'_'+SFScenarios[2].name]*100/mining2020_copper,
                   color='orange', lw=3, alpha=.3)

axs.set_xlim([2020,2050])
axs.legend()
#axs.set_yscale('log')

axs.set_ylabel('Virgin material needs as a percentage of 2020 global mining production capacity [%]')

fig.savefig(title_Method+' Fig_1x1_MaterialNeeds Ratio to Production.png', dpi=600)


# In[ ]:



for k in keys:
    plt.figure()
    plt.plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data[k])
    plt.xlabel('Year')
    plt.ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')


# In[45]:


for k in keys:
    plt.figure()
    plt.plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data[k])
    plt.xlabel('Year')
    plt.ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')


# In[46]:


r1.scenario['standard'].data.year[0]


# In[ ]:





# In[47]:


weibulls = r1.scenario['standard'].data.WeibullParams
weibulls = pd.DataFrame(weibulls.tolist())


# In[ ]:





# In[ ]:





# In[48]:


avgt= (r1.scenario['standard'].data['mod_reliability_t50']+r1.scenario['standard'].data['mod_reliability_t90'])/2.0
avgtmax = r1.scenario['standard'].data['mod_reliability_t90']+5
avgtmin = r1.scenario['standard'].data['mod_reliability_t50']-5


# In[49]:


df = r1.scenario['standard'].data

#for generation, row in df.iterrows(): 
    #generation is an int 0,1,2,.... etc.
generation=0
row=df.iloc[generation]

t50, t90 = row['t50'], row['t90']   #  t50 = 17.0; t90 = 22.0
weibullInputParams = weibull_params({t50: 0.50, t90: 0.90})      #  alpha = 4.65, beta = 18.39
f = weibull_cdf(**weibull_params({t50: 0.50, t90: 0.90}))
x = np.clip(df.index - generation, 0, np.inf)
cdf = list(map(f, x))


generation=40
row=df.iloc[generation]
t50, t90 = row['t50'], row['t90']   #  t50 = 17.0; t90 = 22.0
weibullInputParams2 = weibull_params({t50: 0.50, t90: 0.90})      #  alpha = 4.65, beta = 18.39
g = weibull_cdf(**weibull_params({t50: 0.50, t90: 0.90}))
generation = 0
x = np.clip(df.index - generation, 0, np.inf)
gdf = list(map(g, x))


#weibullInputParams = {'alpha': 3.4,
#                      'beta': 4.5}

#g = weibull_cdf(weibullInputParams['alpha'], weibullInputParams['beta'])
#x = np.clip(df.index - generation, 0, np.inf)
#gdf = list(map(g, x))

h = weibull_cdf_alphaonly(2.4928, 30)
x = np.clip(df.index - generation, 0, np.inf)
hdf = list(map(h, x))

j = weibull_cdf_alphaonly(5.3759, 30)
x = np.clip(df.index - generation, 0, np.inf)
jdf = list(map(j, x))

i = weibull_cdf_alphaonly(14.41, 30)
x = np.clip(df.index - generation, 0, np.inf)
idf = list(map(i, x))



plt.plot(cdf, label=r'$ \alpha $ : '+str(round(weibullInputParams['alpha'],2))+ r' $ \beta $ : '+ str(round(weibullInputParams['beta'],2)) + ' PV ICE, gen 1995')
plt.plot(gdf, label=r'$ \alpha $ : '+str(round(weibullInputParams2['alpha'],2))+ r' $ \beta $ : '+ str(round(weibullInputParams2['beta'],2)) + ' PV ICE, gen 2030')
plt.plot(hdf, label=r'$ \alpha $ : 2.49, Early Loss Baseline Irena 2016')
plt.plot(jdf, label=r'$ \alpha $ : 5.3759, Regular Loss Baseline Irena 2016')
plt.plot(idf, label=r'$ \alpha $ : 14.41, Upper Shape Factor Kumar 2013')
plt.legend()
plt.ylabel('Cumulative Distribution Function (CDF)')
plt.xlabel('Years since install')
plt.xlim([0,50])
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

#   pdf = [0] + [j - i for i, j in zip(cdf[: -1], cdf[1 :])]

# In[3]:


# In[50]:



fig, axs = plt.subplots(2,3, figsize=(15, 6), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=.2)
axs = axs.ravel()
i = 0

axs[i].axvspan(1995, 2018, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
#axs[i].plot([],[],color='g', label='aluminum', linewidth=5)
axs[i].plot(r1.scenario['standard'].data.year,r1.scenario['standard'].data['mod_reliability_t50'],color='g', label='t50', linewidth=5)
axs[i].plot(r1.scenario['standard'].data.year,r1.scenario['standard'].data['mod_reliability_t90'],color='b', label='t90', linewidth=5)
axs[i].set_xlim([1995, 2050])
axs[i].plot(r1.scenario['standard'].data.year,r1.scenario['standard'].data['mod_lifetime'],color='k', label='Project Lifetime', linewidth=5)


#axs[i].fill_between(r1.scenario['standard'].data.year, r1.scenario['standard'].data['mod_reliability_t50'], r1.scenario['standard'].data['mod_reliability_t90'], 
#                   alpha= 0.3, color='cyan', lw=3)# , alpha=.6)

axs[i].fill_between(r1.scenario['standard'].data.year, avgtmin, avgtmax, 
                   alpha= 0.3, color='cyan', lw=3, label='Confidence interval')# , alpha=.6)
axs[i].set_ylabel('Years')
axs[i].set_title('Module Reliability points t50 and t90')
axs[i].legend()

# ALPHA AND BETA
i = 1
axs[i].plot(weibulls['alpha'])
axs[i].plot(weibulls['beta'])


# EFFICIENCY
i=3
axs[i].axvspan(1995, 2018, facecolor='0.9', alpha=0.5)
axs[i].axvspan(2018, 2050.5, facecolor='yellow', alpha=0.1)
#axs[i].plot([],[],color='g', label='aluminum', linewidth=5)
axs[i].plot(r1.scenario['standard'].data.year,r1.scenario['standard'].data['mod_eff'],color='g', label='t50', linewidth=5)
axs[i].set_xlim([1995, 2050])


# # Module Files 

# ## USA

# In[ ]:


print(baseline_modules_US)


# In[ ]:


plt.plot(baseline_modules_US)


# In[ ]:




