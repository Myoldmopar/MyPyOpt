from unittest import TestCase

from mypyopt.demos.pretend_energyplus.calibrate_walltemperatures import run as run_pretend_ep
from mypyopt.demos.wall_temperature.optimize_resistance import run as run_wall_temp


class TestDemos(TestCase):
    def test_pretend_energyplus(self):
        run_pretend_ep()

    def test_wall_temp(self):
        run_wall_temp()
