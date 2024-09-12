import math

class main:
    def __init__(self, s, u, v, a, t, f, q1, q2, r, m):
        # SUVATS
        self.s = 0
        self.u = 0
        self.v = 0
        self.a = 0
        self.t = 0
        # Coulombs
        self.f = 0
        self.q1 = q1
        self.q2 = q2
        k = 8.99 * 10 ^ 9
        self.r = r
        # Newton's second law
        self.mass = m
        # also uses F and a but they are already defined
        self.p2x = p2x
        self.p2y = p2y
        self.grad = 1

        def Coulombs(self):
            qt = self.q1 * self.q2
            denom = k * (r ^ 2)
            self.f = qt / denom

        def Nsl(self):
            self.a = self.f / self.m

        def suvat(self):
            step1 = self.u * self.t
            step2 = self.a * self.t ^ 2
            step3 = step2 * 0.5
            self.s = step1 + step3

        def get_p2x(self):
            return (self.p2x)

        def get_p2y(self):
            return (self.p2y)

        def line(self):
            grady = self.p2y - p1y
            gradx = self.p2y - p1y
            self.grad = gradient = grady / gradx


p1x = 0
p1y = 0
p2x = main.get_p2x()
p2y = main.get_p2y()

grady = p1y - p2y
gradx = p1y - p2y
gradient = grady / gradx
