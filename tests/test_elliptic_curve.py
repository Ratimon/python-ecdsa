from py_ecc.bn128 import  eq
from python_ecdsa.elliptic_curve import EllipticCurve

def test_is_on_curve():
    ec = EllipticCurve(2, 2, 17)
    assert ec.is_on_curve((5, 1))
    assert not ec.is_on_curve((5, 3))  # A point not on the curve

def test_add():
    # y^2 = x^3 + 2x + 2 mod 17
    ec = EllipticCurve(2, 2, 17)

    # (6,3) + (5,1) = (10,6)
    point1 = (6, 3)
    point2 = (5, 1)
    point3 = (10, 6)
    result = ec.add(point1, point2)
    assert eq(result, point3)

    # (5,1) + (5,1) = (6,3)
    point1 = (5, 1)
    point2 = (5, 1)
    point3 = (6, 3)
    result = ec.add(point1, point2)
    assert eq(result, point3)

    # (10, 6) + (5, 1) = (3,1)
    point1 = (10, 6)
    point2 = (5, 1)
    point3 = (3, 1)
    result = ec.add(point1, point2)
    assert eq(result, point3)

    # (16, 13) + (5, 1) = (0, 6)
    point1 = (16, 13)
    point2 = (5, 1)
    point3 = (0, 6)
    result = ec.add(point1, point2)
    assert eq(result, point3)

    # (6,3) + I = (6,3)
    point1 = (6, 3)
    result = ec.add(point1, None)
    assert eq(result, point1)

    # I + I = 2 * I = I
    result = ec.add(None, None)
    assert result is None

    # (5,16) + (5,1) = I
    point1 = (5, 16)
    point2 = (5, 1)
    result = ec.add(point1, point2)
    assert result is None

def test_double():
    # y^2 = x^3 + 2x + 2 mod 17
    ec = EllipticCurve(2, 2, 17)

    # (5,1) + (5,1) = 2 (5, 1) = (6,3)
    point1 = (5, 1)
    point3 = (6, 3)

    result = ec.double(point1)
    assert eq(result, point3)

    # I + I = 2 * I = I
    result = ec.double(None)
    assert result is None


def test_scalar_multiplication():
    # y^2 = x^3 + 2x + 2 mod 17
    ec = EllipticCurve(2, 2, 17)

    # Scalar multiplication (5,1) * 2 = (6,3)
    point1 = (5, 1)
    scalar = 2
    point2 = (6, 3)

    result = ec.scalar_mul(point1, scalar)
    assert eq(result, point2)

    # Scalar multiplication (5,1) * 10 = (7,11)
    point3 = (7, 11)
    scalar = 10

    result = ec.scalar_mul(point1, scalar)
    assert eq(result, point3)

    # Scalar multiplication (5,1) * 15 = (3,16)
    point4 = (3, 16)
    scalar = 15

    result = ec.scalar_mul(point1, scalar)
    assert eq(result, point4)

    # Scalar multiplication (5,1) * 16 = (10,11)
    point5 = (10, 11)
    scalar = 16

    result = ec.scalar_mul(point1, scalar)
    assert eq(result, point5)

    # Scalar multiplication (5,1) * 17 = (6,14)
    point6 = (6, 14)
    scalar = 17

    result = ec.scalar_mul(point1, scalar)
    assert eq(result, point6)

    # Scalar multiplication (5,1) * 18 = (5,16)
    point7 = (5, 16)
    scalar = 18

    result = ec.scalar_mul(point1, scalar)
    assert eq(result, point7)

    # Scalar multiplication (5,1) * 19 = None (Identity element)
    scalar = 19

    result = ec.scalar_mul(point1, scalar)
    assert result is None

    # Scalar multiplication (10,6) * 2 = (16,13)
    point8 = (10, 6)
    scalar = 2
    point9 = (16, 13)

    result = ec.scalar_mul(point8, scalar)
    assert eq(result, point9)