import math
import time
import numpy as np

class Constants:
    gravitational_constant = 6.6740e-11
    mu_earth = 3.986004418e14  # in m^3 s^-2

class PointMass:
    def __init__(self, name, position, mass, radius, colour, velocity, acceleration):
        self.name = name
        self.position = np.array(position) #in KM
        self.mass = mass #in Kilograms
        self.radius = radius #in meters
        self.colour = colour
        self.velocity = np.array(velocity) #in m/s
        self.acceleration = np.array(acceleration) #in m/s per second
        self.gForce = None #This is in Newtons
        self.previous_position = self.position - self.velocity  # Initialize previous position for Verlet integration

    #see textfile for more information
    def cal_gForce(self,other_mass, distance):
        return Constants.gravitational_constant * (self.mass * other_mass) / distance**2
 
    def distance_to(self, other):
        dVector = other.position - self.position
        distance = np.linalg.norm(dVector)
        
        return distance
    def acceleration_due_to_gravity(self,other):
        dVector = other.position - self.position# distance vector from self to the other point mass
        r = np.linalg.norm(dVector) #Compute the Euclidean distance
        if r == 0:
            raise ValueError("Collision detected or overlapping objects.")
        unit_vector = dVector / r #the unit vector for the direction of the force
        acceleration_magnitude = -Constants.gravitational_constant * self.mass / r**2 #using the mass instead of Mu so it's more polymorphic.
        return acceleration_magnitude * unit_vector #Return the acceleration vector by multiplying the magnitude with the unit vector
        #the returned acceleration vector is in m/s
   
    def get_theta_angle(self, other):
        dot_product = np.dot(self.position,other.position) #dot product of the two vectors
        mag1 = np.linalg.norm(self.position)  #norms of the vectors
        mag2 = np.linalg.norm(other.position)
        
        cos_theta = dot_product / (mag1 * mag2)
        theta_radians = np.arccos(cos_theta)
        theta_degrees = np.degrees(theta_radians)
        return theta_degrees
    def get_velocity(self,other): # this is for a circular orbit
        r = other.distance_to(self)
        v = math.sqrt(Constants.mu_earth / r)
        return v
    
    def get_orbital_period(self,other): # this is for a circular orbit
        r = other.distance_to(self)
        v = other.get_velocity(self)
        c = 2 * math.pi * r
        
        period = c / v
        return period   