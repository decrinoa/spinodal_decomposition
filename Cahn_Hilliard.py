# -*- coding: utf-8 -*-
"""

Created on Thu Oct  10 13:08:11 2024

@author: decrinoa

"""

import numpy as np

#flunctuation of the concentration generated randomly in every point of the system
def add_fluctuation(Nx, Ny, c0, noise):
    np.random.seed(24)
    return c0 + noise * (0.5 - np.random.rand(Nx,Ny))

def chemical_potential(c, A):
    return 2 * A * (c * ((1 - c) ** 2) - (c ** 2) * (1 -c))

#c_top, c_bot, c_lef, c_rig necessary to ensure the periodic boundary condition
def my_laplacian(c, dx, dy):
    Ny, Nx = c.shape
    c_top = np.vstack((c[-1, :], c[:-1, :]))                #Top bc
    c_bot = np.vstack((c[1:, :], c[0, :]))                  #bottom bc
    c_lef = np.hstack((c[:, -1][:, np.newaxis], c[:, :-1])) #left bc, [:, np.newaxis] ensure c[:, -1] is 2D
    c_rig = np.hstack((c[:, 1:], c[:, 0][:, np.newaxis]))   #rigth bc, [:, np.newaxis] ensure c[:, -1] is 2D
    
    return (c_top + c_bot + c_rig + c_lef - 4 * c) / (dx * dy)