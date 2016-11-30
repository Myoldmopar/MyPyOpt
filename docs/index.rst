.. MyPyOpt documentation master file, created by
   sphinx-quickstart on Mon Nov 28 13:13:50 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MyPyOpt's documentation!
===================================

This project is a very minimal optimization tool in Python.  The basis for this work was my own development in
an optimization course in grad school.  The original implementation was in Fortran, but I converted it to Python,
cleaned it up drastically, added tests and CI, docs, etc., and here it is.

The easiest way to see it in action is to check out the demos folder in the repository.  It has demonstrations that use
a simple Python function call as the simulation, and also one that pretends like it is calling EnergyPlus, both
then calibrating given specific decision variables and an objective to minimize.

Contents:

.. toctree::
   :maxdepth: 2

   DecisionVariable
   Exceptions
   InputOutput
   ObjectiveEvaluation
   OptimizationStructure
   Optimizer
   OptimizerHeuristicSearch
   ReturnStateEnum
   SearchReturnType

Index and tables
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

