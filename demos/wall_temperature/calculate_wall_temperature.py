#!/usr/bin/python

import sys

outdoor_temp = 20
indoor_temp = 10
resistance_value = float(sys.argv[1])
q_calculated = (outdoor_temp - indoor_temp)/resistance_value

print(q_calculated)