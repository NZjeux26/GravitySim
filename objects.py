import math
import time
import numpy as np
import array

class Constants:
    gravitational_constant = 6.6740e-11

class PointMass:
    def __init__(self, position, mass, radius, colour, velocity, acceleration):
        self.position = np.array(position)
        self.mass = mass #in Kilograms
        self.radius = radius #in meters
        self.colour = colour
        self.velocity = np.array(velocity) #in m/s
        self.acceleration = np.array(acceleration), 
        self.gForce = None #This is in Newtons
    #see textfile for more information
    def cal_gForce(self,other_mass, distance):
        return Constants.gravitational_constant * (self.mass * other_mass) / distance**2
    #returns the distance between two point obejcts, adding the base distance from the centre of the first object
    #the below is matching the known numbers from doing it manually so safe to say this function is fine...
    def distance_to(self, other):
        dVector = self.position - other.position
        distance = np.linalg.norm(dVector)
        #Each Pixel is 1KM so the result in the test data says 360 so i need to times that by 1000 
        return (distance * 1000) + self.radius
    
    #something is going very wrong in here
    def acceleration_due_to_gravity(self,other):
        dVector = self.position - other.position
        distance = np.linalg.norm(dVector)
        #the above is the same as the distance calculation do i need to add the distance to the centre of the first mass
        unit_vector = dVector / distance
        acceleration_magnitude = (-Constants.gravitational_constant * other.mass) / dVector**2
        return acceleration_magnitude * unit_vector
    