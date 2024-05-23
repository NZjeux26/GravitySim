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
        self.acceleration = np.array(acceleration), #in m/s per second
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
        return distance
        #return (distance * 1000) + self.radius
    
    #something is going very wrong in here
    def acceleration_due_to_gravity(self,other):
        dVector = self.position - other.position # distance vector from self to the other point mass in pixels(km)
        distance_km = np.linalg.norm(dVector)  #Compute the Euclidean distance in km

        distance_m = distance_km * 1000 + other.radius #the distance including the radius to the centre in meters
        unit_vector = (dVector / distance_km) #the unit vector for the direction of the force
        acceleration_magnitude = -Constants.gravitational_constant * other.mass / distance_m**2#magnitude of the acceleration due to gravity in meters
        return acceleration_magnitude * (unit_vector * 1000) #Return the acceleration vector by multiplying the magnitude with the unit vector(converted to meters)
        #the returned acceleration vector is in m/s
        #I could just leave it unchanged and get the output in km/s instead and do the math conversion on the other side?