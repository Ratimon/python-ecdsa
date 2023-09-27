import random
from python_ecdsa.ecdsa import ECDSA

def test_sign_verify():
    # Define elliptic curve parameters (a, b, p),
    # generator point (gen), and
    # curve order (curve_order)
    a = 2
    b = 2
    p = 17
    gen = (5, 1)
    curve_order = 19

    ecdsa = ECDSA(a, b, p, gen, curve_order)

    priv_key = int(8) 
    # Generate a random private key
    # priv_key = ecdsa.generate_priv_key()
   
    # Generate a public key
    pub_key = ecdsa.generate_pub_key(priv_key)
    # priv_key, pub_key =ecdsa.generate_key_pair()

    k_random = int(18) 
    # Generate a random value for k
    # k_random = random.randint(1, curve_order - 1)

    message = "Bob -> 1 BTC -> Alice"
    hash_value = ecdsa.generate_hash_less_than(message, ecdsa.curve_order)
    signature = ecdsa.sign(hash_value, priv_key, k_random)
    is_valid = ecdsa.verify(hash_value, pub_key, signature)

    assert is_valid, "Verification should success"

def test_revert_when_tempered_msg_sign_verify():
    a = 2
    b = 2
    p = 17
    gen = (5, 1)
    curve_order = 19

    ecdsa = ECDSA(a, b, p, gen, curve_order)

    priv_key = int(8)
    # Generate a public key (replace with your logic)
    pub_key = ecdsa.generate_pub_key(priv_key)

    message1 = "Bob -> 1 BTC -> Alice"
    hash_value1 = ecdsa.generate_hash_less_than(message1, curve_order)

    k_random = 18
    signature = ecdsa.sign(hash_value1, priv_key, k_random)

    message2 = "Bob -> 2 BTC -> Alice"
    hash_value2 = ecdsa.generate_hash_less_than(message2, curve_order)

    verify_result = ecdsa.verify(hash_value2, pub_key, signature)

    assert not verify_result, "Verification should fail when the message is tempered"

def test_secp256_sign_verify():
    
    p_hex = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F"
    curve_order_hex = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141"

    gx_hex = "79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798"
    gy_hex = "483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8"

    a = 0
    b = 7
    p = int(p_hex, 16)
    curve_order = int(curve_order_hex, 16)
    gen = (int(gx_hex, 16), int(gy_hex, 16))

    ecdsa = ECDSA(a, b, p, gen, curve_order)

    priv_key = int(8)
    pub_key = ecdsa.generate_pub_key(priv_key)
    k_random_hex = "19BE666EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B15E81798"
    k_random = int(k_random_hex, 16)

    message = "Bob -> 1 BTC -> Alice"
    hash_value = ecdsa.generate_hash_less_than(message, ecdsa.curve_order)
    signature = ecdsa.sign(hash_value, priv_key, k_random)
    is_valid = ecdsa.verify(hash_value, pub_key, signature)

    assert is_valid, "Verification should success"