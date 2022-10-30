#!/usr/bin/env python
# coding: utf-8

# # Analysis of Cell Technology
# 3 competing cell technologies may claim marketshare in future; Bifacial PERC, bifacial SHJ, and Bifacial TOPCon. Each design has different efficiency and a different silver intensity. This analysis seeks compare these technologies on a mass and energy basis. A psuedo global deployment projection hitting 100% RE targets in 2050 is used so that silver demand can be evaluated at the global level.
# 
# Make 4+ scenarios
# 1. All PERC
# 2. All SHJ
# 3. All TOPCon
# 4. Realistic blend / ITRPV numbers from Martin Springer or Jarett Zuboy – DURAMat tech scounting report
# 5. All of the above and turn Bifacial ON/OFF
# 
# We will use the silver intensity and module efficiency projections from:
# 
#     Zhang, Yuchao, Moonyong Kim, Li Wang, Pierre Verlinden, and Brett Hallam. 2021. “Design Considerations for Multi-Terawatt Scale Manufacturing of Existing and Future Photovoltaic Technologies: Challenges and Opportunities Related to Silver, Indium and Bismuth Consumption.” Energy & Environmental Science. https://doi.org/10.1039/D1EE01814K. 
# 
# and
# 
#     Gervais, Estelle, Shivenes Shammugam, Lorenz Friedrich, and Thomas Schlegl. 2021. “Raw Material Needs for the Large-Scale Deployment of Photovoltaics – Effects of Innovation-Driven Roadmaps on Material Constraints until 2050.” Renewable and Sustainable Energy Reviews 137 (March): 110589. https://doi.org/10.1016/j.rser.2020.110589.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt

cwd = os.getcwd() #grabs current working directory

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'CellTechCompare')
inputfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')
baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')

if not os.path.exists(testfolder):
    os.makedirs(testfolder)


# # Data Preparation
# Bring in the data from Zhang et al 2021 and Gervais et al 2021.

# In[2]:


lit_celltech = pd.read_excel(os.path.join(supportMatfolder,'CellTechCompare','PERCvSHJvTOPCon-LitData.xlsx'), sheet_name='Sheet2',
                             header=[0,1,2], index_col=0)


# In[3]:


lit_celltech.columns.get_level_values


# In[4]:


#Zhang et al Table 2 gives cell size assumptions 166mm cells
cell_size_m2 = np.square(0.166)


# In[5]:


#calculate silver use per meter squared for each tech
zhang_perc_Ag_kgpm2 = lit_celltech['Zhang et al 2021 (hallam)']['PERC']['Ag_mgpcell']/1000/cell_size_m2 #creates series
zhang_shj_Ag_kgpm2 = lit_celltech['Zhang et al 2021 (hallam)']['SHJ']['Ag_mgpcell']/1000/cell_size_m2
zhang_topcon_Ag_kgpm2 = lit_celltech['Zhang et al 2021 (hallam)']['TOPCon']['Ag_mgpcell']/1000/cell_size_m2


# Gervais et al 2021 also project silver use, but through 2050. We wil use Zhang et al silver intensity through 2030, then a futher decrease from Gervais et al to 2050. There is no projection of TOPCon from Gervais et al, so we will assume a similar magnitude of continued decrease.

# In[6]:


lit_celltech.loc[2030]


# In[7]:


Gervais_perc_2050 = pd.Series({2050:40}) #mg/cell
Gervais_shj_2050 = pd.Series({2050:80}) #mg/cell
guess_topcon_2050 = pd.Series({2050:(95-18)}) # mg/cell 99-80 = 19, 57-40 = 17, guess further 18mg decrease
#assuming the same cell size as Zhang et al (it isn't specified in Gervais)
Gervais_perc_2050_kgpm2 = Gervais_perc_2050/1000/cell_size_m2
Gervais_shj_2050_kgpm2 = Gervais_shj_2050/1000/cell_size_m2
guess_topcon_2050_kgpm2 = guess_topcon_2050/1000/cell_size_m2


# In[8]:


perc_Ag_kgpm2 = pd.concat([zhang_perc_Ag_kgpm2.loc[:2049], Gervais_perc_2050_kgpm2])
shj_Ag_kgpm2 = pd.concat([zhang_shj_Ag_kgpm2.loc[:2049], Gervais_shj_2050_kgpm2])
topcon_Ag_kgpm2 = pd.concat([zhang_topcon_Ag_kgpm2.loc[:2049], guess_topcon_2050_kgpm2])


# In[9]:


#filled projections 2020 through 2050
perc_Ag_kgpm2.interpolate(inplace=True)
shj_Ag_kgpm2.interpolate(inplace=True)
topcon_Ag_kgpm2.interpolate(inplace=True)


# Now lets use Zhang et al's projections of efficiency increases. These are reasonably ambitious, achieving ~25% by 2030, but PV is usually an overachiever. We will hold efficiency constant after 2030.

# In[10]:


zhang_perc_modeff = lit_celltech['Zhang et al 2021 (hallam)']['PERC']['ModuleEff']
zhang_shj_modeff = lit_celltech['Zhang et al 2021 (hallam)']['SHJ']['ModuleEff']
zhang_topcon_modeff = lit_celltech['Zhang et al 2021 (hallam)']['TOPCon']['ModuleEff']


# In[11]:


zhang_perc_modeff.interpolate(inplace=True)
zhang_shj_modeff.interpolate(inplace=True)
zhang_topcon_modeff.interpolate(inplace=True)


# In[12]:


modeffs = pd.concat([zhang_perc_modeff,zhang_shj_modeff,zhang_topcon_modeff], axis=1)
modeffs.columns=['PERC','SHJ','TOPCon']
Aguse = pd.concat([perc_Ag_kgpm2,shj_Ag_kgpm2,topcon_Ag_kgpm2], axis=1)
Aguse.columns=['PERC','SHJ','TOPCon']


# In[13]:


plt.plot(modeffs.index, modeffs['PERC'], color='#0079C2')
plt.plot(modeffs.index, modeffs['SHJ'], color='#F7A11A', ls='--')
plt.plot(modeffs.index, modeffs['TOPCon'], color='#5D9732', ls='-.')

plt.legend(modeffs.columns)
plt.title('Module Efficiency over Time')
plt.ylabel('Module Efficiency [%]')


# In[14]:


plt.plot(Aguse.index, Aguse['PERC'], color='#0079C2')
plt.plot(Aguse.index, Aguse['SHJ'], color='#F7A11A', ls='--')
plt.plot(Aguse.index, Aguse['TOPCon'], color='#5D9732', ls='-.')
plt.legend(Aguse.columns)
plt.title('Silver Use over time')
plt.ylabel('Silver Intensity [kg/m2]')


# One important aspect of these technologies is bifaciality. Each has a different bifaciality factor, and they are not expected to increase substantially with time (ITRPV 2022). We plan to explore monofacial and bifacial modules of these technologies (for example residential vs utility). We will use a static inventory of bifacial factors.

# In[15]:


bifiFactors = {'PERC':0.7,
              'SHJ':0.9,
              'TOPCon':0.8} # ITRPV 2022, Fig. 58


# In[16]:


#PV ICE currently set up to read in a csv of bifi factors, so generate files to read in 
idx_temp = Aguse.index
df_temp = pd.DataFrame(index=idx_temp, columns=['bifi'], dtype=float)
bifi_perc = df_temp.copy()
bifi_perc['bifi'] = bifiFactors['PERC']
bifi_shj = df_temp.copy()
bifi_shj['bifi'] = bifiFactors['SHJ']
bifi_topcon = df_temp.copy()
bifi_topcon['bifi'] = bifiFactors['TOPCon']


# In[17]:


bifi_perc.to_csv(path_or_buf=os.path.join(testfolder,'bifi_perc.csv'), index_label='Year')
bifi_shj.to_csv(path_or_buf=os.path.join(testfolder,'bifi_shj.csv'), index_label='Year')
bifi_topcon.to_csv(path_or_buf=os.path.join(testfolder,'bifi_topcon.csv'), index_label='Year')


