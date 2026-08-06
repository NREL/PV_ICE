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
from datetime import date

print("DATE: ", date.today())
print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# In[5]:


US_base_dir = r'C:\Users\sayala\Documents\GitHub\PV_ICE\PV_ICE\baselines'
US_baseline_file = 'baseline_modules_mass_US_Si.csv' # 'baseline_modules_mass_US_updatedT50T90.csv'
US_baseline_file_CdTe = 'baseline_modules_mass_US_CdTe.csv'
degradation_file = r'PVFleets_Degradation_Data.csv' # same folder

out_dir = 'baselines_fleetsdeg'


# In[6]:


# SI First
baseline_path = os.path.join(US_base_dir, US_baseline_file)

# --- Read baseline ---
df_raw = pd.read_csv(baseline_path)
columns_order = df_raw.columns.tolist()
units_row = df_raw.iloc[0:1].copy()          # exact units row as in source

deg = pd.read_csv(degradation_file, sep=None, engine='python')


capacity_col  = 'new_Installed_Capacity_[MW]'
year_col  = 'year'

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

# Work on a cleaned copy for math
df_base = df_raw.iloc[1:].copy()

# Coerce numerics to drop non-numeric rows (like the units row) for calculations
df_base[year_col] = pd.to_numeric(df_base[year_col], errors='coerce')
df_base[capacity_col] = pd.to_numeric(df_base[capacity_col], errors='coerce')

# --- Helper: prepend units row and enforce original column order ---
def finalize_with_units(df_calc: pd.DataFrame) -> pd.DataFrame:
    # Reorder to original columns (plus any new ones we ensured in units_row)
    df_calc = df_calc.reindex(columns=columns_order)
    # Align units row to same columns
    units_aligned = units_row.reindex(columns=columns_order)
    # Prepend units row exactly as it appeared
    out = pd.concat([units_aligned, df_calc], ignore_index=True)
    return out

year_num = pd.to_numeric(df_raw[year_col], errors='coerce')
mask_startyear = year_num >= 2017

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
    base_name = "baseline_modules_mass_Si"   # no .csv, just the stem
    out_name = f"{base_name}__cohort_{pct:0.2f}pct__deg_{abs(rate):0.1f}.csv"
    df_out = finalize_with_units(df_cohort)
    out_path = os.path.join(out_dir, out_name)
    df_out.to_csv(out_path, index=False)
    saved_files.append(Path(out_path).stem)

saved_files


# In[7]:


# SI First
baseline_path = os.path.join(US_base_dir, US_baseline_file_CdTe)

# --- Read baseline ---
df_raw = pd.read_csv(baseline_path)
columns_order = df_raw.columns.tolist()
units_row = df_raw.iloc[0:1].copy()          # exact units row as in source

deg = pd.read_csv(degradation_file, sep=None, engine='python')


capacity_col  = 'new_Installed_Capacity_[MW]'
year_col  = 'year'

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

# Work on a cleaned copy for math
df_base = df_raw.iloc[1:].copy()

# Coerce numerics to drop non-numeric rows (like the units row) for calculations
df_base[year_col] = pd.to_numeric(df_base[year_col], errors='coerce')
df_base[capacity_col] = pd.to_numeric(df_base[capacity_col], errors='coerce')

# --- Helper: prepend units row and enforce original column order ---
def finalize_with_units(df_calc: pd.DataFrame) -> pd.DataFrame:
    # Reorder to original columns (plus any new ones we ensured in units_row)
    df_calc = df_calc.reindex(columns=columns_order)
    # Align units row to same columns
    units_aligned = units_row.reindex(columns=columns_order)
    # Prepend units row exactly as it appeared
    out = pd.concat([units_aligned, df_calc], ignore_index=True)
    return out

year_num = pd.to_numeric(df_raw[year_col], errors='coerce')
mask_startyear = year_num >= 2017

saved_files_CdTE = []

