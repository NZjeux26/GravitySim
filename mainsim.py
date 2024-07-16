import pygame
import sys
import time
import numpy as np
import math
import cProfile
import pstats
from objects import Constants, PointMass
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations

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
    position=[900e4,0.0,0.0],
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

def transform_position(position, window_size, scale_factor=1e-4):
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
        if obj.name not in ("planet", "sat", "moon"):
            cpositions[obj.name] = transform_position(obj.position, window_size)
    return c1_pos,c2_pos,c3_pos

#multi threaded N objects calculations
def process_obejcts(obejcts, dt):
    relevant_objects = [obj for obj in objects if obj.name not in ("sat", "moon")]
    
    with ThreadPoolExecutor() as executor:
        futures = []
        
        #RK4 checks all objects against the planet
        for obj1 in relevant_objects:
            if obj1.name != "planet":
                futures.append(executor.submit(rk4_intergration,obj1,next(obj for obj in objects if obj.name == "planet"),dt))
        
        #checks all objects with eachother.
        for obj1, obj2 in combinations(relevant_objects, 2):
            futures.append(executor.submit(rk4_intergration,obj1,obj2,dt))
        
        for future in as_completed(futures):
            future.result()
                 
num_objects = 5
objects = [planet, satellite, moon] #list of pointmasses
for i in range(num_objects):
    objects.append(PointMass(f"obj{i}",
                             [np.random.uniform(-1e7,1e7), np.random.uniform(-1e7,1e7), 0], #position
                              np.random.uniform(1,1e20), #mass ##the square brackets here were the issue
                              np.random.uniform(1,1e4), #radius
                             (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)), #colour
                             [0, np.random.uniform(-35000,35000), 0], #veloctiy
                             (0,0,0))) #acceleration
    
positions = { obj.name: [] for obj in objects }
cpositions = { obj.name: [] for obj in objects }

#actual drawing of obejcts on screen
circle_radius = 10
c1_pos = 0
c2_pos = 0 
c3_pos = 0
c1_pos, c2_pos, c3_pos = update_positons()
    
#set the starting velocity(ies)
satellite.velocity[1] = -get_starting_velocity(satellite)
moon.velocity[1] = -get_starting_velocity(moon)

# for obj in objects:
#     if obj.name not in ("planet", "sat", "moon"):
#         obj.velocity[1] = -get_starting_velocity(obj)
    
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
    rk4_intergration(moon,planet,dt)
    
    process_obejcts(objects, dt)
    # for obj in objects:
    #     if obj.name not in ("planet", "sat", "moon"):
    #         rk4_intergration(obj,planet,dt)
    #        for obj2 in objects:
    #            if obj2.name not in ("planet", "sat", "moon"):
    #                if obj.name != obj2.name:
    #                    rk4_intergration(obj,obj2,dt)
                    
    #checks for drawing traces. Only draw every modulus and reset counter every ten thousand
    pos_count +=1
    if pos_count % 10 == 0:
        for obj in objects:
            positions[obj.name].append(transform_position(obj.position, window_size))
        if pos_count > 10000:
            pos_count = 0
    
    #Calculate elapsed time
    elapsed_time = datetime.now() - start_time
    elapsed_time_str = str(elapsed_time).split('.')[0]  # Format as HH:MM:SS
    
    #update the position of the drawn obejct on screen##
    c1_pos, c2_pos, c3_pos = update_positons()
    
    #Draw
    window.fill((0,0,0))
    pygame.draw.circle(window, planet.colour, c1_pos, 30)
    pygame.draw.circle(window, satellite.colour, c2_pos, 4)
    pygame.draw.circle(window, moon.colour, c3_pos, 12)
    
    for obj in objects:
        if obj.name not in ("planet", "sat", "moon"):
            pygame.draw.circle(window, obj.colour, cpositions[obj.name], 2)
    
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

if __name__ == "__main__":
    cProfile.run('main()', 'profiling_results')
    p = pstats.Stats('profiling_results')
    p.sort_stats('cumulative').print_stats(20)
    
# Quit Pygame
pygame.quit()
sys.exit()

