#!/usr/bin/env python
# coding: utf-8

# # Glass Baseline: V2, splitting G-G and G-B
# This journal documents and generates the calculations supporting the splitting of the PV ICE module baseline into a glass-glass and a glass-backsheet conformation. This deconvolutes the information of the two, enabling more refined modeling.

# In[ ]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
from urllib.request import urlretrieve
import glob
#import PV_ICE
cwd = os.getcwd() #grabs current working directory


# In[ ]:


#print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("pyplot ", plt.matplotlib.__version__)
#print("PV_ICE version ", PV_ICE.__version__)


# In[ ]:


supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')
baselinesFolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines')
cwd


# In[ ]:


skipcols = ['Source', 'Source.1']
density_glass = 2500*1000 # g/m^3   


# In[ ]:


pd.read_csv(os.path.join(baselinesFolder, ''), 
            index_col = 0, usecols=['year','mat_massperm2'], skiprows=[1])

glass_raw = pd.read_csv(cwd+"/../../../PV_ICE/baselines/SupportingMaterial/Marketshare_glass.csv", 
                           index_col='Year', usecols=lambda x: x not in skipcols)


# In[ ]:





# In[ ]:





# In[ ]:




