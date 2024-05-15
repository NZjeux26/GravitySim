import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame Window")

#drawn objects

circle_radius = 50
c1_pos = (200,300)
c2_pos = (600, 300)


clock = pygame.time.Clock()
fps = 60

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update

    # Draw
    window.fill(255,255,255)
    pygame.draw.circle(window, 255,0,0, c1_pos, circle_radius)
    pygame.draw.circle(window, 0,255,0, c2_pos, circle_radius)
    # Refresh display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
