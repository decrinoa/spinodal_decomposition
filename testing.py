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

c0 = config['settings']['c0']
dc = config['settings']['dc']

Nx = int(Nx)
Ny = int(Ny)
dx = float(dx)
dy = float(dy)

c0 = float(c0)
dc = float(dc)
 
@given( Nx = st.integers(1,Nx), Ny = st.integers(1,Ny), c0 = st.floats(0, c0), dc = st.floats(0, dc))
def test_add_fluctuation_boundaries(Nx,Ny,c0,dc):
    #Test that all the values of c are between the low and up bounds
    c = Cahn_Hilliard.add_fluctuation(Nx, Ny, c0, dc)
    lower_bound = c0 - dc*(0.5)
    upper_bound = c0 + dc*(0.5)
    
    assert np.all(c >= lower_bound)
    assert np.all(c <= upper_bound)


@given(Nx = st.integers(1,Nx), Ny = st.integers(1,Ny))
def test_chemical_potential_shape(Nx, Ny):
    # Test output shape matches input shape with specific values
    c = np.random.rand(Nx, Ny)
    A = 1
    result = Cahn_Hilliard.chemical_potential(c, A)
    assert result.shape == c.shape

@given(Nx = st.integers(1,Nx), Ny = st.integers(1,Ny), dx = st.floats(0.1,dx), dy = st.floats(0.1,dy))
def test_my_laplacian_shape(Nx, Ny, dx, dy):
    # Test output shape matches input shape with specific values
    c = np.random.rand(Nx, Ny)
    result = Cahn_Hilliard.my_laplacian(c, dx, dy)
    assert result.shape == c.shape