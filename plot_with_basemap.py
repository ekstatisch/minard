from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

# 1. get data frame
connection = sqlite3.connect("data/minard.db")
city_df = pd.read_sql(""" SELECT * FROM cities""", con=connection)
temp_df = pd.read_sql(""" SELECT * FROM temperature ORDER BY lont""", con=connection)
troop_df = pd.read_sql(""" SELECT * FROM troops""", con=connection)
connection.close()

loncs = city_df["lonc"].values
latcs = city_df["latc"].values
city_names = city_df["city"].values

lonps = troop_df["lonp"].values
latps = troop_df["latp"].values
survives = troop_df["surviv"].values
directions = troop_df["direc"].values
rows = troop_df.shape[0] 


# 2. create plots
fig, axes = plt.subplots(nrows=2, figsize=(25,12), gridspec_kw={"height_ratios":[4, 1]})

# [axes 0]
# 3. draw city
m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000, lon_0=31, lat_0=55, ax=axes[0])
m.drawcounties()
m.drawrivers()
m.drawparallels(range(54,58), labels=[True, False, False, False])
m.drawmeridians(range(23,55,2), labels=[False, False, False, True])
x,y = m(loncs, latcs)
for xi,yi,city_name in zip(x, y, city_names):
    axes[0].annotate(text = city_name, xy=(xi,yi), fontsize=14, zorder=2)

# 4. drew troop
x, y = m(lonps, latps)
for i in range(rows - 1):
    start_stop_lon = (x[i], x[i+1])
    start_stop_lat = (y[i], y[i+1])
    line_width = survives[i]
    if(directions[i] == "A"):
        line_color = "tan"
    else:
        line_color = "black"
    m.plot(start_stop_lon, start_stop_lat, line_color, linewidth=(line_width/10000),zorder=1)

# [axes 1]
# 5. draw temperature
temps_celsius = (temp_df["temp"]*5/4).astype(int)   #pandas series
annotaions = temps_celsius.astype(str).str.cat(temp_df["date"], sep="°C ")
lonts = temp_df["lont"].values
axes[1].plot(lonts, temps_celsius, linestyle = "dashed", color="black")
for lont, temp, annotation in zip(lonts, temps_celsius, annotaions):
    axes[1].annotate(annotation, xy=(lont-0.3, temp - 7), fontsize=10)

axes[1].set_ylim(-50, 10)
axes[1].spines["top"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].grid(True, which="major", axis="both")
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])
#set title
axes[0].set_title("Napoleon's disastrous Russian compaign of 1812", loc="center", fontsize=20)
plt.tight_layout()
#fig.savefig("minard_clone_basemap.png")
plt.show()
