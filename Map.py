# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import easygui as g
import matplotlib.pyplot as plt
import matplotlib.colors as col
from scipy.interpolate import griddata

m = g.fileopenbox(msg="select the data file (must be in .txt format)")
# importation of the .txt datafile (three column, x, y and z, separated by spaces)
M = np.loadtxt(m)  # loading of the data contained in the file
s = g.enterbox(msg="Enter map resolution (in millimetres)")  # definition of the map calculation step
step = float(s)
x, y, z = M.T  # translation of the arrays: x, y and z become lines instead of columns
xmin = int(min(x))
xmax = round(max(x))
ymin = int(min(y))
ymax = round(max(y))
print(min(z))
print(max(z))
X = np.arange(xmin,xmax,step)  # definition of the size and step of the new regular grid along the X axis
Y = np.arange(ymin, ymax, step)  # idem along the Y axis
XI, YI = np.meshgrid(X, Y)  # making of a regular grid from X and Y arrays values
ZI = griddata((x, y), z, (XI, YI), method='linear')  # Interpolation of new ZI values from the original z values. ZI values are calculated at each [XI, YI] point of the regular grid


#customcolorbase = g.fileopenbox(msg='colormap.txt')
customcolorbase = open('colormap_jet.txt','r')  # definition of the colormap used in the plot from a .txt datafile containing RGB values (in 0 to 1 floats)
datacustcmp = np.loadtxt(customcolorbase)
CS = plt.contourf(XI, YI, ZI, 64, cmap=col.ListedColormap(datacustcmp) ,norm=col.Normalize(vmin=min(z), vmax=max(z)))  # contour map of interpolated grain size ZI along the grid, using 64 contour steps (as many steps in the contour as in the colormap)
plt.xlim(xmin, xmax)  # limits of the plot along x
plt.ylim(ymin, ymax)  # idem along y
plt.axis('scaled')  # plotting of the map, with the same scale for x and y axes
plt.colorbar(orientation='vertical', shrink=1.0, fraction=0.5, aspect=30,
            ticks=[0.016, 0.031, 0.062, 0.125, 0.250, 0.500, max(z)])
plt.clim(vmin=min(z), vmax=max(z))
plt.ylabel('Depth (mm)')
plt.tick_params(axis='x',which='both', bottom='off', top='off', labelbottom='off')
plt.show()
