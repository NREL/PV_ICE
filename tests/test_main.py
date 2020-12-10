# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:12:46 2020

@author: Silvana

Using pytest to create unit tests for PV ICE
to run unit tests, run pytest from the command line in the bifacial_radiance directory
to run coverage tests, run py.test --cov-report term-missing --cov=bifacial_radiance

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
    
