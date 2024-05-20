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
    position=[600.0,400.0,0.0],
    mass=5.9722e24,
    radius=6.371e6,
    velocity=[0.0,0.0,0.0], #in m/s
    acceleration=[0.0,0.0,0.0], #in m/s^2
    colour=[125,100,100]
)

satellite = PointMass(
    position=[300.0,600.0,0.0],
    mass=100,
    radius=1,
    velocity=[4500.0,7700.0,0.0], #need an intial velocity or else it'll jsut fall to the central mass
    acceleration=[0.0,0.0,0.0],
    colour=[255,255,255]
)

#drawn objects
#actual drawing of obejcts on screen
circle_radius = 10
c1_pos = (planet.position[0],planet.position[1])
c2_pos = (satellite.position[0], satellite.position[1])

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
    
    #calculate acceleration + velocity
    satellite.acceleration = satellite.acceleration_due_to_gravity(planet)
    satellite.velocity += satellite.acceleration * dt
    
    #add the velocity change to the position
    satellite.position += (satellite.velocity / 1000)#convert into kilometers
    
    #update the position of the drawn obejct on screen
    c1_pos = (planet.position[0],planet.position[1]) #redundant but maybe for later
    c2_pos = (satellite.position[0], satellite.position[1])
    
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
