# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 09:58:31 2020

@author: sayala
"""


file = r'C:\Users\Silvana\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_modules_test.csv'
fileglass = r'C:\Users\Silvana\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_material_test.csv'
r1 = Simulation()
r1.createScenario('standard', file=file)
r1.scenario['standard'].addMaterial('glass', fileglass )

r1.__dict__
r1.scenario['standard']
r1.scenario['standard'].__dict__
r1.scenario['standard'].material['glass']


###

def weibull_params(keypoints):
    '''Returns shape parameter `alpha` and scale parameter `beta`
    for a Weibull distribution whose CDF passes through the
    two time: value pairs in `keypoints`'''
    t1, t2 = tuple(keypoints.keys())
    cdf1, cdf2 = tuple(keypoints.values())
    alpha = np.ndarray.item(np.real_if_close(
        (np.log(np.log(1 - cdf1)+0j) - np.log(np.log(1 - cdf2)+0j))/(np.log(t1) - np.log(t2))
    ))
    beta = np.abs(np.exp(
        (
            np.log(t2)*((0+1j)*np.pi + np.log(np.log(1 - cdf1)+0j))
            + np.log(t1)*(((0-1j))*np.pi - np.log(np.log(1 - cdf2)+0j))
        )/(
            np.log(np.log(1 - cdf1)+0j) - np.log(np.log(1 - cdf2)+0j)
        )
    ))
    return {'alpha': alpha, 'beta': beta}

def weibull_cdf(alpha, beta):
    '''Return the CDF for a Weibull distribution having:
    shape parameter `alpha`
    scale parameter `beta`'''
    def cdf(x):
        return 1 - np.exp(-(np.array(x)/beta)**alpha)
    return cdf

def weibull_pdf(alpha, beta):
    '''Return the PDF for a Weibull distribution having:
        shape parameter `alpha`
        scale parameter `beta`/'''
    def pdf(x):
        return (alpha/np.array(x)) * ((np.array(x)/beta)**alpha) * (np.exp(-(np.array(x)/beta)**alpha))
    return pdf



# In[2] : Testing inner C alculate DMF
df = r1.scenario['standard'].data

#df['t50'] = 30.0
#df['t90'] = 40.0
#df['mod_lifetime'] = 20.0  # for easier testing


irradiance_stc = 1000 # W/m^2

# Renaming and re-scaling
df['new_Installed_Capacity_[W]'] = df['new_Installed_Capacity_[MW]']*1e6
df['t50'] = df['mod_reliability_t50']
df['t90'] = df['mod_reliability_t90']

# Calculating Area and Mass
df['Area'] = df['new_Installed_Capacity_[W]']/(df['mod_eff']*0.01)/irradiance_stc # m^2                

df['Area'] = df['Area'].fillna(0)


# In[3.5]:
'''
for year, row in df.iterrows():
    print("****")
    print(year)
    print(np.clip(df.index - year, 0, np.inf))
    print(df.index - year)
# In[3.6]:

# QUICK AND DIRTY PDF:
i=0  # Generation 0 
waste2w = iA *weibull_pdf(alpha, beta)(np.clip(range(0-i,len(df)-i),0, np.inf))
    
# Summing same PDF of 200 + PDF of 200 vs PDF of 400
plt.plot(waste2w+waste2w)
plt.plot(waste4w)

'''

# In[3]:
    # Modifications for TEST
    
df['Area'][10] = df['Area'][0]
df['Area'][1] = df['Area'][0]
df['t50'][1] = df['t50'][0]
df['t90'][1] = df['t90'][0]
df['mod_Repairing'] = .30
df['mod_Repairing'][4] = .90
df['mod_lifetime'] = 14.0
df['mod_Repowering'] = 0.0

# In[4]:
#generation is an int 0,1,2,.... etc.
Generation_Disposed_byYear = []
Generation_Active_byYear= []
Generation_Power_byYear = []
df['Cumulative_Area_disposedby_Failure'] = 0
df['Cumulative_Area_disposedby_Degradation'] = 0
df['Cumulative_Area_disposed'] = 0
df['Cumulative_Active_Area'] = 0
df['Cumulative_Power_[W]'] = 0

for generation, row in df.iterrows(): 

#    generation=0
#    row=df.iloc[generation]
    
    t50, t90 = row['t50'], row['t90']
    f = weibull_cdf(**weibull_params({t50: 0.50, t90: 0.90}))
    x = np.clip(df.index - generation, 0, np.inf)
    cdf = list(map(f, x))
   # pdf = [0] + [j - i for i, j in zip(cdf[: -1], cdf[1 :])]

    activearea = row['Area']
    if np.isnan(activearea):
        activearea=0
        
    activeareacount = []
    areadisposed_failure = []
    areadisposed_degradation = []

    areapowergen = []
    active=-1
    disposed_degradation=0
    for age in range(len(cdf)):
        disposed_degradation=0
        if cdf[age] == 0.0:
            activeareacount.append(0)
            areadisposed_failure.append(0)
            areadisposed_degradation.append(0)
            areapowergen.append(0)
        else:
            active += 1
            activeareaprev = activearea                            
            activearea = activearea*(1-cdf[age]*(1-df.iloc[age]['mod_Repairing']))
            areadisposed_failure.append(activeareaprev-activearea)
            if age == row['mod_lifetime']+generation:
                activearea_temp = activearea
                activearea = 0+activearea*df.iloc[age]['mod_Repowering']
                disposed_degradation = activearea_temp-activearea
            areadisposed_degradation.append(disposed_degradation)
            activeareacount.append(activearea)
            areapowergen.append(activearea*row['mod_eff']*0.01*irradiance_stc*(1-row['mod_degradation']/100)**active)                            
    
    try:
        # becuase the clip starts with 0 for the installation year, identifying installation year
        # and adding initial area
        fixinitialareacount = next((i for i, e in enumerate(x) if e), None) - 1
        activeareacount[fixinitialareacount] = activeareacount[fixinitialareacount]+row['Area']    
        areapowergen[fixinitialareacount] = (activeareacount[fixinitialareacount] +  
                             row['Area'] * row['mod_eff'] *0.01 * irradiance_stc)
    except:
        print("Issue on initial area fix")
        print("gen", generation)
        

#   area_disposed_of_generation_by_year = [element*row['Area'] for element in pdf]
    df['Cumulative_Area_disposedby_Failure'] += areadisposed_failure
    df['Cumulative_Area_disposedby_Degradation'] += areadisposed_degradation
    df['Cumulative_Area_disposed'] += areadisposed_failure
    df['Cumulative_Area_disposed'] += areadisposed_degradation
    
    
    df['Cumulative_Active_Area'] += activeareacount
    df['Cumulative_Power_[W]'] += areapowergen
    Generation_Disposed_byYear.append([x + y for x, y in zip(areadisposed_failure, areadisposed_degradation)])
    Generation_Active_byYear.append(activeareacount)
    Generation_Power_byYear.append(areapowergen)

FailuredisposalbyYear = pd.DataFrame(Generation_Disposed_byYear, columns = df.index, index = df.index)
FailuredisposalbyYear = FailuredisposalbyYear.add_prefix("Failed_on_Year_")

try:
    df = df[df.columns.drop(list(df.filter(regex='Failed_on_Year_')))]
except:
    print("First Run")

df = df.join(FailuredisposalbyYear)

# In[5]:
    
filter_col = [col for col in df if col.startswith('Failed_on_Year_')]
print(df[filter_col].sum(axis=1))

# In[6]:
    
filter_col = [col for col in df if col.startswith('Failed_on_Year_')]
EOL = df[filter_col]
df['mod_EOL_collection_eff'] = 80.0 
df['mod_EOL_collection_eff'][2] = 20.0 
df['mod_EOL_collected_recycled'] = 50.0
df['mod_EOL_collected_recycled'][2] = 100.0


# This Multiplication pattern goes through Module and then material.
# It is for processes that depend on each year as they improve, i.e. 
# Collection Efficiency,
#
# [  G1_1   G1_2    G1_3   G2_4 ...]       [N1
# [    0    G2_1    G2_2   G2_3 ...]   X    N2
# [    0      0     G3_1   G3_2 ...]        N3
#                                           N4]
#
#      EQUAL
# EOL_Collected =
# [  G1_1*N1   G1_2 *N2   G1_3 *N3   G2_4 *N4 ...]
# [    0       G2_1 *N2   G2_2 *N3   G2_3 *N4 ...]
# [    0        0         G3_1 *N3   G3_2 *N4 ...]        
#

EOL_Collected = EOL.mul(df['mod_EOL_collection_eff'].values*0.01)
df['EoL_Collected'] = list(EOL_Collected.sum())
landfill_Collection = EOL.mul(1-(df['mod_EOL_collection_eff'].values*0.01)) 
df['EoL_NotCollected'] = list(landfill_Collection.sum())

EOL_Recycled = EOL_Collected.mul(df['mod_EOL_collected_recycled'].values*0.01)
df['EoL_Recycled'] = list(EOL_Recycled.sum())
EOL_NotRecycled_Landfilled = EOL_Collected.mul((1-df['mod_EOL_collected_recycled'].values*0.01))
df['EoL_NotRecycled_Landfilled'] = list(EOL_NotRecycled_Landfilled.sum())

# MATERIAL LAYER NOW

dm = r1.scenario['standard'].material['glass'].materialdata
dm['mat_massperm2'] = 10.0
dm['mat_massperm2'][1] = 0.5
dm['mat_EOL_collected_Recycled'] = 100.0
dm['mat_EOL_Recycled_into_HQ'] = 10.0

# SWITCH TO MASS UNITS FOR THE MATERILA NOW:
# THIS IS DIFFERENT MULTIPLICATION THAN THE REST
# BECAUSE IT DEPENDS TO THE ORIGINAL MASS OF EACH MODULE WHEN INSTALLED
# [M1  * [  G1_1   G1_2    G1_3   G2_4 ...]
#  M2     [    0    G2_1    G2_2   G2_3 ...]
#  M3]    [    0      0     G3_1   G3_2 ...]
# 
#           EQUAL
# mat_EOL_sentoRecycling = 
#     [  G1_1*M1   G1_2*M1    G1_3*M1   G2_4*M1 ...]
#     [    0       G2_1*M2    G2_2*M2   G2_3*M2 ...]
#     [    0           0      G3_1*M3   G3_2*M3 ...]
#

mat_modules_EOL_sentoRecycling = EOL_Recycled.multiply(dm['mat_massperm2'], axis=0)
dm['mat_modules_NotRecycled'] = list(EOL_NotRecycled_Landfilled.multiply(dm['mat_massperm2'], axis=0).sum())
dm['mat_modules_NotCollected'] = list(landfill_Collection.multiply(dm['mat_massperm2'], axis=0).sum())
                   
                                                            
# mat_EOL_collected_Recycled CHANGE NAME
# chnge also landfill_material_EOL_NotRecycled_Landfilled 
mat_EOL_sento_Recycling = mat_modules_EOL_sentoRecycling.mul(dm['mat_EOL_collected_Recycled'].values*0.01)
dm['mat_EOL_sento_Recycling'] = list(mat_EOL_sento_Recycling.sum())
landfill_material_EOL_NotRecycled_Landfilled = mat_modules_EOL_sentoRecycling.mul(1-(dm['mat_EOL_collected_Recycled'].values*0.01))
dm['mat_EOL_NotRecycled_Landfilled'] = list(landfill_material_EOL_NotRecycled_Landfilled.sum())

mat_EOL_Recycled_Succesfully = mat_EOL_sento_Recycling.mul(dm['mat_EOL_collected_Recycled'].values*0.01)
dm['mat_EOL_Recycled'] = list(mat_EOL_Recycled_Succesfully.sum())
landfill_material_EOL_Recyled_Losses_Landfilled = mat_EOL_sento_Recycling.mul(1-(dm['mat_EOL_collected_Recycled'].values*0.01))
dm['mat_EOL_Recycled_Losses_Landfilled'] = list(landfill_material_EOL_Recyled_Losses_Landfilled.sum())


mat_EOL_Recycled_HQ = mat_EOL_Recycled_Succesfully.mul(dm['mat_EOL_Recycled_into_HQ'].values*0.01)
dm['mat_EoL_Recycled_into_HQ'] = list(mat_EOL_Recycled_HQ.sum())
mat_EOL_Recycled_OQ = mat_EOL_Recycled_Succesfully.mul(1-(dm['mat_EOL_Recycled_into_HQ'].values*0.01))
dm['mat_EoL_Recycled_into_OQ'] = list(mat_EOL_Recycled_OQ.sum())

mat_EOL_Recycled_HQ_into_MFG = mat_EOL_Recycled_HQ.mul(dm['mat_EOL_RecycledHQ_Reused4MFG'].values*0.01)
dm['mat_EoL_Recycled_HQ_into_MFG'] = list(mat_EOL_Recycled_HQ_into_MFG.sum())
mat_EOL_Recycled_HQ_into_OU = mat_EOL_Recycled_HQ.mul(1-(dm['mat_EOL_RecycledHQ_Reused4MFG'].values*0.01))
dm['mat_EOL_Recycled_HQ_into_OU'] = list(mat_EOL_Recycled_HQ_into_OU.sum())

# BULK Calculations Now
dm['mat_Manufactured'] = df['Area'] * dm['mat_massperm2']
dm['mat_Manufacturing_Input'] = dm['mat_Manufactured'] / (dm['material_MFG_eff'] * 0.01)
dm['mat_MFG_Scrap'] = dm['mat_Manufactured'] - dm['mat_Manufacturing_Input']
dm['mat_MFG_Scrap_Sentto_Recycling'] = dm['mat_MFG_Scrap'] * dm['mat_MFG_scrap_recycled'] * 0.01
dm['mat_MFG_Scrap_Landfilled'] = dm['mat_MFG_Scrap'] - dm['mat_MFG_Scrap_Sentto_Recycling'] 
dm['mat_MFG_Scrap_Recycled'] = (dm['mat_MFG_Scrap_Sentto_Recycling'] *
                                                 dm['mat_MFG_scrap_recycling_eff'] * 0.01)
dm['mat_MFG_Scrap_Recycled_Losses_Landfilled'] = (dm['mat_MFG_Scrap_Sentto_Recycling'] - 
                                                          dm['mat_MFG_Scrap_Recycled'])
dm['mat_MFG_Recycled_into_HQ'] = (dm['mat_MFG_Scrap_Recycled'] * 
                                        dm['mat_MFG_scrap_Recycled_into_HQ'] * 0.01)
dm['mat_MFG_Recycled_into_OQ'] = dm['mat_MFG_Scrap_Recycled'] - dm['mat_MFG_Recycled_into_HQ']
dm['mat_MFG_Recycled_HQ_into_MFG'] = (dm['mat_MFG_Recycled_into_HQ'] * 
                          dm['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] * 0.01)
dm['mat_MFG_Recycled_HQ_into_OU'] = dm['mat_MFG_Recycled_into_HQ'] - dm['mat_MFG_Recycled_HQ_into_MFG']
dm['mat_Virgin_Stock'] = dm['mat_Manufacturing_Input'] - dm['mat_EoL_Recycled_HQ_into_MFG'] - dm['mat_MFG_Recycled_HQ_into_MFG']
 
# Add Wastes
dm['mat_Total_EoL_Landfilled'] = (dm['mat_modules_NotCollected'] + 
                                  dm['mat_modules_NotRecycled'] +
                                  dm['mat_EOL_NotRecycled_Landfilled'] +
                                  dm['mat_EOL_Recycled_Losses_Landfilled'])      

dm['mat_Total_MFG_Landfilled'] = (dm['mat_MFG_Scrap_Landfilled'] + 
                                 dm['mat_MFG_Scrap_Recycled_Losses_Landfilled'])

dm['mat_Total_Landfilled'] = (dm['mat_Total_EoL_Landfilled'] + 
                              dm['mat_Total_MFG_Landfilled'])

dm['mat_Total_Recycled_OU'] = (dm['mat_EoL_Recycled_into_OQ'] + 
                               dm['mat_EOL_Recycled_HQ_into_OU'] + 
                               dm['mat_MFG_Recycled_into_OQ'] + 
                               dm['mat_MFG_Recycled_HQ_into_OU'])
