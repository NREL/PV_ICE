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


plt.plot(modeffs, label=modeffs.columns)
plt.legend()
plt.title('Module Efficiency over Time')
plt.ylabel('Module Efficiency [%]')


# In[14]:


plt.plot(Aguse, label=Aguse.columns)
plt.legend()
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


scennames = ['PERC','SHJ','TOPCon'] #add later Blend and bifi on/off
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
    sim1.scenario[scen].dataIn_m.loc[0:len(modeffs.index-1),'mod_eff'] = modeffs[scen].values


# In[40]:


#glass modify
for scen in scennames:
    sim1.scenario[scen].material['glass'].matdataIn_m['mat_massperm2'] = glassperm2


# In[41]:


#silver modify
#Aguse
for scen in scennames:
    sim1.scenario[scen].material['silver'].matdataIn_m.loc[0:len(Aguse.index-1),'mat_massperm2'] = Aguse[scen].values


# In[42]:


sim1.scenario['PERC'].dataIn_m.head()


# In[43]:


sim1.scenario['SHJ'].material['silver'].matdataIn_m.head()


# # Run Simulations

# In[44]:


scennames
bifi_perc_path
bifi_shj_path 
bifi_topcon_path
bifipaths = [bifi_perc_path,bifi_shj_path,bifi_topcon_path]
bifipaths[0]


# In[45]:


#simple area deploy list to test new feature
idx_temp = Aguse.index
area_deploy = pd.DataFrame(index=idx_temp, dtype=float)
area_deploy['Area'] = 100.0
type(area_deploy)


# In[46]:


list(area_deploy['Area'])


# In[47]:


list()


# In[48]:


#option 1, install identical power
sim1.calculateFlows(scenarios='PERC', bifacialityfactors=bifi_perc_path, installByArea=list(area_deploy['Area']))
sim1.calculateFlows(scenarios='SHJ', bifacialityfactors=bifi_shj_path,  installByArea=list(area_deploy['Area']))
sim1.calculateFlows(scenarios='TOPCon', bifacialityfactors=bifi_topcon_path,  installByArea=list(area_deploy['Area']))

perc_yearly, perc_cum = sim1.aggregateResults(scenarios='PERC')
shj_yearly, shj_cum = sim1.aggregateResults(scenarios='SHJ')
topcon_yearly, topcon_cum = sim1.aggregateResults(scenarios='TOPCon')


# In[49]:


sim1.scenario['TOPCon'].dataOut_m.head()


# In[62]:


plt.plot(sim1.scenario['PERC'].dataIn_m['year'], sim1.scenario['PERC'].dataOut_m['Installed_Capacity_[W]'])
plt.plot(sim1.scenario['PERC'].dataIn_m['year'], sim1.scenario['SHJ'].dataOut_m['Installed_Capacity_[W]'])
plt.plot(sim1.scenario['PERC'].dataIn_m['year'], sim1.scenario['TOPCon'].dataOut_m['Installed_Capacity_[W]'])
plt.title('Installed Capacity [W]')
plt.legend(['PERC','SHJ','TOPCon'])


# In[51]:


sim1.plotMaterialComparisonAcrossScenarios(keyword='mat_Virgin_Stock', material='silver')


# In[52]:


plt.plot(sim1.scenario['TOPCon'].dataIn_m['year'],sim1.scenario['PERC'].dataOut_m['Cumulative_Active_Area'])
plt.plot(sim1.scenario['TOPCon'].dataIn_m['year'],sim1.scenario['SHJ'].dataOut_m['Cumulative_Active_Area'])
plt.plot(sim1.scenario['TOPCon'].dataIn_m['year'],sim1.scenario['TOPCon'].dataOut_m['Cumulative_Active_Area'])
plt.title('Active Area')
plt.legend(['PERC','SHJ','TOPCon'])


# In[53]:


sim1.scenario['PERC'].dataOut_m['irradiance_stc'].head()


# In[54]:


plt.plot(sim1.scenario['PERC'].dataIn_m['year'], sim1.scenario['PERC'].dataOut_m['Yearly_Sum_Area_disposed'])
plt.plot(sim1.scenario['PERC'].dataIn_m['year'], sim1.scenario['SHJ'].dataOut_m['Yearly_Sum_Area_disposed'])
plt.plot(sim1.scenario['PERC'].dataIn_m['year'], sim1.scenario['TOPCon'].dataOut_m['Yearly_Sum_Area_disposed'])
plt.title('Yearly Sum of Area Disposed')
plt.legend(['PERC','SHJ','TOPCon'])


# In[60]:


sim1.scenario['PERC'].dataOut_m.head()


# In[56]:


#pulling out energy generation results
#the index location is a temp fix due to having extra lenght index, likely due to empty material energy files
perc_energyGen_annual = sim1.scenario['PERC'].dataOut_e.loc[0:30,['e_out_annual_[Wh]']]
shj_energyGen_annual = sim1.scenario['SHJ'].dataOut_e.loc[0:30,['e_out_annual_[Wh]']]
topcon_energyGen_annual = sim1.scenario['TOPCon'].dataOut_e.loc[0:30,['e_out_annual_[Wh]']]
energyGen = pd.concat([perc_energyGen_annual, shj_energyGen_annual, topcon_energyGen_annual],axis=1)
energyGen.index=idx_temp
energyGen.columns = ['PERC','SHJ','TOPCon']


