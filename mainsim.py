import pygame
import sys
import time
import numpy as np
import math
from objects import Constants, PointMass
from datetime import datetime, timedelta
# Initialize Pygame
pygame.init()
### THINGS TO ADD ####


# Set up the window
window_size = (2560, 1440)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("N Body Simulation")
# Create a font object
font = pygame.font.SysFont(None, 24)
                        # x, y ,z
planet = PointMass( #even though this is called a planet let's just pretend it's a black hole with the mass of the earth. (which doesn't make sense with the radius but work with me.)
    position=[0.0,0.0,0.0],
    mass=5.9722e24,
    radius=6.371e6,
    velocity=[0.0,0.0,0.0], #in m/s
    acceleration=[0.0,0.0,0.0], #in m/s^2
    colour=[125,100,100],
    name="planet"
)

satellite = PointMass(
    position=[620e3,0.0,0.0], #the planet is the 0,0,0 (centre) so the position is now realtive to that. Currently that 320km + Planet Radius
    mass=100,
    radius=1,
    velocity=[0.0,0.0,0.0], #need an intial velocity or else it'll jsut fall to the central mass 35100.0 @300km || Using a neg number here instead of the position at the start since it's easier
    acceleration=[1.0,0.0,0.0],
    colour=[255,255,255],
    name="sat"
)

moon = PointMass(
    position=[38440,0.0,0.0],
    mass = 7.3476e22,
    radius = 1.737e6,
    velocity=[0.0,1022,0.0],#25930
    acceleration=[0.0,0.0,0.0],
    colour=[200,200,200],
    name="moon"
)
    
grid_spacing = 50
# Function to draw the grid
def draw_grid():
    for x in range(0, window_size[0], grid_spacing):
        pygame.draw.line(window, [255,255,255], (x, 0), (x, window_size[1]))
    for y in range(0, window_size[1], grid_spacing):
        pygame.draw.line(window, [255,255,255], (0, y), (window_size[0], y))

def transform_position(position, window_size, scale_factor=1e-3):
    transformed_x = int(position[0] * scale_factor) + window_size[0] // 2
    transformed_y = int(position[1] * scale_factor) + window_size[1] // 2
    return (transformed_x, transformed_y)

def leapfrog_integration(satellite, planet, dt):
    # Update velocity by half-step
    satellite.velocity += dt * 0.5 * satellite.acceleration
    # Update position
    satellite.position += satellite.velocity
    # Calculate new acceleration
    satellite.acceleration = planet.acceleration_due_to_gravity(satellite)
    # Update velocity by another half-step
    satellite.velocity += dt * 0.5 * satellite.acceleration

def euler_integration(satellite, planet, dt):
    satellite.acceleration = planet.acceleration_due_to_gravity(satellite)
    satellite.velocity += satellite.acceleration * dt
    satellite.position += satellite.velocity * dt
    
def verlet_integration(satellite, planet, dt):
    acc_c = planet.acceleration_due_to_gravity(satellite)  
    satellite.velocity = (satellite.position - satellite.previous_position)
    new_pos = 2 * satellite.position - satellite.previous_position + acc_c
    satellite.previous_position = satellite.position
    satellite.position = new_pos
    satellite.velocity = (satellite.position - satellite.previous_position)

def rk4_intergration(satellite, planet, dt):
    def get_acceleration(position, velocity):
        temp_mass = PointMass("temp",position,satellite.mass,satellite.radius,satellite.colour,(velocity), np.zeros_like(satellite.acceleration))
        return planet.acceleration_due_to_gravity(temp_mass)
    
    k1_v = dt * get_acceleration(satellite.position, (satellite.velocity))
    k1_r = dt * (satellite.velocity)
    
    k2_v = dt * get_acceleration(satellite.position + 0.5 * k1_r, (satellite.velocity) + 0.5 * k1_v)
    k2_r = dt * (satellite.velocity + 0.5 * k1_v)
    
    k3_v = dt * get_acceleration(satellite.position + 0.5 * k2_r, (satellite.velocity) + 0.5 * k2_v)
    k3_r = dt * (satellite.velocity + 0.5 * k2_v)
    
    k4_v = dt * get_acceleration(satellite.position + k3_r, (satellite.velocity) + k3_v)
    k4_r = dt * (satellite.velocity + k3_v)
    
    satellite.position +=(k1_r + 2*k2_r + 2*k3_r + k4_r) / 6 
    satellite.velocity +=(k1_v + 2*k2_v + 2*k3_v + k4_v) / 6

