# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:12:46 2020

@author: Silvana

Using pytest to create unit tests for PV ICE
to run unit tests, run pytest from the command line in the PV_ICE directory
to run coverage tests, run py.test --cov-report term-missing --cov=PV_ICE

"""

import PV_ICE
import numpy as np
import pytest
import os


# try navigating to tests directory so tests run from here.
try:
    os.chdir('tests')
except:
    pass


TESTDIR = os.path.dirname(__file__)  # this folder

# test the Baseline and Module on dummy input files in the /test/ directory
MODULEBASELINE = 'baseline_module_test.csv'
MATERIALBASELINE = 'baseline_material_test.csv'

def test_project_lifetime():
    r1 = PV_ICE.Simulation()
    r1.createScenario('standard', massmodulefile=MODULEBASELINE)
    r1.scenario['standard'].addMaterial('glass', massmatfile=MATERIALBASELINE)
    failyear = r1.scenario['standard'].dataIn_m['mod_lifetime'][0] 
    r1.calculateMassFlow(debugflag=True)
    # Assert all modules go to trash at end of lifetime
    assert r1.scenario['standard'].dataDebug_m['EOL_PG_Year_'+str(int(failyear)+1)].iloc[0] == 0
    # Assert that since the manufacturing process is perfect, and there is no
    # trash and recycled input on this year, euqlas 0
    mat_massperm2 = r1.scenario['standard'].material['glass'].matdataIn_m['mat_massperm2'].iloc[0]
    assert (r1.scenario['standard'].dataOut_m['Area'][0]*mat_massperm2-
            r1.scenario['standard'].material['glass'].matdataOut_m['mat_Virgin_Stock'][0]) == 0.0
    

def test_infinite_Weibull():
    r1 = PV_ICE.Simulation()
    r1.createScenario('standard', massmodulefile=MODULEBASELINE)
    r1.scenario['standard'].addMaterial('glass', massmatfile=MATERIALBASELINE)
    r1.scenario['standard'].dataIn_m['mod_lifetime'] = 50.0
    r1.calculateMassFlow(debugflag=True)
    data = r1.scenario['standard'].dataDebug_m

    # If no recycling as input material, then virgin material is constant for this scenario
    r1.scenario['standard'].material['glass'].matdataIn_m['mat_EOL_RecycledHQ_Reused4MFG'] = 0.0
    r1.calculateMassFlow()
    mat_massperm2 = r1.scenario['standard'].material['glass'].matdataIn_m['mat_massperm2'].iloc[0]

    assert r1.scenario['standard'].material['glass'].matdataOut_m['mat_Virgin_Stock'][0] == r1.scenario['standard'].dataOut_m['Area'][10]*mat_massperm2
    
    # If nothing is collected, everything goes to landfill.
    r1.scenario['standard'].dataIn_m['mod_EOL_collection_eff'] = 0.0
    r1.calculateMassFlow()
    # Comparing to a year in the future where steady state has been achieved.
    assert (round(r1.scenario['standard'].dataOut_m['Area'][0]*mat_massperm2/1000,0) == 
    round(r1.scenario['standard'].material['glass'].matdataOut_m['mat_Total_Landfilled'][30]/1000,0))
    assert (round(r1.scenario['standard'].material['glass'].matdataOut_m['mat_Total_Landfilled'][0],0) ==
    round(r1.scenario['standard'].material['glass'].matdataOut_m['mat_Total_EOL_Landfilled'][0],0))


def test_landfilledArea_vs_AreafromWaste():
    r1 = PV_ICE.Simulation()
    r1.createScenario('standard', massmodulefile=MODULEBASELINE)
    r1.scenario['standard'].addMaterial('glass', massmatfile=MATERIALBASELINE)
    r1.scenario['standard'].dataIn_m['mod_EOL_collection_eff'] = 0.0
    r1.calculateMassFlow()
    data = r1.scenario['standard'].dataOut_m
    matdata = r1.scenario['standard'].material['glass'].matdataOut_m
    UscumAreaDisp_100years = data['Yearly_Sum_Area_atEOL'].cumsum() # original called for Cumulative_Area_disposed
    UscumAreaDisp_100years = UscumAreaDisp_100years*1e-6 # convert to km2
    B = UscumAreaDisp_100years.iloc[-1]
    
    UScumLandfillGr_disposed_tonnes = matdata['mat_Total_Landfilled']/1000000
    UScumLandfillGr_disposed_tonnes = UScumLandfillGr_disposed_tonnes.cumsum()
    A = UScumLandfillGr_disposed_tonnes.iloc[-1]
    A = A*1000 # convet to kg
    A = A/20 # convert to modules if each module is 22 kg
    A = A*2 # convert to area if each module is ~2 m2
    A = A*1e-6 # Convert to km 2
    assert (round(A,0) == (round(B,0))) 
