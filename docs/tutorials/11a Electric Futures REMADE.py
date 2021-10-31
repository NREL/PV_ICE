#!/usr/bin/env python
# coding: utf-8

# # Journal for Results included in PV ICE Paper 1

# In[1]:


m1 = False
m2 = False
m3 = True


# In[2]:


import PV_ICE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP' / 'ElectricFutures')

# Another option using relative address; for some operative systems you might need '/' instead of '\'
# testfolder = os.path.abspath(r'..\..\PV_DEMICE\TEMP')  

print ("Your simulation will be stored in %s" % testfolder)


# In[3]:


PV_ICE.__version__


# In[4]:


plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 5)


# In[5]:



MATERIALS = ['glass','silver','silicon', 'copper','aluminium_frames', 'backsheet', 'encapsulant']
MATERIAL = MATERIALS[0]

MODULEBASELINE = r'..\..\baselines\ElectrificationFutures_2021\baseline_modules_US_NREL_Electrification_Futures_2021_basecase.csv'
MODULEBASELINE_High = r'..\..\baselines\ElectrificationFutures_2021\baseline_modules_US_NREL_Electrification_Futures_2021_LowREHighElec.csv'


# In[6]:


r1 = PV_ICE.Simulation(name='PV_ICE', path=testfolder)
r1.createScenario(name='base', file=MODULEBASELINE)
r1.createScenario(name='high', file=MODULEBASELINE_High)

r1.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r1.scenario['high'].addMaterials(MATERIALS, r'..\..\baselines')


# In[7]:


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


# In[8]:


r3 = PV_ICE.Simulation(name='Irena_EL', path=testfolder)
r3.createScenario(name='base', file=MODULEBASELINE)
r3.createScenario(name='high', file=MODULEBASELINE_High)
r3.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r3.scenario['high'].addMaterials(MATERIALS, r'..\..\baselines')

r3.scenMod_IRENIFY(scenarios=['base', 'high'], ELorRL = 'EL' )


# In[9]:


r4 = PV_ICE.Simulation(name='Irena_RL', path=testfolder)
r4.createScenario(name='base', file=MODULEBASELINE)
r4.createScenario(name='high', file=MODULEBASELINE_High)
r4.scenario['base'].addMaterials(MATERIALS, r'..\..\baselines')
r4.scenario['high'].addMaterials(MATERIALS, r'..\..\baselines')
r4.scenMod_IRENIFY(scenarios=['base', 'high'], ELorRL = 'RL' )


# In[10]:


r1.calculateMassFlow(m1=m1, m2=m2, m3=m3)
r2.calculateMassFlow(m1=m1, m2=m2, m3=m3)
r3.calculateMassFlow(m1=m1, m2=m2, m3=m3)
r4.calculateMassFlow(m1=m1, m2=m2, m3=m3)


# # Compile Results

# In[11]:


objects = [r1, r2, r3, r4]
scenarios = ['base', 'high']


# In[12]:


pvice_Usyearly1, pvice_Uscum1 = r1.aggregateResults()
pvice_Usyearly2, pvice_Uscum2 = r2.aggregateResults()
pvice_Usyearly3, pvice_Uscum3 = r3.aggregateResults()
pvice_Usyearly4, pvice_Uscum4 = r4.aggregateResults()
UScum = pd.concat([pvice_Uscum1, pvice_Uscum2, pvice_Uscum3, pvice_Uscum4], axis=1)
USyearly = pd.concat([pvice_Usyearly1, pvice_Usyearly2, pvice_Usyearly3, pvice_Usyearly4], axis=1)

UScum.to_csv('pvice_USCum.csv')
USyearly.to_csv('pvice_USYearly.csv')


# # Plotting Galore

# In[13]:


mining2020_aluminum = 65267000
mining2020_silver = 22260
mining2020_copper = 20000000
mining2020_silicon = 8000000


# In[14]:


plt.rcParams.update({'font.size': 10})
plt.rcParams['figure.figsize'] = (12, 8)
    
keyw='VirginStock_'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']

fig, axs = plt.subplots(1,1, figsize=(4, 6), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.2)


# Loop over CASES
name2 = 'PV_ICE_high_[Tonnes]'
name0 = 'PV_ICE_base_[Tonnes]'
# ROW 2, Aluminum and Silicon:        g-  4 aluminum k - 1 silicon   orange - 3 copper  gray - 2 silver
axs.plot(USyearly[keyw+materials[2]+'_'+name2]*100/mining2020_silver, 
         color = 'gray', linewidth=2.0, label='Silver')

axs.fill_between(USyearly.index, USyearly[keyw+materials[2]+'_'+name0]*100/mining2020_silver, USyearly[keyw+materials[2]+'_'+name2]*100/mining2020_silver,
                   color='gray', lw=3, alpha=.3)
    

axs.plot(USyearly[keyw+materials[1]+'_'+name2]*100/mining2020_silicon, 
         color = 'k', linewidth=2.0, label='Silicon')
axs.fill_between(USyearly.index, USyearly[keyw+materials[1]+'_'+name0]*100/mining2020_silicon, 
                                USyearly[keyw+materials[1]+'_'+name2]*100/mining2020_silicon,
                   color='k', lw=3, alpha=.5)



axs.plot(USyearly[keyw+materials[4]+'_'+name2]*100/mining2020_aluminum, 
         color = 'g', linewidth=2.0, label='Aluminum')

axs.fill_between(USyearly.index, USyearly[keyw+materials[4]+'_'+name0]*100/mining2020_aluminum, 
                                USyearly[keyw+materials[4]+'_'+name2]*100/mining2020_aluminum,
                   color='g', lw=3, alpha=.3)



axs.plot(USyearly[keyw+materials[3]+'_'+name2]*100/mining2020_copper, 
         color = 'orange', linewidth=2.0, label='Copper')

axs.fill_between(USyearly.index, USyearly[keyw+materials[3]+'_'+name0]*100/mining2020_copper, 
                                USyearly[keyw+materials[3]+'_'+name2]*100/mining2020_copper,
                   color='orange', lw=3, alpha=.3)



axs.set_xlim([2020,2050])
axs.legend()
#axs.set_yscale('log')

axs.set_ylabel('Virgin material needs as a percentage of \n 2020 global mining production capacity [%]')

fig.savefig(os.path.join(testfolder,'Fig_1x1_MaterialNeeds Ratio to Production_NREL2018.png'), dpi=600)


# # THRI PLOT

# In[15]:


materials = ['glass', 'aluminium_frames', 'silicon', 'copper', 'silver', 'encapsulant', 'backsheet']
modulemat = 'Module'

plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.figsize'] = (15, 20.4)


f, a0 = plt.subplots(3, 2, gridspec_kw={'width_ratios': [3.5,1.5], 'wspace':0.15, 'hspace':0.25})

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

a0[0,0].legend()
a0[0,0].set_title('Yearly Virgin Material Needs by Scenario')
a0[0,0].set_ylabel('Module Mass [Million Tonnes]')
a0[0,0].set_xlim([2020, 2050])
a0[0,0].set_xlabel('Years')

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
a0[0,1].set_xticks(ind, ('S1', 'S2', 'S3', 'S4'))
#plt.yticks(np.arange(0, 81, 10))
a0[0,1].legend((p0[0], p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]), 
          ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver', 'Encapsulant', 'Backsheets' ))

print("Cumulative Virgin Needs by 2050 Million Tones by Scenario")
print(dfcumulations2050[materials].sum(axis=1))


#################################
# ROW 2
################################

# SCENARIO 1 ***************
keyw='WasteEOL_'
a0[1,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name1]/1000000, 'k', linestyle='dotted', linewidth=4, label='S1: PV ICE, ref')
a0[1,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name2]/1000000, 'c', linewidth=3, label='S2: PV ICE, h.e.')
a0[1,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name3]/1000000, 'g', linestyle='dashdot', linewidth=3, label='S3: IRENA, Early Loss, h.e.')
a0[1,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name4]/1000000, 'b--', linewidth=3, label='S4: IRENA, Regular Loss, h.e.')

