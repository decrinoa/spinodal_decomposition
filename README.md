# Spinodal Decomposition

The spinodal decomposition is a type of second order phase transformation where the order parameter is consituted by the concentration of a certain atomic species.
The equation that describes the kinetics of the order parameter is the Cahn-Hilliard equation. 

$$ \frac{\partial c}{\partial t} = \nabla \cdot \left[ M \nabla \left[ \frac{\partial f^{hom}}{\partial c} - 2 K_c \nabla^2c \right] \right] $$

where $M$ is the mobility, $\frac{\partial f^{hom}}{\partial c}$ is the chemical potential for diffusion, $K_c$ is the interface curvature. 
The equation can be simplified by replacing $M$ with ist average value $M_0$, leading to:

$$ \frac{\partial c}{\partial t} = M_0 \nabla^2 \left[ \frac{\partial f^{hom}}{\partial c} - 2 K_c \nabla^2c \right] $$

The kinetics is therefore governed by two terms: the diffusive term and the gradients term.
The diffusive term tends to amplify any composition fluctuations that spontaneously develop in the system.
On the other hand, the gradient term tends to dampen these fluctuations.

The study of spinodal decomposition is fundamental in the framework of phase-field modelling for microstructure and their stability.
In this project we will simulate the spinodal decomposition of different systems. 

# Structure of the project