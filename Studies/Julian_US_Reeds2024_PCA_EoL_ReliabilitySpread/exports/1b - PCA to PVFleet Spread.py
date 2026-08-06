#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import glob
from pathlib import Path
import pandas as pd


# In[4]:


testfolder = 'TEMP'


# In[5]:


# =========================================================
# INPUTS
# =========================================================

pca_dir = os.path.join(testfolder, 'PCAs_Method2_Hybrid')   # folder with your PCA baseline files
degradation_file = r'PVFleets_Degradation_Data.csv'

out_dir = os.path.join(pca_dir, 'baselines_fleetsdeg')
os.makedirs(out_dir, exist_ok=True)

capacity_col = 'new_Installed_Capacity_[MW]'
year_col = 'year'
deg_col_target = 'mod_degradation'


# In[9]:


# =========================================================
# LOAD DEGRADATION TABLE
# =========================================================

degradation_file = r'PVFleets_Degradation_Data.csv' # same folder

deg = pd.read_csv(degradation_file, sep=None, engine='python')
deg.columns = [c.strip() for c in deg.columns]

rename_map = {}
for c in deg.columns:
    if 'Degradation' in c and 'Rate' in c:
        rename_map[c] = 'deg_rate'
    if '%' in c and ('Cohort' in c or 'cohort' in c):
        rename_map[c] = 'cohort_pct'

deg = deg.rename(columns=rename_map)

deg['deg_rate'] = pd.to_numeric(deg['deg_rate'], errors='coerce')
deg['cohort_pct'] = pd.to_numeric(deg['cohort_pct'], errors='coerce')
deg = deg.dropna(subset=['deg_rate', 'cohort_pct']).copy()
deg = deg.reset_index(drop=True)

# optional: add a bin id so filenames stay unique even if deg_rate repeats
deg['deg_bin'] = [f"{i+1:02d}" for i in range(len(deg))]

print(deg[['deg_bin', 'deg_rate', 'cohort_pct']].head())


# In[10]:


# =========================================================
# HELPER
# =========================================================

def finalize_with_units(df_calc: pd.DataFrame, units_row: pd.DataFrame, columns_order: list) -> pd.DataFrame:
    df_calc = df_calc.reindex(columns=columns_order)
    units_aligned = units_row.reindex(columns=columns_order)
    out = pd.concat([units_aligned, df_calc], ignore_index=True)
    return out


# In[11]:


# =========================================================
# FIND PCA FILES
# =========================================================

all_pca_files = glob.glob(os.path.join(pca_dir, '*.csv'))

# keep only the main PCA baseline files, not already-generated degradation files
all_pca_files = [f for f in all_pca_files if 'degbin_' not in os.path.basename(f)]

print(f"Found {len(all_pca_files)} PCA baseline files")

saved_files = []


# In[12]:


# =========================================================
# LOOP OVER PCA FILES
# =========================================================

for baseline_path in all_pca_files:
    basefile = os.path.basename(baseline_path)
    stem = Path(baseline_path).stem   # e.g. MidCase_Si_p1

    # -----------------------------
    # READ PCA BASELINE FILE
    # -----------------------------
    df_raw = pd.read_csv(baseline_path)
    columns_order = df_raw.columns.tolist()
    units_row = df_raw.iloc[0:1].copy()
    df_base = df_raw.iloc[1:].copy()

    # numeric coercion for calculations
    df_base[year_col] = pd.to_numeric(df_base[year_col], errors='coerce')
    df_base[capacity_col] = pd.to_numeric(df_base[capacity_col], errors='coerce')

    if deg_col_target in df_base.columns:
        df_base[deg_col_target] = pd.to_numeric(df_base[deg_col_target], errors='coerce')

    # only set modified degradation from 2017 onward
    mask_startyear = df_base[year_col] >= 2017

    # -----------------------------
    # MAKE ONE FILE PER DEG BIN
    # -----------------------------
    for _, row in deg.iterrows():
        rate = float(row['deg_rate'])         # may be negative in source
        pct = float(row['cohort_pct'])        # percent share
        deg_bin = row['deg_bin']

        df_cohort = df_base.copy()

        # scale capacity by cohort share
        df_cohort[capacity_col] = df_cohort[capacity_col] * (pct / 100.0)

        # set degradation as positive absolute value from 2017 onward
        df_cohort.loc[mask_startyear, deg_col_target] = abs(rate)

        # output filename
        # simpler naming: no explicit cohort string
        out_name = f"{stem}__degbin_{deg_bin}__deg_{abs(rate):0.1f}.csv"

        df_out = finalize_with_units(df_cohort, units_row, columns_order)
        out_path = os.path.join(out_dir, out_name)
        df_out.to_csv(out_path, index=False)

        saved_files.append(out_name)

print(f"Saved {len(saved_files)} degradation-by-PCA files")
print(saved_files[:10])


# In[ ]:




