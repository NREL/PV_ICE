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


plt.plot(IAI_refinesmelt_world, color='orange')
plt.title('World Alumina+Aluminum Smelting Energy \n Neglects Anode Energy and mining')
plt.ylabel('kWh/kg')
plt.ylim(10,22)


# In[ ]:





# In[ ]:





# ## Bauxite Mining

# In[11]:


#skipcols = ['Source', 'Notes','Country']
e_mineAl_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-mining.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[12]:


e_mineAl_raw.dropna(how='all')


# Mining energy is a small contributor. Unlike other ores, bauxite usually doesnt require blasting or apparently significant sorting/crushing. For conservative estimate, we will take the mean of the energy values and use 56% fuels from IAI (2018).

# In[13]:


mine_avg = e_mineAl_raw[['E_mine_kWhpkg']].mean().values
e_mineAl = pd.DataFrame({'E_mine_kWhpkg':mine_avg, 'PrctFuel':56}, index=e_mineAl_raw.index)
e_mineAl.head()


# ## Alumina Production & Aluminum Smelting
# This step includes the production of alumina from bauxite, and the smelting of aluminum from alumina through the Hall-H process. Energy of the anode has been included here (i.e. more than just electricity and fuels) because the anode is critical and is mostly fuels and electricity.

# In[14]:


#skipcols = ['Source', 'Notes','Country']
e_refinesmeltAl_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-refinesmelt.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[15]:


e_refinesmeltAl_raw.dropna(how='all')


# In[16]:


plt.scatter(e_refinesmeltAl_raw.index, e_refinesmeltAl_raw['E_refineSmelt_kWhpkg'], marker='o')
plt.title('Energy Refine and Smelt Raw Lit')
plt.ylabel('kWh/kg')
plt.plot(IAI_refinesmelt_world, color='orange')


# In[17]:


#teasing out the differences
e_refinesmeltAl_trim = e_refinesmeltAl_raw.dropna(how='all')
e_refinesmeltAl_trim_elecOnly = e_refinesmeltAl_trim[e_refinesmeltAl_trim['Notes'].str.contains('electricity only')]
e_refinesmeltAl_trim_elecOnly.index


# In[18]:


plt.scatter(e_refinesmeltAl_raw.index, e_refinesmeltAl_raw['E_refineSmelt_kWhpkg'], marker='o')
plt.scatter(e_refinesmeltAl_trim_elecOnly.index, e_refinesmeltAl_trim_elecOnly['E_refineSmelt_kWhpkg'], marker='o', color='red')

plt.title('Energy Refine and Smelt Raw Lit')
plt.ylabel('kWh/kg')
plt.plot(IAI_refinesmelt_world, color='orange')


# The low values are electricity only, while the higher values are full energy demand. Therefore we will drop those numbers, and interpolate between the full energy numbers

# In[19]:


#set the electricity only rows to Nan
e_refinesmeltAl = e_refinesmeltAl_raw.copy()
e_refinesmeltAl.loc[e_refinesmeltAl_raw.index.isin(e_refinesmeltAl_trim_elecOnly.index),:]=np.nan
e_refinesmeltAl.head()


# In[20]:


plt.scatter(e_refinesmeltAl.index, e_refinesmeltAl['E_refineSmelt_kWhpkg'], marker='o')

plt.title('Energy Refine and Smelt Gross Energy')
plt.ylabel('kWh/kg')
plt.plot(IAI_refinesmelt_world, color='orange')


# In[21]:


e_refinesmeltAl.dropna(how='all')


# Based on the resources and level of detailed information provided, I trust the International Aluminum Institute and (therefore) Lennon et al 2022 more than Farjana. Therefore, we will drop Farjana and interpolate. We will also use the 21% fuels vs electricity from IAI (2018).

# In[22]:


e_refinesmeltAl.loc[2020]=np.nan #droping Farjana
e_refinesmeltAl_filled = e_refinesmeltAl.loc[1995:,['E_refineSmelt_kWhpkg']].interpolate()
e_refinesmeltAl_filled['PrctFuel'] = e_refinesmeltAl.loc[2018,'PrctFuel']


# In[23]:


plt.plot(e_refinesmeltAl_filled)
plt.title('Energy to Refine and Smelt Al')
plt.ylabel('kWh/kg')
plt.legend(e_refinesmeltAl_filled.columns)


# ## Casting, Extruding, Anodizing

# In[24]:


#skipcols = ['Source', 'Notes','Country']
e_formanodize_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-formanodize.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[25]:


e_formanodize_raw.dropna(how='all')


# These are not helped by plotting. extrude and anodize seem to be mostly thermal processes maxing out around 5 kWh/kg. (Note the Harscoet is in kg/m2, not per mass and are intented to be added together. Therefore we will assume 5 kWh/kg and 87% of the energy is fuels for thermal.

# In[26]:


e_formanodize = pd.DataFrame({'E_formanodize_kWhpkg':5.0,'PrctFuel':87}, index=e_formanodize_raw.index)


# In[27]:


#plt.plot(e_formanodize)


# ## Sum the Mining, Refine and Smelt, and Form and Anodize Energies

# In[28]:


pd.concat([e_refinesmeltAl_filled,e_formanodize], axis=1)


# In[29]:


e_AlFrames = e_refinesmeltAl_filled['E_refineSmelt_kWhpkg']+e_formanodize['E_formanodize_kWhpkg']


# In[30]:


#e_mine_wtd = e_mineAl['E_mine_kWhpkg']*(e_mineAl['PrctFuel']/100)
e_refine_wtd = e_refinesmeltAl_filled['E_refineSmelt_kWhpkg']*(e_refinesmeltAl_filled['PrctFuel']/100)
e_form_wtd = e_formanodize['E_formanodize_kWhpkg']*(e_formanodize['PrctFuel']/100)
fuel_sum = e_refine_wtd+e_form_wtd


# In[31]:


fuel_prct = fuel_sum/e_AlFrames


# In[32]:


e_AlFrames_final = pd.concat([e_AlFrames,fuel_prct*100], axis=1, keys=['E_AlFrames_kWhpkg','PrctFuel'])
e_AlFrames_final.to_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/output-energy-aluminumframes.csv")


# ## Cumulative Energy Demand Comparison

# In[33]:


#skipcols = ['Source', 'Notes','Country']
e_AlCED_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-CED.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[34]:


e_AlCED_raw.dropna(how='all')


# In[35]:


#literature
plt.scatter(e_AlCED_raw.index, e_AlCED_raw['PED_kWhpkg'], marker='o', label='Lit. CED')
plt.scatter(e_AlCED_raw.index, e_AlCED_raw['PrctFuel'], marker='^', color='orange', label='Lit. %Fuel')
plt.plot(IAI_refinesmelt_world, color='blue', label='Lit. Refine&Smelt')
#our baseline
plt.plot(e_AlFrames_final, label=['PVICE Energy','PVICE % Fuel'], ls='--')

plt.title('Energy for Al Frames\n Comparison with Literature')
plt.ylabel('kWh/kg and %')
plt.xlim(1993,2025)
plt.legend()


# In[ ]:





# ## Recycling

# In[36]:


#skipcols = ['Source', 'Notes','Country']
e_recycleAl_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-aluminum-recycle.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[37]:


e_recycleAl_raw.dropna(how='all')


# The regular reported energy savings is that recycling is only ~5% of primary Al production. So either I can use these raw data, OR can take 5% of the CED of Al MFGing energy

# In[38]:


plt.scatter(e_recycleAl_raw.index,e_recycleAl_raw['E_recycle_kWhpkg'])
plt.title('Energy of Recycling Aluminum')
plt.ylabel('kWh/kg')


# In[39]:


e_recycleAl_raw['E_recycle_kWhpkg'].mean()


# In[40]:


e_recycleAl_raw['E_recycle_kWhpkg'].mean()/e_AlFrames_final['E_AlFrames_kWhpkg']


# The mean gets to be ~15% of CED, which is too high, and it increases over time, which we don't expect, so we can't just use the mean.

# In[41]:


e_AlFrames_final['E_AlFrames_kWhpkg']*0.08


# 8% of the CEd is more reasonable, but drops fairly low by the end.
# 
# The Wang 2022 publication from The Aluminum Association is an LCA update with global data from manufacturers. This publication also breaks down 100% recycled scrap (CED of 2.5 kWh/kg, 7% of their primary Al CED) and a product realistic which has a high recycled content but uses a small amount of primary aluminum to enable precise alloying (CED of 4.6 kWh/kg, 12% of primary Al CED). We will therefore use these data.
# 
# * LQ open-loop recycling will be 2.5 kWh/kg.
# * HQ open-loop and closed-loop recycling will be an additional 2.1 kWh/kg at EOL. For MFG HQ, no additional energy is needed, since it just gets remelted with no contamination issues.
# * 80% fuel fraction will be used for recycled material

# In[43]:


4.6/e_AlFrames_final['E_AlFrames_kWhpkg']

