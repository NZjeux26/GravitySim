import math
import time
import numpy
import array

class Constants:
    gravitational_constant = 6.6740e-11

class PointMass:
    def __init__(self, xpos, ypos, zpos, mass, radius, colour, velocity=array([0, 0, 0]), acceleration=array([0,0,0])):
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.mass = mass
        self.radius = radius
        self.colour = colour
        self.velocity = velocity
        self.acceleration = acceleration
    def cal_gForce(self,mass1, mass2, distance):
        return  Constants.gravitational_constant * (mass1 * mass2) / distance^2
    
        