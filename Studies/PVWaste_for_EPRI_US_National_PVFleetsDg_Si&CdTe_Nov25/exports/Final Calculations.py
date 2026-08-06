#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd

# Load file
df = pd.read_csv(r"C:\Users\sayala\Documents\GitHub\public\PV_ICE\Studies\PVWaste_for_EPRI_US_National_PVFleetsDg_Si&CdTe_Nov25\Sims\Yearly_2036.csv")

# Identify columns
si_cols = df.filter(regex=r"^WasteAll_Module_Sim1_Si_deg_").columns
cdte_cols = df.filter(regex=r"^WasteAll_Module_Sim1_CdTe_").columns

# Combine both sets
all_cols = list(si_cols) + list(cdte_cols)

# Sum per row (per year)
df["WasteAll_Modules_total_tonnes"] = df[all_cols].sum(axis=1)

# Optional: keep only Year + result
result = df[["year", "WasteAll_Modules_total_tonnes"]]

print(result.head(36))


# In[7]:


result[result["year"] == 2030]

