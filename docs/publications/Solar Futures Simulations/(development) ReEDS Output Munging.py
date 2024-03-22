#!/usr/bin/env python
# coding: utf-8

# # ReEDS Scenarios on PV ICE Tool

# <div class="alert alert-block alert-danger">
# <b>Journal Not Finished:</b> The below journal was made to avoid doing pre-analysis in the excel for the baseline creation (the excel has a tab where we multiplied by the DC:AC factors [1.1,1.3,1.3] for the ['distpv','dupv','upv'] and the added them for using in the Solar Futures analysis. However this journal is not finished (I marked where I stopped), and it saves the PCA data incorrectly (every 2 years). Leaving in case it becomes useful at some point in life.
# </div>
# 
# 
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

# In[3]:


#We need to come up with a default location to save ReEDS output files
#reedsFile = str(Path().resolve().parent.parent.parent.parent / 'December Core Scenarios ReEDS Outputs Solar Futures v3a.xlsx')
#print ("Input file is stored in %s" % reedsFile)
reedsFile = str(Path().resolve().parent.parent.parent/ 'PV_ICE' / 'baselines' / 'SupportingMaterial' / '100REby2035-cumulative.csv')
print ("Input file is stored in %s" % reedsFile)


# In[4]:


REEDSInput = pd.read_csv(reedsFile)
REEDSInput.head


# ### Aggregate down to simple MW Installed input

# In[5]:


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

# In[6]:


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

# In[7]:


df_annualAdds_evens = df_addedCap_evens/2
print(df_annualAdds_evens)


# ### Create the odd years

# In[8]:


#Now create the odd years by duplicating the even years and changing the index
df_odds = df_annualAdds_evens.copy()
df_odds.index = df_odds.index-1 #set the index = one year less
print(df_odds)


# In[9]:


#put the evens and odds together, sort by year
df_allyrs = pd.concat([df_annualAdds_evens, df_odds])
df_allyrs.sort_index(axis=0, inplace=True)
#df_allyrs_byscen = df_allyrs.unstack(level=0)
#print(df_allyrs_byscen)

#modify by DC:AC ratio(1.2 avg) and 85% average marketshare of c-Si technology and convert to MW
df_cSi_installs = df_allyrs*1.2*0.85*1000
print(df_cSi_installs)


# In[10]:


#output the file
df_cSi_installs.to_csv('output_reeds4PVICE.csv', index=True)


# # Reading a ReEDS annual built capacity file
# This data file is the "annual built capacity", or the additions (not net additions) to the grid. This is an annual number reported biannually, so the assumption is that the previous odd year installed the same amount of PV capacity.

# In[11]:


reedsFile = str(Path().resolve().parent.parent.parent/ 'PV_ICE' / 'baselines' / 'SupportingMaterial' / '100REby2035-annuals.csv')
print ("Input file is stored in %s" % reedsFile)
REEDSInput = pd.read_csv(reedsFile)
REEDSInput.head


# In[12]:


rawdf = REEDSInput.copy()

#currently, we're ignoring region, so drop PCA
rawdf.drop(columns=['region'], inplace=True)

#aggregate and sum by scenarios and year to get an annual (bi-annual) installation by scenario
df = pd.DataFrame(rawdf.groupby(['tech', 'scenario', 'year'])['Capacity (GW)'].sum())
df.head


# Now we multiply each technology by it's respective DC:AC ratio, because distributed PV (i.e. rooftop) in ReEDS is reported in AC with a 1.1 DC:AC ratio. We install in DC, therefore, we multiply ReEDS output by 1.1. For both types of utility PV (Distributed UPV and UPV), the DC:AC ratio is 1.3.

# In[13]:


#create a litte dataframe of the factors with index that matches tech names
dc_ac = pd.DataFrame({'factor':[1.1,1.3,1.3]}, index=['distpv','dupv','upv'])
#multiply techs by DC:AC ratios
df_dc = df.mul(dc_ac['factor'], level=0, axis='index')
print(df_dc)


# Now we're in DC, we can sum the techs for each scenario and year.

