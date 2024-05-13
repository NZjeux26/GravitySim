import math
import time
import numpy
import array

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
        