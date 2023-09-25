from python_ecdsa.elliptic_curve import EllipticCurve
import random

# This represents an elliptic curve of the form

#  an elliptic curve: y^2 = x^3 + ax + b mod p
#  a generator point
#  a curve order 
class ECDSA():
    def __init__(self, a, b, p, gen, curve_order):

        self.elliptic_curve = EllipticCurve(a, b, p)
        self.gen = gen
        self.curve_order = curve_order

    def generate_key_pair(self):
        """Generates a key pair (private key, public key)."""
        priv_key = self.generate_priv_key()
        pub_key = self.generate_pub_key(priv_key)
        return priv_key, pub_key

    def generate_priv_key(self):
        """Generates a private key."""
        return self.generate_random_positive_number_less_than(self.curve_order)

    def generate_pub_key(self, priv_key):
        """Generates a public key given a private key."""
        return self.elliptic_curve.scalar_mul(self.gen, priv_key)

    def generate_random_positive_number_less_than(self, max_value):
        """Generates a random positive number less than a given maximum value."""
        return random.randint(1, max_value - 1)    
