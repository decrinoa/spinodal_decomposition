# -*- coding: utf-8 -*-
"""

Created on Wed Oct  16 16:45:43 2024

@author: decrinoa

"""
import Cahn_Hilliard
import configparser
import matplotlib.pyplot as plt
import os

config = configparser.ConfigParser()
config.read('configuration.ini')

Nx = config['settings']['Nx']
Ny = config['settings']['Ny']

nsave = config['settings']['nsave']

Nx = int(Nx)
Ny = int(Ny)

nsave = int(nsave)

def plot_results(results, nsave, folder='images'):
    
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