a0[1,0].legend()
a0[1,0].set_title('Yearly EoL Material by Scenario')
a0[1,0].set_ylabel('Module Mass [Million Tonnes]')
a0[1,0].set_xlim([2020, 2050])
a0[1,0].set_xlabel('Years')

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
a0[1,1].set_xticks(ind, ('S1', 'S2', 'S3', 'S4'))
#plt.yticks(np.arange(0, 81, 10))
a0[1,1].legend((p0[0], p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]), 
          ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver', 'Encapsulant', 'Backsheets' ),
              loc='upper right')


print("Cumulative Virgin Needs by 2050 Million Tones by Scenario")
print(dfcumulations2050[materials].sum(axis=1))





#################################
# ROW 3
################################

# SCENARIO 1 ***************
keyw='WasteMFG_'
a0[2,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name1]/1000000, 'k.', linestyle='dotted', linewidth=4, label='S1: PV ICE, ref')
a0[2,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name2]/1000000, 'c', linewidth=3, label='S2: PV ICE, h.e.')
a0[2,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name3]/1000000, 'g', linestyle='dashdot', linewidth=3, label='S3: IRENA, Early Loss, h.e.')
a0[2,0].plot(USyearly.index, USyearly[keyw+modulemat+'_'+name4]/1000000, 'b--', linewidth=3, label='S4: IRENA, Regular Loss, h.e.')

a0[2,0].legend()
a0[2,0].set_title('Yearly Manufacturing Scrap by Scenario')
a0[2,0].set_ylabel('Module Mass [Million Tonnes]')
a0[2,0].set_xlim([2020, 2050])
a0[2,0].set_xlabel('Years')

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
a0[2,1].set_xticks(ind, ('S1', 'S2', 'S3', 'S4'))
#plt.yticks(np.arange(0, 81, 10))
a0[2,1].legend((p0[0], p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]), 
          ('Glass', 'aluminium_frames', 'Silicon','Copper','Silver', 'Encapsulant', 'Backsheets' ),
              loc='lower right')

f.tight_layout()

f.savefig(os.path.join(testfolder,'THRI_PLOT.png'), dpi=600)

print("Cumulative Virgin Needs by 2050 Million Tones by Scenario")
print(dfcumulations2050[materials].sum(axis=1))


# # TABLE 7: METRIC TONNES IN FIELD IN 2030

# In[16]:


names = ['PV_ICE_base', 'PV_ICE_high', 'Irena_EL_base', 'Irena_EL_high', 'Irena_RL_base', 'Irena_RL_high']
materials = ['Module', 'glass', 'encapsulant', 'backsheet', 'aluminium_frames', 'copper', 'silicon', 'silver']


# In[17]:


print("TABLE 7 - METRIC TONNES IN FIELD IN 2030")

tableapp=[]
for name in names:
    colapp=[]
    for mat in materials:
         colapp.append(UScum.filter(regex='VirginStock_'+mat+'_'+name).loc[2030][0]-
                       UScum.filter(regex='WasteAll_'+mat+'_'+name).loc[2030][0])
    tableapp.append(colapp)
    
df= pd.DataFrame(tableapp, columns = materials, index=names)
df = df.T
df


# # Figure 12 Cumulative EOL MAterial, 2016, 2020, 2030, 2040, 2050

# In[18]:


names = ['Irena_EL_base', 'Irena_RL_base', 'PV_ICE_base']


# In[19]:


print("Figure 12 - Cumulative EOL Material 2016, 2020, 2030, 240, 2050")

years = [2016, 2020, 2030, 2040, 2050]
tableapp=[]
for name in names:
    colapp=[]
    for year in years:
         colapp.append(UScum.filter(regex='WasteEOL_Module_'+name).loc[year][0])
    tableapp.append(colapp)
    
df= pd.DataFrame(tableapp, columns = years, index=names)
df = df.T 
df


# # FIX THIS NUMBER!

# In[20]:


df.insert(loc=0, column='Irena 2016 Early Loss', value=[9000, 11000,110000,1000000,8000000])
df.insert(loc=1, column='Irena 2016 Regular Loss', value=[9000, 11000,110000,1000000,8000000])
df.insert(loc=2, column='CSA 2020 Early Loss', value=[9000, 11000,110000,1000000,8000000])
df.insert(loc=3, column='CSA 2020 Regular Loss', value=[9000, 11000,110000,1000000,8000000])


# In[21]:


import matplotlib.ticker as ticker
import numpy as np


# In[22]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (10, 6)


my_colors=[(0.74609375, 0.5625, 0),
(0.99609375, 0.75, 0),
(0.09375, 0.9375, 0.91796875),
(0.71875, 0.9765625, 0.96875),
(0.0390625, 0.6015625, 0.58984375),
(0.35546875, 0.60546875, 0.83203125),
(0.61328125, 0.76171875, 0.8984375)]


#ax = df.plot(kind='bar', edgecolor='white', linewidth=1, width=0.65, colormap='Paired') #color=my_colors)# width=0.5)
ax = df.plot(kind='bar', edgecolor='white', linewidth=1, width=0.65, color=my_colors)# width=0.5)

ax.set_yscale('log')
ax.grid(axis='y')
ax.set_axisbelow(b=True) # Set grid behind plots
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
ax.set_xticklabels(df.index, rotation = 0)
ax.set_ylabel('Cumulative EoL Materials [metric tons]')
# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax.legend(['Irena 2016 Early Loss', 'Irena 2016 Regular Loss', 'CSA 2020 Early Loss', 'CSA 2020 Regular Loss',
          'PV ICE + EF (ref), Early loss', 'PV ICE + EF (ref), Regular loss', 'PV ICE + EF (ref), PV ICE loss'], 
          loc='upper center', bbox_to_anchor=(0.5, 1.38), fancybox=True, shadow=True, ncol=2)

plt.show()


# In[23]:


# Some options Silvana liked
# vlag_r, viridis, tab20b, tab10_r, rainbow_r, plasma, nipy_spectral_r

# ALL OPTIONS
# Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, icefire, icefire_r, inferno, inferno_r, jet, jet_r, magma, magma_r, mako, mako_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, rocket, rocket_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, vlag, vlag_r, winter, winter_r


# In[24]:


plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (10, 6)


my_colors=[(0.74609375, 0.5625, 0),
(0.99609375, 0.75, 0),
(0.09375, 0.9375, 0.91796875),
(0.71875, 0.9765625, 0.96875),
(0.0390625, 0.6015625, 0.58984375),
(0.35546875, 0.60546875, 0.83203125),
(0.61328125, 0.76171875, 0.8984375)]



ax = df.plot(kind='bar', edgecolor='white', linewidth=1, width=0.65, colormap='nipy_spectral_r') #color=my_colors)# width=0.5)

ax.set_yscale('log')
ax.grid(axis='y')
ax.set_axisbelow(b=True) # Set grid behind plots
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
ax.set_xticklabels(df.index, rotation = 0)
ax.set_ylabel('Cumulative EoL Materials [metric tons]')
# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax.legend(['Irena 2016 Early Loss', 'Irena 2016 Regular Loss', 'CSA 2020 Early Loss', 'CSA 2020 Regular Loss',
          'PV ICE + EF (ref), Early loss', 'PV ICE + EF (ref), Regular loss', 'PV ICE + EF (ref), PV ICE loss'], 
          loc='upper center', bbox_to_anchor=(0.5, 1.38), fancybox=True, shadow=True, ncol=2)

plt.show()


# # Figure 11 Installed Capacity for all Scenarios

# In[25]:


names = ['PV_ICE_base', 'PV_ICE_high', 'Irena_EL_base', 'Irena_EL_high', 'Irena_RL_base', 'Irena_RL_high']


# In[26]:


print("Figure 11 Installed CApacity for all Scenarios")

years = [2030, 2050]
tableapp=[]
for name in names:
    colapp=[]
    for year in years:
         colapp.append(USyearly.filter(regex='Capacity_'+name).loc[year][0])
    tableapp.append(colapp)
    
df= pd.DataFrame(tableapp, columns = years, index=names)
df = df.T 
df


# In[27]:


df['PV_ICE_increase_high'] = df['PV_ICE_high']-df['PV_ICE_base']
df['Irena_EL_increase_high'] = df['Irena_EL_high']-df['Irena_EL_base']
df['Irena_RL_increase_high'] = df['Irena_RL_high']-df['Irena_RL_base']
df['Irena 2016'] = [240000, 512000]
df['CSA 2000'] = [437000, 0]
df['inc0'] = [0, 0]


# In[28]:


df


# In[29]:


import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (10, 10)


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
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # OTHER PLOT CODE TESTED

# In[30]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[31]:


'''
df = df.rename_axis('year')
foo = pd.melt(df.reset_index(), id_vars=["year"])
foo

plt.rcParams.update({'font.size': 15})
plt.rcParams['figure.figsize'] = (14, 6)

sns.set_context(rc = {'patch.linewidth': 1})
sns.barplot(x = "year", y='value', hue='variable', data = foo, edgecolor='white')
''';


# In[32]:


from matplotlib.patches import Polygon, Patch


# In[33]:


import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt

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
                      **kwargs)  # make bar plots

    colorlist = ['orange','orange','orange', 'orange', 
                 'green','green','green', 'green', 
                 'blue', 'blue', 'blue', 'blue',
                 'cyan', 'cyan', 'cyan', 'cyan']
    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    jj=0
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        zz = 0
        
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                if zz >= 2:
                    rect.set_hatch('/') #edited part   
                    rect.set_facecolor('red')
                zz += 1
                jj+=1
                rect 
                rect.set_color(colorlist[jj])
         #       rect.set_color('green')
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)
    axe.set_title(title)

    # Add invisible data to add another legend
    n=[]        
    print(n_df)
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plt.legend(n, labels, loc=[1.01, 0.1]) 
    axe.add_artist(l1)
    return axe

# create fake dataframes
df1 = df[['PV_ICE_base', 'PV_ICE_increase_high']]
df2 = df[['Irena_EL_base', 'Irena_EL_increase_high']]
df3 = df[['Irena_RL_base', 'Irena_EL_increase_high']]
df4 = df[['Irena 2016', 'inc0']]
df5 = df[['CSA 2000', 'inc0']]

# Then, just call :
plot_clustered_stacked([df1, df2, df3, df4, df5],["df1", "df2", "df3", "df4", "df5"])
    


# In[ ]:


df.keys()


# In[ ]:


ax=df['PV_ICE_high'].plot.bar(position=0, width=.1, color=['mediumspringgreen'], align='center', hatch='/')

df['PV_ICE_base'].plot.bar(position=0, width=.1, color=['mediumspringgreen'], align='center')
   
df['Irena_EL_high'].plot.bar(ax=ax, position=-1, width=.1, color=['green'], hatch='/')

df['Irena_EL_base'].plot.bar(ax=ax, position=-1, stacked=True, width=.1, color=['blue'])

df['Irena_RL_high'].plot.bar(ax=ax, position=-2, width=.1, color=['red'], hatch='/')
        
df['Irena_RL_base'].plot.bar(ax=ax, position=-2, width=.1, color=['cyan'])

df['Irena 2016'].plot.bar(ax=ax, position=-3, width=.1, color=['magenta'])
df['CSA 2000'].plot.bar(ax=ax, position=-4, width=.1, color=['yellow'])

ax.


# In[ ]:


ax=df[['PV_ICE_base', 'PV_ICE_increase_high']].plot.bar(stacked=True, position=0,
                            width=.1, color=['yellowgreen', 'mediumspringgreen'], align='center')
   
df[['Irena_EL_base', 'Irena_EL_increase_high']].plot.bar(ax=ax, stacked=True, position=-1, width=.1, 
                                                              color=['green', 'blue'], hatch=('+','/'))
        
cx = df[['Irena_RL_base', 'Irena_RL_increase_high']].plot.bar(ax=ax,  stacked=True, position=-2, width=.1, color=['green', 'red'])
dx = df[['Irena 2016']].plot.bar(ax=ax, position=-3, width=.1, color=['magenta'])
ex = df[['CSA 2000']].plot.bar(ax=ax, position=-4, width=.1, color=['yellow'])

for container, hatch in zip(ax.containers, ("-", "*")):
    for patch in container.patches:
        patch.set_hatch(hatch)


# In[ ]:


ax=df['PV_ICE_high'].plot.bar(position=2, width=.1, color=['mediumspringgreen'], align='center', hatch='/')

df['PV_ICE_base'].plot.bar(position=2, width=.1, color=['mediumspringgreen'], align='center')
   
df['Irena_EL_high'].plot.bar(ax=ax, position=1, width=.1, color=['green'], hatch='/')

df['Irena_EL_base'].plot.bar(ax=ax, position=1, stacked=True, width=.1, color=['blue'])

df['Irena_RL_high'].plot.bar(ax=ax, position=0, width=.1, color=['red'], hatch='/')
        
df['Irena_RL_base'].plot.bar(ax=ax, position=0, width=.1, color=['cyan'])

df['Irena 2016'].plot.bar(ax=ax, position=-1, width=.1, color=['magenta'])
df['CSA 2000'].plot.bar(ax=ax, position=-2, width=.1, color=['yellow'])

ax.axhline(10, linewidth=5, color='r')


# In[ ]:


ax


# In[ ]:





# In[ ]:


c = ["blue", "purple"]
for i, g in enumerate(dfall.groupby("variable")):
    ax = sns.barplot(data=g[1],
                     x="index",
                     y="vcs",
                     hue="Name",
                     color=c[i],
                     zorder=-i, # so first bars stay on top
                     edgecolor="k")
ax.legend_.remove() # remove the redundant legends 


# In[ ]:





# In[ ]:


pd.melt(df.reset_index(), id_vars=["index"])


# In[ ]:





# In[ ]:


import seaborn as sns


# In[ ]:


for i, g in enumerate(df):
    print(i, g)


# In[ ]:





# In[ ]:


for i, g in enumerate(df):
    ax = sns.barplot(data=df[g],
#                     x="index",
#                     y="value",
#                     hue="Name",
#                     color=c[i],
              #       zorder=-i, # so first bars stay on top
 #                    edgecolor="k"
                    )
ax.legend_.remove() # remove the redundant legends 


# In[ ]:


df1["Name"] = "df1"
df2["Name"] = "df2"
df3["Name"] = "df3"
dfall = pd.concat([pd.melt(i.reset_index(),
                           id_vars=["Name", "index"]) # transform in tidy format each df
                   for i in [df1, df2, df3]],
                   ignore_index=True)


# In[ ]:


print("Figure 11 Installed CApacity for all Scenarios")

years = [2030, 2050]
tableapp=[]
for name in names:
    colapp=[]
    for year in years:
         colapp.append(USyearly.filter(regex='Capacity_'+name).loc[year][0])
    tableapp.append(colapp)
    
df= pd.DataFrame(tableapp, columns = years, index=names)
df = df.T 
df


# In[ ]:


print("TABLE 7 - METRIC TONNES IN FIELD IN 2030")

tableapp=[]
for name in names:
    colapp=[]
    for mat in materials:
         colapp.append(UScum.filter(regex='VirginStock_'+mat+'_'+name).loc[2030][0]-
                       UScum.filter(regex='WasteAll_'+mat+'_'+name).loc[2030][0])
    tableapp.append(colapp)
    
df= pd.DataFrame(tableapp, columns = materials, index=names)
df = df.T
df.loc['Module'] = df.sum(axis=0)
df


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


keyw='WasteEOL_'


# Loop over CASES
name0 = 'PV_ICE_base_[Tonnes]'
name2 = 'PV_ICE_high_[Tonnes]'
name3 = 'Irena_EL_high_[Tonnes]'
name4 = 'Irena_RL_high_[Tonnes]'

cumulations2050 = {}
for ii in range(0, len(materials)):
    matcum = []
    matcum.append(UScum[keyw+materials[ii]+'_'+name0].loc[2020])
    matcum.append(UScum[keyw+materials[ii]+'_'+name2].loc[2020])
    matcum.append(UScum[keyw+materials[ii]+'_'+name3].loc[2020])
    matcum.append(UScum[keyw+materials[ii]+'_'+name4].loc[2020])
    cumulations2050[materials[ii]] = matcum

dfcumulations2050 = pd.DataFrame.from_dict(cumulations2050) 
dfcumulations2050 = dfcumulations2050/1000000   # in Million Tonnes
dfcumulations2050['Module'] = dfcumulations2050.sum(axis=1)
dfcumulations2050['Module']

print("Cumulative Values on 2020")
dfcumulations2050


# In[ ]:





# In[ ]:





# In[ ]:





# ### Previous way of compiling results

# In[ ]:


r'''
USyearly=pd.DataFrame()


# In[10]:


keyword='mat_Total_Landfilled'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']

# Loop over objects
for kk in range(0, len(objects)):
    obj = objects[kk]

    # Loop over Scenarios
    for jj in range(0, len(scenarios)):
        case = scenarios[jj]
        
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = obj.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["Waste_"+material+'_'+obj.name+'_'+case] = foo[material]

        filter_col = [col for col in USyearly if (col.startswith('Waste') and col.endswith(obj.name+'_'+case)) ]
        USyearly['Waste_Module_'+obj.name+'_'+case] = USyearly[filter_col].sum(axis=1)

# Converting to grams to Tons. 
USyearly.head(20)


# In[12]:


keyword='mat_Total_EOL_Landfilled'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']

# Loop over objects
for kk in range(0, len(objects)):
    obj = objects[kk]

    # Loop over Scenarios
    for jj in range(0, len(scenarios)):
        case = scenarios[jj]
        
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = obj.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["Waste_EOL_"+material+'_'+obj.name+'_'+case] = foo[material]

        filter_col = [col for col in USyearly if (col.startswith('Waste_EOL_') and col.endswith(obj.name+'_'+case)) ]
        USyearly['Waste_EOL_Module_'+obj.name+'_'+case] = USyearly[filter_col].sum(axis=1)

# Converting to grams to Tons. 
USyearly.head(20)


# In[13]:


keyword='mat_Total_MFG_Landfilled'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']

# Loop over objects
for kk in range(0, len(objects)):
    obj = objects[kk]

    # Loop over Scenarios
    for jj in range(0, len(scenarios)):
        case = scenarios[jj]
        
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = obj.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["Waste_MFG_"+material+'_'+obj.name+'_'+case] = foo[material]

        filter_col = [col for col in USyearly if (col.startswith('Waste_MFG') and col.endswith(obj.name+'_'+case)) ]
        USyearly['Waste_MFG_Module_'+obj.name+'_'+case] = USyearly[filter_col].sum(axis=1)

# Converting to grams to Tons. 
USyearly.head(20)


# In[14]:


keyword='mat_Virgin_Stock'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']

# Loop over objects
for kk in range(0, len(objects)):
    obj = objects[kk]

    # Loop over Scenarios
    for jj in range(0, len(scenarios)):
        case = scenarios[jj]
        
        for ii in range (0, len(materials)):    
            material = materials[ii]
            foo = obj.scenario[case].material[material].materialdata[keyword].copy()
            foo = foo.to_frame(name=material)
            USyearly["VirginStock_"+material+'_'+obj.name+'_'+case] = foo[material]

        filter_col = [col for col in USyearly if (col.startswith('VirginStock_') and col.endswith(obj.name+'_'+case)) ]
        USyearly['VirginStock_Module_'+obj.name+'_'+case] = USyearly[filter_col].sum(axis=1)


# ### Converting to grams to METRIC Tons. 
# 

# In[15]:


USyearly = USyearly/1000000  # This is the ratio for Metric tonnes
#907185 -- this is for US tons


# In[16]:


UScum = USyearly.copy()
UScum = UScum.cumsum()
UScum.head()


# ### Adding Installed Capacity to US

# In[17]:


keyword='Installed_Capacity_[W]'
materials = ['glass', 'silicon', 'silver', 'copper', 'aluminium_frames']

# Loop over SF Scenarios
for kk in range(0, len(objects)):
    obj = objects[kk]
    
    # Loop over Scenarios
    for jj in range(0, len(scenarios)):
        case = scenarios[jj]
        
        foo = obj.scenario[case].data[keyword]
        foo = foo.to_frame(name=keyword)
        UScum["Capacity_"+obj.name+'_'+case] = foo[keyword]


# ## Mining Capacity

# In[19]:


USyearly.index = r1.scenario['base'].data['year']
UScum.index = r1.scenario['base'].data['year']


UScum.to_csv('USCum.csv')
''';

