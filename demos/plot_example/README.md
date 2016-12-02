This demonstrates the creation of a graphical interface that shows the status and progress of convergence.

Before running, make sure you have matplotlib installed!  It is listed in the requirements.txt file, so you can pip install -r requirements.txt.

The optimization is set up with:
 - Three decision variables, which are actually the terms A, B, and C, in the equation A + Bx + Cx^2
 - Standard project settings otherwise
 - A simulation callback function that evaluates the polynomial at the current coefficient values, for a range of X values.
 - An objective function callback that compares the evaluated function values and the known polynomial evaluated values and returns the sum of squared error between them.

To execute, just run the `main.py` file and it will run, showing the convergence in a Tk window.
