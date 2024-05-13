import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame Window")

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update

    # Draw

    # Refresh display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
