# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:12:46 2020

@author: Silvana

Using pytest to create unit tests for PV ICE
to run unit tests, run pytest from the command line in the bifacial_radiance directory
to run coverage tests, run py.test --cov-report term-missing --cov=bifacial_radiance

cd C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\tests

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
    r1.createScenario('standard', file=MODULEBASELINE)
    r1.scenario['standard'].addMaterial('glass', file=MATERIALBASELINE)
    failyear = r1.scenario['standard'].data['mod_lifetime'][0] 
    r1.calculateMassFlow()
    # Assert all modules go to trash at end of lifetime
    assert r1.scenario['standard'].data['EOL_on_Year_'+str(int(failyear)+1)].iloc[0] == 0
    # Assert that since the manufacturing process is perfect, and there is no
    # trash and recycled input on this year, euqlas 0
    mat_massperm2 = r1.scenario['standard'].material['glass'].materialdata['mat_massperm2'].iloc[0]
    assert (r1.scenario['standard'].data['Area'][0]*mat_massperm2-
            r1.scenario['standard'].material['glass'].materialdata['mat_Virgin_Stock'][0]) == 0.0
    

def test_infinite_Weibull():
    r1 = PV_ICE.Simulation()
    r1.createScenario('standard', file=MODULEBASELINE)
    r1.scenario['standard'].addMaterial('glass', file=MATERIALBASELINE)
    r1.scenario['standard'].data['mod_lifetime'] = 50.0
    failyear = r1.scenario['standard'].data['mod_lifetime'][0] 
    r1.calculateMassFlow()
    data = r1.scenario['standard'].data
    EOLrow = data.loc[0, data.columns.str.startswith("EOL_on_Year")]
    assert round(r1.scenario['standard'].data['Area'][0],0) ==round(EOLrow.sum(),0)
    EOLrow = data.loc[10, data.columns.str.startswith("EOL_on_Year")]
    assert round(r1.scenario['standard'].data['Area'][10],0) ==round(EOLrow.sum(),0)

    # If no recycling as input material, then virgin material is constant for this scenario
    r1.scenario['standard'].material['glass'].materialdata['mat_EOL_RecycledHQ_Reused4MFG'] = 0.0
    r1.calculateMassFlow()
    assert r1.scenario['standard'].material['glass'].materialdata['mat_Virgin_Stock'][0] == r1.scenario['standard'].data['Area'][10]*mat_massperm2
    
    # If nothing is collected, everything goes to landfill.
    r1.scenario['standard'].data['mod_EOL_collection_eff'] = 0.0
    r1.calculateMassFlow()
    # Comparing to a year in the future where steady state has been achieved.
    assert (round(r1.scenario['standard'].data['Area'][0]*mat_massperm2,0) == 
    round(r1.scenario['standard'].material['glass'].materialdata['mat_Total_Landfilled'][30],0))
    assert (round(r1.scenario['standard'].material['glass'].materialdata['mat_Total_Landfilled'][0],0) ==
    round(r1.scenario['standard'].material['glass'].materialdata['mat_Total_EOL_Landfilled'][0],0))


def test_landfilledArea_vs_AreafromWaste():
    r1 = PV_ICE.Simulation()
    r1.createScenario('standard', file=MODULEBASELINE)
    r1.scenario['standard'].addMaterial('glass', file=MATERIALBASELINE)
    r1.scenario['standard'].data['mod_EOL_collection_eff'] = 0.0
    r1.calculateMassFlow()
    data = r1.scenario['standard'].data
    matdata = r1.scenario['standard'].material['glass'].materialdata
    UscumAreaDisp_100years = data['Cumulative_Area_disposed'].cumsum()
    UscumAreaDisp_100years = UscumAreaDisp_100years*1e-6 # convert to km2
    B = UscumAreaDisp_100years.iloc[-1]
    
    UScumLandfillGr_disposed_tonnes = matdata['mat_Total_Landfilled']/1000000
    UScumLandfillGr_disposed_tonnes = UScumLandfillGr_disposed_tonnes.cumsum()
    A = UScumLandfillGr_disposed_tonnes.iloc[-1]
    A = A*1000 # convet to kg
    A = A/20 # convert to modules if each module is 22 kg
    A = A*2 # convert to area if each module is ~2 m2
    A = A*1e-6 # Convert to km 2
    assert (round(A,0) == (round(B,0))  
