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
import datetime
import os
import matplotlib.pyplot as plt

def read_baseline_material(scenario, material='None', file=None):
    
    if file is None:
        try:
            file = _interactive_load('Select baseline file')
        except:
            raise Exception('Interactive load failed. Tkinter not supported'+
                            'on this system. Try installing X-Quartz and reloading')
    

def _interactive_load(title=None):
    # Tkinter file picker
    import tkinter
    from tkinter import filedialog
    root = tkinter.Tk()
    root.withdraw() #Start interactive file input
    root.attributes("-topmost", True) #Bring window into foreground
    return filedialog.askopenfilename(parent=root, title=title) #initialdir = data_dir

def _unitReferences(keyword):
    '''
    Specify units for variable in scenario or materials
    
    Parameters
    ----------
    keyword : str
       String of scenario or material column label
    
    Returns
    -------
    yunits : str
        Unit specific to the keyword provided
    '''

    moduleDictionary = {'year': {'unit': 'Years', 'source': 'input'},
                        'new_Installed_Capacity_[MW]': {'unit': 'Power [MW]', 'source':'input'},
                        'mod_eff': {'unit': 'Efficiency $\eta$ [%]', 'source':'input'},
                        'mod_reliability_t50': {'unit': 'Years' , 'source':'input'},
                        'mod_reliability_t90': {'unit': 'Years', 'source':'input'},
                        'mod_degradation': {'unit': 'Percentage [%]', 'source':'input'},
                        'mod_lifetime': {'unit': 'Years', 'source':'input'},
                        'mod_MFG_eff': {'unit': 'Efficiency $\eta$ [%]', 'source':'input'},
                        'mod_EOL_collection_eff': {'unit': 'Efficiency $\eta$ [%]', 'source':'input'},
                        'mod_EOL_collected_recycled': {'unit': 'Percentage [%]', 'source':'input'},
                        'mod_Repowering': {'unit': 'Percentage [%]', 'source':'input'},
                        'mod_Repairing': {'unit': 'Percentage [%]', 'source':'input'},
                        'Area': {'unit': 'm$^2$', 'source': 'generated'},
                        'Cumulative_Area_disposedby_Failure': {'unit': 'm$^2$', 'source': 'generated'},
                        'Cumulative_Area_disposedby_ProjectLifetime': {'unit': 'm$^2$', 'source': 'generated'},
                        'Cumulative_Area_disposed': {'unit': 'm$^2$', 'source': 'generated'},
                        'Cumulative_Active_Area': {'unit': 'm$^2$', 'source': 'generated'},
                        'Installed_Capacity_[W]': {'unit': 'Power [W]', 'source': 'generated'},
                        'EOL_on_Year_0': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_1': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_2': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_3': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_4': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_5': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_6': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_7': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_8': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_9': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_10': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_11': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_12': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_13': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_14': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_15': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_16': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_17': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_18': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_19': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_20': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_21': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_22': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_23': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_24': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_25': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_26': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_27': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_28': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_29': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_30': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_31': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_32': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_33': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_34': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_35': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_36': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_37': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_38': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_39': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_40': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_41': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_42': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_43': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_44': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_45': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_46': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_47': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_48': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_49': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_50': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_51': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_52': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_53': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_54': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_on_Year_55': {'unit': 'm$^2$', 'source': 'generated'},
                        'EoL_Collected': {'unit': 'm$^2$', 'source': 'generated'},
                        'EoL_NotCollected': {'unit': 'm$^2$', 'source': 'generated'},
                        'EoL_Recycled': {'unit': 'm$^2$', 'source': 'generated'},
                        'EoL_NotRecycled_Landfilled': {'unit': 'm$^2$', 'source': 'generated'}
                        }

    materialDictionary={'year': {'unit': 'Years', 'source': 'input'},
                        'mat_virgin_eff': {'unit': 'Efficiency $\eta$ [%]', 'source': 'input'},
                        'mat_massperm2': {'unit': 'Mass [g]', 'source': 'input'},
                        'mat_MFG_eff': {'unit': 'Efficiency $\eta$ [%]', 'source': 'input'},
                        'mat_MFG_scrap_recycled': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mat_MFG_scrap_Recycled': {'unit': 'Efficiency $\eta$ [%]', 'source': 'input'},
                        'mat_MFG_scrap_Recycled_into_HQ': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mat_EOL_collected_Recycled': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mat_EOL_Recycling_eff': {'unit': 'Efficiency $\eta$ [%]', 'source': 'input'},
                        'mat_EOL_Recycled_into_HQ': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mat_EOL_RecycledHQ_Reused4MFG': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mat_modules_NotRecycled': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_modules_NotCollected': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_EOL_sento_Recycling': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_EOL_NotRecycled_Landfilled': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_EOL_Recycled': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_EOL_Recycled_Losses_Landfilled': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_EOL_Recycled_2_HQ': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_EOL_Recycled_2_OQ': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_EoL_Recycled_HQ_into_MFG': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_EOL_Recycled_HQ_into_OU': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_UsedinManufacturing': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_Manufacturing_Input': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_MFG_Scrap': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_MFG_Scrap_Sentto_Recycling': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_MFG_Scrap_Landfilled': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_MFG_Scrap_Recycled_Successfully': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_MFG_Scrap_Recycled_Losses_Landfilled': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_MFG_Recycled_into_HQ': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_MFG_Recycled_into_OQ': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_MFG_Recycled_HQ_into_MFG': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_MFG_Recycled_HQ_into_OU': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_Virgin_Stock': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_Total_EOL_Landfilled': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_Total_MFG_Landfilled': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_Total_Landfilled': {'unit': 'Mass [g]', 'source': 'generated'},
                        'mat_Total_Recycled_OU': {'unit': 'Mass [g]', 'source': 'generated'}
                        }
    

    if keyword in moduleDictionary.keys():
      yunits = moduleDictionary[keyword]['unit']
    elif keyword in materialDictionary.keys():
        yunits = materialDictionary[keyword]['unit']
    else:
        print("Warning: Keyword / Units not Found")
        yunits =  'UNITS'
     
    return yunits
    

