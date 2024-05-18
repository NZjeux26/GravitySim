import math
import time
import numpy
import array

class Constants:
    gravitational_constant = 6.6740e-11

class PointMass:
    def __init__(self, xpos, ypos, zpos, mass, radius, colour, velocity, acceleration):
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.mass = mass #in Kilograms
        self.radius = radius #in meters
        self.colour = colour
        self.velocity = velocity #in m/s
        self.acceleration = acceleration, 
        self.gForce = None #This is in Newtons
    #see textfile for more information
    def cal_gForce(self,mass, distance):
        return Constants.gravitational_constant * (self.mass * mass) / distance**2
    #returns the distance between two point obejcts, adding the base distance from the centre of the first object
    def distance_to(self, other):
        dx = self.xpos - other.xpos
        dy = self.ypos - other.ypos
        dz = self.zpos - other.zpos
        
        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        
        return (distance * 1000) + self.radius #always need to include the distance from the centre of mass
    
        #Each Pixel is 1KM so the result in the test data says 360 so i need to times that by 1000 