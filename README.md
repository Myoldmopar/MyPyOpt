# MyPyOpt
Python version of my simple optimization app from school

## Source
These are based on my optimization class from grad school.

## Documentation [![](https://readthedocs.org/projects/solar-calculations/badge/?version=latest)](http://solar-calculations.readthedocs.org/en/latest/)
Documentation is hosted on [ReadTheDocs](http://solar-calculations.readthedocs.org/en/latest/).  The functions are all documented with Markdown syntax doc strings in a way that Sphinx can interpret them.  To build the documentation, enter the docs/ subdirectory and execute `make html`; then open `/docs/_build/html/index.html` to see the documentation.

## Testing [![](https://travis-ci.org/Myoldmopar/SolarCalculations.svg?branch=master)](https://travis-ci.org/Myoldmopar/SolarCalculations)
The source is tested using the python unittest framework.  To execute all the unit tests, just execute the test file (since it calls `unittest.main()`): `python test/test_solar.py`.  The tests are also executed by [Travis CI](https://travis-ci.org/Myoldmopar/SolarCalculations).

## Validation
The code has been carefully compared against numerous sampled points in the unit tests, and also [against EnergyPlus output](https://github.com/Myoldmopar/SolarCalculations/wiki/CompareToEnergyPlus), to ensure accurate values are being calculated.  If you find something wrong, just [file an issue](https://github.com/Myoldmopar/SolarCalculations/issues/new)!

## Demonstration
In order to show how to use the library, a [demonstration page](https://github.com/Myoldmopar/SolarCalculations/wiki/DemoSolarAngles) was created, that is based on the source in the demos/ folder.