def distance(s_lat, s_lng, e_lat, e_lng):
    """
    # Haversine formula for numpy arrays
    # Author: MalyutinS
    # imported from comment on: https://gist.github.com/rochacbruno/2883505
    # Example: 
    # s_lat = 45; s_lng = -110; e_lat=[33, 44]; e_lng = [-115, -140]
    # Returns distance from the source point  to the two ending points:
    # r = distance(s_lat, s_lng, e_lat, e_lng)
    # r = array([1402.24996689, 2369.0150434 ])
    #
    """
    
    
    # approximate radius of earth in km
    R = 6373.0  
    
#    s_lat = s_lat*np.pi/180.0                      
    s_lat = np.deg2rad(s_lat)                     
    s_lng = np.deg2rad(s_lng)     
    e_lat = np.deg2rad(e_lat)                       
    e_lng = np.deg2rad(e_lng)  
    
    d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2
    distance = 2 * R * np.arcsin(np.sqrt(d)) 
    
    return distance

def drivingdistance(origin, destination, APIkey):
    """
    Creates call for google-maps api to get driving directions betwen two points.
    
    Input
    -----
    origin: array
        [lat, lon] expected
    destination: array
        [lat, lon] expected
    APYkey: str
        String
    """
    
    lat1, lon1 = origin
    lat2, lon2 = destination
    
    gm_url = ('https://maps.googleapis.com/maps/api/directions/xml?'+
              'origin='+str(lat1)+','+str(lon1)+
              '&destination='+str(lat2)+','+str(lon2)+
              '&key='+APIkey)

    return gm_url
    
    
    
