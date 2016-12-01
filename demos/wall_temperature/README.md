This demonstrates a very simple calibration using an external "program".  The optimization is set up with:

 - A single decision variable, called `wall_resistance`, which makes this a 1D search.
 - Standard project settings otherwise
 - A simulation callback function that executes an external program, called `calculate_wall_temperature.py`.  This program simply reports out a heat transfer rate for the wall.  **Yes I know the naming here is bad**.  The callback then retrieves the value from the program and return it.
 - An objective function callback that calculates the squared error between the "known" heat transfer rate, and the calculated version.
 
 To execute, just run the `optimize_resistance.py` file and it will run, putting the results in a projects/ subdirectory of your current working directory.
