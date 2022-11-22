This demonstrates a calibration against time-series data using a pretend version of EnergyPlus.  While the actual EnergyPlus program takes an idf file, this pretend version takes a simple json file for convenience.  Like EnergyPlus, it can report out a csv file of time series results.  A JSON template is included in the directory, which is how I expect one would use this with an actual EnergyPlus IDF template.  The template is then modified with current parameter values and rewritten to the expected input file name before calling the pretend EnergyPlus program.  This EnergyPlus program simply takes a couple inputs, runs a full 24 hour simulation, updating the outdoor temperature, and calculating the interior surface temperature, and reporting that as the only output.

The optimization is set up with:

 - Two decision variables:
   - The first, called `wall_resistance`
   - And a second, called `min_outdoor_temp`
 - Standard project settings otherwise
 - A simulation callback function that executes the pretend EnergyPlus, called `pretend_energyplus.py`.  This reports out a csv file with 24 rows of hourly data, with 2 columns: an hour index, and the interior surface temperature.
 - An objective function callback that calculates the sum of squared errors between the "known" surface temperature at each hour and the calculated value at each hour.  The "known" surface temperature data is fuzzy with a small randomized multiplier applied to make it appear more like "measured" data.
 
To execute, just run the `calibrate_walltemperatures.py` file and it will run, putting the results in a projects/ subdirectory of your current working directory.
