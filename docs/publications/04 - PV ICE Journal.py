#!/usr/bin/env python
# coding: utf-8

# # 11 - PV ICE Journal: PV in the Circular Economy, A Dynamic Framework Analyzing Technology Evolution and Reliability Impacts

# In[1]:


import PV_ICE
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np
import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'ElectricFutures')
print ("Your simulation will be stored in %s" % testfolder)



# In[2]:


PV_ICE.__version__


# In[3]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[4]:


MATERIALS = ['glass','silver','silicon', 'copper','aluminium_frames', 'backsheet', 'encapsulant']
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'..\..\baselines\ElectrificationFutures_2021\baseline_modules_US_NREL_Electrification_Futures_2021_basecase.csv'
MODULEBASELINE_High = r'..\..\baselines\ElectrificationFutures_2021\baseline_modules_US_NREL_Electrification_Futures_2021_LowREHighElec.csv'


# In[5]:


r1 = PV_ICE.Simulation(name='PV_ICE', path=testfolder)
r1.createScenario(name='base', file=MODULEBASELINE)
r1.createScenario(name='high', file=MODULEBASELINE_High)

r1.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r1.scenario['high'].addMaterials(MATERIALS, r'..\..\baselines')


# In[6]:


r2 = PV_ICE.Simulation(name='bifacialTrend', path=testfolder)
r2.createScenario(name='base', file=MODULEBASELINE)
r2.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')

r2.createScenario(name='high', file=MODULEBASELINE_High)
r2.scenario['high'].addMaterials(MATERIALS, r'..\..\baselines')


# Rewriting with bifacial ones
MATERIALBASELINE = r'..\..\baselines\PVSC_2021\baseline_material_glass_bifacialTrend.csv'
r2.scenario['base'].addMaterial('glass', file=MATERIALBASELINE)
MATERIALBASELINE = r'..\..\baselines\PVSC_2021\baseline_material_aluminium_frames_bifacialTrend.csv'
r2.scenario['base'].addMaterial('aluminium_frames', file=MATERIALBASELINE)

MATERIALBASELINE = r'..\..\baselines\PVSC_2021\baseline_material_glass_bifacialTrend.csv'
r2.scenario['high'].addMaterial('glass', file=MATERIALBASELINE)
MATERIALBASELINE = r'..\..\baselines\PVSC_2021\baseline_material_aluminium_frames_bifacialTrend.csv'
r2.scenario['high'].addMaterial('aluminium_frames', file=MATERIALBASELINE)



# In[7]:


r3 = PV_ICE.Simulation(name='Irena_EL', path=testfolder)
r3.createScenario(name='base', file=MODULEBASELINE)
r3.createScenario(name='high', file=MODULEBASELINE_High)
r3.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r3.scenario['high'].addMaterials(MATERIALS, r'..\..\baselines')

r3.scenMod_IRENIFY(scenarios=['base', 'high'], ELorRL = 'EL' )


# In[8]:


r4 = PV_ICE.Simulation(name='Irena_RL', path=testfolder)
r4.createScenario(name='base', file=MODULEBASELINE)
r4.createScenario(name='high', file=MODULEBASELINE_High)
r4.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r4.scenario['high'].addMaterials(MATERIALS, r'..\..\baselines')

r4.scenMod_IRENIFY(scenarios=['base', 'high'], ELorRL = 'RL' )


# In[9]:


r1.calculateMassFlow()
r2.calculateMassFlow()
r3.calculateMassFlow()
r4.calculateMassFlow()


# # Compile Results

# In[10]:


objects = [r1, r2, r3, r4]
scenarios = ['base', 'high']


# In[11]:


pvice_Usyearly1, pvice_Uscum1 = r1.aggregateResults()
pvice_Usyearly2, pvice_Uscum2 = r2.aggregateResults()
pvice_Usyearly3, pvice_Uscum3 = r3.aggregateResults()
pvice_Usyearly4, pvice_Uscum4 = r4.aggregateResults()
UScum = pd.concat([pvice_Uscum1, pvice_Uscum2, pvice_Uscum3, pvice_Uscum4], axis=1)
USyearly = pd.concat([pvice_Usyearly1, pvice_Usyearly2, pvice_Usyearly3, pvice_Usyearly4], axis=1)

UScum.to_csv('pvice_USCum.csv')
USyearly.to_csv('pvice_USYearly.csv')


# # Fig 10 - Virgin Needs, Eol Waste and MFG Waste

# In[12]:


materials = ['glass', 'aluminium_frames', 'silicon', 'copper', 'silver', 'encapsulant', 'backsheet']
modulemat = 'Module'

mytitlefont = 18
mylegendfont = 14
plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = (15, 20.2)


f, a0 = plt.subplots(3, 2, gridspec_kw={'width_ratios': [3.5,1.5], 'wspace':0.15, 'hspace':0.3})

########################    
# SUBPLOT 1
########################
#######################
   
# Loop over CASES
name4 = 'Irena_RL_high_[Tonnes]'
name3 = 'Irena_EL_high_[Tonnes]'
name2 = 'PV_ICE_high_[Tonnes]'
name1 = 'PV_ICE_base_[Tonnes]'


# SCENARIO 1 ***************
keyw='VirginStock_'
a0[0,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name1]/1000000, 'k', linestyle='dotted', linewidth=4, label='S1: PV ICE, ref')
a0[0,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name2]/1000000, 'c', linewidth=3, label='S2: PV ICE, h.e.')
a0[0,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name3]/1000000, 'g', linestyle='dashdot', linewidth=3, label='S3: IRENA, Early Loss, h.e.')
a0[0,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name4]/1000000, 'b--', linewidth=3, label='S4: IRENA, Regular Loss, h.e.')

a0[0,0].legend(prop={'size': mylegendfont})
a0[0,0].set_title('Yearly Virgin Material Needs by Scenario', fontsize=mytitlefont, weight='roman')
a0[0,0].set_ylabel('Module Mass [Million Tonnes]')
a0[0,0].set_xlim([2020, 2050])
a0[0,0].set_xlabel('Years')
a0[0,0].minorticks_on()
a0[0,0].text(-0.1, 1.05, 'a', transform=a0[0,0].transAxes, size=20, weight='bold')

########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name1].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name3].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name4].loc[2050])

    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']
dfcumulations2050['bottom5'] = dfcumulations2050['bottom4']+dfcumulations2050['silver']
dfcumulations2050['bottom6'] = dfcumulations2050['bottom5']+dfcumulations2050['encapsulant']



## Plot BARS Stuff
ind=np.arange(4)
width=0.35 # width of the bars.
p0 = a0[0,1].bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a0[0,1].bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a0[0,1].bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a0[0,1].bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a0[0,1].bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])
p5 = a0[0,1].bar(ind, dfcumulations2050['encapsulant'], width,
             bottom=dfcumulations2050['bottom5'])
p6 = a0[0,1].bar(ind, dfcumulations2050['backsheet'], width,
             bottom=dfcumulations2050['bottom6'])

a0[0,1].yaxis.set_label_position("right")
a0[0,1].yaxis.tick_right()
a0[0,1].set_ylabel('Cumulative Virgin Material Needs\n2020-2050 [Million Tonnes]')
a0[0,1].set_xlabel('Scenario')

print("Cumulative Virgin Needs by 2050 Million Tones by Scenario")
print(dfcumulations2050[materials].sum(axis=1))

plt.sca(a0[0,1])
plt.xticks(range(4), ['S1', 'S2', 'S3', 'S4'], color='black', rotation=0)
plt.tick_params(axis='y', which='minor', bottom=False)
#plt.yticks(minor=True)
a0[0,1].legend((p6[0], p5[0], p4[0], p3[0], p2[0], p1[0], p0[0] ), ('Backsheet',  'Encapsulant', 'Silver', 'Copper', 
                                                                    'Silicon','Aluminum','Glass'), loc='lower right', prop={'size': mylegendfont})
a0[0,1].minorticks_on()
             



#################################
# ROW 2
################################

# SCENARIO 1 ***************
keyw='WasteEOL_'
a0[1,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name1]/1000000, 'k', linestyle='dotted', linewidth=4, label='S1: PV ICE, ref')
a0[1,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name2]/1000000, 'c', linewidth=3, label='S2: PV ICE, h.e.')
a0[1,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name3]/1000000, 'g', linestyle='dashdot', linewidth=3, label='S3: IRENA, Early Loss, h.e.')
a0[1,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name4]/1000000, 'b--', linewidth=3, label='S4: IRENA, Regular Loss, h.e.')

a0[1,0].legend(prop={'size': mylegendfont})
a0[1,0].set_title('Yearly EoL Material by Scenario', fontsize=mytitlefont, weight='roman')
a0[1,0].set_ylabel('Module Mass [Million Tonnes]')
a0[1,0].set_xlim([2020, 2050])
a0[1,0].set_xlabel('Years')
a0[1,0].minorticks_on()
a0[0,0].text(-0.1, 1.05, 'b', transform=a0[1,0].transAxes, size=20, weight='bold')

########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name1].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name3].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name4].loc[2050])

    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']
dfcumulations2050['bottom5'] = dfcumulations2050['bottom4']+dfcumulations2050['silver']
dfcumulations2050['bottom6'] = dfcumulations2050['bottom5']+dfcumulations2050['encapsulant']



## Plot BARS Stuff
ind=np.arange(4)
width=0.35 # width of the bars.
p0 = a0[1,1].bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a0[1,1].bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a0[1,1].bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a0[1,1].bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a0[1,1].bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])
p5 = a0[1,1].bar(ind, dfcumulations2050['encapsulant'], width,
             bottom=dfcumulations2050['bottom5'])
p6 = a0[1,1].bar(ind, dfcumulations2050['backsheet'], width,
             bottom=dfcumulations2050['bottom6'])

a0[1,1].yaxis.set_label_position("right")
a0[1,1].yaxis.tick_right()
a0[1,1].set_ylabel('Cumulative EoL Material\n2020-2050 [Million Tonnes]')
a0[1,1].set_xlabel('Scenario')

print("Cumulative Virgin Needs by 2050 Million Tones by Scenario")
print(dfcumulations2050[materials].sum(axis=1))

plt.sca(a0[1,1])
plt.xticks(range(4), ['S1', 'S2', 'S3', 'S4'], color='black', rotation=0)
plt.tick_params(axis='y', which='minor', bottom=False)
#plt.yticks(minor=True)
a0[1,1].legend((p6[0], p5[0], p4[0], p3[0], p2[0], p1[0], p0[0] ), ('Backsheet',  'Encapsulant', 'Silver', 'Copper', 
                                                                    'Silicon','Aluminum','Glass'), loc='upper left', prop={'size': mylegendfont})
a0[1,1].minorticks_on()
             




#################################
# ROW 3
################################

# SCENARIO 1 ***************
keyw='WasteMFG_'
a0[2,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name1]/1000000, 'k.', linestyle='dotted', linewidth=4, label='S1: PV ICE, ref')
a0[2,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name2]/1000000, 'c', linewidth=3, label='S2: PV ICE, h.e.')
a0[2,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name3]/1000000, 'g', linestyle='dashdot', linewidth=3, label='S3: IRENA, Early Loss, h.e.')
a0[2,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name4]/1000000, 'b--', linewidth=3, label='S4: IRENA, Regular Loss, h.e.')

a0[2,0].legend(prop={'size': mylegendfont})
a0[2,0].set_title('Yearly Manufacturing Scrap by Scenario', fontsize=mytitlefont, weight='roman')
a0[2,0].set_ylabel('Module Mass [Million Tonnes]')
a0[2,0].set_xlim([2020, 2050])
a0[2,0].set_xlabel('Years')
a0[2,0].minorticks_on()
a0[0,0].text(-0.1, 1.05, 'c', transform=a0[2,0].transAxes, size=20, weight='bold')

########################    
# SUBPLOT 2
########################
#######################
# Calculate    

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name1].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name3].loc[2050])
    matcum.append(UScum[keyw+materials[ii]+'_'+name4].loc[2050])

    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes

dfcumulations2050['bottom1'] = dfcumulations2050['glass']
dfcumulations2050['bottom2'] = dfcumulations2050['bottom1']+dfcumulations2050['aluminium_frames']
dfcumulations2050['bottom3'] = dfcumulations2050['bottom2']+dfcumulations2050['silicon']
dfcumulations2050['bottom4'] = dfcumulations2050['bottom3']+dfcumulations2050['copper']
dfcumulations2050['bottom5'] = dfcumulations2050['bottom4']+dfcumulations2050['silver']
dfcumulations2050['bottom6'] = dfcumulations2050['bottom5']+dfcumulations2050['encapsulant']



## Plot BARS Stuff
ind=np.arange(4)
width=0.35 # width of the bars.
p0 = a0[2,1].bar(ind, dfcumulations2050['glass'], width, color='c')
p1 = a0[2,1].bar(ind, dfcumulations2050['aluminium_frames'], width,
             bottom=dfcumulations2050['bottom1'])
p2 = a0[2,1].bar(ind, dfcumulations2050['silicon'], width,
             bottom=dfcumulations2050['bottom2'])
p3 = a0[2,1].bar(ind, dfcumulations2050['copper'], width,
             bottom=dfcumulations2050['bottom3'])
p4 = a0[2,1].bar(ind, dfcumulations2050['silver'], width,
             bottom=dfcumulations2050['bottom4'])
p5 = a0[2,1].bar(ind, dfcumulations2050['encapsulant'], width,
             bottom=dfcumulations2050['bottom5'])
p6 = a0[2,1].bar(ind, dfcumulations2050['backsheet'], width,
             bottom=dfcumulations2050['bottom6'])

