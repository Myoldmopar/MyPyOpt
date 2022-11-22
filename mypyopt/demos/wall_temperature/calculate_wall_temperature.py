#!/usr/bin/python

def calculate_wall_temp(resistance_value: float):
    outdoor_temp = 20
    indoor_temp = 10
    return (outdoor_temp - indoor_temp) / resistance_value
