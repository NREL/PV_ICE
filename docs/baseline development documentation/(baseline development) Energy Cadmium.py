#!/usr/bin/env python
# coding: utf-8

# # Baseline Development - Energy of Cadmium
# 
# This journal documents the calculations for the energy of refining cadmium for CdTe PV. The Energy of extraction is calculated separately of the energy of manufacturing. Extraction includes mining and initial processing. Energy of manufacturing covers refining, purification, and incorporation into the semiconductor CdTe. Because Cd is a secondary product of zinc, e_mat_extractin will be zinc mining energy. Additionally, energies associated with refining zinc will be included in Cd energy as necessary steps on the way to cadmium purification. The manufacturing energy includes a % fuel contribution.

# In[ ]:


import numpy as np
import pandas as pd
import os,sys
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[ ]:


baselinesfolder = str(Path().resolve().parent.parent /'PV_ICE' / 'baselines')
supportMatfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'baselines' / 'SupportingMaterial')


# In[ ]:


cwd = os.getcwd() #grabs current working directory
print(cwd)


# #### Mining Energy
# See the Supporting Materials Folder, input-energy-CdTe-ZnCdMining.csv for the collected data. Based on the numbers, and notes/caveats, a value of 2.0 kWh/kg was assumed for e_mat_extraction.

# #### Manufacturing Energy

# In[ ]:


skipcols = ['Source', 'Notes']
e_modmfg_raw = pd.read_csv(os.path.join(supportMatfolder, "input-energy-CdTe-moduleMFGing.csv"), index_col='year')
                           #, usecols=lambda x: x not in skipcols)


# In[ ]:





# In[ ]:




