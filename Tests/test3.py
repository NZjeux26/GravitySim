import numpy as np
import pygame

# Define the gravitational parameter (mu)
G = 6.67430e-11  # m^3 kg^-1 s^-2
m1 = 5.972e24    # kg (Earth mass)
m2 = 7.342e22    # kg (Moon mass)
mu = G * (m1 + m2)

# Initial conditions
r0 = np.array([384400000, 0, 0])   # Initial position vector (m)
v0 = np.array([0, 1022, 0])        # Initial velocity vector (m/s)

# Time parameters
dt = 60  # Time step (seconds)
num_steps = int(3600 * 24 * 30 / dt)  # Number of steps for one month

# Initialize arrays to store positions and velocities
positions = np.zeros((num_steps, 3))
velocities = np.zeros((num_steps, 3))

# Set initial conditions
positions[0] = r0
velocities[0] = v0

# Function to compute acceleration due to gravity
def acceleration(r):
    r_norm = np.linalg.norm(r)
    return -mu / r_norm**3 * r

# Verlet integration
for i in range(1, num_steps):
    if i == 1:
        # First step using Euler's method to get the initial velocity half step
        positions[i] = positions[i-1] + velocities[i-1] * dt + 0.5 * acceleration(positions[i-1]) * dt**2
    else:
        positions[i] = 2 * positions[i-1] - positions[i-2] + acceleration(positions[i-1]) * dt**2
    velocities[i] = (positions[i] - positions[i-1]) / dt

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Orbit Simulation')

# Function to transform simulation coordinates to screen coordinates
def transform_coords(x, y, scale=1e-6):
    return int(x * scale + 600), int(-y * scale + 400)

# Main loop
running = True
clock = pygame.time.Clock()
index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear screen with black

    # Draw the Earth at the center
    pygame.draw.circle(screen, (0, 0, 255), (600, 400), 10)

    # Draw the Moon's orbit
    for i in range(1, len(positions)):
        x1, y1 = transform_coords(positions[i-1][0], positions[i-1][1])
        x2, y2 = transform_coords(positions[i][0], positions[i][1])
        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2))

    # Draw the Moon's current position
    moon_pos = transform_coords(positions[index][0], positions[index][1])
    pygame.draw.circle(screen, (255, 255, 255), moon_pos, 5)

    # Update the display
    pygame.display.flip()

    # Increment the index to move along the orbit
    index = (index + 1) % len(positions)

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
