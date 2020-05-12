# -*- coding: utf-8 -*-
"""
Created on Fri May  8 06:11:39 2020

@author: sayala
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
import datetime

font = {'family' : 'arial',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

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

def sens_lifetime(df, lifetime_increase=1.3, year_increase=2025):
    '''
    Modifies baseline scenario for evaluatig sensitivity of lifetime parameter.
    t50 and t90 reliability years get incresed by lifetime_increase parameter
    starting the year_increase year specified. 
    '''

    current_year = int(datetime.datetime.now().year)
    
    if current_year > year_increase:
        print("Error. Increase Year is before current year")
        return
    
    #df[df.index > 2000]['Reliability_t50_[years]'].apply(lambda x: x*1.3)
    df['Reliability_t50_[years]'] = df['Reliability_t50_[years]'].astype(float)
    df['Reliability_t90_[years]'] = df['Reliability_t90_[years]'].astype(float)
    df.loc[df.index > year_increase, 'Reliability_t50_[years]'] = df[df.index > current_year]['Reliability_t50_[years]'].apply(lambda x: x*lifetime_increase)
    df.loc[df.index > year_increase, 'Reliability_t90_[years]'] = df[df.index > current_year]['Reliability_t90_[years]'].apply(lambda x: x*lifetime_increase)
    
    return df

def sens_ManufacturingYield(df, target_efficiency = 95.0, goal_year = 2030):
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


def sens_ManufacturingRecycling(df, target_recycling = 95.0, goal_year = 2030):
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

def sens_PanelEff(df, target_panel_eff= 25.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase in panel efficiencies.  
    Increases Efficiency_[%] from current year until goal_year by linear interpolation until
    reaching the target_panel_eff.
    
    Inputs
    ------
    df (dataframe) : dataframe to be modified
    target_panel_eff (float) : target panel efficiency in percentage to be reached. i.e., 25.0 .
    goal_year : year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df (dataframe) : modified dataframe.
    
    '''
   
    current_year = int(datetime.datetime.now().year)
    
    if current_year > goal_year:
        print("Error. Goal Year is before current year")
        return
     
    df['Efficiency_[%]']=df['Efficiency_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'Efficiency_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'Efficiency_[%]'] = target_panel_eff
    df['Efficiency_[%]'] = df['Efficiency_[%]'].interpolate()

    return df

def sens_ManufacturingRecyclingEff(df, target_recycling_eff = 95.0, goal_year = 2030, start_year = None):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of manufacturing scrap recycling efficiency.  
    Increases ``Manufacturing_Scrap_Recycling_Efficiency_[%]`` from current year until ``goal_year`` by linear interpolation until
    reaching the ``target_recycling_eff``.
    
    Inputs
    ------
    df : dataframe
        Dataframe to be modified
    target_recycling_eff : float
        Target recovery value in percentage to be reached. i.e., 95.0 .
    goal_year : int
        Year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe
        Modified dataframe.
    
    '''

    if start_year is None:
        start_year = int(datetime.datetime.now().year) # Setting to current_year
    
    if start_year > goal_year:
        print("Error. Goal Year is before start of the change requested.")
        return
     
    if 0 < abs(target_recycling_eff) < 1:  # checking it is not 0.95 but 95% i.e.
        print("Warning: target_recyling_eff value is between 0 and 1; it has been"
              "multiplied by 100% assuming it was a percentage in decimal form.")
        target_recycling_eff = target_recycling_eff*100
        
    if target_recycling_eff > 100 or target_recycling_eff < 0:
        print("Warning: target_recycling_eff is out of range. Input value between"
              "0 and 100")
        return
        
    df['Manufacturing_Scrap_Recycling_Efficiency_[%]']=df['Manufacturing_Scrap_Recycling_Efficiency_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > start_year), 'Manufacturing_Scrap_Recycling_Efficiency_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'Manufacturing_Scrap_Recycling_Efficiency_[%]'] = target_recycling_eff
    df['Manufacturing_Scrap_Recycling_Efficiency_[%]'] = df['Manufacturing_Scrap_Recycling_Efficiency_[%]'].interpolate()

    return df

def sens_ManufacturingHQRecycling(df, target_hq_recycling = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increasing the percentage of manufacturing scrap recyclied into high quality material.  
    Increases Manufacturing_Scrap_Recycled_into_HighQuality_[%] from current year until goal_year by linear interpolation until
    reaching the target_hq_recycling.

    Datafframe is obtiane from :py:func:`~CEMFC.calculateMF`      
    
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
     
    df['Manufacturing_Scrap_Recycled_into_HighQuality_[%]']=df['Manufacturing_Scrap_Recycled_into_HighQuality_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'Manufacturing_Scrap_Recycled_into_HighQuality_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'Manufacturing_Scrap_Recycled_into_HighQuality_[%]'] = target_hq_recycling
    df['Manufacturing_Scrap_Recycled_into_HighQuality_[%]'] = df['Manufacturing_Scrap_Recycled_into_HighQuality_[%]'].interpolate()

    return df

def sens_ManufacturingHQRecyclingEff(df, target_hq_efficiency = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of Manufacturing scrap recycling into high quality yeild efficiency. 
    Increases Manufacturing_Scrap_Recycled_HighQuality_Reused_for_Manufacturing_[%] from current year until goal_year by linear interpolation until
    reaching the target_hq_efficiency.
    
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
     
    df['Manufacturing_Scrap_Recycled_HighQuality_Reused_for_Manufacturing_[%]']=df['Manufacturing_Scrap_Recycled_HighQuality_Reused_for_Manufacturing_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'Manufacturing_Scrap_Recycled_HighQuality_Reused_for_Manufacturing_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'Manufacturing_Scrap_Recycled_HighQuality_Reused_for_Manufacturing_[%]'] = target_hq_efficiency
    df['Manufacturing_Scrap_Recycled_HighQuality_Reused_for_Manufacturing_[%]'] = df['Manufacturing_Scrap_Recycled_HighQuality_Reused_for_Manufacturing_[%]'].interpolate()

    return df

def sens_EOLCollection(df, target_loss = 0.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to decrease of end of life collection loss percentage.  
    Decreases EOL_Collection_Losses_[%] from current year until goal_year by linear interpolation until
    reaching the target_loss.
    
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
     
    df['EOL_Collection_Losses_[%]']=df['EOL_Collection_Losses_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'EOL_Collection_Losses_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'EOL_Collection_Losses_[%]'] = target_loss
    df['EOL_Collection_Losses_[%]'] = df['EOL_Collection_Losses_[%]'].interpolate()

    return df

def EOLRecycling(df, target_recycling = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increase of EOL percentage recycled.  
    Increases EOL_Collected_Material_Percentage_Recycled_[%] from current year until goal_year by linear interpolation until
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
     
    df['EOL_Collected_Material_Percentage_Recycled_[%]']=df['EOL_Collected_Material_Percentage_Recycled_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'EOL_Collected_Material_Percentage_Recycled_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'EOL_Collected_Material_Percentage_Recycled_[%]'] = target_recycling
    df['EOL_Collected_Material_Percentage_Recycled_[%]'] = df['EOL_Collected_Material_Percentage_Recycled_[%]'].interpolate()

    return df

def sens_EOLRecyclingYield(df, target_efficiency = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of end of life recycling yeild. 
    Increases EOL_Recycling_Efficiency_[%] from current year until goal_year by linear interpolation until
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
     
    df['EOL_Recycling_Efficiency_[%]']=df['EOL_Recycling_Efficiency_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'EOL_Recycling_Efficiency_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'EOL_Recycling_Efficiency_[%]'] = target_efficiency
    df['EOL_Recycling_Efficiency_[%]'] = df['EOL_Recycling_Efficiency_[%]'].interpolate()

    return df

def sens_EOLHQRecycling(df, target_recycling = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of end of life high quality recycling percentage.  
    Increases EOL_Recycled_Material_into_HighQuality_[%] from current year until goal_year by linear interpolation until
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
     
    df['EOL_Recycled_Material_into_HighQuality_[%]']=df['EOL_Recycled_Material_into_HighQuality_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'EOL_Recycled_Material_into_HighQuality_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'EOL_Recycled_Material_into_HighQuality_[%]'] = target_recycling
    df['EOL_Recycled_Material_into_HighQuality_[%]'] = df['EOL_Recycled_Material_into_HighQuality_[%]'].interpolate()

    return df

def sens_EOLHQRecyclingYield(df, target_efficiency = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of end of life high quality recycling efficiency. 
    Increases EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%] efficiecny from current year until goal_year by linear interpolation until
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
     
    df['EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%]']=df['EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%]'] = target_efficiency
    df['EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%]'] = df['EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%]'].interpolate()

    return df

def sens_ReUse(df, target_reuse = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increase of percent of end of life panels that find a second life.  
    Increases Repowering_of_Failed_Modules_[%] from current year until goal_year by linear interpolation until
    reaching the target_reuse.
    
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
     
    df['Repowering_of_Failed_Modules_[%]']=df['Repowering_of_Failed_Modules_[%]'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'Repowering_of_Failed_Modules_[%]'] = np.nan
    df.loc[df.index >= goal_year , 'Repowering_of_Failed_Modules_[%]'] = target_reuse
    df['Repowering_of_Failed_Modules_[%]'] = df['Repowering_of_Failed_Modules_[%]'].interpolate()

    return df

