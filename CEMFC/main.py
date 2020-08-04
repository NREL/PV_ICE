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

def calculateMassFlow(mod, mat, debugflag=False):
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

    df = pd.concat([mod, mat], axis=1, sort=False)
    # Constants
    irradiance_stc = 1000 # W/m^2
    density_glass = 2500 # kg/m^3    
    thickness_glass = 0.0035

    # Renaming and re-scaling
    df['new_Installed_Capacity_[MW]'] = df['new_Installed_Capacity_[MW]']*1e6
    df['t50'] = df['mod_reliability_t50']
    df['t90'] = df['mod_reliability_t90']
    
    # Calculating Area and Mass
    df['Area'] = df['new_Installed_Capacity_[MW]']/(df['mod_eff']*0.01)/irradiance_stc # m^2
    df['mat_Mass'] = df['Area']*df['mat_massperm2']
    
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
        area_disposed_of_generation_by_year = [element*row['mat_Mass'] for element in pdf]
        df['Cumulative_Waste_Glass'] += area_disposed_of_generation_by_year
        Area_Disposed_GenbyYear.append(area_disposed_of_generation_by_year)

    
    # Making Table to Show Observations
    if debugflag:
        WasteGenerationbyYear = pd.DataFrame(Area_Disposed_GenbyYear, columns = df.index, index = df.index)
        WasteGenerationbyYear = WasteGenerationbyYear.add_prefix("Disposed_on_Year_")
        df = df.join(WasteGenerationbyYear)
    
    
    # Calculations of Repowering and Adjusted EoL Waste Glass
    df['Repowered_Modules_Glass'] = df['Cumulative_Waste_Glass'] * df['mod_repowering'] * 0.01
    df['EoL_Waste_Glass'] = df['Cumulative_Waste_Glass'] - df['Repowered_Modules_Glass']

    
    # Installed Capacity
    df['installedCapacity_glass'] = 0.0
    df['installedCapacity_glass'][df.index[0]] = ( df['mat_Mass'][df.index[0]] - 
                                                 df['EoL_Waste_Glass'][df.index[0]] )

    for i in range (1, len(df)):
        year = df.index[i]
        prevyear = df.index[i-1]
        df['installedCapacity_glass'][year] = (df[f'installedCapacity_glass'][prevyear]+
                                               df[f'mat_Mass'][year] - 
                                                df['EoL_Waste_Glass'][year] )

