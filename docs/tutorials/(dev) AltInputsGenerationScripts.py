#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

cwd = os.getcwd() #grabs current working directory


# In[ ]:


#Lifetime and Degradation
#median annual power degradation Jordan et al 2022, Table 6
idx_temp = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index

df_shj_eff = pd.DataFrame(index=idx_temp, columns=['mod_eff'], dtype=float)
df_shj_eff.loc[2022] = 19.0
df_shj_eff.loc[2030] = 20.5
df_shj_eff.loc[2050] = 22
df_shj_eff.interpolate(inplace=True)

df_shj_deg = pd.DataFrame(index=idx_temp, columns=['mod_deg'], dtype=float)
df_shj_deg.loc[2022] = 1.6
df_shj_deg.loc[2030] = 1.4
df_shj_deg.loc[2050] = 1.2
df_shj_deg.interpolate(inplace=True)

#degradation rate:
#sim1.modifyScenario('SHJ', 'mod_degradation', df_shj_deg.loc[2022:,'mod_deg'], start_year=2022) 

#Mod Project Lifetime
df_shj_life = pd.DataFrame(index=idx_temp, columns=['mod_lifetime'], dtype=float)
df_shj_life.loc[2022] = 25
df_shj_life.loc[2030] = 25
df_shj_life.loc[2050] = 25
df_shj_life.interpolate(inplace=True)
#sim1.modifyScenario('SHJ', 'mod_lifetime', df_shj_life.loc[2022:,'mod_lifetime'], start_year=2022) #

#T50
df_shj_t50 = pd.DataFrame(index=idx_temp, columns=['mod_t50'], dtype=float)
df_shj_t50.loc[2022] = 25
df_shj_t50.loc[2030] = 28
df_shj_t50.loc[2050] = 40
df_shj_t50.interpolate(inplace=True)
#sim1.modifyScenario('SHJ', 'mod_reliability_t50', df_shj_t50.loc[2022:,'mod_t50'], start_year=2022)
#t90
df_shj_t90 = pd.DataFrame(index=idx_temp, columns=['mod_t90'], dtype=float)
df_shj_t90.loc[2022] = 30
df_shj_t90.loc[2030] = 33
df_shj_t90.loc[2050] = 44
df_shj_t90.interpolate(inplace=True)
#sim1.modifyScenario('SHJ', 'mod_reliability_t90', df_shj_t90.loc[2022:,'mod_t90'], start_year=2022) 

pd.concat([df_shj_eff,df_shj_t50,df_shj_t90,df_shj_deg,df_shj_life], axis=1)


# In[ ]:


idx_temp = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
df_shj_merchanttail = pd.DataFrame(index=idx_temp, columns=['mod_merchanttail'], dtype=float)
df_shj_merchanttail.loc[2022] = 0
df_shj_merchanttail.loc[2030] = 0
df_shj_merchanttail.loc[2050] = 0
df_shj_merchanttail.interpolate(inplace=True)
#module collection
df_shj_modcollect = pd.DataFrame(index=idx_temp, columns=['mod_collect'], dtype=float)
df_shj_modcollect.loc[2022] = 15
df_shj_modcollect.loc[2030] = 30
df_shj_modcollect.loc[2050] = 75
df_shj_modcollect.interpolate(inplace=True)
#collection
#sim1.modifyScenario('SHJ', 'mod_EOL_collection_eff', df_shj_modcollect.loc[2022:,'mod_collect'], start_year=2022) #
df_shj_modremfg = pd.DataFrame(index=idx_temp, columns=['mod_remfg'], dtype=float)
df_shj_modremfg.loc[2022] = 0
df_shj_modremfg.loc[2030] = 0
df_shj_modremfg.loc[2050] = 0
df_shj_modremfg.interpolate(inplace=True)

#module recycling target
df_shj_modrecycle = pd.DataFrame(index=idx_temp, columns=['mod_recycle'], dtype=float)
df_shj_modrecycle.loc[2022] = 75
df_shj_modrecycle.loc[2030] = 80
df_shj_modrecycle.loc[2050] = 95
df_shj_modrecycle.interpolate(inplace=True)

df_modrecycle_alt = 100-df_shj_modremfg

pd.concat([df_shj_merchanttail,df_shj_modcollect,df_shj_modremfg,df_shj_modrecycle, df_modrecycle_alt], axis=1)


# In[ ]:





# In[ ]:


idx_temp = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
columns = ['mat_MFG_scrap_Recycled','mat_MFG_scrap_Recycling_eff','mat_MFG_scrap_Recycled_into_HQ',
           'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG','mat_PG3_ReMFG_target','mat_ReMFG_yield',
           'mat_PG4_Recycling_target','mat_Recycling_yield','mat_EOL_Recycled_into_HQ','mat_EOL_RecycledHQ_Reused4MFG']
glassimprovedrecycle = pd.DataFrame(index=idx_temp, columns=columns, dtype=float)

#MFGing Scrap
glassimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2022] = 80
glassimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2030] = 100
glassimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2050] = 100

glassimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2022] = 50
glassimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2030] = 80
glassimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2050] = 90

glassimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2022] = 0
glassimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2030] = 30
glassimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2050] = 75

glassimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2022] = 0
glassimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2030] = 100
glassimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2050] = 100

#REMFG

glassimprovedrecycle['mat_PG3_ReMFG_target'].loc[2022] = 0
glassimprovedrecycle['mat_PG3_ReMFG_target'].loc[2030] = 50
glassimprovedrecycle['mat_PG3_ReMFG_target'].loc[2050] = 100


glassimprovedrecycle['mat_ReMFG_yield'].loc[2022] = 60
glassimprovedrecycle['mat_ReMFG_yield'].loc[2030] = 80
glassimprovedrecycle['mat_ReMFG_yield'].loc[2050] = 98

#EoL Recycling
#glassimprovedrecycle['mat_PG4_Recycling_target'].loc[2022] = 90
#glassimprovedrecycle['mat_PG4_Recycling_target'].loc[2030] = 100
#glassimprovedrecycle['mat_PG4_Recycling_target'].loc[2050] = 100
glassimprovedrecycle['mat_PG4_Recycling_target'] = 100-glassimprovedrecycle['mat_PG3_ReMFG_target']

glassimprovedrecycle['mat_Recycling_yield'].loc[2022] = 40
glassimprovedrecycle['mat_Recycling_yield'].loc[2030] = 60
glassimprovedrecycle['mat_Recycling_yield'].loc[2050] = 90

glassimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2022] = 0
glassimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2030] = 30
glassimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2050] = 75

glassimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2022] = 100
glassimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2030] = 100
glassimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2050] = 100


glassimprovedrecycle.interpolate()


# In[ ]:


idx_temp = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
columns = ['mat_MFG_scrap_Recycled','mat_MFG_scrap_Recycling_eff','mat_MFG_scrap_Recycled_into_HQ',
           'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG','mat_PG3_ReMFG_target','mat_ReMFG_yield',
           'mat_PG4_Recycling_target','mat_Recycling_yield','mat_EOL_Recycled_into_HQ','mat_EOL_RecycledHQ_Reused4MFG']
Siimprovedrecycle = pd.DataFrame(index=idx_temp, columns=columns, dtype=float)

#MFGing Scrap
Siimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2022] = 100
Siimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2030] = 100
Siimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2050] = 100

Siimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2022] = 20
Siimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2030] = 30
Siimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2050] = 60

Siimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2022] = 0
Siimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2030] = 50
Siimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2050] = 100

Siimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2022] = 100
Siimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2030] = 100
Siimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2050] = 100

#REMFG

Siimprovedrecycle['mat_PG3_ReMFG_target'].loc[2022] = 0
Siimprovedrecycle['mat_PG3_ReMFG_target'].loc[2030] = 30
Siimprovedrecycle['mat_PG3_ReMFG_target'].loc[2050] = 80

Siimprovedrecycle['mat_ReMFG_yield'].loc[2022] = 0
Siimprovedrecycle['mat_ReMFG_yield'].loc[2030] = 50
Siimprovedrecycle['mat_ReMFG_yield'].loc[2050] = 90

#EoL Recycling
Siimprovedrecycle['mat_PG4_Recycling_target'].loc[2022] = 100
Siimprovedrecycle['mat_PG4_Recycling_target'].loc[2030] = 50
Siimprovedrecycle['mat_PG4_Recycling_target'].loc[2050] = 10

Siimprovedrecycle['mat_Recycling_yield'].loc[2022] = 20
Siimprovedrecycle['mat_Recycling_yield'].loc[2030] = 30
Siimprovedrecycle['mat_Recycling_yield'].loc[2050] = 75

Siimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2022] = 0
Siimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2030] = 50
Siimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2050] = 90

Siimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2022] = 0
Siimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2030] = 100
Siimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2050] = 100


Siimprovedrecycle.interpolate()


# In[ ]:


idx_temp = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
columns = ['mat_MFG_scrap_Recycled','mat_MFG_scrap_Recycling_eff','mat_MFG_scrap_Recycled_into_HQ',
           'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG','mat_PG3_ReMFG_target','mat_ReMFG_yield',
           'mat_PG4_Recycling_target','mat_Recycling_yield','mat_EOL_Recycled_into_HQ','mat_EOL_RecycledHQ_Reused4MFG']
Alimprovedrecycle = pd.DataFrame(index=idx_temp, columns=columns, dtype=float)

#MFGing Scrap
Alimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2022] = 100
Alimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2030] = 100
Alimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2050] = 100

Alimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2022] = 60
Alimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2030] = 70
Alimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2050] = 90

Alimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2022] = 100
Alimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2030] = 100
Alimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2050] = 100

Alimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2022] = 100
Alimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2030] = 100
Alimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2050] = 100

#REMFG

Alimprovedrecycle['mat_PG3_ReMFG_target'].loc[2022] = 0
Alimprovedrecycle['mat_PG3_ReMFG_target'].loc[2030] = 0
Alimprovedrecycle['mat_PG3_ReMFG_target'].loc[2050] = 0

Alimprovedrecycle['mat_ReMFG_yield'].loc[2022] = 0
Alimprovedrecycle['mat_ReMFG_yield'].loc[2030] = 0
Alimprovedrecycle['mat_ReMFG_yield'].loc[2050] = 0

#EoL Recycling
Alimprovedrecycle['mat_PG4_Recycling_target'].loc[2022] = 100
Alimprovedrecycle['mat_PG4_Recycling_target'].loc[2030] = 100
Alimprovedrecycle['mat_PG4_Recycling_target'].loc[2050] = 100

Alimprovedrecycle['mat_Recycling_yield'].loc[2022] = 42
Alimprovedrecycle['mat_Recycling_yield'].loc[2030] = 75
Alimprovedrecycle['mat_Recycling_yield'].loc[2050] = 98

Alimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2022] = 100
Alimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2030] = 100
Alimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2050] = 100

Alimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2022] = 20
Alimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2030] = 50
Alimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2050] = 100


Alimprovedrecycle.interpolate()


# In[ ]:


idx_temp = pd.RangeIndex(start=2022,stop=2051,step=1) #create the index
columns = ['mat_MFG_scrap_Recycled','mat_MFG_scrap_Recycling_eff','mat_MFG_scrap_Recycled_into_HQ',
           'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG','mat_PG3_ReMFG_target','mat_ReMFG_yield',
           'mat_PG4_Recycling_target','mat_Recycling_yield','mat_EOL_Recycled_into_HQ','mat_EOL_RecycledHQ_Reused4MFG']
Agimprovedrecycle = pd.DataFrame(index=idx_temp, columns=columns, dtype=float)

#MFGing Scrap
Agimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2022] = 95
Agimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2030] = 100
Agimprovedrecycle['mat_MFG_scrap_Recycled'].loc[2050] = 100

Agimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2022] = 97
Agimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2030] = 98
Agimprovedrecycle['mat_MFG_scrap_Recycling_eff'].loc[2050] = 99

Agimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2022] = 100
Agimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2030] = 100
Agimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ'].loc[2050] = 100

Agimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2022] = 16.61
Agimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2030] = 30
Agimprovedrecycle['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].loc[2050] = 75

#REMFG

Agimprovedrecycle['mat_PG3_ReMFG_target'].loc[2022] = 0
Agimprovedrecycle['mat_PG3_ReMFG_target'].loc[2030] = 0
Agimprovedrecycle['mat_PG3_ReMFG_target'].loc[2050] = 0

Agimprovedrecycle['mat_ReMFG_yield'].loc[2022] = 0
Agimprovedrecycle['mat_ReMFG_yield'].loc[2030] = 0
Agimprovedrecycle['mat_ReMFG_yield'].loc[2050] = 0

#EoL Recycling
Agimprovedrecycle['mat_PG4_Recycling_target'].loc[2022] = 0
Agimprovedrecycle['mat_PG4_Recycling_target'].loc[2030] = 100
Agimprovedrecycle['mat_PG4_Recycling_target'].loc[2050] = 100

Agimprovedrecycle['mat_Recycling_yield'].loc[2022] = 97
Agimprovedrecycle['mat_Recycling_yield'].loc[2030] = 98
Agimprovedrecycle['mat_Recycling_yield'].loc[2050] = 99

Agimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2022] = 80
Agimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2030] = 100
Agimprovedrecycle['mat_EOL_Recycled_into_HQ'].loc[2050] = 100

Agimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2022] = 16.61
Agimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2030] = 30
Agimprovedrecycle['mat_EOL_RecycledHQ_Reused4MFG'].loc[2050] = 75


Agimprovedrecycle.interpolate()


# In[2]:


import PV_ICE


# In[ ]:


cdf = PV_ICE.weibull_cdf(12.596192434998898, 41.18098)

year = range(0,50,1)
cdfs = pd.DataFrame(index=year, columns=['cdf'], dtype=float)
for yr in year:
    cdfs.loc[yr] = cdf(yr)
    
#round(cdfs,2)
plt.plot(cdfs)


# In[ ]:


alpha = 12.596192434998898
beta = 41.18098


# In[ ]:


cdf = PV_ICE.weibull_cdf(12.596192434998898, 41.18098)

year = range(0,50,1)
cdfs = pd.DataFrame(index=year, columns=['cdf'], dtype=float)
for yr in year:
    cdfs.loc[yr] = cdf(yr)


# In[ ]:


def alphabeta2T50T90(alpha,beta):
    T10 = round(-beta*-np.abs(np.log(0.9))**(1/alpha),2)
    T50 = round(-beta*-np.abs(np.log(0.5))**(1/alpha),2)
    T90 = round(-beta*-np.abs(np.log(0.1))**(1/alpha),2)
    return T10,T50,T90


# In[ ]:


alphabeta2T50T90(alpha,beta)


# In[ ]:


alpha = pd.Series([x / 10.0 for x in range(1, 500,1)])
beta = pd.Series([x / 10.0 for x in range(1, 1000,1)])


# In[ ]:


ts = pd.DataFrame(columns=['alpha','beta','T10','T50','T90'], dtype=float)
for a in alpha:
    for b in beta:
        tstemp = pd.DataFrame(columns=['alpha','beta','T10','T50','T90'], dtype=float)
        tstemp['alpha'] = a
        tstemp['beta'] = b
        tstemp['T10'],tstemp['T50'],tstemp['T90'] = alphabeta2T50T90(a,b)
        ts = pd.concat([ts,tstemp])


# In[ ]:


tstemp


# In[3]:


def alphabeta2T10(alpha,beta):
    T10 = round(-beta*-np.abs(np.log(0.9))**(1/alpha),2)
    return T10


# In[8]:


PV_ICE.weibull_params({10:0.5,20:0.9})


# In[14]:


t5


# In[13]:


T50 = pd.Series(range(10,20,1))
T90 = pd.Series(range(11,21,1))
ts2 = pd.DataFrame(columns=['alpha','beta','T10','T50','T90'], dtype=float)
for t5 in T50:
    for t9 in T90:
        params = PV_ICE.weibull_params({t5:0.5,t9:0.9})
        T10 = alphabeta2T10(params['alpha'],params['beta'])
        tstemp2 = pd.DataFrame(columns=['alpha','beta','T10','T50','T90'], dtype=float)
        tstemp2['alpha'] = params['alpha']
        tstemp2['beta'] = params['beta']
        tstemp2['T50'] = t5
        tstemp2['T90'] = t9
        tstemp2['T10'] = T10
        ts2 = pd.concat([ts2,tstemp2])


# In[20]:


ts2


# In[16]:


params = PV_ICE.weibull_params({T50:0.5,T90:0.9})
T10 = alphabeta2T10(params['alpha'],params['beta'])
tstemp2 = pd.DataFrame(columns=['alpha','beta','T10','T50','T90'], dtype=float)
tstemp2['alpha'] = params['alpha']
tstemp2['beta'] = params['beta']
tstemp2['T50'] = t5
tstemp2['T90'] = t9
tstemp2['T10'] = T10
ts2 = pd.concat([ts2,tstemp2])


# In[ ]:


alphabeta2T10(1,5)


# In[ ]:


params = PV_ICE.weibull_params({t5:0.5,t9:0.9})
params['beta']

