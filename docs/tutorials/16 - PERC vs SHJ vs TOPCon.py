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


# In[202]:


plt.plot(modeffs.index, modeffs['PERC'], color='#0079C2')
plt.plot(modeffs.index, modeffs['SHJ'], color='#F7A11A', ls='--')
plt.plot(modeffs.index, modeffs['TOPCon'], color='#5D9732', ls='-.')

plt.legend(modeffs.columns)
plt.title('Module Efficiency over Time')
plt.ylabel('Module Efficiency [%]')


# In[203]:


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


# In[ ]:





# # Scenario Creation

# In[34]:


#creating scenarios for identical power and identical area deployed
scennames = ['PERC_p','SHJ_p','TOPCon_p', 'PERC_a','SHJ_a','TOPCon_a'] #add later Blend and bifi on/off
MATERIALS = ['glass','silver','silicon'] #, 'copper', 'encapsulant', 'backsheet', 'aluminum_frames'
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_US.csv')
moduleFile_e = os.path.join(baselinesfolder, 'baseline_modules_energy.csv')


# In[35]:


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

# In[36]:


#trim to 2020-2050, this trims module and materials
sim1.trim_Years(startYear=2020)


# In[37]:


#no circularity
sim1.scenMod_noCircularity()


# In[38]:


#deployment projection
#NEED TO PULL IN DEPLOYMENT PROJECTION

for scen in scennames:
    sim1.scenario[scen].dataIn_m.loc[0:len(newdeploymentcurve.index-1),'new_Installed_Capacity_[MW]'] = newdeploymentcurve.values


# In[39]:


#module eff
#modeffs
for scen in scennames:
    sim1.scenario[scen].dataIn_m.loc[0:len(modeffs.index-1),'mod_eff'] = modeffs.filter(like=str(scen[0:3])).values


# In[40]:


#glass modify
for scen in scennames:
    sim1.scenario[scen].material['glass'].matdataIn_m['mat_massperm2'] = glassperm2


# In[41]:


#silver modify
#Aguse
for scen in scennames:
    sim1.scenario[scen].material['silver'].matdataIn_m.loc[0:len(Aguse.index-1),'mat_massperm2'] = Aguse.filter(like=str(scen[0:3])).values


# Check to make sure the modifications took.

# In[42]:


sim1.scenario['SHJ_a'].dataIn_m.head(10)


# In[43]:


sim1.scenario['SHJ_p'].material['silver'].matdataIn_m.head()


# # Run Simulations

# ## Option 1: Compare with Idential Power Installed

# In[44]:


scennames_p = ['PERC_p','SHJ_p','TOPCon_p']
bifipaths = [bifi_perc_path,bifi_shj_path,bifi_topcon_path]


# In[45]:


#option 1, install identical power
sim1.calculateFlows(scenarios='PERC_p', bifacialityfactors=bifi_perc_path)
sim1.calculateFlows(scenarios='SHJ_p', bifacialityfactors=bifi_shj_path)
sim1.calculateFlows(scenarios='TOPCon_p', bifacialityfactors=bifi_topcon_path)

perc_p_yearly, perc_p_cum = sim1.aggregateResults(scenarios='PERC_p')
shj_p_yearly, shj_p_cum = sim1.aggregateResults(scenarios='SHJ_p')
topcon_p_yearly, topcon_p_cum = sim1.aggregateResults(scenarios='TOPCon_p')


# ## Option 2: Compare with Idential Area Installed

# In[46]:


scennames_a = ['PERC_a','SHJ_a','TOPCon_a']
bifipaths = [bifi_perc_path,bifi_shj_path,bifi_topcon_path]


# In[47]:


#Calculate Area deployed based on PERC and modified SF projection above
idx_temp = Aguse.index #grab matching index
area_deploy = pd.DataFrame(index=idx_temp, dtype=float) #create an empty DF
area_deploy['Area'] = sim1.scenario['PERC_p'].dataOut_m['Area'].values
area_deploy.head()


# In[48]:


#option 1, install identical power
sim1.calculateFlows(scenarios='PERC_a', bifacialityfactors=bifi_perc_path, installByArea=list(area_deploy['Area']))
sim1.calculateFlows(scenarios='SHJ_a', bifacialityfactors=bifi_shj_path,  installByArea=list(area_deploy['Area']))
sim1.calculateFlows(scenarios='TOPCon_a', bifacialityfactors=bifi_topcon_path,  installByArea=list(area_deploy['Area']))

perc_a_yearly, perc_a_cum = sim1.aggregateResults(scenarios='PERC_a')
shj_a_yearly, shj_a_cum = sim1.aggregateResults(scenarios='SHJ_a')
topcon_a_yearly, topcon_a_cum = sim1.aggregateResults(scenarios='TOPCon_a')


# In[49]:


all_results_yearly, all_results_cum = sim1.aggregateResults()
all_results_yearly.columns


# ### Compare Effective Capacity

# In[50]:


activecapacity_yearly_TW = pd.DataFrame(all_results_yearly.filter(like='ActiveCapacity'))/1e6
activecapacity_yearly_TW_p = activecapacity_yearly_TW.filter(like='_p')
activecapacity_yearly_TW_a = activecapacity_yearly_TW.filter(like='_a')


# In[98]:


plt.plot(activecapacity_yearly_TW_p.index, activecapacity_yearly_TW_p.iloc[:,[0]], color='#0079C2')
plt.plot(activecapacity_yearly_TW_p.index, activecapacity_yearly_TW_p.iloc[:,[1]], color='#F7A11A', ls='--')
plt.plot(activecapacity_yearly_TW_p.index, activecapacity_yearly_TW_p.iloc[:,[2]], color='#5D9732', ls='-.')
plt.legend(scennames_p)
plt.title('Identical Installed Power: Effective Capacity')
plt.ylabel('Effective Capacity [TW]')


# In[97]:


plt.plot(activecapacity_yearly_TW_a.index, activecapacity_yearly_TW_a.iloc[:,[0]], color='#0079C2')
plt.plot(activecapacity_yearly_TW_a.index, activecapacity_yearly_TW_a.iloc[:,[1]], color='#F7A11A', ls='--')
plt.plot(activecapacity_yearly_TW_a.index, activecapacity_yearly_TW_a.iloc[:,[2]], color='#5D9732', ls='-.')
plt.legend(scennames_a)
plt.title('Identical Installed Area: Effective Capacity')
plt.ylabel('Effective Capacity [TW]')


# ### Compare Area Deployed

# In[53]:


#compile all energy out results
area_deployed=pd.DataFrame()
for scen in scennames:
    # add the scen name as a prefix for later filtering
    scen_area = sim1.scenario[scen].dataOut_m[['Cumulative_Active_Area']].add_prefix(str(scen+'_'))
    #concat into one large df
    area_deployed = pd.concat([area_deployed, scen_area], axis=1)

area_deployed.index = idx_temp
area_deployed.tail()


# In[99]:


plt.plot(area_deployed.index, area_deployed.iloc[:,[0]]/1e6, color='#0079C2')
plt.plot(area_deployed.index, area_deployed.iloc[:,[1]]/1e6, color='#F7A11A', ls='--')
plt.plot(area_deployed.index, area_deployed.iloc[:,[2]]/1e6, color='#5D9732', ls='-.')
plt.legend(scennames_p)
plt.title('Identical Installed Power: Cumulative Active Area')
plt.ylabel('Area [million m2]')


# In[100]:


plt.plot(area_deployed.index, area_deployed.iloc[:,[3]]/1e6, color='#0079C2')
plt.plot(area_deployed.index, area_deployed.iloc[:,[4]]/1e6, color='#F7A11A', ls='--')
plt.plot(area_deployed.index, area_deployed.iloc[:,[5]]/1e6, color='#5D9732', ls='-.')
plt.legend(scennames_a)
plt.title('Identical Installed Area: Cumulative Active Area')
plt.ylabel('Area [million m2]')


# ## Compare Silver Demand

# In[56]:


sim1.plotMaterialComparisonAcrossScenarios(keyword='mat_Virgin_Stock', material='silver')


# In[57]:


silver_demand_cum = pd.DataFrame(all_results_cum.filter(like='VirginStock_silver').loc[2050]).T


# In[58]:


silver_demand_cum
silver_demand_cum.to_csv(os.path.join(testfolder,'Ag_demand_cum2050_allScens.csv'))


# In[101]:


plt.bar(silver_demand_cum.columns, silver_demand_cum.loc[2050], tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Silver Demand by Scenario')
plt.ylabel('[Tonnes]')


# In[60]:


silver_demand_cum


# In[61]:


activecapacity = pd.DataFrame(all_results_yearly.loc[2050].filter(like='ActiveCapacity')).T/1e6
activecapacity


# In[62]:


silver_demand_cum.columns = activecapacity.columns = scennames


# In[63]:


agperW = silver_demand_cum/activecapacity
agperW


# In[102]:


plt.bar(agperW.columns[0:3], agperW.loc[2050][0:3], color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Silver Demand per Capacity')
plt.ylabel('Tonne/TW')


# ## Energy Data Org

# In[118]:


#compile all energy out results
energy_mod=pd.DataFrame()
for scen in scennames:
    # add the scen name as a prefix for later filtering
    scende = sim1.scenario[scen].dataOut_e.loc[0:30].add_prefix(str(scen+'_'))
    #concat into one large df
    energy_mod = pd.concat([energy_mod, scende], axis=1)

energy_mod.tail()


# In[119]:


energy_mat = pd.DataFrame()
for scen in scennames:
    for mat in MATERIALS:
        # add the scen name as a prefix for later filtering
        scenmatde = sim1.scenario[scen].material[mat].matdataOut_e.loc[0:30].add_prefix(str(scen+'_'+mat+'_'))
        #concat into one large df
        energy_mat = pd.concat([energy_mat, scenmatde], axis=1)

energy_mat.tail()


# In[120]:


allenergy = pd.concat([energy_mod,energy_mat], axis=1)
allenergy.index=idx_temp


# ## Graphing Energy Generation

# In[121]:


energyGen = allenergy.filter(like='e_out_annual')


# In[122]:


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


# In[70]:


energyGen_p = energyGen.filter(like='_p')/1e12
energyGen_a = energyGen.filter(like='_a')/1e12


# In[103]:


#plt.plot(energyGen_p)#, color=['#006fa2','#ee005b','#734296'])
plt.plot(energyGen_p.index, energyGen_p.iloc[:,[0]], color='#0079C2')
plt.plot(energyGen_p.index, energyGen_p.iloc[:,[1]], color='#F7A11A', ls='--')
plt.plot(energyGen_p.index, energyGen_p.iloc[:,[2]], color='#5D9732', ls='-.')
plt.legend(scennames_p)
plt.title('Identical Power Installed: Annual Energy Generation')
plt.ylabel('Energy Generated [TWh]')


# In[104]:


#plt.plot(energyGen_p)#, color=['#006fa2','#ee005b','#734296'])
plt.plot(energyGen_a.index, energyGen_a.iloc[:,[0]], color='#0079C2')
plt.plot(energyGen_a.index, energyGen_a.iloc[:,[1]], color='#F7A11A', ls='--')
plt.plot(energyGen_a.index, energyGen_a.iloc[:,[2]], color='#5D9732', ls='-.')
plt.legend(scennames_a)
plt.title('Identical Area Installed: Annual Energy Generation')
plt.ylabel('Energy Generated [TWh]')


# Or as a bar plot

# In[108]:


energyGen_cum = energyGen.cumsum()
energyGen_cum_2050 = energyGen_cum.loc[[2050]]
energyGen_cum_2050/1e12
energyGen_cum_2050.columns = scennames
energyGen_cum_2050


# In[109]:


plt.bar(energyGen_cum_2050.columns, energyGen_cum_2050.loc[2050]/1e12, tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Energy Generated Cumulatively by Scenario')
plt.ylabel('[TWh]')


# In[110]:


energyGen_cum_2050_norm = energyGen_cum_2050/energyGen_cum_2050.loc[2050,'PERC_a']
plt.bar(energyGen_cum_2050_norm.columns, energyGen_cum_2050_norm.loc[2050], tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Energy Generated Cumulatively by Scenario - Normalized to PERC')
plt.ylabel('[TWh]')


# In[111]:


energyGen_cum_2050_norm


# ## Energy vs Silver Demand

# In[114]:


energyGen_cum_2050.columns=silver_demand_cum.columns=scennames
whpag = (energyGen_cum_2050)/silver_demand_cum #Wh generated cumulative, per silver demand
normalizer = whpag.loc[2050,'PERC_a']
whpag/normalizer


# In[117]:


plt.bar(whpag.columns, whpag.loc[2050]/1e12, tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Energy Generated Cumulatively per Silver Demand Tonnes')
plt.ylabel('[TWh/tonnes]')


# In[115]:


energyGen_cum_2050.columns=silver_demand_cum.columns=scennames
agpwh= silver_demand_cum/(energyGen_cum_2050) #Wh generated cumulative, per silver demand
normalizer = agpwh.loc[2050,'PERC_a']
agpwh_norm = agpwh/normalizer
agpwh_norm


# In[116]:


plt.bar(agpwh_norm.columns, agpwh_norm.loc[2050], tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Silver Demand Tonnes per energy generation, normalized')
plt.ylabel('[tonnes/TWh] Normalized')


# ## Net Energy Calcs

# In[159]:


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


# In[162]:


#select the non energy generation columns for all scenarios
energy_demands = allenergy.loc[:,~allenergy.columns.isin(energyGen.columns)] 
edemand_perc_p = energy_demands.filter(like='PERC_p')
edemand_shj_p = energy_demands.filter(like='SHJ_p')
edemand_topcon_p = energy_demands.filter(like='TOPCon_p')
edemand_perc_a = energy_demands.filter(like='PERC_a')
edemand_shj_a = energy_demands.filter(like='SHJ_a')
edemand_topcon_a = energy_demands.filter(like='TOPCon_a')


# In[169]:


#for each scenario, create a cumulative total energy demand
for scen in scennames:
    colname = str(scen+'_e_demand_total')
    energy_demands[colname] = energy_demands.filter(like=scen).sum(axis=1)


# In[193]:


energy_demands_annual = energy_demands.filter(like='e_demand_total')
yrlyedemand_perc_p = energy_demands_annual.filter(like='PERC_p')
yrlyedemand_shj_p = energy_demands_annual.filter(like='SHJ_p')
yrlyedemand_topcon_p = energy_demands_annual.filter(like='TOPCon_p')
yrlyedemand_perc_a = energy_demands_annual.filter(like='PERC_a')
yrlyedemand_shj_a = energy_demands_annual.filter(like='SHJ_a')
yrlyedemand_topcon_a = energy_demands_annual.filter(like='TOPCon_a')


# In[200]:


#plt.plot(energy_demands_annual)
plt.plot(yrlyedemand_perc_p.index, yrlyedemand_perc_p/1e12, color='#0079C2')
plt.plot(yrlyedemand_shj_p.index, yrlyedemand_shj_p/1e12, color='#F7A11A', ls='--')
plt.plot(yrlyedemand_topcon_p.index, yrlyedemand_topcon_p/1e12, color='#5D9732', ls='-.')
plt.legend(scennames_p)
plt.title('Identical Power Installed: Annual Energy Demands for Manufacturing')
plt.ylabel('Energy Demand [TWh]')


# In[177]:


energy_demand_total_cum = energy_demands.filter(like='e_demand_total').cumsum()
energy_demand_total_cum_2050 = energy_demand_total_cum.loc[[2050]]
energy_demand_total_cum_2050.columns = scennames


# In[184]:


energy_demand_total_cum_2050/1e12


# In[188]:


energy_demand_total_cum_2050/energy_demand_total_cum_2050.loc[2050,'PERC_p']


# In[187]:


plt.bar(energy_demand_total_cum_2050.columns, energy_demand_total_cum_2050.loc[2050]/1e12, tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Cumulative Energy Demand 2020-2050')
plt.ylabel('[TWh]')


# In[185]:


energyGen_cum_2050/1e12


# ## Net Energy

# In[189]:


net_energy_cum_2050 = (energyGen_cum_2050-energy_demand_total_cum_2050)/1e12
net_energy_cum_2050


# In[181]:


plt.bar(net_energy_cum_2050.columns, net_energy_cum_2050.loc[2050], tick_label=(scennames), color=['#0079C2','#F7A11A','#5D9732'])
plt.title('Net Energy Cumulatively 2020-2050')
plt.ylabel('[TWh]')


# In[214]:


energyGen.columns = energy_demands_annual.columns = scennames
netEnergyAnnual_TWh = (energyGen - energy_demands_annual)/1e12


# In[231]:


round(netEnergyAnnual_TWh,0)


# In[230]:


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





# In[ ]:


def aggregateEnergyResults(self, scenarios=None, materials=None):
        if scenarios is None:
        scenarios = list(self.scenario.keys())
    else:
        if isinstance(scenarios, str):
            scenarios = [scenarios]

    if materials is None:
        materials = list(self.scenario[scenarios[0]].material.keys())
    else:
        if isinstance(materials, str):
            materials = [materials]
    #categorize the energy in values into lifecycle stages
    mfg_energies = ['mod_MFG','mat_extraction','mat_MFG_virgin']
    mfg_recycle_energies_LQ = ['mat_MFGScrap_LQ'] #LQ and HQ are separate becuase LQ is only LQ
    mfg_recycle_energies_HQ = ['mat_MFGScrap_HQ'] #and HQ material is E_LQ + E_HQ
    use_energies = ['mod_Install','mod_OandM','mod_Repair']
    eol_energies = ['mat_Landfill','mod_Demount','mod_Store','mod_Resell_Certify']
    eol_remfg_energies = ['mod_ReMFG_Disassmbly','mat_EoL_ReMFG_clean']
    eol_recycle_energies_LQ = ['mod_Recycle_Crush','mat_Recycled_LQ']
    eol_recycle_energies_HQ = ['mod_Recycle_Crush','mat_Recycled_HQ']
    
    


# In[ ]:


#categorize the energy in values into lifecycle stages
mfg_energies = ['mod_MFG','mat_extraction','mat_MFG_virgin']
mfg_recycle_energies_LQ = ['mat_MFGScrap_LQ'] #LQ and HQ are separate becuase LQ is only LQ
mfg_recycle_energies_HQ = ['mat_MFGScrap_HQ'] #and HQ material is E_LQ + E_HQ
use_energies = ['mod_Install','mod_OandM','mod_Repair']
eol_energies = ['mat_Landfill','mod_Demount','mod_Store','mod_Resell_Certify']
eol_remfg_energies = ['mod_ReMFG_Disassmbly','mat_EoL_ReMFG_clean']
eol_recycle_energies_LQ = ['mod_Recycle_Crush','mat_Recycled_LQ']
eol_recycle_energies_HQ = ['mod_Recycle_Crush','mat_Recycled_HQ']