a0[2,1].yaxis.set_label_position("right")
a0[2,1].yaxis.tick_right()
a0[2,1].set_ylabel('Cumulative Manufacturing Scrap\n2020-2050 [Million Tonnes]')
a0[2,1].set_xlabel('Scenario')

plt.sca(a0[2,1])
plt.xticks(range(4), ['S1', 'S2', 'S3', 'S4'], color='black', rotation=0)
plt.tick_params(axis='y', which='minor', bottom=False)
#plt.yticks(minor=True)
a0[2,1].legend((p6[0], p5[0], p4[0], p3[0], p2[0], p1[0], p0[0] ), 
               ('Backsheet',  'Encapsulant', 'Silver', 'Copper', 'Silicon','Aluminum','Glass'), loc='lower right',
              prop={'size': mylegendfont})
a0[2,1].minorticks_on()
             
    
    
f.tight_layout()

f.savefig(os.path.join(testfolder,'Fig 10 - Three-panels of Virgin Needs, EoL Material and MFG Waste.png'), dpi=600)
f.savefig(os.path.join(testfolder,'Fig 10 - Three-panels of Virgin Needs, EoL Material and MFG Waste.pdf'), dpi=600)

print("Cumulative Virgin Needs by 2050 Million Tones by Scenario")
print(dfcumulations2050[materials].sum(axis=1))


# # Abstract Values

# In[13]:


print("Percentage of Waste represented by Manufacturing") 
print("Reference: ", UScum['WasteMFG_Module_PV_ICE_base_[Tonnes]'].loc[2050]*100/UScum['WasteAll_Module_PV_ICE_base_[Tonnes]'].loc[2050])
print("H.E.: ", UScum['WasteMFG_Module_PV_ICE_high_[Tonnes]'].loc[2050]*100/UScum['WasteAll_Module_PV_ICE_high_[Tonnes]'].loc[2050])
print("Waste in 2050 ref ",UScum['WasteAll_Module_PV_ICE_base_[Tonnes]'].loc[2050]/1e6, "h.e. : ",UScum['WasteAll_Module_PV_ICE_high_[Tonnes]'].loc[2050]/1e6 )

print("")
print("Installed Capacity 2050", round(USyearly['Capacity_PV_ICE_base_[MW]'].loc[2050]/1e6,1), 'h.e.', round(USyearly['Capacity_PV_ICE_high_[MW]'].loc[2050]/1e6,1))


# # TABLE 7: METRIC TONNES IN FIELD IN 2030

# In[14]:


names = ['PV_ICE_base', 'PV_ICE_high', 'Irena_EL_base', 'Irena_EL_high', 'Irena_RL_base', 'Irena_RL_high']
materials = ['Module', 'glass', 'encapsulant', 'backsheet', 'aluminium_frames', 'copper', 'silicon', 'silver']


# In[15]:


print("TABLE 7 - METRIC TONNES IN FIELD IN 2030")

tableapp=[]
for name in names:
    colapp=[]
    for mat in materials:
         colapp.append(round((UScum.filter(regex='VirginStock_'+mat+'_'+name).loc[2030][0]-
                       UScum.filter(regex='WasteAll_'+mat+'_'+name).loc[2030][0])/1000,0)*1000)
    tableapp.append(colapp)
    
df= pd.DataFrame(tableapp, columns = materials, index=names)
df = df.T
df


# In[16]:


print("Table 7 Effective Capacity PV ICE, Reference", round(USyearly['Capacity_PV_ICE_base_[MW]'].loc[2030]/1000,1))
print("Table 7 Effective Capacity PV ICE, Reference", round(USyearly['Capacity_PV_ICE_high_[MW]'].loc[2030]/1000,1))


# # Figure 12 Cumulative EOL MAterial, 2016, 2020, 2030, 2040, 2050

# In[17]:


names = ['Irena_EL_base', 'Irena_RL_base', 'PV_ICE_base']


# In[18]:


pd.options.display.float_format = '{:20,.2f}'.format


# In[19]:


print("Figure 12 - Cumulative EOL Material 2016, 2020, 2030, 240, 2050")

years = [2016, 2020, 2030, 2040, 2050]
tableapp=[]
for name in names:
    colapp=[]
    for year in years:
         colapp.append(round(UScum.filter(regex='WasteEOL_Module_'+name).loc[year][0]/1000,0)*1000)
    tableapp.append(colapp)
    
df= pd.DataFrame(tableapp, columns = years, index=names)
df = df.T 
df


# In[20]:


df.insert(loc=0, column='Irena 2016 Early Loss', value=[24000, 85000, 1000000, 4000000, 10000000])
df.insert(loc=1, column='Irena 2016 Regular Loss', value=[6500, 13000, 170000, 1700000, 7500000])
df.insert(loc=2, column='CSA 2020 Early Loss', value=[0, 0, 1200000, 0, 0])
df.insert(loc=3, column='CSA 2020 Regular Loss', value=[0, 0, 214900, 0, 0])


# In[21]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (10, 6)


my_colors=[(0.74609375, 0.5625, 0),
(0.99609375, 0.75, 0),
(0.09375, 0.9375, 0.91796875),
(0.71875, 0.9765625, 0.96875),
(0.0390625, 0.6015625, 0.58984375),
(0.35546875, 0.60546875, 0.83203125),
(0.61328125, 0.76171875, 0.8984375)]

my_colors=[(0.74609375, 0.5625, 0),
(0.99609375, 0.75, 0),  
(0.796875, 0.97265625, 0),
(0, 0.7265625, 0),
(0, 0.640625, 0.73046875),
(0.02734375, 0.02734375, 0.73046875),
(0, 0, 0)]

ax = df.plot(kind='bar', edgecolor='white', linewidth=1, width=0.65, color=my_colors)# width=0.5)
# Some optiosn that Silvana liked: vlag_r, viridis, tab20b, tab10_r, rainbow_r, plasma, nipy_spectral_r
#ax = df.plot(kind='bar', edgecolor='white', linewidth=1, width=0.65, colormap='nipy_spectral_r') #color=my_colors)# width=0.5)


ax.set_yscale('log')
ax.grid(axis='y')
ax.set_axisbelow(b=True) # Set grid behind plots
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
ax.set_xticklabels(df.index, rotation = 0)
ax.set_ylabel('Cumulative EoL Materials [metric tons]')
# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.95])

ax.legend(['Irena 2016 Early Loss', 'Irena 2016 Regular Loss', 'CSA 2020 Early Loss', 'CSA 2020 Regular Loss',
          'PV ICE + EF (ref), Early loss', 'PV ICE + EF (ref), Regular loss', 'PV ICE + EF (ref), PV ICE loss'], 
          loc='upper center', bbox_to_anchor=(0.5, 1.38), fancybox=True, shadow=True, ncol=2)

plt.show()

