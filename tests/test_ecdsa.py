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

    # Generate a random private key
    # priv_key = ecdsa.generate_priv_key()
    # priv_key = random.randint(1, curve_order - 1)
    priv_key = int(7) 
    
    # Generate a public key
    public_key = ecdsa.generate_pub_key(priv_key)

    # Generate a random value for k
    # k_random = random.randint(1, curve_order - 1)
    k_random = int(18) 

    # Generate a message
    message = "Bob -> 1 BTC -> Alice"

    # Compute the hash of the message
    hash_value = ecdsa.generate_hash_less_than(message, ecdsa.curve_order)

    # Sign the message
    signature = ecdsa.sign(hash_value, priv_key, k_random)

    # Verify the signature
    is_valid = ecdsa.verify(hash_value, public_key, signature)

    assert is_valid == True