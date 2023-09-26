class InvalidPointError(Exception):
    pass

class InvalidScalarError(Exception):
    pass

# This represents an elliptic curve of the form
#  y^2 = x^3 + ax + b mod p
class EllipticCurve():
    def __init__(self, a, b, p): 
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, point):
        if point is None:
            return True
        x, y = point
        return (y**2 % self.p) == (x**3 + self.a * x + self.b) % self.p

    def add(self, point1, point2):
        if not self.is_on_curve(point1) or not self.is_on_curve(point2):
            raise InvalidPointError("Invalid result")
        if point1 is None:
            return point2
        if point2 is None:
            return point1
        x1, y1 = point1
        x2, y2 = point2
        # vertical
        if x1 == x2 and y1 + y2 == 0 :
            return None  # Identity element
        if point1 == point2:
            return self.double(point1)
        else:
            if x1 == x2:
                return None   # Identity element
            m = (y2 - y1) * pow(x2 - x1, -1, self.p)

        x3 = (m**2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p

        return (x3, y3)
    
    def double(self, point):
        if not self.is_on_curve(point):
            raise InvalidPointError("Invalid result")
        if point is None:
            return None  # Identity element
        x1, y1 = point
        if y1 == 0:
            return None  # Identity element

        # s = (3 * x1^2 + a) / (2 * y1) mod p
        numerator = pow(x1, 2, self.p) * 3 + self.a
        denominator = (y1 * 2) % self.p
        s = (numerator * pow(denominator, -1, self.p)) % self.p

        x3 = (pow(s, 2, self.p) - x1 - x1) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p

        return (x3, y3)

    # Naive approach:
    # def scalar_mul(self, point, scalar):
    #     if scalar == 0:
    #         raise InvalidScalarError(scalar)

    #     result = None
    #     for _ in range(scalar):  # or range(scalar % N)
    #         result = self.add(result, point)
    #     return result
    
    # Optimized approach using binary expansion
    def scalar_mul(self, point, scalar):
        if scalar == 0:
            raise InvalidScalarError(scalar)

        current = point
        result = None
        while scalar:
            if scalar & 1:  # same as scalar % 2
                result = self.add(result, current)
            current = self.double(current)  # point doubling
            scalar >>= 1  # same as scalar / 2
        return result