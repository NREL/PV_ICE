#!/usr/bin/env python
# coding: utf-8

# # MassFlows Calculations

# ## 1. Initial setup

# In[1]:


import PV_ICE
import numpy as np
import pandas as pd
import os,sys
import glob
import matplotlib.pyplot as plt
from pathlib import Path


# In[2]:


testfolder = os.path.join(os.getcwd(), 'TEMP')
print ("Your simulation will be stored in %s" % testfolder)


# In[ ]:


baselinesFolder = Path().resolve().parent.parent.parent / 'PV_ICE' / 'PV_ICE' /'baselines'
baselinesFolder


# ### Reading GIS inputs

# In[ ]:


from geopy.geocoders import Nominatim
from geopy.point import Point
# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")


# In[ ]:


GISfile = os.path.join(baselinesFolder, 'SupportingMaterial','gis_centroid_n.csv')
GIS = pd.read_csv(GISfile)
GIS = GIS.set_index('id')


# ## 2. Load PCA baselines, create the 2 Scenarios and assign baselines
# 
# Keeping track of each scenario as its own PV ICE Object.

# Select the method folder you want to run (uncomment your choice). There are three choices:
# 1. Method 1: Uses the raw regionalized capacity by ReEEDS, this creates a very uneven peak of wastes.
# 2. Method 2: Uses ordered wastes between 2021 to 2035 and 2046 to 2050. Still creates unrealistic peaks.
# 3. Method 3: Uses the cummulative capacity between 2021 to 2035 and 2034 to 2050 to create a logarithmic growth of waste (this method is being tested, not validated yet, and subjected to ongoing changes).

# In[ ]:


projectionmethod = 'baselines_fleetsdeg'


# In[ ]:


SFscenarios = ['Mid_Case_Si','Mid_Case_CdTe']


# In[ ]:


testfolder


# In[ ]:


deg_folder = os.path.join(testfolder, 'baselines_fleetsdeg')
all_files = glob.glob(os.path.join(deg_folder, '*.csv'))

print(f"Found {len(all_files)} files")
print(all_files[:5])


# In[ ]:





# In[ ]:


records = []

for f in all_files:
    stem = Path(f).stem
    # expected: Mid_Case_Si_p1__degbin_01__deg_5.2
    parts = stem.split('__')

    main = parts[0]
    degbin = parts[1].replace('degbin_', '') if len(parts) > 1 else None
    degrate = parts[2].replace('deg_', '') if len(parts) > 2 else None

    main_parts = main.split('_')

    pca = main_parts[-1]          # p1
    tech = main_parts[-2]         # Si or CdTe
    scenario = '_'.join(main_parts[:-2])   # Mid_Case

    records.append({
        'filepath': f,
        'filename': os.path.basename(f),
        'scenario': scenario,
        'tech': tech,
        'PCA': pca,
        'degbin': degbin,
        'deg': degrate
    })

files_df = pd.DataFrame(records)
files_df.head()


# In[ ]:


print(files_df['tech'].value_counts())
print(files_df['degbin'].nunique(), "degradation bins")
print(files_df['PCA'].nunique(), "PCAs")


# In[ ]:


PCAs_Si = sorted(files_df.loc[files_df['tech'] == 'Si', 'PCA'].unique())
PCAs_CdTe = sorted(files_df.loc[files_df['tech'] == 'CdTe', 'PCA'].unique())

print("Si PCAs:", len(PCAs_Si))
print("CdTe PCAs:", len(PCAs_CdTe))

PCAs = sorted(set(PCAs_Si) & set(PCAs_CdTe))
print("Shared PCAs:", len(PCAs))


# In[ ]:


degbins = sorted(files_df['degbin'].dropna().unique())
print(degbins)


# In[ ]:


deg_folder = os.path.join(testfolder, 'baselines_fleetsdeg')
results_folder = os.path.join(testfolder, 'results_fleetdeg')
os.makedirs(results_folder, exist_ok=True)

projectionmethod = 'Method2_Hybrid'
scenario_keep = 'Mid_Case'   # scenario part in filename
PERFECTMFG = True

energy_file_Si = 'baseline_modules_energy_Si.csv'
energy_file_CdTe = 'baseline_modules_energy_CdTe.csv'

# materials
materials_Si = [
    'glass', 'silicon', 'silver', 'copper',
    'aluminium_frames', 'encapsulant', 'backsheet'
]

materials_CdTe = [
    'cadmium', 'tellurium', 'glass_cdte',
    'aluminium_frames_cdte', 'encapsulant_cdte', 'copper_cdte'
]


# In[ ]:


deg_folder


# In[ ]:


# =====================================================================================
# LOAD AND PARSE FILES
# =====================================================================================

all_files = glob.glob(os.path.join(deg_folder, '*.csv'))
print(f'Found {len(all_files)} degradation baseline files')

records = []

for f in all_files:
    stem = Path(f).stem
    # expected: Mid_Case_Si_p1__degbin_01__deg_5.2
    parts = stem.split('__')

    if len(parts) < 3:
        print(f"Skipping unexpected filename format: {stem}")
        continue

    main = parts[0]
    degbin = parts[1].replace('degbin_', '')
    degrate = parts[2].replace('deg_', '')

    main_parts = main.split('_')
    if len(main_parts) < 3:
        print(f"Skipping badly formatted main filename: {stem}")
        continue

    pca = main_parts[-1]
    tech = main_parts[-2]
    scenario = '_'.join(main_parts[:-2])

    records.append({
        'filepath': f,
        'filename': os.path.basename(f),
        'scenario': scenario,
        'tech': tech,
        'PCA': pca,
        'degbin': degbin,
        'deg': degrate
    })

files_df = pd.DataFrame(records)

print(files_df.head())
print("\nScenarios found:", sorted(files_df['scenario'].unique()))
print("Techs found:", sorted(files_df['tech'].unique()))
print("Degbins found:", sorted(files_df['degbin'].unique()))

# keep only target scenario
files_df = files_df[files_df['scenario'] == scenario_keep].copy()
print(f"\nFiles kept for scenario {scenario_keep}: {len(files_df)}")


# In[ ]:


# =====================================================================================
# SANITY CHECKS
# =====================================================================================

if files_df.empty:
    raise ValueError(f"No files found for scenario {scenario_keep}")

missing_gis = sorted(set(files_df['PCA']) - set(GIS.index))
print(f"PCAs missing from GIS: {len(missing_gis)}")
if len(missing_gis) > 0:
    print("Sample missing GIS PCAs:", missing_gis[:20])

summary_counts = files_df.groupby(['tech', 'degbin'])['PCA'].nunique().unstack(fill_value=0)
print("\nPCA count per tech/bin:")
print(summary_counts)

degbins = sorted(files_df['degbin'].dropna().unique())


# In[ ]:


# =====================================================================================
# RUN PV ICE BY DEGBIN
# =====================================================================================

for degbin in degbins:
    print(f"\n==============================")
    print(f"Running degradation bin {degbin}")
    print(f"==============================")

    sub_si = files_df[(files_df['tech'] == 'Si') & (files_df['degbin'] == degbin)].copy()
    sub_cdte = files_df[(files_df['tech'] == 'CdTe') & (files_df['degbin'] == degbin)].copy()

    PCAs_Si = sorted(sub_si['PCA'].unique())
    PCAs_CdTe = sorted(sub_cdte['PCA'].unique())
    PCAs = sorted(set(PCAs_Si) & set(PCAs_CdTe) & set(GIS.index))

    print(f"Shared PCAs with GIS for degbin {degbin}: {len(PCAs)}")

    if len(PCAs) == 0:
        print(f"No usable PCAs for degbin {degbin}, skipping")
        continue

    # -----------------------------
    # Build r1 = Si
    # -----------------------------
    r1 = PV_ICE.Simulation(name=f'{scenario_keep}_Si_degbin_{degbin}', path=testfolder)

    for pca in PCAs:
        filetitle = sub_si.loc[sub_si['PCA'] == pca, 'filepath'].iloc[0]

        r1.createScenario(
            name=pca,
            massmodulefile=filetitle,
            energymodulefile=energy_file_Si
        )
        r1.scenario[pca].addMaterials(materials_Si)
        r1.scenario[pca].latitude = GIS.loc[pca].lat
        r1.scenario[pca].longitude = GIS.loc[pca].long

    r1.trim_Years(startYear=2010, endYear=2050)

    # -----------------------------
    # Build r2 = CdTe
    # -----------------------------
    r2 = PV_ICE.Simulation(name=f'{scenario_keep}_CdTe_degbin_{degbin}', path=testfolder)

    for pca in PCAs:
        filetitle = sub_cdte.loc[sub_cdte['PCA'] == pca, 'filepath'].iloc[0]

        r2.createScenario(
            name=pca,
            massmodulefile=filetitle,
            energymodulefile=energy_file_CdTe
        )
        r2.scenario[pca].addMaterials(materials_CdTe)
        r2.scenario[pca].latitude = GIS.loc[pca].lat
        r2.scenario[pca].longitude = GIS.loc[pca].long

    r2.trim_Years(startYear=2010, endYear=2050)

    # -----------------------------
    # Run your normal workflow
    # -----------------------------
    if PERFECTMFG:
        r1.scenMod_PerfectManufacturing()
        r2.scenMod_PerfectManufacturing()
        title_Method = 'PVICE_PerfectMFG'
    else:
        title_Method = 'PVICE'

    r1.calculateMassFlow()
    r2.calculateMassFlow()

    r1.aggregateResults()
    r2.aggregateResults()

    datay = r1.USyearly
    datac = r1.UScum

    datay_CdTe = r2.USyearly
    datac_CdTe = r2.UScum

    # -----------------------------
    # Save yearly WasteEOL by degbin
    # -----------------------------
    filter_colc = [col for col in datay.columns if col.startswith('WasteEOL')]
    out_si = os.path.join(
        results_folder,
        f'PVICE_PCA_Si_WasteEOL_{projectionmethod}_degbin_{degbin}.csv'
    )
    datay[filter_colc].to_csv(out_si)

    filter_colc = [col for col in datay_CdTe.columns if col.startswith('WasteEOL')]
    out_cdte = os.path.join(
        results_folder,
        f'PVICE_PCA_CdTe_WasteEOL_{projectionmethod}_degbin_{degbin}.csv'
    )
    datay_CdTe[filter_colc].to_csv(out_cdte)

    # optional: cumulative too
    filter_colc = [col for col in datac.columns if col.startswith('WasteEOL')]
    out_si_cum = os.path.join(
        results_folder,
        f'PVICE_PCA_Si_WasteEOLcum_{projectionmethod}_degbin_{degbin}.csv'
    )
    datac[filter_colc].to_csv(out_si_cum)

    filter_colc = [col for col in datac_CdTe.columns if col.startswith('WasteEOL')]
    out_cdte_cum = os.path.join(
        results_folder,
        f'PVICE_PCA_CdTe_WasteEOLcum_{projectionmethod}_degbin_{degbin}.csv'
    )
    datac_CdTe[filter_colc].to_csv(out_cdte_cum)

    print(f"Finished degbin {degbin}")

print("\nFinished all degradation-bin simulations.")



# In[ ]:


# =====================================================================================
# SUM ALL DEGBINS AFTERWARD
# =====================================================================================

def sum_csvs(file_list):
    if len(file_list) == 0:
        return None

    dfs = [pd.read_csv(f, index_col=0) for f in file_list]
    total = dfs[0].copy()

    for df in dfs[1:]:
        total = total.add(df, fill_value=0)

    return total

# yearly Si
si_yearly_files = sorted(glob.glob(
    os.path.join(results_folder, f'PVICE_PCA_Si_WasteEOL_{projectionmethod}_degbin_*.csv')
))
Si_total_yearly = sum_csvs(si_yearly_files)
if Si_total_yearly is not None:
    Si_total_yearly.to_csv(
        os.path.join(results_folder, f'PVICE_PCA_Si_WasteEOL_{projectionmethod}_ALLDEGBINS.csv')
    )
    print(f"Saved total yearly Si waste from {len(si_yearly_files)} degbins")

# yearly CdTe
cdte_yearly_files = sorted(glob.glob(
    os.path.join(results_folder, f'PVICE_PCA_CdTe_WasteEOL_{projectionmethod}_degbin_*.csv')
))
CdTe_total_yearly = sum_csvs(cdte_yearly_files)
if CdTe_total_yearly is not None:
    CdTe_total_yearly.to_csv(
        os.path.join(results_folder, f'PVICE_PCA_CdTe_WasteEOL_{projectionmethod}_ALLDEGBINS.csv')
    )
    print(f"Saved total yearly CdTe waste from {len(cdte_yearly_files)} degbins")

# cumulative Si
si_cum_files = sorted(glob.glob(
    os.path.join(results_folder, f'PVICE_PCA_Si_WasteEOLcum_{projectionmethod}_degbin_*.csv')
))
Si_total_cum = sum_csvs(si_cum_files)
if Si_total_cum is not None:
    Si_total_cum.to_csv(
        os.path.join(results_folder, f'PVICE_PCA_Si_WasteEOLcum_{projectionmethod}_ALLDEGBINS.csv')
    )
    print(f"Saved total cumulative Si waste from {len(si_cum_files)} degbins")

# cumulative CdTe
cdte_cum_files = sorted(glob.glob(
    os.path.join(results_folder, f'PVICE_PCA_CdTe_WasteEOLcum_{projectionmethod}_degbin_*.csv')
))
CdTe_total_cum = sum_csvs(cdte_cum_files)
if CdTe_total_cum is not None:
    CdTe_total_cum.to_csv(
        os.path.join(results_folder, f'PVICE_PCA_CdTe_WasteEOLcum_{projectionmethod}_ALLDEGBINS.csv')
    )
    print(f"Saved total cumulative CdTe waste from {len(cdte_cum_files)} degbins")



# In[ ]:


# =====================================================================================
# OPTIONAL: COMBINE SI + CDTE TOTALS
# =====================================================================================

if (Si_total_yearly is not None) and (CdTe_total_yearly is not None):
    Total_yearly_alltech = Si_total_yearly.add(CdTe_total_yearly, fill_value=0)
    Total_yearly_alltech.to_csv(
        os.path.join(results_folder, f'PVICE_PCA_ALLTECH_WasteEOL_{projectionmethod}_ALLDEGBINS.csv')
    )
    print("Saved total yearly waste across Si + CdTe")

if (Si_total_cum is not None) and (CdTe_total_cum is not None):
    Total_cum_alltech = Si_total_cum.add(CdTe_total_cum, fill_value=0)
    Total_cum_alltech.to_csv(
        os.path.join(results_folder, f'PVICE_PCA_ALLTECH_WasteEOLcum_{projectionmethod}_ALLDEGBINS.csv')
    )
    print("Saved total cumulative waste across Si + CdTe")


# In[ ]:


import os
import re
import pandas as pd

infile = os.path.join(results_folder, f'PVICE_PCA_ALLTECH_WasteEOL_{projectionmethod}_ALLDEGBINS.csv')
outfile = os.path.join(results_folder, f'PVICE_PCA_ALLTECH_WasteEOL_{projectionmethod}_ByPCA.csv')

df = pd.read_csv(infile)

# keep year separately
year_col = 'year'
value_cols = [c for c in df.columns if c != year_col]

# extract PCA name from each column, like p1, p27, p134
pca_map = {}
for col in value_cols:
    m = re.search(r'_(p\d+)_\[Tonnes\]$', col)
    if m:
        pca_map[col] = m.group(1)

# keep only columns where a PCA was found
valid_cols = list(pca_map.keys())

# rename columns to just the PCA name, then sum duplicate PCA columns
df_pca = df[[year_col] + valid_cols].copy()
df_pca = df_pca.rename(columns=pca_map)

# sum all columns with the same PCA label
df_pca = df_pca.groupby(axis=1, level=0).sum()

# groupby may move year into the sort, so put it first if needed
if year_col in df_pca.columns:
    cols = [year_col] + [c for c in df_pca.columns if c != year_col]
    df_pca = df_pca[cols]
else:
    df_pca.insert(0, year_col, df[year_col].values)

df_pca.to_csv(outfile, index=False)

print("Saved:", outfile)
print(df_pca.head())


# In[ ]:


a=2


# # SECOND PART SAVE

# In[14]:


import os
import re
import glob
import pandas as pd
from pathlib import Path

# =========================================================
# PATHS
# =========================================================

testfolder = os.path.join(os.getcwd(), 'TEMP')
print("Your simulation will be stored in %s" % testfolder)

results_folder = os.path.join(testfolder, 'results_fleetdeg')
print("Reading PV ICE result files from %s" % results_folder)

projectionmethod = 'Method2_Hybrid'

# =========================================================
# HELPERS
# =========================================================

def parse_result_filename(filepath):
    """
    Example filename:
    PVICE_PCA_CdTe_WasteEOL_Method2_Hybrid_degbin_01.csv
    """
    base = os.path.basename(filepath).replace('.csv', '')
    m = re.match(
        r'^PVICE_PCA_(?P<tech>Si|CdTe)_WasteEOL_(?P<proj>.+)_degbin_(?P<bin>\d+)$',
        base
    )
    if not m:
        return None
    return m.groupdict()

def collapse_one_file_to_pca_material(infile):
    """
    Convert columns like:
      WasteEOL_glass_Mid_Case_CdTe_degbin_01_p1_[Tonnes]
      WasteEOL_silver_Mid_Case_Si_degbin_02_p7_[Tonnes]
      WasteEOL_Module_Mid_Case_CdTe_degbin_01_p1_[Tonnes]

    into:
      p1_glass
      p7_silver
      p1_Module

    summing duplicate columns if needed.
    """
    meta = parse_result_filename(infile)
    if meta is None:
        print(f"Skipping bad filename: {os.path.basename(infile)}")
        return None

    tech = meta['tech']
    degbin = meta['bin']

    df = pd.read_csv(infile)

    if 'year' not in df.columns:
        print(f"Skipping {os.path.basename(infile)}: no year column")
        return None

    year = df['year'].copy()
    value_cols = [c for c in df.columns if c != 'year']

    rename_map = {}
    unmatched = []

    for col in value_cols:
        # Find PCA at the end
        m_pca = re.search(r'_(p\d+)_\[Tonnes\]$', col)
        if not m_pca:
            unmatched.append(col)
            continue

        pca = m_pca.group(1)

        # Remove the ending _pXX_[Tonnes]
        left = re.sub(r'_(p\d+)_\[Tonnes\]$', '', col)

        # Remove the leading WasteEOL_
        left = re.sub(r'^WasteEOL_', '', left)

        # Remove the scenario/tech/degbin tail, leaving only the material/component part
        # Example:
        #   glass_Mid_Case_CdTe_degbin_01   -> glass
        #   Module_Mid_Case_CdTe_degbin_01  -> Module
        #   aluminium_frames_cdte_Mid_Case_CdTe_degbin_01 -> aluminium_frames_cdte
        tail_pattern = rf'_(.+)?'  # dummy placeholder, overwritten below
        m_tail = re.match(rf'^(?P<material>.+)_.+_{re.escape(tech)}_degbin_{re.escape(degbin)}$', left)

        if not m_tail:
            # More robust fallback: split at _{tech}_degbin_{bin}
            split_token = f'_{tech}_degbin_{degbin}'
            if split_token not in left:
                unmatched.append(col)
                continue
            material = left.split(split_token)[0]
            # remove trailing scenario chunk by taking text before last "_<scenario>"
            # safest fallback: keep as-is if we can't isolate better
            rename_map[col] = f"{pca}_{material}"
            continue

        material = m_tail.group('material')

        # material still includes scenario before tech; remove scenario by taking the part
        # before the LAST occurrence of "_<something>"? No — safer approach:
        # use filename-independent regex from the right: material is everything before
        # the scenario block. Since scenario can have underscores, remove the longest suffix
        # that starts with "_" and contains "_{tech}_degbin_{bin}".
        split_token = f'_{tech}_degbin_{degbin}'
        material = left.split(split_token)[0]

        # Now material looks like "glass_Mid_Case" or "Module_Mid_Case"
        # Remove scenario by chopping off the final "_<scenario words>" chunk using the fact
        # that material names are the prefix before "_Mid_Case" in your files.
        # General rule: PCA/material is the first token family after WasteEOL_.
        # So for common PV ICE waste columns, take everything before the scenario suffix
        # by removing the last two underscore-separated words only if they match Mid_Case.
        if material.endswith('_Mid_Case'):
            material = material[:-len('_Mid_Case')]

        rename_map[col] = f"{pca}_{material}"

    if len(rename_map) == 0:
        print(f"Skipping {os.path.basename(infile)}: no columns matched")
        if unmatched:
            print("Sample unmatched columns:", unmatched[:5])
        return None

    df2 = df[list(rename_map.keys())].copy()
    df2 = df2.rename(columns=rename_map)

    # Sum duplicate pca_material columns
    df_pm = df2.T.groupby(level=0).sum().T
    df_pm.insert(0, 'year', year.values)

    outfile = infile.replace('.csv', '_ByPCAMaterial.csv')
    df_pm.to_csv(outfile, index=False)
    print(f"Saved: {os.path.basename(outfile)}")

    return outfile

def sum_bypcamaterial_files(file_list, outfile):
    if len(file_list) == 0:
        print(f"No files found for {os.path.basename(outfile)}")
        return None

    dfs = [pd.read_csv(f) for f in file_list]

    total = dfs[0].copy()
    for df in dfs[1:]:
        total.iloc[:, 1:] = total.iloc[:, 1:].add(df.iloc[:, 1:], fill_value=0)

    total.to_csv(outfile, index=False)
    print(f"Saved: {os.path.basename(outfile)}")
    return total

# =========================================================
# STEP 1: CONVERT EACH RAW DEGBIN FILE -> ByPCAMaterial
# =========================================================

raw_files = glob.glob(os.path.join(results_folder, f'PVICE_PCA_*_WasteEOL_{projectionmethod}_degbin_*.csv'))

raw_files = [
    f for f in raw_files
    if '_ByPCAMaterial' not in os.path.basename(f)
    and '_ByPCA' not in os.path.basename(f)
    and '_ALLDEGBINS' not in os.path.basename(f)
]

print(f"Found {len(raw_files)} raw degbin files")

created_files = []
for infile in raw_files:
    out = collapse_one_file_to_pca_material(infile)
    if out is not None:
        created_files.append(out)

print(f"Created {len(created_files)} ByPCAMaterial files")

# =========================================================
# STEP 2: SUM ALL DEGBINS FOR CDTE, KEEPING PCA_MATERIAL
# =========================================================

cdte_files = sorted(glob.glob(
    os.path.join(results_folder, f'PVICE_PCA_CdTe_WasteEOL_{projectionmethod}_degbin_*_ByPCAMaterial.csv')
))

out_cdte = os.path.join(
    results_folder,
    f'PVICE_PCA_CdTe_WasteEOL_{projectionmethod}_ALLDEGBINS_ByPCAMaterial.csv'
)

CdTe_total = sum_bypcamaterial_files(cdte_files, out_cdte)

# =========================================================
# STEP 3: SUM ALL DEGBINS FOR SI, KEEPING PCA_MATERIAL
# =========================================================

si_files = sorted(glob.glob(
    os.path.join(results_folder, f'PVICE_PCA_Si_WasteEOL_{projectionmethod}_degbin_*_ByPCAMaterial.csv')
))

out_si = os.path.join(
    results_folder,
    f'PVICE_PCA_Si_WasteEOL_{projectionmethod}_ALLDEGBINS_ByPCAMaterial.csv'
)

Si_total = sum_bypcamaterial_files(si_files, out_si)

# =========================================================
# STEP 4: OPTIONAL ALLTECH SUM, STILL KEEPING PCA_MATERIAL
# =========================================================

if (Si_total is not None) and (CdTe_total is not None):
    AllTech_total = Si_total.copy()
    AllTech_total.iloc[:, 1:] = Si_total.iloc[:, 1:].add(CdTe_total.iloc[:, 1:], fill_value=0)

    out_alltech = os.path.join(
        results_folder,
        f'PVICE_PCA_ALLTECH_WasteEOL_{projectionmethod}_ALLDEGBINS_ByPCAMaterial.csv'
    )
    AllTech_total.to_csv(out_alltech, index=False)
    print(f"Saved: {os.path.basename(out_alltech)}")

# =========================================================
# STEP 5: QUICK CHECK
# =========================================================

check_file = os.path.join(
    results_folder,
    f'PVICE_PCA_CdTe_WasteEOL_{projectionmethod}_ALLDEGBINS_ByPCAMaterial.csv'
)

if os.path.exists(check_file):
    df_check = pd.read_csv(check_file)
    print(df_check.columns[:20].tolist())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