#    df['Area'] = df['new_Installed_Capacity_[MW]']/(df['mod_eff']*0.01)/irradiance_stc # m^2
#    df['mat_Mass'] = df['Area']*thickness_glass*density_glass
    df['installedCapacity_MW_glass'] = ( df['installedCapacity_glass'] / (thickness_glass*density_glass) ) *  (df['mod_eff']*0.01) * irradiance_stc / 1e6

    
    # Other calculations of the Mass Flow
    df['EoL_CollectionLost_Glass'] =  df['EoL_Waste_Glass']* df['mod_EOL_collection_losses'] * 0.01

    df['EoL_Collected_Glass'] =  df['EoL_Waste_Glass'] - df['EoL_CollectionLost_Glass']

    df['EoL_Collected_Recycled'] = df['EoL_Collected_Glass'] * df['mod_EOL_collected_recycled'] * 0.01

    df['EoL_Collected_Landfilled'] = df['EoL_Collected_Glass'] - df['EoL_Collected_Recycled']


    df['EoL_Recycled_Succesfully'] = df['EoL_Collected_Recycled'] * df['mat_EOL_Recycling_eff'] * 0.01

    df['EoL_Recycled_Losses_Landfilled'] = df['EoL_Collected_Recycled'] - df['EoL_Recycled_Succesfully'] 

    df['EoL_Recycled_into_HQ'] = df['EoL_Recycled_Succesfully'] * df['mat_EOL_Recycled_into_HQ'] * 0.01

    df['EoL_Recycled_into_Secondary'] = df['EoL_Recycled_Succesfully'] - df['EoL_Recycled_into_HQ']

    df['EoL_Recycled_HQ_into_MFG'] = (df['EoL_Recycled_into_HQ'] * 
                                                      df['mat_EOL_RecycledHQ_Reused4MFG'] * 0.01)

    df['EoL_Recycled_HQ_into_OtherUses'] = df['EoL_Recycled_into_HQ'] - df['EoL_Recycled_HQ_into_MFG']


    df['Manufactured_Input'] = df['mat_Mass'] / (df['mat_MFG_eff'] * 0.01)

    df['MFG_Scrap'] = df['Manufactured_Input'] - df['mat_Mass']

    df['MFG_Scrap_Recycled'] = df['MFG_Scrap'] * df['mat_MFG_scrap_recycled'] * 0.01

    df['MFG_Scrap_Landfilled'] = df['MFG_Scrap'] - df['MFG_Scrap_Recycled'] 

    df['MFG_Scrap_Recycled_Succesfully'] = (df['MFG_Scrap_Recycled'] *
                                                     df['mat_MFG_scrap_recycling_eff'] * 0.01)

    df['MFG_Scrap_Recycled_Losses_Landfilled'] = (df['MFG_Scrap_Recycled'] - 
                                                              df['MFG_Scrap_Recycled_Succesfully'])

    df['MFG_Recycled_into_HQ'] = (df['MFG_Scrap_Recycled_Succesfully'] * 
                                            df['mat_MFG_scrap_Recycled_into_HQ'] * 0.01)

    df['MFG_Recycled_into_Secondary'] = df['MFG_Scrap_Recycled_Succesfully'] - df['MFG_Recycled_into_HQ']

    df['MFG_Recycled_HQ_into_MFG'] = (df['MFG_Recycled_into_HQ'] * 
                              df['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] * 0.01)

    df['MFG_Recycled_HQ_into_OtherUses'] = df['MFG_Recycled_into_HQ'] - df['MFG_Recycled_HQ_into_MFG']


    df['Virgin_Stock'] = df['Manufactured_Input'] - df['EoL_Recycled_HQ_into_MFG'] - df['MFG_Recycled_HQ_into_MFG']

    df['Total_EoL_Landfilled_Waste'] = df['EoL_CollectionLost_Glass'] + df['EoL_Collected_Landfilled'] + df['EoL_Recycled_Losses_Landfilled']

    df['Total_MFG_Landfilled_Waste'] = df['MFG_Scrap_Landfilled'] + df['MFG_Scrap_Recycled_Losses_Landfilled']

    df['Total_Landfilled_Waste'] = (df['EoL_CollectionLost_Glass'] + df['EoL_Collected_Landfilled'] + df['EoL_Recycled_Losses_Landfilled'] +
                                    df['Total_MFG_Landfilled_Waste'])

    df['Total_EoL_Recycled_OtherUses'] = (df['EoL_Recycled_into_Secondary'] + df['EoL_Recycled_HQ_into_OtherUses'] + 
                                          df['MFG_Recycled_into_Secondary'] + df['MFG_Recycled_HQ_into_OtherUses'])

    df['new_Installed_Capacity_[MW]'] = df['new_Installed_Capacity_[MW]']/1e6

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
    
    #df[df.index > 2000]['mod_reliability_t50'].apply(lambda x: x*1.3)
    df['mod_reliability_t50'] = df['mod_reliability_t50'].astype(float)
    df['mod_reliability_t90'] = df['mod_reliability_t90'].astype(float)
    df.loc[df.index > year_increase, 'mod_reliability_t50'] = df[df.index > current_year]['mod_reliability_t50'].apply(lambda x: x*lifetime_increase)
    df.loc[df.index > year_increase, 'mod_reliability_t90'] = df[df.index > current_year]['mod_reliability_t90'].apply(lambda x: x*lifetime_increase)
    
    return df

def sens_PanelEff(df, target_panel_eff= 25.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase in panel efficiencies.  
    Increases `mod_eff` from current year until goal_year by linear interpolation until
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
     
    df['mod_eff']=df['mod_eff'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mod_eff'] = np.nan
    df.loc[df.index >= goal_year , 'mod_eff'] = target_panel_eff
    df['mod_eff'] = df['mod_eff'].interpolate()

    return df

def sens_MFGYield(df, target_eff = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increasing MFG Yield efficiency. 
    Increases `MFG_Material_eff` from current year 
    until `goal_year` by linear interpolation until
    reaching the `target_eff`.
    
    Parameters
    ----------
    df : dataframe 
        dataframe to be modified
    target_eff: float
        target eff value in percentage to be reached. i.e. 95.0 %.
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
     
    df['mat_MFG_eff']=df['mat_MFG_eff'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mat_MFG_eff'] = np.nan
    df.loc[df.index >= goal_year , 'mat_MFG_eff'] = target_eff
    df['mat_MFG_eff'] = df['mat_MFG_eff'].interpolate()

    return df

def sens_MFGRecycling(df, target_recycling = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of Manufacturing loss percentage recycled.  
    Increases `MFG_Scrap_Percentage_Recycled` from current year until `goal_year` by linear interpolation until
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
     
    df['mat_MFG_scrap_recycled']=df['mat_MFG_scrap_recycled'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mat_MFG_scrap_recycled'] = np.nan
    df.loc[df.index >= goal_year , 'mat_MFG_scrap_recycled'] = target_recycling
    df['mat_MFG_scrap_recycled'] = df['mat_MFG_scrap_recycled'].interpolate()

    return df

def sens_MFGRecyclingEff(df, target_recycling_eff = 95.0, goal_year = 2030, start_year = None):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of manufacturing scrap recycling efficiency.  
    Increases `MFG_Scrap_Recycling_eff` from current year until `goal_year` by linear interpolation until
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
        
    df['mat_MFG_scrap_recycling_eff']=df['mat_MFG_scrap_recycling_eff'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > start_year), 'mat_MFG_scrap_recycling_eff'] = np.nan
    df.loc[df.index >= goal_year , 'mat_MFG_scrap_recycling_eff'] = target_recycling_eff
    df['mat_MFG_scrap_recycling_eff'] = df['mat_MFG_scrap_recycling_eff'].interpolate()

    return df

def sens_MFGHQRecycling(df, target_hq_recycling = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increasing the percentage of manufacturing scrap recyclied into high quality material.  
    Increases `MFG_Scrap_Recycled_into_HighQuality` from current year until `goal_year` by linear interpolation until
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
     
    df['mat_MFG_scrap_Recycled_into_HQ']=df['mat_MFG_scrap_Recycled_into_HQ'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mat_MFG_scrap_Recycled_into_HQ'] = np.nan
    df.loc[df.index >= goal_year , 'mat_MFG_scrap_Recycled_into_HQ'] = target_hq_recycling
    df['mat_MFG_scrap_Recycled_into_HQ'] = df['mat_MFG_scrap_Recycled_into_HQ'].interpolate()

    return df

def sens_MFGHQRecyclingEff(df, target_hq_eff = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increase of Manufacturing scrap recycling into high quality yeild efficiency. 
    Increases `MFG_Scrap_Recycled_HighQuality_Reused_for_MFG` from current year until `goal_year` by linear interpolation until
    reaching the `target_hq_eff`.
    
    Parameters
    -----------
    df : dataframe
        dataframe to be modified
    target_eff : float
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
     
    df['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG']=df['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] = np.nan
    df.loc[df.index >= goal_year , 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] = target_hq_eff
    df['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] = df['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'].interpolate()

    return df

def sens_EOLCollection(df, target_loss = 0.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to decrease of end of life collection loss percentage.  
    Decreases `EOL_Collection_Losses` from current year until `goal_year` by linear interpolation until
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
     
    df['mod_EOL_collection_losses']=df['mod_EOL_collection_losses'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mod_EOL_collection_losses'] = np.nan
    df.loc[df.index >= goal_year , 'mod_EOL_collection_losses'] = target_loss
    df['mod_EOL_collection_losses'] = df['mod_EOL_collection_losses'].interpolate()

    return df

def sens_EOLRecycling(df, target_recycling = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increase of EOL percentage recycled.  
    Increases `EOL_Collected_Material_Percentage_Recycled` from current year until `goal_year` by linear interpolation until
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
     
    df['mod_EOL_collected_recycled']=df['mod_EOL_collected_recycled'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mod_EOL_collected_recycled'] = np.nan
    df.loc[df.index >= goal_year , 'mod_EOL_collected_recycled'] = target_recycling
    df['mod_EOL_collected_recycled'] = df['mod_EOL_collected_recycled'].interpolate()

    return df

def sens_EOLRecyclingYield(df, target_eff = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increase of end of 
    life recycling yeild.     Increases `EOL_Recycling_eff` from 
    current year until `goal_year` by linear interpolation until
    reaching the `target_eff`.
    
    Parameters
    ----------
    df : dataframe
        dataframe to be modified
    target_eff : float
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
     
    df['mat_EOL_Recycling_eff']=df['mat_EOL_Recycling_eff'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mat_EOL_Recycling_eff'] = np.nan
    df.loc[df.index >= goal_year , 'mat_EOL_Recycling_eff'] = target_eff
    df['mat_EOL_Recycling_eff'] = df['mat_EOL_Recycling_eff'].interpolate()

    return df

def sens_EOLHQRecycling(df, target_recycling = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of end of 
    life high quality recycling percentage. 
    Increases `EOL_Recycled_Material_into_HighQuality` from current year 
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
     
    df['mat_EOL_Recycled_into_HQ']=df['mat_EOL_Recycled_into_HQ'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mat_EOL_Recycled_into_HQ'] = np.nan
    df.loc[df.index >= goal_year , 'mat_EOL_Recycled_into_HQ'] = target_recycling
    df['mat_EOL_Recycled_into_HQ'] = df['mat_EOL_Recycled_into_HQ'].interpolate()

    return df

def sens_EOLHQRecyclingYield(df, target_eff = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluatig sensitivity to increase of end of 
    life high quality recycling efficiency. 
    Increases `EOL_Recycled_HighQuality_Reused_for_MFG` efficiecny 
    from current year until `goal_year` by linear interpolation until
    reaching the `target_eff`.
    
    Parameters
    ----------
    df : dataframe
        dataframe to be modified
    target_eff : float 
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
     
    df['mat_EOL_RecycledHQ_Reused4MFG']=df['mat_EOL_RecycledHQ_Reused4MFG'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mat_EOL_RecycledHQ_Reused4MFG'] = np.nan
    df.loc[df.index >= goal_year , 'mat_EOL_RecycledHQ_Reused4MFG'] = target_eff
    df['mat_EOL_RecycledHQ_Reused4MFG'] = df['mat_EOL_RecycledHQ_Reused4Manufacturing'].interpolate()

    return df

def sens_ReUse(df, target_reuse = 95.0, goal_year = 2030):
    '''
    Modifies baseline scenario for evaluating sensitivity to increase of percent 
    of end of life panels that find a second life.  
    Increases `mod_Repowering` from current year 
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
     
    df['mod_repowering']=df['mod_repowering'].astype(float)
    df.loc[(df.index < goal_year) & (df.index > current_year), 'mod_repowering'] = np.nan
    df.loc[df.index >= goal_year , 'mod_repowering'] = target_reuse
    df['mod_repowering'] = df['mod_repowering'].interpolate()

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