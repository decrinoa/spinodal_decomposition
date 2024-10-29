# Spinodal Decomposition

This code is based on the didactic material of the course Microscopic Kinetics and Thermodynamics from Prof. Luca Pasquini at the University of Bologna.

Its purpose is to simulate the spinodal decomposition of a two element system, by focusing only on one species. 
In fact, the state where the concentration value is equal to zero corresponds to a concentration equal to one of the other species.  

In the following section there will be a guide for the user to download and start the code, an explanation of its structure and some theoretical remarks on spinodal decomposition.

# How to download and start the code

The project has been developed on the Windows Subsystem for Linux, 
these steps are referred to linux or WSL users. 

1- In the terminal or command prompt clone the repository
```
git clone https://github.com/decrinoa/spinodal_decomposition.git
```
2- Make sure you have all the needed packages for Python 3. 
   You can install them using the `requirements.txt` file: 
```
pip install -r requirements.txt
```
Note: The version of numpy must be lower than 2.x.x because it is incompatible with the used matplotlib methods. 
The version recommended is numpy 1.26.4.

3- Navigate into the project directory
```
cd spinodal_decomposition 
```
4- Start the simulation
```
python3 simulation.py
```
5- Plot the results
```
python3 plotting.py
```

# Structure of the project

This project is divided into five blocks:

In the file Cahn_Hilliard there are stored the main function to run the simulation.
The scope of these functions is to generate a perturbation for the initial concentration matrix and to compute the related important quantities for the simulation (chemical_potential and my_laplacian).

In the file testing there are the tests related to the Cahn_Hilliard file, the test are performed using hypothesis library.

In the file configuration there are all the definitions of the parameters used in the simulation file. 
These parameters are divided in two section: the 'settings' section is related to the parameters of the simulation, 
i.e. the dimension of the matrix, the discrete spacing used in the Laplacian calculation, the parameters linked to the simulation steps and to its printing;
the material section contains the parameters typical of the system simulated, 
i.e the initial concentration, the fluctuations of the concentration, the mobility and the constants of the various equations. 

In the file simulation there is the main part of the code. The simulations is first executed by calling the functions present in Cahn_Hilliard. 
The results of the simulation are then stored in the 'results' variable that is then saved to a csv file by using pandas library.
The scope of the simulation is to show the evolution of the concentrations and the chemical potential values in the mesh grid that constitutes the system.  

In the file plotting there is the function that plots the evolution of the concentration and chemical potential values by means of two color maps. 
The data for the plotting are uploaded from the csv file and 10 significant frame of the simulation are saved in the newly created images folder.

## Guide on the configuration modification

The user can decide which of the two configuration to use.
 
In order to switch from one to the other, is necessary to open and modify the simulation.py file.

At line 31 there is the section regarding the material's parameter, in the base version the material chosen is 'material1',
in order to switch to 'material2' is necessary to substitute the keyword 'material1' with 'material2'. 

If the user wants to add a new configuration, a new section in the configuration.ini file can be added.
This new configuration must be preceded by the keyword [material3]. 

It is suggested to leave the value of the initial concentration to 0.5, since in this way the starting point is and heterogeneous system. 
The value of the amplitude of the fluctuations should not be too big since it is a fluctuation. 
A recommended maximum value is 0.1.  

If the user wants a system that evolves more rapidly it is suggested to enhance the 'mobility' value. 
Also the user can decide to amplify the evolution of the concentration's fluctuation by enhancing the constant of the chemical potential 'A'.
Finally, if the user wants to dump the concentration's fluctuation is can do so by enhancing the 'grad_coef' value.

# Theory of Spinodal Decomposition

The spinodal decomposition is a type of second order phase transformation where the order parameter is constituted by the concentration of a certain atomic species.
The equation that describes the kinetics of the order parameter is the Cahn-Hilliard equation[1]. 

$$ \frac{\partial c}{\partial t} = \nabla \cdot \left[ M \nabla \left[ \frac{\partial f^{hom}}{\partial c} - 2 K_c \nabla^2c \right] \right] $$

where $M$ is the mobility, $\frac{\partial f^{hom}}{\partial c}$ is the chemical potential for diffusion, $K_c$ is the interface curvature. 
The equation can be simplified by replacing $M$ with its average value $M_0$, leading to:

$$ \frac{\partial c}{\partial t} = M_0 \nabla^2 \left[ \frac{\partial f^{hom}}{\partial c} - 2 K_c \nabla^2c \right]. $$

The expression in parentheses is the generalised diffusion potential. 
The kinetics is therefore governed by two terms: the diffusive term and the gradients term.
The diffusive term tends to amplify any composition fluctuations that spontaneously develop in the system.
On the other hand, the gradient term tends to dampen these fluctuations.

The study of spinodal decomposition is fundamental in the framework of phase-field modelling for microstructure and their stability.
In this project we will simulate the spinodal decomposition of different systems. 

## Remarks on the chemical potential 

The chemical potential is defined as the derivative of homogeneous free energy in terms of the concentration.
In this code the homogeneous free energy is chosen to be:

$$ f^{hom} = Ac^2(1-c)^2.$$

Therefore the derivative in terms of the concetration will be:

$$ \mu = \frac{\partial f^{hom}}{\partial c} = 2A[c(1-c)^2-c^2(1-c)]. $$

## Remarks on the method used for the Laplacian calculation

The second-order derivatives can be easily handled by replacing them with central differences[2]. 
The most widely used difference approximation of the second-order derivative is: 

$$ \frac{\partial^2 f(x_i,y_j)}{\partial x^2} \approx \frac{f_{i+1}^{j} - 2 f_{i}^{j} + f_{i-1}^{j}}{{\Delta x}^2}. $$

The Laplacian function, also call Poisson equation, can be therefore approximated using:

$$ \nabla^2 f(x_i, y_j) = \frac{\partial^2 f(x_i,y_j)}{\partial y^2} + \frac{\partial^2 f(x_i,y_j)}{\partial x^2}.$$

In this code the calculation of the displaced terms is obtained by creating 4 new 2D arrays:

- i(j-1) item is obtained by stacking vertically the last row of the original matrix in top of the original matrix deprived of the last row;
- i(j+1) item is obtained by stacking vertically all the row of the original matrix starting from the second one in top of the original matrix deprived of the first row;
- (i-1)j item is obtained by stacking horizontally the last column of the original matrix on the left of the original matrix deprived of the last column; 
- (i+1)j item is obtained by stacking horizontally all the column of the original matrix starting from the second one on the left of the original matrix deprived of the first column.

In this way also the element at the border of the matrix are properly handled. 


## Remarks on the configurations used and their main outcomes
 
In the file configuration.ini two examples are reported: 
- the 'material1' parameters corresponds to a system where the predominant term is the diffusive term, 
therefore the fluctuations of the concentration will be amplified and the system will evolve faster in the two phase configuration;
- the 'material2' parameters corresponds to a system where the predominant term is the gradient term, the fluctuations are therefore dumped and the system will evolve slowly. 

An illustration of the difference between the two materials can be seen in the following image. 
The outcomes of the simulation at time 50s, 250s and 500s are presented for both the configuration given. 

![alt text](https://github.com/decrinoa/spinodal_decomposition/blob/main/images/comparison.png) 

# References

[1] Robert W. Balluffi, Samuel M. Allen, W. Craig Carter - Kinetics of Materials (2005, Wiley-Interscience)

[2] https://github.com/john-s-butler-dit/Numerical-Analysis-Python.git