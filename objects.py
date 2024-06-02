import math
import time
import numpy as np

class Constants:
    gravitational_constant = 6.6740e-11
    mu_earth = 3.986004418e14  # in m^3 s^-2

class PointMass:
    def __init__(self, position, mass, radius, colour, velocity, acceleration):
        self.position = np.array(position)
        self.mass = mass #in Kilograms
        self.radius = radius #in meters
        self.colour = colour
        self.velocity = np.array(velocity) #in m/s
        self.acceleration = np.array(acceleration) #in m/s per second
        self.gForce = None #This is in Newtons
    
    #see textfile for more information
    def cal_gForce(self,other_mass, distance):
        return Constants.gravitational_constant * (self.mass * other_mass) / distance**2
 
    def distance_to(self, other):
        dVector = self.position - other.position
        distance = np.linalg.norm(dVector)
        #Each Pixel is 1KM so the result in the test data says 360 so i need to times that by 1000 
        return distance
    def acceleration_due_to_gravity(self,other):
        dVector = self.position - other.position # distance vector from self to the other point mass in pixels(km)
        distance_km = np.linalg.norm(dVector)  #Compute the Euclidean distance in km

        distance_m = distance_km * 1000 + other.radius #the distance including the radius to the centre in meters
        unit_vector = (dVector / distance_km) #the unit vector for the direction of the force
        acceleration_magnitude = -Constants.mu_earth / distance_m**2
        #acceleration_magnitude = -Constants.gravitational_constant * other.mass / distance_m**2  #magnitude of the acceleration due to gravity in meters ** This is actually the G force
        return acceleration_magnitude * (unit_vector * 1000) #Return the acceleration vector by multiplying the magnitude with the unit vector(converted to meters)
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
        r = other.radius + self.distance_to(other) * 1000 # centre of earth to surface + alt which are in KM then converted into meters
        v = math.sqrt(Constants.mu_earth / r)
        return v
    def get_orbital_period(self,other): # this is for a circular orbit
        r = self.distance_to(other) * 1000 
        v = self.get_velocity(other)
        c = 2 * math.pi * r
        
        period = c / v
        return period
        