for _, row in deg.iterrows():
    rate = float(row['deg_rate'])        # typically negative in PV Fleets (e.g., -2.0 %/yr)
    pct = float(row['cohort_pct'])       # in percent (e.g., 5.0 means 5%)

    df_cohort = df_base.copy()

    # Scale the installed capacity by the cohort share
    df_cohort[capacity_col] = df_cohort[capacity_col] * (pct / 100.0)

    # Set mod_degradation to the positive number (e.g., 2.0 for -2.0), per your example
    df_cohort.loc[mask_startyear, 'mod_degradation'] = abs(rate)

    # Save per-cohort file
    base_name = "baseline_modules_mass_CdTe"   # no .csv, just the stem
    out_name = f"{base_name}__cohort_{pct:0.2f}pct__deg_{abs(rate):0.1f}.csv"
    df_out = finalize_with_units(df_cohort)
    out_path = os.path.join(out_dir, out_name)
    df_out.to_csv(out_path, index=False)
    saved_files_CdTE.append(Path(out_path).stem)

saved_files_CdTE


# In[8]:


out_dir


# In[9]:


import re
deg_parts = [re.search(r'(deg_[^_]+)$', n).group(1) for n in saved_files if re.search(r'(deg_[^_]+)$', n)]


# In[10]:


r1 = PV_ICE.Simulation(name='Sim1', path=testfolder)


# In[11]:


r1.createScenario(name='base_Si', massmodulefile='baseline_modules_mass_US_Si.csv', energymodulefile='baseline_modules_energy.csv')
r1.scenario['base_Si'].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant'])


# In[12]:


r1.createScenario(name='base_CdTe', massmodulefile='baseline_modules_mass_US_CdTe.csv', energymodulefile='baseline_modules_energy.csv')
r1.scenario['base_CdTe'].addMaterials(['cadmium', 'tellurium', 'glass_cdte', 'aluminium_frames_cdte', 'encapsulant_cdte', 'copper_cdte'])


# In[13]:


for ii in range(0, len(saved_files)):
    foopath = r'C:\Users\sayala\Documents\GitHub\PV_ICE\Studies\PVWaste_for_EPRI_US_National_PVFleetsDg_Si&CdTe_Nov25\baselines_fleetsdeg'
    ii_csv = saved_files[ii] + '.csv'
    ii_csv_path =  os.path.join(foopath, ii_csv)
    ii_name = 'Si_'+deg_parts[ii]
    r1.createScenario(name=ii_name, massmodulefile=ii_csv_path, energymodulefile='baseline_modules_energy.csv')
    r1.scenario[ii_name].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant'])


# In[14]:


for ii in range(0, len(saved_files)):
    foopath = r'C:\Users\sayala\Documents\GitHub\PV_ICE\Studies\PVWaste_for_EPRI_US_National_PVFleetsDg_Si&CdTe_Nov25\baselines_fleetsdeg'
    ii_csv = saved_files[ii] + '.csv'
    ii_csv_path =  os.path.join(foopath, ii_csv)
    ii_name = 'CdTe_'+deg_parts[ii]
    r1.createScenario(name=ii_name, massmodulefile=ii_csv_path, energymodulefile='baseline_modules_energy.csv')
    r1.scenario[ii_name].addMaterials(['cadmium', 'tellurium', 'glass_cdte', 'aluminium_frames_cdte', 'encapsulant_cdte', 'copper_cdte'])


# In[15]:


#r1.trim_Years(startYear=1995, endYear=2026)
r1.trim_Years(startYear=1995, endYear=2036)


# In[16]:


r1.calculateFlows()


# In[17]:


USyearly, UScum = r1.aggregateResults()


# In[18]:


#r1.saveSimulation()


# In[19]:


UScum.to_csv('Cumulative_2036.csv')
USyearly.to_csv('Yearly_2036.csv')


# In[ ]:


UScum.to_csv('Cumulative.csv')
USyearly.to_csv('Yearly.csv')


# In[ ]:


UScum.keys()[:80]


# # POST PROCESSING

# In[ ]:


#'WasteEOL_Module_Sim1_base_Si_[Tonnes]'
#'WasteEOL_Module_Sim1_Si_deg_5.2_[Tonnes]'


# In[20]:


# 1. identify the deg_* columns
deg_cols = [c for c in UScum.columns if c.startswith("WasteEOL_Module_Sim1_Si_deg_")]

total_col = 'WasteEOL_Module_Sim1_Si_deg_TOTAL_[Tonnes]'

# 2. create a new column with the row-wise sum
UScum[total_col] = UScum[deg_cols].sum(axis=1)


# In[21]:


# 1. identify the deg_* columns
deg_cols = [c for c in UScum.columns if c.startswith("WasteEOL_Module_Sim1_CdTe_deg_")]

total_col_CdTe = 'WasteEOL_Module_Sim1_CdTe_deg_TOTAL_[Tonnes]'

# 2. create a new column with the row-wise sum
UScum[total_col_CdTe] = UScum[deg_cols].sum(axis=1)


# In[22]:


main_results= UScum[['WasteEOL_Module_Sim1_base_Si_[Tonnes]', 'WasteEOL_Module_Sim1_base_CdTe_[Tonnes]', total_col, total_col_CdTe]]


# In[ ]:


pwd


# In[35]:


#main_results.to_csv('Main_Results.csv')
main_results.to_csv('Main_Results_2036.csv')


# # Mini excel

# In[36]:


deg_colsSi = [c for c in UScum.columns if c.startswith("WasteEOL_Module_Sim1_Si_deg_")]
deg_colsCdTe = [c for c in UScum.columns if c.startswith("WasteEOL_Module_Sim1_CdTe_deg_")]


# In[42]:


import re
import pandas as pd

# --- Base total (Si + CdTe) ---
base_total = (
    UScum["WasteEOL_Module_Sim1_base_Si_[Tonnes]"] +
    UScum["WasteEOL_Module_Sim1_base_CdTe_[Tonnes]"]
)

# --- helper to extract numeric degradation value (or TOTAL) ---
def extract_deg(col):
    m = re.search(r"deg_([0-9.]+|TOTAL)", col)
    return m.group(1) if m else None

# keep only deg columns with numeric value or TOTAL
deg_colsSi_use   = [c for c in deg_colsSi   if extract_deg(c) is not None]
deg_colsCdTe_use = [c for c in deg_colsCdTe if extract_deg(c) is not None]

deg_vals = sorted({extract_deg(c) for c in deg_colsSi_use})

deg_sum = {}

for d in deg_vals:
    si_col   = next(c for c in deg_colsSi_use   if f"deg_{d}" in c)
    cdte_col = next(c for c in deg_colsCdTe_use if f"deg_{d}" in c)

    deg_sum[f"deg_{d}_TOTAL"] = UScum[si_col] + UScum[cdte_col]

# final df: base + ONLY summed deg columns
deg_df = pd.concat([base_total.rename("base_TOTAL"), pd.DataFrame(deg_sum, index=UScum.index)], axis=1)


# In[43]:


deg_df


# In[44]:


deg_df.columns = (
    deg_df.columns
    .str.replace("deg_", "", regex=False)
    .str.replace("_TOTAL", "", regex=False)
)


# In[45]:


deg_df.keys()


# In[46]:


deg_df["TOTAL_to_base_ratio"] = (
    deg_df["TOTAL"] / deg_df["base"]
)


# In[48]:


plt.plot(deg_df.TOTAL_to_base_ratio)


# In[50]:


deg_df.TOTAL_to_base_ratio


# In[49]:


deg_df.to_csv('waste_cum_clean_togetherforSi&CdTe_2036.csv')


# In[71]:


import numpy as np
import matplotlib.pyplot as plt

# --- slice to start at 2020 ---
deg_df_2020 = deg_df.loc[deg_df.index >= 2020]

# --- pick only numeric degradation columns like '0.2', '0.4', ...
num_cols = []
num_vals = []
for c in deg_df_2020.columns:
    try:
        v = float(c)
        num_cols.append(c)
        num_vals.append(v)
    except (ValueError, TypeError):
        pass

# sort by numeric degradation value
order = np.argsort(num_vals)
num_cols = [num_cols[i] for i in order]
num_vals = [num_vals[i] for i in order]

# --- stacked data (convert to million tonnes) ---
Y = np.vstack([
    deg_df_2020[c].to_numpy() / 1e6
    for c in num_cols
])
x = deg_df_2020.index.to_numpy()

# --- colors: light vs dark blue split at 2.0 ---
light_blue = "#9ecae1"
dark_blue  = "#08519c"
colors = [light_blue if v < 2.0 else dark_blue for v in num_vals]

# --- plot ---
plt.figure()

# stacked degradation scenarios
plt.stackplot(
    x, Y,
    labels=[str(v) for v in num_vals],
    colors=colors
)

# base case line (orange), also in million tonnes
plt.plot(
    x,
    deg_df_2020["base"] / 1e6,
    linewidth=2.5,
    color="orange",
    label="Reference - all systems @ 0.7"
)

plt.xlabel("Year")
plt.ylabel("PV capacity above 80% \nof initial output [Million Tonnes]")
#plt.title("End-of-life PV under degradation scenarios vs base case")

# --- reorder legend so base appears first ---
handles, labels = plt.gca().get_legend_handles_labels()
base_idx = labels.index("Reference - all systems @ 0.7")
handles = [handles[base_idx]] + handles[:base_idx] + handles[base_idx+1:]
labels  = [labels[base_idx]]  + labels[:base_idx]  + labels[base_idx+1:]

plt.legend(handles, labels, loc="upper left", ncol=2, fontsize=8)


leg = plt.legend(
    handles,
    labels,
    title="Degradation assumption (%/yr)",
    loc="upper left",
    ncol=2,
    fontsize=8
)
leg.get_title().set_fontsize(9)


plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# ## PLOTS 

# In[23]:


'Si_'+deg_parts[ii]


# In[24]:


plt.plot(r1.scenario['base_Si'].dataIn_m.year, r1.scenario['base_Si'].dataIn_m['new_Installed_Capacity_[MW]'])
plt.plot(r1.scenario['base_CdTe'].dataIn_m.year, r1.scenario['base_CdTe'].dataIn_m['new_Installed_Capacity_[MW]'])
plt.ylabel('Yearly Installed Capacity [MW]')


# In[19]:


# Cumulative plot
plt.plot(r1.scenario['base_Si'].dataIn_m.year,
         r1.scenario['base_Si'].dataIn_m['new_Installed_Capacity_[MW]'].cumsum(),
         label='Si')

plt.plot(r1.scenario['base_CdTe'].dataIn_m.year,
         r1.scenario['base_CdTe'].dataIn_m['new_Installed_Capacity_[MW]'].cumsum(),
         label='CdTe')

plt.legend()
plt.xlabel('Year')
plt.ylabel('US Cumulative Installed Capacity [MW]')
plt.title('Cumulative Installed Capacity Over Time')
plt.show()


# In[41]:


plt.figure(figsize=(6, 6))  # square-ish figure

plt.rcParams.update({
    'font.size': 20,
    'axes.labelsize': 19,
    'axes.titlesize': 10,
    'legend.fontsize': 20
})


# Cumulative plot
plt.plot(
    r1.scenario['base_Si'].dataIn_m.year,
    r1.scenario['base_Si'].dataIn_m['new_Installed_Capacity_[MW]'].cumsum(),
    label='Si'
)

plt.plot(
    r1.scenario['base_CdTe'].dataIn_m.year,
    r1.scenario['base_CdTe'].dataIn_m['new_Installed_Capacity_[MW]'].cumsum(),
    label='CdTe'
)

plt.yscale('log')
plt.xlim(right=2025)

plt.legend()
plt.xlabel('Year')
plt.ylabel('US Cumulative Capacity [MW]')
#plt.title('Cumulative Installed Capacity Over Time')

plt.tight_layout()
plt.show()


# In[25]:


r1.scenario['base_Si'].dataIn_m.year


# In[29]:


r1.scenario['base_Si'].dataIn_m['new_Installed_Capacity_[MW]']
#20.926667 MW
#8586.216928 + 41399.161240


# In[26]:


# PVRW


# In[27]:


main_results.keys()


# In[28]:


df = main_results[[
    "WasteEOL_Module_Sim1_base_Si_[Tonnes]",
    "WasteEOL_Module_Sim1_base_CdTe_[Tonnes]",
    "WasteEOL_Module_Sim1_Si_deg_TOTAL_[Tonnes]",
    "WasteEOL_Module_Sim1_CdTe_deg_TOTAL_[Tonnes]"
]].assign(
    base_TOTAL=lambda x: x.iloc[:, 0] + x.iloc[:, 1],
    deg_TOTAL=lambda x: x.iloc[:, 2] + x.iloc[:, 3],
)[["base_TOTAL", "deg_TOTAL"]]


# In[29]:


plt.plot(df)


# In[30]:


df["deg_to_base_ratio"] = df["deg_TOTAL"] / df["base_TOTAL"]


# In[32]:


plt.plot(df.deg_to_base_ratio)


# In[34]:


df["deg_increase_pct"] = (
    df["deg_TOTAL"] / df["base_TOTAL"] - 1
) * 100


# In[ ]:


plt.plot(df.deg_increase_pct)


# In[ ]:




