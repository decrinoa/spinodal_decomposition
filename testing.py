# -*- coding: utf-8 -*-
"""

Created on Wed Oct  16 16:45:43 2024

@author: decrinoa

"""

import Cahn_Hilliard
import configparser
import numpy as np
from hypothesis import strategies as st
from hypothesis import given


config = configparser.ConfigParser()
config.read('configuration.ini')

Nx = config['settings']['Nx']
Ny = config['settings']['Ny']
dx = config['settings']['dx']
dy = config['settings']['dy']

c0 = config['material']['c0']
dc = config['material']['dc']

Nx = int(Nx)
Ny = int(Ny)
dx = float(dx)
dy = float(dy)

c0 = float(c0)
dc = float(dc)
 
@given( Nx = st.integers(1,Nx), Ny = st.integers(1,Ny), c0 = st.floats(0, c0), dc = st.floats(0, dc))
def test_add_fluctuation_boundaries(Nx,Ny,c0,dc):
    """
    This test ensures that the concentration values generated by the 
    'add_fluctuation' function are within specified bounds. The bounds are defined
    from the expression of 'add_fluctuation', namely as the initial concentration 'c0' 
    plus or minus half of the fluctuation range 'dc'.

    Parameters:
    ----------
    Nx : The number of columns in the concentration matrix. Must be greater or equal than 1 and lower or euqual than Nx in configuration file.
       
    Ny : The number of rows in the concentration matrix. Must be greater or equal than 1 and lower or euqual than Ny in configuration file.
       
    c0 : The base concentration value around which fluctuations will occur. Must be greater or equal than 0 and lower or euqual than c0 in configuration file.
       
    dc : The amplitude of the random fluctuations added to the base concentration. Must be greater or equal than 0 and lower or euqual than dc in configuration file.

    Assertions:
    -----------
    - Asserts that all concentration values are greater than or equal to 'c0 - dc * 0.5'.
    - Asserts that all concentration values are less than or equal to 'c0 + dc * 0.5'.
    """
    c = Cahn_Hilliard.add_fluctuation(Nx, Ny, c0, dc)
    lower_bound = c0 - dc*(0.5)
    upper_bound = c0 + dc*(0.5)
    
    assert np.all(c >= lower_bound)
    assert np.all(c <= upper_bound)

@given(c = st.floats(0, 1))
def test_chemical_potential_boundaries(c):
    """
    This test ensures that the chemical potential values calculated by the 
    'chemical_potential' function are within specified bounds. The bounds are defined
    from the expression of 'chemical_potential', where the maxima condition is 'c = 0.5' 
    and the minima condition is 'c = 0'.

    Parameters:
    ----------   
    c : The concentration value generated between 0 and 1.
       
    Assertions:
    -----------
    - Asserts that all chemical potential values are greater than or equal to 'chemical_potential(0, A)'.
    - Asserts that all chemical potential values are less than or equal to 'chemical_potential(0.5, A)'.
    """
    c_max = 0.5 - 1 / (2*np.sqrt(3))
    c_min = 0.5 + 1 / (2*np.sqrt(3))
    A = 1.0
    lower_bound = Cahn_Hilliard.chemical_potential(c_min, A)
    upper_bound = Cahn_Hilliard.chemical_potential(c_max, A)
    result = Cahn_Hilliard.chemical_potential(c, A)
    
    assert np.all(result >= lower_bound)
    assert np.all(result <= upper_bound)


@given(Nx = st.integers(1,Nx), Ny = st.integers(1,Ny))
def test_chemical_potential_shape(Nx, Ny):
    """
    This test verifies that the output of the 'chemical_potential' function 
    has the same shape as the input concentration matrix 'c'.

    Parameters:
    ----------
    Nx : The number of columns in the concentration matrix. Must be greater or equal than 1 and lower or euqual than Nx in configuration file.
       
    Ny : The number of rows in the concentration matrix. Must be greater or equal than 1 and lower or euqual than Ny in configuration file.

    Assertions:
    -----------
    - Asserts that the shape of the output from 'chemical_potential' matches the shape of the input concentration matrix 'c'.
    """
    np.random.seed(24)
    c = np.random.rand(Nx, Ny)
    A = 1
    result = Cahn_Hilliard.chemical_potential(c, A)
    
    assert result.shape == c.shape

@given(Nx = st.integers(1,Nx), Ny = st.integers(1,Ny), dx = st.floats(0.1,dx), dy = st.floats(0.1,dy))
def test_my_laplacian_shape(Nx, Ny, dx, dy):
    """
    This test verifies that the output of the 'my_laplacian' function 
    has the same shape as the input concentration matrix 'c'.

    Parameters:
    ----------
    Nx : The number of columns in the concentration matrix. Must be greater or equal than 1 and lower or euqual than Nx in configuration file.
       
    Ny : The number of rows in the concentration matrix. Must be greater or equal than 1 and lower or euqual than Ny in configuration file.

    dx : The spacing between points in the x-direction. Must be greater or equal than 0.1 and lower or equal than dx in configuration file.
    
    dy : The spacing between points in the y-direction. Must be greater or equal than 0.1 and lower or equal than dy in configuration file.
    
    Assertions:
    -----------
    - Asserts that the shape of the output from 'my_laplacian' matches the shape of the input concentration matrix 'c'.
    """
    np.random.seed(24)
    c = np.random.rand(Nx, Ny)
    result = Cahn_Hilliard.my_laplacian(c, dx, dy)
    
    assert result.shape == c.shape    