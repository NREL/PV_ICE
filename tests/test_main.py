# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:12:46 2020

@author: Silvana

Using pytest to create unit tests for PV DEMICE
to run unit tests, run pytest from the command line in the bifacial_radiance directory
to run coverage tests, run py.test --cov-report term-missing --cov=bifacial_radiance

"""

import PVDEMICE
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
    r1 = PVDEMICE.Simulation()
    r1.createScenario('standard', file=MODULEBASELINE)
    r1.scenario['standard'].addMaterial('glass', file=MATERIALBASELINE)
    failyear = r1.scenario['standard'].data['mod_lifetime'][0] 
    r1.calculateMassFlow()
    assert r1.scenario['standard'].data['Failed_on_Year_'+str(int(failyear)+1)].iloc[0] == 0
    
