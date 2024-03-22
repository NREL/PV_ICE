#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (10, 6)
cwd = os.getcwd() #grabs current working directory


# In[2]:


#alumina to aluminum
IAI_alumina_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/InternationalAluminumInst-1995-2021-PrimaryAluminaRefineEnergy-MJpTonne.csv",
                                     index_col='year')
#IAI_alumina_raw.head()

#Smelting energy
IAI_aluminumSmelt_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/InternationalAluminumInst-1995-2021-PrimaryAlSmeltEnergy-kWhpTonne.csv",
                                     index_col=['year','Type'])
#IAI_aluminumSmelt_raw.head()


# In[3]:


IAI_alumina_kwhpkg = (IAI_alumina_raw*0.2777)/1000 #convert from MJ/tonne to kWh/kg
IAI_alumina_kwhpkg.loc[2001] = np.nan# drop the weirdness at 2001
IAI_alumina_kwhpkg.interpolate(inplace=True) #replace with interpolated data


# In[4]:


plt.plot(IAI_alumina_kwhpkg)
plt.legend(IAI_alumina_kwhpkg.columns)
plt.ylabel('kWh/kg')
plt.title('Alumina Refining Energy')


# In[ ]:





# In[5]:


#we probably only want the total energy, as process energy is dc.
#IAI_aluminumSmelt_raw.loc[(slice(None),['Total Energy_ac']),:] #slice on the multilevel
#IAI_aluminumSmelt_totE = IAI_aluminumSmelt_raw[['World']].xs('Total Energy_ac', level=1) # slice on the multilevel, option to drop the type column
IAI_aluminumSmelt_totE = IAI_aluminumSmelt_raw.xs('Total Energy_ac', level=1) # slice on the multilevel, option to drop the type column
IAI_aluminumSmelt_totE.head()


# In[6]:


plt.plot(IAI_aluminumSmelt_totE/1000)
plt.title('Total Energy (AC) Aluminum Smelting')
plt.ylabel('kWh/kg')
plt.ylim(10,18)
plt.legend(IAI_aluminumSmelt_totE.columns, fontsize=12, loc='lower left')


# In[7]:


#add these two processes together
IAI_alumina_kwhpkg_world = IAI_alumina_kwhpkg[['World']]
IAI_aluminumSmelt_totE_world = IAI_aluminumSmelt_totE[['World']]/1000
IAI_refinesmelt_world = IAI_alumina_kwhpkg_world + IAI_aluminumSmelt_totE_world


# In[8]:


plt.plot(IAI_refinesmelt_world, color='orange')
plt.title('World Alumina+Aluminum Smelting Energy \n Neglects Anode Energy and mining')
plt.ylabel('kWh/kg')
plt.ylim(10,22)


# In[14]:


#create a percentage of each energy (alumina vs aluminium) by country
IAI_aluminumSmelt_kWhpkg = IAI_aluminumSmelt_totE/1000 #this was in kWh/tonne


# In[15]:


IAI_alumina_kwhpkg+IAI_aluminumSmelt_kWhpkg


# In[18]:


IAI_aluminumSmelt_kWhpkg.add(IAI_alumina_kwhpkg)


# In[16]:


IAI_aluminumSmelt_kWhpkg.columns


# In[17]:


IAI_alumina_kwhpkg.columns

