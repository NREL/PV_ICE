# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 09:58:31 2020

@author: sayala
"""


file = r'C:\Users\Silvana\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_modules_US.csv'
fileglass = r'C:\Users\Silvana\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_material_glass.csv'
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
    alpha = np.asscalar(np.real_if_close(
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



# In[2] : Testing inner C alculate DMF
df = r1.scenario['standard'].data

df['t50'] = 30
df['t90'] = 40
df['mod_lifetime'] = 20  # for easier testing


irradiance_stc = 1000 # W/m^2

# Renaming and re-scaling
df['new_Installed_Capacity_[W]'] = df['new_Installed_Capacity_[MW]']*1e6
df['t50'] = df['mod_reliability_t50']
df['t90'] = df['mod_reliability_t90']

# Calculating Area and Mass
df['Area'] = df['new_Installed_Capacity_[W]']/(df['mod_eff']*0.01)/irradiance_stc # m^2                

# Applying Weibull Disposal Function
df['disposal_function'] = [
weibull_cdf(**weibull_params({t50: 0.5, t90: 0.9}))
for t50, t90
in zip(df['t50'], df['t90'])
]

# Calculating Wast by Generation by Year, and Cumulative Waste by Year.
Generation_Disposed_byYear = []
Generation_Active_byYear= []
Generation_Power_byYear = []

df['Cumulative_Area_disposedby_Failure'] = 0
df['Cumulative_Area_disposedby_Degradation'] = 0
df['Cumulative_Area_disposed'] = 0
df['Cumulative_Active_Area'] = 0
df['Cumulative_Power_[W]'] = 0

# In[3]: 
row = df.iloc[4]
year = row.year

# In[3.4]:
for year, row in df.iterrows(): 

# In[4]:
    
    #row=df.iloc[4]
    #year=row.year  # 1999
    
    t50, t90 = row['t50'], row['t90']
    f = weibull_cdf(**weibull_params({t50: 0.50, t90: 0.90}))
    x = np.clip(df.index - year, 0, np.inf)
    cdf = list(map(f, x))
    pdf = [0] + [j - i for i, j in zip(cdf[: -1], cdf[1 :])]

    activearea = row['Area']
    activeareacount = []
    areadisposed_failure = []
    areadisposed_degradation = []

    areapowergen = []
    active=-1
    activearea2=0
    disposed_degradation=0
    for prob in range(len(cdf)):
        disposed_degradation=0
        if cdf[prob] == 0.0:
            activeareacount.append(0)
            areadisposed_failure.append(0)
            areadisposed_degradation.append(0)
            areapowergen.append(0)
        else:
            active += 1
            activeareaprev = activearea                            
            activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
            areadisposed_failure.append(activeareaprev-activearea)
            if prob == row['mod_lifetime']:
                activearea_temp = activearea
                activearea = 0+activearea*df.iloc[prob]['mod_Repowering']
                disposed_degradation = activearea_temp-activearea
            areadisposed_degradation.append(disposed_degradation)
            activeareacount.append(activearea)
            areapowergen.append(activearea*row['mod_eff']*0.01*irradiance_stc*(1-row['mod_degradation']/100)**active)                            
            
            # m^2 
#                    area_disposed_of_generation_by_year = [element*row['Area'] for element in pdf]
    df['Cumulative_Area_disposedby_Failure'] += areadisposed_failure
    df['Cumulative_Area_disposedby_Degradation'] += areadisposed_degradation
    df['Cumulative_Area_disposed'] += areadisposed_failure
    df['Cumulative_Area_disposed'] += areadisposed_degradation
    
    df['Cumulative_Active_Area'] += activeareacount
    df['Cumulative_Power_[W]'] += areapowergen
    Generation_Disposed_byYear.append(areadisposed_failure)
    Generation_Active_byYear.append(activeareacount)
    Generation_Power_byYear.append(areapowergen)

# In[5]:
    # Making Table to Show Observations
FailuredisposalbyYear = pd.DataFrame(Generation_Disposed_byYear, columns = df.index, index = df.index)
FailuredisposalbyYear = FailuredisposalbyYear.add_prefix("Failed_on_Year_")
df = df.join(FailuredisposalbyYear)