# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:32:28 2023

@author: sayala
"""


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
import PV_ICE

testfolder = r'C:\Users\sayala\Documents\GitHub\PV_ICE\tests\TEMP'
baselinesfolder = r'C:\Users\sayala\Documents\GitHub\PV_ICE\tests'

MATERIALS = ['silicon']
moduleFile_m = os.path.join(baselinesfolder, 'baseline_modules_mass_test_degradation.csv')

sim1 = PV_ICE.Simulation(name='sim1', path=testfolder)

sim1.createScenario(name='PV_ICE', massmodulefile=moduleFile_m)
for mat in range (0, len(MATERIALS)):
    matbaseline_m = os.path.join(baselinesfolder,'baseline_material_mass_'+MATERIALS[mat]+'_test_degradation.csv')
    sim1.scenario['PV_ICE'].addMaterial(MATERIALS[mat], massmatfile=matbaseline_m)

# In[2]:

nameplatedeglimit = 0.8
bifacialityfactors = None
scen = 'PV_ICE'
installByArea = None
reducecapacity = False
weibullInputParams = None

print("Working on Scenario: ", scen)
print("********************")
df = sim1.scenario[scen].dataIn_m.copy()
initialCols = df.keys()

# Constant
if bifacialityfactors is not None:
    bf = pd.read_csv(bifacialityfactors)
    df['irradiance_stc'] = 1000.0 + bf['bifi']*100.0
    # W/m^2 (min. Bifacial STC Increase)
else:
    df['irradiance_stc'] = 1000.0  # W/m^2

# Renaming and re-scaling
df['t50'] = df['mod_reliability_t50']
df['t90'] = df['mod_reliability_t90']

# Calculating Area and Mass

# Method to pass mass instead of calculating by Power to Area
if 'Mass_[MetricTonnes]' in df:
    df['new_Installed_Capacity_[W]'] = 0
    df['new_Installed_Capacity_[MW]'] = 0
    df['Area'] = df['Mass_[MetricTonnes]']
    print("Warning, this is for special debuging of Wambach " +
          "procedure. Make sure to use `Wambach Module`")
# Method to pass Area to then calculate Power
elif installByArea is not None:
    df['Area'] = installByArea
    df['new_Installed_Capacity_[W]'] = ((df['mod_eff']*0.01) *
                                        df['irradiance_stc'] *
                                        df['Area'])  # W
    df['new_Installed_Capacity_[MW]'] = (
        df['new_Installed_Capacity_[W]']/1000000)
    print("Calculating installed capacity based on installed Area")

# Standard method to calculate Area from the Power
else:
    df['new_Installed_Capacity_[W]'] = (
        df['new_Installed_Capacity_[MW]']*1e6)

    if reducecapacity:
        df['Area'] = (df['new_Installed_Capacity_[W]'] /
                      (df['mod_eff']*0.01)/df['irradiance_stc'])
        # m^2
    else:
        df['Area'] = (df['new_Installed_Capacity_[W]'] /
                      (df['mod_eff']*0.01)/1000.0)  # m^2

df['Area'] = df['Area'].fillna(0)  # Chagne na's to 0s.

# Calculating Wast by Generation by Year, and Cum. Waste by Year.
Generation_EOL_pathsG = []
Matrix_Landfilled_noncollected = []
Matrix_area_bad_status = []
Matrix_Failures = []
weibullParamList = []
# Not used at the moment. legacy. REMOVE?
# Generation_Disposed_byYear = []
# Generation_Active_byYear= []
# Generation_Power_byYear = []

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

# In[3]:
# GENERATION 1 ONLY LOOP

generation=0
row=df.iloc[generation]

if weibullInputParams:
    weibullIParams = weibullInputParams
elif 'weibull_alpha' in row:
    # "Weibull Input Params passed internally as a column"
    weibullIParams = {'alpha': row['weibull_alpha'],
                      'beta': row['weibull_beta']}
else:
    # "Calculating Weibull Params from Modules t50 and T90"
    t50, t90 = row['t50'], row['t90']
    weibullIParams = PV_ICE.weibull_params({t50: 0.50, t90: 0.90})

f = PV_ICE.weibull_cdf(weibullIParams['alpha'],
                weibullIParams['beta'])

weibullParamList.append(weibullIParams)

x = np.clip(df.index - generation, 0, np.inf)
cdf = list(map(f, x))
# TODO: Check this line, does it need commas or remove space
# for linting?
pdf = [0] + [j - i for i, j in zip(cdf[: -1], cdf[1 :])]

activearea = row['Area']
if np.isnan(activearea):
    activearea = 0

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

active = 0
disposed_projectlifetime = 0
powerdisposed_projectlifetime0 = 0
landfilled_noncollected = 0
area_resold0 = 0
power_resold0 = 0
area_otherpaths0 = 0
power_otherpaths0 = 0
area_bad_status0 = 0
power_bad_status0 = 0

# In[3b]:
# age 0

age = 0
disposed_projectlifetime = 0
landfilled_noncollected = 0
area_otherpaths0 = 0

if x[age] == 0.0: # RUNS FOR deployment year (and pre-install years)!
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

# In[3c]:
# Age 1 --

age = 1
disposed_projectlifetime = 0 
landfilled_noncollected = 0 # ? 
area_otherpaths0 = 0
active += 1
firstlife = True

deg_nameplate = (1-row['mod_degradation']*0.01)**active
poweragegen = (row['mod_eff'] * 0.01 *
               row['irradiance_stc']*deg_nameplate)

# FAILURES HERE!
activeareaprev = activearea

failures = row['Area']*pdf[age]

if failures > activearea:
    # TODO: make this code comment pr re,pve
    #print("More failures than active area, reducing failures to possibilities now.")
    failures = activearea

area_repaired0 = (failures *
                  df.iloc[age]['mod_Repair']*0.01)
power_repaired0 = area_repaired0*poweragegen

area_notrepaired0 = failures-area_repaired0
power_notrepaired0 = area_notrepaired0*poweragegen

activearea = activeareaprev-area_notrepaired0

# Degradation check
if deg_nameplate < nameplatedeglimit and firstlife:
    # TODO check this! killing and not sending 
    # to EOL collection paths,
    area_disposed_due_degradation = activearea   # area_disposed_due_degradation new name of area_bad_status0 ?
    power_disposed_due_degradation = (
        area_disposed_due_degradation * poweragegen)
    activearea = 0

# End of project lifetime decisions
if age == int(row['mod_lifetime']+generation):
    # activearea_temp = activearea
    merchantTail_area = (
            0+activearea *
            (df.iloc[age]['mod_MerchantTail']*0.01))
    if merchantTail_area > 0:
        firstlife = False

    disposed_projectlifetime = (activearea -
                                merchantTail_area)
    activearea = merchantTail_area

    # I don't think these should be here.
    # area_notrepaired0 = 0
    # power_notrepaired0 = 0

    #  TO DO: Make deg_nameplate variable an input

    area_collected = (
        disposed_projectlifetime *
        (df.iloc[age]['mod_EOL_collection_eff'] *
         0.01))
    landfilled_noncollected = (
        disposed_projectlifetime-area_collected)

    area_resold0 = (
        area_collected *
        (df.iloc[age]['mod_EOL_pg0_resell']*0.01))
    power_resold0 = area_resold0*poweragegen

    area_otherpaths0 = (
        area_collected - area_resold0)

    power_otherpaths0 = (
        area_otherpaths0 * poweragegen)

    activearea = activearea + area_resold0

    # disposed_projectlifetime does not include
    # Merchant Tail & Resold as they went back to
    # active
    disposed_projectlifetime = (
        disposed_projectlifetime - area_resold0)
    powerdisposed_projectlifetime0 = (
        disposed_projectlifetime*poweragegen)

    # activearea = (0+disposed_projectlifetime*
    #              (df.iloc[age]['mod_Reuse']*0.01))
    # disposed_projectlifetime = ( activearea_temp -
    #                             activearea)

areadisposed_failure.append(area_notrepaired0)
powerdisposed_failure.append(power_notrepaired0)

# TODO IMPORTANT: Add Failures matrices to EoL Matrix.

# areadisposed_failure_collected.append(area_notrepaired0*df.iloc[age]['mod_EOL_collection_eff']*0.01)
areadisposed_projectlifetime.append(
    disposed_projectlifetime)
powerdisposed_projectlifetime.append(
    powerdisposed_projectlifetime0)

area_landfill_noncollected.append(
    landfilled_noncollected)

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
# print('PowerAgeGen: '+str(poweragegen))


# In[3cc]:
# Age 2  through 13: 
       
for age in range(1, 14):
    disposed_projectlifetime = 0
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
        poweragegen = (row['mod_eff'] * 0.01 *
                       row['irradiance_stc']*deg_nameplate)

        # FAILURES HERE!
        activeareaprev = activearea

        failures = row['Area']*pdf[age]

        if failures > activearea:
            # TODO: make this code comment pr re,pve
            #print("More failures than active area, reducing failures to possibilities now.")
            failures = activearea

        area_repaired0 = (failures *
                          df.iloc[age]['mod_Repair']*0.01)
        power_repaired0 = area_repaired0*poweragegen

        area_notrepaired0 = failures-area_repaired0
        power_notrepaired0 = area_notrepaired0*poweragegen

        activearea = activeareaprev-area_notrepaired0

        if age == int(row['mod_lifetime']+generation):
            # activearea_temp = activearea
            merchantTail_area = (
                    0+activearea *
                    (df.iloc[age]['mod_MerchantTail']*0.01))
            disposed_projectlifetime = (activearea -
                                        merchantTail_area)
            activearea = merchantTail_area

            # I don't think these should be here.
            # area_notrepaired0 = 0
            # power_notrepaired0 = 0

            #  TO DO: Make deg_nameplate variable an input
            if nameplatedeglimit > 0.7:
                print("WARNING! nameplatedeglimit has a bug" +
                      "waste duplication, need to check ASAP" +
                      "note from 5/17/2023")
            if deg_nameplate > nameplatedeglimit:
                area_collected = (
                    disposed_projectlifetime *
                    (df.iloc[age]['mod_EOL_collection_eff'] *
                     0.01))
                landfilled_noncollected = (
                    disposed_projectlifetime-area_collected)

                area_resold0 = (
                    area_collected *
                    (df.iloc[age]['mod_EOL_pg0_resell']*0.01))
                power_resold0 = area_resold0*poweragegen

                area_otherpaths0 = (
                    area_collected - area_resold0)

                power_otherpaths0 = (
                    area_otherpaths0 * poweragegen)

                activearea = activearea + area_resold0

                # disposed_projectlifetime does not include
                # Merchant Tail & Resold as they went back to
                # active
                disposed_projectlifetime = (
                    disposed_projectlifetime - area_resold0)
                powerdisposed_projectlifetime0 = (
                    disposed_projectlifetime*poweragegen)
            else: 
                # TODO check this! killing and not sending 
                # to EOL collection paths,
                area_bad_status0 = disposed_projectlifetime
                power_bad_status0 = (
                    area_bad_status0 * poweragegen)
                # powerdisposed_projectlifetime0 = 0 # CHECK?

            # activearea = (0+disposed_projectlifetime*
            #              (df.iloc[age]['mod_Reuse']*0.01))
            # disposed_projectlifetime = ( activearea_temp -
            #                             activearea)

        areadisposed_failure.append(area_notrepaired0)
        powerdisposed_failure.append(power_notrepaired0)

        # TODO IMPORTANT: Add Failures matrices to EoL Matrix.

#                        areadisposed_failure_collected.append(area_notrepaired0*df.iloc[age]['mod_EOL_collection_eff']*0.01)
        areadisposed_projectlifetime.append(
            disposed_projectlifetime)
        powerdisposed_projectlifetime.append(
            powerdisposed_projectlifetime0)

        area_landfill_noncollected.append(
            landfilled_noncollected)

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
        # print('PowerAgeGen: '+str(poweragegen))

# In[3d]: 

# Age 14  
age = 14
disposed_projectlifetime = 0
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
    poweragegen = (row['mod_eff'] * 0.01 *
                   row['irradiance_stc']*deg_nameplate)

    # FAILURES HERE!
    activeareaprev = activearea

    failures = row['Area']*pdf[age]

    if failures > activearea:
        # TODO: make this code comment pr re,pve
        #print("More failures than active area, reducing failures to possibilities now.")
        failures = activearea

    area_repaired0 = (failures *
                      df.iloc[age]['mod_Repair']*0.01)
    power_repaired0 = area_repaired0*poweragegen

    area_notrepaired0 = failures-area_repaired0
    power_notrepaired0 = area_notrepaired0*poweragegen

    activearea = activeareaprev-area_notrepaired0

    if age == int(row['mod_lifetime']+generation):
        # activearea_temp = activearea
        merchantTail_area = (
                0+activearea *
                (df.iloc[age]['mod_MerchantTail']*0.01))
        disposed_projectlifetime = (activearea -
                                    merchantTail_area)
        activearea = merchantTail_area

        # I don't think these should be here.
        # area_notrepaired0 = 0
        # power_notrepaired0 = 0

        #  TO DO: Make deg_nameplate variable an input
        if nameplatedeglimit > 0.7:
            print("WARNING! nameplatedeglimit has a bug" +
                  "waste duplication, need to check ASAP" +
                  "note from 5/17/2023")
        if deg_nameplate > nameplatedeglimit:
            area_collected = (
                disposed_projectlifetime *
                (df.iloc[age]['mod_EOL_collection_eff'] *
                 0.01))
            landfilled_noncollected = (
                disposed_projectlifetime-area_collected)

            area_resold0 = (
                area_collected *
                (df.iloc[age]['mod_EOL_pg0_resell']*0.01))
            power_resold0 = area_resold0*poweragegen

            area_otherpaths0 = (
                area_collected - area_resold0)

            power_otherpaths0 = (
                area_otherpaths0 * poweragegen)

            activearea = activearea + area_resold0

            # disposed_projectlifetime does not include
            # Merchant Tail & Resold as they went back to
            # active
            disposed_projectlifetime = (
                disposed_projectlifetime - area_resold0)
            powerdisposed_projectlifetime0 = (
                disposed_projectlifetime*poweragegen)
        else: 
            # TODO check this! killing and not sending 
            # to EOL collection paths,
            area_bad_status0 = disposed_projectlifetime
            power_bad_status0 = (
                area_bad_status0 * poweragegen)
            # powerdisposed_projectlifetime0 = 0 # CHECK?

        # activearea = (0+disposed_projectlifetime*
        #              (df.iloc[age]['mod_Reuse']*0.01))
        # disposed_projectlifetime = ( activearea_temp -
        #                             activearea)

    areadisposed_failure.append(area_notrepaired0)
    powerdisposed_failure.append(power_notrepaired0)

    # TODO IMPORTANT: Add Failures matrices to EoL Matrix.

#                        areadisposed_failure_collected.append(area_notrepaired0*df.iloc[age]['mod_EOL_collection_eff']*0.01)
    areadisposed_projectlifetime.append(
        disposed_projectlifetime)
    powerdisposed_projectlifetime.append(
        powerdisposed_projectlifetime0)

    area_landfill_noncollected.append(
        landfilled_noncollected)

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
    # print('PowerAgeGen: '+str(poweragegen))
        
# In[3EEE]:
# END OF FOR AGE LOOP

try:
    # becuase the clip starts with 0 for the installation year,
    # dentifying installation year and adding initial area
    fixinitialareacount = next((i for i, e in enumerate(x)
                                if e), None) - 1
    activeareacount[fixinitialareacount] = (
        activeareacount[fixinitialareacount]+row['Area'])
    area_powergen[fixinitialareacount] = (
        area_powergen[fixinitialareacount] +
        row['Area'] * row['mod_eff'] * 0.01 *
        row['irradiance_stc'])
    # TODO: note mentioned 'this addition seems to do nothing.'
    # Check who /when wrote this and if theres need to fix.

except:
    # Last value doesnt have a xclip value of nonzero so it
    # gives except. But it also means the loop finished for
    # the calculations of Lifetime.
    fixinitialareacount = len(cdf)-1
    activeareacount[fixinitialareacount] = (
        activeareacount[fixinitialareacount]+row['Area'])
    area_powergen[fixinitialareacount] = (
        area_powergen[fixinitialareacount] + row['Area'] *
        row['mod_eff'] * 0.01 * row['irradiance_stc'])
    print("Finished Area+Power Generation Calculations")

#   area_disposed_of_generation_by_year = [element*row['Area']
#                                           for element in pdf]
# This used to be labeled as cumulative; but in the sense that
# they cumulate yearly deaths for all cohorts that die.
df['Yearly_Sum_Area_disposedby_Failure'] += (
    areadisposed_failure)
df['Yearly_Sum_Power_disposedby_Failure'] += (
    powerdisposed_failure)

df['Yearly_Sum_Area_disposedby_ProjectLifetime'] += (
    areadisposed_projectlifetime)
df['Yearly_Sum_Power_disposedby_ProjectLifetime'] += (
    powerdisposed_projectlifetime)

df['Yearly_Sum_Area_disposed'] += areadisposed_failure
df['Yearly_Sum_Area_disposed'] += areadisposed_projectlifetime

df['Yearly_Sum_Power_disposed'] += powerdisposed_failure
df['Yearly_Sum_Power_disposed'] += (
    powerdisposed_projectlifetime)

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
Matrix_Landfilled_noncollected.append(
    area_landfill_noncollected)
Matrix_area_bad_status.append(area_bad_status)
Matrix_Failures.append(areadisposed_failure)

# Generation_Disposed_byYear.append([x + y for x, y in
#   zip(areadisposed_failure, areadisposed_projectlifetime)])

# Not using at the moment:
# Generation_Active_byYear.append(activeareacount)
# Generation_Power_byYear.append(area_powergen)

# In[4]:

for generation, row in df[1:].iterrows():
    # generation is an int 0,1,2,.... etc.
    # generation=4
    # row=df.iloc[generation]

    if weibullInputParams:
        weibullIParams = weibullInputParams
    elif 'weibull_alpha' in row:
        # "Weibull Input Params passed internally as a column"
        weibullIParams = {'alpha': row['weibull_alpha'],
                          'beta': row['weibull_beta']}
    else:
        # "Calculating Weibull Params from Modules t50 and T90"
        t50, t90 = row['t50'], row['t90']
        weibullIParams = weibull_params({t50: 0.50, t90: 0.90})

    f = weibull_cdf(weibullIParams['alpha'],
                    weibullIParams['beta'])

    weibullParamList.append(weibullIParams)

    x = np.clip(df.index - generation, 0, np.inf)
    cdf = list(map(f, x))
    # TODO: Check this line, does it need commas or remove space
    # for linting?
    pdf = [0] + [j - i for i, j in zip(cdf[: -1], cdf[1 :])]

    activearea = row['Area']
    if np.isnan(activearea):
        activearea = 0

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

    active = 0
    disposed_projectlifetime = 0
    powerdisposed_projectlifetime0 = 0
    landfilled_noncollected = 0
    area_resold0 = 0
    power_resold0 = 0
    area_otherpaths0 = 0
    power_otherpaths0 = 0
    area_bad_status0 = 0
    power_bad_status0 = 0
    for age in range(len(cdf)):
        disposed_projectlifetime = 0
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
            poweragegen = (row['mod_eff'] * 0.01 *
                           row['irradiance_stc']*deg_nameplate)

            # FAILURES HERE!
            activeareaprev = activearea

            failures = row['Area']*pdf[age]

            if failures > activearea:
                # TODO: make this code comment pr re,pve
                #print("More failures than active area, reducing failures to possibilities now.")
                failures = activearea

            area_repaired0 = (failures *
                              df.iloc[age]['mod_Repair']*0.01)
            power_repaired0 = area_repaired0*poweragegen

            area_notrepaired0 = failures-area_repaired0
            power_notrepaired0 = area_notrepaired0*poweragegen

            activearea = activeareaprev-area_notrepaired0

            if age == int(row['mod_lifetime']+generation):
                # activearea_temp = activearea
                merchantTail_area = (
                        0+activearea *
                        (df.iloc[age]['mod_MerchantTail']*0.01))
                disposed_projectlifetime = (activearea -
                                            merchantTail_area)
                activearea = merchantTail_area

                # I don't think these should be here.
                # area_notrepaired0 = 0
                # power_notrepaired0 = 0

                #  TO DO: Make deg_nameplate variable an input
                if nameplatedeglimit > 0.7:
                    print("WARNING! nameplatedeglimit has a bug" +
                          "waste duplication, need to check ASAP" +
                          "note from 5/17/2023")
                if deg_nameplate > nameplatedeglimit:
                    area_collected = (
                        disposed_projectlifetime *
                        (df.iloc[age]['mod_EOL_collection_eff'] *
                         0.01))
                    landfilled_noncollected = (
                        disposed_projectlifetime-area_collected)

                    area_resold0 = (
                        area_collected *
                        (df.iloc[age]['mod_EOL_pg0_resell']*0.01))
                    power_resold0 = area_resold0*poweragegen

                    area_otherpaths0 = (
                        area_collected - area_resold0)

                    power_otherpaths0 = (
                        area_otherpaths0 * poweragegen)

                    activearea = activearea + area_resold0

                    # disposed_projectlifetime does not include
                    # Merchant Tail & Resold as they went back to
                    # active
                    disposed_projectlifetime = (
                        disposed_projectlifetime - area_resold0)
                    powerdisposed_projectlifetime0 = (
                        disposed_projectlifetime*poweragegen)
                else: 
                    # TODO check this! killing and not sending 
                    # to EOL collection paths,
                    area_bad_status0 = disposed_projectlifetime
                    power_bad_status0 = (
                        area_bad_status0 * poweragegen)
                    # powerdisposed_projectlifetime0 = 0 # CHECK?

                # activearea = (0+disposed_projectlifetime*
                #              (df.iloc[age]['mod_Reuse']*0.01))
                # disposed_projectlifetime = ( activearea_temp -
                #                             activearea)

            areadisposed_failure.append(area_notrepaired0)
            powerdisposed_failure.append(power_notrepaired0)

            # TODO IMPORTANT: Add Failures matrices to EoL Matrix.

#                        areadisposed_failure_collected.append(area_notrepaired0*df.iloc[age]['mod_EOL_collection_eff']*0.01)
            areadisposed_projectlifetime.append(
                disposed_projectlifetime)
            powerdisposed_projectlifetime.append(
                powerdisposed_projectlifetime0)

            area_landfill_noncollected.append(
                landfilled_noncollected)

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
            # print('PowerAgeGen: '+str(poweragegen))

    try:
        # becuase the clip starts with 0 for the installation year,
        # dentifying installation year and adding initial area
        fixinitialareacount = next((i for i, e in enumerate(x)
                                    if e), None) - 1
        activeareacount[fixinitialareacount] = (
            activeareacount[fixinitialareacount]+row['Area'])
        area_powergen[fixinitialareacount] = (
            area_powergen[fixinitialareacount] +
            row['Area'] * row['mod_eff'] * 0.01 *
            row['irradiance_stc'])
        # TODO: note mentioned 'this addition seems to do nothing.'
        # Check who /when wrote this and if theres need to fix.

    except:
        # Last value doesnt have a xclip value of nonzero so it
        # gives except. But it also means the loop finished for
        # the calculations of Lifetime.
        fixinitialareacount = len(cdf)-1
        activeareacount[fixinitialareacount] = (
            activeareacount[fixinitialareacount]+row['Area'])
        area_powergen[fixinitialareacount] = (
            area_powergen[fixinitialareacount] + row['Area'] *
            row['mod_eff'] * 0.01 * row['irradiance_stc'])
        print("Finished Area+Power Generation Calculations")

    #   area_disposed_of_generation_by_year = [element*row['Area']
    #                                           for element in pdf]
    # This used to be labeled as cumulative; but in the sense that
    # they cumulate yearly deaths for all cohorts that die.
    df['Yearly_Sum_Area_disposedby_Failure'] += (
        areadisposed_failure)
    df['Yearly_Sum_Power_disposedby_Failure'] += (
        powerdisposed_failure)

    df['Yearly_Sum_Area_disposedby_ProjectLifetime'] += (
        areadisposed_projectlifetime)
    df['Yearly_Sum_Power_disposedby_ProjectLifetime'] += (
        powerdisposed_projectlifetime)

    df['Yearly_Sum_Area_disposed'] += areadisposed_failure
    df['Yearly_Sum_Area_disposed'] += areadisposed_projectlifetime

    df['Yearly_Sum_Power_disposed'] += powerdisposed_failure
    df['Yearly_Sum_Power_disposed'] += (
        powerdisposed_projectlifetime)

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
    Matrix_Landfilled_noncollected.append(
        area_landfill_noncollected)
    Matrix_area_bad_status.append(area_bad_status)
    Matrix_Failures.append(areadisposed_failure)

    # Generation_Disposed_byYear.append([x + y for x, y in
    #   zip(areadisposed_failure, areadisposed_projectlifetime)])

    # Not using at the moment:
    # Generation_Active_byYear.append(activeareacount)
    # Generation_Power_byYear.append(area_powergen)



# In[5]:
    
df['WeibullParams'] = weibullParamList

# TODO: remove this?
# We don't need this Disposed by year because we already collected,
# merchaint tailed and resold.
# Just need Landfil matrix, and Paths Good Matrix (and Paths Bad
# Eventually)
# MatrixDisposalbyYear = pd.DataFrame(Generation_Disposed_byYear,
#                       columns = df.index, index = df.index)
# MatrixDisposalbyYear = MatrixDisposalbyYear.add_prefix(
#                                                   "EOL_on_Year_")

# Cleanup of old calculations. Needed when you run twice function.
try:
    df = df[df.columns.drop(list(df.filter(regex='^EOL_')))]
except:
    print("Warning: Issue dropping EOL columns generated by "
          "calculateMFC routine to overwrite")

PG = pd.DataFrame(Generation_EOL_pathsG, columns=df.index,
                  index=df.index)

L0 = pd.DataFrame(Matrix_Landfilled_noncollected,
                  columns=df.index, index=df.index)

PB = pd.DataFrame(Matrix_area_bad_status, columns=df.index,
                  index=df.index)

PF = pd.DataFrame(Matrix_Failures, columns=df.index,
                  index=df.index)

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

# # Start to do EOL Processes PATHS GOOD
#######################################

# This Multiplication goes through Module and then material.
# It is for processes that depend on each year as they improve,
# i.e. Collection Efficiency,
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
SUMS1 = (df['mod_EOL_pg1_landfill'] + df['mod_EOL_pg0_resell'] +
         df['mod_EOL_pg2_stored'] + df['mod_EOL_pg3_reMFG'] +
         df['mod_EOL_pg4_recycled'])
SUMS2 = (df['mod_EOL_pg0_resell'] +
         df['mod_EOL_pg2_stored'] + df['mod_EOL_pg3_reMFG'] +
         df['mod_EOL_pg4_recycled'])

if (SUMS2 > 100).any():
    print("WARNING: Paths 0 through 4 should add to a 100%." +
          " and there is no way to correct by updating " +
          " path1_landfill. " +
          " STOPPING SIMULATION NOW GO AND FIX YOUR INPUT. Tx <3")
    return

if (SUMS1 > 100).any():
    print("Warning: Paths 0 through 4 add to above 100%;" +
          "Fixing by Updating Landfill value to the remainder of" +
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

# TODO: evaluate if PG3_reMFG, PG3_reMFG_yield and
# PG3_reMFG_unyield are given as output and if not are needed.
# Also for BAD PATHS PB3_reMFG, PB3_reMFG_yield, PB3_reMFG_unyield

PG3_reMFG = PG.mul(df['mod_EOL_pg3_reMFG'].values*0.01)
df['PG3_reMFG'] = list(PG3_reMFG.sum())

PG3_reMFG_yield = PG3_reMFG.mul(
                            df['mod_EOL_reMFG_yield'].values*0.01)
df['PG3_reMFG_yield'] = list(PG3_reMFG_yield.sum())

PG3_reMFG_unyield = PG3_reMFG-PG3_reMFG_yield
df['PG3_reMFG_unyield'] = list(PG3_reMFG_unyield.sum())

# PATH 4
PG4_recycled = PG.mul(df['mod_EOL_pg4_recycled'].values*0.01)
df['PG4_recycled'] = list(PG4_recycled.sum())

# PATH BADS:
# ~~~~~~~~~~~

# Check for 100% sum.
# If P1-P5 over 100% will reduce landfill.
# If P2-P5 over 100% it will shut down with Warning and Exit.
SUMS1 = (df['mod_EOL_pb1_landfill'] +
         df['mod_EOL_pb2_stored'] + df['mod_EOL_pb3_reMFG'] +
         df['mod_EOL_pb4_recycled'])
SUMS2 = (df['mod_EOL_pb2_stored'] + df['mod_EOL_pb3_reMFG'] +
         df['mod_EOL_pb4_recycled'])

if (SUMS2 > 100).any():
    print("WARNING: Paths B 1 through 4 should add to a 100%." +
          " and there is no way to correct by updating " +
          " path1_landfill. " +
          " STOPPING SIMULATION NOW GO AND FIX YOUR INPUT. Tx <3")
    return

if (SUMS1 > 100).any():
    print("Warning: Paths B 1 through 4 add to above 100%;" +
          "Fixing by Updating Landfill value to the remainder of" +
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
df['PB3_reMFG'] = list(PB3_reMFG.sum())

PB3_reMFG_yield = PB3_reMFG.mul(
                            df['mod_EOL_reMFG_yield'].values*0.01)
df['PB3_reMFG_yield'] = list(PB3_reMFG_yield.sum())

PB3_reMFG_unyield = PB3_reMFG-PB3_reMFG_yield
df['PB3_reMFG_unyield'] = list(PB3_reMFG_unyield.sum())

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
df.drop(['new_Installed_Capacity_[W]', 't50', 't90'],
        axis=1, inplace=True)

# Printout ref. of how much more module area is being manufactured.
# The manufactured efficiency is calculated on more detail on the
# material loop below for hte mass.
df['ModuleTotal_MFG'] = df['Area']*100/df['mod_MFG_eff']

################
# Material Loop#
################