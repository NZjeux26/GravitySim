import pygame
import sys
import time
import numpy as np
import math
from objects import Constants, PointMass
# Initialize Pygame
pygame.init()

# Set up the window
window_size = (1200, 800)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Two Body Simulation")
# Create a font object
font = pygame.font.SysFont(None, 24)
                        # x, y ,z
planet = PointMass(
    position=[600.0,400.0,0.0],
    mass=5.9722e24,
    radius=6.371e6,
    velocity=[0.0,0.0,0.0], #in m/s
    acceleration=[0.0,0.0,0.0], #in m/s^2
    colour=[125,100,100]
)

satellite = PointMass(
    position=[280.0,400.0,0.0],
    mass=100,
    radius=1,
    velocity=[0.0,7718.0,0.0], #need an intial velocity or else it'll jsut fall to the central mass
    acceleration=[1.0,0.0,0.0],#added an non-zero acceleration jsut to make sure there's no issues with the intergrations.
    colour=[255,255,255]
)

def draw_info(surface, font, satellite):
    velocity_text = f"Velocity: {satellite.velocity}"
    acceleration_text = f"Acceleration: {satellite.acceleration}"
    position_text = f"Position: {satellite.position}"
    alt_text = f"Altitude: {satalt}"
    theta_text = f"Theta: {theta}"
    velocityMag_text = f"Velocity_Mag: {satellite_velocity}"
    Orbit_amount_text = f"Orbit Count: {orbits}"
    delta_t = f"Delta T: {dt}"
    
    velocity_surface = font.render(velocity_text, True, (255, 255, 255))
    acceleration_surface = font.render(acceleration_text, True, (255, 255, 255))
    position_surface = font.render(position_text, True, (255, 255, 255))
    alt_sat = font.render(alt_text, True, (255, 255, 255))
    theta_sat = font.render(theta_text, True, (255, 255, 255))
    velocity_sat = font.render(velocityMag_text, True, (255, 255, 255))
    orbit_sat = font.render(Orbit_amount_text,True,(255,255,255))
    deltat = font.render(delta_t,True,(255,255,255))
    
    surface.blit(velocity_surface, (20, 20))
    surface.blit(acceleration_surface, (20, 50))
    surface.blit(position_surface, (20, 80))
    surface.blit(alt_sat, (20, 110))
    surface.blit(theta_sat, (20, 140))
    surface.blit(velocity_sat, (20, 170))
    surface.blit(orbit_sat, (20, 200))
    surface.blit(deltat, (20, 230))
    
grid_spacing = 50
# Function to draw the grid
def draw_grid():
    for x in range(0, window_size[0], grid_spacing):
        pygame.draw.line(window, [255,255,255], (x, 0), (x, window_size[1]))
    for y in range(0, window_size[1], grid_spacing):
        pygame.draw.line(window, [255,255,255], (0, y), (window_size[0], y))
#drawn objects

def leapfrog_integration(satellite, planet, dt): #most accurate under 5 orbits
    # Update velocity by half-step
    satellite.velocity += 0.5 * satellite.acceleration * dt
    # Update position
    satellite.position += (satellite.velocity / 1000)
    # Calculate new acceleration
    satellite.acceleration = satellite.acceleration_due_to_gravity(planet)
    # Update velocity by another half-step
    satellite.velocity += 0.5 * satellite.acceleration * dt

def euler_integration(satellite, planet, dt):
   # satellite.accleration = satellite.calculate_gravity(planet)
    satellite.acceleration = satellite.acceleration_due_to_gravity(planet)
    satellite.velocity += satellite.acceleration * dt
    satellite.position += (satellite.velocity / 1000) #convert into kilometers
    
def verlet_integration(satellite, planet, dt):
    acc_c = (satellite.acceleration_due_to_gravity(planet) / 1000)#convert to km/s
    satellite.velocity = (satellite.position - satellite.previous_position)
    new_pos = 2 * satellite.position - satellite.previous_position + (acc_c * dt) 
    satellite.previous_position = satellite.position #km
    satellite.position = new_pos #km
    satellite.velocity = (satellite.position - satellite.previous_position)

def rk4_intergration(satellite, planet, dt):# need to resolve the conversion to km for position. If i remove the DT from the kx_r then it's the excat same as Verlet and Euler
    def get_acceleration(position, velocity):
        temp_mass = PointMass(position,satellite.mass,satellite.radius,satellite.colour,(velocity), np.zeros_like(satellite.acceleration))
        return temp_mass.acceleration_due_to_gravity(planet)
    
    k1_v = dt * get_acceleration(satellite.position, (satellite.velocity))
    k1_r = (satellite.velocity / 1000)
    
    k2_v = dt * get_acceleration(satellite.position + 0.5 * k1_r, (satellite.velocity) + 0.5 * k1_v)
    k2_r = (satellite.velocity + 0.5 * k1_v) / 1000
    
    k3_v = dt * get_acceleration(satellite.position + 0.5 * k2_r, (satellite.velocity) + 0.5 * k2_v)
    k3_r = (satellite.velocity + 0.5 * k2_v) / 1000
    
    k4_v = dt * get_acceleration(satellite.position + 0.5 * k3_r, (satellite.velocity) + 0.5 * k3_v)
    k4_r = (satellite.velocity + 0.5 * k3_v) / 1000
    
    satellite.position +=(k1_r + 2*k2_r + 2*k3_r + k4_r) / 6 
    satellite.velocity +=(k1_v + 2*k2_v + 2*k3_v + k4_v) / 6
        
#actual drawing of obejcts on screen
circle_radius = 10
c1_pos = (planet.position[0],planet.position[1])
c2_pos = (int(satellite.position[0]), int(satellite.position[1]))
   
clock = pygame.time.Clock()
fps = 50 #50 ends up giving a dt of 0.021 which seems to really work well with the sim
positions = []
orbits = 0
in_start_area = False
has_left_start_area = False

# Time parameters
#dt = 1

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    dt = clock.tick(fps) / 1000.0
    
    #Euler Intergration.
    euler_integration(satellite, planet, dt)
    
    #Leapfrog integration
    #leapfrog_integration(satellite, planet, dt)
    
    #Verlet intergration()
    verlet_integration(satellite, planet, dt)
    
    #RK4 intergration()
   # rk4_intergration(satellite, planet, dt)
    #Add old position to array for drawing
    positions.append((int(satellite.position[0]), satellite.position[1])) #This WILL cause an oevrflow if left long enough
    
    # Check if satellite is in the starting area
    current_in_start_area = (200 < satellite.position[0] < 300) and (400 < satellite.position[1] < 500)
    
    if current_in_start_area:
        if not in_start_area and has_left_start_area:
            orbits += 1  #satellite has re-entered the starting area
            has_left_start_area = False
        in_start_area = True
    else:
        if in_start_area:
            has_left_start_area = True
        in_start_area = False
    
    #update onscreen numbers
    satalt = satellite.distance_to(planet)
    theta = satellite.get_theta_angle(planet)
    satellite_velocity = satellite.get_velocity(planet) 
    
    #update the position of the drawn obejct on screen
    c1_pos = (planet.position[0],planet.position[1])
    c2_pos = (int(satellite.position[0]), int(satellite.position[1]))
   
    #Draw
    window.fill((0,0,0))
    pygame.draw.circle(window, planet.colour, c1_pos, 25)
    pygame.draw.circle(window, satellite.colour, c2_pos, 5)
    #Draw orbit trace on screen
    if len(positions) > 1:
        for i in range(len(positions) - 1):
            pygame.draw.line(window,(205,205,205),positions[i], positions[i + 1], 1)

    #Draw information
    draw_info(window, font, satellite)
    draw_grid()
    
    #Refresh display
    pygame.display.flip()
    #Cap the frame rate to 60 FPS
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()


#Notes
#Observations:

#Euler Method
#< 10 orbits it's reasonably stable and accurate. However past like 25 it's about 25px and by 50 orbits it's either at 40px or flying off weirdly

#Leapfrog
#Most accurate under 10 orbits staying around 5-9 px. Above 25 it evens out to the same as Euler but is more stable over longer orbits 100+

#Verlet
#Same accuracy as Euler but doesn't tend ot fly off after 70 orbits

#RK
#Same as Verlet and Euler for under 10 orbits but above it slowly looses eneregy which is translating into a slow velocity and a high alt.