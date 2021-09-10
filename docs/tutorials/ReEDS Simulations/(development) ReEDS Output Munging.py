#!/usr/bin/env python
# coding: utf-8

# # ReEDS Scenarios on PV ICE Tool

# To explore different scenarios for furture installation projections of PV (or any technology), ReEDS output data can be useful in providing standard scenarios. ReEDS installation projections are used in this journal as input data to the PV ICE tool. 
# 
# Current sections include:
# 
# <ol>
#     <li> ### Reading a cumulative capacity ReEDS output file </li>
#     <li> ### Reading an annual built ReEDS output file </li>
#     <li> ### Saving PCA data as PV ICE input format </li>
#     <li> ### Saving State data as PV ICE input format </li>
# </ol>
# 

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

testfolder = str(Path().resolve().parent.parent.parent / 'PV_ICE' / 'TEMP')

print ("Your simulation will be stored in %s" % testfolder)


# # Reading a ReEDS cumulative capacity output file
# This reEDS output file is the cumulative capacity every other year. To get GW/yr installed, we need to take the difference between the years, then divide by 2. This is less accurate than getting an "annual built" data file because the cumulative capacity accounts for 30 year lifetime removal from field (default ReEDS assumption). This munging also neglects PCA region.

# In[77]:


#We need to come up with a default location to save ReEDS output files
#reedsFile = str(Path().resolve().parent.parent.parent.parent / 'December Core Scenarios ReEDS Outputs Solar Futures v3a.xlsx')
#print ("Input file is stored in %s" % reedsFile)
reedsFile = str(Path().resolve().parent.parent.parent/ 'PV_ICE' / 'baselines' / 'SupportingMaterial' / '100REby2035-cumulative.csv')
print ("Input file is stored in %s" % reedsFile)


# In[78]:


REEDSInput = pd.read_csv(reedsFile)
REEDSInput.head


# ### Aggregate down to simple MW Installed input

# In[79]:


rawdf = REEDSInput.copy()

#currently, we're ignoring region, so drop PCA
rawdf.drop(columns=['PCA'], inplace=True)

#aggregate and sum by scenarios and year to get an annual (bi-annual) installation by scenario
df = rawdf.groupby(['scenario', 'year'])['Capacity (GW)'].sum()
df_evens = pd.DataFrame(df)
df_evens_byscen = df.unstack(level='scenario')#this df contains all the scenarios, even years only
print(df_evens_byscen)


# ### Take the difference and Divide by 2
# The file provided is cumulative installs, therefore we need to take the difference between years

# In[80]:


#take the difference between years to get the annual installs (not cumulative)
#grab scenario names
SCEN = df_evens.index.levels[0]
#len(SCEN)
#create a for loop to iterate through all the provided scenarios
for i in range(len(SCEN)):
    df_evens_byscen[SCEN[i]+'_added_cap(GW)'] = df[SCEN[i]].diff() #takes diff between rows and creates new column
#print(df_evens_byscen)
df_addedCap_evens = df_evens_byscen.filter(regex = 'added_cap') #create df of just added capacity, removes multiIndex
print(df_addedCap_evens)


# Because we prefer to use real world data whereever possible, anything prior to the current year will use real world installs. Therefore, we can ignore the NaN values in 2010.
# 
# Now we divide this added installations in half.

# In[81]:


df_annualAdds_evens = df_addedCap_evens/2
print(df_annualAdds_evens)


# ### Create the odd years

# In[82]:


#Now create the odd years by duplicating the even years and changing the index
df_odds = df_annualAdds_evens.copy()
df_odds.index = df_odds.index-1 #set the index = one year less
print(df_odds)


# In[83]:


#put the evens and odds together, sort by year
df_allyrs = pd.concat([df_annualAdds_evens, df_odds])
df_allyrs.sort_index(axis=0, inplace=True)
#df_allyrs_byscen = df_allyrs.unstack(level=0)
#print(df_allyrs_byscen)

#modify by DC:AC ratio(1.2 avg) and 85% average marketshare of c-Si technology and convert to MW
df_cSi_installs = df_allyrs*1.2*0.85*1000
print(df_cSi_installs)


# In[84]:


#output the file
df_cSi_installs.to_csv('output_reeds4PVICE.csv', index=True)


# # Reading a ReEDS annual built capacity file
# This data file is the "annual built capacity", or the additions (not net additions) to the grid. This is an annual number reported biannually, so the assumption is that the previous odd year installed the same amount of PV capacity.

# In[5]:


reedsFile = str(Path().resolve().parent.parent.parent/ 'PV_ICE' / 'baselines' / 'SupportingMaterial' / '100REby2035-annuals.csv')
print ("Input file is stored in %s" % reedsFile)
REEDSInput = pd.read_csv(reedsFile)
REEDSInput.head


# In[39]:


rawdf = REEDSInput.copy()

#currently, we're ignoring region, so drop PCA
rawdf.drop(columns=['region'], inplace=True)

#aggregate and sum by scenarios and year to get an annual (bi-annual) installation by scenario
df = pd.DataFrame(rawdf.groupby(['tech', 'scenario', 'year'])['Capacity (GW)'].sum())
df.head


# Now we multiply each technology by it's respective DC:AC ratio, because distributed PV (i.e. rooftop) in ReEDS is reported in AC with a 1.1 DC:AC ratio. We install in DC, therefore, we multiply ReEDS output by 1.1. For both types of utility PV (Distributed UPV and UPV), the DC:AC ratio is 1.3.

# In[43]:


#create a litte dataframe of the factors with index that matches tech names
dc_ac = pd.DataFrame({'factor':[1.1,1.3,1.3]}, index=['distpv','dupv','upv'])
#multiply techs by DC:AC ratios
df_dc = df.mul(dc_ac['factor'], level=0, axis='index')
print(df_dc)


# Now we're in DC, we can sum the techs for each scenario and year.

# In[52]:


df_byscen = pd.DataFrame(df_dc.groupby(['scenario', 'year'])['Capacity (GW)'].sum())
df_evens_byscen = df_byscen.unstack(level='scenario')
#print(df_evens_byscen)


# This gives us the annual added capacity, by scenario, but only on even years. ReEDS recommendation is to back duplicate the installation, i.e. the same amount of PV is installed in 2049 and 2050. Now we create an odd year data set.

# In[53]:


#Now create the odd years by duplicating the even years and changing the index
df_odds = df_evens_byscen.copy()
df_odds.index = df_odds.index-1 #set the index = one year less
#print(df_odds)


# Now concatinate the two dataframes, and reorder by year number.

# In[50]:


#put the evens and odds together, sort by year
df_allyrs = pd.concat([df_evens_byscen, df_odds])
df_allyrs.sort_index(axis=0, inplace=True)
#print(df_allyrs)


# Finally, we only consider c-Si installations right now, and the historical average is 85% c-Si market share in the US (most of the rest is CdTe). Therefore, we multiply everything by 0.85 to account for only c-Si material.

# In[54]:


#multiply by 85% average marketshare of c-Si technology and convert to MW
df_cSi_installs = df_allyrs*0.85*1000
print(df_cSi_installs)


# In[55]:


#output the file
df_cSi_installs.to_csv('output_reeds4PVICE.csv', index=True)


# # Append to Projections Options File

# In[ ]:





# In[ ]:





# ## Save Input Files by PCA

# #### Create a copy of the REEDS Input and modify structure for PCA focus

# #### Loading Module Baseline. Will be used later to populate all the columsn otehr than 'new_Installed_Capacity_[MW]' which will be supplied by the REEDS model

# In[6]:


import PV_ICE
r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='US', file=r'..\baselines\SolarFutures_2021\baseline_modules_US_Reeds.csv')
baseline = r1.scenario['US'].data
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]'])
baseline.set_index('year', inplace=True)
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual
baseline.head()


# #### For each Scenario and for each PCA, combine with baseline and save as input file

# In[8]:


for ii in range (len(rawdf.unstack(level=1))):
    PCA = rawdf.unstack(level=1).iloc[ii].name[1]
    SCEN = rawdf.unstack(level=1).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = SCEN+'_'+PCA +'.csv'
    subtestfolder = os.path.join(testfolder, 'PCAs')
    if not os.path.exists(subtestfolder):
        os.makedirs(subtestfolder)
    filetitle = os.path.join(subtestfolder, filetitle)
    A = rawdf.unstack(level=1).iloc[ii]
    A = A.droplevel(level=0)
    A.name = 'new_Installed_Capacity_[MW]'
    A = pd.DataFrame(A)
    A.index=pd.PeriodIndex(A.index, freq='A')
    A = pd.DataFrame(A)
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 0.85
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 1000   # ReEDS file is in GW.
    # Add other columns
    A = pd.concat([A, baseline.reindex(A.index)], axis=1)
   
    header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,"    "mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,"    "mod_Repair,mod_MerchantTail,mod_Reuse\n"    "year,MW,%,years,years,%,years,%,%,%,%,%,%\n"

    with open(filetitle, 'w', newline='') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
        for line in header:
            ict.write(line)

        #    savedata.to_csv(ict, index=False)
        A.to_csv(ict, header=False)


