#!/usr/bin/env python
# coding: utf-8

# # (development) Glass Share Calculations
# 
# 

# In[ ]:


'''
# Based on ITRPV numbers. ITRPV 2014 sets thickness of glass to 3.5, so assuming that value for all previous modules since 1995.
# Starting 2015 ITRPV, transparent backside (glass + transparent sheet) starts at 2%. Assuming 50% is glass.and same front thickness.
# Starting 2017, front thicknesses are indicated for front side. Thinner modules coincide with the values for expected bifacial modules with glass-glass backside, so assuming all thiner modules have a backside of same thickness.
# Glass backside thickness is not specified, so assuming for glass-glass backside is 2 mm thick for all cases
#  where front side is between 2-3 mm (assuming 2 mm for front side), and 1.8mm for cases where front side is < 2 mmm ( assuming 1.8mm for front side as well)
#  So overall module per panel is 3.5 for single side glass to up 4 mm glass-glass
df['glass_3p5'] = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 93, 93])/100

df['glass_3p5'] = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 93, 93, 90])/100
df['glass_2p'] = np.array([0, 0, 0, 0, 0, 0 , 15, 0.6, 0.55, 0.5, 0.5, 0.45, 0.4, 0.35, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.1, 0.075, 0.05, 0.05])/100
df['glass_1p8'] = np.array([100, 100, 100, 100, 100, 100, 85, 0.6, 0.55, 0.5, 0.5, 0.45, 0.4, 0.35, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.1, 0.075, 0.05, 0.05])/100

df['glass_3p5'] = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 93, 93])/100
df['glass_2p5'] = np.array([np.nan, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, np.nan, 100, 100, 100, 100, 100, 100, 100, 93, np.nan])/100

# doesn't change the 1st one, last one is just repeated value.
df.interpolate(method='linear', axis=0, limit=None, inplace=False, limit_direction='forward', limit_area=None, downcast=None)

import pandas as pd
from scipy.optimize import curve_fit

# Do the original interpolation
#df.interpolate(method='nearest', axis=0, inplace=True)

# Display result
print ('Interpolated data:')
print (df)
print ()

# Function to curve fit to the data
def func(x, a, b, c, d):
    return a * (x ** 3) + b * (x ** 2) + c * x + d

# Initial parameter guess, just to kick off the optimization
guess = (0.5, 0.5, 0.5, 0.5)

# Create copy of data to remove NaNs for curve fitting
fit_df = df.dropna()

# Place to store function parameters for each column
col_params = {}

# Curve fit each column
for col in fit_df.columns:
    # Get x & y
    x = fit_df.index.astype(float).values
    y = fit_df[col].values
    # Curve fit column and get curve parameters
    params = curve_fit(func, x, y, guess)
    # Store optimized parameters
    col_params[col] = params[0]

# Extrapolate each column
for col in df.columns:
    # Get the index values for NaNs in the column
    x = df[pd.isnull(df[col])].index.astype(float).values
    # Extrapolate those points with the fitted function
    df[col][x] = func(x, *col_params[col])

# Display result
print ('Extrapolated data:')
print (df)
print ()

print ('Data was extrapolated with these column functions:')
for col in col_params:
    print ('f_{}(x) = {:0.3e} x^3 + {:0.3e} x^2 + {:0.4f} x + {:0.4f}'.format(col, *col_params[col]))
   
   
# Mass of Silicon
# Fake numbers, just to establish process
df['cell_size_155'] = np.array([100, 100, 100, 100, 100, 100, 85, 0.6, 0.55, 0.5, 0.5, 0.45, 0.4, 0.35, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.1, 0.075, 0.05, 0.05])/100
df['cell_size_165'] = np.array([0, 0, 0, 0, 0, 0 , 15, 0.6, 0.55, 0.5, 0.5, 0.45, 0.4, 0.35, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.1, 0.075, 0.05, 0.05])/100

df['thickness_0p1'] = np.array([100, 100, 100, 100, 100, 100, 85, 0.6, 0.55, 0.5, 0.5, 0.45, 0.4, 0.35, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.1, 0.075, 0.05, 0.05])/100
df['thickness_0p2'] = np.array([0, 0, 0, 0, 0, 0 , 15, 0.6, 0.55, 0.5, 0.5, 0.45, 0.4, 0.35, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.1, 0.075, 0.05, 0.05])/100

area_cell_155 = 0.155**2
area_cell_165 = 0.165**2
df['area_cells_155'] = df['area']*df['cell_size_155']
df['area_cells_165'] = df['area']*df['cell_size_165']

df['VolumeSi_0p1_155'] = df['area_cells_155'] * df['thickness_0p1'] * 0.1
df['VolumeSi_0p1_165'] = df['area_cells_165'] * df['thickness_0p1'] * 0.1

df['VolumeSi_0p2_155'] = df['area_cells_155'] * df['thickness_0p2'] * 0.2
df['VolumeSi_0p2_165'] = df['area_cells_165'] * df['thickness_0p2'] * 0.2

silicon_density = 2532.59  # kg/m^3 Google knows best.
df['Mass_Silicon'] = silicon_density * (df['VolumeSi_0p1_155'] + df['VolumeSi_0p1_165'] + df['VolumeSi_0p2_155'] + df['VolumeSi_0p2_165'])

'''
print("")

