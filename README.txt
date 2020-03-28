=============================================

Grainstat suite

=============================================

The grainstat suite is a suite of very simple scripts written in Python and originally designed to process grain size data of fine grained tsunami deposits samples, gathered from X-ray microtomography (see reference at the end of this readme). These scripts are meant to be easily and freely usable by anyone even on entry-level computers, using either Windows, Linux or Mac OSX. 


=============================================

Requirements

=============================================


- Python version:

  coded & tested with python 3.6.0 using Anaconda 4.3 and Pycharm Community Edition 2017 (recommended to edit the scripts if needed)

- Used modules:

  numpy
  scipy
  matplotlib
  tkinter
  easygui

  (to check if the modules are installed, type "pip freeze" (without the quotes) in the command line. If some are missing, here are the command lines to get a missing module :

	Linux : sudo apt-get install modulename

	Windows / OSX : pip install modulename 

	[pip is already installed with latest versions of python, but if needed, here's how to install pip : https://pypi.python.org/pypi/pip ])

- All scripts and colormaps must stay in the same file (unless the user manually modifies the paths in the scripts). Data files can be anywhere.


=============================================

Usable files

=============================================

- x, y, z tables, x being the abscissa of the particle, y its ordinate (depth) and z the grain size. Values must be in millimetres.

- The depth values (y column) must be negative and sorted from the highest to the lowest depth.
	
- Three columns, space or tab separated, saved as .csv, .txt or .xls.

	Example:

	  x        y      z

	6.734	-0.04	0.062
	3.313	-0.064	0.13
	11.794	-0.065	0.122
	15.708	-0.066	0.072
	6.466	-0.07	0.134
	1.217	-0.074	0.132
	5.589	-0.077	0.077
	5.45	-0.079	0.162
	6.883	-0.093	0.085
	7.179	-0.096	0.306
	8.737	-0.114	0.174
	2.257	-0.12	0.156
	9.497	-0.126	0.128
	13.115	-0.136	0.234
	17.171	-0.136	0.19


=============================================

Scripts description

=============================================


All scripts are commented, allowing the user to know which part of the scripts do what. While specialized editors such as PyCharm community allow an easy manipulation of the scripts, they can be opened and edited with any standard text editor, such as Notepad++, Microsoft notepad (Windows), Textedit (OSX), Notepadqq (Linux), etc.
Here are a few additionnal guidelines.


=> Map.py:


	- Grain size mapping script. Draws a map representing the size of the particles along the studied slice. 


	- The user has to enter the pixel size (vertical resolution of the scans in millimetres). This will define the calculation step on the map. Steps larger or smaller than the scans resolution can be entered, but larger step will most often only marginally increase processing speed and cost spatial resolution, while smaller steps will quickly make calculations a lot longer for no gain in precision. Entering the resolution of the scans is most often the best option.


	- The default colormap (colormap_jet) is designed to represent the smallest particles in hues of blue and the biggest in hues of red. It is devided into 64 different colors and is intended to represent grain size according to the Wentworth scale (the ticks on the colorbar correspond to the Wentworth scale steps: fine silts, coarse silts, very fine sands, fine sands, medium sands, coarse sands, very coarse sands). Additionnal ticks for the colorbar can be added easily by modifying line 31.


	- By default, the colormap colors will be distributed between the lowest and the higest values of the dataset, leaving no color unassigned regardless of the maximum and minimum grain size. This can be a problem if the user wants to have colors assigned to the same grain size value each time they run the script, or if the user needs to compare two different grain size maps. In this case, the colormap has to be normalized. This is done by uncommenting the last part of line 26:

	 CS = plt.contourf(XI, YI, ZI, 64, cmap=col.ListedColormap(datacustcmp))# ,norm=col.Normalize(vmin=0.016, vmax=0.500))

becomes: CS = plt.contourf(XI, YI, ZI, 64, cmap=col.ListedColormap(datacustcmp) ,norm=col.Normalize(vmin=0.016, vmax=0.500))

where vmin is the minimum grain size to take into account and vmax the maximum grain size (in millimetres). If grain sizes outside the range defined by vmin and vamx are present, they will be assigned the colors corresponding to the boundaries of the colormap (deep blue or deep red in the case of the colormap_jet colormap for instance). If they whole range defined by vmin and vmax is not represented in the dataset, some colors won't be assigned. The minimal and maximal grain size values can be known by using the Stats.py script (see below).


	- The user can select another colormap either by: 
		- modifying the colormap name in line 24 (default name : 'colormap_jet.txt')
		- uncommenting line 23 (erase the # sign at the beginning of the line) and commenting line 24 (put a # sign at the beginning of the line) in order to be able to manually select a colormap file each time the script is run.


	- The colormap must be in .txt, .csv ou .xls format, each line representing a color defined by three values : Red, Green and Blue values, scaled from 0 to 1 (check colormap_jet.txt for an example).
	

	- A basic greyscale colormap is available (colormap_greys.txt).




=> Stats.py:

	Calculation of statistics regarding grain size :
	Grains number
	Mean, maximum and minimum sizes
	D25 and D75
	Standard deviation
	Sorting index
	Kurtosis and Skewness

	The user has to enter the calculation step in millimetres. Smaller steps mean better vertical resolution but lower representativity (the calculations are conducted on less grains for each step). Check the grains number curve to ensure the calculations are conducted on enough particles.




=> Counting.py:

	Simplified version of Stats.py, retaining only the measurement of grains number at each step. Use it when only particles numbers (e.g. bioclasts or crystal countings along a slice) are useful and other measurements aren't needed.




=> Grainstat.py:

	Small script used to rapidly run one of the three other scripts. Not really useful but it can be convenient, so it exists.


=============================================

Improving the scripts

=============================================

I am not a programmer, which means that my programming skills are limited (to say the least). Corrections and improvements are most welcome. Feel free to modify the scripts according to your needs.

For questions and comments : s.falvard@opgc.univ-bpclermont.fr

These scripts are based on and improved from Matlab® scripts originally published in:

Falvard, S. & Paris, R., 2017. X-ray tomography of tsunami deposits: Towards a new depositional model of tsunami deposits. Sedimentology 64(2), 453-477.

DOI : http://dx.doi.org/10.1111/sed.12310