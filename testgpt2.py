import numpy as np

class Constants:
    gravitational_constant = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2

class PointMass:
    def __init__(self, position, mass, radius, colour, velocity, acceleration):
        self.position = np.array(position)  # Position as a numpy array [x, y, z]
        self.mass = mass  # in kilograms
        self.radius = radius  # in meters
        self.colour = colour
        self.velocity = np.array(velocity)  # in m/s
        self.acceleration = np.array(acceleration)  # in m/s^2
        self.gForce = None  # This is in Newtons

    def cal_gForce(self, other_mass, distance):
        return Constants.gravitational_constant * (self.mass * other_mass) / distance**2

    def distance_to(self, other):
        dVector = self.position - other.position
        distance_km = np.linalg.norm(dVector)  # Distance in kilometers (assuming screen distance in km)
        distance_m = distance_km * 1000  # Convert to meters
        return distance_m + self.radius

    def acceleration_due_to_gravity(self, other):
        dVector = other.position - self.position
        distance = np.linalg.norm(dVector)
        unit_vector = dVector / distance
        acceleration_magnitude = -Constants.gravitational_constant * other.mass / distance**2
        return acceleration_magnitude * unit_vector

# Example usage
planet = PointMass([600, 400, 0], 5.972e24, 6371000, 'blue', [0, 0, 0], [0, 0, 0])
object_mass = PointMass([300, 600, 0], 1000, 1, 'red', [0, 0, 0], [0, 0, 0])

# Calculate the acceleration of the object mass due to the planet
object_mass.acceleration = object_mass.acceleration_due_to_gravity(planet)

print("Acceleration of the object mass:", object_mass.acceleration)
