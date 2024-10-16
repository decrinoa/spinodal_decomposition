# -*- coding: utf-8 -*-
"""

Created on Wed Oct  16 16:45:43 2024

@author: decrinoa

"""

import Cahn_Hilliard
import configuration
import numpy as np
from hypothesis import strategies as st
from hypothesis import given

#test that all the values of c are between the low and up bounds 
@given( Nx = st.integers(1,configuration.Nx), Ny = st.integers(1,configuration.Ny))
def test_add_fluctuation_boundaries(Nx,Ny,c0,dc):
    c = Cahn_Hilliard.add_fluctuation(Nx, Ny, c0, dc)
    lower_bound = c0 - dc*(0.5)
    upper_bound = c0 + dc*(0.5)
    
    assert np.all(c >= lower_bound)
    assert np.all(c <= upper_bound)


