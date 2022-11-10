#!/usr/bin/env python
# coding: utf-8

# # Energy Requirements of Aluminum Frames MFGing
# This journal documents the processing of literature data of the manufacturing energy of aluminum frames, from mining through extrusion, and recycling.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (10, 6)
cwd = os.getcwd() #grabs current working directory


# ### Aluminum LCI 2019
# This is a nice LCI/LCA from the International Aluminum Inst. updated in 2019. Pulling global energy details in here. NOTE MJ/tonne.

# In[2]:


pd.read_excel(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/InternationalAluminumInst-2019-LCI-energyGLO.xlsx")


# This resource also has timelines of energy demand of the two most energy intensive steps over time.

# In[3]:


#alumina to aluminum
IAI_alumina_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/InternationalAluminumInst-1995-2021-PrimaryAluminaRefineEnergy-MJpTonne.csv",
                                     index_col='year')
IAI_alumina_raw


# In[4]:


IAI_alumina_kwhpkg = (IAI_alumina_raw*0.2777)/1000 #convert from MJ/tonne to kWh/kg
IAI_alumina_kwhpkg.loc[2001] = np.nan# drop the weirdness at 2001
IAI_alumina_kwhpkg.interpolate(inplace=True) #replace with interpolated data


# In[5]:


plt.plot(IAI_alumina_kwhpkg)
plt.legend(IAI_alumina_kwhpkg.columns)
plt.ylabel('kWh/kg')
plt.title('Alumina Refining Energy')


# In[ ]:





# In[6]:


#Smelting energy
IAI_aluminumSmelt_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/InternationalAluminumInst-1995-2021-PrimaryAlSmeltEnergy-kWhpTonne.csv",
                                     index_col=['year','Type'])
IAI_aluminumSmelt_raw.head()


# In[7]:


#we probably only want the total energy, as process energy is dc.
#IAI_aluminumSmelt_raw.loc[(slice(None),['Total Energy_ac']),:] #slice on the multilevel
#IAI_aluminumSmelt_totE = IAI_aluminumSmelt_raw[['World']].xs('Total Energy_ac', level=1) # slice on the multilevel, option to drop the type column
IAI_aluminumSmelt_totE = IAI_aluminumSmelt_raw.xs('Total Energy_ac', level=1) # slice on the multilevel, option to drop the type column
IAI_aluminumSmelt_totE.head()


# In[8]:


plt.plot(IAI_aluminumSmelt_totE/1000)
plt.title('Total Energy (AC) Aluminum Smelting')
plt.ylabel('kWh/kg')
plt.ylim(10,18)
plt.legend(IAI_aluminumSmelt_totE.columns, fontsize=12, loc='lower left')


# In[9]:


#add these two processes together
IAI_alumina_kwhpkg_world = IAI_alumina_kwhpkg[['World']]
IAI_aluminumSmelt_totE_world = IAI_aluminumSmelt_totE[['World']]/1000
IAI_refinesmelt_world = IAI_alumina_kwhpkg_world + IAI_aluminumSmelt_totE_world


# In[10]:


plt.plot(IAI_refinesmelt_world)
plt.title('World Alumina+Aluminum Smelting Energy \n Neglects Anode Energy and mining')
plt.ylabel('kWh/kg')


# In[ ]:





# In[ ]:





# ## Bauxite Mining

# In[11]:


#skipcols = ['Source', 'Notes','Country']
e_mineAl_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-mining.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[12]:


e_mineAl_raw.dropna(how='all')


# So this is a massively wide range. I have confidence in the International Aluminum Inst. LCI, but it is also the highest value. However, when compared to the other numbers from that report, it is still <1% of the overall energy demand

# In[ ]:





# In[ ]:





# ## Alumina Production & Aluminum Smelting
# This step includes the production of alumina from bauxite, and the smelting of aluminum from alumina through the Hall-H process. Energy of the anode has been included here (i.e. more than just electricity and fuels) because the anode is critical and is mostly fuels and electricity.

# In[13]:


#skipcols = ['Source', 'Notes','Country']
e_refinesmeltAl_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-refinesmelt.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[14]:


e_refinesmeltAl_raw.dropna(how='all')


# In[15]:


plt.scatter(e_refinesmeltAl_raw.index, e_refinesmeltAl_raw['E_refineSmelt_kWhpkg'], marker='o')
plt.title('Energy Refine and Smelt Raw Lit')
plt.ylabel('kWh/kg')
plt.plot(IAI_refinesmelt_world, color='orange')


# In[16]:


#teasing out the differences
e_refinesmeltAl_trim = e_refinesmeltAl_raw.dropna(how='all')
e_refinesmeltAl_trim_elecOnly = e_refinesmeltAl_trim[e_refinesmeltAl_trim['Notes'].str.contains('electricity only')]


# In[17]:


plt.scatter(e_refinesmeltAl_raw.index, e_refinesmeltAl_raw['E_refineSmelt_kWhpkg'], marker='o')
plt.scatter(e_refinesmeltAl_trim_elecOnly.index, e_refinesmeltAl_trim_elecOnly['E_refineSmelt_kWhpkg'], marker='o', color='red')

plt.title('Energy Refine and Smelt Raw Lit')
plt.ylabel('kWh/kg')
plt.plot(IAI_refinesmelt_world, color='orange')


# The low values are electricity only, while the higher values are full energy demand. Therefore we will drop those numbers, and interpolate between the full energy numbers

# In[43]:


#remove the electricity only rows
#e_refinesmeltAl_raw.loc[~e_refinesmeltAl_raw.index.isin(e_refinesmeltAl_trim.index),:]
e_refinesmeltAl_raw[~e_refinesmeltAl_trim['Notes'].str.contains('electricity only')]

#.loc[:,~allenergy.columns.isin(energyGen.columns)], e_refinesmeltAl_trim_elecOnly 
#e_refinesmeltAl_trim[e_refinesmeltAl_trim['Notes'].str.contains('electricity only')]
#IAI_aluminumSmelt_raw.loc[(slice(None),['Total Energy_ac']),:] #slice on the multilevel
#IAI_aluminumSmelt_totE = IAI_aluminumSmelt_raw[['World']].xs('Total Energy_ac', level=1) # slice on the multilevel


# In[ ]:





# ## Casting, Extruding, Anodizing

# In[18]:


#skipcols = ['Source', 'Notes','Country']
e_formanodize_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-formanodize.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[19]:


e_formanodize_raw.dropna(how='all')


# These are not helped by plotting. extrude and anodize seem to be mostly thermal processes maxing out around 5 kWh/kg. (Note the Harscoet is in kg/m2, not per mass and are intented to be added together. Therefore we will assume 5 kWh/kg and 87% of the energy is fuels for thermal.

# In[ ]:





# In[ ]:





# ## Cumulative Energy Demand Comparison

# In[20]:


#skipcols = ['Source', 'Notes','Country']
e_AlCED_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-CED.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[21]:


e_AlCED_raw.dropna(how='all')


# In[22]:


plt.scatter(e_AlCED_raw.index, e_AlCED_raw['PED_kWhpkg'], marker='o')
plt.title('Cumulative Energy Demand Raw Lit')
plt.ylabel('kWh/kg')
plt.plot(IAI_refinesmelt_world, color='orange')


# In[ ]:





# In[ ]:





# In[ ]:





# ## Recycling

# In[23]:


#skipcols = ['Source', 'Notes','Country']
e_recycleAl_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-recycle.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[24]:


e_recycleAl_raw.dropna(how='all')


# The regular reported energy savings is that recycling is only ~5% of primary Al production. So either I can use these raw data, OR can take 5% of the CED of Al MFGing energy

# In[26]:


plt.scatter(e_recycleAl_raw.index,e_recycleAl_raw['E_recycle_kWhpkg'])
plt.title('Energy of Recycling Aluminum')
plt.ylabel('kWh/kg')


# In[ ]:




