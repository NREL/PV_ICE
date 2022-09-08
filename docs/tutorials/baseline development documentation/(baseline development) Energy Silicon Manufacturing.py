#!/usr/bin/env python
# coding: utf-8

# # Energy Requirements of Silicon Manufacturing

# This journal creates a baseline for the energy required to manufacture silicon for PV applications. The processes covered here include silica to MG-Si, MG-Si to polysilicon (siemens and FBR), Cz ingot growth, wafering, and cell processing steps. 
# 
# 

# In[3]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (10, 6)
cwd = os.getcwd() #grabs current working directory


# ## Silica to MG-Si
# 
# After mining cleaning the silica sand to sufficient purity (>95%), the silica sand is mixed with carboniferous materials and undergoes carbothermic reduction to extract the silicon. This is referred to as metallurgical grade silicon, or MG-Si. The carbothermic reduction is generally done in an arc furnace, frequently an electric arc furnace.

# In[2]:


cwd = os.getcwd() #grabs current working directory
#skipcols = ['Source', 'Notes','Country']
e_reducesilica_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-silicon-reduceSilicaSi.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[3]:


e_reducesilica_raw.dropna(how='all')


# In[4]:


plt.scatter(e_reducesilica_raw.index,e_reducesilica_raw.iloc[:,0])
plt.title('Electricity: Silica Reduction')
plt.ylabel('[kWh/kg]')


# Two of the energy points are higher than the others, 1990 from Phylipsen and Alsema, and 2016 from Chen et al. From Phylipsen and Alsema, the note explains that 51.34 kWh/kg is the sum of direct process energy (13 kWh/kg) and the primary energy demand of the carbon inputs+carbon electrodes (11.4kWh/kg). Similarly, Chen et al 2016 has 27 kWh/kg as the sum of electricity plus carbon inputs+carbon electrodes. Our current method is to capture only the electricity or thermal process energy (natural gas/methane) in the energy flows. 
# 
# The final datapoint from Heidari and Anctil also includes electricity plus carbon; they use the 2020 Muller/PVPS electricity value of 11 kWh/kg.
# 
# Therefore, we will adjust the values for these sections down to just the electricity numbers.

# In[5]:


e_reducesilica_raw.loc[1990,['E_reduce_SilicatoMGSi']] = 13.0 #Phylipsen Alsema
e_reducesilica_raw.loc[2016,['E_reduce_SilicatoMGSi']] = 12.0 #Chen Fig. 2
e_reducesilica_raw.loc[2022,['E_reduce_SilicatoMGSi']] = 11.0 #Heidari Anctil


# In[6]:


plt.scatter(e_reducesilica_raw.index,e_reducesilica_raw.iloc[:,0])
plt.title('Electricity: Silica Reduction')
plt.ylabel('[kWh/kg]')


# Literature values for electric arc furnaces range from 11-13 kWh/kg of MG-Si. Chen et al 2017 notes that while electric arc furnaces in EU countries have energy demands around 11 kWh/kg, Chinese arc furnaces average around 13.1 kWh/kg. The marketshare of Chinese MG-Si has increased in the last decade, as documented in Heidari and Anctil 2022 (derived from USGS 2020, Figure 3.D) between 2005 and 2018.
# 
# Pre 2005, we will do a linear interpolation between 1990 values and 2005 values.
# 
# 2005-2018, we will do a marketshare weighting of RoW = 11 kWh/kg and China = 13 kWh/kg.
# 
# 2018 through 2030, we will do a linear interpolation down to 11 kWh/kg, assuming continued improvement.

# In[7]:


#Pre-2005
#take average of pre 2005 value
e_reducesilica = pd.DataFrame(columns=['E_reduceSilicatoMGSi'], index=range(1990,2005))
e_reducesilica.index.name='year'
e_reducesilica.loc[1990,['E_reduceSilicatoMGSi']] = e_reducesilica_raw.loc[:1995,['E_reduce_SilicatoMGSi']].dropna(how='all').mean().iloc[0]
#e_reducesilica


# In[8]:


#2005-2018
mrktshr_mgsi_region = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-silicon-marketshareMGSiProdRegion.csv", index_col='year')
mrktshr_mgsi_region['MarketShare_RoW_MGSi'] = 1.0-mrktshr_mgsi_region['MarketShare_Chinese_MGSi']
mrktshr_mgsi_region['MarketShare_Chinese_MGSi']*=13 #multiply by kWh/kg China
mrktshr_mgsi_region['MarketShare_RoW_MGSi']*=11 #multiply by kWh/kg RoW
wtd_mrktshr_mgsi_region = pd.DataFrame(mrktshr_mgsi_region.sum(axis=1)) #sum weighted kWh/kg, is a series
wtd_mrktshr_mgsi_region.columns=['E_reduceSilicatoMGSi'] #rename for merge/join
#wtd_mrktshr_mgsi_region


# In[9]:


#2018-2030, linear decrease to 11 kWh/kg in 2030
e_reducesilica_end = pd.DataFrame(columns=['E_reduceSilicatoMGSi'], index=range(2019,2031))
e_reducesilica_end.index.name='year'
e_reducesilica_end.loc[2030,['E_reduceSilicatoMGSi']] = 11
#e_reducesilica_end


# In[10]:


#join all together
e_reducesilica_gappy = pd.concat([e_reducesilica,wtd_mrktshr_mgsi_region,e_reducesilica_end])


# In[11]:


e_reducesilica_gaps = e_reducesilica_gappy.astype(float) #for some reason this was objects?!
e_reducesilica_full = e_reducesilica_gaps.interpolate() #linearly interpolate between points
e_reducesilica_trim = e_reducesilica_full.loc[1995:,['E_reduceSilicatoMGSi']] #trim to 1995-2030


# In[12]:


plt.plot(e_reducesilica_trim)
plt.title('Electricity to reduce silica to MG-Si')
plt.ylabel('Electricity Demand [kWh/kg]')


# ## Refine MG-Si to Solar or Electrical Grade polysilicon
# 
# The next step in crystalline silicon PV cell manufacturing is purifying or refining the metallurgical grade silicon to solar or electronic grade polysilicon. Currently this is primarily done through the Seimens process, which entails conversion through trichlorosilane:
# 
#     Si(s) + 3HCl = HSiCl3 + H2        (26)  followed by HSiCl3 + 3H = Si + 3HCl
#     This reaction occurs at 350°C normally without a catalyst. A competing reaction is 
#     Si(s) + 4HCl = SiCl4 + 2H2        (27) 
#     contributing to the formation of unsuitable tetrachlorosilane in molar proportion of 10 to 20%."
#     "for  each  mole  of  Si  converted  to  polysilicon,  3  to  4  moles  are  converted  to SiCl4,"
#     "The present market of fumed silica is about 60 000 MT measured in terms of silicon unit. This presently corresponds to three times the  output  of  polysilicon  in  2000."
# 	A. CIFTJA, “Refining and Recycling of Silicon: A Review,” NORWEGIAN UNIVERSITY OF SCIENCE AND TECHNOLOGY, Feb. 2008.
# 
# Here we will combine the steps of MG-Si to Trichlorosilane and trichlorosilane to polysilicon electricity demands. Please note these are electricity demands, not total ENERGY demands.
# 
# We will create energy values for both the Siemens process and the FBR process as options for user.

# In[13]:


#skipcols = ['Source', 'Notes','Country']
e_refinesilicon_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-silicon-refineMGtoSo.csv",
                                     index_col='year')#, usecols=lambda x: x not in skipcols)


# In[14]:


#split siemens and fbr dataframes
e_refineSi_siemens = e_refinesilicon_raw.iloc[:,0:2]
e_refineSi_fbr = e_refinesilicon_raw.iloc[:,3:5]


# ### Siemens

# In[15]:


e_refineSi_siemens.dropna(how='all')


# In[16]:


plt.scatter(e_refineSi_siemens.index,e_refineSi_siemens.iloc[:,0])
plt.title('Electricity: Siemens Process')
plt.ylabel('[kWh/kg]')


# Starting with the major outlier in 1996 from Williams et al 2002. This data point is the sum of 250 and 50 from Table 3, and the data is sourced from 3 citations ranging from 1990 through 1998. It is noted that this is the electrical energy for the two Siemens steps. Handbook from 1990 has the 250, 305 enegries but these are for small reactors, Takegoshi 1996 is unavailable, Tsuo et al 1998 state "about 250 kWh/kg" number with no citation.  Therefore we will exclude Williams et al. 

# In[17]:


e_refineSi_siemens.loc[1996] = np.nan #removing Williams et al.


# In[18]:


plt.scatter(e_refineSi_siemens.index, e_refineSi_siemens.iloc[:,0])
plt.title('Electricity: Siemens Process')
plt.ylabel('[kWh/kg]')


# There is noise, but generally there is an observable downward trend. Rather than curve fitting and being wrong all the time, I will manually remove points that cause upward or downward jumps, and interpolate based on the remaining data points. This is not a perfect solution, but should provide a decent approximation to reality.

# In[19]:


e_refineSi_siemens_manual = e_refineSi_siemens.copy()
e_refineSi_siemens_manual.loc[1998] = np.nan #removing bumps
e_refineSi_siemens_manual.loc[2008] = np.nan #removing bumps
e_refineSi_siemens_manual.loc[2014] = np.nan #removing bumps
e_refineSi_siemens_manual.loc[2015] = np.nan #removing bumps

e_refineSi_siemens_manual=e_refineSi_siemens_manual.interpolate()

plt.plot(e_refineSi_siemens_manual.index, e_refineSi_siemens_manual.iloc[:,0])
plt.scatter(e_refineSi_siemens.index, e_refineSi_siemens.iloc[:,0], marker='^', color='black')

plt.title('Electricity: Siemens Process')
plt.ylabel('[kWh/kg]')
plt.xlim(1989,2021)


# ### FBR

# In[20]:


e_refineSi_fbr.dropna(how='all')


# ## Ingot growth
# 
# The next step in manufacturing silicon PV is ingot growth. There are two primary methods of ingot growth in the PV industry over it's history; multi-crystalline silicon and monocrystalline silicon. Initially, all PV was monocrystalline, then Multicrystalline silicon ingots were the dominent market share for most of a decade, and currently monocrystalline is making a resurgence to market dominence. We will cover the energy associated with both processes here, and weight the historical energy demand by the marketshare of these two technologies.

# In[21]:


e_ingotenergy_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-silicon-ingotgrowing.csv",
                                     index_col='year')


# ### Multi-crystalline Silicon
# 
# mc-Si is created through putting chunked polysilicon into a large block, heating and casting into a single large block. This process results in many crystallographic grains within the block, which slightly reduces the efficiency of the cell, but is cheap. 

# In[22]:


e_casting_raw = e_ingotenergy_raw.iloc[:,3:6]
e_casting_raw.dropna(how='all')


# In[23]:


plt.scatter(e_casting_raw.index, e_casting_raw['E_mcSiCast_kWhpkg'])


# The two high outliers are Fan et al and Woodhouse et al. Both of these datapoint include the wafering, which we prefer to calculate separately, therefore we will drop these two points, and use them later as a check that our energy demands are lining up.
# 
# Next the energy seems to step up and then down over time. This is potenially real due the increasing size of blocks over time.

# In[24]:


e_casting_manual = e_casting_raw.copy()
e_casting_manual.loc[2016] = np.nan #drop Fan et al
e_casting_manual.loc[2018] = np.nan # drop Woodhouse et al


# In[25]:


plt.scatter(e_casting_manual.index, e_casting_manual['E_mcSiCast_kWhpkg'])
plt.ylim(5,16)
plt.title('Electricity: DS of mc-Si')
plt.ylabel('Electricity Demand [kWh/kg]')


# From this lovely scatter plot graph, we can see that the energy demand of directional solification casting for mc-Si has not particularly changed in the last decades. Therefore, we will take an average of these datapoints and apply it for all time.

# In[26]:


e_casting_mcSi = e_casting_manual['E_mcSiCast_kWhpkg'].mean()
print('The electrical energy to make mc-Si through direct solidification is '+str(e_casting_mcSi)+' kWh/kg.')


# ### Mono-crystalline Silicon
# 
# mono-Si is created through the Czochralski process, in which a seed crystal is rotated and drawn away from a vat of molten silicon, growing a large boule. This results in the whole boule/ingot being oriented in one crystallographic direction, which increases the cell efficiency, but is time consuming and expensive.

# In[27]:


e_growczingot_raw = e_ingotenergy_raw.iloc[:,0:3]
e_growczingot_raw.dropna(how='all')


# In[28]:


plt.scatter(e_growczingot_raw.index, e_growczingot_raw['E_Cz_kWhpkg'])
plt.title('Electricity: Cz Ingot Growth')
plt.ylabel('[kWh/kg]')


# There is a general downward trend. There is a lot of noise at the end. The 2016 datapoint from Fan et al is much higher, as is Woodhouse et al 2018. Fan et al data is the average of Chinese manufacturers surveys and literature data. Both sources include the wafering step (Which we prefer to calculate separately). Therefore we will drop both datapoints for this calculation, but use them as a reality check later for energy demand of the two steps.
# 
# Knapp 1999 is lower than Jungbluth 2004. This is possible, but is a very small difference in overall energy demand (117 vs 123 kWh/kg). Therefore, we will take the average of the two points, and set both dates equal to that average.
# 
# Lastly, the final datapoint from Muller et al ticks upward slightly, however, the previous datapoint is from ITRPV which is a global survey report whereas the Muller et al is an updated LCI ostensibly with real world data. Therefore, we will leave this slight increase  given the data quality and non-drastic change.

# In[29]:


e_growczingot_manual = e_growczingot_raw.copy()
e_growczingot_manual.loc[2016] = np.nan #drop Fan et al
e_growczingot_manual.loc[2018] = np.nan # drop Woodhouse et al


# In[30]:


avg = np.mean([e_growczingot_manual.loc[1999,'E_Cz_kWhpkg'], e_growczingot_manual.loc[2004,'E_Cz_kWhpkg']])
e_growczingot_manual.loc[1999] = avg
e_growczingot_manual.loc[2004] = avg


# In[31]:


e_ingotcz_filled = e_growczingot_manual.interpolate()


# In[32]:


plt.plot(e_ingotcz_filled.index, e_ingotcz_filled['E_Cz_kWhpkg'])
plt.scatter(e_growczingot_raw.index, e_growczingot_raw['E_Cz_kWhpkg'], color='black')
plt.title('Electricity: Cz Ingot Growth')
plt.ylabel('[kWh/kg]')
plt.xlim(1993,2021)


# ### Market Share Weight mono-Si vs mc-Si
# Here we blend the two calculated data into an annual average energy demand based on the marketshare of installed cell type.

# In[33]:


pvice_mcSimono_marketshare = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/output_scaledmrktshr_mcSi_mono.csv",
                                     index_col='Year')


# In[34]:


e_ingotcz = e_ingotcz_filled.loc[1995:,['E_Cz_kWhpkg']] #slice Cz dataframe
e_ingots = e_ingotcz.copy() #create new df for math
e_ingots['E_DS_kWhpkg'] = e_casting_mcSi #add column for mcsi DS
pvice_mcSimono_marketshare_trim = pvice_mcSimono_marketshare.loc[1995:,] #trim the marketshare to start in 1995

e_ingots_wtd = pd.DataFrame(index=e_ingots.index) #create new df for math
e_ingots_wtd['mono'] = pvice_mcSimono_marketshare_trim['monoSi']*e_ingots['E_Cz_kWhpkg'] #mrktshr mono*CZ energy
e_ingots_wtd['mocsi'] = pvice_mcSimono_marketshare_trim['mcSi']*e_ingots['E_DS_kWhpkg'] #mrktshr mcSi*DS energy
e_ingots_wtd_final = e_ingots_wtd.sum(axis=1) # sum the annual energy demand PV Si ingot growth


# In[35]:


fig, ax1 = plt.subplots()

ax1.plot(e_ingots_wtd_final, label='Wtd Avg Electricity Demand')
ax1.scatter(e_growczingot_raw.index, e_growczingot_raw['E_Cz_kWhpkg'], color='black', label='CZ, mono-Si, raw data')
ax1.scatter(e_casting_raw.index, e_casting_raw['E_mcSiCast_kWhpkg'], color='green', 
            marker='^', label='DS, mc-Si, raw data')
ax1.set_ylabel('Electricity Demand [kWh/kg]')

ax2 = ax1.twinx()
ax2.plot(pvice_mcSimono_marketshare_trim['monoSi'], color ='orange', label='Mono Si Market Share', ls=':', lw=3)
ax2.set_ylim(0,1.0)
plt.ylabel('Market Share Monocrystalline Si [%]', color='orange')
ax2.tick_params(axis='y', color='red', labelcolor='orange')

plt.xlim(1989,2030)
plt.title('Electricity: Weighted Average of Si Ingot Growth')

ax1.legend(loc='upper center')
plt.show()


# ## Wafering Electricity
# 
# This step captures the electricity demands of wafering the grown silicon ingot (CZ or DS) into wafers. This includes the prep and demounting as well as the sawing step itself.

# In[13]:


e_wafering_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/energy-input-silicon-wafering.csv",
                             index_col='year')


# In[14]:


e_wafering_raw.dropna(how='all')


# In[15]:


plt.scatter(e_wafering_raw.index, e_wafering_raw['E_Wafering_kWhpkg']) 


# In[74]:


e_wafering_trim = e_wafering_raw.loc[1995:].dropna(how='all') #remove pre 1995 data .loc[1995:,['E_Cz_kWhpkg']]
e_wafering_trim_drop=e_wafering_trim['E_Wafering_kWhpkg']
e_wafering_trim_drop.loc[1997] = np.nan # this is an outlier


# In[78]:


e_wafering_filled = e_wafering_trim_drop.interpolate()

plt.plot(e_wafering_filled, label='interpolated')
plt.scatter(e_wafering_raw.index, e_wafering_raw['E_Wafering_kWhpkg'], label='raw', color='black') 
plt.title('Electricity demand: Wafering')
plt.ylabel('[kWh/kg]')


# ## Cell Production Electricity

# In[ ]:





# ## Combine All MFG energy
# 
# For the energy baseline to match up with the mass baseline, we are separating the energy demands into virgin material, transport, and manufacturing energy. This journal covers the Manufacturing energy, batch processing through forming and cutting. The following calculation sum all the energies associate with manufacturing at the flat glass facility.
# 
# To track the use of methane/natural gas in the processing, we will do a weighted average percent fuel column to accompany the total energy value.

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


.to_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/output_energy_silicon.csv")

