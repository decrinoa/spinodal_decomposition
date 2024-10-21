# Spinodal Decomposition

The spinodal decomposition is a type of second order phase transformation where the order parameter is consituted by the concentration of a certain atomic species.
The equation that describes the kinetics of the order parameter is the Cahn-Hilliard equation[1]. 

$$ \frac{\partial c}{\partial t} = \nabla \cdot \left[ M \nabla \left[ \frac{\partial f^{hom}}{\partial c} - 2 K_c \nabla^2c \right] \right] $$

where $M$ is the mobility, $\frac{\partial f^{hom}}{\partial c}$ is the chemical potential for diffusion, $K_c$ is the interface curvature. 
The equation can be simplified by replacing $M$ with ist average value $M_0$, leading to:

$$ \frac{\partial c}{\partial t} = M_0 \nabla^2 \left[ \frac{\partial f^{hom}}{\partial c} - 2 K_c \nabla^2c \right]. $$

The expression in parentheses is the generalised diffusion potentail. 
The kinetics is therefore governed by two terms: the diffusive term and the gradients term.
The diffusive term tends to amplify any composition fluctuations that spontaneously develop in the system.
On the other hand, the gradient term tends to dampen these fluctuations.

The study of spinodal decomposition is fundamental in the framework of phase-field modelling for microstructure and their stability.
In this project we will simulate the spinodal decomposition of different systems. 

# Remarks on the method used for the Laplacian calculation

The second-order derivatives can be easily handled by replacing them with central differences[2]. 
The most widely used difference approximation of the second-order derivative is: 

$$ \frac{\partial^2 f(x_i,y_j)}{\partial x^2} \approx \frac{f_{i+1}^{j} - 2 f_{i}^{j} + f_{i-1}^{j}}{{\Delta x}^2}. $$

The laplacian function, also call Poisson equation, can be therefore approximated using:

$$ \nabla^2 f(x_i, y_j) = \frac{\partial^2 f(x_i,y_j)}{\partial y^2} + \frac{\partial^2 f(x_i,y_j)}{\partial x^2}.$$

In this code the calculation of the displaced terms is obtained by creating 4 new 2D arrays:

- i(j-1) item is obtained by stacking vertically the last row of the original matrix in top of the original matrix deprived of the last row;
- i(j+1) item is obtained by stacking vertically all the row of the original matrix starting from the second one in top of the original matrix deprived of the first row;
- (i-1)j item is obtained by stacking orizontally the last column of the original matrix on the left of the original matrix deprived of the last column; 
- (i+1)j item is obtained by stacking orizontally all the column of the original matrix starting from the second one on the left of the original matrix deprived of the first column.

# How to download and start the projet

The project has been developed on the Windows Subsystem for Linux, 
these steps are referred to linux or WSL users. 

1- In the terminal or command prompt clone the repository
```
git clone https://github.com/decrinoa/spinodal_decomposition.git
```
2- Make sure that you have all the needed packages in python3: 
```
pip install numpy 
pip install matplotlib
pip install pandas
pip install configparser
pip install os
pip install hypothesis
```
The version of numpy must be lower than 2.x.x because it is incompatible with the used matplotlib methods. 
The version raccomended is numpy 1.26.4.

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


# References

[1] Robert W. Balluffi, Samuel M. Allen, W. Craig Carter - Kinetics of Materials (2005, Wiley-Interscience)
[2] https://github.com/john-s-butler-dit/Numerical-Analysis-Python.git