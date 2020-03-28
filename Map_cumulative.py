# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import easygui as g
import matplotlib.pyplot as plt
import matplotlib.colors as col
from scipy.interpolate import griddata

############ Data import ############

m = g.fileopenbox(msg="select the data file (must be in .txt format)")
# importation of the .txt datafile (three column, x, y and z, separated by spaces)
M = np.loadtxt(m)  # loading of the data contained in the file
step = 0.1  # TODO: à enlever
#step = float(g.enterbox(msg="Enter map resolution (millimetres)"))  # definition of the map calculation step

############ Map calculation ############

x, y, z = M.T  # translation of the arrays: x, y and z become lines instead of columns
xmin = int(min(x))
xmax = round(max(x))
ymin = int(min(y))
ymax = round(max(y))
X = np.arange(xmin, xmax, step)  # definition of the size and step of the new regular grid along the X axis
Y = np.arange(ymin, ymax, step)  # idem along the Y axis
XI, YI = np.meshgrid(X, Y)  # making of a regular grid from X and Y arrays values
ZI = griddata((x, y), z, (XI, YI), method='linear')  # Interpolation of new ZI values from the original z values. ZI values are calculated at each [XI, YI] point of the regular grid
"""
for test purposes only (colorbar ticks) 
print(min(z))
print(max(z))
"""

############ Stats calculation ############

stepStat = 0.5  # TODO: step definition enterbox
yStatsMax = max(y)  # ymax = max value inside list y
yStatsMin = min(y)  # ymin = min value inside list y
zStatsMaxI = np.size(z)  # zmaxI = size (number of elements inside) of the z list
ycalc = ymax - stepStat  # todo : MODIF
k = stepStat  # used to increment the while loop and go through the whole sequence of values
results_array = []  # (creation of an empty array, to be filled later with the calculation results)

while yStatsMin + k <= (ymax + stepStat):  # as long as this statement is true, the following occur:
    j = k - stepStat
    ya = yStatsMax - j
    yb = yStatsMax - k
    ida = (np.abs(y - ya)).argmin()  # ida = the value in the y list which is the closest (argmin) to ya
    # (absolute value of y - ya)
    idb = (np.abs(y - yb)).argmin()  # idb = idem for yb
    zmes = z[ida:idb]  # zmes = array containing the values of z associated to the ida to idb values
    clay = []
    silt = []
    sand = []
    gravel = []

    for grain in zmes:
        if grain < 0.040:
            clay.append(grain)
        elif grain < 0.062:
            silt.append(grain)
        elif grain < 2.000:
            sand.append(grain)
        else:
            gravel.append(grain)
        if (len(clay) + len(silt) + len(sand) + len(gravel)) > 0:
            claypercent = len(clay) / (len(clay) + len(silt) + len(sand) + len(gravel)) * 100
            siltpercent = len(silt) / (len(clay) + len(silt) + len(sand) + len(gravel)) * 100
            sandpercent = len(sand) / (len(clay) + len(silt) + len(sand) + len(gravel)) * 100
            gravelpercent = len(gravel) / (len(clay) + len(silt) + len(sand) + len(gravel)) * 100
        else:
            claypercent = 0
            siltpercent = 0
            sandpercent = 0
            gravelpercent = 0
    start = ymax - k + stepStat
    results_array.append([start, claypercent, siltpercent, sandpercent, gravelpercent])
    k = k + stepStat

r = np.array(results_array)

categories = ['clay', 'silt', 'sand', 'gravel']
resultsToPlot = {
    'start': r[:, 0],
    'clay': r[:, 1],
    'silt': r[:, 2],
    'sand': r[:, 3],
    'gravel': r[:, 4],
}

############ Plotting ############
### grainsize map

plt.subplot(1, 2, 1)

#customcolorbase = g.fileopenbox(msg='colormap.txt') # optional: select a colormap
customcolorbase = open('colormap_jet.txt','r')  # definition of the colormap used in the plot from a .txt datafile containing RGB values (in 0 to 1 floats)
datacustcmp = np.loadtxt(customcolorbase)
CS = plt.contourf(XI, YI, ZI, 64, cmap=col.ListedColormap(datacustcmp), norm=col.Normalize(vmin=min(z), vmax=max(z)))  # contour map of interpolated grain size ZI along the grid, using 64 contour steps (as many steps in the contour as in the colormap)
plt.xlim(xmin, xmax)  # limits of the plot along x
plt.ylim(ymin, ymax)  # idem along y
plt.axis('scaled')  # plotting of the map, with the same scale for x and y axes
plt.colorbar(orientation='vertical', shrink=1.0, fraction=0.5, aspect=30,
             ticks=[0.016, 0.031, 0.062, 0.125, 0.250, 0.500, max(z)])
plt.clim(vmin=min(z), vmax=max(z))
plt.ylabel('Depth (mm)')
plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

### Cumulative bar chart
print(r)

plt.subplot(1, 2, 2)
p1 = plt.barh(r[:, 0], r[:, 1], height=stepStat, left=0, align='edge')
p2 = plt.barh(r[:, 0], r[:, 2], height=stepStat, left=r[:, 1], align='edge')
p3 = plt.barh(r[:, 0], r[:, 3], height=stepStat, left=(r[:, 1] + r[:, 2]), align='edge')
p4 = plt.barh(r[:, 0], r[:, 4], height=stepStat, left=(r[:, 1] + r[:, 2] + r[:, 3]), align='edge')
plt.ylim(ymin, ymax)

plt.show()
