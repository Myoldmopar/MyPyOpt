#!/usr/bin/python

import json
from typing import List, Tuple


def pretend_e_plus(pretend_idf_contents: str) -> List[Tuple[int, float]]:
    # read the in.json file
    input_data = json.loads(pretend_idf_contents)
    resistance = float(input_data['wall_properties']['resistance'])
    min_out_temp = float(input_data['outdoor_temps']['minimum'])

    # run 24 hours, calculating surface temperature and storing it
    zone_temp = 23  # Celsius
    conv_coeff = 3  # W/m2K

    # set up the outdoor temp modifier array
    temp_adder = [0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 6, 8, 10, 12, 13, 14, 13, 11, 9, 8, 6, 4, 2, 1]

    # output data to column 2 in out.csv
    output_csv = []
    for i in range(1, 25):
        current_outdoor_temp = min_out_temp + temp_adder[i - 1]
        surf_temp = (current_outdoor_temp / resistance + zone_temp * conv_coeff) / (conv_coeff + 1 / resistance)
        output_csv.append((i, surf_temp))
    return output_csv
