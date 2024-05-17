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
    
        