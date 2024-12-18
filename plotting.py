# -*- coding: utf-8 -*-
"""

Created on Wed Oct  16 16:45:43 2024

@author: decrinoa

"""
import Cahn_Hilliard
import configparser
import matplotlib.pyplot as plt
import os
import sys

config = configparser.ConfigParser()
config.read(sys.argv[1])

Nx = config['settings']['Nx']
Ny = config['settings']['Ny']

nsave = config['settings']['nsave']

Nx = int(Nx)
Ny = int(Ny)

nsave = int(nsave)

def plot_results(results, nsave, folder='images'):
    """
    This function visualizes the concentration and chemical potential data from the 
    simulation results. For each time step, it creates subplots displaying the concentration 
    and chemical potential, and saves the plots as PNG files in the specified folder 
    at defined intervals.

    Parameters:
    ----------
    results : A list where each tuple contains:
        - time (float): The time point of the simulation.
        - c (numpy.ndarray): A 2D array representing the concentration at the given time.
        - mu_c (numpy.ndarray): A 2D array representing the chemical potential at the given time.

    nsave : The interval at which to save the plots (in terms of time steps). 
            Only plots for times that are multiples of this value will be saved.

    folder : The directory where the plots will be saved (default is 'images'). 
             The directory will be created if it does not exist.

    Returns:
    -------
    None
        The function does not return any value. It produces plots and saves them to disk.

    """
    os.makedirs(folder, exist_ok=True)
    
    plt.figure(figsize=(12, 6))

    for time, c, mu_c in results:
        plt.subplot(1, 2, 1)
        im_c = plt.imshow(c, cmap='gray', vmin=0, vmax=1)
        plt.colorbar(im_c, label='c (a.u.)', aspect=40)
        plt.title(f'Concentration at time {time:.2f} s')

        plt.subplot(1, 2, 2)
        im_m = plt.imshow(mu_c, cmap='plasma')
        plt.colorbar(im_m, label='μ (x,y)', aspect=40)
        plt.title(f'Chemical potential at time {time:.2f} s')
    
        plt.tight_layout()
        
        if time % nsave == 0:
            plt.savefig(os.path.join(folder, f'plot_at_time_{time:.2f}.png'))
            print(f'Saved plot for time {time:.2f} s')
            
        plt.pause(0.1)

    plt.show()
    

plot_results(Cahn_Hilliard.load_results_from_csv(Nx, Ny, filename='simulation_results.csv'), nsave)