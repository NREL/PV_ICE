# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:43:40 2020

@author: Silvana
"""

import PV_DEMICE

file = r'C:\Users\Silvana\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_modules_US.csv'
fileglass = r'C:\Users\Silvana\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_material_glass.csv'
r1 = PV_DEMICE.Simulation()
r1.createScenario('standard', file=file)
r1.scenario['standard'].addMaterial('glass', fileglass )
