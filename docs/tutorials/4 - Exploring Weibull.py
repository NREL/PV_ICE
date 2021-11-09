#!/usr/bin/env python
# coding: utf-8

# # 4 - Exploring Weibull
# 
# 
# PV ICE handles failures through a probabilistic distribution, so far in specific the Weibull. The Weibull equation is defined by an Alfa and a Beta parameters. These parameters can be found on literature, or they can be calculated if the reliability is known. Altough other values can be set by changing the probabilities, we use by default:
#     - T50: number of years when 50 % of the year will be off and 
#     - T90 are used:
#     
# Below we show a couple ways of passing the parameters, plot a comparison between different literature values, and highlight the significance of T50 and T90.
# 

# In[11]:


import PV_ICE
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os,sys

cwd = os.getcwd() #grabs current working directory
print(cwd)
r1 = PV_ICE.Simulation(name='Simulation1')

baselinefile = cwd+'/../../PV_ICE/baselines/baseline_modules_US.csv'
materialfile = cwd+'/../../PV_ICE/baselines/baseline_material_glass.csv'
r1.createScenario(name='standard', file=baselinefile)
r1.scenario['standard'].addMaterial('glass', file=materialfile)


# ## A. Passing Alpha and Beta values

# In[15]:


weibullInputParams = {'alpha': 3.4,
                      'beta': 4.5}
r1.calculateMassFlow(weibullInputParams=weibullInputParams) 
print(r1.scenario['standard'].data.WeibullParams.head())


# ## B. Internally calculated Weibull with t50 and t90

# In[17]:


r1.calculateMassFlow()  # Note we are not passing weibullInputParams, 
#so it defaults to clculating alpha and beta from the T50 and t90 passed.

print(r1.scenario['standard'].data.WeibullParams)


# This is what T50, T90 look like for this dataset, and the alpha and beta values resulting for each year.

# In[4]:


# Plotting T50 and T90
plt.plot(r1.scenario['standard'].data.mod_reliability_t50)
plt.plot(r1.scenario['standard'].data.mod_reliability_t90)
plt.ylabel('Years')
plt.legend(['T50', 'T90'])

# Making a dataframe of the list of dictionary values for alpha and beta
foo = r1.scenario['standard'].data.WeibullParams
foo = pd.DataFrame.from_records(foo)
foo.set_index(r1.scenario['standard'].data.year, inplace=True)

# Plotting Alpha and Beta
plt.figure()
plt.plot(foo)
plt.ylabel('Value')
plt.legend(['Alpha', 'Beta']);


# # Plotting CDFs with Helper Function
# 
# Using ``PV_ICE.weibull_cdf_vis`` to plot different values of alpha and beta, some calculated from t50 and t90 and some passed from literature values.
# 
# 

# In[5]:


firstgen = r1.scenario['standard'].data.WeibullParams.iloc[0]
ares = PV_ICE.weibull_cdf_vis(firstgen['alpha'],firstgen['beta'])

twentythirtygen = firstgen = r1.scenario['standard'].data.WeibullParams.iloc[35]
bres = PV_ICE.weibull_cdf_vis(twentythirtygen['alpha'],twentythirtygen['beta'])

#userWeibulls = {'alpha': 3.4,
#               'beta': 4.5}
#userres = PV_ICE.weibull_cdf_vis(userWeibulls['alpha'],userWeibulls['beta'])

# Irena 'EL' 2016
alpha = 2.4928
Lifetime = 30
IrenaEarly = PV_ICE.weibull_cdf_vis(alpha, beta=Lifetime)

# Irena 'RL' 2016
alpha = 5.3759
Lifetime = 30
IrenaReg = PV_ICE.weibull_cdf_vis(alpha, beta=Lifetime)

# Upper Shape Factor Kumar 2013
alpha = 14.41
Lifetime = 30
Kumar = PV_ICE.weibull_cdf_vis(alpha, beta=Lifetime)


# In[6]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (10, 8)
    
plt.plot(ares, label=r'$ \alpha $ : '+str(round(firstgen['alpha'],2))+ r' $ \beta $ : '+ str(round(firstgen['beta'],2)) + ' PV ICE, gen 1995')
plt.plot(bres, color='b', label=r'$ \alpha $ : '+str(round(twentythirtygen['alpha'],2))+ r' $ \beta $ : '+ str(round(twentythirtygen['beta'],2)) + ' PV ICE, gen 2030')
plt.plot(IrenaEarly, color='red', linewidth=4.0, label=r'$ \alpha $ : 2.49, Early Loss Baseline Irena 2016')
plt.plot(IrenaReg, color='orange', linewidth=4.0, label=r'$ \alpha $ : 5.3759, Regular Loss Baseline Irena 2016')
plt.plot(Kumar, '-', color='orange', label=r'$ \alpha $ : 14.41, Upper Shape Factor Kumar 2013')
plt.legend()
plt.ylabel('Cumulative Distribution Function (CDF)')
plt.xlabel('Years since install')
plt.xlim([0,50])
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='bottom');


