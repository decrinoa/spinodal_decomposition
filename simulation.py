# -*- coding: utf-8 -*-
"""

Created on Wed Oct  16 16:45:43 2024

@author: decrinoa

"""
import Cahn_Hilliard
import configparser
import pandas as pd
import numpy as np

def run_simulation():
    #load data from configuration file
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

    # Material specific parameters
    c0 = config['settings']['c0']
    dc = config['settings']['dc']
    mobility = config['settings']['mobility']
    grad_coef = config['settings']['grad_coef']
    A = config['settings']['A'] 

    Nx = int(Nx)
    Ny = int(Ny)
    dx = float(dx)
    dy = float(dy)

    nstep = int(nstep)
    nprint = int(nprint)
    dtime = float(dtime)

    c0 = float(c0)
    dc = float(dc)
    mobility = float(mobility)
    grad_coef = float(grad_coef)
    A = float(A)


    c = Cahn_Hilliard.add_fluctuation(Nx, Ny, c0, dc)

    #evolve
    results = []
    for istep in range(1, nstep + 1):
        lap_c = Cahn_Hilliard.my_laplacian(c, dx, dy)  # Laplacian of concentration
        mu_c = Cahn_Hilliard.chemical_potential(c, A)  # Chemical potential
        dF_dc = mu_c - 2 * grad_coef * lap_c  # δF/δc
        lap_dF_dc = Cahn_Hilliard.my_laplacian(dF_dc, dx, dy)  # Laplacian of dF/dc

        # Time evolution
        c += dtime * mobility * lap_dF_dc
        
        if istep % nprint == 0:
            results.append((istep * dtime, np.copy(c), np.copy(mu_c)))
            
    save_results_csv(results, filename='simulation_results.csv')

def save_results_csv(results, filename='simulation_results.csv'):
    data = []
    for time, c, mu_c in results:
        data.append({
            'Time': time,
            'Concentration': c.flatten().tolist(),
            'Chemical Potential': mu_c.flatten().tolist()
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

run_simulation()
print("Simulation done! Data saved in simulation_results.csv")    