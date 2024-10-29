# -*- coding: utf-8 -*-
"""

Created on Wed Oct  16 16:45:43 2024

@author: decrinoa

"""
import Cahn_Hilliard
import configparser
import sys
from sys import argv
import numpy as np

def run_simulation():
    """
    Run the Cahn-Hilliard simulation based on parameters defined in a configuration file.

    This function initializes the simulation environment by loading parameters from 
    a configuration file (`configuration.ini`). It sets up the necessary simulation 
    parameters, initializes the concentration field, and evolves the simulation using 
    the Cahn-Hilliard equation. The results are then saved to a CSV file.

    Steps performed in this function:
    1. Load simulation parameters from the configuration file.
    2. Initialize the random seed for reproducibility.
    3. Create the initial concentration field with fluctuations.
    4. Evolve the simulation over a defined number of time steps.
    5. Save the simulation results to a CSV file.

    Returns:
    -------
    None
        The function does not return any value. It produces side effects by 
        saving the simulation results to a file.
    """
    # Load data from configuration file
    config = configparser.ConfigParser()
    config.read(sys.argv[1])


    # Define the simulation cell parameters
    Nx = config['settings']['Nx']
    Ny = config['settings']['Ny']
    dx = config['settings']['dx']
    dy = config['settings']['dy']

    # Time integration parameters
    nstep = config['settings']['nstep']
    nprint = config['settings']['nprint']
    dtime = config['settings']['dtime']

    # Random Seed
    seed = config['settings']['seed']

    # Material specific parameters
    c0 = config['material1']['c0']
    dc = config['material1']['dc']
    mobility = config['material1']['mobility']
    grad_coef = config['material1']['grad_coef']
    A = config['material1']['A'] 

    Nx = int(Nx)
    Ny = int(Ny)
    dx = float(dx)
    dy = float(dy)

    nstep = int(nstep)
    nprint = int(nprint)
    dtime = float(dtime)
    
    seed = int(seed)

    c0 = float(c0)
    dc = float(dc)
    mobility = float(mobility)
    grad_coef = float(grad_coef)
    A = float(A)
    
    # Initialization of the random seed
    np.random.seed(seed)
    
    # Creation of the empty 2Darray
    c = np.zeros((Ny, Nx))

    # Initial configuration with fluctuation
    c = Cahn_Hilliard.add_fluctuation(Nx, Ny, c0, dc)

    results = Cahn_Hilliard.evolve_simulation(c, nstep, nprint, dtime, mobility, grad_coef, A, dx, dy)
            
    Cahn_Hilliard.save_results_csv(results, filename='simulation_results.csv')

run_simulation()
print("Simulation done! Data saved in simulation_results.csv")    