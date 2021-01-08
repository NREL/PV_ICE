#!/usr/bin/env python
# coding: utf-8

# # ReEDS Scenarios on PV ICE Tool

# To explore different scenarios for furture installation projections of PV (or any technology), ReEDS output data can be useful in providing standard scenarios. ReEDS installation projections are used in this journal as input data to the PV ICE tool. 
# 
# Current sections include:
# 
# <ol>
#     <li> ### Reading a standard ReEDS output file and saving it in a PV ICE input format </li>
# <li>### Reading scenarios of interest and running PV ICE tool </li>
# <li>###Plotting </li>
# <li>### GeoPlotting.</li>

# In[1]:


import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = (12, 8)


# In[2]:


import os
from pathlib import Path

testfolder = str(Path().resolve().parent.parent / 'PV_ICE' / 'TEMP')

print ("Your simulation will be stored in %s" % testfolder)


# # Reading a standard ReEDS output file and saving it in a PV ICE input format

# In[3]:


reedsFile = str(Path().resolve().parent.parent.parent / 'December Core Scenarios ReEDS Outputs Solar Futures v2a.xlsx')
print ("Input file is stored in %s" % reedsFile)


# In[4]:


rawdf = pd.read_excel(reedsFile,
                        sheet_name="UPV Capacity (GW)")
                        #index_col=[0,2,3]) #this casts scenario, PCA and State as levels
#now set year as an index in place
rawdf.drop(columns=['State'], inplace=True)
rawdf.drop(columns=['Tech'], inplace=True)
rawdf.set_index(['Scenario','Year','PCA'], inplace=True)


# In[5]:


rawdf.head()


# In[6]:


scenarios = list(rawdf.index.get_level_values('Scenario').unique())
PCAs = list(rawdf.index.get_level_values('PCA').unique())
scenarios


# In[7]:


import PV_ICE
r1 = PV_ICE.Simulation(name='Simulation1', path=testfolder)
r1.createScenario(name='US', file=r'..\baselines\baseline_modules_US.csv')
baseline = r1.scenario['US'].data
baseline = baseline.drop(columns=['new_Installed_Capacity_[MW]'])
baseline.set_index('year', inplace=True)
baseline.index = pd.PeriodIndex(baseline.index, freq='A')  # A -- Annual


# In[8]:


baseline.head()


# In[12]:


rawdf.head(21)


# In[ ]:


A = rawdf.unstack(level=1).iloc[0]
A = A.droplevel(level=0)
A.name = 'new_Installed_Capacity_[MW]'
A = pd.DataFrame(A)
A.index=pd.PeriodIndex(A.index, freq='A')
A = A.resample('Y').asfreq()
A = A['new_Installed_Capacity_[MW]'].fillna(0).groupby(A['new_Installed_Capacity_[MW]'].notna().cumsum()).transform('mean')    
A = pd.DataFrame(A)
A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 1000   # ReEDS file is in GW.
# Add other columns
A = pd.concat([A, baseline.reindex(A.index)], axis=1)


# In[117]:


A = rawdf.unstack(level=1).iloc[0]
A = A.droplevel(level=0)
A.name = 'new_Installed_Capacity_[MW]'
A = pd.DataFrame(A)
A.index=pd.PeriodIndex(A.index, freq='A')
A = A.resample('Y').asfreq()


# In[119]:


A = A['new_Installed_Capacity_[MW]'].fillna(0)


# In[121]:


B = A[1:]


# In[123]:


B.index=B.index-1


# In[128]:


B = pd.DataFrame(B)


# In[131]:


B = B.groupby(B['new_Installed_Capacity_[MW]'].cumsum()).transform('mean')    


# In[132]:





# In[ ]:


for ii in range (len(rawdf.unstack(level=1))):
    PCA = rawdf.unstack(level=1).iloc[ii].name[1]
    SCEN = rawdf.unstack(level=1).iloc[ii].name[0]
    SCEN=SCEN.replace('+', '_')
    filetitle = SCEN+'_'+PCA +'.csv'
    filetitle = os.path.join(testfolder, filetitle)
    A = rawdf.unstack(level=1).iloc[ii]
    A = A.droplevel(level=0)
    A.name = 'new_Installed_Capacity_[MW]'
    A = pd.DataFrame(A)
    A.index=pd.PeriodIndex(A.index, freq='A')
    A = A.resample('Y').asfreq()
    A = A['new_Installed_Capacity_[MW]'].fillna(0).groupby(A['new_Installed_Capacity_[MW]'].notna().cumsum()).transform('mean')    
    A = pd.DataFrame(A)
    A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 1000   # ReEDS file is in GW.
    # Add other columns
    A = pd.concat([A, baseline.reindex(A.index)], axis=1)

    header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,"    "mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,"    "mod_Repowering,mod_Repairing\n"    "year,MW,%,years,years,%,years,%,%,%,%,%\n"

    with open(filetitle, 'w', newline='') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
        for line in header:
            ict.write(line)

        #    savedata.to_csv(ict, index=False)
        A.to_csv(ict, header=False)


# In[ ]:


# EXAMPLE FOR JUST ONE 
ii = 0
PCA = rawdf.unstack(level=1).iloc[ii].name[1]
SCEN = rawdf.unstack(level=1).iloc[ii].name[0]
SCEN=SCEN.replace('+', '_')
filetitle = SCEN+'_'+PCA +'.csv'
filetitle = os.path.join(testfolder, filetitle)
A = rawdf.unstack(level=1).iloc[ii]        
A = A.droplevel(level=0)
A.name = 'new_Installed_Capacity_[MW]'
A = pd.DataFrame(A)
A['new_Installed_Capacity_[MW]'] = A['new_Installed_Capacity_[MW]'] * 1000
A.index=pd.PeriodIndex(A.index, freq='A')
B = A.resample('Y').asfreq()
B = B['new_Installed_Capacity_[MW]'].fillna(0).groupby(B['new_Installed_Capacity_[MW]'].notna().cumsum()).transform('mean')
B = pd.DataFrame(B)
B.to_csv(filetitle)

# Add other columns
B = pd.concat([B, baseline.reindex(B.index)], axis=1)


header = "year,new_Installed_Capacity_[MW],mod_eff,mod_reliability_t50,mod_reliability_t90,""mod_degradation,mod_lifetime,mod_MFG_eff,mod_EOL_collection_eff,mod_EOL_collected_recycled,""mod_Repowering,mod_Repairing\n""year,MW,%,years,years,%,years,%,%,%,%,%\n"

with open(filetitle, 'w', newline='') as ict:
# Write the header lines, including the index variable for
# the last one if you're letting Pandas produce that for you.
# (see above).
    for line in header:
        ict.write(line)

    #    savedata.to_csv(ict, index=False)
    B.to_csv(ict, header=False)


# ### Reading GIS inputs

# In[ ]:


GISfile = str(Path().resolve().parent.parent.parent / 'gis_centroid_n.xlsx')
GIS = pd.read_excel(GISfile)
GIS = GIS.set_index('id')


# In[ ]:


GIS.head()


# In[ ]:


GIS.loc['p1'].long


# ### Create Scenarios

# In[ ]:


simulationname = scenarios
simulationname = [w.replace('+', '_') for w in simulationname]
PCA = PCAs[0]
simulationname


# In[ ]:


SFscenarios = [scenarios[0], scenarios[4], scenarios[8]]


# In[ ]:


SFscenarios


# In[ ]:


#for ii in range (0, 1): #len(scenarios):
r1 = PV_ICE.Simulation(name=SFscenarios[0], path=testfolder)
for jj in range (0, len(PCAs)): 
    filetitle = SFscenarios[0]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, filetitle)        
    r1.createScenario(name=PCAs[jj], file=filetitle)
    r1.scenario[PCAs[jj]].addMaterial('glass', file=r'..\baselines\baseline_material_glass_Reeds.csv')
    r1.scenario[PCAs[jj]].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon_Reeds.csv')
    r1.scenario[PCAs[jj]].addMaterial('silver', file=r'..\baselines\baseline_material_silver_Reeds.csv')
    r1.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r1.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long

r2 = PV_ICE.Simulation(name=SFscenarios[1], path=testfolder)
for jj in range (0, len(PCAs)): 
    filetitle = SFscenarios[1]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, filetitle)        
    r2.createScenario(name=PCAs[jj], file=filetitle)
    r2.scenario[PCAs[jj]].addMaterial('glass', file=r'..\baselines\baseline_material_glass_Reeds.csv')
    r2.scenario[PCAs[jj]].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon_Reeds.csv')
    r2.scenario[PCAs[jj]].addMaterial('silver', file=r'..\baselines\baseline_material_silver_Reeds.csv')
    r2.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r2.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long

r3 = PV_ICE.Simulation(name=SFscenarios[2], path=testfolder)
for jj in range (0, len(PCAs)): 
    filetitle = simulationname[8]+'_'+PCAs[jj]+'.csv'
    filetitle = os.path.join(testfolder, filetitle)        
    r3.createScenario(name=PCAs[jj], file=filetitle)
    r3.scenario[PCAs[jj]].addMaterial('glass', file=r'..\baselines\baseline_material_glass_Reeds.csv')
    r3.scenario[PCAs[jj]].addMaterial('silicon', file=r'..\baselines\baseline_material_silicon_Reeds.csv')
    r3.scenario[PCAs[jj]].addMaterial('silver', file=r'..\baselines\baseline_material_silver_Reeds.csv')
    r3.scenario[PCAs[jj]].latitude = GIS.loc[PCAs[jj]].lat
    r3.scenario[PCAs[jj]].longitude = GIS.loc[PCAs[jj]].long


# In[ ]:


r1.calculateMassFlow()


# In[ ]:


r2.calculateMassFlow()
r3.calculateMassFlow()


# In[ ]:


r1.scenario.keys()


# In[ ]:


r1.scenario[PCAs[jj]].data.keys()


# In[ ]:


r1.scenario[PCAs[jj]].material['glass'].materialdata.keys()


# In[ ]:


r1.scenario['p1'].data.head()


# In[ ]:


r1.scenario['p107'].data['Cumulative_Area_disposedby_Failure'].sum()


# In[ ]:


#new_Installed_Capacity_[MW]

keyword='new_Installed_Capacity_[MW]'

foo = r1.scenario[PCAs[12]].data[keyword].copy()
plt.figure()
plt.plot(r1.scenario[PCAs[0]].data['year'], foo, label=PCAs[12])
plt.legend()
print(max(foo))
print(foo)


# In[ ]:


for jj in range (1, len(PCAs)): 
    foo += r1.scenario[PCAs[jj]].data[keyword]
     
#UScumsumlandfill_glass = np.cumsum(USlandfill_glass)
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax.plot(r1.scenario[PCAs[0]].data['year'], foo, label='US')
#ax.set_yscale('log')
print(max(foo))


# In[ ]:


r1.scenario['p105'].data['Cumulative_Area_disposedby_Failure'].sum()


# In[ ]:


r1.plotScenariosComparison(keyword='Cumulative_Area_disposedby_Failure')


# In[ ]:


r1.plotMaterialComparisonAcrossScenarios(material='silicon', keyword='mat_Total_Landfilled')


# In[ ]:


r1.plotMaterialComparisonAcrossScenarios(material='silver', keyword='mat_Total_Landfilled')


# In[ ]:


r1.plotMaterialComparisonAcrossScenarios(material='glass', keyword='mat_Total_Landfilled')


# In[ ]:


# Plot Cumulative Material Waste


# In[ ]:


if keyword is None:
    scens = list(self.scenario.keys())[0]
    mats = list(self.scenario[scens].material.keys())[0]
    print("Choose one of the keywords: ",  list(self.scenario[scens].material[mats].materialdata.keys())) 
    return

if material is None:
    scens = list(self.scenario.keys())[0]
    mats = list(self.scenario[scens].material.keys())
    print("Choose one of the Materials: ", mats) 
    return

yunits = _unitReferences(keyword)

plt.figure()

for scen in self.scenario:
    plt.plot(self.scenario[scen].data['year'], self.scenario[scen].material[material].materialdata[keyword], label=scen)
    plt.legend()

plt.xlabel('Year')
plt.title((material + ' ' + keyword.replace('_', " ")))
plt.ylabel(yunits)    


# In[ ]:


material1='glass'
material2='silicon'
material3='silver'
keyword='mat_Total_Landfilled'

