#!/usr/bin/env python
# coding: utf-8

# # MassFlows Calculations

# ## 1. Initial setup

# In[1]:


import PV_ICE
import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
from pathlib import Path


# In[2]:


testfolder = os.path.join(os.getcwd(), 'TEMP')
print ("Your simulation will be stored in %s" % testfolder)


# In[3]:


baselinesFolder = Path().resolve().parent.parent.parent / 'PV_ICE' / 'PV_ICE' /'baselines'
baselinesFolder


# ### Reading GIS inputs

# In[4]:


from geopy.geocoders import Nominatim
from geopy.point import Point
# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")


# In[5]:


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

# In[6]:


projectionmethod = 'Method2_Hybrid'


# ### Scenario creation

# In[ ]:


# All of this to get the Old File PCAs
reedsFile = os.path.join(baselinesFolder, 'SupportingMaterial','December Core Scenarios ReEDS Outputs Solar Futures v3a.xlsx')
print ("Input file is stored in %s" % reedsFile)
REEDSInput = pd.read_excel(reedsFile, sheet_name="new installs PV")
rawdf = REEDSInput.copy()
rawdf.drop(columns=['State'], inplace=True)
rawdf.drop(columns=['Tech'], inplace=True) #tech=pvtotal from "new installs PV sheet", so can drop
rawdf.set_index(['Scenario','Year','PCA'], inplace=True)
PCAs = list(rawdf.unstack(level=2).iloc[0].unstack(level=0).index.unique())


# In[ ]:


# Getting New file PCAs


# In[ ]:


import os
import glob

merged_folder = os.path.join(testfolder, 'PCAs_Method2_Hybrid')

all_files = glob.glob(os.path.join(merged_folder, '*.csv'))

print(f"Found {len(all_files)} csv files")

pcas_from_files = set()

for f in all_files:
    base = os.path.basename(f).replace('.csv', '')
    parts = base.split('_')
    # expected pattern: MidCase_Si_p1  or MidCase_CdTe_p1
    pca = parts[-1]
    pcas_from_files.add(pca)

PCAs_final = sorted(pcas_from_files)

print(f"Final PCA count: {len(PCAs_final)}")
print(PCAs_final[:20])

PCAs = PCAs_final


# In[ ]:





# In[33]:


SFscenarios = ['Mid_Case_Si','Mid_Case_CdTe']


# In[9]:


i = 0
r1 = PV_ICE.Simulation(name=SFscenarios[i], path=testfolder)


# In[10]:


jj=0


# In[17]:





# In[19]:


filetitle = SFscenarios[i]+'_'+PCAs[jj]+'.csv'
filetitle = os.path.join(testfolder, f'PCAs_{projectionmethod}', filetitle)    # Change this number to the simulation you want to run
r1.createScenario(name=PCAs[jj], massmodulefile=filetitle)
r1.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant', 'backsheet'], )
r1.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
r1.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long


# In[35]:


#for ii in range (0, 1): #len(scenarios):
i = 0
r1 = PV_ICE.Simulation(name=SFscenarios[i], path=testfolder)

for jj in range (0, len(PCAs)): 
    filetitle = SFscenarios[i]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, f'PCAs_{projectionmethod}', filetitle)    # Change this number to the simulation you want to run
    r1.createScenario(name=PCAs[jj], massmodulefile=filetitle, energymodulefile='baseline_modules_energy_Si.csv')
    r1.scenario[PCAs[jj]].addMaterials(['glass', 'silicon', 'silver', 'copper', 'aluminium_frames', 'encapsulant', 'backsheet'])
    r1.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r1.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long

r1.trim_Years(startYear=2010, endYear=2050)


# In[36]:


i = 1
r2 = PV_ICE.Simulation(name=SFscenarios[i], path=testfolder)

for jj in range (0, len(PCAs)): 
    filetitle = SFscenarios[i]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, f'PCAs_{projectionmethod}', filetitle)        
    r2.createScenario(name=PCAs[jj], massmodulefile=filetitle, energymodulefile='baseline_modules_energy_CdTe.csv')
    r2.scenario[PCAs[jj]].addMaterials(['cadmium', 'tellurium', 'glass_cdte', 'aluminium_frames_cdte', 'encapsulant_cdte', 'copper_cdte'])
    r2.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r2.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long

r2.trim_Years(startYear=2010, endYear=2050)


# ### Set characteristics for Manufacturing 
# IF only EoL needed, set manufacturing waste to 0 by running PercetManufacturing() modifying scenario function

# In[37]:


PERFECTMFG = True
# Set to false if I want to see how much goes to mnf waste
if PERFECTMFG:
    r1.scenMod_PerfectManufacturing()
    r2.scenMod_PerfectManufacturing()
    title_Method = 'PVICE_PerfectMFG'
else:
    title_Method = 'PVICE'


# ## 3. Calculate Mass Flow

# In[38]:


r1.calculateMassFlow()


# In[39]:


r2.calculateMassFlow()


# In[41]:


print("PCAs:", r1.scenario.keys())
print("Module Keys:", r1.scenario[PCAs[jj]].dataIn_m.keys())
print("Material Keys: ", r1.scenario[PCAs[jj]].material['glass'].matdataIn_m.keys())


# In[18]:


"""
r1.plotScenariosComparison(keyword='Cumulative_Area_disposedby_Failure')
r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_Total_Landfilled')
r1.scenario['p1'].dataIn_m.head(21)
r2.scenario['p1'].dataIn_m.head(21)
r3.scenario['p1'].dataIn_m.head(21)
"""
pass


# ## 4. Aggregate & Save Data

# In[ ]:


r1.aggregateResults()
r2.aggregateResults()


# In[20]:


datay = r1.USyearly
datac = r1.UScum


# In[21]:


datay_CdTe = r2.USyearly
datac_CdTe = r2.UScum


# ### Get the EOL waste

# In[22]:


filter_colc = [col for col in datay if col.startswith('WasteEOL')]
datay[filter_colc].to_csv(f'PVICE_PCA_cSi_WasteEOL_{projectionmethod}.csv')
filter_colc = [col for col in datay_CdTe if col.startswith('WasteEOL')]
datay_CdTe[filter_colc].to_csv(f'PVICE_PCA_CdTe_WasteEOL_{projectionmethod}.csv')


# ### Get the Virgin materials

# In[23]:


filter_colc = [col for col in datay if col.startswith('VirginStock')]
datay[filter_colc].to_csv(f'PVICE_PCA_cSi_VirginStock_{projectionmethod}.csv')
filter_colc = [col for col in datay_CdTe if col.startswith('VirginStock')]
datay_CdTe[filter_colc].to_csv(f'PVICE_PCA_CdTe_VirginStock_{projectionmethod}.csv')


# In[30]:


filter_colc = [col for col in datay if col.startswith('WasteEOL_Module')]
foo = datay[filter_colc]
filter_colc = [col for col in datay_CdTe if col.startswith('WasteEOL_Module')]
foo_CdTe = datay_CdTe[filter_colc]


# In[31]:


foo.keys()


# In[33]:


import re


# In[34]:


foo.columns = [re.search(r'p\d+', col).group(0) if re.search(r'p\d+', col) else col for col in foo.columns]


# In[36]:


foo_CdTe.columns = [re.search(r'p\d+', col).group(0) if re.search(r'p\d+', col) else col for col in foo_CdTe.columns]


# In[38]:


foo_total = foo + foo_CdTe


# In[44]:


foo_flipped = foo_total.T


# In[45]:


foo_selected = foo_flipped[[2025, 2030, 2035]]


# In[46]:


foo_selected


# In[48]:


merged = foo_selected.merge(GIS[['lat', 'long']], left_index=True, right_index=True, how='left')


# In[50]:


merged.to_csv('Kepler_WasteEoL.csv')


# In[71]:


import pandas as pd
import numpy as np
import re

# ===== 0) Inputs =====
gid_df = merged.copy()                 # <- your GID table with 'lat' and 'long'
gid_df.columns = gid_df.columns.map(str)

recyclers = pd.read_csv(
    r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\SEIA Recycling Centers 07Oct2025.csv"
)
recyclers.columns = recyclers.columns.map(lambda x: str(x).strip())

# ===== 1) Helpers =====
def pick_col(df, candidates):
    cols_map = {c.strip().lower(): c for c in df.columns}
    for cand in candidates:
        key = cand.strip().lower()
        if key in cols_map:
            return cols_map[key]
    raise KeyError(f"None of {candidates} found. Available: {list(df.columns)}")

def clean_num_series(s: pd.Series) -> pd.Series:
    s = s.astype(str)
    s = s.str.replace(r'[\u2212\u2012\u2013\u2014]', '-', regex=True)   # unicode minus/dashes -> '-'
    s = s.str.replace(r'[°\sNSEWnsew]', '', regex=True)                # drop degree & NSEW letters
    s = s.str.replace(',', '', regex=False)                            # remove commas
    s = s.str.replace(r'[^0-9.\-+]', '', regex=True)                   # keep only digits . + -
    return pd.to_numeric(s, errors='coerce')

# ===== 2) Select/clean columns =====
# GIDs
gid_lat = pick_col(gid_df, ['lat','latitude','Lat','Latitude'])
gid_lon = pick_col(gid_df, ['long','lon','longitude','Long','Lon','Longitude'])
gids = gid_df[[gid_lat, gid_lon]].copy()
gids[gid_lat] = pd.to_numeric(gids[gid_lat], errors='coerce')
gids[gid_lon] = pd.to_numeric(gids[gid_lon], errors='coerce')
gids = gids.dropna(subset=[gid_lat, gid_lon])

# Recyclers
rec_id   = pick_col(recyclers, ['RID','rID','rid'])
rec_city = pick_col(recyclers, ['Region / Nearby City','Region/Nearby City','City','Region'])
rec_lat  = pick_col(recyclers, ['Latitude','latitude','Lat','lat'])
rec_lon  = pick_col(recyclers, ['Longitude','longitude','Long','long','Lon','lon'])

recyclers = recyclers[[rec_id, rec_city, rec_lat, rec_lon]].copy()
recyclers[rec_lat] = clean_num_series(recyclers[rec_lat])
recyclers[rec_lon] = clean_num_series(recyclers[rec_lon])
recyclers = recyclers.dropna(subset=[rec_lat, rec_lon]).reset_index(drop=True)

# Safety checks
if len(gids) == 0:
    raise ValueError("No valid GID coordinates after coercion. Check gid_df lat/long.")
if len(recyclers) == 0:
    raise ValueError("No valid recycler coordinates after coercion. Check recycler Latitude/Longitude.")

# ===== 3) Haversine & nearest =====
R = 6371.0088  # km

g = np.radians(gids[[gid_lat, gid_lon]].to_numpy())          # (N,2)
r = np.radians(recyclers[[rec_lat, rec_lon]].to_numpy())     # (M,2)

lat1, lon1 = g[:, [0]], g[:, [1]]
lat2, lon2 = r[:, 0][None, :], r[:, 1][None, :]

dlat, dlon = lat2 - lat1, lon2 - lon1
a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
dist_km = R * c  # (N,M)

nearest_idx  = dist_km.argmin(axis=1)
nearest_dist = dist_km[np.arange(dist_km.shape[0]), nearest_idx]
nearest_rows = recyclers.iloc[nearest_idx].reset_index(drop=True)

# Format RID as r#
nearest_ids = nearest_rows[rec_id].astype(str).str.replace(r'\.0$', '', regex=True)
nearest_ids = nearest_ids.apply(lambda x: f"r{x}" if not str(x).lower().startswith('r') else x)

# ===== 4) Output =====
out = gids.copy()
out.columns = ['lat','long']  # standardize
out['nearest_RID']   = nearest_ids.to_numpy()
out['nearest_city']  = nearest_rows[rec_city].to_numpy()
out['recycler_lat']  = nearest_rows[rec_lat].to_numpy()
out['recycler_lon']  = nearest_rows[rec_lon].to_numpy()
out['distance_km']   = nearest_dist

print(f"Assigned {len(out)} GIDs to {recyclers[rec_id].nunique()} recyclers.")
print(out.head())
out.to_csv("gid_nearest_recycler.csv")


# # KEPLER

# In[72]:


import pandas as pd

# File paths
path = r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP"
gid_recycler = pd.read_csv(f"{path}\\gid_nearest_recycler.csv")
gid_waste = pd.read_csv(f"{path}\\Kepler_WasteEoL.csv")

# Merge on GID (index column)
merged = gid_recycler.merge(gid_waste, on=['lat', 'long'], how='left')

# Save merged file for Kepler
merged.to_csv(f"{path}\\Kepler_GID_Recyclers_Merged.csv", index=False)
print("✅ File saved for Kepler.gl")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[56]:


out


# In[65]:


import pandas as pd
import numpy as np

# ------------------ Load Data ------------------
# Force all column names to strings (fixes your error)
gid_df = merged.copy()
gid_df.columns = gid_df.columns.map(str)

recyclers = pd.read_csv(
    r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\SEIA Recycling Centers 07Oct2025.csv"
).rename(columns=str.strip)

# ------------------ Identify Columns ------------------
# Find which ones exist
print("GID columns:", gid_df.columns.tolist())
print("Recycler columns:", recyclers.columns.tolist())

# Adjust to your actual column names
gid_lat, gid_lon = 'lat', 'long'  # columns in your merged dataframe
rec_id, rec_city, rec_lat, rec_lon = 'RID', 'Region / Nearby City', 'Latitude', 'Longitude'

# ------------------ Clean Data ------------------
# Drop NaNs and ensure numeric
gids = gid_df[[gid_lat, gid_lon]].apply(pd.to_numeric, errors='coerce').dropna().copy()
recyclers = recyclers[[rec_id, rec_city, rec_lat, rec_lon]].copy()
recyclers[[rec_lat, rec_lon]] = recyclers[[rec_lat, rec_lon]].apply(pd.to_numeric, errors='coerce')
recyclers = recyclers.dropna(subset=[rec_lat, rec_lon]).reset_index(drop=True)

# ------------------ Compute Distances ------------------
R = 6371.0088  # km
g = np.radians(gids[[gid_lat, gid_lon]].to_numpy())           # (N,2)
r = np.radians(recyclers[[rec_lat, rec_lon]].to_numpy())      # (M,2)

lat1, lon1 = g[:, [0]], g[:, [1]]
lat2, lon2 = r[:, 0][None, :], r[:, 1][None, :]
dlat, dlon = lat2 - lat1, lon2 - lon1

a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
dist_km = R * c

# --- Match Nearest ---
nearest_idx = dist_km.argmin(axis=1)
nearest_dist = dist_km[np.arange(dist_km.shape[0]), nearest_idx]
nearest = recyclers.iloc[nearest_idx].reset_index(drop=True)

# 🧠 Fix RID formatting (e.g., 1.0 → r1)
nearest_ids = nearest['RID'].astype(str).str.replace(r'\.0$', '', regex=True)  # remove .0
nearest_ids = nearest_ids.apply(lambda x: f"r{x}" if not x.startswith("r") else x)

out = gids.copy()
out['nearest_RID']   = nearest_ids.to_numpy()
out['nearest_city']  = nearest['Region / Nearby City'].to_numpy()
out['recycler_lat']  = nearest['Latitude'].to_numpy()
out['recycler_lon']  = nearest['Longitude'].to_numpy()
out['distance_km']   = nearest_dist

print(out.head())
# out.to_csv('gid_nearest_recycler.csv', index=True)


# In[66]:


import pandas as pd
import numpy as np

# ------------------ Load & normalize ------------------
gid_df = merged.copy()
gid_df.columns = gid_df.columns.map(str)   # ensure string headers

recyclers = pd.read_csv(
    r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\SEIA Recycling Centers 07Oct2025.csv"
)
recyclers.columns = recyclers.columns.map(lambda x: str(x).strip())

# ------------------ Column selection ------------------
# GIDs: you said it's lat + long (not lon)
gid_lat, gid_lon = None, None
for cand in ['lat','Lat','latitude','Latitude']:
    if cand in gid_df.columns: gid_lat = cand; break
for cand in ['long','Long','lon','Lon','longitude','Longitude']:
    if cand in gid_df.columns: gid_lon = cand; break
if gid_lat is None or gid_lon is None:
    raise KeyError(f"Could not find GID lat/long columns in {gid_df.columns.tolist()}")

# Recyclers: your CSV now has cleaned city coords; common headers:
rec_id   = 'RID'  # you confirmed this
# Try a few options for city and lat/lon
rec_city = next((c for c in ['Region / Nearby City','Region/Nearby City','City','Region'] if c in recyclers.columns), None)
rec_lat  = next((c for c in ['Latitude','latitude','Lat','lat'] if c in recyclers.columns), None)
rec_lon  = next((c for c in ['Longitude','longitude','Long','long','Lon','lon'] if c in recyclers.columns), None)
if rec_city is None or rec_lat is None or rec_lon is None:
    raise KeyError(f"Missing recycler columns. Have: {recyclers.columns.tolist()}")

# ------------------ Clean & validate ------------------
gids = gid_df[[gid_lat, gid_lon]].copy()
gids[g_id := gid_lat] = pd.to_numeric(gids[gid_lat], errors='coerce')
gids[g_on := gid_lon] = pd.to_numeric(gids[gid_lon], errors='coerce')
gids = gids.dropna(subset=[gid_lat, gid_lon])

recyclers = recyclers[[rec_id, rec_city, rec_lat, rec_lon]].copy()
recyclers[rec_lat] = pd.to_numeric(recyclers[rec_lat], errors='coerce')
recyclers[rec_lon] = pd.to_numeric(recyclers[rec_lon], errors='coerce')
recyclers = recyclers.dropna(subset=[rec_lat, rec_lon]).reset_index(drop=True)

print(f"GIDs with valid coords: {len(gids)}")
print(f"Recyclers with valid coords: {len(recyclers)}")

if len(gids) == 0:
    raise ValueError("No valid GID coordinates after coercion. Check gid_df lat/long contents.")
if len(recyclers) == 0:
    raise ValueError("No valid recycler coordinates after coercion. Check recycler Latitude/Longitude values.")

# ------------------ Haversine + nearest ------------------
R = 6371.0088  # km
g = np.radians(gids[[gid_lat, gid_lon]].to_numpy())           # (N,2)
r = np.radians(recyclers[[rec_lat, rec_lon]].to_numpy())      # (M,2)

# Sanity (prevents empty sequence argmin)
N, M = g.shape[0], r.shape[0]
if N == 0 or M == 0:
    raise ValueError(f"Empty distance matrix (N={N}, M={M}).")

lat1, lon1 = g[:, [0]], g[:, [1]]
lat2, lon2 = r[:, 0][None, :], r[:, 1][None, :]
dlat, dlon = lat2 - lat1, lon2 - lon1

a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
dist_km = R * c                                               # (N,M)

nearest_idx  = dist_km.argmin(axis=1)                         # (N,)
nearest_dist = dist_km[np.arange(N), nearest_idx]             # (N,)

nearest_rows = recyclers.iloc[nearest_idx].reset_index(drop=True)

# Format RID as r1..r10 even if numeric
nearest_ids = nearest_rows[rec_id].astype(str).str.replace(r'\.0$', '', regex=True)
nearest_ids = nearest_ids.apply(lambda x: f"r{x}" if not x.lower().startswith('r') else x)

# ------------------ Output ------------------
out = gids.copy()
out.columns = ['lat','long']  # standardize
out['nearest_RID']   = nearest_ids.to_numpy()
out['nearest_city']  = nearest_rows[rec_city].to_numpy()
out['recycler_lat']  = nearest_rows[rec_lat].to_numpy()
out['recycler_lon']  = nearest_rows[rec_lon].to_numpy()
out['distance_km']   = nearest_dist

print(out.head())
# out.to_csv("gid_nearest_recycler.csv")


# In[60]:


import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# --- 0) Inputs ---------------------------------------------------------------
# GIDs with lat/lon (index = p1..p150). If you followed earlier steps:
#   merged has columns: ['lat','lon', 2025, 2030, 2035, ...]
gids = merged[['lat', 'long']].copy()

# Recycler centers CSV (your table with rID, city, lat, lon)
recyclers = pd.read_csv(r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\SEIA Recycling Centers 07Oct2025.csv")  # adjust path
recyclers = recyclers.rename(columns=str.strip)

# --- 1) Clean & prepare ------------------------------------------------------
# keep only rows with valid coordinates
gids = gids.dropna(subset=['lat', 'long'])
recyclers = recyclers.dropna(subset=['Latitude', 'Longitude'])

# radians for haversine/BallTree
gids_rad = np.radians(gids[['lat', 'long']].to_numpy())
recyclers_rad = np.radians(recyclers[['Latitude', 'Longitude']].to_numpy())

# --- 2) Build tree & query nearest ------------------------------------------
tree = BallTree(recyclers_rad, metric='haversine')
dist_rad, idx = tree.query(gids_rad, k=1)

# convert arc distance (radians) to km
EARTH_RADIUS_KM = 6371.0088
dist_km = dist_rad.flatten() * EARTH_RADIUS_KM
nearest_idx = idx.flatten()

# --- 3) Assemble result ------------------------------------------------------
nearest = recyclers.iloc[nearest_idx].reset_index(drop=True)
nearest = nearest.rename(columns={
    'rID': 'nearest_rID',
    'Region / Nearby City': 'nearest_city',
    'Latitude': 'recycler_lat',
    'Longitude': 'recycler_lon'
})

out = gids.copy()
out['nearest_rID']   = nearest['nearest_rID'].to_numpy()
out['nearest_city']  = nearest['nearest_city'].to_numpy()
out['recycler_lat']  = nearest['recycler_lat'].to_numpy()
out['recycler_lon']  = nearest['recycler_lon'].to_numpy()
out['distance_km']   = dist_km

# optional: keep the original year columns, etc.
# out = out.join(merged[[2025, 2030, 2035]])

# sanity check
print(out.head())


# In[ ]:




