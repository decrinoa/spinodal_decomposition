# -*- coding: utf-8 -*-
"""

Created on Wed Oct  16 16:45:43 2024

@author: decrinoa

"""
import configparser
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

config = configparser.ConfigParser()
config.read('configuration.ini')

Nx = config['settings']['Nx']
Ny = config['settings']['Ny']

Nx = int(Nx)
Ny = int(Ny)

def load_results_from_csv(filename='simulation_results.csv'):
    # Load data from CSV file
    df = pd.read_csv(filename)
    
    # Reconstruct results into a list of tuples
    results = []
    for index, row in df.iterrows():
        time = row['Time']
        c = np.fromstring(row['Concentration'].strip('[]'), sep=',', dtype=float).reshape((Ny, Nx))
        mu_c = np.fromstring(row['Chemical Potential'].strip('[]'), sep=',', dtype=float).reshape((Ny, Nx))
        
        results.append((time, c, mu_c))
    
    return results

def plot_results(results):
    plt.figure(figsize=(12, 10))

    for time, c, mu_c in results:
        plt.subplot(1, 2, 1)
        plt.imshow(c, cmap='gray', vmin=0, vmax=1)
        plt.colorbar()
        plt.title(f'Concentration at time {time:.2f}')

        plt.subplot(1, 2, 2)
        plt.imshow(mu_c, cmap='jet')
        plt.title(f'Chemical potential at time {time:.2f}')
        plt.colorbar(label='μ (x,y)')

        plt.tight_layout()
        plt.pause(0.1)

    plt.show()

plot_results(load_results_from_csv(filename='simulation_results.csv'))