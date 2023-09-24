# from py_ecc.bn128 import G1, multiply, add, eq

# This represents an elliptic curve of the form
#  y^2 = x^3 + ax + b mod p
class EllipticCurve():
    def __init__(self, a, b, p): 
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, point):
        x, y = point
        return (y**2 % self.p) == (x**3 + self.a * x + self.b) % self.p