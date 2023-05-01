#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 09:09:07 2020

@author: hagen
"""

import numpy as np
from matplotlib import pyplot as plot

def digtizer_data(file_name):
    with open(file_name, mode='r') as data:
        numbers = list()
        for line in data.read().splitlines():
            numbers.append(line.split())
        values = np.array(numbers).astype(np.float64)
    return values

def watchpoint_data(file_name, position = 5):
    with open(file_name, mode='r') as data:
        numbers = list()
        for line in data.read().splitlines():
            numbers.append(line.split())
        value_names = numbers.pop(0)
        values = np.array(numbers).astype(np.float64)

    selection = np.zeros((values.shape[0], 2))
    selection[:,0] = values[:,0]
    selection[0,1] = values[0,position]
    for i, val in enumerate(values):
        selection[i,1] = selection[i-1,1] + val[position]
    return selection

plot.title('Absolut Y-Position of movingWall')
plot.xlabel('t')
plot.ylabel('Y')
plot.rc('grid', linestyle="dotted", color='grey')
plot.grid()

#displacement = digtizer_data('previous_work')
#plot.plot(displacement[:,0], displacement[:,1], label='previous', linestyle='--')

displacement = digtizer_data('max_displacement_y')
plot.plot(displacement[:,0], displacement[:,1], label='Fluid_Solid_oneway')

#displacement = watchpoint_data('precice-Structure_Solver-watchpoint-point1.log')
#plot.plot(displacement[:,0], displacement[:,1], label='current')

# plot.xlim(0, 5)
#plot.ylim(-0.04, 0.04)
plot.legend()
plot.savefig('flap-trailingedge-displacement.svg')
plot.show()

