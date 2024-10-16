# -*- coding: utf-8 -*-
"""

Created on Wed Oct  16 16:45:43 2024

@author: decrinoa

"""
import Cahn_Hilliard
import configparser
import matplotlib.pyplot as plt


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

c = Cahn_Hilliard.add_fluctuation(Nx, Ny, c0, dc)


# Evolve
iplot = 0
plt.figure(figsize=(12, 10))

for istep in range(1, nstep + 1):
    lap_c = Cahn_Hilliard.my_laplacian(c, dx, dy)  # Laplacian of concentration
    mu_c = Cahn_Hilliard.chemical_potential(c, A)  # Chemical potential
    dF_dc = mu_c - 2 * grad_coef * lap_c  # δF/δc
    lap_dF_dc = Cahn_Hilliard.my_laplacian(dF_dc, dx, dy)  # Laplacian of dF/dc

    # Time evolution
    c += dtime * mobility * lap_dF_dc

    # Plot results every nprint iterations
    if istep % nprint == 0:
        iplot += 1
        
        plt.subplot(1, 2, 1)
        plt.imshow(c, cmap='gray', vmin=0, vmax=1)
        plt.colorbar()
        plt.title(f'Concentration at time {istep * dtime:.2f}')
        
        plt.subplot(1, 2, 2)
        plt.imshow(mu_c, cmap='jet')
        plt.title(f'Chemical potential at time {istep * dtime:.2f}')
        plt.colorbar(label='μ (x,y)')
        
        plt.tight_layout()
        plt.pause(0.1)
        
plt.show()  