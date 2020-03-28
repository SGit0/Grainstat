# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import easygui as g
import scipy.stats as stat
import matplotlib.pyplot as plt
import csv
from tkinter import filedialog, Tk


m = g.fileopenbox(msg="select the data file (.txt format)")  # importation of the .txt datafile
# (three column, x, y and z, separated by blanks)

M = np.loadtxt(m)  # loading of the data contained in the file
s = g.enterbox(msg="Enter the calculation step (mm)")  # definition of vertical step used to calculate the statistics
step = float(s)  # conversion of the string obtained in s in a float type number
x, y, z = M.T  # translation of the arrays: x, y and z become lines instead of columns
ymax = max(y)  # ymax = max value inside list y
ymin = min(y)  # ymin = min value inside list y
zmaxI = np.size(z)  # zmaxI = size (number of elements inside) of the z list
ycalc = ymin + step
k = step  # used to increment the while loop and go through the whole sequence of values
resultats = []  # (creation of an empty "resultats" array, to be filled later)

while ymin+k <= ymax:  # as long as this statement is true, the following occur:
    j = k - step
    ya = ymin + j
    yb = ymin + k
    ida = (np.abs(y - ya)).argmin()  # ida = the value in the y list which is the closest (argmin) to ya
    # (absolute value of y - ya)
    idb = (np.abs(y - yb)).argmin()  # idb = idem for yb
    zmes = z[idb:ida]  # zmes = array containing the values of z associated to the ida to idb values

    if zmes.size == 0:  # if zmes doesn't contain any value (i.e no particle in the analysed depth step)
        znum = 0
        zmin = 0
        zmax = 0
        zmoy = 0
        zstd = 0
        meandepth = ymin + k - step / 2  # calculation of the mean depth of the subsample (depth of the upper boundary
        # minus half of the measurement step)
        d25 = 0
        d75 = 0
        d50 = 0
        so = 1
        zkurt = 0
        zskew = 0
        resultats.append([meandepth, znum, zmin, zmax, zmoy, zstd, so, d25, d75, zkurt, zskew])  # add all the values
        # to the 'resultats' array
        k = k + step  # incrementation of k by the step value at the end of the loop

    else:
        znum = len(zmes)  # znum = length of the zmes list
        zmin = min(zmes)
        zmax = max(zmes)
        zmoy = np.mean(zmes)  # calculation of the mean value
        zstd = np.std(zmes)  # calculation of the standard deviation
        meandepth = ymin + k - step/2  # calculation of the mean depth of the subsample (depth of the upper boundary
        # minus half of the measurement step)
        # Calculation of D25 and D75
        zperc = sorted(zmes)  # sort the zmes list by ascending order
        resultd25 = int(0.25*znum)  # take the value corresponding to 25% of the length of the sorted list
        d25 = zperc[resultd25]  # d25 corresponds to the value with an index value of 'resultd25' inside the zperc list
        resultd75 = int(0.75*znum)  # idem for d75
        d75 = zperc[resultd75]
        resultd50 = int(0.50*znum)
        d50 = zperc[resultd50]

        so = np.sqrt(d75/d25)  # Sorting coefficient

        zkurt = stat.kurtosis(zmes)  # Kurtosis

        # zskew = stat.skew(zmes)  # Skewness
        zskew = (d25+d75-2*d50)/2

        resultats.append([meandepth, znum, zmin, zmax, zmoy, zstd, so, d25, d75, zkurt, zskew])  # add all the results
        # from the previous calculation to the 'resultats' array

        k = k + step  # incrementation of k by the step value at the end of the loop

r = np.array(resultats)  # association of the values in the 'resultats' array to the 'r' value
meandepth = r[:, 0]  # mean depth measurements are retrieved from all the lines (:) of the first column (0) in 'r'
znum = r[:, 1]  # etc
zmin = r[:, 2]
zmax = r[:, 3]
zmoy = r[:, 4]
zstd = r[:, 5]
so = r[:, 6]
d25 = r[:, 7]
d75 = r[:, 8]
zkurt = r[:, 9]
zskew = r[:, 10]

plt.figure()  # creation of a new figure
plt.plot(znum, meandepth, 'k-')  # plot of znum (x) against mean depth (y), in the form of a black line ('k-')
plt.ylabel('Depth')
plt.xlabel('Number of particles')
plt.draw()

plt.figure()
plt.plot(zmin, meandepth, 'k-')
plt.plot(zmax, meandepth, 'k-')
plt.plot(zmoy, meandepth, 'k-.', label='mean')
plt.plot(zstd, meandepth, 'k--', label='standard dev')
plt.ylabel('Depth')
plt.xlabel('Grain size (mm)')
plt.legend(loc='upper right')
plt.draw()

plt.figure()
plt.plot(d25, meandepth, 'k-.', label='d25')
plt.plot(d75, meandepth, 'k-', label='d75')
plt.ylabel('Depth')
plt.xlabel('Grain size (mm)')
plt.legend(loc='upper right')
plt.draw()

plt.figure()
plt.plot(so, meandepth, 'k-')
plt.ylabel('Depth')
plt.xlabel('Sorting')
plt.draw()

plt.figure()
plt.plot(zkurt, meandepth, 'k-')
plt.ylabel('Depth')
plt.xlabel('Kurtosis')
plt.draw()

plt.figure()
plt.plot(zskew, meandepth, 'k-')
plt.ylabel('Depth')
plt.xlabel('Skewness')
plt.draw()

plt.show()  # show all figures

root = Tk()
root.withdraw()
s = g.ynbox(msg="Would you like to save the results ?")
if s:
    t = filedialog.asksaveasfilename(title="Select file", defaultextension='*.csv',
                                     filetypes=(("csv file", "*.csv"), ("excel file", "*.xls"),
                                                ("text file", "*.txt"), ("all files", "*.*")))
    # t = g.filesavebox(msg="Enter file name", filetypes=["*.csv", "*"])
    with open(t, 'w', newline='') as u:
        writer = csv.writer(u, dialect='excel-tab')
        writer.writerow(["Mean depth (mm)", "particles number", "Min grain size(mm)", "Max grain size(mm)",
                         "Mean grain size (mm)", "Standard deviation", "Sorting coefficient", "D25 (mm)", "D75 (mm)",
                         "Kurtosis", "Skewness"])
        writer.writerows(r)