# In[14]:


df_byscen = pd.DataFrame(df_dc.groupby(['scenario', 'year'])['Capacity (GW)'].sum())
df_evens_byscen = df_byscen.unstack(level='scenario')
#print(df_evens_byscen)


# This gives us the annual added capacity, by scenario, but only on even years. ReEDS recommendation is to back duplicate the installation, i.e. the same amount of PV is installed in 2049 and 2050. Now we create an odd year data set.

# In[15]:


#Now create the odd years by duplicating the even years and changing the index
df_odds = df_evens_byscen.copy()
df_odds.index = df_odds.index-1 #set the index = one year less
#print(df_odds)


# Now concatinate the two dataframes, and reorder by year number.

# In[16]:


#put the evens and odds together, sort by year
df_allyrs = pd.concat([df_evens_byscen, df_odds])
df_allyrs.sort_index(axis=0, inplace=True)
#print(df_allyrs)


# Finally, we only consider c-Si installations right now, and the historical average is 85% c-Si market share in the US (most of the rest is CdTe). Therefore, we multiply everything by 0.85 to account for only c-Si material.

# In[17]:


#multiply by 85% average marketshare of c-Si technology and convert to MW
df_cSi_installs = df_allyrs*0.85*1000
print(df_cSi_installs)


# In[18]:


#output the file
df_cSi_installs.to_csv('output_reeds4PVICE.csv', index=True)


# ## Save Input Files by PCA Region for Mapping

# In[19]:


rawdf2 = REEDSInput.copy()

#aggregate and sum by scenarios and year to get an annual (bi-annual) installation by scenario
df_byregion = pd.DataFrame(rawdf2.groupby(['tech', 'scenario', 'year', 'region'])['Capacity (GW)'].sum())
df_byregion.head


# Multiply the dataframe by the tech factors AC to DC ratio here so that it can be dropped and simplify the df

# In[21]:


#create a litte dataframe of the factors with index that matches tech names
dc_ac = pd.DataFrame({'factor':[1.1,1.3,1.3]}, index=['distpv','dupv','upv'])
#multiply techs by DC:AC ratios
df_byregion_dc = df_byregion.mul(dc_ac['factor'], level=0, axis='index')


# In[23]:


#now weight by c-si technology ~85% marketshare
c_si = pd.DataFrame({'factor':[1.0,0.85,0.85]}, index=['distpv','dupv','upv']) 
#distpv = residential, which is pretty much all c-Si, others are utility, so 85%
df_byregion_dc_si = df_byregion_dc.mul(c_si['factor'], level=0, axis='index')


# In[24]:


df_byregion_dc_si_mw = df_byregion_dc_si*1000 #reeds outputs are in GW, so changing to MW for PV ICE


# Now everything is c-Si in DC, can use groupby sum to combine the techs

# In[25]:


#after multiplying to get dc, sum the installs across techs, to simplify for PCA region analysis
df_dc_byregion = pd.DataFrame(df_byregion_dc_si_mw.groupby(['scenario', 'year', 'region'])['Capacity (GW)'].sum()) 
df_dc_byregion.rename(columns = {'Capacity (GW)':'new_Installed_Capacity_[MW]'}, inplace = True)
df_dc_byregion


# #### Loading Module Baseline. Will be used later to populate all the columsn otehr than 'new_Installed_Capacity_[MW]' which will be supplied by the REEDS model

# In[31]:


import PV_ICE
r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
#r1.createScenario(name='US', file=r'..\baselines\baseline_modules_US_100RE2050.csv')
r1.createScenario(name='US', massmodulefile=r'..\baselines\baseline_modules_mass_US.csv') # Don't need this one specifically 
baseline = r1.scenario['US'].dataIn_m
baseline.set_index('year', inplace=True)
history = pd.DataFrame(baseline['new_Installed_Capacity_[MW]'].loc[1995:2020]) #preserve historical installs
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]'])
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual
history


# In[36]:


r1.scenario['US'].dataIn_m.loc[2018:2023]


