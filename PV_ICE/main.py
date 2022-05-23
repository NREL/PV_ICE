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
                        'mod_Repair': {'unit': 'Percentage [%]', 'source':'input'},
                        'mod_MerchantTail': {'unit': 'Percentage [%]', 'source':'input'},
                        'mod_Reuse': {'unit': 'Percentage [%]', 'source':'input'},
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
                        'EOL_Collected': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_NotCollected': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_Recycled': {'unit': 'm$^2$', 'source': 'generated'},
                        'EOL_NotRecycled_Landfilled': {'unit': 'm$^2$', 'source': 'generated'}
                        }

    materialDictionary={'year': {'unit': 'Years', 'source': 'input'},
                        'mat_virgin_eff': {'unit': 'Efficiency $\eta$ [%]', 'source': 'input'},
                        'mat_massperm2': {'unit': 'Mass [g]', 'source': 'input'},
                        'mat_MFG_eff': {'unit': 'Efficiency $\eta$ [%]', 'source': 'input'},
                        'mat_MFG_scrap_recycled': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mat_MFG_scrap_Recycled': {'unit': 'Efficiency $\eta$ [%]', 'source': 'input'},
                        'mat_MFG_scrap_Recycled_into_HQ': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mat_MFG_scrap_Recycled_into_HQ_Reused4MFG': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mod_EOL_p5_recycled': {'unit': 'Percentage [%]', 'source': 'input'},
                        'mat_EOL_Recycling_yield': {'unit': 'Efficiency $\eta$ [%]', 'source': 'input'},
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
                        'mat_EOL_Recycled_HQ_into_MFG': {'unit': 'Mass [g]', 'source': 'generated'},
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
        


    def modifyScenario(self, scenarios, stage, value, start_year=None):
    
        if start_year is None:
            start_year = int(datetime.datetime.now().year)
    
        if scenarios is None:
            scenarios = list(self.scenario.keys())
        else:
            if isinstance(scenarios, str):
                scenarios = [scenarios]
        
        selectyears = self.scenario[scenarios[0]].data['year']>start_year
        
        for scen in scenarios:
            self.scenario[scen].data.loc[selectyears, stage] = value
          
    def calculateMassFlow(self, scenarios = None, materials=None, weibullInputParams = None, 
                          bifacialityfactors = None, reducecapacity = True, debugflag=False):
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
        scenarios : None
            string with the scenario name or list of strings with
            scenarios names to loop over. Must exist on the PV ICE object.
        materials : None
            string with the material name or list of strings with the
            materials names to loop over. Must exists on the PV ICE object 
            scenario(s) modeled.
        bifacialityfactors : str
            File with bifacialtiy factors for each year under consideration
        
        Returns
        --------
        df: dataframe 
            input dataframe with addeds columns for the calculations of recycled,
            collected, waste, installed area, etc. 
        
        '''
        
        if scenarios is None:
            scenarios = list(self.scenario.keys())
        else:
            if isinstance(scenarios, str):
                scenarios = [scenarios]
        
        for scen in scenarios:
            
            print("Working on Scenario: ", scen)
            print("********************")
            df = self.scenario[scen].data

            # Constant
            if bifacialityfactors is not None:   
                bf = pd.read_csv(bifacialityfactors)
                df['irradiance_stc'] = 1000.0 + bf['bifi']*100.0 # W/m^2 (min. Bifacial STC Increase)
            else:
                df['irradiance_stc'] = 1000.0 # W/m^2

            # Renaming and re-scaling
            df['t50'] = df['mod_reliability_t50']
            df['t90'] = df['mod_reliability_t90']
            
            # Calculating Area and Mass
            
            if 'Mass_[MetricTonnes]' in df:
                df['new_Installed_Capacity_[W]'] = 0
                df['new_Installed_Capacity_[MW]'] = 0
                df['Area'] = df['Mass_[MetricTonnes]']
                print("Warning, this is for special debuging of Wambach Procedure."+
                      "Make sure to use Wambach Module")
            else:
                df['new_Installed_Capacity_[W]'] = df['new_Installed_Capacity_[MW]']*1e6

                if reducecapacity:
                    df['Area'] = df['new_Installed_Capacity_[W]']/(df['mod_eff']*0.01)/df['irradiance_stc'] # m^2                
                else:
                    df['Area'] = df['new_Installed_Capacity_[W]']/(df['mod_eff']*0.01)/1000.0 # m^2
            
                    
            df['Area'] = df['Area'].fillna(0) # Chagne na's to 0s.

            # Calculating Wast by Generation by Year, and Cumulative Waste by Year.
            Generation_EOL_pathsG = []
            Generation_Disposed_byYear = []
            Matrix_Landfilled_noncollected = []
            Matrix_area_bad_status = []
            Matrix_Failures = []
            # Generation_Active_byYear= [] Not being used at the moment, commenting out.
            # Generation_Power_byYear = [] Not being used at the moment, commenting out.
            weibullParamList = []

            df['Yearly_Sum_Area_disposedby_Failure'] = 0
            df['Yearly_Sum_Power_disposedby_Failure'] = 0
            df['Yearly_Sum_Area_disposedby_ProjectLifetime'] = 0
            df['Yearly_Sum_Power_disposedby_ProjectLifetime'] = 0
            df['Yearly_Sum_Area_disposed'] = 0  # Failure + ProjectLifetime
            df['Yearly_Sum_Power_disposed'] = 0

            df['landfilled_noncollected'] = 0
            
            df['Repaired_[W]'] = 0
            df['Repaired_Area'] = 0
            
            df['Resold_Area'] = 0
            df['Resold_[W]'] = 0

            df['Cumulative_Active_Area'] = 0
            df['Installed_Capacity_[W]'] = 0

            df['Status_BAD_Area'] = 0
            df['Status_BAD_[W]'] = 0

            df['Area_for_EOL_pathsG'] = 0
            df['Power_for_EOL_pathsG'] = 0
            
            df['Landfill_0'] = 0
            
            for generation, row in df.iterrows(): 
                #generation is an int 0,1,2,.... etc.
                #generation=4
                #row=df.iloc[generation]
                
                if weibullInputParams:
                    weibullIParams = weibullInputParams
                elif 'weibull_alpha' in row:
                    # "Weibull Input Params passed internally as a column"
                    weibullIParams = {'alpha': row['weibull_alpha'], 'beta': row['weibull_beta']}
                else:
                    # "Calculating Weibull Params from Modules t50 and T90"
                    t50, t90 = row['t50'], row['t90']
                    weibullIParams = weibull_params({t50: 0.50, t90: 0.90})      
               
                f = weibull_cdf(weibullIParams['alpha'], weibullIParams['beta'])
                
                weibullParamList.append(weibullIParams)

                x = np.clip(df.index - generation, 0, np.inf)
                cdf = list(map(f, x))
                pdf = [0] + [j - i for i, j in zip(cdf[: -1], cdf[1 :])]

                activearea = row['Area']
                if np.isnan(activearea):
                    activearea=0
                
                activeareacount = []
                area_landfill_noncollected = []

                areadisposed_failure = []
                powerdisposed_failure = []
                
                areadisposed_projectlifetime = []
                powerdisposed_projectlifetime = []

                area_repaired = []
                power_repaired = []

                power_resold = []
                area_resold = []

                area_powergen = []  # Active area production.

                area_bad_status = []
                power_bad_status = []
                area_otherpaths = []
                power_otherpaths = []
                
                active=0
                disposed_projectlifetime=0
                powerdisposed_projectlifetime0 = 0
                landfilled_noncollected = 0
                area_resold0 = 0
                power_resold0 = 0
                area_otherpaths0 = 0
                power_otherpaths0 = 0
                area_bad_status0 = 0 
                power_bad_status0 = 0
                for age in range(len(cdf)):
                    disposed_projectlifetime=0
                    landfilled_noncollected = 0
                    area_otherpaths0 = 0
                    
                    
                    if x[age] == 0.0:
                        activeareacount.append(0)
                        areadisposed_failure.append(0)
                        powerdisposed_failure.append(0)
                        areadisposed_projectlifetime.append(0)
                        powerdisposed_projectlifetime.append(0)
                        area_resold.append(0)
                        power_resold.append(0)
                        area_bad_status.append(0)
                        power_bad_status.append(0)
                        area_powergen.append(0)
                        area_repaired.append(0)
                        power_repaired.append(0)
                        area_otherpaths.append(0)
                        power_otherpaths.append(0)
                        area_landfill_noncollected.append(0)
                    else:
                        active += 1
                        deg_nameplate = (1-row['mod_degradation']*0.01)**active  
                        poweragegen = row['mod_eff']*0.01*row['irradiance_stc']*deg_nameplate
                        
                        # FAILURES HERE! 
                        activeareaprev = activearea

                        failures = row['Area']*pdf[age]
                        
                        if failures > activearea:
                            #print("More failures than active area, reducing failures to possibilities now.")
                            failures = activearea
                        
                        area_repaired0 = failures*df.iloc[age]['mod_Repair']*0.01      
                        power_repaired0 = area_repaired0*poweragegen

                        area_notrepaired0 = failures-area_repaired0
                        power_notrepaired0 = area_notrepaired0*poweragegen

                        activearea = activeareaprev-area_notrepaired0

                        if age == int(row['mod_lifetime']+generation):
                            #activearea_temp = activearea
                            merchantTail_area = 0+activearea*(df.iloc[age]['mod_MerchantTail']*0.01)
                            disposed_projectlifetime = activearea-merchantTail_area
                            activearea = merchantTail_area

                            # I don't think these should be here.
                            #area_notrepaired0 = 0
                            #power_notrepaired0 = 0
                            
                            if deg_nameplate > 0.8:
                                # TO DO: check math here
                                area_collected = disposed_projectlifetime*(df.iloc[age]['mod_EOL_collection_eff']*0.01)
                                landfilled_noncollected = disposed_projectlifetime-area_collected
                                
                                area_resold0 = area_collected*(df.iloc[age]['mod_EOL_pg0_resell']*0.01)
                                power_resold0 = area_resold0*poweragegen
                                
                                area_otherpaths0 = area_collected - area_resold0
                                power_otherpaths0 = area_otherpaths0*poweragegen
                                
                                activearea = activearea + area_resold0  
                                
                                # disposed_projectlifetime does not include Merchant Tail & Resold as they went back to ACtive
                                disposed_projectlifetime = disposed_projectlifetime - area_resold0  
                                powerdisposed_projectlifetime0 = disposed_projectlifetime*poweragegen
                            else:
                                area_bad_status0 = disposed_projectlifetime
                                power_bad_status0 = area_bad_status0*poweragegen
                                #powerdisposed_projectlifetime0 = 0 # CHECK? 
                                
#                            activearea = 0+disposed_projectlifetime*(df.iloc[age]['mod_Reuse']*0.01)
#                            disposed_projectlifetime = activearea_temp-activearea
                        

                        areadisposed_failure.append(area_notrepaired0)
                        powerdisposed_failure.append(power_notrepaired0)

                        # TODO IMPORTANT: Add Failures matrices to EoL Matrix.
                        
#                        areadisposed_failure_collected.append(area_notrepaired0*df.iloc[age]['mod_EOL_collection_eff']*0.01)
                        areadisposed_projectlifetime.append(disposed_projectlifetime)
                        powerdisposed_projectlifetime.append(powerdisposed_projectlifetime0)                     

                        area_landfill_noncollected.append(landfilled_noncollected)
    
                        area_repaired.append(area_repaired0)
                        power_repaired.append(power_repaired0)
                        
                        area_resold.append(area_resold0)
                        power_resold.append(power_resold0)
                        
                        area_bad_status.append(area_bad_status0)
                        power_bad_status.append(power_bad_status0)

                        area_otherpaths.append(area_otherpaths0)
                        power_otherpaths.append(power_otherpaths0)

                        activeareacount.append(activearea)
                        area_powergen.append(activearea*poweragegen)                        
                
                try:
                    # becuase the clip starts with 0 for the installation year, identifying installation year
                    # and adding initial area
                    fixinitialareacount = next((i for i, e in enumerate(x) if e), None) - 1
                    activeareacount[fixinitialareacount] = activeareacount[fixinitialareacount]+row['Area']    
                    area_powergen[fixinitialareacount] = (area_powergen[fixinitialareacount] +  
                                         row['Area'] * row['mod_eff'] *0.01 * row['irradiance_stc'])   
                except:
                    # Last value does not have a xclip value of nonzero so it goes
                    # to except. But it also means the loop finished for the calculations
                    # of Lifetime.
                    fixinitialareacount = len(cdf)-1
                    activeareacount[fixinitialareacount] = activeareacount[fixinitialareacount]+row['Area']    
                    area_powergen[fixinitialareacount] = (area_powergen[fixinitialareacount] +  
                                         row['Area'] * row['mod_eff'] *0.01 * row['irradiance_stc'])                   
                    print("Finished Area+Power Generation Calculations")
                    
            
            #   area_disposed_of_generation_by_year = [element*row['Area'] for element in pdf]
                # This used to be labeled as cumulative; but in the sense that they cumulate
                # yearly deaths for all cohorts that die.
                df['Yearly_Sum_Area_disposedby_Failure'] += areadisposed_failure
                df['Yearly_Sum_Power_disposedby_Failure'] += powerdisposed_failure
                
                df['Yearly_Sum_Area_disposedby_ProjectLifetime'] += areadisposed_projectlifetime 
                df['Yearly_Sum_Power_disposedby_ProjectLifetime'] += powerdisposed_projectlifetime 

                df['Yearly_Sum_Area_disposed'] += areadisposed_failure
                df['Yearly_Sum_Area_disposed'] += areadisposed_projectlifetime

                df['Yearly_Sum_Power_disposed'] += powerdisposed_failure
                df['Yearly_Sum_Power_disposed'] += powerdisposed_projectlifetime
                              
                df['Repaired_Area'] += area_repaired
                df['Repaired_[W]'] += power_repaired
                df['Resold_Area'] += area_resold
                df['Resold_[W]'] += power_resold

                df['Status_BAD_Area'] += area_bad_status
                df['Status_BAD_[W]'] += power_bad_status

                df['Area_for_EOL_pathsG'] += area_otherpaths
                df['Power_for_EOL_pathsG'] += power_otherpaths

                df['Installed_Capacity_[W]'] += area_powergen
                df['Cumulative_Active_Area'] += activeareacount
                
                df['Landfill_0'] += area_landfill_noncollected
                
                
                Generation_EOL_pathsG.append(area_otherpaths)
                Matrix_Landfilled_noncollected.append(area_landfill_noncollected)
                Matrix_area_bad_status.append(area_bad_status)
                Matrix_Failures.append(areadisposed_failure)
                
                # Generation_Disposed_byYear.append([x + y for x, y in zip(areadisposed_failure, areadisposed_projectlifetime)])
                
                # Not using at the moment:
                # Generation_Active_byYear.append(activeareacount)
                # Generation_Power_byYear.append(area_powergen)
            
            
            df['WeibullParams'] = weibullParamList

            # We don't need this Disposed by year  because we already collected, merchaint tailed and resold.
            # Just need Landfil matrix, and Paths Good Matrix (and Paths Bad Eventually)
            # MatrixDisposalbyYear = pd.DataFrame(Generation_Disposed_byYear, columns = df.index, index = df.index)
            # MatrixDisposalbyYear = MatrixDisposalbyYear.add_prefix("EOL_on_Year_")
            
            PG = pd.DataFrame(Generation_EOL_pathsG, columns = df.index, index = df.index)
                     
            L0 = pd.DataFrame(Matrix_Landfilled_noncollected, columns = df.index, index=df.index)
            
            PB = pd.DataFrame(Matrix_area_bad_status, columns = df.index, index=df.index)
    
            PF = pd.DataFrame(Matrix_Failures, columns = df.index, index=df.index)

            # Path Bad includes Path Bad from Project Lifetime and adding now 
            #  the path bads from Failures disposed (not repaired)            
            PB = PB + PF
            
            # Updating Path Bad for collection efficiency.
            PBC = PB.mul(df['mod_EOL_collection_eff'].values*0.01)
            PBNC = PB - PBC
            
            # What doesn't get collected of Path Bad, goes to Landfill 0. 
            L0 = L0 + PBNC

            # What goes on forward to Path Bads EoL Pathways is PBC. 
            

            df = df.join(PG.add_prefix("EOL_PG_Year_"))
            df = df.join(L0.add_prefix("EOL_L0_Year_"))
            df = df.join(PBC.add_prefix("EOL_BS_Year"))
            
            df['EOL_Landfill0'] = L0.sum(axis=0)
            df['EOL_BadStatus'] = PBC.sum(axis=0)
            df['EOL_PG'] = PG.sum(axis=0)
            df['EOL_PATHS'] = (PBC+PG).sum(axis=0)            
            
            ## Start to do EOL Processes PATHS GOOD
            #######################################
            
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
            
                       
            # Re-scaling Path Good Matrix, becuase Resold modules already got 
            # resold in the cohort loop above.
            # 'originalMatrix' = reducedMatrix x 100 / (100-p2)
            PG = PG.mul(100/(100-df['mod_EOL_pg0_resell']), axis=0)
            
            # Paths GOOD Check for 100% sum. 
            # If P1-P5 over 100% will reduce landfill.
            # If P2-P5 over 100% it will shut down with Warning and Exit.
            SUMS1 = (df['mod_EOL_pg1_landfill'] + df['mod_EOL_pg0_resell']+
                     df['mod_EOL_pg2_stored'] + df['mod_EOL_pg3_reMFG']+
                     df['mod_EOL_pg4_recycled'])
            SUMS2 = (df['mod_EOL_pg0_resell']+
                     df['mod_EOL_pg2_stored'] + df['mod_EOL_pg3_reMFG']+
                     df['mod_EOL_pg4_recycled'])
            
            if (SUMS2 > 100).any():
                print("WARNING: Paths 0 through 4 should add to a 100%." +
                      " and there is no way to correct by updating " +
                      " path1_landfill. " +
                      " STOPPING SIMULATION NOW GO AND FIX YOUR INPUT. Tx <3")
                return
                      
            if (SUMS1 > 100).any():
                print("Warning: Paths 0 through 4 add to above 100%;"+
                      "Fixing by Updating Landfill value to the remainder of"+
                      "100-(P0+P2+P3+P4).")
                df['mod_EOL_pg1_landfill'] = 100-SUMS2
                
            # PATH1
            PG1_landfill = PG.mul(df['mod_EOL_pg1_landfill'].values*0.01)
            df['PG1_landfill'] = list(PG1_landfill.sum())

            # PATH2
            PG2_stored = PG.mul(df['mod_EOL_pg2_stored'].values*0.01)
            df['PG2_stored'] = list(PG2_stored.sum())
            # TODO: Future development of Stored path here.
            
            # PATH3
            PG3_reMFG = PG.mul(df['mod_EOL_pg3_reMFG'].values*0.01)
            df['PG3_reMFG'] = list(PG3_reMFG.sum())  # Need as output?
            
            PG3_reMFG_yield = PG3_reMFG.mul(df['mod_EOL_reMFG_yield'].values*0.01)
            df['PG3_reMFG_yield'] = list(PG3_reMFG_yield.sum())  # Need as output? 
            
            PG3_reMFG_unyield = PG3_reMFG-PG3_reMFG_yield
            df['PG3_reMFG_unyield'] = list(PG3_reMFG_unyield.sum()) # Need as output?
            
            # PATH 4
            PG4_recycled = PG.mul(df['mod_EOL_pg4_recycled'].values*0.01)
            df['PG4_recycled'] = list(PG4_recycled.sum())
              
            
            # PATH BADS:
            # ~~~~~~~~~~~
            
            
            # Check for 100% sum. 
            # If P1-P5 over 100% will reduce landfill.
            # If P2-P5 over 100% it will shut down with Warning and Exit.
            SUMS1 = (df['mod_EOL_pb1_landfill'] + 
                     df['mod_EOL_pb2_stored'] + df['mod_EOL_pb3_reMFG']+
                     df['mod_EOL_pb4_recycled'])
            SUMS2 = (df['mod_EOL_pb2_stored'] + df['mod_EOL_pb3_reMFG']+
                     df['mod_EOL_pb4_recycled'])
            
            if (SUMS2 > 100).any():
                print("WARNING: Paths B 1 through 4 should add to a 100%." +
                      " and there is no way to correct by updating " +
                      " path1_landfill. " +
                      " STOPPING SIMULATION NOW GO AND FIX YOUR INPUT. Tx <3")
                return
                      
            if (SUMS1 > 100).any():
                print("Warning: Paths B 1 through 4 add to above 100%;"+
                      "Fixing by Updating Landfill value to the remainder of"+
                      "100-(P2+P3+P4).")
                df['mod_EOL_pb1_landfill'] = 100-SUMS2
            
            # PATH1
            PB1_landfill = PBC.mul(df['mod_EOL_pb1_landfill'].values*0.01)
            df['PB1_landfill'] = list(PB1_landfill.sum())

            # PATH2
            PB2_stored = PBC.mul(df['mod_EOL_pg2_stored'].values*0.01)
            df['PB2_stored'] = list(PB2_stored.sum())
            # TODO: Future development of Stored path here.
            
            # PATH3
            PB3_reMFG = PBC.mul(df['mod_EOL_pb3_reMFG'].values*0.01)
            df['PB3_reMFG'] = list(PB3_reMFG.sum())  # Need as output?
            
            PB3_reMFG_yield = PB3_reMFG.mul(df['mod_EOL_reMFG_yield'].values*0.01)
            df['PB3_reMFG_yield'] = list(PB3_reMFG_yield.sum())  # Need as output? 
            
            PB3_reMFG_unyield = PB3_reMFG-PB3_reMFG_yield
            df['PB3_reMFG_unyield'] = list(PB3_reMFG_unyield.sum()) # Need as output?
            
            # PATH 4
            PB4_recycled = PBC.mul(df['mod_EOL_pb4_recycled'].values*0.01)
            df['PB4_recycled'] = list(PB4_recycled.sum())

            # ADD Matrices now for path goods and bads, becuase we don't need 
            # to distinguish on the source of the material stream.
            P1_landfill = PG1_landfill + PB1_landfill 
            P2_stored = PG2_stored + PB2_stored 
            P3_reMFG_yield = PG3_reMFG_yield + PB3_reMFG_yield
            P3_reMFG_unyield = PG3_reMFG_unyield + PB3_reMFG_unyield
            
            df['P2_stored'] = list(P2_stored.sum())

            df['P3_reMFG'] = list((P3_reMFG_yield+P3_reMFG_unyield).sum())
            
            P4_recycled = PG4_recycled + PB4_recycled            
            df['P4_recycled'] = list(P4_recycled.sum())
            
            # Cleanup of internal renaming and internal use columns
            df.drop(['new_Installed_Capacity_[W]', 't50', 't90'], axis = 1, inplace=True) 
            
            # Printout reference of how much more module area is being manufactured.
            # The manufactured efficiency is calculated on more detail on the
            # material loop below for hte mass. 
            df['ModuleTotal_MFG']=df['Area']*100/df['mod_MFG_eff']
            
            ################
            # Material Loop#
            ################

            if materials is None:
                materials = list(self.scenario[scenarios[0]].material.keys())
            else:
                if isinstance(materials, str):
                    materials = [materials]
            
            for mat in materials:

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
                
               
                dm['mat_L0'] = list(L0.multiply(dm['mat_massperm2'], axis=0).sum())
                
                dm['mat_PG2_stored'] = list(P2_stored.multiply(dm['mat_massperm2'],axis=0).sum())
                
                dm['mat_L1'] = list(P1_landfill.multiply(dm['mat_massperm2'], axis=0).sum())
       
                # PATH 3
                mat_reMFG = P3_reMFG_yield.multiply(dm['mat_massperm2'],axis=0)
                mat_reMFG_mod_unyield = P3_reMFG_unyield.multiply(dm['mat_massperm2'],axis=0)
                dm['mat_reMFG'] = list(mat_reMFG.sum())
                dm['mat_reMFG_mod_unyield'] = list(mat_reMFG_mod_unyield.sum())
      
                dm['mat_reMFG_target'] = dm['mat_reMFG'] * dm['mat_PG3_ReMFG_target'] * 0.01
                dm['mat_reMFG_untarget'] = dm['mat_reMFG']-dm['mat_reMFG_target']

                dm['mat_reMFG_yield'] = dm['mat_reMFG_target'] * dm['mat_ReMFG_yield'] * 0.01
                dm['mat_reMFG_unyield'] = dm['mat_reMFG_target'] - dm['mat_reMFG_yield']
                              
                
                # SUBPATH 1: ReMFG to Recycling
                dm['mat_reMFG_all_unyields'] = dm['mat_reMFG_mod_unyield'] + dm['mat_reMFG_untarget'] + dm['mat_reMFG_unyield']
                dm['mat_reMFG_2_recycle'] = dm['mat_reMFG_all_unyields'] * df['mod_EOL_sp_reMFG_recycle']               
                dm['mat_L2'] = dm['mat_reMFG_all_unyields']-dm['mat_reMFG_2_recycle']
                
                
                # PATH 4
                mat_recycled = P4_recycled.multiply(dm['mat_massperm2'],axis=0)
                dm['mat_recycled_PG4'] = list(mat_recycled.sum())
                dm['mat_recycled_all'] = dm['mat_recycled_PG4'] + dm['mat_reMFG_2_recycle'] 
                
                dm['mat_recycled_target'] = dm['mat_recycled_all'] * dm['mat_PG4_Recycling_target'] * 0.01                 
                dm['mat_L3'] = dm['mat_recycled_all'] - dm['mat_recycled_target']  # material un-target

                dm['mat_recycled_yield'] = dm['mat_recycled_target'] * dm['mat_Recycling_yield'] * 0.01
                dm['mat_L4'] = dm['mat_recycled_target'] - dm['mat_recycled_yield']  # material un-target

                # HQ and OQ reycling paths:
                dm['mat_EOL_Recycled_2_HQ'] = dm['mat_recycled_yield'] * dm['mat_EOL_Recycled_into_HQ'] * 0.01
                dm['mat_EOL_Recycled_2_OQ'] = dm['mat_recycled_yield'] - dm['mat_EOL_Recycled_2_HQ']

                dm['mat_EOL_Recycled_HQ_into_MFG'] = dm['mat_EOL_Recycled_2_HQ'] * dm['mat_EOL_RecycledHQ_Reused4MFG'] * 0.01
                dm['mat_EOL_Recycled_HQ_into_OU'] = dm['mat_EOL_Recycled_2_HQ'] - dm['mat_EOL_Recycled_HQ_into_MFG']               
                   
                
                ## Beginning of Life Calculations Now
                ######################################
                # TODO: Close loop later to reduce MFG step... something. mat_reMFG_yield closing to mat_
                
                # CHECK 
                dm['mat_EnteringModuleManufacturing_total'] = (df['Area'] * dm['mat_massperm2']*100/df['mod_MFG_eff'])
                dm['mat_UsedSuccessfullyinModuleManufacturing'] = (df['Area'] * dm['mat_massperm2'])
                dm['mat_LostinModuleManufacturing'] = dm['mat_EnteringModuleManufacturing_total'] - dm['mat_UsedSuccessfullyinModuleManufacturing']

                dm['mat_EnteringModuleManufacturing_total'] = (df['Area'] * dm['mat_massperm2']*100/df['mod_MFG_eff'])
                
                # Input from Successful ReMFG to offset Module Manufacturing Material Needs.
                dm['mat_EnteringModuleManufacturing_virgin'] = dm['mat_EnteringModuleManufacturing_total'] - dm['mat_reMFG_yield']    

                
                # Material Manufacturing Stage                
                dm['mat_Manufacturing_Input'] = dm['mat_EnteringModuleManufacturing_virgin'] / (dm['mat_MFG_eff'] * 0.01)
                
                # Scrap = Lost to Material manufacturing losses + Module manufacturing losses
                dm['mat_MFG_Scrap'] = (dm['mat_Manufacturing_Input'] - dm['mat_EnteringModuleManufacturing_virgin'] + 
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
                
                # Input from Successful Recycling to offset Mateirla Manufacturing Virgin Needs:
                dm['mat_Virgin_Stock'] = dm['mat_Manufacturing_Input'] - dm['mat_EOL_Recycled_HQ_into_MFG'] - dm['mat_MFG_Recycled_HQ_into_MFG']
                
                # Calculate raw virgin needs before mining and refining efficiency losses
                dm['mat_Virgin_Stock_Raw'] = (dm['mat_Virgin_Stock'] * 100 /  dm['mat_virgin_eff'])

                # Add Wastes

                dm['mat_Total_EOL_Landfilled'] = (dm['mat_L0']+  #'mat_modules_NotCollected'] + 
                                                  dm['mat_L1']+ # 'mat Path Good Chosen to be Landfilled + 
                                                  dm['mat_L2']+ # mat not reMFG (yields module, target, or yieldds matr) NOT sent to recycling 
                                                  dm['mat_L3']+ # mat in recycling not TARGET so landfilled +
                                                  dm['mat_L4']) # mat in EOL_Recycled_Losses_Landfilled      
                
                dm['mat_Total_MFG_Landfilled'] = (dm['mat_MFG_Scrap_Landfilled'] + 
                                                 dm['mat_MFG_Scrap_Recycled_Losses_Landfilled'])
                
                dm['mat_Total_Landfilled'] = (dm['mat_Total_EOL_Landfilled'] + 
                                              dm['mat_Total_MFG_Landfilled'])
                
                dm['mat_Total_Recycled_OU'] = (dm['mat_EOL_Recycled_2_OQ'] + 
                                               dm['mat_EOL_Recycled_HQ_into_OU'] + 
                                               dm['mat_MFG_Recycled_into_OQ'] + 
                                               dm['mat_MFG_Recycled_HQ_into_OU'])
 
                
                self.scenario[scen].material[mat].materialdata = dm

         
            # CLEANUP MATRICES HERE:
            #try:
            #    df = df[df.columns.drop(list(df.filter(regex='EOL_PG_Year_')))]
            #except:
            #    print("Warning: Issue dropping EOL_PG columns generated by " \
            #          "calculateMFC routine to overwrite")

            self.scenario[scen].data = df
            
            
    #method to calculate energy flows as a function of mass flows and circular pathways
    def calculateEnergyFlow(self, scenarios=None, materials=None, modEnergy=None, matEnergy=None):
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

            
        for scen in scenarios:
            for mat in materials:
                df = self.scenario[scen].data
                dm = self.scenario[scen].material[mat].materialdata
            #self.modEnergy
            #modEnergy = 
            #matEnergy = 
            
            #modEnergy and matEnergy are input files
                de = pd.DataFrame()
            #module
                print(type(df['ModuleTotal_MFG']))
                print(type(modEnergy['e_mod_MFG']))
                                      
                de['mod_MFG'] = df['ModuleTotal_MFG']*modEnergy['e_mod_MFG']
                de['mod_Install'] = df['Area']*modEnergy['e_mod_Install']
                de['mod_OandM'] = df['Cumulative_Active_Area']*modEnergy['e_mod_OandM']
                de['mod_Repair'] = df['Repaired_Area']*modEnergy['e_mod_Repair']
                de['mod_Demount'] = (df['Resold_Area']+df['Status_BAD_Area']+df['Landfill_0']
                                   +df['Area_for_EOL_pathsG'])*modEnergy['e_mod_Demount']
                de['mod_Store'] = df['P2_stored']*modEnergy['e_mod_Store']
                de['mod_Resell_Certify'] = df['Resold_Area']*modEnergy['e_mod_Resell_Certify']
                de['mod_ReMFG_Disassembly'] = df['P3_reMFG']*modEnergy['e_mod_ReMFG_Disassembly']
                de['mod_Recycle_Crush'] = df['P4_recycled']*modEnergy['e_mod_Recycle_Crush']
            
            #material
                de['mat_extraction'] = dm['mat_Virgin_Stock_Raw']*matEnergy['e_mat_extraction']
                de['mat_MFG'] = dm['mat_Manufacturing_Input']*matEnergy['e_mat_MFG']
                de['mat_MFGScrap_LQ'] = dm['mat_MFG_Scrap_Sentto_Recycling']*matEnergy['e_mat_MFGScrap_LQ']
                de['mat_MFGScrap_HQ'] = dm['mat_MFG_Recycled_into_HQ']*matEnergy['e_mat_MFGScrap_HQ']
                de['mat_Landfill'] = dm['mat_Total_Landfilled']*matEnergy['e_mat_Landfill']
                de['mat_EoL_ReMFG_clean'] = dm['mat_reMFG_target']*matEnergy['e_mat_EoL_ReMFG_clean']
                de['mat_Recycled_LQ'] = dm['mat_recycled_target']*matEnergy['e_mat_Recycled_LQ']
                de['mat_Recycled_HQ'] = dm['mat_EOL_Recycled_2_HQ']*matEnergy['e_mat_Recycled_HQ']
            
            return de
        
    def scenMod_IRENIFY(self, scenarios=None, ELorRL='RL'):
        
        if ELorRL == 'RL':
            weibullInputParams = {'alpha': 5.3759, 'beta': 30}  # Regular-loss scenario IRENA
            print("Using Irena Regular Loss Assumptions")
        if ELorRL == 'EL':
            weibullInputParams = {'alpha': 2.4928, 'beta': 30}  # Regular-loss scenario IRENA
            print("Using Irena Early Loss Assumptions")
            
        if scenarios is None:
            scenarios = list(self.scenario.keys())
        else:
            if isinstance(scenarios, str):
                scenarios = [scenarios]

        for scen in scenarios:
            self.scenario[scen].data['weibull_alpha'] = weibullInputParams['alpha']
            self.scenario[scen].data['weibull_beta'] = weibullInputParams['beta']
            self.scenario[scen].data['mod_lifetime'] = 40.0
            self.scenario[scen].data['mod_MFG_eff'] = 100.0
            
            for mat in self.scenario[scen].material:
                self.scenario[scen].material[mat].materialdata['mat_MFG_eff'] = 100.0   
                self.scenario[scen].material[mat].materialdata['mat_MFG_scrap_Recycled'] = 0.0 
              
        return


    def check_Years_dataandMaterials(self, scenarios=None, materials=None):
        '''
        '''
        print ("Not Done")

    def trim_Years( self, startYear=None, endYear=None, aggregateInstalls=False, 
                   averageEfficiency=False, averageMaterialData = False, methodAddedYears='repeat', 
                   scenarios=None, materials=None):
        '''
        
        methodStart : str
            'trim' or 'aggregate'. Trim cuts the values before the year specified.
            Aggregate sums the values (if any) up to the year specified and sets it
            in that year. No backfilling of data enabled at the moment.
        methodEnd : str
            'repeat' or 'zeroes' only options at the moment. 
            'repeat' Increases to the endYear by repeating the last value. 
            zeroes places zeroes.
            
        '''

        if scenarios is None:
            scenarios = list(self.scenario.keys())
        else:
            if isinstance(scenarios, str):
                scenarios = [scenarios]

        scen0 = scenarios[0]
        dataStartYear = int(self.scenario[scen0].data.iloc[0]['year'])
        dataEndYear = int(self.scenario[scen0].data.iloc[-1]['year'])

        if startYear is None:
            startYear = dataStartYear
            print("startYear not provided. Setting to start year of Module data", startYear)

        if endYear is None:
            endYear = dataEndYear
            print("endYear not provided. Setting to end year of Module data", endYear)

        startYear = startYear
        endYear = endYear


        for scen in scenarios:
            baseline = self.scenario[scen].data
            
            if int(startYear) < int(dataStartYear):
                print("ADD YEARS HERE. not done yet")

            if int(endYear) > int(dataEndYear):
                print("ADD YEARS HERE. not done yet")

            # Add check if data does not need to be reduced to not do these.
            reduced = baseline.loc[(baseline['year']>=startYear) & (baseline['year']<=endYear)].copy()

            if aggregateInstalls:
                prev = baseline.loc[(baseline['year']<startYear)].sum()
                reduced.loc[reduced['year'] == startYear, 'new_Installed_Capacity_[MW]'] = prev['new_Installed_Capacity_[MW]']
            
            if averageEfficiency:
                prev = baseline.loc[(baseline['year']<startYear)].mean()
                reduced.loc[reduced['year'] == startYear, 'mod_eff	'] = prev['mod_eff	']
                
            reduced.reset_index(drop=True, inplace=True)
            self.scenario[scen].data = reduced #reassign the material data to the simulation

            for mat in self.scenario[scen].material:
                if int(startYear) < int(dataStartYear):
                    print("ADD YEARS HERE. not done yet")
    
                if int(endYear) > int(dataEndYear):
                    print("ADD YEARS HERE. not done yet")
    
                matdf = self.scenario[scen].material[mat].materialdata #pull out the df
                reduced = matdf.loc[(matdf['year']>=startYear) & (matdf['year']<=endYear)].copy()
                
                if averageMaterialData == 'average':
                    prev = matdf.loc[(baseline['year']<startYear)].mean()
                    matkeys = list(reduced.keys())[1:12]
                    for matkey in matkeys: # skipping year (0). Skipping added columsn from mass flow
                        reduced.loc[reduced['year'] == startYear, matkey] = prev[matkey]
                
                reduced.reset_index(drop=True, inplace=True)
                self.scenario[scen].material[mat].materialdata = reduced #reassign the material data to the simulation
            

    def scenMod_IRENIFY(self, scenarios=None, ELorRL='RL'):
        
        if ELorRL == 'RL':
            weibullInputParams = {'alpha': 5.3759, 'beta': 30}  # Regular-loss scenario IRENA
            print("Using Irena Regular Loss Assumptions")
        if ELorRL == 'EL':
            weibullInputParams = {'alpha': 2.4928, 'beta': 30}  # Regular-loss scenario IRENA
            print("Using Irena Early Loss Assumptions")
            
        if scenarios is None:
            scenarios = list(self.scenario.keys())
        else:
            if isinstance(scenarios, str):
                scenarios = [scenarios]

        for scen in scenarios:
            self.scenario[scen].data['weibull_alpha'] = weibullInputParams['alpha']
            self.scenario[scen].data['weibull_beta'] = weibullInputParams['beta']
            self.scenario[scen].data['mod_lifetime'] = 40.0
            self.scenario[scen].data['mod_MFG_eff'] = 100.0
            
            for mat in self.scenario[scen].material:
                self.scenario[scen].material[mat].materialdata['mat_MFG_eff'] = 100.0   
                self.scenario[scen].material[mat].materialdata['mat_MFG_scrap_Recycled'] = 0.0 
              
        return



    def scenMod_PerfectManufacturing(self, scenarios=None):
        
        if scenarios is None:
            scenarios = list(self.scenario.keys())
        else:
            if isinstance(scenarios, str):
                scenarios = [scenarios]

        for scen in scenarios:
            self.scenario[scen].data['mod_MFG_eff'] = 100.0
            
            for mat in self.scenario[scen].material:
                self.scenario[scen].material[mat].materialdata['mat_virgin_eff'] = 100.0   
                self.scenario[scen].material[mat].materialdata['mat_MFG_eff'] = 100.0   
        return

    def scenMod_noCircularity(self, scenarios=None):
        
        if scenarios is None:
            scenarios = list(self.scenario.keys())
        else:
            if isinstance(scenarios, str):
                scenarios = [scenarios]

        for scen in scenarios:
            self.scenario[scen].data['mod_EOL_collection_eff '] = 0.0
            self.scenario[scen].data['mod_EOL_collected_recycled'] = 0.0
            self.scenario[scen].data['mod_Repair'] = 0.0
            self.scenario[scen].data['mod_MerchantTail'] = 0.0
            self.scenario[scen].data['mod_Reuse'] = 0.0

            for mat in self.scenario[scen].material:
                self.scenario[scen].material[mat].materialdata['mat_MFG_scrap_Recycled'] = 0.0 
                self.scenario[scen].material[mat].materialdata['mat_MFG_scrap_Recycling_eff'] = 0.0 
                self.scenario[scen].material[mat].materialdata['mat_MFG_scrap_Recycled_into_HQ'] = 0.0 
                self.scenario[scen].material[mat].materialdata['mat_MFG_scrap_Recycled_into_HQ_Reused4MFG'] = 0.0 

                self.scenario[scen].material[mat].materialdata['mod_EOL_p5_recycled'] = 0.0 
                self.scenario[scen].material[mat].materialdata['mat_EOL_Recycling_yield'] = 0.0 
                self.scenario[scen].material[mat].materialdata['mat_EOL_Recycled_into_HQ'] = 0.0 
                self.scenario[scen].material[mat].materialdata['mat_EOL_RecycledHQ_Reused4MFG'] = 0.0 


        return        

    def aggregateResults(self, scenarios=None, materials=None):

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

        keywds = ['mat_Virgin_Stock', 'mat_Total_Landfilled', 'mat_Total_EOL_Landfilled', 'mat_Total_MFG_Landfilled']
        nice_keywds = ['VirginStock', 'WasteAll', 'WasteEOL', 'WasteMFG']

        USyearly=pd.DataFrame()

        for scen in scenarios:
            for ii in range(len(keywds)):
                keywd = keywds[ii]
                nicekey = nice_keywds[ii]

                for mat in materials:
                    USyearly[nicekey+'_'+mat+'_'+self.name+'_'+scen] = self.scenario[scen].material[mat].materialdata[keywd]
                filter_col = [col for col in USyearly if (col.startswith(nicekey) and col.endswith(self.name+'_'+scen)) ]
                USyearly[nicekey+'_Module_'+self.name+'_'+scen] = USyearly[filter_col].sum(axis=1)
                # 2DO: Add multiple objects option

                
        USyearly = USyearly/1000000  # This is the ratio for grams to Metric tonnes
        USyearly = USyearly.add_suffix('_[Tonnes]')
        
        # Different units, so no need to do the ratio to Metric tonnes :p
        keywd1='new_Installed_Capacity_[MW]'
        
        for scen in scenarios:
            USyearly['newInstalledCapacity_'+self.name+'_'+scen+'_[MW]'] = self.scenario[scen].data[keywd1]
 
        # Creating c umulative results
        UScum = USyearly.copy()
        UScum = UScum.cumsum()
 
        # Adding Installed Capacity to US (This is already 'Cumulative') so not including it in UScum
        # We are also renaming it to 'ActiveCapacity' and calculating Decommisioned Capacity. 
        # TODO: Rename Installed_CApacity to ActiveCapacity throughout.
        keywd='Installed_Capacity_[W]'  
        for scen in scenarios:
            USyearly['ActiveCapacity_'+self.name+'_'+scen+'_[MW]'] = self.scenario[scen].data[keywd]/1e6
            USyearly['DecommisionedCapacity_'+self.name+'_'+scen+'_[MW]'] = (
                UScum['newInstalledCapacity_'+self.name+'_'+scen+'_[MW]']-
                USyearly['ActiveCapacity_'+self.name+'_'+scen+'_[MW]'])

        # Adding Decommissioned Capacity

        # Reindexing and Merging
        USyearly.index = self.scenario[scen].data['year']
        UScum.index = self.scenario[scen].data['year']
        
        self.USyearly = USyearly
        self.UScum = UScum
        
        return USyearly, UScum
 
    def plotScenariosComparison(self, keyword=None, scenarios=None):

        if scenarios is None:
            scenarios = list(self.scenario.keys())
        else:
            if isinstance(scenarios, str):
                scenarios = [scenarios]
                
        if keyword is None:
            scens = list(self.scenario.keys())[0]
            print("Choose one of the keywords: ", list(self.scenario[scens].data.keys())) 
            return
        
        yunits = _unitReferences(keyword)
       
        plt.figure()
    
        for scen in scenarios:
            plt.plot(self.scenario[scen].data['year'],self.scenario[scen].data[keyword], label=scen)
        plt.legend()
        plt.xlabel('Year')
        plt.title(keyword.replace('_', " "))
        plt.ylabel(yunits)        


    def plotMetricResults(self):
        from plotly.subplots import make_subplots
       # import plotly.graph_objects as go

        
        y1 = self.plotMaterialResults(keyword='VirginStock', yearlyorcumulative='yearly') 
        y2 = self.plotMaterialResults(keyword='WasteAll', yearlyorcumulative='yearly')
        y3 = self.plotMaterialResults(keyword='WasteEOL', yearlyorcumulative='yearly')
        y4 = self.plotMaterialResults(keyword='WasteMFG', yearlyorcumulative='yearly')
        c1 = self.plotMaterialResults(keyword='VirginStock', yearlyorcumulative='cumulative')
        c2 = self.plotMaterialResults(keyword='WasteAll', yearlyorcumulative='cumulative')
        c3 = self.plotMaterialResults(keyword='WasteEOL', yearlyorcumulative='cumulative')
        c4 = self.plotMaterialResults(keyword='WasteMFG', yearlyorcumulative='cumulative')
        ic = self.plotInstalledCapacityResults()
        
    def plotMaterialResults(self, keyword, yearlyorcumulative='yearly', cumplot=False):
        import plotly.express as px
        import re
        
        if yearlyorcumulative == 'yearly':
            data = self.USyearly
        else:
            data = self.UScum

        if keyword is None:
            print("keyword options are :" 'VirginStock', 'WasteALL', 'WasteEOL', 'WasteMFG')
            return
            #TODO: add a split to first bracket and print unique values option and return.
            
        filter_col = [col for col in data if col.startswith(keyword)]
        
        # Getting Title, Y-Axis Labels, and Legend Readable
        titlekeyword = str.capitalize(yearlyorcumulative) + re.sub( r"([A-Z])", r" \1", keyword)
        units = filter_col[0].split('_')[-1]
        
        mylegend = [col.split('_')[1:] for col in filter_col]
        mylegend = [col[:-1] for col in mylegend]
        mylegend = [' '.join(col) for col in mylegend]
        mylegend = [str.capitalize(col) for col in mylegend]

        fig = px.line(data[filter_col], template="plotly_white")
        
        fig.update_layout(
            title=titlekeyword,
            xaxis_title="Year", 
            yaxis_title=units
        )
        
        for idx, name in enumerate(mylegend):
            fig.data[idx].name = name
            fig.data[idx].hovertemplate = name
        
        if cumplot:
            return fig
        else:
            fig.show()    
        return
    
    def plotInstalledCapacityResults(self, cumplot=False):
        # TODO: Add scenarios input to subselect which ones to plot.

        import plotly.express as px
        
        datay = self.USyearly
        datac = self.UScum
        
        filter_colc = [col for col in datac if col.startswith('newInstalledCapacity')]
        filter_coly = [col for col in datay if col.startswith('Capacity')]

        datay = datay[filter_coly].copy()
        mylegend = [col.split('_')[1:] for col in datay]
        mylegend = [col[:-1] for col in mylegend]
        mylegend = [str(col)[2:-2] for col in mylegend]
        mylegendy = ['Cumulative New Installs, '+col for col in mylegend]

        print(mylegend)
        
        datac = datac[filter_colc].copy()
        mylegend = [col.split('_')[1:] for col in datac]
        mylegend = [col[:-1] for col in mylegend]
        mylegend = [str(col)[2:-2] for col in mylegend]
        mylegendc = ['Capacity, '+col for col in mylegend]

        data = datay.join(datac)
        mylegend = mylegendy + mylegendc
        
        titlekeyword = 'Installed Capacity and Cumulative new Installs'

            
        # Getting Title, Y-Axis Labels, and Legend Readable
        units = filter_colc[0].split('_')[-1]
        

        
        fig = px.line(data, template="plotly_white")
        
        fig.update_layout(
            title=titlekeyword,
            xaxis_title="Year", 
            yaxis_title=units
        )
        
        for idx, name in enumerate(mylegend):
            fig.data[idx].name = name
            fig.data[idx].hovertemplate = name
            
        if cumplot:
            return fig
        else:
            fig.show()    
        return
        

    def plotMaterialComparisonAcrossScenarios(self, keyword=None, scenarios=None, material = None):

        if scenarios is None:
            scenarios = list(self.scenario.keys())
        else:
            if isinstance(scenarios, str):
                scenarios = [scenarios]
    
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
        else:
            if isinstance(material, str) is False: 
                mats = list(self.scenario[scens].material.keys())
                print("Can only pass one material name (str). Choose one of the Materials: ", mats) 
                return

        yunits = _unitReferences(keyword)

        plt.figure()
    
        for scen in scenarios:
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

    def addMaterials(self, materials, baselinefolder=None, nameformat=None):
        
        if baselinefolder is None:
            baselinefolder = r'..\..\baselines'    

        if nameformat is None:
            nameformat = r'\baseline_material_{}.csv'
        for mat in materials:
            filemat = baselinefolder + nameformat.format(mat)
            self.material[mat] = Material(mat, filemat)
    
    
    def modifyMaterials(self, materials, stage, value, start_year=None):
    
        if start_year is None:
            start_year = int(datetime.datetime.now().year)
    
        if materials is None:
            materials = list(self.material.keys())
        else:
            if isinstance(materials, str):
                materials = [materials]

        selectyears = self.data['year']>start_year
        
        for mat in materials:
            self.material[mat].materialdata.loc[selectyears, stage] = value


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

def weibull_pdf_vis(alpha, beta, xlim=56):
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
        i = weibull_pdf(alpha, beta)
    
    idf = list(map(i, x))
    
    return idf


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
        'mat_EOL_Recycling_yield', 'mat_EOL_Recycled_into_HQ', 
        'mat_EOL_RecycledHQ_Reused4MFG', 'mod_Repair',
        'mod_MerchantTail', 'mod_Reuse', 'mod_eff', etc.
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
        'mat_EOL_Recycling_yield', 'mat_EOL_Recycled_into_HQ', 
        'mat_EOL_RecycledHQ_Reused4MFG', 'mod_Repair',
        'mod_MerchantTail', 'mod_Reuse', 'mod_eff', etc.
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