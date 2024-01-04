import random


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def is_coprime(x, y):
    return gcd(x, y) == 1


def generate_prime():
    while True:
        p = random.randint(2 ** 16, 2 ** 32)
        for i in range(2, int(p ** 0.5) + 1):
            if p % i == 0:
                break
        else:
            if p % 4 == 3:
                return p


def generate_keys():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    return (p, q), n


def blum_blum_shub(p, q, seed, n_bits):
    n = p * q
    if not is_coprime(seed, n):
        raise ValueError("seed повинен бути взаємно простим з n.")
    x = seed
    for _ in range(n_bits):
        x = (x * x) % n
        yield x % 2


def encrypt_message(message, seed, n_bits):
    private_key, public_key = generate_keys()
    bbs_generator = blum_blum_shub(*private_key, seed, n_bits)
    bits = list(bbs_generator)
    encrypted_message = [m ^ b for m, b in zip(message, bits)]
    return encrypted_message, private_key, public_key


def decrypt_message(encrypted_message, private_key, seed, n_bits):
    bbs_generator = blum_blum_shub(*private_key, seed, n_bits)
    bits = list(bbs_generator)
    decrypted_message = [em ^ b for em, b in zip(encrypted_message, bits)]
    return decrypted_message