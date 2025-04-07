#!/usr/bin/env python
# coding: utf-8

# # Glass Baseline: V2, splitting G-G and G-B
# This journal documents and generates the calculations supporting the splitting of the PV ICE module baseline into a glass-glass and a glass-backsheet conformation. This deconvolutes the information of the two, enabling more refined modeling.

# In[1]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
from urllib.request import urlretrieve
import glob
#import PV_ICE
cwd = os.getcwd() #grabs current working directory


# In[2]:


#print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("pyplot ", plt.matplotlib.__version__)
#print("PV_ICE version ", PV_ICE.__version__)


# In[3]:


supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
baselinesFolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
cwd


# In[59]:


#skipcols = ['Source', 'Source.1']
density_glass = 2500*1000 # g/m^3   
thicknesses = pd.DataFrame({'gtr3mm':3.2,
            '2to3mm':2.5,
            'less2mm':1.8}, index=['mm']) #dataframe of the glass thicknesses
glass_gpm2 = thicknesses/1000*density_glass
glass_gpm2


# In[5]:


#pd.read_csv(os.path.join(baselinesFolder, ''), index_col = 0, usecols=['year','mat_massperm2'], skiprows=[1])

#pull in the complete marketshare of module conformation and glass thickness file
glass_raw = pd.read_excel(os.path.join(supportMatfolder,'input_Marketshare_Glass_Thickness_G-GvG-B.xlsx'), 
                           index_col=0, header=[0,1])


# In[16]:


glass_raw.columns
#glass_raw['Module conformation marketshare']['glass-glass'].dropna(how='all')


# In[50]:


glass_data = glass_raw.drop(level=1,columns='Source', axis=1) #drop the source columns for interpolation
#glass_data
glass_filled = glass_data.interpolate(limit_direction='both') #interpolate to fill years of missing data
glass_fract = glass_filled/100 #turn % into fractions
glass_fract


# In[ ]:





# ## Glass-Backsheet Glass Intensity
# Early modules were mostly glass-backsheet, but marketshare has decreased over time. Most front glass is the 3.2mm, but marketshare of 2.5mm has been increasing. We will multiply the thicknesses by glass density and marketshare to get an average glass intensity for a module by year:
# 
#     avg_glassperm2 = SUM(thickness_glass * density_glass * marketshare)

# In[70]:


#multiply each thickness by density to get fraction of mass per m2
g_b_frontglassmass = glass_fract['g-b front glass thickness']*glass_gpm2.values
g_b_glassMass = g_b_frontglassmass.sum(axis=1)


# ## Glass-Glass Glass Intensity
# This is becoming the dominant technology. We assume in early years that both front and back glass are 2.5mm, because the  marketshare of 2.5mm glass and the marketshare of g-g are nearly identical, as reported by ITRPV. Newer reports provide more discrete data.

# In[92]:


#multiply each thickness by density to get fraction of mass per m2
#front side glass
g_g_frontglasses = glass_fract['g-g front glass thickness']*glass_gpm2.values
g_g_frontglassMass = g_g_frontglasses.sum(axis=1)

#back side glass
g_g_backglasses = glass_fract['back glass thickness']*glass_gpm2.values
g_g_backglassMass = g_g_backglasses.sum(axis=1)

#sum the front and back glasses
g_g_glassMass = g_g_frontglassMass+g_g_backglassMass


# In[93]:


plt.plot(g_b_glassMass, label='G-B')
plt.plot(g_g_glassMass, label='G-G')
plt.title('Glass Intensity over time')
plt.ylabel('grams/m$^2$')
plt.ylim(7000,14000)
plt.legend()


# ## Create a Single Average glass weight by marketshare as well
# In addition, here we will also use the module conformation marketshare to create a single average of glass intentsity per year. Ideally, we will only use this for demonstration/graphing, use the individual g-g and g-b weights in respective baselines to improve model accuracy.

# In[96]:


g_b_market_mass = glass_fract['Module conformation marketshare']['glass-backsheet']*g_b_glassMass
g_g_market_mass = glass_fract['Module conformation marketshare']['glass-glass']*g_g_glassMass
avg_module_glassMass = g_g_market_mass + g_b_market_mass


# In[97]:


plt.plot(g_b_glassMass, label='G-B')
plt.plot(g_g_glassMass, label='G-G')
plt.plot(avg_module_glassMass, label='Market Avg')

plt.title('Glass Intensity over time')
plt.ylabel('grams/m$^2$')
plt.ylim(7000,14000)
plt.legend()


# In[106]:


output_glass_gmp2_baselines = pd.DataFrame([avg_module_glassMass,g_b_glassMass,g_g_glassMass], index=['market_avg_module','G-B','G-G']).T
output_glass_gmp2_baselines.to_csv(os.path.join(supportMatfolder, 'output_glass_gmp2_baselines.csv'))

