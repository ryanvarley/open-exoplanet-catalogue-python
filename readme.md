# ExoData
[![Build Status](https://api.travis-ci.org/ryanvarley/ExoData.png?branch=master)](https://travis-ci.org/ryanvarley/ExoData)
[![Documentation Status](https://readthedocs.org/projects/exodata/badge/?version=latest)](http://exodata.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/ryanvarley/ExoData/badge.svg)](https://coveralls.io/r/ryanvarley/ExoData)

This python interface (formerly oecpy) serves as a link between the raw XML of the [Open Exoplanet Catalogue](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue). It allows:

* Searching of planets (including alternate names)
* Easy reference of planet parameters ie GJ1214b.ra, GJ1214b.T, GJ1214b.R
* Calculation of values like the transit duration.
* Define planet types and query planets to find out what they are
* Easy rescale of units
* Easily navigate hierarchy (ie from planet to star or star to planets)
* Availability of system parameters in planets (ie ra, dec, d (distance))

If you use ExoData in a scientific publication, please include a reference to this paper [http://dx.doi.org/10.1016/j.cpc.2016.05.009](http://dx.doi.org/10.1016/j.cpc.2016.05.009).

# Documentation

Full documentation is currently being built [here](http://exodata.readthedocs.io/en/latest/).
For now this page and the [ExoData paper](http://dx.doi.org/10.1016/j.cpc.2016.05.009) are the best sources.

# Installation
This module depends on

* [Quantities](https://github.com/python-quantities/python-quantities)
* [numpy](http://www.numpy.org/)
* nose
* matplotlib
* requests
* hypothesis
* [Open Exoplanet Catalogue](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue) (somewhere on your system)

**Currently only tested under Python 2.7, 3.4, 3.5 on mac and linux**. If you use windows or a different python version try it anyway and open an issue if you encounter problems.

Easiest way

`pip install exodata`

Or from this repo

    python setup.py install

You can either download and manage the Open Exoplanet Catalogue yourself or automatically load the latest version from the web each time.

To get your own copy move to the folder on your system where you want to store it and clone the Open Exoplanet Catalogue (this process will create a folder named open-exoplanet-catalogue within your working directory).

    git clone https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue.git

The catalogue should then download. If you want to update the catalogue, move to the open_exoplanet_catalogue folder and pull

    cd open_exoplanet_catalogue/
    git pull origin master

If you want to keep track of this repo in a GUI way, I recommend [sourcetree](http://www.sourcetreeapp.com/) or the [github client](https://help.github.com/articles/set-up-git).

# Usage

This section was generated using the OEC version dc8c08a4ba0c64dd039e96c801d12f17c82a7ff3 (1st May 2016)

	import exodata
	databaseLocation = '/git/open_exoplanet_catalogue/systems/' # Your path here (to systems folder)
	exocat = exodata.OECDatabase(databaseLocation)

	# To automatically load the latest version from github you can instead use load_db_from_url() which fetches
	# the latest version from https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz
	exocat = exodata.load_db_from_url()

You can then access the lists

	exocat.systems
	exocat.stars
	exocat.planets
	exocat.transitingPlanets

The following code assumes the imports (along with loading exocat as above)

    import exodata
    import exodata.astroquantities as aq

You can now perform more advanced queries such as fetching all planets whose radius is less than 10 Earth Radii

	>>> superEarths = [planet for planet in exocat.planets if planet.R < (10 * aq.R_e)]
	>>> len(superEarths)
	1096

To choose a planet

	>>> kepler60b = exocat.searchPlanet('kepler60b')
	>>> print kepler60b
	Planet('Kepler-60 b')

	>>> exocat.searchPlanet('kepler60')  # or all the kepler 60 planets
	[Planet('Kepler-60 c'), Planet('Kepler-60 b'), Planet('Kepler-60 d')]

	>>> kepler60b.star  # to get the star kepler-60
	Star('Kepler-60')

	>>> kepler60b.R  # to get the planetary radius
	array(0.196) * R_j  # this works like an array in most functions

	>>> kepler60b.R.rescale(aq.R_e) # See Units section for more
	array(2.150770051797206) * R_e

	>>> kepler60b.R.rescale(aq.m)
	array(13702556.0) * m

	>>> kepler60b.dec
	<Latitude 42.265011111111114 deg>

	>>> kepler60b.dec.dms  # or in degrees, minutes and seconds
	dms_tuple(d=42.0, m=15.0, s=54.040000000011901)

	>>> gj1214b = exocat.searchPlanet('gj1214')
	Planet('Gliese 1214 b')

	>>> exocat.planetDict['Gliese 1214 b']  # or with the exact name
	Planet('Gliese 1214 b')

For a full list of planets, star and system parameters see Appendix B (pg 16-19) of the [ExoData paper](http://arxiv.org/pdf/1510.02738v1.pdf).

# Units
units are handled by the quantities package
`import quantities as pq`

You can then access most units and constants such as meters pq.m, astronomical units pq.au etc!

Some astronomy units such as R_e, R_j, R_s (where e is Earth, j is Jupiter and s in the Sun) are not included (yet) in quantities so you need to refer to them as aq.R_e by importing exodata.astroquantities

	import exodata.astroquantities as aq

exodata.astroquantities includes all pq units so only the *aq* import is necessary

There are also other units such as mass (M_e, M_s and M_j).

You can read more about the Quantities package [here](https://github.com/python-quantities/python-quantities).

# Equations

The equations module contains many exolanet equations that be be used independantly or called directly from a planet or star object. Most equations are classes that when given all parameters bar one will calculate the missing one.

	>>> from exodata.equations import KeplersThirdLaw
	>>> KeplersThirdLaw(a=0.01488*aq.au, M_s=0.176*aq.M_s).P
	array(1.579696141940911) * d

	>>> KeplersThirdLaw(a=0.015*aq.au, P=1.58*aq.d).M_s
	array(0.18022315673929148) * M_s

	>>> gj1214b = exocat.planetDict['Gliese 1214 b']
	>>> gj1214b.calcSurfaceGravity()
	array(7.929735778087916) * m/s**2

	>>> gj1214b.calcLogg()
	2.8992587166958947

	>>>> gj1214b.calcTransitDuration(circular=True)
	array(52.74732533968579) * min

# Assumptions

These are how a planet is classified acoridng to mass, radius and temperature along with assumptions for the albedo and mean molecular weight based on these parameters. Currently they are stored in the dictionary `exodata.assumptions.planetAssumptions`.

Overwriting these values (or adding new ones) will change the output. for example, looking at the mass types we can see a list defining the limits. Editing this list to change the values or add new classes will chnage how planet are classified in the program.

	>>> exodata.assumptions.planetAssumptions['massType']
	[(array(10.0) * M_e, 'Super-Earth'), (array(20.0) * M_e, 'Neptune'), (inf, 'Jupiter')]

# ExoData Global Parameters
A few options can be set within ExoData to change the global behaviour of the program. By default if a quantity is missing for a parameter it is calculated if possible. For example if you use .a for the semi-major axis and it is not present in the catalogue it will be calculated using the period and stellar mass and returned. This happens silently except for raising the `Calculated SMA` flag. (see flags). You can turn this behaviour off by typing

	exodata.params.estimateMissingValues = False

This will only take scope in the current project so if you close the interpreter it will reset to True.

# Plotting

ExoData features a plotting library for planet and stellar parameters in a scatter plot and per parameter bin. Please see the [plots section](https://github.com/ryanvarley/open-exoplanet-catalogue-python/wiki/Plotting) of the documentation for further information. Note that all plots are shown here were produced after `import seaborn` which changes the plot style.

Note if you want to replicate these plots in the default python interpretor you will need to **import pyplot and issue the show command after each plotting code** shown below. You will also need to close the open plot before typing any further commands.

	import matplotlib.pyplot as plt
	plt.show()

### Discovery Method by Year

```python
dm_plot = exodata.plots.DiscoveryMethodByYear(exocat.planets, methods_to_plot=('RV', 'transit', 'Other'))
dm_plot.plot(method_labels=('Radial Velocity', 'Transit Method', 'Other'))
```
![Discovery method by year](https://github.com/ryanvarley/ExoData/blob/images/discovery_year_method_v2.png?raw=true "Discovery method by year")

### Planet Mass with Planet Radius
```python
exodata.plots.GeneralPlotter(exocat.planets, 'R', 'M', yaxislog=True).plot()
plt.xlim(0, 2.5)
```
![Planet Mass with Planet Radius](https://github.com/ryanvarley/ExoData/blob/images/planetR-M_v5.png?raw=true "Planet Mass with Planet Radius Plot")

### Stellar V Magnitude with Planet Radius
```python
exodata.plots.GeneralPlotter(exocat.planets, 'R', 'star.magV',
                            xunit=aq.R_e, xaxislog=True).plot()
```

![Stellar V Magnitude with Planet Radius](https://github.com/ryanvarley/ExoData/blob/images/planetR-starMagV_v5.png "Stellar V Magnitude with Planet Radius Plot")

### Planet Eccentricity
```python
exodata.plots.DataPerParameterBin(exocat.planets, 'e',
      (0, 0, 0.05, 0.1, 0.2, 0.4, float('inf'))).plotBarChart(label_rotation=45)
```
![Planet Eccentricity](https://github.com/ryanvarley/ExoData/blob/images/exodata-orbital-eccentricity_v5.png "Planet Eccentricity Plot")

You can also plot this as a pie chart

```python
exodata.plots.DataPerParameterBin(exocat.planets, 'e',
      (0, 0, 0.05, 0.1, 0.2, 0.4, float('inf'))).plotPieChart()
```

![Planet Eccentricity](https://github.com/ryanvarley/ExoData/blob/images/exodata-orbital-eccentricity-pie_v6.png?raw=true "Planet Eccentricity Pie Chart")

Plots can also be large (i.e. for presentations), and you can change the color easily with normal *matplotlib* syntax

```python
exodata.plots.DataPerParameterBin(exocat.planets, 'M',
    (0, 0.2, 0.5, 1, 2, 3, 6, 12, float('inf')), size='large').plotBarChart(c='r')
```
![Planet Eccentricity](https://github.com/ryanvarley/ExoData/blob/images/exodata-orbital-eccentricity-large_v5.png?raw=true "Planet Eccentricity Plot Large")

# Licence

MIT License

Copyright (c) 2016 Ryan Varley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
