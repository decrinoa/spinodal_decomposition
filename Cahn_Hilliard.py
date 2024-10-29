# -*- coding: utf-8 -*-
"""

Created on Thu Oct  10 13:08:11 2024

@author: decrinoa

"""

import numpy as np
import pandas as pd

def add_fluctuation(Nx, Ny, c0, dc):
    """
    This function generates a 2D matrix of size (Nx, Ny) 
    representing concentration values.
    Each value is perturbed by a random noise term, 
    which is uniformly distributed around the base concentration 'c0',
    between -noise*0.5 and +noise*0.5.

    Parameters:
    ----------
    Nx : The number of columns in the concentration matrix.
       
    Ny : The number of rows in the concentration matrix.
       
    c0 : The base concentration value around which fluctuations will occur.
       
    dc : The amplitude of the fluctuations added to the base concentration.

    Returns:
    -------
    np.ndarray
        A 2D numpy array of shape (Ny, Nx) containing 
        the concentration values with fluctuations.
    
    Raise:
    -----
    ValueError if one dimension of the matrix is less than 1. 
    """
    if Nx < 1 or Ny < 1:
        raise ValueError('Both dimensions of the matrix must be > 1, but are {} and {}'.format(Nx,Ny))
    np.random.seed(24)
    return c0 + dc*(0.5-np.random.rand(Ny,Nx))

def chemical_potential(c, A):
    """
    This function calculates the chemical potential using 
    the provided concentration array and a constant 'A'.

    Parameters:
    ----------
    c : 2D numpy array representing the concentration values, 
        where each element corresponds to a concentration 
        at a specific spatial point.

    A : Multiplicative constant in the free energy.

    Returns:
    -------
    np.ndarray
        A 2D numpy array of the same shape as 'c', 
        containing the computed chemical potential values.
    """
    return 2*A*(c*((1-c)**2) - (c**2)*(1-c))

def my_laplacian(c, dx, dy):
    """
    This function calculates the Laplacian operator for a 2D concentration matrix 'c' 
    while enforcing periodic boundary conditions. 
    The Laplacian is calculated based on the subtraction 
    of the values surrounding each point in the matrix.

    Parameters:
    ----------
    c : 2D numpy array of shape (Ny, Nx) representing the concentration values.

    dx : The spacing between points in the x-direction.

    dy : The spacing between points in the y-direction.

    Returns:
    -------
    np.ndarray
        A 2D numpy array of the same shape as `c`, 
        containing the computed Laplacian values.
    Raise:
    -----
    ValueError if one spacing is less than or equal to 0.
    """
    if dx <= 0 or dy <= 0:
        raise ValueError('Both spacing must be greater than 0.')
    Ny, Nx = c.shape
    # In the position ij now there's i(j-1)
    c_top = np.vstack((c[-1, :], c[:-1, :]))
    # In the position ij now there's i(j-1)                
    c_bot = np.vstack((c[1:, :], c[0, :]))
    # In the position ij now there's (i-1)j                  
    c_lef = np.hstack((c[:, -1][:, np.newaxis], c[:, :-1])) 
    # In the position ij now there's (i+1)j
    c_rig = np.hstack((c[:, 1:], c[:, 0][:, np.newaxis]))   
    # np.newaxis assures that c_lef and c_right are 2D arrays
    # Finite second derivative for the x direction
    d2c_dx2 = (c_top+c_bot-2*c) / (dx*dx)
    # Finite second derivative for the y direction
    d2c_dy2 = (c_lef+c_rig-2*c) / (dy*dy)
    return d2c_dx2 + d2c_dy2

def save_results_csv(results, filename='simulation_results.csv'):
    """
    This function takes simulation results, which include time, concentration,
    and chemical potential data, and saves them in a CSV format. 
    Each entry in the CSV will have three columns: 
    'Time', 'Concentration', and 'Chemical Potential'.

    Parameters:
    ----------
    results : A list where each tuple contains the following elements:
        - time (float): The time point of the simulation.
        - c (numpy.ndarray): 
            A 2D array representing the concentration at the given time.
        - mu_c (numpy.ndarray): 
            A 2D array representing the chemical potential at the given time.

    filename : The name of the output CSV file (default is 'simulation_results.csv').

    Returns:
    -------
    None
        The function writes the data to a CSV file and does not return any value.
    """
    data = []
    for time, c, mu_c in results:
        data.append({
            'Time': time,
            'Concentration': c.flatten().tolist(),
            'Chemical Potential': mu_c.flatten().tolist()
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def load_results_from_csv(Nx, Ny, filename='simulation_results.csv'):
    """
    This function reads a CSV file containing simulation results and reconstructs
    the data into a list of tuples. Each tuple contains the time, concentration,
    and chemical potential data.

    Parameters:
    ----------
    Nx : The number of spatial points in the x-direction for reshaping 
         the concentration and chemical potential arrays.

    Ny : The number of spatial points in the y-direction for reshaping 
         the concentration and chemical potential arrays.

    filename : The name of the input CSV file (default is 'simulation_results.csv').

    Returns:
    -------
    results : A list where each tuple contains:
        - time (float): The time point of the simulation.
        - c (numpy.ndarray): A 2D array of shape (Ny, Nx) 
          representing the concentration at the given time.
        - mu_c (numpy.ndarray): A 2D array of shape (Ny, Nx) 
          representing the chemical potential at the given time.
    """
    df = pd.read_csv(filename)
    
    results = []
    for index, row in df.iterrows():
        time = row['Time']
        c = np.fromstring(row['Concentration'].strip('[]'),
                          sep=',', dtype=float).reshape((Ny, Nx))
        mu_c = np.fromstring(row['Chemical Potential'].strip('[]'),
                             sep=',', dtype=float).reshape((Ny, Nx))
        
        results.append((time, c, mu_c))
    
    return results