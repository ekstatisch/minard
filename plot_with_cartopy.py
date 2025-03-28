import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import sqlite3
import numpy as np

# 1. get data frame
connection = sqlite3.connect("data/minard.db")
city_df = pd.read_sql(""" SELECT * FROM cities""", con=connection)
temp_df = pd.read_sql(""" SELECT * FROM temperature  ORDER BY lont asc""", con=connection)
troop_df = pd.read_sql(""" SELECT * FROM troops""", con=connection)
connection.close()
# city data
loncs = city_df["lonc"].values
latcs = city_df["latc"].values
cities = city_df["city"].values
# troop data
lonps = troop_df["lonp"].values
latps = troop_df["latp"].values
survives = troop_df["surviv"].values
directions = troop_df["direc"].values
rows = troop_df.shape[0] 

# 2. create plots
#fig, axes = plt.subplots(nrows=2, figsize=(25,12), gridspec_kw={"height_ratios":[4, 1]})
fig = plt.figure(figsize=(25,12))
gs = gridspec.GridSpec(2,1,height_ratios=[4,1])
axes = [
    fig.add_subplot(gs[0],projection = ccrs.LambertConformal(central_longitude=np.median(loncs), central_latitude=np.median(latcs))),
    fig.add_subplot(gs[1])
]

# create city map canvas in plt
# set range
axes[0].set_extent([np.min(loncs)-1,np.max(loncs)+1,np.min(latcs)-1,np.max(latcs)+1],crs=ccrs.PlateCarree())
axes[0].add_feature(cfeature.COASTLINE, linewidth=0.8)
axes[0].add_feature(cfeature.RIVERS, linewidth=0.5)
axes[0].gridlines(draw_labels={"left": True, "bottom": True}, linewidth=0.5)

axes[0].scatter(loncs, latcs, transform=ccrs.PlateCarree(), color='red', s=50, zorder=4)
for lon,lat,city in zip(loncs, latcs, cities):
    axes[0].annotate(text = city, xy=(lon,lat), fontsize=8,transform=ccrs.PlateCarree(), zorder=5)

# create troops
for i in range(rows-1):
    start_stop_lon = (lonps[i], lonps[i+1])
    start_stop_lat = (latps[i], latps[i+1])
    if directions[i] == "A":
        line_color = "tan"
    else:
        line_color = "gray"
    axes[0].plot(start_stop_lon, start_stop_lat, linewidth=(survives[i]/10000), color= line_color, zorder=1, transform=ccrs.PlateCarree())


# create temperature on axes[1]
lonts = temp_df["lont"].values
temps_celsius = (temp_df["temp"]*5/4).astype(int)   #pandas series
annotations = temps_celsius.astype(str).str.cat(temp_df["date"], sep="°C ")
axes[1].plot(lonts, temps_celsius)
for lont, temp, annotation in zip(lonts, temps_celsius, annotations):
    axes[1].annotate(annotation, xy=(lont-0.3, temp - 7), fontsize=10)

axes[1].set_ylim(-50, 10)
axes[1].set_xlim(np.min(loncs)-1, np.max(loncs)+1)

yticks = np.arange(-50, 11, 20)
axes[1].set_yticks(yticks)
axes[1].set_yticklabels([f"{tick}°C" for tick in yticks])

axes[1].spines["top"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].grid(True, which="major", axis="both")

#set title
axes[0].set_title("Napoleon's disastrous Russian compaign of 1812", loc="center", fontsize=20)
axes[0].set_position([0.05, 0.25, 0.9, 0.7])  # [left, bottom, width, height]
axes[1].set_position([0.05, 0.05, 0.9, 0.2])

plt.savefig("minard_clone_cartopy.png", dpi=300)
plt.show()