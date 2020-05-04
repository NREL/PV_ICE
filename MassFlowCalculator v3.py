#!/usr/bin/env python
# coding: utf-8

# # MASS FLOW CALCULATOR v2
# 
# Streamlined to read from the Excel.

# # Preamble and definitions

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
import datetime

get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


font = {'family' : 'arial',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)


# In[4]:


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


# In[5]:


def calculateMassFlow(df, thickness_glass = 3.5e-3, debugflag=False):
    '''
    Function takes as input a baseline dataframe already imported, with the right number of columns and content. It returns the dataframe
    with all the added calculation columns.
    
    '''

    
    # Constants
    irradiance_stc = 1000 # W/m^2
    density_glass = 2500 # kg/m^3    

    # Renaming and re-scaling
    df['New_Installed_Capacity_[MW]'] = df['New_Installed_Capacity_[MW]']*1e6
    df['t50'] = df['Reliability_t50_[years]']
    df['t90'] = df['Reliability_t90_[years]']
    
    # Calculating Area and Mass
    df['Area'] = df['New_Installed_Capacity_[MW]']/(df['Efficiency_[%]']*0.01)/irradiance_stc # m^2
    df['Mass_Glass'] = df['Area']*thickness_glass*density_glass
    
    # Applying Weibull Disposal Function
    df['disposal_function'] = [
    weibull_cdf(**weibull_params({t50: 0.5, t90: 0.9}))
    for t50, t90
    in zip(df['t50'], df['t90'])
    ]
    
    # Calculating Wast by Generation by Year, and Cumulative Waste by Year.
    Area_Disposed_GenbyYear = []
    df['Cumulative_Waste_Glass'] = 0

    for year, row in df.iterrows(): 

        t50, t90 = row['t50'], row['t90']
        f = weibull_cdf(**weibull_params({t50: 0.50, t90: 0.90}))
        x = np.clip(df.index - year, 0, np.inf)
        cdf = list(map(f, x))
        pdf = [0] + [j - i for i, j in zip(cdf[: -1], cdf[1 :])]
        area_disposed_of_generation_by_year = [element*row['Mass_Glass'] for element in pdf]
        df['Cumulative_Waste_Glass'] += area_disposed_of_generation_by_year
        Area_Disposed_GenbyYear.append(area_disposed_of_generation_by_year)

    
    # Making Table to Show Observations
    if debugflag:
        WasteGenerationbyYear = pd.DataFrame(Area_Disposed_GenbyYear, columns = df.index, index = df.index)
        WasteGenerationbyYear = WasteGenerationbyYear.add_prefix("Disposed_on_Year_")
        df = df.join(WasteGenerationbyYear)
    
    
    # Calculations of Repowering and Adjusted EoL Waste Glass
    df['Repowered_Modules_Glass'] = df['Cumulative_Waste_Glass'] * df['Repowering_of_Failed_Modules_[%]'] * 0.01
    df['EoL_Waste_Glass'] = df['Cumulative_Waste_Glass'] - df['Repowered_Modules_Glass']

    
    # Installed Capacity
    df['installedCapacity_glass'] = 0.0
    df['installedCapacity_glass'][df.index[0]] = ( df['Mass_Glass'][df.index[0]] - 
                                                 df['EoL_Waste_Glass'][df.index[0]] )

    for i in range (1, len(df)):
        year = df.index[i]
        prevyear = df.index[i-1]
        df[f'installedCapacity_glass'][year] = (df[f'installedCapacity_glass'][prevyear]+
                                               df[f'Mass_Glass'][year] - 
                                                df['EoL_Waste_Glass'][year] )

    # Other calculations of the Mass Flow
    df['EoL_CollectionLost_Glass'] =  df['EoL_Waste_Glass']* df['EOL_Collection_Losses_[%]'] * 0.01

    df['EoL_Collected_Glass'] =  df['EoL_Waste_Glass'] - df['EoL_CollectionLost_Glass']

    df['EoL_Collected_Recycled'] = df['EoL_Collected_Glass'] * df['EOL_Collected_Material_Percentage_Recycled_[%]'] * 0.01

    df['EoL_Collected_Landfilled'] = df['EoL_Collected_Glass'] - df['EoL_Collected_Glass']


    df['EoL_Recycled_Succesfully'] = df['EoL_Collected_Recycled'] * df['EOL_Recycling_Efficiency_[%]'] * 0.01

    df['EoL_Recycled_Losses_Landfilled'] = df['EoL_Collected_Recycled'] - df['EoL_Recycled_Succesfully'] 

    df['EoL_Recycled_into_HQ'] = df['EoL_Recycled_Succesfully'] * df['EOL_Recycled_Material_into_HighQuality_[%]'] * 0.01

    df['EoL_Recycled_into_Secondary'] = df['EoL_Recycled_Succesfully'] - df['EoL_Recycled_into_HQ']

    df['EoL_Recycled_HQ_into_Manufacturing'] = (df['EoL_Recycled_into_HQ'] * 
                                                      df['EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%]'] * 0.01)

    df['EoL_Recycled_HQ_into_OtherUses'] = df['EoL_Recycled_into_HQ'] - df['EoL_Recycled_HQ_into_Manufacturing']


    df['Manufactured_Input'] = df['Mass_Glass'] / (df['Manufacturing_Material_Efficiency_[%]'] * 0.01)

    df['Manufacturing_Scrap'] = df['Manufactured_Input'] - df['Mass_Glass']

    df['Manufacturing_Scrap_Recycled'] = df['Manufacturing_Scrap'] * df['Manufacturing_Scrap_Percentage_Recycled_[%]'] * 0.01

    df['Manufacturing_Scrap_Landfilled'] = df['Manufacturing_Scrap'] - df['Manufacturing_Scrap_Recycled'] 

    df['Manufacturing_Scrap_Recycled_Succesfully'] = (df['Manufacturing_Scrap_Recycled'] *
                                                     df['Manufacturing_Scrap_Recycling_Efficiency_[%]'] * 0.01)

    df['Manufacturing_Scrap_Recycled_Losses_Landfilled'] = (df['Manufacturing_Scrap_Recycled'] - 
                                                              df['Manufacturing_Scrap_Recycled_Succesfully'])

    df['Manufacturing_Recycled_into_HQ'] = (df['Manufacturing_Scrap_Recycled_Succesfully'] * 
                                            df['Manufacturing_Scrap_Recycled_into_HighQuality_[%]'] * 0.01)

    df['Manufacturing_Recycled_into_Secondary'] = df['Manufacturing_Scrap_Recycled_Succesfully'] - df['Manufacturing_Recycled_into_HQ']

    df['Manufacturing_Recycled_HQ_into_Manufacturing'] = (df['Manufacturing_Recycled_into_HQ'] * 
                              df['Manufacturing_Scrap_Recycled_HighQuality_Reused_for_Manufacturing_[%]'] * 0.01)

    df['Manufacutring_Recycled_HQ_into_OtherUses'] = df['Manufacturing_Recycled_into_HQ'] - df['Manufacturing_Recycled_HQ_into_Manufacturing']


    df['Virgin_Stock'] = df['Manufactured_Input'] - df['EoL_Recycled_HQ_into_Manufacturing'] - df['Manufacturing_Recycled_HQ_into_Manufacturing']

    df['Total_EoL_Landfilled_Waste'] = df['EoL_CollectionLost_Glass'] + df['EoL_Collected_Landfilled'] + df['EoL_Recycled_Losses_Landfilled']

    df['Total_Manufacturing_Landfilled_Waste'] = df['Manufacturing_Scrap_Landfilled'] + df['Manufacturing_Scrap_Recycled_Losses_Landfilled']

    df['Total_Landfilled_Waste'] = (df['EoL_CollectionLost_Glass'] + df['EoL_Collected_Landfilled'] + df['EoL_Recycled_Losses_Landfilled'] +
                                    df['Total_Manufacturing_Landfilled_Waste'])

    df['Total_EoL_Recycled_OtherUses'] = (df['EoL_Recycled_into_Secondary'] + df['EoL_Recycled_HQ_into_OtherUses'] + 
                                          df['Manufacturing_Recycled_into_Secondary'] + df['Manufacutring_Recycled_HQ_into_OtherUses'])

    return df


# In[130]:


df = pd.read_excel('baseline_glass.xlsx', index_col='Year')


# In[ ]:


dffull = calculateMassFlow(df)


# ## Comparing Scenarios
# 
# 

# In[77]:


df2 = sens_lifetime(df, 1.3)


# In[74]:


def sens_lifetime(df=df, lifetime_increase=1.3, year_increase=2025):
    '''
    Modifies baseline scenario for evaluatig sensitivity of lifetime parameter.
    t50 and t90 reliability years get incresed by lifetime_increase parameter
    starting the year_increase year specified. 
    '''
    
    #df[df.index > 2000]['Reliability_t50_[years]'].apply(lambda x: x*1.3)
    df['Reliability_t50_[years]'] = df['Reliability_t50_[years]'].astype(float)
    df['Reliability_t90_[years]'] = df['Reliability_t90_[years]'].astype(float)
    df.loc[df.index > year_increase, 'Reliability_t50_[years]'] = df[df.index > current_year]['Reliability_t50_[years]'].apply(lambda x: x*lifetime_increase)
    df.loc[df.index > year_increase, 'Reliability_t90_[years]'] = df[df.index > current_year]['Reliability_t90_[years]'].apply(lambda x: x*lifetime_increase)
    
    return df


# In[146]:


def sens_ManufacturingYield(df=df, target_efficiency = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of Manufacturing Yield efficiency. 
    Increases Manufacturing Yield efficiecny from current year until goal_year by linear interpolation until
    reaching the target_efficiency.
    
    Inputs
    ------
    df (dataframe) : dataframe to be modified
    target_efficiency (float) : target efficiency value in percentage to be reached. i.e., 95.0 .
    goal_year : year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df (dataframe) : modified dataframe.
    
    '''
   
    current_year = int(datetime.datetime.now().year)
    
    if current_year > goal_year:
        print("Error. Goal Year is before current year")
        return
     
    df['Manufacturing_Material_Efficiency_[%]']=df['Manufacturing_Material_Efficiency_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'Manufacturing_Material_Efficiency_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'Manufacturing_Material_Efficiency_[%]'] = target_efficiency
    df['Manufacturing_Material_Efficiency_[%]'] = df['Manufacturing_Material_Efficiency_[%]'].interpolate()

    return df


# In[149]:


def sens_ManufacturingRecycling(df=df, target_recycling = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of Manfuacturing loss percentage recycled.  
    Increases Manufacturing_Scrap_Percentage_Recycled_[%] from current year until goal_year by linear interpolation until
    reaching the target_recovery.
    
    Inputs
    ------
    df (dataframe) : dataframe to be modified
    target_recycling (float) : target recovery value in percentage to be reached. i.e., 95.0 .
    goal_year : year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df (dataframe) : modified dataframe.
    
    '''
   
    current_year = int(datetime.datetime.now().year)
    
    if current_year > goal_year:
        print("Error. Goal Year is before current year")
        return
     
    df['Manufacturing_Scrap_Percentage_Recycled_[%]']=df['Manufacturing_Scrap_Percentage_Recycled_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'Manufacturing_Scrap_Percentage_Recycled_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'Manufacturing_Scrap_Percentage_Recycled_[%]'] = target_recycling
    df['Manufacturing_Scrap_Percentage_Recycled_[%]'] = df['Manufacturing_Scrap_Percentage_Recycled_[%]'].interpolate()

    return df


# ## Waste from Recycling
# Also in development

# In[28]:





# In[69]:


fig, ax = plt.subplots(figsize=(20,10))


plt.stackplot(df.index, df['Virgin_Stock'], df['EoL_Recycled_HQ_into_Manufacturing'], 
              df['Manufacturing_Recycled_HQ_into_Manufacturing'], 
              colors=['blue', 'orange', 'brown'],
             labels=['Virgin_stock','EoL_Recycled_HQ_into_Manufacturing', 
                    'Manufacturing_Recycled_HQ_into_Manufacturing'])
plt.legend()


plt.legend()
plt.ylabel("Glass [kg]")
plt.yscale("log")
plt.xlabel("Year")
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(title='Inputs into to Manufacturing', loc='center left', fontsize='small', ncol=1, shadow=True, fancybox=True, bbox_to_anchor=(1, 0.5))
#ax.legend(title='year installed', loc='upper center', fontsize='small', ncol=3, shadow=True, fancybox=True, bbox_to_anchor=(0.5, 1.05))



# In[72]:


fig, ax = plt.subplots(figsize=(20,10))

plt.stackplot(df.index, df['Manufacturing_Recycled_HQ_into_Manufacturing'], 
              colors=['orange', 'brown'],
             labels=['Manufacturing_Recycled_HQ_into_Manufacturing'])
plt.legend()
plt.ylabel("Glass [kg]")
plt.yscale("log")
plt.xlabel("Year")
plt.ylim([0,10e7])
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(title='Inputs OTHER than Virgin Stock to Manufacturing', loc='center left', fontsize='small', ncol=1, shadow=True, fancybox=True, bbox_to_anchor=(1, 0.5))
#ax.legend(title='year installed', loc='upper center', fontsize='small', ncol=3, shadow=True, fancybox=True, bbox_to_anchor=(0.5, 1.05))


# In[67]:


fig, ax = plt.subplots(figsize=(20,10))

plt.stackplot(df.index, df['EoL_Recycled_HQ_into_Manufacturing'], 
              df['Manufacturing_Recycled_HQ_into_Manufacturing'], 
              colors=['orange', 'brown'],
             labels=['EoL_Recycled_HQ_into_Manufacturing', 
                    'Manufacturing_Recycled_HQ_into_Manufacturing'])
plt.legend()
plt.ylabel("Glass [kg]")
plt.yscale("log")
plt.xlabel("Year")
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(title='Inputs OTHER than Virgin Stock to Manufacturing', loc='center left', fontsize='small', ncol=1, shadow=True, fancybox=True, bbox_to_anchor=(1, 0.5))
#ax.legend(title='year installed', loc='upper center', fontsize='small', ncol=3, shadow=True, fancybox=True, bbox_to_anchor=(0.5, 1.05))


# In[68]:


#plt.plot([], [], color='blue',)
fig, ax = plt.subplots(figsize=(20,10))

plt.stackplot(df.index, df['EoL_CollectionLost_Glass'], 
              df['EoL_Collected_Landfilled'], df['EoL_Recycled_Losses_Landfilled'],
              df['Total_EoL_Recycled_OtherUses'],
              colors=['blue','orange', 'brown', 'red'], 
              labels=['EoL_CollectionLost_Glass', 
                      'EoL_Collected_Landfilled', 'EoL_Recycled_Losses_Landfilled',
                      'Total_EoL_Recycled_OtherUses'])
plt.yscale("log")
plt.xlabel("Year")
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(title='Where the Material EXITS the Loop', loc='center left', fontsize='small', ncol=1, shadow=True, fancybox=True, bbox_to_anchor=(1, 0.5))
#ax.legend(title='year installed', loc='upper center', fontsize='small', ncol=3, shadow=True, fancybox=True, bbox_to_anchor=(0.5, 1.05))
plt.ylabel("Glass [kg]")


# In[ ]:


# Plotting Installed Capacity of Silicon

fig, ax = plt.subplots(figsize=(9, 5))
plt.plot(df.index, df['New_Installed_Capacity_[MW]']/1e6, linewidth=4)
plt.ylabel('Silicon installations [MW]')
ax.set_yscale('log')
pass


# Ploting Silicon Installations vs New Installed Area

fig, ax = plt.subplots(figsize=(9, 5))
plt.plot(df.index, df['Efficiency_[%]']*100, 'g', linewidth=4)
plt.ylabel('Average Module Efficiency [%]')


fig, ax = plt.subplots(figsize=(9, 5))
plt.plot(df.index, df['New_Installed_Capacity_[MW]']/1e6, linewidth=4)
plt.ylabel('Silicon installations [MW]')
ax.set_yscale('log')

fig, ax = plt.subplots(figsize=(9, 5))
plt.plot(df.index, df['area'], 'r', linewidth=4)
plt.ylabel('New Installed Area [$m^2$]')
ax.set_yscale('log')
plt.show()

fig, ax = plt.subplots(figsize=(9, 5))
plt.plot(df.index, df['New_Installed_Capacity_[MW]']/1e6, linewidth=4)
plt.ylabel('Silicon installations [MW]')
ax.set_yscale('log')

ax2=ax.twinx()
ax2.plot(df.index, df['area'], 'r', linewidth=4)
ax2.set_ylabel('New Installed Area [$m^2$]')
ax2.set_yscale('log')
plt.show()

pass





fig, ax = plt.subplots(figsize=(9, 5))
plt.plot(df.index, df['mass_glass']/1000000, color='blue', label='Glass', linewidth=4)
ax.set_ylabel('Glass x 10$^6$ [kg]', color='blue')
ax.tick_params(axis='y', colors='blue')
plt.title("Installed materials' mass")

fig, ax = plt.subplots(figsize=(9, 5))
plt.plot(df.index, df['mass_glass'], color='blue', label='Glass', linewidth=4)
ax.set_ylabel('Glass [kg]', color='blue')
ax.tick_params(axis='y', colors='blue')
ax.set_yscale('log')
plt.title("Installed materials' mass")
pass


fig, ax = plt.subplots(figsize=(9, 7))
plt.plot(df.index, df['t50'], color='purple', label='t50', linewidth=4)
plt.plot(df.index, df['t90'], color='green', label='t90', linewidth=4)
#ax.set_ylabel('T50 (Median Time to Fail) and T90 [Years]')

ybox1 = TextArea("T50 ", textprops=dict(color="purple", size=25,rotation=90,ha='left',va='bottom'))
ybox2 = TextArea("and ",     textprops=dict(color="black", size=25,rotation=90,ha='left',va='bottom'))
ybox3 = TextArea("T90 ", textprops=dict(color="green", size=25,rotation=90,ha='left',va='bottom'))
ybox4 = TextArea("[Years]",     textprops=dict(color="black", size=25,rotation=90,ha='left',va='bottom'))

ybox = VPacker(children=[ybox4, ybox3, ybox2, ybox1],align="bottom", pad=-155, sep=5)

anchored_ybox = AnchoredOffsetbox(loc=8, child=ybox, pad=0., frameon=False, bbox_to_anchor=(-0.12, 0.6), 
                                  bbox_transform=ax.transAxes, borderpad=0.)

ax.add_artist(anchored_ybox)


pass


fig, ax = plt.subplots(figsize=(20,10))
for year, row in df.iterrows():
    t50, t90 = row['t50'], row['t90']
    f = weibull_cdf(**weibull_params({t50: 0.50, t90: 0.90}))
    x = np.clip(df.index - year, 0, np.inf)
    y = list(map(f, x))
    if year%3 != 1:
        continue
    ax.plot(x + year, np.array(y)*row['area'], label=str(year) + ', ' + str(round(row['area'])))
plt.ylim(0, 0.05E7)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(title='Installation Year, Area [m$^2$]', loc='center left', fontsize='small', ncol=2, shadow=True, fancybox=True, bbox_to_anchor=(1, 0.5))
#ax.legend(title='year installed', loc='upper center', fontsize='small', ncol=3, shadow=True, fancybox=True, bbox_to_anchor=(0.5, 1.05))
ax.set_ylabel('Cumulative Area Disposed [m$^2$]')
pass

print("SANITY CHECK OF RESULTS")
print("Sum of WasteGenerationbyYear")
print(WasteGenerationbyYear.sum(axis=0))
print("df [ 'Cumulative_Waste_Area']")
print(df['Cumulative_Waste_Area'])


plt.subplots(figsize=(9, 15))
plt.plot(df['installedCapacity_glass'])
plt.yscale("log")
plt.ylabel("Installed Capacity of Glass, \n Considering new additions and Decommissions [kg]")


# In[ ]:





# In[ ]:




