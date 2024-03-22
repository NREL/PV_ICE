#!/usr/bin/env python
# coding: utf-8

# Attempting to make materials more dynamic by defining some classes

# In[3]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


# In[30]:


class Material:
    """
    create the material inputs more dynamically
    properties of a material:
    materialname = name the material
    thickness = single value or value over time
    marketshare = single value or value over time of the marketshare of a particular material
    nlayers = number of layers of the material that appear in a pv module
    
    
    """
            
    densitydict = {        # density of common PV materials in g/m^3
        'glass': 2500*1000,
        'silicon': 2.3290*1e6,
        'aluminium': 2.70*1e6,
        'silver':  10.49*1e6,
        'copper': 8.96*1e6,
        'encapsulant': 1.0*1e6, #average of several materials
        'backsheet': 1.5*1e6 #average of tedlar and kynar composite films
    }
    
    def __init__(self, materialname, thickness=None, nlayers=None):
        self.materialname = materialname
        self.thickness = thickness
        self.nlayers = nlayers
        if materialname in densitydict:
            self.density = densitydict[materialname]

    def setDensity(self, user_density=None): # add a type check to user
        if user_density is None:
            print('Please enter a density in g/m^3 for the target material.')
        else:
            self.density = user_density
    
    def setThickness(self, user_thickness=None):
        if user_thickness is None:
            print('Please enter the thickness of a single layer in mm. It can be a list over time.')
        else:
            self.thickness = user_thickness
    
    


# In[36]:


glass = Material('glass')
range_thickness = {'thickness':[2,2,2,2,2,2,2]}
glass.setThickness(range_thickness)


# In[37]:


glass.thickness