# Now join the pca region to the module file and create files by scenario and pca region

# In[37]:


df_odds = df_evens_byscen.copy()
df_odds.index = df_odds.index-1 #set the index = one year less
#put the evens and odds together, sort by year
df_allyrs = pd.concat([df_evens_byscen, df_odds])
df_allyrs.sort_index(axis=0, inplace=True)


# In[38]:


for scenarios in range(len(df_dc_byregion.index.levels[0])): # iterate over the scenarios (3 scenarios)
    scenario_name = df_dc_byregion.index.levels[0][scenarios] #assigns the current scenario name to a variable
    for pcas in range(len(df_dc_byregion.index.levels[2])): #iterate over pca regions (134 pca regions)
        pca = df_dc_byregion.index.levels[2][pcas] #assigns current pca name to a variable
        filetitle = scenario_name+'_'+pca +'.csv'
        subtestfolder = os.path.join(testfolder, 'ColePCAs')
        if not os.path.exists(subtestfolder):
            os.makedirs(subtestfolder)
        filetitle = os.path.join(subtestfolder, filetitle) #these lines create a folder and file naming structure
        
        B = df_dc_byregion.xs(scenario_name,level='scenario') #takes cross section by the scenario name
        A = B.xs(pca,level='region') #takes cross section by the pca region
        A.name = 'new_Installed_Capacity_[MW]' #makes sure the name is right for pv ice
        A = pd.DataFrame(A)
        A.index=pd.PeriodIndex(A.index, freq='A')
        A = pd.DataFrame(A)
        # Add other columns
        A = pd.concat([A.reindex(baseline.index), baseline], axis=1)
        A.update(history) #not working yet
        #A.replace((['new_Installed_Capacity_[MW]'][1995:2020]), history, inplace=True)
        
        header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,"    "mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,"    "mod_Repair,mod_MerchantTail,mod_Reuse\n"    "year,MW,%,years,years,%,years,%,%,%,%,%,%\n"

        with open(filetitle, 'w', newline='') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
            for line in header:
                ict.write(line)

        #    savedata.to_csv(ict, index=False)
            A.to_csv(ict, header=False)
        


# ## UPDATED UNTIL HERE on Nov 29, 2022
# 
# 
# # Save Input Files By States

# #### Reassign data from REEDS Input, as we need one of the columns we dropped.

# In[41]:


REEDSInput


# In[40]:


rawdf = REEDSInput.copy()
#rawdf.drop(columns=['State'], inplace=True)
rawdf.drop(columns=['Tech'], inplace=True)
rawdf.set_index(['Scenario','Year','PCA', 'State'], inplace=True)
rawdf.head(21)


# #### Group data so we can work with the States instead

# In[ ]:


#df = rawdf.groupby(['Scenario','State', 'Year'])['Capacity (GW)'].sum(axis=0)
df = rawdf.groupby(['Scenario','State', 'Year'])['Capacity (GW)'].sum()
df = pd.DataFrame(df)
df.head()


# #### For each Scenario and for each STATE, combine with baseline and save as input file

# In[ ]:


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

# In[ ]:


rawdf = REEDSInput.copy()
#rawdf.drop(columns=['State'], inplace=True)
rawdf.drop(columns=['Tech'], inplace=True)
rawdf.set_index(['Scenario','Year'], inplace=True)
rawdf.head(21)


# In[ ]:


#df = rawdf.groupby(['Scenario','Year'])['Capacity (GW)'].sum(axis=0)
df = rawdf.groupby(['Scenario','Year'])['Capacity (GW)'].sum()


# ### Loading Module Baseline. Will be used later to populate all the columsn other than 'new_Installed_Capacity_[MW]' which will be supplied by the REEDS model

# In[ ]:


import PV_ICE
r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='US', file=r'..\baselines\SolarFutures_2021\baseline_modules_US_Reeds.csv')
baseline = r1.scenario['US'].data
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]'])
baseline.set_index('year', inplace=True)
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual
baseline.head()


# ### For each Scenario, combine with baseline and save as input file¶

# In[ ]:


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