# In[ ]:





# ## Save Input Files By States

# #### Reassign data from REEDS Input, as we need one of the columns we dropped.

# In[9]:


rawdf = REEDSInput.copy()
#rawdf.drop(columns=['State'], inplace=True)
rawdf.drop(columns=['Tech'], inplace=True)
rawdf.set_index(['Scenario','Year','PCA', 'State'], inplace=True)
rawdf.head(21)


# #### Group data so we can work with the States instead

# In[10]:


#df = rawdf.groupby(['Scenario','State', 'Year'])['Capacity (GW)'].sum(axis=0)
df = rawdf.groupby(['Scenario','State', 'Year'])['Capacity (GW)'].sum()
df = pd.DataFrame(df)
df.head()


# #### For each Scenario and for each STATE, combine with baseline and save as input file

# In[11]:


for ii in range (len(df.unstack(level=2))):   
    STATE = df.unstack(level=2).iloc[ii].name[1]
    SCEN = df.unstack(level=2).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = SCEN+'_'+STATE +'.csv'
    
    subtestfolder = os.path.join(testfolder, 'STATEs')
    if not os.path.exists(subtestfolder):
        os.makedirs(subtestfolder)
    filetitle = os.path.join(subtestfolder, filetitle)

    A = df.unstack(level=2).iloc[ii]
    A = A.droplevel(level=0)
    A.name = 'new_Installed_Capacity_[MW]'
    A = pd.DataFrame(A)
    A.index=pd.PeriodIndex(A.index, freq='A')
    A = pd.DataFrame(A)
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 0.85 # marketshares['Si']
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 1000   # ReEDS file is in GW.
    # Add other columns
    A = pd.concat([A, baseline.reindex(A.index)], axis=1)
    
    
    header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,"    "mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,"    "mod_Repair,mod_MerchantTail,mod_Reuse\n"    "year,MW,%,years,years,%,years,%,%,%,%,%,%\n"

    with open(filetitle, 'w', newline='') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
        for line in header:
            ict.write(line)

        #    savedata.to_csv(ict, index=False)
        A.to_csv(ict, header=False)


# # Saving US Baseline

# ### Create a copy of the REEDS Input and modify structure for PCA focus

# In[12]:


rawdf = REEDSInput.copy()
#rawdf.drop(columns=['State'], inplace=True)
rawdf.drop(columns=['Tech'], inplace=True)
rawdf.set_index(['Scenario','Year'], inplace=True)
rawdf.head(21)


# In[13]:


#df = rawdf.groupby(['Scenario','Year'])['Capacity (GW)'].sum(axis=0)
df = rawdf.groupby(['Scenario','Year'])['Capacity (GW)'].sum()


# ### Loading Module Baseline. Will be used later to populate all the columsn other than 'new_Installed_Capacity_[MW]' which will be supplied by the REEDS model

# In[14]:


import PV_ICE
r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='US', file=r'..\baselines\SolarFutures_2021\baseline_modules_US_Reeds.csv')
baseline = r1.scenario['US'].data
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]'])
baseline.set_index('year', inplace=True)
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual
baseline.head()


# ### For each Scenario, combine with baseline and save as input file¶

# In[15]:


for ii in range (len(df.unstack(level=1))):
    SCEN = df.unstack(level=1).index[ii]
    SCEN=SCEN.replace('+', '_')
    filetitle = SCEN+'.csv'
    
    subtestfolder = os.path.join(testfolder, 'USA')
    if not os.path.exists(subtestfolder):
        os.makedirs(subtestfolder)
    filetitle = os.path.join(subtestfolder, filetitle)
    
    A = df.unstack(level=1).iloc[ii]

    A.name = 'new_Installed_Capacity_[MW]'
    A = pd.DataFrame(A)
    A.index=pd.PeriodIndex(A.index, freq='A')
    A = pd.DataFrame(A)
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 0.85 # marketshares['Si']
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 1000   # ReEDS file is in GW.
    # Add other columns
    A = pd.concat([A, baseline.reindex(A.index)], axis=1)
   
    header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,"    "mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,"    "mod_Repair,mod_MerchantTail,mod_Reuse\n"    "year,MW,%,years,years,%,years,%,%,%,%,%,%\n"

    with open(filetitle, 'w', newline='') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
        for line in header:
            ict.write(line)

        #    savedata.to_csv(ict, index=False)
        A.to_csv(ict, header=False)


# In[ ]:





# In[ ]:



