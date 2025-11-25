#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# --- Step 1: Load the merged file ---
df = pd.read_csv(r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\Kepler_GID_Recyclers_Merged.csv")

# --- Step 2: Ensure column types are correct ---
# Clean RID column (in case it was saved as float like 1.0 → r1)
df['nearest_RID'] = df['nearest_RID'].astype(str).str.replace(r'\.0$', '', regex=True)
df['nearest_RID'] = df['nearest_RID'].apply(lambda x: f"r{x}" if not str(x).startswith('r') else x)

# --- Step 3: Identify year columns ---
year_cols = [2025, 2030, 2035]
# Convert to string if needed
year_cols = [str(y) for y in year_cols if str(y) in df.columns]

# --- Step 4: Group by recycler and sum ---
sum_by_rid = df.groupby('nearest_RID')[year_cols].sum()

# --- Step 5: Optional total column ---
sum_by_rid['Total'] = sum_by_rid.sum(axis=1)

# --- Step 6: Preview or save ---
print(sum_by_rid)

# Optionally export:
sum_by_rid.to_csv(r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\Kepler_Recycler_Totals.csv")


# In[2]:


sum_by_rid.to_csv(r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\Kepler_Recycler_Totals.csv")



# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt


# In[21]:


import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
import numpy as np

# --- Load totals (index = nearest_RID) ---
sum_by_rid = pd.read_csv(
    r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\Kepler_Recycler_Totals.csv",
    index_col='nearest_RID'
)

year_cols = [c for c in ['2025','2030','2035'] if c in sum_by_rid.columns]

outdir = r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\plots"
os.makedirs(outdir, exist_ok=True)

colors = ['#00E1C6', '#00B7C2', '#008B8B']  # teal set

# tightly clustered x positions (very small gaps)
x = np.array([0.00, 0.34, 0.68])   # cluster width ~0.68
bar_width = 0.30                   # leaves ~0.04 gap between bars

for rid, row in sum_by_rid[year_cols].iterrows():
    vals_kt = (row.astype(float) / 1000.0).round(1)

    # make the figure a bit NARROWER so the cluster looks compact
    fig, ax = plt.subplots(figsize=(1.1, 1.6))

    bars = ax.bar(x, vals_kt.values, color=colors[:len(year_cols)], width=bar_width)

    # label only the last bar (2035)
    last_bar = bars[-1]
    val = vals_kt.values[-1]
    ax.text(
        last_bar.get_x() + last_bar.get_width()/2,
        last_bar.get_height() + max(0.03, 0.06 * (vals_kt.max() > 0)),
        f"{val:.1f} kt",
        ha='center', va='bottom',
        fontsize=12, color='white', fontweight='bold',
        path_effects=[pe.withStroke(linewidth=2.8, foreground='black')]
    )

    # remove axes, pack limits tight around cluster
    ax.axis('off')
    ax.set_xlim(-0.05, 0.73)                    # hugs the cluster
    ax.set_ylim(0, vals_kt.max() * 1.28 if vals_kt.max() > 0 else 0.5)
    plt.margins(x=0, y=0)

    plt.tight_layout(pad=0)
    plt.savefig(
        os.path.join(outdir, f"{rid}_bars.svg"),
        format='svg', transparent=True, bbox_inches='tight', pad_inches=0
    )
    plt.close(fig)


# In[23]:


# Plots 3 labels

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
import numpy as np

# --- Load totals (index = nearest_RID) ---
sum_by_rid = pd.read_csv(
    r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\Kepler_Recycler_Totals.csv",
    index_col='nearest_RID'
)

year_cols = [c for c in ['2025','2030','2035'] if c in sum_by_rid.columns]

outdir = r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\plots"
os.makedirs(outdir, exist_ok=True)

colors = ['#00E1C6', '#00B7C2', '#008B8B']  # teal set

# tightly clustered x positions (very small gaps)
x = np.array([0.00, 0.34, 0.68])   # cluster width ~0.68
bar_width = 0.30                   # leaves ~0.04 gap between bars

for rid, row in sum_by_rid[year_cols].iterrows():
    vals_kt = (row.astype(float) / 1000.0).round(1)

    # make the figure a bit NARROWER so the cluster looks compact
    fig, ax = plt.subplots(figsize=(1.1, 1.6))

    bars = ax.bar(x, vals_kt.values, color=colors[:len(year_cols)], width=bar_width)

    # label ALL bars (not just last)
    for bar, val in zip(bars, vals_kt.values):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + max(0.03, 0.06 * (vals_kt.max() > 0)),
            f"{val:.1f} kt",
            ha='center', va='bottom',
            fontsize=12, color='white', fontweight='bold',
            path_effects=[pe.withStroke(linewidth=2.8, foreground='black')]
        )

    # remove axes, pack limits tight around cluster
    ax.axis('off')
    ax.set_xlim(-0.05, 0.73)                    # hugs the cluster
    ax.set_ylim(0, vals_kt.max() * 1.28 if vals_kt.max() > 0 else 0.5)
    plt.margins(x=0, y=0)

    plt.tight_layout(pad=0)
    plt.savefig(
        os.path.join(outdir, f"{rid}_bars.svg"),
        format='svg', transparent=True, bbox_inches='tight', pad_inches=0
    )
    plt.close(fig)


# In[ ]:


# Plots 3 labels

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
import numpy as np

# --- Load totals (index = nearest_RID) ---
sum_by_rid = pd.read_csv(
    r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\Kepler_Recycler_Totals.csv",
    index_col='nearest_RID'
)

year_cols = [c for c in ['2025','2030','2035'] if c in sum_by_rid.columns]

outdir = r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\plots"
os.makedirs(outdir, exist_ok=True)

colors = ['#00E1C6', '#00B7C2', '#008B8B']  # teal set

# tightly clustered x positions (very small gaps)
x = np.array([0.00, 0.34, 0.68])   # cluster width ~0.68
bar_width = 0.30                   # leaves ~0.04 gap between bars

for rid, row in sum_by_rid[year_cols].iterrows():
    vals_kt = (row.astype(float) / 1000.0).round(1)

    # make the figure a bit NARROWER so the cluster looks compact
    fig, ax = plt.subplots(figsize=(1.1, 1.6))

    bars = ax.bar(x, vals_kt.values, color=colors[:len(year_cols)], width=bar_width)

    # label ALL bars (not just last)
    for bar, val in zip(bars, vals_kt.values):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + max(0.03, 0.06 * (vals_kt.max() > 0)),
            f"{val:.1f} kt",
            ha='center', va='bottom',
            fontsize=12, color='white', fontweight='bold',
            path_effects=[pe.withStroke(linewidth=2.8, foreground='black')]
        )

    # remove axes, pack limits tight around cluster
    ax.axis('off')
    ax.set_xlim(-0.05, 0.73)                    # hugs the cluster
    ax.set_ylim(0, vals_kt.max() * 1.28 if vals_kt.max() > 0 else 0.5)
    plt.margins(x=0, y=0)

    plt.tight_layout(pad=0)
    plt.savefig(
        os.path.join(outdir, f"{rid}_bars.svg"),
        format='svg', transparent=True, bbox_inches='tight', pad_inches=0
    )
    plt.close(fig)


# In[24]:


import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
import numpy as np

# --- Files ---
totals_csv = r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\Kepler_Recycler_Totals.csv"
recyclers_csv = r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\SEIA Recycling Centers 07Oct2025.csv"

# --- Load totals (index = nearest_RID) ---
sum_by_rid = pd.read_csv(totals_csv, index_col='nearest_RID')
year_cols = [c for c in ['2025','2030','2035'] if c in sum_by_rid.columns]

# --- Load recycler city names from CSV to avoid mismatches ---
recyclers = pd.read_csv(recyclers_csv)
recyclers.columns = recyclers.columns.str.strip()
recycler_city = recyclers.set_index('RID')['Region / Nearby City'].astype(str)

# --- Output folder (won't overwrite previous) ---
outdir = r"C:\Users\sayala\Documents\GitHub\PV_ICE\docs\tutorials\13 - US Spatial Analysis for US Si & CdTe\TEMP\plots_citylabels"
os.makedirs(outdir, exist_ok=True)

# --- Colors + spacing ---
colors = ['#00E1C6', '#00B7C2', '#008B8B']      # teal set
bar_width = 0.25
gap = 0.25                                       # ~one bar-width gap
x = np.array([0.0, bar_width + gap, 2*(bar_width + gap)])

for rid, row in sum_by_rid[year_cols].iterrows():
    vals_kt = (row.astype(float) / 1000.0).round(1)
    vmax = float(vals_kt.max()) if len(vals_kt) else 0.0

    fig, ax = plt.subplots(figsize=(1.5, 1.9))   # a touch wider for the city label

    bars = ax.bar(x, vals_kt.values, color=colors[:len(year_cols)], width=bar_width)

    # label ALL bars
    for bar, val in zip(bars, vals_kt.values):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.05,
            f"{val:.1f} kt",
            ha='center', va='bottom',
            fontsize=11, color='white', fontweight='bold',
            path_effects=[pe.withStroke(linewidth=2.6, foreground='black')]
        )

    # city label centered under the cluster
    city = recycler_city.get(rid, rid)
    ax.text(
        np.mean(x) + bar_width/2, -0.18 * (vmax if vmax > 0 else 1.0),
        city,
        ha='center', va='top',
        fontsize=10, color='white', fontweight='bold',
        path_effects=[pe.withStroke(linewidth=2.4, foreground='black')]
    )

    # minimal look
    ax.axis('off')
    ax.set_xlim(-0.2, x[-1] + bar_width + 0.2)
    ax.set_ylim(-0.28 * (vmax if vmax > 0 else 1.0), vmax * 1.35 if vmax > 0 else 0.5)
    plt.margins(0, 0)
    plt.tight_layout(pad=0)

    plt.savefig(
        os.path.join(outdir, f"{rid}_bars_city.svg"),
        format='svg', transparent=True, bbox_inches='tight', pad_inches=0
    )
    plt.close(fig)


# In[25]:


# --- find global max across all recyclers ---
global_max = (sum_by_rid[year_cols] / 1000.0).to_numpy().max()

for rid, row in sum_by_rid[year_cols].iterrows():
    vals_kt = (row.astype(float) / 1000.0).round(1)
    vmax = float(vals_kt.max())

    # normalize by global max
    norm_vals = vals_kt * (vmax / global_max) if global_max > 0 else vals_kt

    fig, ax = plt.subplots(figsize=(1.5, 1.9))
    bars = ax.bar(x, norm_vals.values, color=colors[:len(year_cols)], width=bar_width)

    # label all bars with actual (non-normalized) values
    for bar, val in zip(bars, vals_kt.values):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.05,
            f"{val:.1f} kt",
            ha='center', va='bottom',
            fontsize=11, color='white', fontweight='bold',
            path_effects=[pe.withStroke(linewidth=2.6, foreground='black')]
        )

    # city label at bottom
    city = recycler_city.get(rid, rid)
    ax.text(
        np.mean(x) + bar_width/2, -0.18 * (global_max if global_max > 0 else 1.0),
        city,
        ha='center', va='top',
        fontsize=10, color='white', fontweight='bold',
        path_effects=[pe.withStroke(linewidth=2.4, foreground='black')]
    )

    ax.axis('off')
    ax.set_xlim(-0.2, x[-1] + bar_width + 0.2)
    ax.set_ylim(-0.28 * global_max, global_max * 1.35 if global_max > 0 else 0.5)
    plt.margins(0, 0)
    plt.tight_layout(pad=0)

    plt.savefig(
        os.path.join(outdir, f"{rid}_bars_city_scaled.svg"),
        format='svg', transparent=True, bbox_inches='tight', pad_inches=0
    )
    plt.close(fig)

