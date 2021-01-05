#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# This Journal supports the documentation of the baseline input files for the PV_ICE calculator by graphing all baseline inputs of modules and materials for all years. Currently, this includes:
# - USA module installs
# - Global module intalls
# - glass
# - silicon
# - silver (preliminary)

# In[4]:


#read in baseline csv files
cwd = os.getcwd() #grabs current working directory
baseline_modules_US = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_modules_US.csv")
baseline_modules_World = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_modules_World.csv")
baseline_modules_World_Irena_2016 = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_modules_World_Irena_2016.csv")
baseline_modules_World_Irena_2019 = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_modules_World_Irena_2019.csv")
baseline_materials_glass = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_material_glass.csv")
baseline_materials_silicon = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_material_silicon.csv")
baseline_materials_silver = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_material_silver.csv")


# # Module Files 

# ## USA

# In[6]:


print(baseline_modules_US.columns)

