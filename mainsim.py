import pygame
import sys
import time
from objects import Constants, PointMass
# Initialize Pygame
pygame.init()

# Set up the window
window_size = (1200, 800)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame Window")

planet = PointMass(
    position=[600,400,0],
    mass=5.9722e24,
    radius=6.371e6,
    velocity=[0,0,0], #in m/s
    acceleration=[0,0,0], #in m/s^2
    colour=[125,100,100]
)

satellite = PointMass(
    position=[300,600,0],
    mass=100,
    radius=1,
    velocity=[0,3000,0], #need an intial velocity or else it'll jsut fall to the central mass
    acceleration=[0,0,0],
    colour=[255,255,255]
)

#drawn objects
#actual drawing of obejcts on screen
circle_radius = 10
c1_pos = (planet.position[0],planet.position[1])
c2_pos = (satellite.position[0], satellite.position[1])

#distance is from the CENTRE of the masses, so for earth it's 6371km from the centre to the surface
# you need to add the distance from the sruface to the orbit of the satellite ONTOP of this value
# planet.gForce = planet.cal_gForce(satellite.mass, 6.371e6)

# print("planet.gForce = %f" % planet.gForce)

# G = Constants.gravitational_constant * (planet.mass / planet.radius**2)
# dVector = planet.distance_to(satellite)

# A = (-Constants.gravitational_constant * planet.mass) / dVector**2
# print("gravity = %f" % G)
# print("Acc = %f" % A) # This is coming in at a very low amount, the math is right so maybe the formula isn't

# print("dVector = %f" % dVector)
clock = pygame.time.Clock()
fps = 60

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    dt = clock.tick(fps) / 1000.0
    
    # Update
    satellite.acceleration = satellite.acceleration_due_to_gravity(planet)
    
    satellite.velocity += (satellite.acceleration * dt)
    satellite.position += satellite.velocity
    
    # Draw
    window.fill((0,0,0))
    pygame.draw.circle(window, planet.colour, c1_pos, 25)
    pygame.draw.circle(window, satellite.colour, c2_pos, circle_radius)
    
    # Refresh display
    pygame.display.flip()
    #Cap the frame rate to 60 FPS
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
