#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
baselinesfolder =  str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_ICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# This Journal supports the documentation of the baseline input files for the PV_ICE calculator by graphing all baseline inputs of modules and materials for all years. Currently, this includes:
# - USA module installs
# - Global module intalls
# - glass
# - silicon
# - silver (preliminary)

# In[3]:


import PV_ICE


# In[48]:


filelist = sorted(os.listdir(baselinesfolder))
matcher = "modules"
module_baselines = [s for s in filelist if matcher in s]
matcher = "material"
material_baselines = [s for s in filelist if matcher in s]  


# # Plot only 1st module baseline example

# In[49]:


material_baselines[i]


# In[50]:


i=0
r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='standard', file=os.path.join(baselinesfolder, module_baselines[i]))


# In[51]:


r1.scenario['standard'].data.head()


# In[52]:


keys = list(r1.scenario['standard'].metdata[0].keys())
list(keys)


# In[53]:


for k in keys:
    plt.figure()
    plt.plot(r1.scenario['standard'].data.year, r1.scenario['standard'].data[k])
    plt.xlabel('Year')
    plt.ylabel(k+' ['+r1.scenario['standard'].metdata[0][k]+']')


# In[54]:


r1.scenario['standard'].data.year[0]


# In[61]:


r1.calculateMassFlow()


# In[74]:


weibulls = r1.scenario['standard'].data.WeibullParams
weibulls = pd.DataFrame(weibulls.tolist())


# In[ ]:





# In[ ]:





# In[55]:


avgt= (r1.scenario['standard'].data['mod_reliability_t50']+r1.scenario['standard'].data['mod_reliability_t90'])/2.0
avgtmax = r1.scenario['standard'].data['mod_reliability_t90']+5
avgtmin = r1.scenario['standard'].data['mod_reliability_t50']-5


# In[77]:


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


# In[78]:



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

# In[8]:


print(baseline_modules_US)


# In[7]:


plt.plot(baseline_modules_US)

