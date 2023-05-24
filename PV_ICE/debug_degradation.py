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


# In[1]:

sim1.calculateMassFlow(debugflag=True, nameplatedeglimit=0.3)
sim1.saveSimulation()
