import math


class Coulombs():
    def __init__(self, q1, q2, r, m):
        # Coulomb's constant
        self.k = 8.99e9  # in N m^2 / C^2
        self.q1 = q1  # Charge 1
        self.q2 = q2  # Charge 2
        self.r = r  # Initial distance between charges
        self.m = m  # Mass of the particle
        self.t = 0
        self.u = 0
        self.a = 0


        # Initial position
        self.x = r  # X-coordinate on the circle (initially at distance r)
        self.y = 0  # Y-coordinate on the circle (initially 0)

    def calculate_force(self):
        # Calculate force using Coulomb's Law
        qt = self.q1 * self.q2  # Product of charges
        denom = self.k * (self.r ** 2)  # Coulomb's constant and squared distance
        return qt / denom  # Force

    def calculate_displacement(self):
        self.t+=0.1
        acceleration = self.calculate_acceleration()
        part1 = self.u * self.t
        part2 = 0.5 * acceleration * self.t

    def calculate_acceleration(self):
        # Calculate the force
        force = self.calculate_force()
        acceleration = force / self.m

        # Now calculate the new position based on the updated radius
        self.x = self.r * math.cos(math.radians(45))  # Example angle 45° (could vary)
        self.y = self.r * math.sin(math.radians(45))  # Example angle 45° (could vary)

    def get_position(self):
        return (self.x, self.y)


# Example usage:
particle = Coulombs(q1=1e-6, q2=-1e-6, r=10, m=1)
particle.update_position()  # Update position based on force

print(particle.get_position())  # Get the new position of the particle
