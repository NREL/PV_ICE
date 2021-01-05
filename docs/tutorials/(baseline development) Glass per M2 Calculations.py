#!/usr/bin/env python
# coding: utf-8

# # (baseline development) Glass per M2 Calculations
# 

# Based on ITRPV numbers for the most part, this journal attempts to correlate front glass thickness values with the introduction of glass-glass modules.
# 
# Standard front glass thickness is set to 3.2 mm, based on ITRPV 2014, 2012 and 2011. Starting 2017, front glass are divided into >3 mm, 2-3 mm. Assuming that >3mm is still 3.2 mm. Thinner modules in the range of 2-3mm coincide with the values of Glass-Glass modules, so we are assuming all thiner modules have a backside of same thickness as front of 2.5 mm
# 
# So overall thickness of glass per panel goes from 3.2 to 5 mm for Glass-backsheet to Glass-Glass modules.
# 

# In[1]:


import numpy as np
density_glass = 2500*1000 # g/m^3    


# #### Up to 2012

# In[2]:



thickness_glass = 0.0032  # m
glassperm2 = thickness_glass * density_glass
print("Glass g/m2 up to 2012:", glassperm2)


# #### 2013 - 2016

# Glass-Glass percentage starts to increase over the following years. 
# 
# On ITRPV, percentage for 2013 is 98% glass-backsheet,
# percentage for 2014 is 96 % glass-backsheet
# percentage for 2016 is 97 % glass -backsheet.
# 
# We think it's strange that the % of glass-glass modules went suddenly up in 2014 and then back down in 2016. However we're going ahead with this percentages and will quantify this disaprity as uncertainty with the MC analysis.
# 
# Data is not available on Glass-Glass modules for 2015 so we're interpolating between previous year

# In[3]:


#2013
thickness_glass = 0.0032 * 0.98 + (0.0032+0.0032)*0.02 # m
glassperm2 = thickness_glass * density_glass
print("Glass g/m2 2013:", glassperm2)


# In[4]:


#2014
thickness_glass = 0.0032 * 0.96 + (0.0032+0.0032)*0.04 # m
glassperm2 = thickness_glass * density_glass
print("Glass for 2014:", glassperm2)


# In[5]:


#2015
thickness_glass = 0.0032 * 0.965 + (0.0032+0.0032)*0.035 # m
glassperm2 = thickness_glass * density_glass
print("Glass g/m2 2015:", glassperm2)


# In[6]:


#2016 
thickness_glass = 0.0032 * 0.97 + (0.0032+0.0032)*0.03 # m
glassperm2 = thickness_glass * density_glass
print("Glass g/m2 2016:", glassperm2)


# In[ ]:





# #### 2017 onwards
# 
# Starting 2017, ITRPV includes data on modules with Front glass between 2-3mm thick. Data is also available in various years for the percentage of modules that are Glass-Backsheet, vs Glass-Glass. The percentages for 2-3mm and Glass-Glass modules are very similar. We're assuming that 100% of the Glass-Glass modules are therefore 2-3mm thick for their front AND their back glass. Remaining percentage (if any) of 2-3mm front glasses are assumed to be Glass-backsheet.
# For example for 2017:
# 
# ![ITRPV Glass thicknesses deduction example](../images_wiki/ITRPV_GlassDeduction.PNG)
# 

# In[7]:


#2017
thickness_glass = 0.0032 * (0.94 + 0.01) + (0.0025+0.0025)*0.05 # m
glassperm2 = thickness_glass * density_glass
print("2017:", glassperm2)


# Years afer 2017 that don't have values for any these two categories got interpolated.

# ## Automatic Calculation from SupportingMaterial folder to create baseline_material_Glass

# In[ ]:




