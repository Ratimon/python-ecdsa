from python_ecdsa.elliptic_curve import EllipticCurve

# This represents an elliptic curve of the form

#  an elliptic curve: y^2 = x^3 + ax + b mod p
#  a generator point
#  a curve order 
class ECDSA():
    def __init__(self, a, b, p, gen, c_order):

        self.elliptic_curve = EllipticCurve(a, b, p)
        self.gen = gen
        self.c_order = c_order
