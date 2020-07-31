# -*- coding: utf-8 -*-
"""
Main.py contains the functions to calculate the different quantities of materials
in each step of the process. Reffer to the diagram on Package-Overview for the 
steps considered. 

Support functions include Weibull functions for reliability and failure; also, 
functions to modify baseline values and evaluate sensitivity to the parameters.

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

def calculateMassFlow(df, thickness_glass = 0.0035, debugflag=False):
    '''
    Function takes as input a baseline dataframe already imported, 
    with the right number of columns and content.
    It returns the dataframe with all the added calculation columns.
    
    Parameters
    ------------
    thickness_glass: float
        Glass thickness in m
    
    Returns
    --------
    df: dataframe 
        input dataframe with addeds columns for the calculations of recycled,
        collected, waste, installed area, etc. 
    
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
        df['installedCapacity_glass'][year] = (df[f'installedCapacity_glass'][prevyear]+
                                               df[f'Mass_Glass'][year] - 
                                                df['EoL_Waste_Glass'][year] )

#    df['Area'] = df['New_Installed_Capacity_[MW]']/(df['Efficiency_[%]']*0.01)/irradiance_stc # m^2
#    df['Mass_Glass'] = df['Area']*thickness_glass*density_glass
    df['installedCapacity_MW_glass'] = ( df['installedCapacity_glass'] / (thickness_glass*density_glass) ) *  (df['Efficiency_[%]']*0.01) * irradiance_stc / 1e6

    
    # Other calculations of the Mass Flow
    df['EoL_CollectionLost_Glass'] =  df['EoL_Waste_Glass']* df['EOL_Collection_Losses_[%]'] * 0.01

    df['EoL_Collected_Glass'] =  df['EoL_Waste_Glass'] - df['EoL_CollectionLost_Glass']

    df['EoL_Collected_Recycled'] = df['EoL_Collected_Glass'] * df['EOL_Collected_Material_Percentage_Recycled_[%]'] * 0.01

    df['EoL_Collected_Landfilled'] = df['EoL_Collected_Glass'] - df['EoL_Collected_Recycled']


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

    df['New_Installed_Capacity_[MW]'] = df['New_Installed_Capacity_[MW]']/1e6

    return df

def sens_lifetime(df, lifetime_increase=1.3, year_increase=2025):
    '''
    Modifies baseline scenario for evaluating sensitivity of lifetime parameter.
    t50 and t90 reliability years get incresed by `lifetime_increase` parameter
    starting the `year_increase` year specified. 
    
    Parameters
    ----------
    df : dataframe
        dataframe to be modified
    lifetime_increase : decimal
        Percent increase in decimal (i.e. "1.3" for 30% increase in value) 
        or percent decrease (i.e. "0.3") in expected panel lifetime, relative 
        to the values in df.
    year_increase : 
        the year at which the lifetime increase or decrease occurs
    
    Returns
    --------
    df : dataframe
        dataframe of expected module lifetime increased or decreased at specified year
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

def sens_PanelEff(df, target_panel_eff= 25.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase in panel efficiencies.  
    Increases `Efficiency_[%]` from current year until goal_year by linear interpolation until
    reaching the `target_panel_eff`.
    
    Parameters
    ----------
    df : dataframe
        dataframe to be modified
    target_panel_eff : float
        target panel efficiency in percentage to be reached. i.e., 25.0 .
    goal_year : float
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
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

def sens_ManufacturingYield(df, target_efficiency = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increasing Manufacturing Yield efficiency. 
    Increases `Manufacturing_Material_Efficiency_[%]` from current year 
    until `goal_year` by linear interpolation until
    reaching the `target_efficiency`.
    
    Parameters
    ----------
    df : dataframe 
        dataframe to be modified
    target_efficiency: float
        target efficiency value in percentage to be reached. i.e. 95.0 %.
    goal_year : float
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe
        modified dataframe
    
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
    Increases `Manufacturing_Scrap_Percentage_Recycled_[%]` from current year until `goal_year` by linear interpolation until
    reaching the `target_recovery`.
    
    Parameters
    --------
    df : dataframe
        dataframe to be modified
    target_recycling : float 
        target recovery value in percentage to be reached. i.e., 95.0 %.
    goal_year : float
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    --------
    df : dataframe
        modified dataframe.
    
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

def sens_ManufacturingRecyclingEff(df, target_recycling_eff = 95.0, goal_year = 2030, start_year = None):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of manufacturing scrap recycling efficiency.  
    Increases `Manufacturing_Scrap_Recycling_Efficiency_[%]` from current year until `goal_year` by linear interpolation until
    reaching the `target_recycling_eff`.
    
    Parameters
    -----------
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
    Increases `Manufacturing_Scrap_Recycled_into_HighQuality_[%]` from current year until `goal_year` by linear interpolation until
    reaching the `target_hq_recycling`.

    Datafframe is obtained from :py:func:`~CEMFC.calculateMassFlow`      
    
    Parameters
    -----------
    df : dataframe
        dataframe to be modified
    target_recycling : float
        target recovery value in percentage to be reached. i.e., 95.0 .
    goal_year : float
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe
        modified dataframe.
    
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
    Modifies baseline scenario for evaluating sensitivity to increase of Manufacturing scrap recycling into high quality yeild efficiency. 
    Increases `Manufacturing_Scrap_Recycled_HighQuality_Reused_for_Manufacturing_[%]` from current year until `goal_year` by linear interpolation until
    reaching the `target_hq_efficiency`.
    
    Parameters
    -----------
    df : dataframe
        dataframe to be modified
    target_efficiency : float
        target efficiency value in percentage to be reached. i.e., 95.0 .
    goal_year : float
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe 
        modified dataframe.
    
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
    Modifies baseline scenario for evaluating sensitivity to decrease of end of life collection loss percentage.  
    Decreases `EOL_Collection_Losses_[%]` from current year until `goal_year` by linear interpolation until
    reaching the `target_loss`.
    
    Parameters
    ----------
    df : dataframe 
        dataframe to be modified
    target_recycling : float
        target losses in percentage to be reached. i.e. 5.0 % (lower is more is collected).
    goal_year : float
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe
        modified dataframe.
    
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

def sens_EOLRecycling(df, target_recycling = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increase of EOL percentage recycled.  
    Increases `EOL_Collected_Material_Percentage_Recycled_[%]` from current year until `goal_year` by linear interpolation until
    reaching the `target_recovery`.
    
    Parameters
    -----------
    df : dataframe
        dataframe to be modified
    target_recycling : float
        target percent recycled value in percentage to be reached. i.e., 95.0 %.
        Higher is more of the end of life collection percentage is recycled.
    goal_year : float
        year by which target percent recycled will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe 
        modified dataframe.
    
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
    Modifies baseline scenario for evaluating sensitivity to increase of end of 
    life recycling yeild.     Increases `EOL_Recycling_Efficiency_[%]` from 
    current year until `goal_year` by linear interpolation until
    reaching the `target_efficiency`.
    
    Parameters
    ----------
    df : dataframe
        dataframe to be modified
    target_efficiency : float
        target recycling efficiency value in percentage to be reached. i.e., 95.0 % of material is recovered.
    goal_year : float
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe 
        modified dataframe.
    
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
    Modifies baseline scenario for evaluatig sensitivity to increase of end of 
    life high quality recycling percentage. 
    Increases `EOL_Recycled_Material_into_HighQuality_[%]` from current year 
    until `goal_year` by linear interpolation until
    reaching the `target_recovery`.
    
    Parameters
    ----------
    df : dataframe
        dataframe to be modified
    target_recycling : float
        target recycling percentage to be reached. i.e. 95.0 % of recycled material is recycled into high quality.
    goal_year : float 
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe
        modified dataframe.
    
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
    Modifies baseline scenario for evaluatig sensitivity to increase of end of 
    life high quality recycling efficiency. 
    Increases `EOL_Recycled_HighQuality_Reused_for_Manufacturing_[%]` efficiecny 
    from current year until `goal_year` by linear interpolation until
    reaching the `target_efficiency`.
    
    Parameters
    ----------
    df : dataframe
        dataframe to be modified
    target_efficiency : float 
        target efficiency value in percentage to be reached. i.e., 95.0 %.
    goal_year : float
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe 
        modified dataframe.
    
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
    Modifies baseline scenario for evaluating sensitivity to increase of percent 
    of end of life panels that find a second life.  
    Increases `Repowering_of_Failed_Modules_[%]` from current year 
    until `goal_year` by linear interpolation until
    reaching the `target_reuse`.
    
    Parameters
    ----------
    df : dataframe
        dataframe to be modified
    target_recycling : float
        target recovery value in percentage to be reached. i.e., 95.0 .
    goal_year : float
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe 
        modified dataframe.
    
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


def _modDict(originaldict, moddict):
    '''
    Compares keys in originaldict with moddict and updates values of 
    originaldict to moddict if existing.
    
    Parameters
    ----------
    originaldict : dictionary
        Original dictionary calculated, for example frontscan or backscan dictionaries.
    moddict : dictionary
        Modified dictinoary, for example modscan['x'] = 0 to change position of x.
    
    Returns
    -------
    originaldict : dictionary
        Updated original dictionary with values from moddict.
    '''
    for key in moddict:
        try:
            originaldict[key] = moddict[key]
        except:
            print("Wrong key in modified dictionary")
                
    return originaldict


def calculateLCA(PVarea, modified_impacts=None, printflag = False):
    '''


    '''
    
    if printflag:
        print("Doing calculations of LCA analysis for Silicon Photovoltaic Panels")
    
    

    impacts = {'Acidification':{'UUID':  '75d0c8a2-e466-3bd7-813b-5beef2209330',
                                'Result':  1.29374135667815,
                                'Unit': 'kg SO2' },
                'Carcinogenics':{'UUID':  'a6e5e5d8-a1e5-3c77-8170-586c4fe37514',
                                            'Result':  0.0000231966690476102,
                                            'Unit': 'CTUh' },
                'Ecotoxicity':{'UUID': '338e9370-ceb0-3d18-9d87-5f91feb7829c',
                                            'Result':  5933.77859696668,
                                            'Unit': 'CTUe' },
                'Eutrophication':{'UUID':  '45b8cd56-498a-3c6f-9488-134e951d8c02',
                                'Result':  1.34026194777363,
                                'Unit': 'kg N eq' },
                
                'Fossil fuel depletion':{'UUID': '0e45786f-67fa-3b8a-b8a3-73a7c316434c',
                                'Result': 249.642261689385,
                                'Unit': 'MJ surplus' },
                
                'Global warming':{'UUID':  '31967441-d687-313d-9910-13da3a584ab7',
                                'Result': 268.548841324818,
                                'Unit': 'kg CO2 eq' },
                
                'Non carcinogenics':{'UUID':  'd4827ae3-c873-3ea4-85fb-860b7f3f2dee',
                                'Result': 0.000135331806321799,
                                'Unit': 'CTUh' },
                
                'Ozone depletion':{'UUID': '6c05dad1-6661-35f2-82aa-6e8e6a498aec',
                                'Result':  0.0000310937628622019,
                                'Unit': 'kg CFC-11 eq' },
                
                'Respiratory effects':{'UUID':  'e0916d62-7fbd-3d0a-a4a5-52659b0ac9c1',
                                'Result':  0.373415542664206,
                                'Unit': 'kg PM2.5 eq' },
                'Smog':{'UUID':  '7a149078-e2fd-3e07-a5a3-79035c60e7c3',
                                'Result':  15.35483065, 
                                'Unit': 'kg O3 eq' },
            }
    
    if modified_impacts is not None:
        impacts = _modDict(impacts, modified_impacts)
        if printflag:
            print("Following Modified impacts provided instead of TRACI 2.1 default")
            print(impacts)
            print("")
    else:
        if printflag:
            print("Following TRACI 2.1")

    acidification = impacts['Acidification']['Result']*PVarea
    carcinogenics = impacts['Carcinogenics']['Result']*PVarea
    ecotoxicity  = impacts['Ecotoxicity']['Result']*PVarea
    eutrophication = impacts['Eutrophication']['Result']*PVarea
    fossil_fuel_depletion = impacts['Fossil fuel depletion']['Result']*PVarea
    global_warming = impacts['Global warming']['Result']*PVarea
    non_carcinogenics = impacts['Non carcinogenics']['Result']*PVarea
    ozone_depletion = impacts['Ozone depletion']['Result']*PVarea
    respiratory_effects = impacts['Respiratory effects']['Result']*PVarea
    smog = impacts['Smog']['Result']*PVarea
    

    
    if printflag:
        print("RESULTS FOR PV AREA ", PVarea, " m2 ")
        print("****************************************")
        print('Acidification: ', round(impacts['Acidification']['Result']*PVarea, 2), ' ', impacts['Acidification']['Unit'])
        print('Carcinogenics: ', round(impacts['Carcinogenics']['Result']*PVarea, 2), ' ', impacts['Carcinogenics']['Unit'])
        print('Ecotoxicity: ', round(impacts['Ecotoxicity']['Result']*PVarea, 2), ' ', impacts['Ecotoxicity']['Unit'])
        print('Eutrophication: ', round(impacts['Eutrophication']['Result']*PVarea, 2), ' ', impacts['Eutrophication']['Unit'])
        print('Fossil fuel depletion: ', round(impacts['Fossil fuel depletion']['Result']*PVarea, 2), ' ', impacts['Fossil fuel depletion']['Unit'])
        print('Global warming: ', round(impacts['Global warming']['Result']*PVarea, 2), ' ', impacts['Global warming']['Unit'])
        print('Non carcinogenics: ', round(impacts['Non carcinogenics']['Result']*PVarea, 2), ' ', impacts['Non carcinogenics']['Unit'])
        print('Ozone depletion: ', round(impacts['Ozone depletion']['Result']*PVarea, 2), ' ', impacts['Ozone depletion']['Unit'])
        print('Respiratory effects: ', round(impacts['Respiratory effects']['Result']*PVarea, 2), ' ', impacts['Respiratory effects']['Unit'])
        print('Smog: ', round(impacts['Smog']['Result']*PVarea, 2), ' ', impacts['Smog']['Unit'])
        
    return (acidification, carcinogenics, ecotoxicity, eutrophication, 
                fossil_fuel_depletion, global_warming,
                non_carcinogenics, ozone_depletion, respiratory_effects, smog)