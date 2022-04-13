#!/usr/bin/env python
# coding: utf-8

# # Energy Requirements of Glass Manufacturing

# This journal creates a baseline for the energy required to manufacture glass for PV applications. The processes covered here include batch prep, melting, forming, and post forming (ex: annealing). Most glass facilities are vertically integrated; once the silica and other raw materials arrive, they are mixed into proportional batches, melted, formed, and any post forming processes applied. Therefore, we will calcualte this as a single energy step, with transportation of the silica and the finished glass cut to size before and after this energy demand.
# 
# While most PV glass is rolled glass, some is float. In the literature it is hard to distinguish the energy needs and processing of float versus rolled, so here one is used interchangeably for the other. 
# 
# 

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (10, 6)


# ## Batch Prep
# 
# Batch preparation for glass typically involves the mixing of the constituant materials for the glass, including high quality silica and additives such as Al2O3, CaO, MgO, Na2O. This can involve crushers and mixers and conveyer belts. 

# In[2]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_batchglass_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-batchglass.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[3]:


e_batchglass_raw.dropna(how='all')


# In[4]:


plt.plot(e_batchglass_raw.index,e_batchglass_raw.iloc[:,0], marker='o')
plt.title('Energy: Batching Glass')
plt.ylabel('[kWh/kg]')


# The early 2000s data seems significantly higher than the other points. Both are trusted DOE sources. The UK data point assumes 50% cullet, which we know to be high for float/rolled glass, but in mixing, is seems like this wouldn't cause a significant difference in energy demand. Also, the UK value includes contributions from ethane/methane, implying a heating or drying energy demand not represented by the others.
# 
# Overall, all values are quite low on a kWh/kg basis, and the processing tools for this step have not changed significantly in the studied time frame. Therefore, we will average all values together for our baseline.

# In[5]:


avg_batch_e = e_batchglass_raw.iloc[:,0].mean()
print('The average batching energy for glass making is '+str(round(avg_batch_e,3)) + ' kWh/kg.')


# In[6]:


e_batchglass_trim = e_batchglass_raw.loc[1995:,['E_batchingGlass_kWhpkg','Prct_Fuel_batch']]


# In[7]:


e_batchglass_trim['E_batchingGlass_kWhpkg']=avg_batch_e
e_batchglass_trim['Prct_Fuel_batch']=0.0
e_batchglass_trim


# ## Melting
# 
# The next step in glass manufacturing is the melting of the glass. This is seperated out in the literature from the forming, although the process is usually continuous. This step also involves a significant quantity of methane gas heating. We will note this important aspect in our accounting as a fraciton of the total energy neede for each step.

# In[8]:


cwd = os.getcwd()
#skipcols = ['Source', 'Notes','Country']
e_meltrefine_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-glass-meltrefine.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[9]:


e_meltrefine_raw.dropna(how='all')


# In[10]:


e_meltrefine_raw.loc[2019,'Notes']


# One of the fractions of methane is lower than the others. This is M. Zier, P. Stenzel, L. Kotzur, and D. Stolten, “A review of decarbonization options for the glass industry,” Energy Conversion and Management: X, vol. 10, p. 100083, Jun. 2021, doi: 10.1016/j.ecmx.2021.100083. and the energy was adjusted by the overall energy carrier for glass manufacturing in Germany. This may not be representative of the whole world, and it may also include more than just the melting step. Given that the other years are all in agreement, and the 77% is an average since the 1990s, we will remove this value and use the previous datapoint (95% from Worrell).

# In[11]:


e_meltrefine = e_meltrefine_raw.copy()
e_meltrefine.loc[2019,'Prct_Fuel_melt'] = np.nan

#previous version used the average of all values, but this cause the fraction to rise again.
#e_meltrefine.loc[2019,'Prct_Fuel'] = round(e_meltrefine.loc[:,'Prct_Fuel'].mean(),0) 
#e_meltrefine.loc[2019,'Prct_Fuel']


# Now we'll examine the energy totals.

# In[12]:


plt.plot(e_meltrefine.index,e_meltrefine.iloc[:,0], marker='o')
plt.title('Energy: Melt and Refine Glass')
plt.ylabel('[kWh/kg]')


# The 1980 value is much lower than the 1997 value. This data point is from H. L. Brown, Energy Analysis of 108 Industrial Processes. The Fairmont Press, Inc., 1996. (note the publication date and the data date are not the same). and the noted batch size is a few pounds, meaning this is potentially a different scale of glass manufacturing than we are considering. Additionally, we only need to go back to 1995, therefore, we will drop this datapoint, and back propogate the 1997 data.

# In[13]:


e_meltrefine_subrange = e_meltrefine.loc[1995:,['E_melt_refine_total_kWhpkg','Prct_Fuel_melt']]


# Now we will interpolate to create a complete data set for history. It will hold the edge values constant forward and backward.

# In[14]:


e_meltrefine_filled = e_meltrefine_subrange.interpolate(limit_direction='both')


# In[15]:


fig, ax1 = plt.subplots() 
#left axis
ax1.set_ylabel('Melting and Refining Energy [kWh/kg]', color='blue') 
ax1.plot(e_meltrefine_filled.index,e_meltrefine_filled.iloc[:,0], color='blue') 
ax1.set_ylim(0,4)

#right axis
ax2 = ax1.twinx()
plt.ylabel('Fraction of Energy provided by Methane [%]', color='red')
ax2.plot(e_meltrefine_filled.index,e_meltrefine_filled.iloc[:,1], color='red')  
ax2.set_ylim(80,100)

plt.show()


# In[16]:


e_meltrefine_filled.to_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/output_energy_glass_meltrefine.csv")


# ## Forming
# The next step in flat glass formation is forming the flat plate from the melt. There are many ways to do this; float glass entails the molten glass to drop into and float on a bath of molten tin; Rolled glass is drawn through cooled rollers. We will use these two processes interchangably here due to a lack of data.

# In[17]:


cwd = os.getcwd()
#skipcols = ['Source', 'Notes','Country']
e_glassform_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-glassforming.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[18]:


e_glassform_raw.dropna(how='all')


# In[19]:


plt.plot(e_glassform_raw.index,e_glassform_raw['E_Glassforming_kWhpkg'], marker='o')
plt.title('Energy of Forming Flat glass')
plt.xlabel('[kWh/kg]')


# Like the previous set of data, the 1980 datapoint seems unreasonably low, and we know this might potentially be a smaller scale than the other data. Therefore, we will exclude it and perform the same interpolation for the needed time range.

# In[20]:


e_glassform = e_glassform_raw.loc[1995:,['E_Glassforming_kWhpkg','Prct_Fuel_form']]
e_glassform_filled = e_glassform.interpolate(limit_direction='both')


# In[21]:


fig, ax1 = plt.subplots() 
#left axis
ax1.set_ylabel('[kWh/kg]', color='blue') 
ax1.plot(e_glassform_filled.index,e_glassform_filled.iloc[:,0], color='blue') 
ax1.set_ylim(0,1)

#right axis
#ax2 = ax1.twinx()
#plt.ylabel('Fraction of Energy provided by Methane [%]', color='red')
#ax2.plot(e_glassform_filled.index,e_glassform_filled.iloc[:,1], color='red')  
#ax2.set_ylim(0,2)

plt.title('Energy for Forming Flat Glass')

plt.show()


# In[22]:


e_glassform_filled.to_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/output_energy_glass_formflat.csv")


# ## Post Forming: Anneal and Temper
# 
# All PV flat glass for c-Si PV is tempered for safety reasons, and all tempered glass has already been annealed. Therefore, we will account for both the energy to anneal and temper the flat glass.
# 
# For Bifacial PV technology, the glasses are actually NOT tempered. They are heat treated instead. LOOK INTO DIFFERENCES IN THIS ENERGY DEMAND.

# In[23]:


cwd = os.getcwd()
#skipcols = ['Source', 'Notes','Country']
e_glass_annealtemper_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-glass-postforming.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[24]:


e_glass_annealtemper_raw.dropna(how='all')


# In[25]:


e_glass_annealtemper_raw.loc[1997,'Notes']


# In[26]:


plt.plot(e_glass_annealtemper_raw.index,e_glass_annealtemper_raw['E_GlassTempering_kWhpkg'], marker='o')
plt.title('Energy of Annealing and Tempering Flat glass')
plt.xlabel('[kWh/kg]')


# Once again, the 1980 datapoint seems excessively low and will therefore be excluded.
# 
# The jump between 1997 and 2001 data seems unlikely to be a trend and more attributable to differing methods of calculating the energy requirements. The modern datapoint falls between these two points. Therefore, like for the batching energy, we wil take an average of these 3 points and use that for all time. 

# In[27]:


e_glass_annealtemper_trim = e_glass_annealtemper_raw.loc[1995:,['E_GlassTempering_kWhpkg','Prct_fuel_annealtemper']]


# In[28]:


avg_annealtemper_e = e_glass_annealtemper_trim.iloc[:,0].mean()
avg_prctfuel_annealtemper = e_glass_annealtemper_trim.iloc[:,1].mean()
e_glass_annealtemper_trim['E_GlassTempering_kWhpkg']= avg_annealtemper_e
e_glass_annealtemper_trim['Prct_fuel_annealtemper']= avg_prctfuel_annealtemper
e_glass_annealtemper_trim


# ## Combine All MFG energy
# 
# For the energy baseline to match up with the mass baseline, we are separating the energy demands into virgin material, transport, and manufacturing energy. This journal covers the Manufacturing energy, batch processing through forming and cutting. The following calculation sum all the energies associate with manufacturing at the flat glass facility.
# 
# To track the use of methane/natural gas in the processing, we will do a weighted average percent fuel column to accompany the total energy value.

# In[29]:


dfs = [e_batchglass_trim, e_meltrefine_filled, e_glassform_filled, e_glass_annealtemper_trim]
energies_mfg_glass = pd.concat(dfs, axis=1)
energies_mfg_glass


# In[30]:


#Sum the manufacturing energies
energies_mfg_glass['E_mfg_glass_kWhpkg'] = energies_mfg_glass.filter(regex='^E_').sum(axis=1)


# In[31]:


#Take weighted average of PRCT Fuel by energy step
