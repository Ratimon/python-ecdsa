from python_ecdsa.elliptic_curve import EllipticCurve
import random
import hashlib

class BadArgumentError(Exception):
    pass

class OperationError(Exception):
    pass

# This represents the elliptic curve:

#  - the elliptic curve: y^2 = x^3 + ax + b mod p
#  - a generator point
#  - a curve order 
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
    
    def sign(self, message, priv_key, k_random):
        if message >= self.curve_order:
            raise BadArgumentError("Hash is bigger than the order of the EC group")

        if priv_key >= self.curve_order:
            raise BadArgumentError("Private key is bigger than the order of the EC group")

        if k_random >= self.curve_order:
            raise BadArgumentError("Random number `k` is bigger than the order of the EC group")

        r_point = self.elliptic_curve.scalar_mul(self.gen, k_random)

        if r_point is not None:
            r, _ = r_point
            s = (message + priv_key * r) * pow(k_random, -1, self.curve_order) % self.curve_order
            return r, s

        raise OperationError("Result k_random * a_gen is the identity")
    
    def verify(self, message, pub_key, signature):
        hash_value = self.generate_hash_less_than(message, self.curve_order)

        r, s = signature

        if hash_value >= self.curve_order:
            raise OperationError("Hash value >= q (EC group order)")

        s_inv = self.__inv_mul_prime(s, self.curve_order)
        u1 = (s_inv * hash_value) % self.curve_order
        u2 = (s_inv * r) % self.curve_order

        u1a = self.elliptic_curve.scalar_mul(self.gen, u1)
        u2b = self.elliptic_curve.scalar_mul(pub_key, u2)
        p = self.elliptic_curve.add(u1a, u2b)

        if p is not None:
            xp, _ = p
            return xp == r

        raise OperationError("Result is the identity")
    
    
    def generate_hash_less_than(self, message: int, max_value: int) -> int:
        # Convert the integer message to a string
        message_str = str(message)
        print("message_str=", message_str )

        # Hash the message using SHA-256 and convert it to a bytes object
        hash_bytes = hashlib.sha256(message_str.encode()).digest()
        print("hash_bytes=", hash_bytes )

        # Convert the hash_bytes to an integer
        message_hash = int.from_bytes(hash_bytes, byteorder='big')
        print("message_hash=",message_hash )

        print("max_value=", max_value )
        print(" pow(message_hash, 1, p)=",  pow(message_hash, 1, max_value-1) )
        # Ensure the hash value is less than max_value
        # message_hash %= max_value
        message_hash = pow(message_hash, 1, max_value-1)
        
        message_hash += 1
        print("message_hash=",message_hash )        
        return message_hash

    # def generate_hash_less_than(self, message: str, max_value: int) -> int:
    #     # Hash the message using SHA-256 and convert it to a bytes object
    #     hash_bytes = hashlib.sha256(message.encode()).digest()

    #     print("hash_bytes=",hash_bytes )

    #     # Convert the hash_bytes to an integer
    #     message_hash = int.from_bytes(hash_bytes, byteorder='big')

    #     print("hash_bytes=",message_hash )

    #     # Ensure the hash value is less than max_value and greater than zero
    #     message_hash %= max_value
    #     if message_hash == 0:
    #         message_hash += 1

    #     return message_hash
    

    # Finds the multiplicative inverse of an element in the set if p is a
    # prime number using Fermat's Little Theorem:
    #
    # `a^(-1) mod p = a^(p-2) mod p`
    #
    # Such that:
    # `a * a^(-1) = 1 mod p`
    #
    def __inv_mul_prime(self, a, p):
        if a >= p:
            raise OperationError("a must be less than p")

        # Calculate a^(-1) mod p using Fermat's Little Theorem
        a_inverse = pow(a, p - 2, p)

        return a_inverse

    # # Extended Euclidean Algorithm to calculate the modular multiplicative inverse of a mod m
    # def __inverse_mod_prime(self, a, m):
    #     if gcd(a, m) != 1:
    #         raise OperationError("Inverse does not exist")
    #     x, y, _, _ = self.__extended_gcd(a, m)
    #     return x % m

    # def __extended_gcd(self, a, b):
    #     if a == 0:
    #         return (0, 1, b, 0)
    #     x1, y1, gcd, q = self.__extended_gcd(b % a, a)
    #     x = y1 - (b // a) * x1
    #     y = x1
    #     return (x, y, gcd, q - (b // a) * y1)