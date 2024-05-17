import pygame
import sys
import time
from objects import Constants, PointMass
# Initialize Pygame
pygame.init()

# Set up the window
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame Window")

planet = PointMass(
    xpos=200,
    ypos=300,
    zpos=0,
    mass=1000e12 ,
    radius=1000000,
    velocity=[0,0,0],
    acceleration=[0,0,0]
)

moon = PointMass(
    xpos=600,
    ypos=300,
    zpos=0,
    mass=10000,
    radius=1000,
    velocity=[0,0,0],
    acceleration=[0,0,0]
)

#drawn objects

circle_radius = 50
c1_pos = (planet.xpos,planet.ypos)
c2_pos = (moon.xpos, moon.ypos)


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

    # Draw
    window.fill(255,255,255)
    pygame.draw.circle(window, 255,0,0, c1_pos, circle_radius)
    pygame.draw.circle(window, 0,255,0, c2_pos, circle_radius)
    
    # Refresh display
    pygame.display.flip()
    #Cap the frame rate to 60 FPS
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