# In[57]:


fig, ax1 = plt.subplots()

ax1.plot(energyGen)
#ax1.set_ylabel('Annual Deployments [MW]', color='blue')

#ax2 = ax1.twinx()
#ax2.plot(sf_reeds['TW_cum'], color='orange')
#ax2.set_ylabel('Cumulative Capacity [TW]', color='orange')

plt.legend(energyGen.columns)
plt.title('Annual Energy Generation')
plt.show()


# In[ ]:


fig, ax1 = plt.subplots()

ax1.plot(energyGen_alt)
#ax1.set_ylabel('Annual Deployments [MW]', color='blue')

#ax2 = ax1.twinx()
#ax2.plot(sf_reeds['TW_cum'], color='orange')
#ax2.set_ylabel('Cumulative Capacity [TW]', color='orange')

plt.legend(energyGen_alt.columns)
plt.title('Annual Energy Generation Alternate Calc')
plt.show()


# In[ ]:


#option 2, compensation for area deployed
#styled on installation compensation
subscens = ['SHJ','TOPCon']

sim1.calculateFlows(scenarios='PERC', bifacialityfactors=bifi_perc_path)

for row in range (0,len(sim1.scenario['PERC'].dataIn_m)):
    for scenario in range (0, len(subscens)):
        scen = list(subscens)[scenario] 
        
        #perc will install the most area because lowest eff and lowest bifi, so compare to PERC
        #bigger number-smaller number = (+)
        perc_area_installed = (sim1.scenario['PERC'].dataIn_m['new_Installed_Capacity_[MW]'][row]*1e6)/(sim1.scenario['PERC'].dataIn_m['mod_eff'][row]*0.01)/1070
                                #installed cap in W / module eff that year / irradiance that year
        scen_area_installed = sim1.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][row]*1e6/(sim1.scenario[scen].dataIn_m['mod_eff'][row]*0.01)/(1000+bifiFactors[scen]*100) #this bifi factor thing only works because it is constant rn
                                #
        delta_install_area = perc_area_installed-scen_area_installed
        
        #Convert area difference into a new installs modficiation
        delta_install_power = (delta_install_area * (1000+bifiFactors[scen]*100)* (sim1.scenario[scen].dataIn_m['mod_eff'][row]*0.01))/1000000 #MW
        
        #update the new installations to compensate for area deployed
        sim1.scenario[scen].dataIn_m['new_Installed_Capacity_[MW]'][row] -= delta_install_power #subtracting installs
        
    sim1.calculateFlows(bifacialityfactors=bifipaths[scenario])




# In[ ]:


sim1_yearly, sim1_cum = sim1.aggregateResults()


# In[ ]:


plt.plot(sim1.scenario['PERC'].dataIn_m['year'], sim1.scenario['PERC'].dataOut_m['Installed_Capacity_[W]'])
plt.plot(sim1.scenario['PERC'].dataIn_m['year'], sim1.scenario['SHJ'].dataOut_m['Installed_Capacity_[W]'])
plt.plot(sim1.scenario['PERC'].dataIn_m['year'], sim1.scenario['TOPCon'].dataOut_m['Installed_Capacity_[W]'])
plt.title('Installed Capacity [W]')


# In[ ]:


sim1.plotMetricResults()


# In[ ]:


sim1.plotMaterialComparisonAcrossScenarios(keyword='mat_Virgin_Stock', material='silver')


# In[ ]:


plt.plot(sim1.scenario['TOPCon'].dataIn_m['year'],sim1.scenario['PERC'].dataOut_m['Area'])
plt.plot(sim1.scenario['TOPCon'].dataIn_m['year'],sim1.scenario['SHJ'].dataOut_m['Area'])
plt.plot(sim1.scenario['TOPCon'].dataIn_m['year'],sim1.scenario['TOPCon'].dataOut_m['Area'])
plt.title('Active Area')
plt.legend(['PERC','SHJ','TOPCon'])


# In[ ]:


#pulling out energy generation results
#the index location is a temp fix due to having extra lenght index, likely due to empty material energy files
perc_energyGen_annual = sim1.scenario['PERC'].dataOut_e.loc[0:30,['e_out_annual_[Wh]']]
shj_energyGen_annual = sim1.scenario['SHJ'].dataOut_e.loc[0:30,['e_out_annual_[Wh]']]
topcon_energyGen_annual = sim1.scenario['TOPCon'].dataOut_e.loc[0:30,['e_out_annual_[Wh]']]
energyGen = pd.concat([perc_energyGen_annual, shj_energyGen_annual, topcon_energyGen_annual],axis=1)
energyGen.index=idx_temp
energyGen.columns = ['PERC','SHJ','TOPCon']


# In[ ]:


fig, ax1 = plt.subplots()

ax1.plot(energyGen)
#ax1.set_ylabel('Annual Deployments [MW]', color='blue')

#ax2 = ax1.twinx()
#ax2.plot(sf_reeds['TW_cum'], color='orange')
#ax2.set_ylabel('Cumulative Capacity [TW]', color='orange')

plt.legend(energyGen.columns)
plt.title('Annual Energy Generation')
plt.show()


# PROBLEMS:
# - Not deploying the same area - deploying the same power
# - Bifi constants --> create irradiance change --> decreasing the annual energy generation - which seems wrong

# In[ ]:


sim1.scenario['TOPCon'].dataIn_m


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