class Simulation:
    """
    The ScenarioObj top level class is used to work on Circular Economy scenario objects, 
    keep track of filenames, data for module and materials, operations modifying
    the baselines, etc.

    Parameters
    ----------
    name : text to append to output files
    nowstr : current date/time string
    path : working directory with circular economy results

    Methods
    -------
    __init__ : initialize the object
    _setPath : change the working directory

    """
    
    def __init__(self, name=None, path=None):
        '''
        initialize ScenarioObj with path of Scenario's baseline of module and materials
        as well as a basename to append to

        Parameters
        ----------
        name: string, append temporary and output files with this value
        path: location of Radiance materials and objects

        Returns
        -------
        none
        '''

        self.path = ""             # path of working directory
        self.name = ""         # basename to append
        
        now = datetime.datetime.now()
        self.nowstr = str(now.date())+'_'+str(now.hour)+str(now.minute)+str(now.second)

        if path is None:
            self._setPath(os.getcwd())
        else:
            self._setPath(path)

        if name is None:
            self.name = self.nowstr  # set default filename for output files
        else:
            self.name = name

        self.scenario={}

        
    def _setPath(self, path):
        """
        setPath - move path and working directory

        """
        self.path = os.path.abspath(path)

        print('path = '+ path)
        try:
            os.chdir(self.path)
        except OSError as exc:
            LOGGER.error('Path doesn''t exist: %s' % (path))
            LOGGER.exception(exc)
            raise(exc)

        # check for path in the new Radiance directory:
        def _checkPath(path):  # create the file structure if it doesn't exist
            if not os.path.exists(path):
                os.makedirs(path)
                print('Making path: '+path)
    
    def createScenario(self, name, file=None):
        
        self.scenario[name] = Scenario(name, file)
        


    def calculateMassFlow(self, weibullInputParams = None, debugflag=False):
        '''
        Function takes as input a baseline dataframe already imported, 
        with the right number of columns and content.
        It returns the dataframe with all the added calculation columns.
        
        Parameters
        ------------
        weibullInputParams : None
            Dictionary with 'alpha' and 'beta' value for shaping the weibull
            curve. beta is sometimes exchanged with lifetime, for example on
            Irena 2016 values beta = 30. If weibullInputParams = None,
            alfa and beta are calcualted from the t50 and t90 columns on the
            module baseline.
        
        Returns
        --------
        df: dataframe 
            input dataframe with addeds columns for the calculations of recycled,
            collected, waste, installed area, etc. 
        
        '''
        
        
        for scen in self.scenario:
            
            print("Working on Scenario: ", scen)
            print("********************")
            df = self.scenario[scen].data

            # Constant
            irradiance_stc = 1000 # W/m^2
        
            # Renaming and re-scaling
            df['new_Installed_Capacity_[W]'] = df['new_Installed_Capacity_[MW]']*1e6
            df['t50'] = df['mod_reliability_t50']
            df['t90'] = df['mod_reliability_t90']
            
            # Calculating Area and Mass
            df['Area'] = df['new_Installed_Capacity_[W]']/(df['mod_eff']*0.01)/irradiance_stc # m^2                
            df['Area'] = df['Area'].fillna(0) # Chagne na's to 0s.

            # Calculating Wast by Generation by Year, and Cumulative Waste by Year.
            Generation_Disposed_byYear = []
            Generation_Active_byYear= []
            Generation_Power_byYear = []
            weibullParamList = []

            df['Cumulative_Area_disposedby_Failure'] = 0
            df['Cumulative_Area_disposedby_ProjectLifetime'] = 0
            df['Cumulative_Area_disposed'] = 0
            df['Cumulative_Active_Area'] = 0
            df['Installed_Capacity_[W]'] = 0
            for generation, row in df.iterrows(): 
                #generation is an int 0,1,2,.... etc.
                #generation=4
                #row=df.iloc[generation]
                
                t50, t90 = row['t50'], row['t90']
                if not weibullInputParams:
                    weibullIParams = weibull_params({t50: 0.50, t90: 0.90})      
                else: 
                    weibullIParams = weibullInputParams
               
                f = weibull_cdf(weibullIParams['alpha'], weibullIParams['beta'])
                
                weibullParamList.append(weibullIParams)

                x = np.clip(df.index - generation, 0, np.inf)
                cdf = list(map(f, x))
#                pdf = [0] + [j - i for i, j in zip(cdf[: -1], cdf[1 :])]

                activearea = row['Area']
                if np.isnan(activearea):
                    activearea=0
                
                activeareacount = []
                areadisposed_failure = []
                areadisposed_projectlifetime = []
            
                areapowergen = []
                active=-1
                disposed_projectlifetime=0
                for age in range(len(cdf)):
                    disposed_projectlifetime=0
                    if cdf[age] == 0.0:
                        activeareacount.append(0)
                        areadisposed_failure.append(0)
                        areadisposed_projectlifetime.append(0)
                        areapowergen.append(0)
                    else:
                        active += 1
                        activeareaprev = activearea                            
                        activearea = activearea*(1-cdf[age]*(1-df.iloc[age]['mod_Repairing']*0.01))
                        areadisposed_failure.append(activeareaprev-activearea)
                        if age == int(row['mod_lifetime']+generation):
                            activearea_temp = activearea
                            activearea = 0+activearea*(df.iloc[age]['mod_Repowering']*0.01)
                            disposed_projectlifetime = activearea_temp-activearea
                        areadisposed_projectlifetime.append(disposed_projectlifetime)
                        activeareacount.append(activearea)
                        areapowergen.append(activearea*row['mod_eff']*0.01*irradiance_stc*(1-row['mod_degradation']*0.01)**active)                            
                
                try:
                    # becuase the clip starts with 0 for the installation year, identifying installation year
                    # and adding initial area
                    fixinitialareacount = next((i for i, e in enumerate(x) if e), None) - 1
                    activeareacount[fixinitialareacount] = activeareacount[fixinitialareacount]+row['Area']    
                    areapowergen[fixinitialareacount] = (activeareacount[fixinitialareacount] +  
                                         row['Area'] * row['mod_eff'] *0.01 * irradiance_stc)
                except:
                    # Last value does not have a xclip value of nonzero so it goes
                    # to except. But it also means the loop finished for the calculations
                    # of Lifetime.
                    fixinitialareacount = len(cdf)-1
                    activeareacount[fixinitialareacount] = activeareacount[fixinitialareacount]+row['Area']    
                    areapowergen[fixinitialareacount] = (activeareacount[fixinitialareacount] +  
                                         row['Area'] * row['mod_eff'] *0.01 * irradiance_stc)                   
                    print("Finished Area+Power Generation Calculations")
                    
            
            #   area_disposed_of_generation_by_year = [element*row['Area'] for element in pdf]
                df['Cumulative_Area_disposedby_Failure'] += areadisposed_failure
                df['Cumulative_Area_disposedby_ProjectLifetime'] += areadisposed_projectlifetime
                df['Cumulative_Area_disposed'] += areadisposed_failure
                df['Cumulative_Area_disposed'] += areadisposed_projectlifetime
                
                
                df['Cumulative_Active_Area'] += activeareacount
                df['Installed_Capacity_[W]'] += areapowergen
                Generation_Disposed_byYear.append([x + y for x, y in zip(areadisposed_failure, areadisposed_projectlifetime)])
                Generation_Active_byYear.append(activeareacount)
                Generation_Power_byYear.append(areapowergen)
            
            
            df['WeibullParams'] = weibullParamList
            MatrixDisposalbyYear = pd.DataFrame(Generation_Disposed_byYear, columns = df.index, index = df.index)
            MatrixDisposalbyYear = MatrixDisposalbyYear.add_prefix("EOL_on_Year_")
            
            try:
                df = df[df.columns.drop(list(df.filter(regex='EOL_on_Year_')))]
            except:
                print("Warning: Issue dropping EOL columns generated by " \
                      "calculateMFC routine to overwrite")
            
            df = df.join(MatrixDisposalbyYear)

            
            ## Start to do EOL Processes
            ############################
            
            filter_col = [col for col in df if col.startswith('EOL_on_Year_')]
            EOL = df[filter_col]
            
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
    
            # Cleanup of internal renaming and internal use columns
            df.drop(['new_Installed_Capacity_[W]', 't50', 't90'], axis = 1, inplace=True) 
            
            self.scenario[scen].data = df
            
            # collection losses here
            
            # Recyle % here
            
            
            ################
            # Material Loop#
            ################

            for mat in self.scenario[scen].material:

                print("==> Working on Material : ", mat)

                dm = self.scenario[scen].material[mat].materialdata
                
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
                
                mat_EOL_Recycled_Succesfully = mat_EOL_sento_Recycling.mul(dm['mat_EOL_Recycling_eff'].values*0.01)
                dm['mat_EOL_Recycled'] = list(mat_EOL_Recycled_Succesfully.sum())
                landfill_material_EOL_Recyled_Losses_Landfilled = mat_EOL_sento_Recycling.mul(1-(dm['mat_EOL_Recycling_eff'].values*0.01))
                dm['mat_EOL_Recycled_Losses_Landfilled'] = list(landfill_material_EOL_Recyled_Losses_Landfilled.sum())
                
                
                mat_EOL_Recycled_HQ = mat_EOL_Recycled_Succesfully.mul(dm['mat_EOL_Recycled_into_HQ'].values*0.01)
                dm['mat_EOL_Recycled_2_HQ'] = list(mat_EOL_Recycled_HQ.sum())
                mat_EOL_Recycled_OQ = mat_EOL_Recycled_Succesfully.mul(1-(dm['mat_EOL_Recycled_into_HQ'].values*0.01))
                dm['mat_EOL_Recycled_2_OQ'] = list(mat_EOL_Recycled_OQ.sum())
                
                mat_EOL_Recycled_HQ_into_MFG = mat_EOL_Recycled_HQ.mul(dm['mat_EOL_RecycledHQ_Reused4MFG'].values*0.01)
                dm['mat_EoL_Recycled_HQ_into_MFG'] = list(mat_EOL_Recycled_HQ_into_MFG.sum())
                mat_EOL_Recycled_HQ_into_OU = mat_EOL_Recycled_HQ.mul(1-(dm['mat_EOL_RecycledHQ_Reused4MFG'].values*0.01))
                dm['mat_EOL_Recycled_HQ_into_OU'] = list(mat_EOL_Recycled_HQ_into_OU.sum())
                
                # BULK Calculations Now
                dm['mat_UsedSuccessfullyinModuleManufacturing'] = (df['Area'] * dm['mat_massperm2'])
                dm['mat_EnteringModuleManufacturing'] = (df['Area'] * dm['mat_massperm2']*100/df['mod_MFG_eff'])
                dm['mat_LostinModuleManufacturing'] = dm['mat_EnteringModuleManufacturing'] - dm['mat_UsedSuccessfullyinModuleManufacturing']
                
                dm['mat_Manufacturing_Input'] = dm['mat_EnteringModuleManufacturing'] / (dm['mat_MFG_eff'] * 0.01)
                
                # Scrap = Lost to Material manufacturing losses + Module manufacturing losses
                dm['mat_MFG_Scrap'] = (dm['mat_Manufacturing_Input'] - dm['mat_EnteringModuleManufacturing'] + 
                                      dm['mat_LostinModuleManufacturing'])
                dm['mat_MFG_Scrap_Sentto_Recycling'] = dm['mat_MFG_Scrap'] * dm['mat_MFG_scrap_Recycled'] * 0.01
                
                
                
                dm['mat_MFG_Scrap_Landfilled'] = dm['mat_MFG_Scrap'] - dm['mat_MFG_Scrap_Sentto_Recycling'] 
                dm['mat_MFG_Scrap_Recycled_Successfully'] = (dm['mat_MFG_Scrap_Sentto_Recycling'] *
                                                                 dm['mat_MFG_scrap_Recycling_eff'] * 0.01)
                dm['mat_MFG_Scrap_Recycled_Losses_Landfilled'] = (dm['mat_MFG_Scrap_Sentto_Recycling'] - 
                                                                          dm['mat_MFG_Scrap_Recycled_Successfully'])
                dm['mat_MFG_Recycled_into_HQ'] = (dm['mat_MFG_Scrap_Recycled_Successfully'] * 
                                                        dm['mat_MFG_scrap_Recycled_into_HQ'] * 0.01)
                dm['mat_MFG_Recycled_into_OQ'] = dm['mat_MFG_Scrap_Recycled_Successfully'] - dm['mat_MFG_Recycled_into_HQ']
                dm['mat_MFG_Recycled_HQ_into_MFG'] = (dm['mat_MFG_Recycled_into_HQ'] * 
                                          dm['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] * 0.01)
                dm['mat_MFG_Recycled_HQ_into_OU'] = dm['mat_MFG_Recycled_into_HQ'] - dm['mat_MFG_Recycled_HQ_into_MFG']
                dm['mat_Virgin_Stock'] = dm['mat_Manufacturing_Input'] - dm['mat_EoL_Recycled_HQ_into_MFG'] - dm['mat_MFG_Recycled_HQ_into_MFG']
                
                # Calculate raw virgin needs before mining and refining efficiency losses
                dm['mat_Virgin_Stock_Raw'] = (dm['mat_Virgin_Stock'] * 100 /  dm['mat_virgin_eff'])

                # Add Wastes
                dm['mat_Total_EOL_Landfilled'] = (dm['mat_modules_NotCollected'] + 
                                                  dm['mat_modules_NotRecycled'] +
                                                  dm['mat_EOL_NotRecycled_Landfilled'] +
                                                  dm['mat_EOL_Recycled_Losses_Landfilled'])      
                
                dm['mat_Total_MFG_Landfilled'] = (dm['mat_MFG_Scrap_Landfilled'] + 
                                                 dm['mat_MFG_Scrap_Recycled_Losses_Landfilled'])
                
                dm['mat_Total_Landfilled'] = (dm['mat_Total_EOL_Landfilled'] + 
                                              dm['mat_Total_MFG_Landfilled'])
                
                dm['mat_Total_Recycled_OU'] = (dm['mat_EOL_Recycled_2_OQ'] + 
                                               dm['mat_EOL_Recycled_HQ_into_OU'] + 
                                               dm['mat_MFG_Recycled_into_OQ'] + 
                                               dm['mat_MFG_Recycled_HQ_into_OU'])
 
                
                self.scenario[scen].material[mat].materialdata = dm

    
    
    def plotScenariosComparison(self, keyword=None):
    
        if keyword is None:
            scens = list(self.scenario.keys())[0]
            print("Choose one of the keywords: ", list(self.scenario[scens].data.keys())) 
            return
        
        yunits = _unitReferences(keyword)
       
        plt.figure()
    
        for scen in self.scenario:
            plt.plot(self.scenario[scen].data['year'],self.scenario[scen].data[keyword], label=scen)
        plt.legend()
        plt.xlabel('Year')
        plt.title(keyword.replace('_', " "))
        plt.ylabel(yunits)        




    def plotMaterialComparisonAcrossScenarios(self, material = None, keyword=None):
    
        if keyword is None:
            scens = list(self.scenario.keys())[0]
            mats = list(self.scenario[scens].material.keys())[0]
            print("Choose one of the keywords: ",  list(self.scenario[scens].material[mats].materialdata.keys())) 
            return

        if material is None:
            scens = list(self.scenario.keys())[0]
            mats = list(self.scenario[scens].material.keys())
            print("Choose one of the Materials: ", mats) 
            return
        
        yunits = _unitReferences(keyword)

        plt.figure()
    
        for scen in self.scenario:
            plt.plot(self.scenario[scen].data['year'], self.scenario[scen].material[material].materialdata[keyword], label=scen)
            plt.legend()
    
        plt.xlabel('Year')
        plt.title((material + ' ' + keyword.replace('_', " ")))
        plt.ylabel(yunits)    
        
        
class Scenario(Simulation):
    
    def __init__(self, name, file=None):
        self.name = name
        self.material = {}
                
        if file is None:
            try:
                file = _interactive_load('Select module baseline file')
            except:
                raise Exception('Interactive load failed. Tkinter not supported'+
                                'on this system. Try installing X-Quartz and reloading')
                
        csvdata = open(str(file), 'r', encoding="UTF-8")
        csvdata = open(str(file), 'r', encoding="UTF-8-sig")
        firstline = csvdata.readline()
        secondline = csvdata.readline()

        head = firstline.rstrip('\n').split(",")
        meta = dict(zip(head, secondline.rstrip('\n').split(",")))

        data = pd.read_csv(csvdata, names=head)
        data.loc[:, data.columns != 'year'] = data.loc[:, data.columns != 'year'].astype(float)
        self.baselinefile = file
        self.metdata = meta,
        self.data = data
    
    def addMaterial(self, materialname, file=None):
        self.material[materialname] = Material(materialname, file)
    
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key):
        return setattr(self, key)

class Material:
    def __init__(self, materialname, file):
        self.materialname = materialname
        
        if file is None:
            try:
                file = _interactive_load('Select material baseline file')
            except:
                raise Exception('Interactive load failed. Tkinter not supported'+
                                'on this system. Try installing X-Quartz and reloading')
        
        csvdata = open(str(file), 'r', encoding="UTF-8")
        csvdata = open(str(file), 'r', encoding="UTF-8-sig")
        firstline = csvdata.readline()
        secondline = csvdata.readline()

        head = firstline.rstrip('\n').split(",")
        meta = dict(zip(head, secondline.rstrip('\n').split(",")))

        data = pd.read_csv(csvdata, names=head)
        data.loc[:, data.columns != 'year'] = data.loc[:, data.columns != 'year'].astype(float)
        self.materialfile = file
        self.materialmetdata = meta
        self.materialdata = data


def weibull_params(keypoints):
    r'''Returns shape parameter `alpha` and scale parameter `beta`
    for a Weibull distribution whose CDF passes through the
    two time: value pairs in `keypoints`

    Parameters
    ----------
    keypoints : list
        Two lists of t50 and 590 values, where t50 is the year since deployment
        that the cohort has lost 50% of originally installed modules, and t90 
        is the year since deployment that the cohort has lost 90% of the originally
        installed modules. These values are used to calcualte the shape and scale 
        parameters for the weibull distribution.
    
    Returns
    -------
    alpha : float
        Shape parameter `alpha` for weibull distribution.
    beta : float
        Scale parameter `beta` for weibull distribution. Often exchanged with ``lifetime``
        like in Irena 2016, beta = 30.
        
    '''
    
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
    scale parameter `beta`
    
    Parameters
    ----------
    alpha : float
        Shape parameter `alpha` for weibull distribution.
    beta : float
        Scale parameter `beta` for weibull distribution. Often exchanged with ``lifetime``
        like in Irena 2016, beta = 30.
        
    '''
    
    def cdf(x):
        return 1 - np.exp(-(np.array(x)/beta)**alpha)
    return cdf

def weibull_pdf(alpha, beta):
    r'''Return the PDF for a Weibull distribution having:
        shape parameter `alpha`
        scale parameter `beta`
        
    Parameters
    ----------
    alpha : float
        Shape parameter `alpha` for weibull distribution.
    beta : float
        Scale parameter `beta` for weibull distribution. Often exchanged with ``lifetime``
        like in Irena 2016, beta = 30.
        
    '''
    
    def pdf(x):
        return (alpha/np.array(x)) * ((np.array(x)/beta)**alpha) * (np.exp(-(np.array(x)/beta)**alpha))
    
    return pdf


def weibull_cdf_vis(alpha, beta, xlim=56):
    r''' Returns the CDF for a weibull distribution of 1 generation
    so it can be plotted.
    
    Parameters
    ----------
    alpha : float
        Shape parameter `alpha` for weibull distribution.
    beta : float
        Scale parameter `beta` for weibull distribution. Often exchanged with ``lifetime``
        like in Irena 2016, beta = 30.
    xlim : int
        Number of years to calculate the distribution for. i.e. x-axis limit. 

    Returns
    -------
    idf : list
        List of weibull cumulative distribution values for year 0 until xlim.

    '''

    dfindex = pd.RangeIndex(0,xlim,1)
    x = np.clip(dfindex - 0, 0, np.inf)

    if alpha and beta:
        i = weibull_cdf(alpha, beta)
    
    idf = list(map(i, x))
    
    return idf

    
def sens_StageImprovement(df, stage, improvement=1.3, start_year=None):
    '''
    Modifies baseline scenario for evaluating sensitivity of lifetime parameter.
    t50 and t90 reliability years get incresed by `improvement` parameter
    starting the `year_increase` year specified. 
    
    Parameters
    ----------
    df : dataframe
        dataframe to be modified
    stage : str
        Stage that wants to be modified. This can be any of the module or 
        material specified values, for example:'MFG_Material_eff', 
        'mat_MFG_scrap_recycled', 'mat_MFG_scrap_Recycled', 
        'mat_MFG_scrap_Recycled_into_HQ', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'
        'mod_EOL_collection_losses', 'mod_EOL_collected_recycled',
        'mat_EOL_Recycling_eff', 'mat_EOL_Recycled_into_HQ', 
        'mat_EOL_RecycledHQ_Reused4MFG', 'mod_repowering', 'mod_eff', etc.
    improvement : decimal
        Percent increase in decimal (i.e. "1.3" for 30% increase in value) 
        or percent decrease (i.e. "0.3") relative to values in df.
    start_year : 
        the year at which the improvement occurs
    
    Returns
    --------
    df : dataframe
        dataframe of expected module lifetime increased or decreased at specified year
    '''


    if start_year is None:
        start_year = int(datetime.datetime.now().year)

    #df[df.index > 2000]['mod_reliability_t50'].apply(lambda x: x*1.3)
    df[stage] = df[stage].astype(float)
    df.loc[df.index > start_year, stage] = df[df.index > start_year][stage].apply(lambda x: x*improvement)
    
    return df


def sens_StageEfficiency(df, stage, target_eff = 95.0, start_year = None, 
                         goal_year = 2030, plotflag = False):
    '''
    Modifies baseline scenario for evaluating sensitivity to increasing a stage in the 
    lifetime of the module's efficiency. It either increases or decreases from the 
    start year until the goal year the value to the target efficiency by interpolation.
    
    Parameters
    ----------
    df : dataframe 
        dataframe to be modified
    stage : str
        Stage that wants to be modified. This can be any of the module or 
        material specified efficiencies, for example:'MFG_Material_eff', 
        'mat_MFG_scrap_recycled', 'mat_MFG_scrap_Recycled', 
        'mat_MFG_scrap_Recycled_into_HQ', 'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'
        'mod_EOL_collection_losses', 'mod_EOL_collected_recycled',
        'mat_EOL_Recycling_eff', 'mat_EOL_Recycled_into_HQ', 
        'mat_EOL_RecycledHQ_Reused4MFG', 'mod_repowering', 'mod_eff', etc.
    start_year: int
        Year to start modifying the value. This specifies the initial efficiency 
        value that is going to be modified. If None is passed, current year is used.
    target_eff: flat
        target eff value in percentage to be reached. i.e. 95.0 %.
    goal_year : int
        year by which target efficiency will be reached. i.e. 2030. Must be higher than current year.
    
    Returns
    -------
    df : dataframe
        modified dataframe
    '''
    
    if start_year is None:
        start_year = int(datetime.datetime.now().year)
    
    if start_year > goal_year:
        print("Error. Goal Year is before start year")
        return
    
    if 0 < abs(target_eff) < 1:  # checking it is not 0.95 but 95% i.e.
        print("Warning: target_eff value is between 0 and 1; it has been"
              "multiplied by 100% assuming it was a percentage in decimal form.")
        target_eff = target_eff*100
        
    if target_eff > 100 or target_eff < 0:
        print("Warning: target_eff is out of range. Input value between"
              "0 and 100")
        return
    
    if stage in df.columns:
        df2 = df.copy()
        df2[stage]=df2[stage].astype(float)
        df2.loc[(df2.index < goal_year) & (df2.index > start_year), stage] = np.nan
        df2.loc[df2.index >= goal_year , stage] = target_eff
        df2[stage] = df2[stage].interpolate()
        
        if plotflag:
            plt.plot(df[stage], label='Original')
            plt.plot(df2[stage], label='Modified')
            plt.title('Updated values for '+stage)
            plt.legend()
        return df2
    else:
        print("Stage name incorrect.")






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