USlandfill_glass = r1.scenario[PCAs[0]].material[material1].materialdata[keyword]
USlandfill_silicon = r1.scenario[PCAs[0]].material[material2].materialdata[keyword]
USlandfill_silver = r1.scenario[PCAs[0]].material[material3].materialdata[keyword]

for jj in range (1, len(PCAs)): 
    USlandfill_glass += r1.scenario[PCAs[jj]].material[material1].materialdata[keyword] 
    USlandfill_silicon += r1.scenario[PCAs[jj]].material[material2].materialdata[keyword] 
    USlandfill_silver += r1.scenario[PCAs[jj]].material[material3].materialdata[keyword]
    
UScumsumlandfill_glass = np.cumsum(USlandfill_glass)
UScumsumlandfill_silicon = np.cumsum(USlandfill_silicon)
UScumsumlandfill_silver = np.cumsum(USlandfill_silver)


# In[ ]:


plt.plot(r1.scenario[PCAs[0]].data['year'], UScumsumlandfill_glass, label='Glass')
plt.plot(r1.scenario[PCAs[0]].data['year'], UScumsumlandfill_silicon, label='Silicon')
plt.plot(r1.scenario[PCAs[0]].data['year'], UScumsumlandfill_silver, label='Silver')


# In[ ]:





# # GEOPANDAS

# In[ ]:


latitude_all =[]
longitude_all = []
cumulativewaste2050 = []
for scen in r1.scenario.keys():
    latitude_all.append(r1.scenario[scen].latitude)
    longitude_all.append(r1.scenario[scen].longitude)
    cumulativewaste2050.append(r1.scenario[scen].material['glass'].materialdata['mat_Total_Landfilled'].sum())


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon

street_map = gpd.read_file(r'C:\Users\sayala\Desktop\geopandas\cb_2018_us_nation_20m\cb_2018_us_nation_20m.shp')

# Show the map only
#fig, ax = plt.subplots(figsize=(10,15))
#street_map.plot(ax=ax)


# In[ ]:


frame = { 'Latitude': latitude_all, 'Longitude': longitude_all, 'CumulativeWaste2050': cumulativewaste2050}   
df = pd.DataFrame(frame) 


# In[ ]:


df.head()


# In[ ]:


geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
geometry[:3]


# In[ ]:


crs = {'init':'epsg:4326'}


# In[ ]:


geo_df = gpd.GeoDataFrame(df, # specify our data
                         crs = crs, # specify our coordinate reference system
                         geometry = geometry) # specify the geometry list we created
geo_df.head()


# In[ ]:


fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax = ax, alpha = 0.4, color = "grey")
geo_df[geo_df['CumulativeWaste2050'] >= 1.918125e+09].plot(ax=ax, markersize = 20, color= "blue", marker = "o", label = "Bigger Than")
geo_df[geo_df['CumulativeWaste2050'] < 1.918125e+09].plot(ax=ax, markersize = 20, color= "red", marker = "o", label = "Less Than")
plt.xlim([-130, -60])
plt.ylim([20, 50])
plt.legend(prop={'size':15})


# In[ ]:


import random
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon

latitude = random.sample(range(25, 45), 10) 
longitude = random.sample(range(-125, -65), 10) 
weight = random.sample(range(0, 500), 10) 

frame = { 'Latitude': latitude, 'Longitude': longitude, 'Weight': weight}   
df = pd.DataFrame(frame) 

geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
crs = {'init':'epsg:4326'}
geo_df = gpd.GeoDataFrame(df, # specify our data
                         crs = crs, # specify our coordinate reference system
                         geometry = geometry) # specify the geometry list we created

fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax = ax, alpha = 0.4, color = "grey")
geo_df[geo_df['Weight'] >=250].plot(ax=ax, markersize = 20, color= "blue", marker = "o", label = "Bigger Than")
geo_df[geo_df['Weight'] < 250].plot(ax=ax, markersize = 20, color= "red", marker = "o", label = "Less Than")
plt.xlim([-130, -60])
plt.ylim([20, 50])
plt.legend(prop={'size':15})


# In[ ]:


import geoplot


# In[ ]:


ax = street_map.kdeplot(
    geo_df, #clip=boroughs.geometry,
    shade=True, cmap='Reds',
    projection=geoplot.crs.AlbersEqualArea())
geoplot.polyplot(boroughs, ax=ax, zorder=1)


# In[ ]:





# In[ ]:


import scipy.stats
import seaborn.palettes
import seaborn.utils


# In[ ]:


axis = [-130, 48.1667, -70, 100.1667]


# In[ ]:


latlng_bounds = area.total_bounds
area = area.to_crs(epsg=3857)
axis = area.total_bounds

# Create the map stretching over the requested area
ax = area.plot(alpha=0)


# In[ ]:


# Calculate the KDE
data = np.c_[df.Longitude, df.Latitude]
kde = scipy.stats.gaussian_kde(data.T, bw_method="scott", weights=df.CumulativeWaste2050)
data_std = data.std(axis=0, ddof=1)
bw_x = getattr(kde, "scotts_factor")() * data_std[0]
bw_y = getattr(kde, "scotts_factor")() * data_std[1]
grid_x = grid_y = 100
x_support = seaborn.utils._kde_support(data[:, 0], bw_x, grid_x, 3, (axis[0], axis[2]))
y_support = seaborn.utils._kde_support(data[:, 1], bw_y, grid_y, 3, (axis[1], axis[3]))
xx, yy = np.meshgrid(x_support, y_support)
levels = kde([xx.ravel(), yy.ravel()]).reshape(xx.shape)


# In[ ]:


cset = ax.contourf(xx, yy, levels,
    20, # n_levels

    cmap=seaborn.palettes.blend_palette(('#ffffff10', '#ff0000af'), 6, as_cmap=True),
    antialiased=True,       # avoids lines on the contours to some extent
)


# In[ ]:





# In[ ]:


def add_basemap(ax, latlng_bounds, axis, url='https://a.basemaps.cartocdn.com/light_all/tileZ/tileX/tileY@2x.png'):
    prev_ax = ax.axis()
    # TODO: Zoom should surely take output pixel request size into account...
    zoom = ctx.tile._calculate_zoom(*latlng_bounds)
    while ctx.tile.howmany(*latlng_bounds, zoom, ll=True) > max_tiles:      # dont ever try to download loads of tiles
        zoom = zoom - 1
    print("downloading %d tiles with zoom level %d" % (ctx.tile.howmany(*latlng_bounds, zoom, ll=True), zoom))
    basemap, extent = ctx.bounds2img(*axis, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    ax.axis(prev_ax)        # restore axis after changing the background
 
add_basemap(ax, latlng_bounds, axis)


# In[ ]:


import geopandas as gpd


import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

def make_plot(projection_name, projection_crs, extent, heat_data):
    """
    ?
    """
    fig = plt.figure()
    rect = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes(rect, projection=projection_crs)

    # Set display limits to include a set region of latitude * longitude.
    # (Note: Cartopy-specific).
    ax.set_extent(extent, crs=projection_crs)

    # Add coastlines and meridians/parallels (Cartopy-specific).
    ax.coastlines(linewidth=0.2, color='black')
    ax.gridlines(crs=projection_crs, linestyle='-')

    lat = np.linspace(extent[0],extent[1],heat_data.shape[0])
    lon = np.linspace(extent[2],extent[3],heat_data.shape[1])
    Lat,Lon = np.meshgrid(lat,lon)
    ax.pcolormesh(Lat,Lon,np.transpose(heat_data))
    plt.savefig("Test_fig.pdf", bbox_inches='tight')


def main():
    #extent = (-65.0, -62, 44, 45.5)
    extent = (-90, -40, 30, 60)
    # Define some test points with latitude and longitude coordinates.
    #city_data = [('Halifax, NS', 44.67, -63.61, 'black'),
    #             ('Neighbour', 45, -63, 'blue'),
    #             ('Other_Place', 44.1, -64, 'red')]
    heat_data = np.random.normal(0.0,0.2,size=(100,150))

    # Demonstrate with two different display projections.
    # Define a Cartopy 'ordinary' lat-lon coordinate reference system.
    crs_latlon = ccrs.PlateCarree()
    make_plot('Equidistant Cylindrical', crs_latlon, extent, heat_data)
    #crs_ae = ccrs.LambertCylindrical()
    #make_plot('Lambert Cylindrical', crs_ae, extent, heat_data)

if __name__ == '__main__':
    main()