# In[18]:


bifi_perc_path = os.path.join(testfolder,'bifi_perc.csv')
bifi_shj_path = os.path.join(testfolder,'bifi_shj.csv')
bifi_topcon_path = os.path.join(testfolder,'bifi_topcon.csv')


# To create a blended scenario, we will use the ITRPV 2022 cell market share projection through 2030, and then keep it constant through 2050.

# In[19]:


#insert data from Jarett here
itrpv_celltech_marketshare = pd.read_csv(os.path.join(supportMatfolder,'CellTechCompare','ITRPV_celltech_marketshare.csv'), index_col=0)


# In[20]:


itrpv_celltech_marketshare.columns
#there are more cell techs here than I need - I'm not currently concerned with n-type vs p-type
#the marketshares of "n-type back contact", "n-type other", "tandem si-based" are small and outside scope of study
#remove and renormalize.


# In[21]:


#subset for desired techs
celltech_marketshare_sub_raw = itrpv_celltech_marketshare.loc[2020:].filter(regex=('PERC|TOPCon|SHJ')) 
#interpolate to fill gaps
celltech_marketshare_sub_raw.interpolate(inplace=True, limit_direction='both')
#renormalize
celltech_marketshare_sub_raw['temp_sum'] = celltech_marketshare_sub_raw.iloc[:,[0,1,2,3]].sum(axis=1)
celltech_marketshare_sub_raw['scale'] = 1/celltech_marketshare_sub_raw['temp_sum'] #create scaling factor
celltech_marketshare_scaled = celltech_marketshare_sub_raw.iloc[:,[0,1,2,3]]*celltech_marketshare_sub_raw.loc[:,['scale']].values
#celltech_marketshare_scaled.sum(axis=1) # test check that everything adds to 1


# In[22]:


celltech_marketshare_scaled.columns


# In[23]:


plt.plot([],[],color='blue', label='PERC')
plt.plot([],[],color='orange', label='TOPCon (p-type)')
plt.plot([],[],color='red', label='TOPCon (n-type)')
plt.plot([],[],color='purple', label='SHJ')
#plt.plot([],[],color='red', label='Cell')

plt.stackplot(celltech_marketshare_scaled.index,
              celltech_marketshare_scaled['p-type (PERC)'],
              celltech_marketshare_scaled['p-type (TOPCon)'],
              celltech_marketshare_scaled['n-type (TOPCon)'],
              celltech_marketshare_scaled['n-type (SHJ)'],
              colors = ['blue','orange','red','purple'])

plt.title('Market Share Cell Type: Blended Projection')
plt.ylabel('Market Share [fraction]')
#plt.xlim(1995,2022)
plt.legend(loc='lower center')
plt.show()


# In[24]:


celltech_marketshare_scaled['TOPCon'] = celltech_marketshare_scaled.filter(like='TOPCon').sum(axis=1)


# Other Assumptions:
# - silicon wafer thickness is identical, and improvements are identical
# - glass-glass module package for bifacial using 2.5mm glass for both
# - module manufacturing energy is identical (until we get better data)
# - degradation rates between the technologies are identical (until we get better data)
# - Weibull Failure probabilities are identical between technologies (until we get better data)
# - No ciruclarity

# In[25]:


#glass-glass package mass per area calculation
#ITRPV 2022 Figs 36 and 38, we are assuming that the front and back glass heave equal thickness of 2.5mm
density_glass = 2500*1000 # g/m^3 
glassperm2 = (2.5/1000)* 2 * density_glass
print('The mass per module area of glass is '+str(glassperm2)+' g/m^2')


# Pull in deployment projection. This deployment is based on the Solar Futures report, but has been modified to be more reasonable annual deployment schedule (i.e. manufacturing ramps up). However, this does not achieve 95% RE by 2035, but it does achieve 100% RE in 2050.

# In[26]:


sf_reeds_alts = pd.read_excel(os.path.join(supportMatfolder,'SF_reeds_alternates.xlsx'),index_col=0)


# In[27]:


sf_reeds = sf_reeds_alts.loc[2023:2050,['MW']]


# In[28]:


#try sorting the Reeds Deployment to be in ascending order
sf_reeds['MW'].values.sort() #this sorts the column values in place


# In[29]:


sf_reeds['TW_cum'] = sf_reeds['MW'].cumsum()/1e6


# In[30]:


fig, ax1 = plt.subplots()

ax1.plot(sf_reeds['MW'])
ax1.set_ylabel('Annual Deployments [MW]', color='blue')

ax2 = ax1.twinx()
ax2.plot(sf_reeds['TW_cum'], color='orange')
ax2.set_ylabel('Cumulative Capacity [TW]', color='orange')

plt.legend(['Cumulative Capacity'])
plt.show()


# In[31]:


sf_reeds.loc[2030]


# In[32]:


sf_reeds.loc[2050]


# In[33]:


#historical 2020-2022 from Wood Mac
history = sf_reeds_alts.loc[2020:2022,['Historically annual']]
history.columns=['MW']
projection = sf_reeds[['MW']]
newdeploymentcurve = pd.concat([history,projection],axis=0)


# In[34]:


#modify projection to be closer to global scale by x10
newdeploymentcurve_global = newdeploymentcurve*10


# In[35]:


newdeploymentcurve_global['TW_cum'] = newdeploymentcurve_global['MW'].cumsum()/1e6


# In[36]:


fig, ax1 = plt.subplots()

ax1.plot(newdeploymentcurve_global['MW']/1000)
ax1.set_ylabel('Annual Deployments [GW]', color='blue')

ax2 = ax1.twinx()
ax2.plot(newdeploymentcurve_global['TW_cum'], color='orange')
ax2.set_ylabel('Cumulative Capacity [TW]', color='orange')

plt.legend(['Cumulative Capacity'])
plt.show()


# # Scenario Creation

# In[37]:


#creating scenarios for identical power and identical area deployed
scennames = ['PERC_p','SHJ_p','TOPCon_p', 'PERC_a','SHJ_a','TOPCon_a'] #add later Blend and bifi on/off
MATERIALS = ['glass','silver','silicon'] #, 'copper', 'encapsulant', 'backsheet', 'aluminum_frames'
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[38]:


#load in a baseline and materials for modification
import PV_ICE

sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames:
    sim1.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim1.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# Modify the all one tech scenarios Scenarios:
# 
# Module level
# - trim to 2020-2050
# - no circularity
# - deployment projection
# - module eff
# 
# material level
# - glass per m2
# - silver per m2

# In[39]:


#trim to 2020-2050, this trims module and materials
sim1.trim_Years(startYear=2020)


# In[40]:


#no circularity
sim1.scenMod_noCircularity()


# In[41]:


#deployment projection
#NEED TO PULL IN DEPLOYMENT PROJECTION

for scen in scennames:
    sim1.scenario[scen].dataIn_m.loc[0:len(newdeploymentcurve.index-1),'new_Installed_Capacity_[MW]'] = newdeploymentcurve_global['MW'].values


# In[42]:


#module eff
#modeffs
for scen in scennames:
    sim1.scenario[scen].dataIn_m.loc[0:len(modeffs.index-1),'mod_eff'] = modeffs.filter(like=str(scen[0:3])).values


# In[43]:


#glass modify
for scen in scennames:
    sim1.scenario[scen].material['glass'].matdataIn_m['mat_massperm2'] = glassperm2


# In[44]:


#silver modify
#Aguse
for scen in scennames:
    sim1.scenario[scen].material['silver'].matdataIn_m.loc[0:len(Aguse.index-1),'mat_massperm2'] = Aguse.filter(like=str(scen[0:3])).values


# Check to make sure the modifications took.

# In[45]:


sim1.scenario['SHJ_a'].dataIn_m.head(10)


# In[46]:


sim1.scenario['SHJ_p'].material['silver'].matdataIn_m.head()


# # Run Simulations

# ## Option 1: Compare with Idential Power Installed

# In[47]:


scennames_p = ['PERC_p','SHJ_p','TOPCon_p']
bifipaths = [bifi_perc_path,bifi_shj_path,bifi_topcon_path]


# In[48]:


#option 1, install identical power
sim1.calculateFlows(scenarios='PERC_p', bifacialityfactors=bifi_perc_path)
sim1.calculateFlows(scenarios='SHJ_p', bifacialityfactors=bifi_shj_path)
sim1.calculateFlows(scenarios='TOPCon_p', bifacialityfactors=bifi_topcon_path)

perc_p_yearly, perc_p_cum = sim1.aggregateResults(scenarios='PERC_p')
shj_p_yearly, shj_p_cum = sim1.aggregateResults(scenarios='SHJ_p')
topcon_p_yearly, topcon_p_cum = sim1.aggregateResults(scenarios='TOPCon_p')


# ## Option 2: Compare with Idential Area Installed

# In[49]:


scennames_a = ['PERC_a','SHJ_a','TOPCon_a']
bifipaths = [bifi_perc_path,bifi_shj_path,bifi_topcon_path]


# In[50]:


#Calculate Area deployed based on PERC and modified SF projection above
idx_temp = Aguse.index #grab matching index
area_deploy = pd.DataFrame(index=idx_temp, dtype=float) #create an empty DF
area_deploy['Area'] = sim1.scenario['PERC_p'].dataOut_m['Area'].values
area_deploy.head()


# In[51]:


#option 1, install identical power
sim1.calculateFlows(scenarios='PERC_a', bifacialityfactors=bifi_perc_path, installByArea=list(area_deploy['Area']))
sim1.calculateFlows(scenarios='SHJ_a', bifacialityfactors=bifi_shj_path,  installByArea=list(area_deploy['Area']))
sim1.calculateFlows(scenarios='TOPCon_a', bifacialityfactors=bifi_topcon_path,  installByArea=list(area_deploy['Area']))

perc_a_yearly, perc_a_cum = sim1.aggregateResults(scenarios='PERC_a')
shj_a_yearly, shj_a_cum = sim1.aggregateResults(scenarios='SHJ_a')
topcon_a_yearly, topcon_a_cum = sim1.aggregateResults(scenarios='TOPCon_a')


# In[52]:


all_results_yearly, all_results_cum = sim1.aggregateResults()
all_results_yearly.columns


# ### Compare Effective Capacity

# In[53]:


activecapacity_yearly_TW = pd.DataFrame(all_results_yearly.filter(like='ActiveCapacity'))/1e6
activecapacity_yearly_TW_p = activecapacity_yearly_TW.filter(like='_p')
activecapacity_yearly_TW_a = activecapacity_yearly_TW.filter(like='_a')


# In[54]:


plt.plot(activecapacity_yearly_TW_p.index, activecapacity_yearly_TW_p.iloc[:,[0]], color='#0079C2')
plt.plot(activecapacity_yearly_TW_p.index, activecapacity_yearly_TW_p.iloc[:,[1]], color='#F7A11A', ls='--')
plt.plot(activecapacity_yearly_TW_p.index, activecapacity_yearly_TW_p.iloc[:,[2]], color='#5D9732', ls='-.')
plt.legend(scennames_p)
plt.title('Identical Installed Power: Effective Capacity')
plt.ylabel('Effective Capacity [TW]')


# In[55]:


plt.plot(activecapacity_yearly_TW_a.index, activecapacity_yearly_TW_a.iloc[:,[0]], color='#0079C2')
plt.plot(activecapacity_yearly_TW_a.index, activecapacity_yearly_TW_a.iloc[:,[1]], color='#F7A11A', ls='--')
plt.plot(activecapacity_yearly_TW_a.index, activecapacity_yearly_TW_a.iloc[:,[2]], color='#5D9732', ls='-.')
plt.legend(scennames_a)
plt.title('Identical Installed Area: Effective Capacity')
plt.ylabel('Effective Capacity [TW]')


# ### Compare Area Deployed

# In[56]:


#compile all energy out results
area_deployed=pd.DataFrame()
for scen in scennames:
    # add the scen name as a prefix for later filtering
    scen_area = sim1.scenario[scen].dataOut_m[['Cumulative_Active_Area']].add_prefix(str(scen+'_'))
    #concat into one large df
    area_deployed = pd.concat([area_deployed, scen_area], axis=1)

area_deployed.index = idx_temp
area_deployed.tail()


# In[57]:


plt.plot(area_deployed.index, area_deployed.iloc[:,[0]]/1e6, color='#0079C2')
plt.plot(area_deployed.index, area_deployed.iloc[:,[1]]/1e6, color='#F7A11A', ls='--')
plt.plot(area_deployed.index, area_deployed.iloc[:,[2]]/1e6, color='#5D9732', ls='-.')
plt.legend(scennames_p)
plt.title('Identical Installed Power: Cumulative Active Area')
plt.ylabel('Area [million m2]')


# In[58]:


plt.plot(area_deployed.index, area_deployed.iloc[:,[3]]/1e6, color='#0079C2')
plt.plot(area_deployed.index, area_deployed.iloc[:,[4]]/1e6, color='#F7A11A', ls='--')
plt.plot(area_deployed.index, area_deployed.iloc[:,[5]]/1e6, color='#5D9732', ls='-.')
plt.legend(scennames_a)
plt.title('Identical Installed Area: Cumulative Active Area')
plt.ylabel('Area [million m2]')


# ## Compare Silver Demand

# In[59]:


sim1.plotMaterialComparisonAcrossScenarios(keyword='mat_Virgin_Stock', material='silver')


# In[60]:


annual_demand_silver = all_results_yearly.filter(like='VirginStock_silver')
annual_demand_silver.columns=scennames
annual_demand_silver.to_csv(os.path.join(testfolder,'annual_demand_silver.csv'))


# In[61]:


silver_demand_cum = pd.DataFrame(all_results_cum.filter(like='VirginStock_silver').loc[2050]).T


# In[62]:


silver_demand_cum
silver_demand_cum.to_csv(os.path.join(testfolder,'Ag_demand_cum2050_allScens.csv'))


# In[63]:


plt.bar(silver_demand_cum.columns, silver_demand_cum.loc[2050], tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Silver Demand by Scenario')
plt.ylabel('[Tonnes]')


# In[64]:


silver_demand_cum


# In[65]:


all_results_yearly.loc[2050].filter(like='newInstalledCapacity') 
#FYI the area deployment doesn't overwrite the new installs column - do not trust those numbers!


# In[66]:


activecapacity = pd.DataFrame(all_results_yearly.loc[2050].filter(like='ActiveCapacity')).T/1e6
#activecapacity
newInstalledCap_cum_TW = pd.DataFrame(all_results_yearly.loc[2050].filter(like='newInstalledCapacity')).T
newInstalledCap_cum_TW


# In[67]:


silver_demand_cum.columns = newInstalledCap_cum_TW.columns = scennames


# In[68]:


agperW = silver_demand_cum/newInstalledCap_cum_TW
agperW


# In[69]:


plt.bar(agperW.columns[0:3], agperW.loc[2050][0:3], color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Silver Demand per Capacity')
plt.ylabel('Tonne/MW')


# ## Energy Data Org

# In[70]:


#compile all energy out results
energy_mod=pd.DataFrame()
for scen in scennames:
    # add the scen name as a prefix for later filtering
    scende = sim1.scenario[scen].dataOut_e.loc[0:30].add_prefix(str(scen+'_'))
    #concat into one large df
    energy_mod = pd.concat([energy_mod, scende], axis=1)

energy_mod.tail()


# In[71]:


energy_mat = pd.DataFrame()
for scen in scennames:
    for mat in MATERIALS:
        # add the scen name as a prefix for later filtering
        scenmatde = sim1.scenario[scen].material[mat].matdataOut_e.loc[0:30].add_prefix(str(scen+'_'+mat+'_'))
        #concat into one large df
        energy_mat = pd.concat([energy_mat, scenmatde], axis=1)

energy_mat.tail()


# In[72]:


allenergy = pd.concat([energy_mod,energy_mat], axis=1)
allenergy.index=idx_temp


# ## Graphing Energy Generation

# In[73]:


energyGen = allenergy.filter(like='e_out_annual')


# In[74]:


fig, ax1 = plt.subplots()

ax1.plot(energyGen)
#ax1.set_ylabel('Annual Deployments [MW]', color='blue')

#ax2 = ax1.twinx()
#ax2.plot(sf_reeds['TW_cum'], color='orange')
#ax2.set_ylabel('Cumulative Capacity [TW]', color='orange')
#ax1.set_yscale('log')

plt.legend(energyGen.columns)
plt.title('Annual Energy Generation')
plt.show()


# In[75]:


energyGen_p = energyGen.filter(like='_p')/1e12
energyGen_a = energyGen.filter(like='_a')/1e12


# In[76]:


#plt.plot(energyGen_p)#, color=['#006fa2','#ee005b','#734296'])
plt.plot(energyGen_p.index, energyGen_p.iloc[:,[0]], color='#0079C2')
plt.plot(energyGen_p.index, energyGen_p.iloc[:,[1]], color='#F7A11A', ls='--')
plt.plot(energyGen_p.index, energyGen_p.iloc[:,[2]], color='#5D9732', ls='-.')
plt.legend(scennames_p)
plt.title('Identical Power Installed: Annual Energy Generation')
plt.ylabel('Energy Generated [TWh]')


# In[77]:


#plt.plot(energyGen_p)#, color=['#006fa2','#ee005b','#734296'])
plt.plot(energyGen_a.index, energyGen_a.iloc[:,[0]], color='#0079C2')
plt.plot(energyGen_a.index, energyGen_a.iloc[:,[1]], color='#F7A11A', ls='--')
plt.plot(energyGen_a.index, energyGen_a.iloc[:,[2]], color='#5D9732', ls='-.')
plt.legend(scennames_a)
plt.title('Identical Area Installed: Annual Energy Generation')
plt.ylabel('Energy Generated [TWh]')


# Or as a bar plot

# In[78]:


energyGen_cum = energyGen.cumsum()
energyGen_cum_2050 = energyGen_cum.loc[[2050]]
energyGen_cum_2050/1e12
energyGen_cum_2050.columns = scennames
energyGen_cum_2050


# In[79]:


plt.bar(energyGen_cum_2050.columns, energyGen_cum_2050.loc[2050]/1e12, tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Energy Generated Cumulatively by Scenario')
plt.ylabel('[TWh]')


# In[80]:


energyGen_cum_2050_norm = energyGen_cum_2050/energyGen_cum_2050.loc[2050,'PERC_a']
plt.bar(energyGen_cum_2050_norm.columns, energyGen_cum_2050_norm.loc[2050], tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Energy Generated Cumulatively by Scenario - Normalized to PERC')
plt.ylabel('[TWh]')


# In[81]:


energyGen_cum_2050_norm


# ## Energy vs Silver Demand

# In[82]:


energyGen_cum_2050.columns=silver_demand_cum.columns=scennames
whpag = (energyGen_cum_2050)/silver_demand_cum #Wh generated cumulative, per silver demand
normalizer = whpag.loc[2050,'PERC_a']
whpag/normalizer


# In[83]:


plt.bar(whpag.columns, whpag.loc[2050]/1e12, tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Energy Generated Cumulatively per Silver Demand Tonnes')
plt.ylabel('[TWh/tonnes]')


# In[84]:


energyGen_cum_2050.columns=silver_demand_cum.columns=scennames
agpwh= silver_demand_cum/(energyGen_cum_2050) #Wh generated cumulative, per silver demand
normalizer = agpwh.loc[2050,'PERC_a']
agpwh_norm = agpwh/normalizer
agpwh_norm


# In[85]:


plt.bar(agpwh_norm.columns, agpwh_norm.loc[2050], tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Silver Demand Tonnes per energy generation, normalized')
plt.ylabel('[tonnes/TWh] Normalized')


# ## Net Energy Calcs

# In[86]:


#categorize the energy in values into lifecycle stages
mfg_energies = ['mod_MFG','mat_extraction','mat_MFG_virgin']
mfg_recycle_energies_LQ = ['mat_MFGScrap_LQ'] #LQ and HQ are separate becuase LQ is only LQ
mfg_recycle_energies_HQ = ['mat_MFGScrap_HQ'] #and HQ material is E_LQ + E_HQ
use_energies = ['mod_Install','mod_OandM','mod_Repair']
eol_energies = ['mat_Landfill','mod_Demount','mod_Store','mod_Resell_Certify']
eol_remfg_energies = ['mod_ReMFG_Disassmbly','mat_EoL_ReMFG_clean']
eol_recycle_energies_LQ = ['mod_Recycle_Crush','mat_Recycled_LQ']
eol_recycle_energies_HQ = ['mod_Recycle_Crush','mat_Recycled_HQ']

energy_demands_keys = [mfg_energies,mfg_recycle_energies_LQ,mfg_recycle_energies_HQ,use_energies,eol_energies,
                  eol_remfg_energies,eol_recycle_energies_LQ,eol_recycle_energies_HQ]
import itertools
energy_demands_flat = list(itertools.chain(*energy_demands_keys))
#energy_demands_flat


# In[87]:


#select the non energy generation columns for all scenarios
energy_demands = allenergy.loc[:,~allenergy.columns.isin(energyGen.columns)] 
edemand_perc_p = energy_demands.filter(like='PERC_p')
edemand_shj_p = energy_demands.filter(like='SHJ_p')
edemand_topcon_p = energy_demands.filter(like='TOPCon_p')
edemand_perc_a = energy_demands.filter(like='PERC_a')
edemand_shj_a = energy_demands.filter(like='SHJ_a')
edemand_topcon_a = energy_demands.filter(like='TOPCon_a')


# In[88]:


#for each scenario, create a cumulative total energy demand
for scen in scennames:
    colname = str(scen+'_e_demand_total')
    energy_demands[colname] = energy_demands.filter(like=scen).sum(axis=1)


# In[89]:


energy_demands_annual = energy_demands.filter(like='e_demand_total')
yrlyedemand_perc_p = energy_demands_annual.filter(like='PERC_p')
yrlyedemand_shj_p = energy_demands_annual.filter(like='SHJ_p')
yrlyedemand_topcon_p = energy_demands_annual.filter(like='TOPCon_p')
yrlyedemand_perc_a = energy_demands_annual.filter(like='PERC_a')
yrlyedemand_shj_a = energy_demands_annual.filter(like='SHJ_a')
yrlyedemand_topcon_a = energy_demands_annual.filter(like='TOPCon_a')


# In[90]:


#plt.plot(energy_demands_annual)
plt.plot(yrlyedemand_perc_p.index, yrlyedemand_perc_p/1e12, color='#0079C2')
plt.plot(yrlyedemand_shj_p.index, yrlyedemand_shj_p/1e12, color='#F7A11A', ls='--')
plt.plot(yrlyedemand_topcon_p.index, yrlyedemand_topcon_p/1e12, color='#5D9732', ls='-.')
plt.legend(scennames_p)
plt.title('Identical Power Installed: Annual Energy Demands for Manufacturing')
plt.ylabel('Energy Demand [TWh]')


# In[91]:


energy_demand_total_cum = energy_demands.filter(like='e_demand_total').cumsum()
energy_demand_total_cum_2050 = energy_demand_total_cum.loc[[2050]]
energy_demand_total_cum_2050.columns = scennames


# In[92]:


energy_demand_total_cum_2050/1e12


# In[93]:


energy_demand_total_cum_2050/energy_demand_total_cum_2050.loc[2050,'PERC_p']


# In[94]:


plt.bar(energy_demand_total_cum_2050.columns, energy_demand_total_cum_2050.loc[2050]/1e12, tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Cumulative Manufacturing Energy 2020-2050')
plt.ylabel('[TWh]')


# In[95]:


energyGen_cum_2050/1e12


# ## Net Energy

# In[96]:


net_energy_cum_2050 = (energyGen_cum_2050-energy_demand_total_cum_2050)/1e12
net_energy_cum_2050


# In[97]:


plt.bar(net_energy_cum_2050.columns, net_energy_cum_2050.loc[2050], tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Net Energy Cumulatively 2020-2050')
plt.ylabel('[TWh]')


# In[98]:


energyGen.columns = energy_demands_annual.columns = scennames
netEnergyAnnual_TWh = (energyGen - energy_demands_annual)/1e12


# In[99]:


round(netEnergyAnnual_TWh,0)


# In[100]:


fig, ax1 = plt.subplots()
#ax1.plot(netEnergyAnnual_TWh)


ax1.plot(netEnergyAnnual_TWh.index, netEnergyAnnual_TWh.iloc[:,[0]], color='#0079C2')
ax1.plot(netEnergyAnnual_TWh.index, netEnergyAnnual_TWh.iloc[:,[1]], color='#F7A11A', ls='--')
ax1.plot(netEnergyAnnual_TWh.index, netEnergyAnnual_TWh.iloc[:,[2]], color='#5D9732', ls='-.')


ax1.plot(netEnergyAnnual_TWh.index, netEnergyAnnual_TWh.iloc[:,[3]], color='#0079C2')
ax1.plot(netEnergyAnnual_TWh.index, netEnergyAnnual_TWh.iloc[:,[4]], color='#FFC423', ls='--')
ax1.plot(netEnergyAnnual_TWh.index, netEnergyAnnual_TWh.iloc[:,[5]], color='#8CC63F', ls='-.')
ax1.legend(scennames)

ax1.set_ylabel('Energy Demand [TWh]')
plt.title('Annual Net Energy')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Simulation for EROI and EBPT
# Currently we dont have the ability to do cohort energy tracking. Therefore, we will test discrete points in time to evaluate a single cohort (i.e. install in only 1 year and track the energy in and out over time from that one cohort)

# In[101]:


single_deploy_2020 = pd.DataFrame(index=idx_temp, columns=['MW'], dtype=float)
single_deploy_2020['MW'] = 0.0
single_deploy_2020.loc[2020,'MW'] = 100.0


# In[102]:


#creating scenarios for identical power and identical area deployed
scennames2 = ['PERC','SHJ','TOPCon'] #add later Blend and bifi on/off
MATERIALS = ['glass','silver','silicon'] #, 'copper', 'encapsulant', 'backsheet', 'aluminum_frames'
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[103]:


#load in a baseline and materials for modification
import PV_ICE

sim2 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames2:
    sim2.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim2.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# Modify the all one tech scenarios Scenarios:
# 
# Module level
# - trim to 2020-2050
# - no circularity
# - deployment projection
# - module eff
# 
# material level
# - glass per m2
# - silver per m2

# In[104]:


#trim to 2020-2050, this trims module and materials
sim2.trim_Years(startYear=2020)

#no circularity
sim2.scenMod_noCircularity()

#module eff
for scen in scennames2:
    sim2.scenario[scen].dataIn_m.loc[0:len(modeffs.index-1),'mod_eff'] = modeffs.filter(like=str(scen[0:3])).values

#glass modify
for scen in scennames2:
    sim2.scenario[scen].material['glass'].matdataIn_m['mat_massperm2'] = glassperm2
    
#silver modify
for scen in scennames2:
    sim2.scenario[scen].material['silver'].matdataIn_m.loc[0:len(Aguse.index-1),'mat_massperm2'] = Aguse.filter(like=str(scen[0:3])).values
    


# In[105]:


#deployment projection
#NEED TO PULL IN DEPLOYMENT PROJECTION

for scen in scennames2:
    sim2.scenario[scen].dataIn_m.loc[0:len(single_deploy_2020.index-1),'new_Installed_Capacity_[MW]'] = single_deploy_2020.values


# In[106]:


sim2.scenario['PERC'].dataIn_m


# In[107]:


for scen in scennames2:
    sim2.scenario[scen].dataIn_m.to_csv(os.path.join(testfolder,str('sim2_baseline_'+scen+'.csv')))


# ## 2020 Module

# In[108]:


#option 1, install identical power

sim2.calculateFlows(scenarios='PERC', bifacialityfactors=bifi_perc_path)
sim2.calculateFlows(scenarios='SHJ', bifacialityfactors=bifi_shj_path)
sim2.calculateFlows(scenarios='TOPCon', bifacialityfactors=bifi_topcon_path)

#perc_p_yearly, perc_p_cum = sim2.aggregateResults(scenarios='PERC')
#shj_p_yearly, shj_p_cum = sim2.aggregateResults(scenarios='SHJ')
#topcon_p_yearly, topcon_p_cum = sim2.aggregateResults(scenarios='TOPCon')


# In[109]:


plt.plot(sim2.scenario['PERC'].dataOut_m['Installed_Capacity_[W]'])


# In[110]:


#compile all energy out results
energy_mod2=pd.DataFrame()
for scen in scennames2:
    # add the scen name as a prefix for later filtering
    scende = sim2.scenario[scen].dataOut_e.loc[0:30].add_prefix(str(scen+'_'))
    #concat into one large df
    energy_mod2 = pd.concat([energy_mod2, scende], axis=1)

#energy_mod2.head()


# In[111]:


energy_mat2 = pd.DataFrame()
for scen in scennames2:
    for mat in MATERIALS:
        # add the scen name as a prefix for later filtering
        scenmatde = sim2.scenario[scen].material[mat].matdataOut_e.loc[0:30].add_prefix(str(scen+'_'+mat+'_'))
        #concat into one large df
        energy_mat2 = pd.concat([energy_mat2, scenmatde], axis=1)

#energy_mat2.tail()


# In[112]:


allenergy2 = pd.concat([energy_mod2,energy_mat2], axis=1)
allenergy2.index=idx_temp


# In[113]:


allenergy2


# In[114]:


perc_e_flows = allenergy2.filter(like='PERC')
perc_e_out = perc_e_flows.filter(like='e_out_annual_[Wh]')
perc_e_demand = perc_e_flows.loc[:,~perc_e_flows.columns.isin(perc_e_out.columns)] 

shj_e_flows = allenergy2.filter(like='SHJ')
shj_e_out = shj_e_flows.filter(like='e_out_annual_[Wh]')
shj_e_demand = shj_e_flows.loc[:,~shj_e_flows.columns.isin(shj_e_out.columns)] 

topcon_e_flows = allenergy2.filter(like='TOPCon')
topcon_e_out = topcon_e_flows.filter(like='e_out_annual_[Wh]')
topcon_e_demand = topcon_e_flows.loc[:,~topcon_e_flows.columns.isin(topcon_e_out.columns)] 


# In[115]:


perc_e_demand_total_annual = pd.DataFrame(perc_e_demand.sum(axis=1), columns=['Wh']) #includes module and material
shj_e_demand_total_annual = pd.DataFrame(shj_e_demand.sum(axis=1), columns=['Wh']) #includes module and material
topcon_e_demand_total_annual = pd.DataFrame(topcon_e_demand.sum(axis=1), columns=['Wh']) #includes module and material


# In[116]:


perc_e_out.columns=perc_e_demand_total_annual.columns
perc_net_energy_annual = perc_e_out-perc_e_demand_total_annual
#perc_net_energy_annual/1e9 # GWh

shj_e_out.columns = shj_e_demand_total_annual.columns
shj_net_energy_annual = shj_e_out - shj_e_demand_total_annual
#shj_net_energy_annual/1e9 # GWh

topcon_e_out.columns=topcon_e_demand_total_annual.columns
topcon_net_energy_annual = topcon_e_out - topcon_e_demand_total_annual
#perc_net_energy_annual/1e9 # GWh


# In[117]:


width = 0.3
plt.bar(perc_net_energy_annual.index-width, perc_net_energy_annual['Wh']/1e9, width, color='#0079C2')
plt.bar(shj_net_energy_annual.index+width, shj_net_energy_annual['Wh']/1e9, width, color='#F7A11A' )
plt.bar(topcon_net_energy_annual.index, topcon_net_energy_annual['Wh']/1e9, width, color='#5D9732')

plt.legend(scennames2)
plt.title('Net Annual Energy: 2020 Module')
plt.ylabel('Net Energy [GWh]')


# In[118]:


#EROI = Eout/Ein
perc_e_out_cum = perc_e_out.sum()
perc_e_in_cum = perc_e_demand_total_annual.sum()
perc_e_out_cum/perc_e_in_cum


# In[119]:


shj_e_out_cum = shj_e_out.sum()
shj_e_in_cum = shj_e_demand_total_annual.sum()
shj_e_out_cum/shj_e_in_cum


# In[120]:


topcon_e_out_cum = topcon_e_out.sum()
topcon_e_in_cum = topcon_e_demand_total_annual.sum()
topcon_e_out_cum/topcon_e_in_cum


# ## 2030 Module
# Grab the module properties from 2030, and deploy 100 MW for 30 yr project life

# In[121]:


idx_30_60 = pd.Series(range(2030,2061))
single_deploy_2030 = pd.DataFrame(index=idx_30_60, columns=['MW'], dtype=float)
single_deploy_2030['MW'] = 0.0
single_deploy_2030.loc[2030,'MW'] = 100.0
#single_deploy_2030


# In[122]:


#creating scenarios for identical power and identical area deployed
scennames3 = ['PERC','SHJ','TOPCon'] #add later Blend and bifi on/off
MATERIALS = ['glass','silver','silicon'] #, 'copper', 'encapsulant', 'backsheet', 'aluminum_frames'
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[123]:


#load in a baseline and materials for modification
import PV_ICE

sim3 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames3:
    sim3.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim3.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# Modify the all one tech scenarios Scenarios:
# 
# Module level
# - trim to 2020-2050
# - no circularity
# - deployment projection
# - module eff
# 
# material level
# - glass per m2
# - silver per m2

# In[124]:


#trim to 2020-2050, this trims module and materials
sim3.trim_Years(startYear=2020)

#no circularity
sim3.scenMod_noCircularity()

#module eff
for scen in scennames3:
    sim3.scenario[scen].dataIn_m.loc[0:len(modeffs.index-1),'mod_eff'] = modeffs.filter(like=str(scen[0:3])).values

#glass modify
for scen in scennames3:
    sim3.scenario[scen].material['glass'].matdataIn_m['mat_massperm2'] = glassperm2
    
#silver modify
for scen in scennames3:
    sim3.scenario[scen].material['silver'].matdataIn_m.loc[0:len(Aguse.index-1),'mat_massperm2'] = Aguse.filter(like=str(scen[0:3])).values
    


# In[125]:


#Set 2020 module and material properties = 2030
for scen in scennames3:
    sim3.scenario[scen].dataIn_m.loc[0] = sim3.scenario[scen].dataIn_m.loc[10] #reassign row values from 2030 to 2020
    sim3.scenario[scen].dataIn_m.loc[0,'year'] = 2020 #fix the overwrite
    
sim3.scenario[scen].dataIn_m.head()


# In[126]:


#deployment projection
#NEED TO PULL IN DEPLOYMENT PROJECTION

for scen in scennames3:
    sim3.scenario[scen].dataIn_m.loc[0:len(single_deploy_2020.index-1),'new_Installed_Capacity_[MW]'] = single_deploy_2020.values


# In[127]:


sim3.scenario[scen].dataIn_m.head()


# In[128]:


#deployment projection
#NEED TO PULL IN DEPLOYMENT PROJECTION

#for scen in scennames2:
#    sim2.scenario[scen].dataIn_m.loc[0:len(single_deploy_2030.index-1),'new_Installed_Capacity_[MW]'] = single_deploy_2030.values


# In[129]:


#option 1, install identical power

sim3.calculateFlows(scenarios='PERC', bifacialityfactors=bifi_perc_path)
sim3.calculateFlows(scenarios='SHJ', bifacialityfactors=bifi_shj_path)
sim3.calculateFlows(scenarios='TOPCon', bifacialityfactors=bifi_topcon_path)

#perc_p_yearly, perc_p_cum = sim2.aggregateResults(scenarios='PERC')
#shj_p_yearly, shj_p_cum = sim2.aggregateResults(scenarios='SHJ')
#topcon_p_yearly, topcon_p_cum = sim2.aggregateResults(scenarios='TOPCon')


# In[ ]:





# In[130]:


plt.plot(sim3.scenario['PERC'].dataOut_m['Installed_Capacity_[W]'])


# In[131]:


#compile all energy out results
energy_mod3=pd.DataFrame()
for scen in scennames3:
    # add the scen name as a prefix for later filtering
    scende = sim3.scenario[scen].dataOut_e.loc[0:30].add_prefix(str(scen+'_'))
    #concat into one large df
    energy_mod3 = pd.concat([energy_mod3, scende], axis=1)

#energy_mod2.head()


# In[132]:


#compile material energy demands
energy_mat3 = pd.DataFrame()
for scen in scennames3:
    for mat in MATERIALS:
        # add the scen name as a prefix for later filtering
        scenmatde = sim3.scenario[scen].material[mat].matdataOut_e.loc[0:30].add_prefix(str(scen+'_'+mat+'_'))
        #concat into one large df
        energy_mat3 = pd.concat([energy_mat3, scenmatde], axis=1)

#energy_mat3.tail()


# In[133]:


allenergy3 = pd.concat([energy_mod3,energy_mat3], axis=1)
allenergy3.index=idx_30_60


# In[134]:


allenergy3


# In[135]:


perc_e_flows = allenergy3.filter(like='PERC')
perc_e_out = perc_e_flows.filter(like='e_out_annual_[Wh]')
perc_e_demand = perc_e_flows.loc[:,~perc_e_flows.columns.isin(perc_e_out.columns)] 

shj_e_flows = allenergy3.filter(like='SHJ')
shj_e_out = shj_e_flows.filter(like='e_out_annual_[Wh]')
shj_e_demand = shj_e_flows.loc[:,~shj_e_flows.columns.isin(shj_e_out.columns)] 

topcon_e_flows = allenergy3.filter(like='TOPCon')
topcon_e_out = topcon_e_flows.filter(like='e_out_annual_[Wh]')
topcon_e_demand = topcon_e_flows.loc[:,~topcon_e_flows.columns.isin(topcon_e_out.columns)] 


# In[136]:


perc_e_demand_total_annual = pd.DataFrame(perc_e_demand.sum(axis=1), columns=['Wh']) #includes module and material
shj_e_demand_total_annual = pd.DataFrame(shj_e_demand.sum(axis=1), columns=['Wh']) #includes module and material
topcon_e_demand_total_annual = pd.DataFrame(topcon_e_demand.sum(axis=1), columns=['Wh']) #includes module and material


# In[137]:


perc_e_out.columns=perc_e_demand_total_annual.columns
perc_net_energy_annual = perc_e_out-perc_e_demand_total_annual
#perc_net_energy_annual/1e9 # GWh

shj_e_out.columns = shj_e_demand_total_annual.columns
shj_net_energy_annual = shj_e_out - shj_e_demand_total_annual
#shj_net_energy_annual/1e9 # GWh

topcon_e_out.columns=topcon_e_demand_total_annual.columns
topcon_net_energy_annual = topcon_e_out - topcon_e_demand_total_annual
#perc_net_energy_annual/1e9 # GWh


# In[138]:


width = 0.3
plt.bar(perc_net_energy_annual.index-width, perc_net_energy_annual['Wh']/1e9, width, color='#0079C2')
plt.bar(shj_net_energy_annual.index+width, shj_net_energy_annual['Wh']/1e9, width, color='#F7A11A' )
plt.bar(topcon_net_energy_annual.index, topcon_net_energy_annual['Wh']/1e9, width, color='#5D9732')

plt.legend(scennames2)
plt.title('Net Annual Energy: 2030 Module')
plt.ylabel('Net Energy [GWh]')


# In[139]:


#EROI = Eout/Ein
perc_e_out_cum = perc_e_out.sum()
perc_e_in_cum = perc_e_demand_total_annual.sum()
perc_e_out_cum/perc_e_in_cum


# In[140]:


shj_e_out_cum = shj_e_out.sum()
shj_e_in_cum = shj_e_demand_total_annual.sum()
shj_e_out_cum/shj_e_in_cum


# In[141]:


topcon_e_out_cum = topcon_e_out.sum()
topcon_e_in_cum = topcon_e_demand_total_annual.sum()
topcon_e_out_cum/topcon_e_in_cum


# ## 2050 Module

# In[ ]:





# In[142]:


idx_50_80 = pd.Series(range(2050,2081))


# In[143]:


#creating scenarios for identical power and identical area deployed
scennames4 = ['PERC','SHJ','TOPCon'] #add later Blend and bifi on/off
MATERIALS = ['glass','silver','silicon'] #, 'copper', 'encapsulant', 'backsheet', 'aluminum_frames'
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[144]:


#load in a baseline and materials for modification
import PV_ICE

sim4 = PV_ICE.Simulation(name='sim1', path=testfolder)
for scen in scennames4:
    sim4.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim4.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# Modify the all one tech scenarios Scenarios:
# 
# Module level
# - trim to 2020-2050
# - no circularity
# - deployment projection
# - module eff
# 
# material level
# - glass per m2
# - silver per m2

# In[145]:


#trim to 2020-2050, this trims module and materials
sim4.trim_Years(startYear=2020)

#no circularity
sim4.scenMod_noCircularity()

#module eff
for scen in scennames4:
    sim4.scenario[scen].dataIn_m.loc[0:len(modeffs.index-1),'mod_eff'] = modeffs.filter(like=str(scen[0:3])).values

#glass modify
for scen in scennames4:
    sim4.scenario[scen].material['glass'].matdataIn_m['mat_massperm2'] = glassperm2
    
#silver modify
for scen in scennames4:
    sim4.scenario[scen].material['silver'].matdataIn_m.loc[0:len(Aguse.index-1),'mat_massperm2'] = Aguse.filter(like=str(scen[0:3])).values
    


# In[146]:


#Set 2020 module and material properties = 2030
for scen in scennames4:
    sim4.scenario[scen].dataIn_m.loc[0] = sim4.scenario[scen].dataIn_m.iloc[-1] #reassign row values from 2030 to 2020
    sim4.scenario[scen].dataIn_m.loc[0,'year'] = 2020 #fix the overwrite
    
sim4.scenario[scen].dataIn_m.head()


# In[147]:


#deployment projection
#NEED TO PULL IN DEPLOYMENT PROJECTION

for scen in scennames4:
    sim4.scenario[scen].dataIn_m.loc[0:len(single_deploy_2020.index-1),'new_Installed_Capacity_[MW]'] = single_deploy_2020.values


# In[148]:


sim4.scenario[scen].dataIn_m.head()


# In[149]:


#deployment projection
#NEED TO PULL IN DEPLOYMENT PROJECTION

#for scen in scennames2:
#    sim2.scenario[scen].dataIn_m.loc[0:len(single_deploy_2030.index-1),'new_Installed_Capacity_[MW]'] = single_deploy_2030.values


# In[150]:


#option 1, install identical power

sim4.calculateFlows(scenarios='PERC', bifacialityfactors=bifi_perc_path)
sim4.calculateFlows(scenarios='SHJ', bifacialityfactors=bifi_shj_path)
sim4.calculateFlows(scenarios='TOPCon', bifacialityfactors=bifi_topcon_path)

#perc_p_yearly, perc_p_cum = sim2.aggregateResults(scenarios='PERC')
#shj_p_yearly, shj_p_cum = sim2.aggregateResults(scenarios='SHJ')
#topcon_p_yearly, topcon_p_cum = sim2.aggregateResults(scenarios='TOPCon')


# In[ ]:





# In[151]:


plt.plot(sim4.scenario['PERC'].dataOut_m['Installed_Capacity_[W]'])


# In[152]:


#compile all energy out results
energy_mod4=pd.DataFrame()
for scen in scennames4:
    # add the scen name as a prefix for later filtering
    scende = sim4.scenario[scen].dataOut_e.loc[0:30].add_prefix(str(scen+'_'))
    #concat into one large df
    energy_mod4 = pd.concat([energy_mod4, scende], axis=1)

#energy_mod2.head()


# In[153]:


#compile material energy demands
energy_mat4 = pd.DataFrame()
for scen in scennames4:
    for mat in MATERIALS:
        # add the scen name as a prefix for later filtering
        scenmatde = sim4.scenario[scen].material[mat].matdataOut_e.loc[0:30].add_prefix(str(scen+'_'+mat+'_'))
        #concat into one large df
        energy_mat4 = pd.concat([energy_mat4, scenmatde], axis=1)

#energy_mat3.tail()


# In[154]:


allenergy4 = pd.concat([energy_mod4,energy_mat4], axis=1)
allenergy4.index=idx_50_80


# In[155]:


allenergy4


# In[156]:


perc_e_flows = allenergy4.filter(like='PERC')
perc_e_out = perc_e_flows.filter(like='e_out_annual_[Wh]')
perc_e_demand = perc_e_flows.loc[:,~perc_e_flows.columns.isin(perc_e_out.columns)] 

shj_e_flows = allenergy4.filter(like='SHJ')
shj_e_out = shj_e_flows.filter(like='e_out_annual_[Wh]')
shj_e_demand = shj_e_flows.loc[:,~shj_e_flows.columns.isin(shj_e_out.columns)] 

topcon_e_flows = allenergy4.filter(like='TOPCon')
topcon_e_out = topcon_e_flows.filter(like='e_out_annual_[Wh]')
topcon_e_demand = topcon_e_flows.loc[:,~topcon_e_flows.columns.isin(topcon_e_out.columns)] 


# In[157]:


perc_e_demand_total_annual = pd.DataFrame(perc_e_demand.sum(axis=1), columns=['Wh']) #includes module and material
shj_e_demand_total_annual = pd.DataFrame(shj_e_demand.sum(axis=1), columns=['Wh']) #includes module and material
topcon_e_demand_total_annual = pd.DataFrame(topcon_e_demand.sum(axis=1), columns=['Wh']) #includes module and material


# In[158]:


perc_e_out.columns=perc_e_demand_total_annual.columns
perc_net_energy_annual = perc_e_out-perc_e_demand_total_annual
#perc_net_energy_annual/1e9 # GWh

shj_e_out.columns = shj_e_demand_total_annual.columns
shj_net_energy_annual = shj_e_out - shj_e_demand_total_annual
#shj_net_energy_annual/1e9 # GWh

topcon_e_out.columns=topcon_e_demand_total_annual.columns
topcon_net_energy_annual = topcon_e_out - topcon_e_demand_total_annual
#perc_net_energy_annual/1e9 # GWh


# In[159]:


width = 0.3
plt.bar(perc_net_energy_annual.index-width, perc_net_energy_annual['Wh']/1e9, width, color='#0079C2')
plt.bar(shj_net_energy_annual.index+width, shj_net_energy_annual['Wh']/1e9, width, color='#F7A11A' )
plt.bar(topcon_net_energy_annual.index, topcon_net_energy_annual['Wh']/1e9, width, color='#5D9732')

plt.legend(scennames2)
plt.title('Net Annual Energy: 2050 Module')
plt.ylabel('Net Energy [GWh]')


# In[160]:


#EROI = Eout/Ein
perc_e_out_cum = perc_e_out.sum()
perc_e_in_cum = perc_e_demand_total_annual.sum()
perc_e_out_cum/perc_e_in_cum


# In[161]:


shj_e_out_cum = shj_e_out.sum()
shj_e_in_cum = shj_e_demand_total_annual.sum()
shj_e_out_cum/shj_e_in_cum


# In[162]:


topcon_e_out_cum = topcon_e_out.sum()
topcon_e_in_cum = topcon_e_demand_total_annual.sum()
topcon_e_out_cum/topcon_e_in_cum


# In[ ]:





# ## Manufacturing Energy of One module each year

# Assuming a 2.0 m^2 module

# In[163]:


scennames_anModule = ['PERC_anModule','SHJ_anModule','TOPCon_anModule']
bifipaths = [bifi_perc_path,bifi_shj_path,bifi_topcon_path]


# In[164]:


#create an area dataframe to feed in a module each year
idx_temp = Aguse.index #grab matching index
area_deploy_anModule = pd.DataFrame(index=idx_temp, dtype=float) #create an empty DF
area_deploy_anModule['Area'] = 2.0
area_deploy_anModule.head()


# In[165]:


#creating scenarios for identical power and identical area deployed
MATERIALS = ['glass','silver','silicon'] #, 'copper', 'encapsulant', 'backsheet', 'aluminum_frames'
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[166]:


#load in a baseline and materials for modification
import PV_ICE

sim_anModule = PV_ICE.Simulation(name='sim_anModule', path=testfolder)
for scen in scennames_anModule:
    sim_anModule.createScenario(name=scen, massmodulefile=moduleFile_m, energymodulefile=moduleFile_e)
    for mat in range (0, len(MATERIALS)):
        matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'.csv')
        matbaseline_e = os.path.join(baselinesfolder,'baseline_material_energy_'+MATERIALS[mat]+'.csv')
        sim_anModule.scenario[scen].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m, energymatfile=matbaseline_e)


# Modify the all one tech scenarios Scenarios:
# 
# Module level
# - trim to 2020-2050
# - no circularity
# - deployment projection
# - module eff
# 
# material level
# - glass per m2
# - silver per m2

# In[167]:


#trim to 2020-2050, this trims module and materials
sim_anModule.trim_Years(startYear=2020)

#no circularity
sim_anModule.scenMod_noCircularity()

#module eff
for scen in scennames_anModule:
    sim_anModule.scenario[scen].dataIn_m.loc[0:len(modeffs.index-1),'mod_eff'] = modeffs.filter(like=str(scen[0:3])).values

#glass modify
for scen in scennames_anModule:
    sim_anModule.scenario[scen].material['glass'].matdataIn_m['mat_massperm2'] = glassperm2
    
#silver modify
for scen in scennames_anModule:
    sim_anModule.scenario[scen].material['silver'].matdataIn_m.loc[0:len(Aguse.index-1),'mat_massperm2'] = Aguse.filter(like=str(scen[0:3])).values
    


# In[168]:


#option 1, install identical power
sim_anModule.calculateFlows(scenarios='PERC_anModule', bifacialityfactors=bifi_perc_path, installByArea=list(area_deploy_anModule['Area']))
sim_anModule.calculateFlows(scenarios='SHJ_anModule', bifacialityfactors=bifi_shj_path,  installByArea=list(area_deploy_anModule['Area']))
sim_anModule.calculateFlows(scenarios='TOPCon_anModule', bifacialityfactors=bifi_topcon_path,  installByArea=list(area_deploy_anModule['Area']))

perc_anModule_yearly, perc_anModule_cum = sim_anModule.aggregateResults(scenarios='PERC_anModule')
shj_anModule_yearly, shj_anModule_cum = sim_anModule.aggregateResults(scenarios='SHJ_anModule')
topcon_anModule_yearly, topcon_anModule_cum = sim_anModule.aggregateResults(scenarios='TOPCon_anModule')


# In[169]:


anModule_yearly, anModule_cum = sim_anModule.aggregateResults()
anModule_yearly.columns


# In[255]:


#compile all energy out results
energy_anModule=pd.DataFrame()
for scen in scennames_anModule:
    # add the scen name as a prefix for later filtering
    scende = sim_anModule.scenario[scen].dataOut_e.loc[0:30].add_prefix(str(scen+'_'))
    #concat into one large df
    energy_anModule = pd.concat([energy_anModule, scende], axis=1)

energy_anModule.tail()


# In[252]:


energy_mat_anModule = pd.DataFrame()
for scen in scennames_anModule:
    for mat in MATERIALS:
        # add the scen name as a prefix for later filtering
        scenmatde = sim_anModule.scenario[scen].material[mat].matdataOut_e.loc[0:30].add_prefix(str(scen+'_'+mat+'_'))
        #concat into one large df
        energy_mat_anModule = pd.concat([energy_mat_anModule, scenmatde], axis=1)

energy_mat_anModule.tail()


# In[172]:


allenergy_anModule = pd.concat([energy_anModule,energy_mat_anModule], axis=1)
allenergy_anModule.index=idx_temp


# In[200]:


remove = allenergy_anModule.filter(like='e_out_annual').columns
energy_demand_anModule = allenergy_anModule.drop(columns=remove)


# In[208]:


energy_demand_anModule_perc = energy_demand_anModule.filter(like='PERC')
energy_demand_anModule_shj = energy_demand_anModule.filter(like='SHJ')
energy_demand_anModule_topcon = energy_demand_anModule.filter(like='TOPCon')


# In[221]:


energy_demand_anModule_perc_cum = pd.DataFrame(energy_demand_anModule_perc.sum(axis=1), columns=['E_mfg_anModule_[Wh]'])
energy_demand_anModule_shj_cum = pd.DataFrame(energy_demand_anModule_shj.sum(axis=1), columns=['E_mfg_anModule_[Wh]'])
energy_demand_anModule_topcon_cum = pd.DataFrame(energy_demand_anModule_topcon.sum(axis=1), columns=['E_mfg_anModule_[Wh]'])
mfg_anModule = pd.concat([energy_demand_anModule_perc_cum,energy_demand_anModule_shj_cum,energy_demand_anModule_topcon_cum], axis=1)
mfg_anModule.columns = scennames_anModule


# In[222]:


fig, ax1 = plt.subplots()
#ax1.plot(netEnergyAnnual_TWh)


ax1.plot(energy_demand_anModule_perc_cum/1e6, color='#0079C2')
ax1.plot(energy_demand_anModule_shj_cum/1e6, color='#F7A11A', ls='--')
ax1.plot(energy_demand_anModule_topcon_cum/1e6, color='#5D9732', ls='-.')

plt.legend(scennames)
#ax1.set_yscale('log')
ax1.set_ylabel('Manufacturing Energy [MWh/module]')
plt.title('Manufacturing Energy by Technology over Time')
plt.show()


# In[249]:


#mfg_anModule
#shows that they are in fact slightly different energy demands between technologies.
#lets divide by PERC and see % wise how different.
mfg_anModule_normalized = mfg_anModule.iloc[:,[0,1,2]]/mfg_anModule.iloc[:,[0]].values
mfg_anModule_normalized#.loc[[2050]]


# separate out by module vs material energy demand

# In[263]:


energy_mat_anModule_perc_glass = energy_mat_anModule.filter(like='PERC').filter(like='glass')
energy_mat_anModule_perc_si = energy_mat_anModule.filter(like='PERC').filter(like='silicon')
energy_mat_anModule_perc_ag = energy_mat_anModule.filter(like='PERC').filter(like='silver')

energy_anModule_perc_mod_temp = energy_anModule.filter(like='PERC')
remove_1 = energy_anModule.filter(like='PERC').filter(like='e_out').columns
energy_anModule_perc_mod = energy_anModule_perc_mod_temp.drop(columns=remove_1)


# In[267]:


emod = energy_anModule_perc_mod.sum(axis=1)
eglass = energy_mat_anModule_perc_glass.sum(axis=1)
esi = energy_mat_anModule_perc_si.sum(axis=1)
eag = energy_mat_anModule_perc_ag.sum(axis=1)
e_bkdwn_mod_mat = pd.concat([emod,eglass,esi,eag], axis=1, keys=['mod','glass','silicon','silver'])


# In[272]:


e_bkdwn_mod_mat


# In[271]:


plt.plot(e_bkdwn_mod_mat/1e6)
plt.legend(e_bkdwn_mod_mat.columns)
plt.title('PERC MFGing energy Demands by component')
plt.ylabel('Manufacturing Energy [MWh/module]')

