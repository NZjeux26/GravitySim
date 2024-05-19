import numpy as np
from scipy.integrate import solve_ivp

# Define the gravitational parameter (mu)
G = 6.67430e-11  # m^3 kg^-1 s^-2
m1 = 5.972e24    # kg (Earth mass)
m2 = 7.342e22    # kg (Moon mass)
mu = G * (m1 + m2)

# Define the system of differential equations
def equations(t, y):
    r = np.array([y[0], y[1], y[2]])
    v = np.array([y[3], y[4], y[5]])
    r_norm = np.linalg.norm(r)
    
    drdt = v
    dvdt = -mu / r_norm**3 * r
    
    return [drdt[0], drdt[1], drdt[2], dvdt[0], dvdt[1], dvdt[2]]

# Initial conditions (example values)
r0 = [384400000, 0, 0]   # Initial position vector (m)
v0 = [0, 1022, 0]        # Initial velocity vector (m/s)
initial_conditions = r0 + v0

# Time span for the simulation (seconds)
t_span = (0, 3600*24*30)  # One month

# Solve the ODE
solution = solve_ivp(equations, t_span, initial_conditions, method='RK45')

# Extract the results
time = solution.t
positions = solution.y[:3]  # x, y, z positions
velocities = solution.y[3:]  # vx, vy, vz velocities

# Example output
print("Time:", time)
print("Positions:", positions)
print("Velocities:", velocities)
