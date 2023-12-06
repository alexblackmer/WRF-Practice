from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
import cartopy.feature as cfeature

from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)

file_paths = [
    'data/wrfout_d01_2020-12-17_00:00:00',
    'data/wrfout_d01_2020-12-17_01:00:00',
    'data/wrfout_d01_2020-12-17_02:00:00',
    'data/wrfout_d01_2020-12-17_03:00:00',
    'data/wrfout_d01_2020-12-17_04:00:00',
    'data/wrfout_d01_2020-12-17_05:00:00',
    'data/wrfout_d01_2020-12-17_06:00:00',
    'data/wrfout_d01_2020-12-17_07:00:00',
    'data/wrfout_d01_2020-12-17_08:00:00',
    'data/wrfout_d01_2020-12-17_09:00:00',
    'data/wrfout_d01_2020-12-17_10:00:00',
    'data/wrfout_d01_2020-12-17_11:00:00',
    'data/wrfout_d01_2020-12-17_12:00:00',
    'data/wrfout_d01_2020-12-17_13:00:00',
    'data/wrfout_d01_2020-12-17_14:00:00',
    'data/wrfout_d01_2020-12-17_15:00:00',
    'data/wrfout_d01_2020-12-17_16:00:00',
    'data/wrfout_d01_2020-12-17_17:00:00',
    'data/wrfout_d01_2020-12-17_18:00:00',
    'data/wrfout_d01_2020-12-17_19:00:00',
    'data/wrfout_d01_2020-12-17_20:00:00',
    'data/wrfout_d01_2020-12-17_21:00:00',
    'data/wrfout_d01_2020-12-17_22:00:00',
    'data/wrfout_d01_2020-12-17_23:00:00',
    'data/wrfout_d01_2020-12-18_00:00:00',
]

# Open the NetCDF file
ncfile = Dataset(file_paths[0])
# Get the snow acc
snowncStart = getvar(ncfile, "SNOWNC")
# Get the latitude and longitude points
lats, lons = latlon_coords(snowncStart)
# Get the cartopy mapping object
cart_proj = get_cartopy(snowncStart)


snow_cover = None
for file_path in file_paths:
    wrf_file = Dataset(file_path)

    # Assuming your snow variable is 'SNOWNC', change this accordingly
    snownc = getvar(wrf_file, 'SNOWNC', timeidx=0, meta=False)

    if snow_cover is None:
        snow_cover = snownc
    else:
        snow_cover += snownc

# Calculate average snow cover from the 24 files
snow_cover_avg = snow_cover / len(file_paths)

# Create a figure
fig = plt.figure(figsize=(12,6))
# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)

# Download and add the states and coastlines

ax.add_feature(cfeature.STATES, linewidth=.5, edgecolor="black")
ax.coastlines('50m', linewidth=0.8)

# Make the contour outlines and filled contours for the smoothed sea level
# pressure.
plt.contour(to_np(lons), to_np(lats), to_np(snow_cover_avg), 10, colors="black",
            transform=crs.PlateCarree())
plt.contourf(to_np(lons), to_np(lats), to_np(snow_cover_avg), 10,
             transform=crs.PlateCarree(),
             cmap=get_cmap("winter"))

# Add a color bar
plt.colorbar(ax=ax, shrink=.98)

# Set the map bounds
ax.set_xlim(cartopy_xlim(snowncStart))
ax.set_ylim(cartopy_ylim(snowncStart))

# Add the gridlines
ax.gridlines(color="black", linestyle="dotted")

plt.title("D01 24-hr New Snow Cover (mm)")
plt.xlabel("Date: 2020-12-17")

# Show plot
plt.savefig("WRF-d01-SNOWNC.png")