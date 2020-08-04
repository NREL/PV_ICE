#!/usr/bin/env python
# coding: utf-8

# # (baseline development) Glass per M2 Calculations
# 

# Based on ITRPV numbers. ITRPV 2014 sets thickness of glass to 3.5, so assuming that value for all previous modules since 1995.
# Starting 2015 ITRPV, transparent backside (glass + transparent sheet) starts at 2%. Assuming 50% is glass and same front thickness.
# 
# Starting 2017, front thicknesses are indicated for front side. Thinner modules coincide with the values for expected bifacial modules with glass-glass backside, so assuming all thiner modules have a backside of same thickness.
# 
# Glass backside thickness is not specified, so assuming for glass-glass backside is 2 mm thick for all cases
# where front side is between 2-3 mm (assuming 2 mm for front side), and 1.8mm for cases where front side is < 2 mmm ( assuming 1.8mm for front side as well)
# 
# So overall module per panel is 3.5 for single side glass to up 4 mm glass-glass
# 

# In[9]:


import numpy as np
density_glass = 2500 # kg/m^3    


# In[7]:


# U to 2014:
thickness_glass = 0.0035  # m
glassperm2 = thickness_glass * density_glass
print("Glass per m2 up to 2014:", glassperm2)


# In[8]:


# 2015 - 2018 :
thickness_glass = 0.0035 * 0.99 + 0.004 * 0.01  # m
glassperm2 = thickness_glass * density_glass
print("Glass per m2 up to 2014:", np.round(glassperm2,6))


# In[ ]:


#2019 - 2020:


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




