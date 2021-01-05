#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 28})
plt.rcParams['figure.figsize'] = (30, 15)


# This journals' purpose is to graph all baselines used as inputs the the PV_ICE Model.

# In[2]:


cwd = os.getcwd() #grabs current working directory
#shows list of baseline files available


# In[13]:


#read in all baseline files
#Module files
modules_US = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_modules_US.csv", index_col='year', skiprows=[1])
modules_World = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_modules_World.csv", index_col='year', skiprows=[1])
modules_World_Irena_2016 = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_modules_World_Irena_2016.csv", index_col='year', skiprows=[1])
modules_World_Irena_2019 = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_modules_World_Irena_2019.csv", index_col='year', skiprows=[1])
#material files
material_glass = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_material_glass.csv", index_col='year', skiprows=[1])
material_glass_Reeds = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_material_glass_Reeds.csv", index_col='year', skiprows=[1])
material_silicon = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_material_silicon.csv", index_col='year', skiprows=[1])
material_silver = pd.read_csv(cwd+"/../../PV_ICE/baselines/baseline_material_silver.csv", index_col='year', skiprows=[1])

