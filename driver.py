import sys
import os
import shutil
import subprocess
import unittest
from test import test_main


valid_args = ['test', 'clean_projects', 'usage', 'docs']


def usage():
    print("Usage: call with one of the following arguments:")
    for arg in valid_args:
        print("  " + sys.argv[0] + " " + arg)

if len(sys.argv) != 2:
    print("Error: Must call with 1 command line argument!")
    usage()
    sys.exit(1)
elif sys.argv[1] == valid_args[0]:
    suite = unittest.TestLoader().loadTestsFromTestCase(test_main.TestQuadratic)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0)
elif sys.argv[1] == valid_args[1]:
    print("I'll delete this folder: " + os.path.join(os.path.dirname(os.path.realpath(__file__)), "projects"))
    shutil.rmtree(os.path.join(os.path.dirname(os.path.realpath(__file__)), "projects"))
    sys.exit(0)
elif sys.argv[1] == valid_args[2]:
    usage()
    sys.exit(0)
elif sys.argv[1] == valid_args[3]:
    subprocess.call(['make', '-C', 'docs', 'html'])
    sys.exit(0)
else:
    print("Error: Invalid command line argument passed in!")
    usage()
    sys.exit(1)
