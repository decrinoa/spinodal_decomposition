# -*- coding: utf-8 -*-
"""

Created on Wed Oct  16 16:45:43 2024

@author: decrinoa

"""
import Cahn_Hilliard
import configparser
import numpy as np

def run_simulation():
    # Load data from configuration file
    config = configparser.ConfigParser()
    config.read('configuration.ini')


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
    
    # Creation of the empty 2Darrays
    c = np.zeros((Ny, Nx))
    mu_c = np.zeros((Ny, Nx))
    lap_c = np.zeros((Ny, Nx))

    # Initial configuration with fluctuation
    c = Cahn_Hilliard.add_fluctuation(Nx, Ny, c0, dc)

    #evolve
    results = []
    for istep in range(1, nstep + 1):
        # Laplacian of concentration
        lap_c = Cahn_Hilliard.my_laplacian(c, dx, dy)  
        # Chemical potential
        mu_c = Cahn_Hilliard.chemical_potential(c, A)
        # Generalized diffusion potential
        dF_dc = mu_c - 2*grad_coef*lap_c  
        # Laplacian of dF/dc, main term of the Cahn Hilliard equation
        lap_dF_dc = Cahn_Hilliard.my_laplacian(dF_dc, dx, dy)  

        # Time evolution
        c += dtime * mobility * lap_dF_dc
        
        if istep % nprint == 0:
            results.append((istep * dtime, np.copy(c), np.copy(mu_c)))
            
    Cahn_Hilliard.save_results_csv(results, filename='simulation_results.csv')

run_simulation()
print("Simulation done! Data saved in simulation_results.csv")    