def get_starting_velocity(PointMass):
    v2 = Constants.mu_earth / PointMass.position[0]
    v = math.sqrt(v2)
    return v

def update_positons():
    c1_pos = transform_position(planet.position, window_size)
    c2_pos = transform_position(satellite.position, window_size)  
    c3_pos = transform_position(moon.position,window_size)
    
    for obj in objects:
        if obj.name != "planet" or obj.name != "sat" or obj.name != "moon":
            cpositions.append(transform_position(obj.position, window_size))

objects = [planet, satellite, moon] #list of pointmasses
for i in range(97):
    objects.append(PointMass(f"obj{i}",
                             [np.random.uniform(-1e6,1e6), np.random.uniform(-1e6,1e6), 0], #position
                             [np.random.uniform(1,1e6)], #mass
                             [np.random.uniform(1,1e4)], #radius
                             (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)), #colour
                             [0, np.random.uniform(-5e4,5e4), 0], #veloctiy
                             (0,0,0))) #acceleration
    
positions = { obj.name: [] for obj in objects }
cpositions = []

#actual drawing of obejcts on screen
circle_radius = 10
update_positons()

#need to have it so it only does from range 3-100
for obj in objects:
    if obj.name != "planet" or obj.name != "sat" or obj.name != "moon":
        cpositions.append(transform_position(obj.position,window_size))
    
#set the starting velocity(ies)
satellite.velocity[1] = -get_starting_velocity(satellite)

clock = pygame.time.Clock()
fps = 60


orbits = 0
pos_count = 0
in_start_area = False
has_left_start_area = False

# Time parameters
# Start time
start_time = datetime.now()

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    dt = 0.017#clock.tick(fps) / 1000.0
    
    #RK4 intergration()
    rk4_intergration(satellite, planet, dt) #grav influence of planet on the sat
    rk4_intergration(planet,satellite,dt) #grav influence of the sat on the planet
     
    pos_count +=1
    if pos_count % 10 == 0:
        for obj in objects:
            positions[obj.name].append(transform_position(obj.position, window_size))
        if pos_count > 10000:
            pos_count = 0
    
    #Check if satellite is in the starting area
    current_in_start_area = (300e3 < satellite.position[0] < 350e3) and (-50e3 < satellite.position[1] < 50e3)
    
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
    satalt = planet.distance_to(satellite) / 1000 #converted to km, taking away the radius so it's alt above the surface.
    #theta = planet.get_theta_angle(satellite)
    satellite_velocity = np.linalg.norm(satellite.velocity)
    
    #Calculate elapsed time
    elapsed_time = datetime.now() - start_time
    elapsed_time_str = str(elapsed_time).split('.')[0]  # Format as HH:MM:SS
    
    #update the position of the drawn obejct on screen##
    update_positons()
    
    #need to have it so it only does from range 3-100##
    for obj in objects:
        if obj.name != "planet" or "sat" or "moon":
            cpositions.append(transform_position(obj.position,window_size))
    ## could probably put this into it's own function to reduce copying
    #Draw
    window.fill((0,0,0))
    pygame.draw.circle(window, planet.colour, c1_pos, 30)
    pygame.draw.circle(window, satellite.colour, c2_pos, 4)
    pygame.draw.circle(window, moon.colour, c3_pos, 12)
    
    for obj in objects:
        if obj.name != "planet" or "sat" or "moon":
            pygame.draw.circle(window, obj.colour, cpositions, 2)
    
    #Draw orbit trace on screen
    for key, pos_list in positions.items():
        if len(pos_list) > 1:
            for i in range(len(pos_list) - 1):
                pygame.draw.line(window, (205, 205, 205), pos_list[i], pos_list[i + 1], 1)

    #Draw information
    #draw_info(window, font, satellite)
    #draw_grid()
    
    #Refresh display
    pygame.display.flip()
    #Cap the frame rate to 60 FPS
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()

