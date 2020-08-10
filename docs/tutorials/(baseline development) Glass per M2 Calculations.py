#!/usr/bin/env python
# coding: utf-8

# # (baseline development) Glass per M2 Calculations
# 

# Based on ITRPV numbers. ITRPV 2014 sets thickness of glass to 3.5, so assuming that value for all previous modules since 1995.
# Starting 2015 ITRPV, transparent backside (both glass & transparent sheets) starts at 2%. Assuming 50% is glass-glass.  same front thickness.
# 
# Starting 2017, front thicknesses are indicated for front side. Thinner modules coincide with the values for expected bifacial modules with glass-glass backside, so assuming all thiner modules have a backside of same thickness.
# 
# Glass backside thickness is not specified, so assuming for glass-glass backside is 2 mm thick for all cases
# where front side is between 2-3 mm (assuming 2 mm for front side), and 1.8mm for cases where front side is < 2 mmm ( assuming 1.8mm for front side as well)
# 
# So overall module per panel is 3.5 for single side glass to up 4 mm glass-glass
# 
# <b>Assumptions</b>:
# 
# 1 - Assuming nothing Glass-Glass before 2012 (not on ITRPV, bifacial not significant yet).

# In[16]:


import numpy as np
density_glass = 2500 # kg/m^3    


# Glass-Glass starts on ITRPV 2012, with 2 %. Since there is still no other record for Glass thickness, assuming same thickness for back than front.

# In[18]:


# Up to 2012
thickness_glass = 0.0032  # m
glassperm2 = thickness_glass * density_glass
print("Glass kg/m2 up to 2012:", glassperm2)


# Glass-Glass percentage starts to increase over the following years. 
# 
# On ITRPV, percentage for 2013 is 98% glass-backsheet,
# percentage for 2014 is 96 % glass-backsheet
# percentage for 2015 is 98 % glass -backsheet.
# 
# We deemed that this sudden shift in the industry from 98 to 96 and then up to 97 did not make sense, so we linearly interpolated for these years

# In[20]:


#2013 - 2015
thickness_glass = 0.0032 * 0.98 + (0.0032+0.0032)*0.02 # m
glassperm2 = thickness_glass * density_glass
print("Glass kg/m2 2013-2015:", glassperm2)


# In[22]:


#2016 
thickness_glass = 0.0032 * 0.97 + (0.0032+0.0032)*0.03 # m
glassperm2 = thickness_glass * density_glass
print("Glass kg/m2 2013-2015:", glassperm2)


# In[ ]:


#201
thickness_glass = 0.0032 * 0.98 + (0.0032+0.0032)*0.02 # m
glassperm2 = thickness_glass * density_glass
print("2013:", glassperm2)


# In[11]:


# 2014 to 2016:
thickness_glass = 0.0035  # m
glassperm2 = thickness_glass * density_glass
print("Glass kg/m2 up 2014-2016:", glassperm2)


# In[14]:


# 2017:
thickness_glass = 0.0035 * 0.94 + 0.0025 * 0.06
glassperm2 = thickness_glass * density_glass
print("Glass kg/m2 up 2014-2016:", glassperm2)


# In[8]:


# 2018:
thickness_glass = 0.0035 * 0.93 + 0.0025 * 0.07
glassperm2 = thickness_glass * density_glass
print("Glass kg/m2 up 2014-2016:", glassperm2)


# In[ ]:


#2019 - 2020:


# All modules have front glass, consider front glass thickness.
# Some modules have back glass, calculate from G-G and G-B plots
# Assume thickness for back glasses
# 
# Bifacial can be G-G or G-B. But there's also monofacial G-G and G-B.
# 
# 90 G-B, 10 G-G
# 95 Monofacial, 5 Bifacial,
# 
# then 100% of bifacial should be G-G, and 5% Monofaial GG...
# 
# Bifacial modules are not a proxy for 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




