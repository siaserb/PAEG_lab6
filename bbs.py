import random
import math


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = gcd_extended(b % a, a)
        return g, y - (b // a) * x, x


def generate_x0(n):
    x0 = random.randint(2, n - 1)
    while math.gcd(x0, n) != 1:
        x0 = random.randint(2, n - 1)
    return x0


def generate_keys():
    while True:
        p = random.randint(100, 1000)
        q = random.randint(100, 1000)
        if is_prime(p) and is_prime(q) and p % 4 == 3 and q % 4 == 3:
            break

    n = p * q
    public_key = n
    private_key = (p, q)

    return public_key, private_key


def bbs_generator(n, x0, length):
    result = []
    xi = x0
    for _ in range(length):
        xi = pow(xi, 2, n)
        result.append(xi % 2)
    return result


def encrypt_bbs(message, n, x0):
    key_stream = bbs_generator(n, x0, len(message))
    ciphertext = [m ^ k for m, k in zip(message, key_stream)]
    return ciphertext


def decrypt_bbs(ciphertext, p, q, x0):
    n = p * q
    key_stream = bbs_generator(n, x0, len(ciphertext))
    decrypted_message = [c ^ k for c, k in zip(ciphertext, key_stream)]
    return decrypted_message


# Функція для генерації x0 за публічним ключем
def generate_x0_from_public_key(public_key):
    return generate_x0(public_key)



