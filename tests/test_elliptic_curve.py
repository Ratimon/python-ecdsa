from python_ecdsa.elliptic_curve import EllipticCurve
from py_ecc.bn128 import  multiply, add, eq

def test_is_on_curve():
    ec = EllipticCurve(2, 2, 17)
    assert ec.is_on_curve((5, 1))
    assert not ec.is_on_curve((5, 3))  # A point not on the curve

from py_ecc.bn128 import eq

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

    

# def test_double():
#     ec = EllipticCurve(2, 2, 17)
#     point = (5, 1)
#     result = ec.double(point)
#     expected_result = multiply(point, 2)
#     assert eq(result, expected_result)

# def test_scalar_mul():
#     ec = EllipticCurve(2, 2, 17)
#     point = (5, 1)
#     scalar = 3
#     result = ec.scalar_mul(point, scalar)
#     expected_result = multiply(point, scalar)
#     assert eq(result, expected_result)