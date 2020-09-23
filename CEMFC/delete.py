# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 09:58:31 2020

@author: sayala
"""

quickstart example

file = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_modules_US.csv'
fileglass = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_material_glass.csv'
r1 = Simulation()
r1.createScenario('standard', file=r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_modules_US.csv')
r1.scenario['standard'].addMaterial('glass', fileglass )

r1.__dict__
r1.scenario['standard']
r1.scenario['standard'].__dict__
r1.scenario['standard'].material['glass']

foo = ScenarioObj('test')        
foo.__dict__
foo.set_sceneario_baseline('ideal', file)
foo.__dict__
foo.set_sceneario_baseline('decadent', file)

foo.module['ideal']['data']

foo.set_sceneario_baseline('decadent', file)



file = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_modules_US.csv'
foo = ScenarioObj('test')        
foo.__dict__
foo.set_sceneario_baseline('ideal', file)
foo.__dict__
foo.set_sceneario_baseline('decadent', file)

foo.module['ideal']['data']

foo.set_sceneario_baseline('decadent', file)
