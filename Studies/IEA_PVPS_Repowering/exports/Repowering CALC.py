#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path

baselines_fleetsdeg = 'baselines_fleetsdeg' 
testfolder = 'Sims'

if not os.path.exists(testfolder):
    os.makedirs(testfolder)

if not os.path.exists(baselines_fleetsdeg):
    os.makedirs(baselines_fleetsdeg)


# In[2]:


import PV_ICE


# In[3]:


import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.figsize'] = (12, 5)


# In[4]:


# This information helps with debugging and getting support :)
import sys, platform
print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# In[5]:


world_base_dir = r'C:\Users\sayala\Documents\GitHub\PV_ICE\PV_ICE\baselines'
world_baseline_file = 'baseline_modules_mass_World.csv'

degradation_file = r'PVFleets_Degradation_Data.csv' # same folder

out_dir = 'baselines_fleetsdeg'


# In[6]:


# --- Paths ---
baseline_path = os.path.join(world_base_dir, world_baseline_file)

# --- Read baseline ---
df_raw = pd.read_csv(baseline_path)
columns_order = df_raw.columns.tolist()
units_row = df_raw.iloc[0:1].copy()          # exact units row as in source

deg = pd.read_csv(degradation_file, sep=None, engine='python')


# In[7]:


capacity_col  = 'new_Installed_Capacity_[MW]'
year_col  = 'year'


# In[8]:


# Normalize column names (strip spaces, unify)
deg.columns = [c.strip() for c in deg.columns]
# Handle common header variants
rename_map = {}
for c in deg.columns:
    if 'Degradation' in c and 'Rate' in c:
        rename_map[c] = 'deg_rate'
    if '%' in c and ('Cohort' in c or 'cohort' in c):
        rename_map[c] = 'cohort_pct'
deg = deg.rename(columns=rename_map)

# Clean types
deg['deg_rate'] = pd.to_numeric(deg['deg_rate'], errors='coerce')
deg['cohort_pct'] = pd.to_numeric(deg['cohort_pct'], errors='coerce')
deg = deg.dropna(subset=['deg_rate', 'cohort_pct'])


# In[9]:


# Work on a cleaned copy for math
df_base = df_raw.iloc[1:].copy()


# In[10]:


# Coerce numerics to drop non-numeric rows (like the units row) for calculations
df_base[year_col] = pd.to_numeric(df_base[year_col], errors='coerce')
df_base[capacity_col] = pd.to_numeric(df_base[capacity_col], errors='coerce')


# In[11]:


# --- Helper: prepend units row and enforce original column order ---
def finalize_with_units(df_calc: pd.DataFrame) -> pd.DataFrame:
    # Reorder to original columns (plus any new ones we ensured in units_row)
    df_calc = df_calc.reindex(columns=columns_order)
    # Align units row to same columns
    units_aligned = units_row.reindex(columns=columns_order)
    # Prepend units row exactly as it appeared
    out = pd.concat([units_aligned, df_calc], ignore_index=True)
    return out


# In[12]:


year_num = pd.to_numeric(df_raw[year_col], errors='coerce')
mask_startyear = year_num >= 2017


# In[13]:


saved_files = []

for _, row in deg.iterrows():
    rate = float(row['deg_rate'])        # typically negative in PV Fleets (e.g., -2.0 %/yr)
    pct = float(row['cohort_pct'])       # in percent (e.g., 5.0 means 5%)

    df_cohort = df_base.copy()

    # Scale the installed capacity by the cohort share
    df_cohort[capacity_col] = df_cohort[capacity_col] * (pct / 100.0)

    # Set mod_degradation to the positive number (e.g., 2.0 for -2.0), per your example
    df_cohort.loc[mask_startyear, 'mod_degradation'] = abs(rate)

    # Save per-cohort file
    base_name = "baseline_modules_mass_World"   # no .csv, just the stem
    out_name = f"{base_name}__cohort_{pct:0.2f}pct__deg_{abs(rate):0.1f}.csv"
    df_out = finalize_with_units(df_cohort)
    out_path = os.path.join(out_dir, out_name)
    df_out.to_csv(out_path, index=False)
    saved_files.append(Path(out_path).stem)


# In[14]:


saved_files


# In[15]:


import re
deg_parts = [re.search(r'(deg_[^_]+)$', n).group(1) for n in saved_files if re.search(r'(deg_[^_]+)$', n)]


# In[16]:


r1 = PV_ICE.Simulation(name='Sim1', path=testfolder)


# In[17]:


r1.createScenario(name='base', massmodulefile='baseline_modules_mass_World.csv', energymodulefile='baseline_modules_energy.csv')
r1.scenario['base'].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant'])


# In[18]:


for ii in range(0, len(saved_files)):
    #ii = saved_files[0]
    ii_csv = saved_files[ii] + '.csv'
    ii_name = deg_parts[ii]
    r1.createScenario(name=ii_name, massmodulefile=ii_csv, energymodulefile='baseline_modules_energy.csv')
    r1.scenario[ii_name].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant'])


# In[19]:


r1.calculateFlows()


# In[20]:


USyearly, UScum = r1.aggregateResults()


# In[21]:


r1.saveSimulation()


# In[26]:


UScum.to_csv('Cumulative.csv')
USyearly.to_csv('Yearly.csv')


# In[ ]:


'''VirginStock_glass_Sim1_base_[Tonnes]	
VirginStock_silicon_Sim1_base_[Tonnes]	
VirginStock_silver_Sim1_base_[Tonnes]	
VirginStock_copper_Sim1_base_[Tonnes]	
VirginStock_aluminium_frames_Sim1_base_[Tonnes]	
VirginStock_encapsulant_Sim1_base_[Tonnes]	
VirginStock_Module_Sim1_base_[Tonnes]	
WasteAll_glass_Sim1_base_[Tonnes]	
WasteAll_silicon_Sim1_base_[Tonnes]	
WasteAll_silver_Sim1_base_[Tonnes]	
WasteAll_copper_Sim1_base_[Tonnes]	
WasteAll_aluminium_frames_Sim1_base_[Tonnes]	
WasteAll_encapsulant_Sim1_base_[Tonnes]	
WasteAll_Module_Sim1_base_[Tonnes]	
WasteEOL_glass_Sim1_base_[Tonnes]	
WasteEOL_silicon_Sim1_base_[Tonnes]	
WasteEOL_silver_Sim1_base_[Tonnes]	
WasteEOL_copper_Sim1_base_[Tonnes]	
WasteEOL_aluminium_frames_Sim1_base_[Tonnes]	
WasteEOL_encapsulant_Sim1_base_[Tonnes]	
WasteEOL_Module_Sim1_base_[Tonnes]	
WasteMFG_glass_Sim1_base_[Tonnes]	
WasteMFG_silicon_Sim1_base_[Tonnes]	
WasteMFG_silver_Sim1_base_[Tonnes]	
WasteMFG_copper_Sim1_base_[Tonnes]	
WasteMFG_aluminium_frames_Sim1_base_[Tonnes]	
WasteMFG_encapsulant_Sim1_base_[Tonnes]	
WasteMFG_Module_Sim1_base_[Tonnes]
'''


# # POST PROCESSING

# In[28]:


#WasteEOL_Module_Sim1_base_[Tonnes]	
#WasteEOL_Module_Sim1_deg_5.2_[Tonnes]


# In[29]:


# 1. identify the deg_* columns
deg_cols = [c for c in UScum.columns if c.startswith("WasteEOL_Module_Sim1_deg_")]


# In[30]:


# 2. create a new column with the row-wise sum
UScum["WasteEOL_Module_Sim1_deg_TOTAL_[Tonnes]"] = UScum[deg_cols].sum(axis=1)


# In[32]:


UScum["WasteEOL_Module_Sim1_deg_TOTAL_[Tonnes]"]


# In[39]:


UScum.index


# In[48]:


total_col = 'WasteEOL_Module_Sim1_deg_TOTAL_[Tonnes]'


# In[50]:


if "year" in UScum.columns:
    val_2030 = UScum.loc[UScum["year"] == 2030, total_col].squeeze()
else:
    # ensure index is integer (it looks like it already is)
    if UScum.index.dtype != "int64":
        UScum.index = UScum.index.astype(int)
    val_2030 = UScum.loc[2030, total_col]

val_2030


# In[51]:


base_col_res = r'WasteEOL_Module_Sim1_base_[Tonnes]'
if "year" in UScum.columns:
    val_2030_base = UScum.loc[UScum["year"] == 2030, base_col_res].squeeze()
else:
    # ensure index is integer (it looks like it already is)
    if UScum.index.dtype != "int64":
        UScum.index = UScum.index.astype(int)
    val_2030_base = UScum.loc[2030, base_col_res]
val_2030_base


# In[36]:


plt.plot(UScum["WasteEOL_Module_Sim1_base_[Tonnes]"], 'k')
plt.plot(UScum["WasteEOL_Module_Sim1_deg_TOTAL_[Tonnes]"], 'r')


# In[54]:


import matplotlib.pyplot as plt

# Slice from 2025 onward
UScum_2025 = UScum.loc[2025:]

plt.figure(figsize=(8,5))

plt.plot(UScum_2025.index, UScum_2025["WasteEOL_Module_Sim1_base_[Tonnes]"], 'k', label="Baseline (ideal degradation)")
plt.plot(UScum_2025.index, UScum_2025["WasteEOL_Module_Sim1_deg_TOTAL_[Tonnes]"], 'r', label="probability-weighted degradation outcome")

plt.xlabel("Year")
plt.ylabel("Material reaching EOL [Tonnes]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# In[55]:


plt.savefig("wasteEOL_deg_spread.png", dpi=300)  # high-quality PNG


# In[56]:


val_2030_base, val_2030


# In[58]:


val_2030*100/val_2030_base-100