fig = ax.figure
fig.savefig(os.path.join(testfolder,'Fig 12 - Lit_and_PVICE_CumEOL_Comparison_PLOT.png'), dpi=600, bbox_inches='tight')
fig.savefig(os.path.join(testfolder,'Fig 12 - Lit_and_PVICE_CumEOL_Comparison_PLOT.pdf'), dpi=600, bbox_inches='tight')


# # Figure 11 Installed Capacity for all Scenarios

# In[22]:


names = ['PV_ICE_base', 'PV_ICE_high', 'Irena_EL_base', 'Irena_EL_high', 'Irena_RL_base', 'Irena_RL_high']


# In[23]:


print("Figure 11 Installed CApacity for all Scenarios")

years = [2030, 2050]
tableapp=[]
for name in names:
    colapp=[]
    for year in years:
         colapp.append(USyearly['Capacity_'+name+'_[MW]'].loc[year])
    tableapp.append(colapp)
    
df= pd.DataFrame(tableapp, columns = years, index=names)
df = df.T 
df


# In[24]:


print("Improvement for PV ICE over Irena RL, ", round(df['PV_ICE_high'].loc[2050]*100/df['Irena_RL_high'].loc[2050]-100,1))
print("Improvement for PV ICE over Irena EL, ", round(df['PV_ICE_high'].loc[2050]*100/df['Irena_EL_high'].loc[2050]-100,1))


# In[25]:


df['PV_ICE_increase_high'] = df['PV_ICE_high']-df['PV_ICE_base']
df['Irena_EL_increase_high'] = df['Irena_EL_high']-df['Irena_EL_base']
df['Irena_RL_increase_high'] = df['Irena_RL_high']-df['Irena_RL_base']
df['Irena 2016'] = [240000, 512000]
df['CSA 2000'] = [437000, 0]
df['inc0'] = [0, 0]


# In[26]:


df


# In[27]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (8, 7)


def plot_clustered_stacked(dfall, labels=None, title="multiple stacked bar plot",  H="/", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      colormap='Pastel2_r',
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1)-0.01)

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)
    axe.set_title(title)

    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

#    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    l1 = axe.legend(h[:n_col], ['Reference', 'High Electrification'], loc='center left')
    print(l[:n_col])
    if labels is not None:
       # print(labels)
#        l2 = plt.legend(n, labels, loc=[1.01, 0.1])
        l2 = plt.legend(n, labels, loc='upper left')#[1.01, 0.1])

    axe.add_artist(l1)
    axe.set_ylabel('Installed Capacity [GW]')
    axe.grid(axis='y')
    axe.set_axisbelow(b=True) # Set grid behind plots
    
    fig = axe.figure
    fig.savefig(os.path.join(testfolder,'Fig 11 - ClusterStack of Literature and Calculated Installed Capacity.png'), dpi=600)
    fig.savefig(os.path.join(testfolder,'Fig 11 - ClusterStack of Literature and Calculated Installed Capacity.pdf'), dpi=600)


    return axe

# create fake dataframes
df1 = df[['Irena_EL_base', 'Irena_EL_increase_high']]/1000
df2 = df[['Irena_RL_base', 'Irena_EL_increase_high']]/1000
df3 = df[['PV_ICE_base', 'PV_ICE_increase_high']]/1000
df4 = df[['Irena 2016', 'inc0']]/1000
df5 = df[['CSA 2000', 'inc0']]/1000
df6 = df[['inc0', 'inc0']]/1000

# Then, just call :
plot_clustered_stacked([df1, df2, df3, df4, df5, df6],["PV ICE, Early Loss", "PV ICE, Regular Loss", "PV ICE, PV ICE loss", "Irena 2016, Regular Loss", "CSA 2020"], title='')




# # Sensitivity Analysis

# In[28]:


MATERIAL = 'glass'

MODULEBASELINE = r'..\..\baselines\baseline_modules_US.csv' 
MATERIALBASELINE = r'..\..\baselines\baseline_material_'+MATERIAL+'.csv'


# In[29]:


s1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
s1.createScenario(name='baseline', file=MODULEBASELINE)
s1.scenario['baseline'].addMaterial(MATERIAL, file=MATERIALBASELINE)


# #### Load Scenarios and Parameters

# In[30]:


ss = pd.read_excel(r'..\..\..\tests\sensitivity_test.xlsx')


# #### Create Scenarios

# In[31]:


for i in range (0, len(ss)):
    stage = ss['stage'][i]
    stage_highname = stage+'_high'
    stage_lowname = stage+'_low'
    
    if ss['Database'][i] == 'material':

        if ss['Modification'][i] == 'single':

            # Create Scenarios
            s1.createScenario(name=stage_highname, file=MODULEBASELINE)
            s1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            s1.createScenario(name=stage_lowname, file=MODULEBASELINE)
            s1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)

            # Modify Values Absolute
            if ss['AbsRel'][i] == 'abs':
                # Modify Values High
                s1.scenario[stage_highname].material[MATERIAL].materialdata[ss['variables'][i]] = s1.scenario[stage_highname].material[MATERIAL].materialdata[ss['variables'][i]] + ss['High'][i]
                s1.scenario[stage_highname].material[MATERIAL].materialdata[ss['variables'][i]][s1.scenario[stage_highname].material[MATERIAL].materialdata[ss['variables'][i]]>100.0] =100.0
                # Modify Values Low
                s1.scenario[stage_lowname].material[MATERIAL].materialdata[ss['variables'][i]] = s1.scenario[stage_lowname].material[MATERIAL].materialdata[ss['variables'][i]] + ss['Low'][i]
                s1.scenario[stage_lowname].material[MATERIAL].materialdata[ss['variables'][i]][s1.scenario[stage_lowname].material[MATERIAL].materialdata[ss['variables'][i]]<0.0] = 0.0

            # Modify Values Relative
            if ss['AbsRel'][i] == 'rel':
                # Modify Values High
                high_change = 1+ss['High'][i]/100.0
                low_change = 1+ss['Low'][i]/100.0
                s1.scenario[stage_highname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(s1.scenario[stage_highname].material[MATERIAL].materialdata, 
                             stage=ss['variables'][i], improvement=high_change, start_year=0)
                # Modify Values Low
                s1.scenario[stage_lowname].material[MATERIAL].materialdata = PV_ICE.sens_StageImprovement(s1.scenario[stage_lowname].material[MATERIAL].materialdata, 
                             stage=ss['variables'][i], improvement=low_change, start_year=0)
          
        # If multiple, assumed all modifications are ABSOLUTE
        if ss['Modification'][i] == 'multiple':
            varmods = [x.strip() for x in ss['variables'][i].split(',')]
            
            # Create Scenarios
            s1.createScenario(name=stage_highname, file=MODULEBASELINE)
            s1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            s1.createScenario(name=stage_lowname, file=MODULEBASELINE)
            s1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            
            for j in range(0, len(varmods)):
                # Modify Values High
                s1.scenario[stage_highname].material[MATERIAL].materialdata[varmods[j]] = s1.scenario[stage_highname].material[MATERIAL].materialdata[varmods[j]] + ss['High'][i] 
                s1.scenario[stage_highname].material[MATERIAL].materialdata[varmods[j]][s1.scenario[stage_highname].material[MATERIAL].materialdata[varmods[j]]>100.0] =100.0
                # Modify Values Low
                s1.scenario[stage_lowname].material[MATERIAL].materialdata[varmods[j]] = s1.scenario[stage_lowname].material[MATERIAL].materialdata[varmods[j]] + ss['Low'][i]
                s1.scenario[stage_lowname].material[MATERIAL].materialdata[varmods[j]][s1.scenario[stage_lowname].material[MATERIAL].materialdata[varmods[j]]<0.0] = 0.0

        
    if ss['Database'][i] == 'module':
        
        
        if ss['Modification'][i] == 'single':

            # Create Scenarios
            s1.createScenario(name=stage_highname, file=MODULEBASELINE)
            s1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            s1.createScenario(name=stage_lowname, file=MODULEBASELINE)
            s1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE) 
            # Modify Values Absolute
            if ss['AbsRel'][i] == 'abs':


                s1.scenario[stage_highname].data[ss['variables'][i]] = s1.scenario[stage_highname].data[ss['variables'][i]] + ss['High'][i]
                s1.scenario[stage_highname].data[ss['variables'][i]][s1.scenario[stage_highname].data[ss['variables'][i]]>100.0] =100.0


                s1.scenario[stage_lowname].data[ss['variables'][i]] = s1.scenario[stage_lowname].data[ss['variables'][i]] + ss['Low'][i]
                s1.scenario[stage_lowname].data[ss['variables'][i]][s1.scenario[stage_lowname].data[ss['variables'][i]]<0.0] = 0.0

            # Modify Values Relative
            if ss['AbsRel'][i] == 'rel':
                high_change = 1+ss['High'][i]/100.0
                low_change = 1+ss['Low'][i]/100.0
                s1.scenario[stage_highname].data = PV_ICE.sens_StageImprovement(s1.scenario[stage_highname].data, 
                                                 stage=ss['variables'][i], improvement=high_change, start_year=0)
                s1.scenario[stage_lowname].data = PV_ICE.sens_StageImprovement(s1.scenario[stage_lowname].data, 
                                                 stage=ss['variables'][i], improvement=low_change, start_year=0)
        
        # If multiple, assumed all modifications are ABSOLUTE
        if ss['Modification'][i] == 'multiple':
            varmods = [x.strip() for x in ss['variables'][i].split(',')]

            s1.createScenario(name=stage_highname, file=MODULEBASELINE)
            s1.scenario[stage_highname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            s1.createScenario(name=stage_lowname, file=MODULEBASELINE)
            s1.scenario[stage_lowname].addMaterial(MATERIAL, file=MATERIALBASELINE)
            
            for j in range(0, len(varmods)):
                s1.scenario[stage_highname].data[varmods[j]] = s1.scenario[stage_highname].data[varmods[j]] + ss['High'][i] 
                s1.scenario[stage_highname].data[varmods[j]][s1.scenario[stage_highname].data[varmods[j]]>100.0] =100.0

                s1.scenario[stage_lowname].data[varmods[j]] = s1.scenario[stage_lowname].data[varmods[j]] + ss['Low'][i]
                s1.scenario[stage_lowname].data[varmods[j]][s1.scenario[stage_lowname].data[varmods[j]]<0.0] = 0.0

        


# # MASS FLOWS

# In[32]:


s1.calculateMassFlow()


# #### Compile Changes

# In[33]:


s1.scenario


# In[34]:


scenarios = list(s1.scenario.keys())


# In[35]:


virginStock_Changes = []
waste_Changes = []
installedCapacity_Changes = []
virginStockRAW_Changes = []

virgin_keyword = 'mat_Virgin_Stock'
waste_keyword = 'mat_Total_Landfilled'
installs_keyword = 'Installed_Capacity_[W]'
viring_raw_keyword = 'mat_Virgin_Stock_Raw'

virginStock_baseline_cum2050 = s1.scenario['baseline'].material[MATERIAL].materialdata[virgin_keyword].sum()
virginStockRAW_baseline_cum2050 = s1.scenario['baseline'].material[MATERIAL].materialdata[viring_raw_keyword].sum()

# Installed Capacity is already cumulative so no need to sum or cumsum.
waste_baseline_cum2050 = s1.scenario['baseline'].material[MATERIAL].materialdata[waste_keyword].sum()
installedCapacity_baselined_2050 = s1.scenario['baseline'].data[installs_keyword].iloc[-1]

for i in range (1, len(scenarios)):
    stage_name = scenarios[i]
    virginStock_Changes.append(round(100*s1.scenario[stage_name].material[MATERIAL].materialdata[virgin_keyword].sum()/virginStock_baseline_cum2050,5)-100)
    virginStockRAW_Changes.append(round(100*s1.scenario[stage_name].material[MATERIAL].materialdata[viring_raw_keyword].sum()/virginStockRAW_baseline_cum2050,5)-100)

    waste_Changes.append(round(100*s1.scenario[stage_name].material[MATERIAL].materialdata[waste_keyword].sum()/waste_baseline_cum2050,5)-100)
    installedCapacity_Changes.append(round(100*s1.scenario[stage_name].data[installs_keyword].iloc[-1]/installedCapacity_baselined_2050,5)-100)


# In[36]:


stages = scenarios[1::] # removing baseline as we want a dataframe with only changes


# In[37]:


df2 = pd.DataFrame(list(zip(virginStock_Changes, virginStockRAW_Changes, waste_Changes, installedCapacity_Changes)), 
               columns=['Virgin Needs Change', 'Virgin Stock Raw Change', 'Waste Change', 'InstalledCapacity Change'],index=stages) 


# In[38]:


variables_description = {'mat_virgin_eff': "Material Virgin Efficiency",
    'mat_massperm2': "Mass per m2",
    'mat_MFG_eff': "Efficiency of Material Use during Module Manufacturing",
    'mat_MFG_scrap_Recycled': "% of Material Scrap from Manufacturing that undergoes Recycling",
    'mat_MFG_scrap_Recycling_eff': "Recycling Efficiency of the Material Scrap",
    'mat_MFG_scrap_Recycling_eff': "% of Recycled Material Scrap that is high quality",
    'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG': "% of high quality Recycled Material Scrap reused for manufacturing",
    'new_Installed_Capacity_[MW]': "New Installed Capacity",
    'mod_eff': "Module Efficiency",
    'mod_EOL_collection_eff': "Collection Efficiency of EoL Modules",
    'mod_EOL_collected_recycled': "% of collected modules that are recycled",
    'mod_Repowering': "% of EOL modules that are repowered",
    'mod_Repairing' : "% of failed modules that undergo repair",
    'mat_EOL_collected_Recycled': "% of times material is chosen to be recycled",
    'mat_EOL_Recycling_eff': "Efficiency of material recycling",
    'mat_EOL_Recycled_into_HQ': "Fraction of recycled material that is high quality",
    'mat_EOL_RecycledHQ_Reused4MFG': "Fraction of high quality recycled material that is reused for manufacturing",
    'EOL_CE_Pathways': "Overall improvement on EoL Circularity Pathways",
    'Reliability_and_CE_Pathways': "Overall improvement on Eol Circularity Pathways + Reliability and Lifetime",
    'mat_EOL_Recycling_Overall_Improvement': "Overall Improvement on EoL Recycling Loop"}


# In[39]:


df2_Pos = df2[['high' in s for s in df2.index]].copy()
df2_Pos.index = df2_Pos.index.str.replace("_high", "")

col_verbose = []

for i in range (0, len(df2_Pos)):
    if df2_Pos.index[i] in variables_description:
        col_verbose.append(variables_description[df2_Pos.index[i]])
    else:
        col_verbose.append("")
        
df2_Pos['Description'] = col_verbose     
df2_Pos = df2_Pos.reset_index()
df2_Pos = df2_Pos.rename(columns={'index':'variable'})
df2_Pos


# In[40]:


df2_Neg = df2[['low' in s for s in df2.index]].copy()
df2_Neg.index = df2_Neg.index.str.replace("_low", "")

col_verbose = []

for i in range (0, len(df2_Neg)):
    if df2_Neg.index[i] in variables_description:
        col_verbose.append(variables_description[df2_Neg.index[i]])
    else:
        col_verbose.append("")

df2_Neg['Description'] = col_verbose
df2_Neg = df2_Neg.reset_index()
df2_Neg = df2_Neg.rename(columns={'index':'variable'})
df2_Neg


# #### Fancy Plot

# ## Figure 14 - The percent improvement (i.e., decrease) in lifecycle waste from varying the most impactful parameters affecting waste in the PV ICE tool. A decrease (larger bars to the left) in lifecycle waste is considered beneficial. The columns 10% indicate in what direction and magnitude the parameter, listed at the left, was varied

# In[41]:


posvals = [0,
           df2_Pos.loc[df2_Pos['variable'] == 'Reliability_and_CE_Pathways']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'reliability']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'mod_MFG_eff']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'new_Installed_Capacity_[MW]']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'mat_massperm2']['Waste Change'].values[0],
           
df2_Pos.loc[df2_Pos['variable'] == 'mat_MFG_eff']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'mod_eff']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'EOL_CE_Pathways']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'mat_MFG_Scrap_Overall_Improvement']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'mod_Repair']['Waste Change'].values[0],

df2_Pos.loc[df2_Pos['variable'] == 'mat_MFG_scrap_Recycling_eff']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'mod_Reuse']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'mat_MFG_scrap_Recycled']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'mod_EOL_collection_eff']['Waste Change'].values[0]]


negvals = [0,
           df2_Neg.loc[df2_Neg['variable'] == 'Reliability_and_CE_Pathways']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'reliability']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'mod_MFG_eff']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'new_Installed_Capacity_[MW]']['Waste Change'].values[0],
df2_Pos.loc[df2_Pos['variable'] == 'mat_massperm2']['Waste Change'].values[0],

df2_Neg.loc[df2_Neg['variable'] == 'mat_MFG_eff']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'mod_eff']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'EOL_CE_Pathways']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'mat_MFG_Scrap_Overall_Improvement']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'mod_Repair']['Waste Change'].values[0],

df2_Neg.loc[df2_Neg['variable'] == 'mat_MFG_scrap_Recycling_eff']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'mod_Reuse']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'mat_MFG_scrap_Recycled']['Waste Change'].values[0],
df2_Neg.loc[df2_Neg['variable'] == 'mod_EOL_collection_eff']['Waste Change'].values[0]]


desc=['Overall improvement in EoL Circularity Pathways\n+Reliability and Lifetime',
'Module Lifetime and Reliability',
'Module Manufacutring Efficiency/Yield',
'New Installed Capacity [MW]',
'Mass per $m^{2}$',
      
'Efficiency of Material Use\nduring Module Manufacturing',
'Module Efficiency',
'Overall improvement in EoL Circularity Pathways',
'Overall improvement in\nManufacturing Scrap Recycling Loop',
'Module Repair',
      
'Yield of the Material\nManufacturing Scrap Recycling Process',
'Module Reuse',
'Fraction of Material scrap from\nManufacturing that undergoes Recycling',
'Collection Efficiency of EoL Modules']

desc.reverse()
negvals.reverse()
posvals.reverse()


# In[43]:


sns.set(rc={'figure.figsize':(13.5,10)})
sns.set(font_scale=1.5)  # crazy big
sns.set_style("ticks",{'axes.grid' : True})
sns.set_style("white")

## DATAFRAME DATA
df = pd.DataFrame()
df['input'] = ['I','II','III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'blank'] # Mock Placeholders for Ticks
df['+']=posvals
df['-']=negvals
#now stacking it
df2 = pd.melt(df, id_vars ='input', var_name='type of change', value_name='change in the output' )

fig, (ax1, ax, ax3) = plt.subplots(1,3, gridspec_kw={'width_ratios':[0.001,3.4, 0.001], 'wspace':0.4})

## Grid and Background Colors
ax.axvspan(-100, 0, facecolor=(0.8203125, 0.984375, 0.98046875), alpha=0.5)
ax.axvspan(0, 120, facecolor=(0.90234375, 0.89453125, 0.8984375), alpha=0.5)
ax.grid(axis=1)

for typ, df in zip(df2['type of change'].unique(),df2.groupby('type of change')):
    ax.barh(df[1]['input'], df[1]['change in the output'], height=0.5, label=typ)
ax.set_xlim([-60, 100])
ax2 = ax.twinx()

## REPLOT to Add 2nd axis plot
for typ, df in zip(df2['type of change'].unique(),df2.groupby('type of change')):
    ax2.barh(df[1]['input'], df[1]['change in the output'], height=0.8, label=typ)

## REAL TICK VALUES
ax.set_yticklabels( ['+10%','+10%','+10%', '-10%', '-10% rel', '+10%', '+10% rel', '+10%', '+10%', '+10%', '+10%', '+10%', '+10%', '+10%', ''])
ax2.set_yticklabels( ['-10%','-10%','-10%', '+10%', '+10% rel', '-10%', '-10% rel', '-10%', '-10%', '-10%', '-10%', '-10%', '-10%', '-10%', ''])

## FAKE EMPTY PLOT, same ticks
for typ, df in zip(df2['type of change'].unique(),df2.groupby('type of change')):
    ax1.barh(df[1]['input'], df[1]['change in the output'], height=0.5, label=typ)
#ax1.yaxis.set_label_position("right")
#ax1.yaxis.tick_right()

## Verbose Tick Labels
ax1.set_yticklabels(desc);

## REMOVE Ticks from 'Helper Plots'
ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

ax.tick_params(axis='y', which='both', left=False, right=False)      
ax2.tick_params(axis='y', which='both', left=False, right=False)  


ax3.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax3.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

ax.set_xlabel('% Change in Lifecycle Waste')
# ANNOTATE
ax.annotate('Decrease Waste', xy =(-40.2, 14.0), weight='bold', fontsize=17);
ax.annotate('Increase Waste', xy =(6, 14.0), weight='bold', fontsize=17);
ax.xaxis.grid()

#plt.tight_layout()
fig.savefig(os.path.join(testfolder,'Fig 14 - Sensitivity Analysis WASTE.png'), dpi=600, bbox_inches='tight')
fig.savefig(os.path.join(testfolder,'Fig 14 - Sensitivity Analysis WASTE.pdf'), dpi=600, bbox_inches='tight')

plt.show()


# # Figure 13

# In[45]:


posvals = [0,
            df2_Neg.loc[df2_Neg['variable'] == 'new_Installed_Capacity_[MW]']['Virgin Needs Change'].values[0],
            df2_Neg.loc[df2_Neg['variable'] == 'mat_massperm2']['Virgin Needs Change'].values[0],
            df2_Pos.loc[df2_Pos['variable'] == 'mod_eff']['Virgin Needs Change'].values[0],
            df2_Pos.loc[df2_Pos['variable'] == 'mat_MFG_eff']['Virgin Needs Change'].values[0],
            df2_Pos.loc[df2_Pos['variable'] == 'mod_MFG_eff']['Virgin Needs Change'].values[0]]
           


negvals = [0,
            df2_Pos.loc[df2_Pos['variable'] == 'new_Installed_Capacity_[MW]']['Virgin Needs Change'].values[0],
            df2_Pos.loc[df2_Pos['variable'] == 'mat_massperm2']['Virgin Needs Change'].values[0],
            df2_Neg.loc[df2_Neg['variable'] == 'mod_eff']['Virgin Needs Change'].values[0],
            df2_Neg.loc[df2_Neg['variable'] == 'mat_MFG_eff']['Virgin Needs Change'].values[0],
            df2_Neg.loc[df2_Neg['variable'] == 'mod_MFG_eff']['Virgin Needs Change'].values[0]]
           


desc=['New Installed Capacity [MW]',
'Mass per $m^{2}$',
'Module Efficiency',
'Efficiency of Material Use\nduring Module Manufacturing',
'Module Manufacutring Efficiency/Yield']

desc.reverse()
negvals.reverse()
posvals.reverse()


# In[46]:


#sns.set(rc={'figure.figsize':(13.5,10)})
sns.set(rc={'figure.figsize':(13.5,5)})
sns.set(font_scale=1.5)  # crazy big
sns.set_style("ticks",{'axes.grid' : True})
sns.set_style("white")

## DATAFRAME DATA
df = pd.DataFrame()
df['input'] = ['I','II','III', 'IV', 'V', 'blank'] # Mock Placeholders for Ticks
df['+']=posvals
df['-']=negvals
#now stacking it
df2 = pd.melt(df, id_vars ='input', var_name='type of change', value_name='change in the output' )

#fig, (ax1, ax, ax3) = plt.subplots(1,3, gridspec_kw={'width_ratios':[0.001,3.4, 0.001], 'wspace':0.4})
fig, (ax1, ax, ax3) = plt.subplots(1,3, gridspec_kw={'width_ratios':[0.001,3, 0.001], 'wspace':0.4})

## Grid and Background Colors
ax.axvspan(-100, 0, facecolor=(0.8203125, 0.984375, 0.98046875), alpha=0.5)
ax.axvspan(0, 120, facecolor=(0.90234375, 0.89453125, 0.8984375), alpha=0.5)
ax.grid(axis=1)

for typ, df in zip(df2['type of change'].unique(),df2.groupby('type of change')):
    ax.barh(df[1]['input'], df[1]['change in the output'], height=0.5, label=typ)
ax.set_xlim([-12, 12])
ax2 = ax.twinx()

## REPLOT to Add 2nd axis plot
for typ, df in zip(df2['type of change'].unique(),df2.groupby('type of change')):
    ax2.barh(df[1]['input'], df[1]['change in the output'], height=0.8, label=typ)

## REAL TICK VALUES
ax.set_yticklabels( ['-10%','-10% rel','+10% rel', '+10%', '+10%',''])
ax2.set_yticklabels(['+10%','+10% rel','-10% rel', '-10%', '-10%',''])

## FAKE EMPTY PLOT, same ticks
for typ, df in zip(df2['type of change'].unique(),df2.groupby('type of change')):
    ax1.barh(df[1]['input'], df[1]['change in the output'], height=0.5, label=typ)
#ax1.yaxis.set_label_position("right")
#ax1.yaxis.tick_right()

## Verbose Tick Labels
ax1.set_yticklabels(desc);

## REMOVE Ticks from 'Helper Plots'
ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

ax.tick_params(axis='y', which='both', left=False, right=False)      
ax2.tick_params(axis='y', which='both', left=False, right=False)  


ax3.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax3.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

ax.set_xlabel('% Change in Lifecycle Waste')
# ANNOTATE
ax.annotate('Decrease Material Demand', xy =(-9.9, 4.7), weight='bold', fontsize=17);
ax.annotate('Increase Material Demand', xy =(1.1, 4.7), weight='bold', fontsize=17);
ax.xaxis.grid()

#plt.tight_layout()
fig.savefig(os.path.join(testfolder,'Fig 13 - Sensitivity Analysis VIRGIN NEEDS.png'), dpi=600, bbox_inches='tight')
fig.savefig(os.path.join(testfolder,'Fig 13 - Sensitivity Analysis VIRGIN NEEDS.pdf'), dpi=600, bbox_inches='tight')

plt.show()


# # Modifing the installed capacity to stay fixed at BASELINE
# Needs to run each year becuase it needs to calculate the acumulated installs and deads.

# In[ ]:


Diff_Installment = []
for i in range (0, len(s1.scenario['baseline'].data)):
    for jj in range (1, len(list(s1.scenario.keys()))):
        scen = list(s1.scenario.keys())[jj]
        Diff_Installment = ( (s1.scenario['baseline'].data['Installed_Capacity_[W]'][i] - 
                             s1.scenario[scen].data['Installed_Capacity_[W]'][i])/1000000 )  # MWATTS
        s1.scenario[scen].data['new_Installed_Capacity_[MW]'][i] += Diff_Installment
    s1.calculateMassFlow()data:image/png;base64,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YQPFixfP5oieLzExMTRt2pTJc+dSsUqVLK8/M6shPSuep7YCFLG1JeEfPgm2Fs/TZ/s427pv3z7atW/P/PnzjVWz5PF71v7OqsdGRERERESsnhIbERERERGxekpsRERERETE6imxERERERERq6fERkRERERErJ4SGxERERERsXpKbERERERExOopsREREREREaunxEZERERERKyeEhsREREREbF6SmxERERERMTqKbERERERERGrp8RGRERERESsnhIbERERERGxekpsRERERETE6imxERERERERq6fERkRERERErJ4SGxERERERsXpKbERERERExOopsREREREREaunxEZERERERKyeEhsRERHJUskpKdkdgog8h5TYiIiISJa6cfNmdocgIs8hJTYiIiIiImL1lNiIiIiIiIjVU2IjIiIiIiJWT4mNiIiIiIhYPSU2IiIiIiJi9ZTYiIiIiIiI1bPL7gBEROT59FqBQjjZ2mZ3GE9EkeLFszuEJyrVPic5cjpldxhPRJ68ebM7hCfGwd6Om7eTszsMkXtSYiMiItnCycGeBr2WZ3cY8hisGNeQ2BGNsjsMyWKlByzm5u2r2R2GyD1pKJqIiIiIiFg9JTYiIiIiImL1lNiIiIiIiIjVU2IjIiIiIiJWT4mNiIiIiIhYPSU2IiIiIiJi9ZTYSKaYzebsDuG5pusvIiIicn9KbB5BWFgY5cuX53//+1+G+8uVK0dERMQTjgqCgoIYMGBAltZ5+/ZtRo4cyYoVKx7quIiICMqVK5flsS1ZsgSTycSZM2ceWHbz5s107NgRPz8/KlasSN26dZkwYQJXrlz5x3E8LnFxcZhMJpYvv/Nuj4SEBPr3709MTMw/qjcoKAiTyWTUnXYek8nE4sWLMzzmxIkTRpm4uDg2bdqEyWTi+++/T1c2ICAAk8nE5s2bLbabzWa8vb3p378/YWFhRn1Tp079R+151nTr1i3D/x+JiYkMGzYMX19fPDw8aNeuHceOHbMos2vXLurUqYOXlxdDhw4lKSnJYn94eDjdu3d/nOGLiIg8FZTYPKLk5GQ+/PBDkpOf7TfwxsfHM2vWLKtr56hRo2jXrh25c+dm0KBBTJs2jcaNGxMVFUWTJk24ePFidoeYoUKFCrFw4UJq1KgBwOHDh1m6dCmpqan/uO6goCCLugFsbGxYs2ZNhuVXrVpl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


# #### Compile Changes

# In[ ]:


virginStock_Changes = []
waste_Changes = []
installedCapacity_Changes = []
virginStockRAW_Changes = []

virgin_keyword = 'mat_Virgin_Stock'
waste_keyword = 'mat_Total_Landfilled'
installs_keyword = 'Installed_Capacity_[W]'
viring_raw_keyword = 'mat_Virgin_Stock_Raw'

virginStock_baseline_cum2050 = s1.scenario['baseline'].material[MATERIAL].materialdata[virgin_keyword].sum()
virginStockRAW_baseline_cum2050 = s1.scenario['baseline'].material[MATERIAL].materialdata[viring_raw_keyword].sum()

# Installed Capacity is already cumulative so no need to sum or cumsum.
waste_baseline_cum2050 = s1.scenario['baseline'].material[MATERIAL].materialdata[waste_keyword].sum()
installedCapacity_baselined_2050 = s1.scenario['baseline'].data[installs_keyword].iloc[-1]

for i in range (1, len(scenarios)):
    stage_name = scenarios[i]
    virginStock_Changes.append(round(100*s1.scenario[stage_name].material[MATERIAL].materialdata[virgin_keyword].sum()/virginStock_baseline_cum2050,5)-100)
    virginStockRAW_Changes.append(round(100*s1.scenario[stage_name].material[MATERIAL].materialdata[viring_raw_keyword].sum()/virginStockRAW_baseline_cum2050,5)-100)

    waste_Changes.append(round(100*s1.scenario[stage_name].material[MATERIAL].materialdata[waste_keyword].sum()/waste_baseline_cum2050,5)-100)
    installedCapacity_Changes.append(round(100*s1.scenario[stage_name].data[installs_keyword].iloc[-1]/installedCapacity_baselined_2050,5)-100)


# In[ ]:


stages = scenarios[1::] # removing baseline as we want a dataframe with only changes


# In[ ]:


df = pd.DataFrame(list(zip(virginStock_Changes, virginStockRAW_Changes, waste_Changes, installedCapacity_Changes)), 
               columns=['Virgin Needs Change', 'Virgin Stock Raw Change', 'Waste Change', 'InstalledCapacity Change'],index=stages) 


# #### Present Results

# In[ ]:


df_Pos = df[['high' in s for s in df.index]].copy()
df_Pos.index = df_Pos.index.str.replace("_high", "")

col_verbose = []

for i in range (0, len(df_Pos)):
    if df_Pos.index[i] in variables_description:
        col_verbose.append(variables_description[df_Pos.index[i]])
    else:
        col_verbose.append("")
        
df_Pos['Description'] = col_verbose     
df_Pos = df_Pos.reset_index()
df_Pos = df_Pos.rename(columns={'index':'variable'})


# In[ ]:


df_Neg = df[['low' in s for s in df.index]].copy()
df_Neg.index = df_Neg.index.str.replace("_low", "")

col_verbose = []

for i in range (0, len(df_Neg)):
    if df_Neg.index[i] in variables_description:
        col_verbose.append(variables_description[df_Neg.index[i]])
    else:
        col_verbose.append("")

df_Neg['Description'] = col_verbose
df_Neg = df_Neg.reset_index()
df_Neg = df_Neg.rename(columns={'index':'variable'})


# In[ ]:


print("Keeping Installs, the modifications to Virgin Needs, Virgin STock and Waste")
df_Pos


# In[ ]:


print("Keeping Installs, the modifications to Virgin Needs, Virgin STock and Waste")
df_Neg


# In[ ]:


fooPosDemand=df_Pos[['Virgin Needs Change']]
fooPosDemand.set_index(df_Pos['variable'], inplace=True)
fooPosDemand=fooPosDemand.loc[['new_Installed_Capacity_[MW]', 'mat_massperm2', 'mod_eff', 
                  'mod_MFG_eff', 'mat_MFG_Scrap_Overall_Improvement']]

fooNegDemand=df_Neg[['Virgin Needs Change']]
fooNegDemand.set_index(df_Neg['variable'], inplace=True)
fooNegDemand=fooNegDemand.loc[['new_Installed_Capacity_[MW]', 'mat_massperm2', 'mod_eff', 
                  'mod_MFG_eff', 'mat_MFG_Scrap_Overall_Improvement']]


# In[ ]:





# In[ ]:




