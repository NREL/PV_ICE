#!/usr/bin/env python
# coding: utf-8

# # REEDs PCA Baselines for Si & CdTe

# ReEDS installation projections from the Solar Futures Study, published by DOE on 2021.
# 
# Scenario Interest: 
# o	95-by-35+Elec.Adv+DR ,  a.k.a. "Solar Futures Decarbonization + Electrification scenario"
# 
# This code performs three Methods to output files for the Mass Flows:
# <ol>
#     <li> PCA original data by ReEDS </li>
#     <li> PCA data reordered based on ascending production up to 2035, and then descending, </li>
#     <li> PCA data calculated with an exponencial that mathces the cumulative 2035 and 2050 targets </li>
# </ol>

# In[1]:


import PV_ICE
import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
import csv
import platform
from pathlib import Path

plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[2]:


# This information helps with debugging and getting support :)
print("Working on a ", platform.system(), platform.release())
print("Python version ", sys.version)
print("Pandas version ", pd.__version__)
print("PV_ICE version ", PV_ICE.__version__)


# In[3]:


# =========================================================
# PATHS
# =========================================================

testfolder = os.path.join(os.getcwd(), 'TEMP')
print("Your simulation will be stored in %s" % testfolder)

baselinesFolder = Path().resolve().parent.parent.parent / 'PV_ICE' / 'PV_ICE' / 'baselines'
print("Baselines Folder"), baselinesFolder

newReedsFile = 'processed_cap_ivrt_upv.csv'
print("Input file is stored in %s" % newReedsFile)

# output folder
subtestfolder = os.path.join(testfolder, 'PCAs_Metho3_5yr')
os.makedirs(subtestfolder, exist_ok=True)


# In[4]:


# =========================================================
# LOAD FILE
# =========================================================

df_new = pd.read_csv(newReedsFile)
df_new.columns = df_new.columns.str.strip()

print("Columns:")
print(df_new.columns.tolist())

print("\nUnique scenario(s):")
print(df_new['Scenario'].unique())

print("\nUnique tech(s):")
print(df_new['Tech'].unique())


# In[5]:


# =========================================================
# CLEAN TO STANDARD FORMAT
# =========================================================

REEDSInput_new = df_new[['PCA', 'Year', 'Capacity (GW)', 'State']].copy()
REEDSInput_new = REEDSInput_new.rename(columns={
    'PCA': 'r',
    'Year': 'year',
    'Capacity (GW)': 'cap_gw',
    'State': 'state'
})

REEDSInput_new['year'] = pd.to_numeric(REEDSInput_new['year'], errors='coerce')
REEDSInput_new['cap_gw'] = pd.to_numeric(REEDSInput_new['cap_gw'], errors='coerce')

REEDSInput_new = REEDSInput_new.dropna(subset=['r', 'year', 'cap_gw']).copy()
REEDSInput_new['year'] = REEDSInput_new['year'].astype(int)

print("\nCleaned input:")
print(REEDSInput_new.head())


# In[6]:


# =========================================================
# PCA x YEAR TABLE
# =========================================================

new_pivot = REEDSInput_new.pivot_table(
    index='r',
    columns='year',
    values='cap_gw',
    aggfunc='sum'
).sort_index(axis=1)

print("\nPivoted data:")
print(new_pivot.head())


# In[8]:


def annualize_backward_equal(series):
    """
    Convert coarse new-install series into annual series
    by splitting each reported value equally backward across its interval.

    Example for 5-year spacing:
      2015 -> split across 2011,2012,2013,2014,2015
      2020 -> split across 2016,2017,2018,2019,2020
    """
    s = series.dropna().sort_index()
    out = {}

    if len(s) == 0:
        return pd.Series(dtype=float, name='new_Installed_Capacity_[MW]')

    years = list(s.index)
    vals = list(s.values)

    # infer first cadence from next point if possible
    if len(years) > 1:
        first_step = years[1] - years[0]
    else:
        first_step = 1

    y0 = years[0]
    v0 = float(vals[0])

    if first_step == 1:
        out[y0] = v0
    else:
        for yy in range(y0 - first_step + 1, y0 + 1):
            out[yy] = out.get(yy, 0.0) + v0 / first_step

    for i in range(1, len(years)):
        y_prev = years[i - 1]
        y_curr = years[i]
        v_curr = float(vals[i])
        step = y_curr - y_prev

        if step == 1:
            out[y_curr] = out.get(y_curr, 0.0) + v_curr
        else:
            for yy in range(y_curr - step + 1, y_curr + 1):
                out[yy] = out.get(yy, 0.0) + v_curr / step

    out = pd.Series(out).sort_index()
    out.name = 'new_Installed_Capacity_[MW]'
    return out


# In[9]:


debug_pca = new_pivot.index[0]

A_raw = new_pivot.loc[debug_pca].dropna().sort_index()
A_annual = annualize_backward_equal(A_raw)

print("RAW (GW):")
print(A_raw)

print("\nANNUALIZED (GW):")
print(A_annual.loc[2010:2035])


# In[11]:


r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)

# cSi baseline
r1.createScenario(
    name='Si',
    massmodulefile='baseline_modules_mass_US_Si.csv',
    energymodulefile='baseline_modules_energy_Si.csv'
)

# =====================================================================================
# LOAD PV ICE BASELINES
# =====================================================================================


baseline_Si = r1.scenario['Si'].dataIn_m.copy()
baseline_Si = baseline_Si.drop(columns=['new_Installed_Capacity_[MW]'])
baseline_Si.set_index('year', inplace=True)
baseline_Si.index = baseline_Si.index.astype(int)

# CdTe baseline
r1.createScenario(
    name='CdTe',
    massmodulefile='baseline_modules_mass_US_CdTe.csv',
    energymodulefile='baseline_modules_energy_CdTe.csv'
)
baseline_cdte = r1.scenario['CdTe'].dataIn_m.copy()
baseline_cdte = baseline_cdte.drop(columns=['new_Installed_Capacity_[MW]'])
baseline_cdte.set_index('year', inplace=True)
baseline_cdte.index = baseline_cdte.index.astype(int)

# =====================================================================================
# READ THE TWO HEADER ROWS FROM THE BASELINE FILE
# =====================================================================================

massmodulefile = os.path.join(baselinesFolder, 'baseline_modules_mass_US_Si.csv')

with open(massmodulefile, newline='') as f:
    reader = csv.reader(f)
    row1 = next(reader)
    row2 = next(reader)

row11 = 'year,' + ','.join(row1[1:])
row22 = 'year,' + ','.join(row2[1:])
header_text = row11 + '\n' + row22 + '\n'

# =====================================================================================
# LOAD MARKET SHARE
# =====================================================================================

marketsharefile = os.path.join(
    baselinesFolder,
    'SupportingMaterial',
    'output_USA_Si_marketshare.csv'
)

marketshare = pd.read_csv(marketsharefile)
marketshare = marketshare[marketshare['Year'] >= 2010].reset_index(drop=True)
marketshare.set_index('Year', inplace=True)
marketshare.index = marketshare.index.astype(int)

marketshare.rename(columns={'All_Marketshare': 'Si Market Share'}, inplace=True)
marketshare.loc[2021:, 'Si Market Share'] = 0.81
marketshare['CdTe Market Share'] = 1 - marketshare['Si Market Share']


# In[12]:


for PCA in new_pivot.index:
    A_raw = new_pivot.loc[PCA].dropna().sort_index()
    A_annual = annualize_backward_equal(A_raw)

    A = pd.DataFrame(A_annual)

    # keep 2010 onward
    A = A[A.index >= 2010].copy()

    # convert GW -> MW
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 1000

    A.index.name = 'year'

    # align to PV ICE baseline years
    target_years = baseline_Si.index
    A = A.reindex(target_years, fill_value=0.0)

    # align market share
    ms = marketshare.reindex(A.index).copy()
    ms['Si Market Share'] = ms['Si Market Share'].ffill().fillna(0.82)
    ms['CdTe Market Share'] = ms['CdTe Market Share'].ffill().fillna(0.18)

    # -----------------------------
    # Si
    # -----------------------------
    B = A.copy()
    B['new_Installed_Capacity_[MW]'] = (
        B['new_Installed_Capacity_[MW]'] * ms['Si Market Share'].values
    )
    B = pd.concat([B, baseline_Si.reindex(A.index)], axis=1)

    filetitle = os.path.join(subtestfolder, f'Mid_Case_Si_{PCA}.csv')
    with open(filetitle, 'w', newline='') as ict:
        ict.write(header_text)
        B.to_csv(ict, header=False)

    # -----------------------------
    # CdTe
    # -----------------------------
    B = A.copy()
    B['new_Installed_Capacity_[MW]'] = (
        B['new_Installed_Capacity_[MW]'] * ms['CdTe Market Share'].values
    )
    B = pd.concat([B, baseline_cdte.reindex(A.index)], axis=1)

    filetitle = os.path.join(subtestfolder, f'Mid_Case_CdTe_{PCA}.csv')
    with open(filetitle, 'w', newline='') as ict:
        ict.write(header_text)
        B.to_csv(ict, header=False)

print("Saved files in:", subtestfolder)

