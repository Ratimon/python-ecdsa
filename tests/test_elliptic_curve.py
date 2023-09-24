from python_ecdsa.elliptic_curve import EllipticCurve


def test_version():

    # y^2 = x^3 + 2x + 2 mod 17
    ec = EllipticCurve(2,2,17)

    assert ec.is_on_curve( (5,1) )
    