# ## Calculating 'alpha' and 'beta' from t50 and t90 
# 
# Using ``PV_ICe.weibull_params`` to calculate alpha and beta values for t50 and t90. This is done internally usually but this is an example of directly accesing that function

# In[7]:


t50 = 25
t90 = 35

weibullIParams = PV_ICE.weibull_params({t50: 0.50, t90: 0.90})    
print(weibullIParams)


# Here's a plot showing the relationship between the t50 and t90 and how our Weibull looks like.

# In[8]:


calc_cdf = PV_ICE.weibull_cdf_vis(weibullIParams['alpha'], weibullIParams['beta'])
mylabel = r'$ \alpha $: '+str(round(weibullIParams['alpha'],2))+ r'    $ \beta $ : '+ str(round(weibullIParams['beta'],2))
plt.plot(calc_cdf, linewidth=4.0, label=mylabel)
plt.axhline(y=0.9, color='r', linestyle='--')
plt.axhline(y=0.5, color='r', linestyle='--')
plt.axvline(x=25, color='c', linestyle='--')
plt.axvline(x=t90, color='c', linestyle='--')
#plt.axhline(y=0.1, color='r', linestyle='--')
plt.ylabel("CDF")
plt.title('Cumulative Density Function (CDF)\n (a.k.a. Unreliability Function)')

plt.legend();


# # Reliability 101: Relationship between CDF, PDF, Reliability and Failure Rate
# 
# Calculating all of these for a Weibull PDF with Irena Regular Loss Values, of alpha: 5.3759 and beta:30

# In[9]:


weibullIParams = {'alpha': 5.3759,
                      'beta': 30}


# In[10]:


# Changing size for slide presentation of these results
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# ### Calculating CDF with PV ICE 

# In[11]:


calc_cdf = PV_ICE.weibull_cdf_vis(weibullIParams['alpha'], weibullIParams['beta'])


# ### PDF f(t) is the difference between every value of the CDF

# In[12]:


calc_pdf = np.diff(calc_cdf)


# ### Reliability Function R(t) is the "Complement" of the CDF

# In[13]:


reliability_function = [1 - x for x in calc_cdf]


# ### Failure Rate is the ratio of the PDF to the Reliability function (f(t)/R(t))

# In[14]:


failure_rate = calc_pdf / reliability_function[:-1]


# ### Plotting each of the Functions

# In[15]:


mylabel = r'$ \alpha $: '+str(round(weibullIParams['alpha'],2))+ r'    $ \beta $ : '+ str(round(weibullIParams['beta'],2))
plt.plot(calc_cdf, linewidth=4.0, label=mylabel)
plt.axhline(y=0.9, color='r', linestyle='--')
plt.axhline(y=0.5, color='r', linestyle='--')
plt.axvline(x=28, color='c', linestyle='--')
plt.axvline(x=t90, color='c', linestyle='--')
#plt.axhline(y=0.1, color='r', linestyle='--')
plt.ylabel("CDF")
plt.title('Cumulative Density Function (CDF)\n (a.k.a. Unreliability Function)')

plt.legend();


# In[16]:


mylabel = r'$ \alpha $: '+str(round(weibullIParams['alpha'],2))+ r'    $ \beta $ : '+ str(round(weibullIParams['beta'],2))
plt.plot(failure_rate, linewidth=4.0, label=mylabel)

plt.legend();

plt.ylabel("Failure Rate \n(PDF / Reliability)")
plt.title('Failure Rate')

#plt.axhline(y=0.1, color='r', linestyle='--')
#plt.axhline(y=0.5, color='r', linestyle='--')
#plt.axvline(x=28, color='c', linestyle='--')
#plt.axvline(x=t90, color='c', linestyle='--')
#plt.axhline(y=0.1, color='r', linestyle='--')


# In[17]:


mylabel = r'$ \alpha $: '+str(round(weibullIParams['alpha'],2))+ r'    $ \beta $ : '+ str(round(weibullIParams['beta'],2))
plt.plot(reliability_function, linewidth=4.0, label=mylabel)

plt.legend();
plt.axhline(y=0.1, color='r', linestyle='--')
plt.axhline(y=0.5, color='r', linestyle='--')
plt.axvline(x=28, color='c', linestyle='--')
plt.axvline(x=t90, color='c', linestyle='--')
#plt.axhline(y=0.1, color='r', linestyle='--')
plt.ylabel("RELIABILITY")
plt.title('Reliability Function \na.k.a. Survival Plot')


# In[18]:


mylabel = r'$ \alpha $: '+str(round(weibullIParams['alpha'],2))+ r'    $ \beta $ : '+ str(round(weibullIParams['beta'],2))
plt.plot(calc_pdf, linewidth=4.0, label=mylabel)

plt.legend();
#plt.axhline(y=0.9, color='r', linestyle='--')
#plt.axhline(y=0.5, color='r', linestyle='--')
plt.axvline(x=28, color='c', linestyle='--')
plt.axvline(x=t90, color='c', linestyle='--')
#plt.axhline(y=0.1, color='r', linestyle='--')
plt.title('Probability Density Function (PDF) \na.k.a. Density')
plt.ylabel("DENSITY")


# In[ ]:




