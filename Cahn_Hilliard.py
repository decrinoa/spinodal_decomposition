# -*- coding: utf-8 -*-
"""

Created on Thu Oct  10 13:08:11 2024

@author: decrinoa

"""

import numpy as np

def add_fluctuation(Nx, Ny, c0, noise):
    """
    This function generates a 2D matrix of size (Nx, Ny) representing concentration values.
    Each value is perturbed by a random noise term, which is uniformly distributed around the base concentration 'c0',
    between -noise*0.5 and +noise*0.5.

    Parameters:
    ----------
    Nx : The number of columns in the concentration matrix.
       
    Ny : The number of rows in the concentration matrix.
       
    c0 : The base concentration value around which fluctuations will occur.
       
    noise : The amplitude of the random fluctuations added to the base concentration.

    Returns:
    -------
    np.ndarray
        A 2D numpy array of shape (Ny, Nx) containing the concentration values with fluctuations.
    """
    np.random.seed(24)
    return c0 + noise * (0.5 - np.random.rand(Nx,Ny))

def chemical_potential(c, A):
    """
    This function calculates the chemical potential using the provided concentration 
    array and a constant 'A'.

    Parameters:
    ----------
    c : 2D numpy array representing the concentration values, where each element corresponds
        to a concentration at a specific spatial point.

    A : Multiplicative constant in the free energy.

    Returns:
    -------
    np.ndarray
        A 2D numpy array of the same shape as 'c', containing the computed chemical potential values.
    """
    return 2 * A * (c * ((1 - c) ** 2) - (c ** 2) * (1 -c))

def my_laplacian(c, dx, dy):
    """
    This function calculates the Laplacian operator for a 2D concentration matrix 'c' 
    while enforcing periodic boundary conditions. The Laplacian is calculated based on 
    the values surrounding each point in the matrix.

    Parameters:
    ----------
    c : 2D numpy array of shape (Ny, Nx) representing the concentration values.

    dx : The spacing between points in the x-direction.

    dy : The spacing between points in the y-direction.

    Returns:
    -------
    np.ndarray
        A 2D numpy array of the same shape as `c`, containing the computed Laplacian values.
    """
    Ny, Nx = c.shape
    c_top = np.vstack((c[-1, :], c[:-1, :]))                #in the position ij now there's (i-1)j
    c_bot = np.vstack((c[1:, :], c[0, :]))                  #in the position ij now there's (i+1)j
    c_lef = np.hstack((c[:, -1][:, np.newaxis], c[:, :-1])) #in the position ij now there's i(j-1)
    c_rig = np.hstack((c[:, 1:], c[:, 0][:, np.newaxis]))   #in the position ij now there's i(j-1)
    #np.newaxis assures that c_lef and c_right are 2D arrays
    return (c_top + c_bot + c_rig + c_lef - 4 * c) / (dx * dy)