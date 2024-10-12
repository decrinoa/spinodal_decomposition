"""
@author: decrinoa

purpose of the program: to simulate a spinodal decomposition
using the Cahn-Hilliard equation
"""

import numpy as np
import matplotlib.pyplot as plt

#flunctuation of the concentration generated randomly in every point of the system
def add_fluctuation(Nx, Ny, c0, noise):
    return c0 + noise * (0.5 - np.random.rand(Nx,Ny))

def chemical_potential(c, A):
    return 2 * A * (c * ((1 - c) ** 2) - (c ** 2) * (1 -c))

#c_top, c_bot, c_lef, c_rig necessary to ensure the periodic boundary condition
def my_laplacian(c, dx, dy):
    Ny, Nx = c.shape
    c_top = np.vstack((c[-1, :], c[:-1, :]))                #Top bc
    c_bot = np.vstack((c[1:, :], c[0, :]))                  #bottom bc
    c_lef = np.hstack((c[:, -1][:, np.newaxis], c[:, :-1])) #left bc, [:, np.newaxis] ensure c[:, -1] is 2D
    c_rig = np.hstack((c[:, 1:], c[:, 0][:, np.newaxis]))   #rigth bc, [:, np.newaxis] ensure c[:, -1] is 2D
    
    return (c_top + c_bot + c_rig + c_lef - 4 * c) / (dx * dy)

# Define the simulation cell parameters
Nx = 150
Ny = 150
dx = 1.0
dy = 1.0

# Time integration parameters
nstep = 50000
nprint = 500
dtime = 1.0e-2

# Material specific parameters
c0 = 0.50
dc = 0.02
mobility = 1.0
grad_coef = 0.5
A = 1.0  # multiplicative constant in free energy

# Initialize concentration with fluctuations
c = add_fluctuation(Nx, Ny, c0, dc)


# Evolve
iplot = 0
plt.figure(figsize=(12, 10))

for istep in range(1, nstep + 1):
    lap_c = my_laplacian(c, dx, dy)  # Laplacian of concentration
    mu_c = chemical_potential(c, A)  # Chemical potential
    dF_dc = mu_c - 2 * grad_coef * lap_c  # δF/δc
    lap_dF_dc = my_laplacian(dF_dc, dx, dy)  # Laplacian of dF/dc

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

#test that all the values of c are between the low and up bounds 
#note, if you change the 0.5 value in add_fluctuations, it must change here too
def test_add_fluctuation():
    c = add_fluctuation(Nx, Ny, c0, dc)
    lower_bound = c0 - dc*(0.5)
    upper_bound = c0 + dc*(0.5)
    
    assert np.all(c >= lower_bound)
    assert np.all(c <= upper_bound)

            