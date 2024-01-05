import random
import math
import sys


def gcd(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a


def modexp(base, exp, modulus):
    return pow(base, exp, modulus)


def jacobi(a, n):
    if a == 0:
        return 1 if n == 1 else 0
    elif a == -1:
        return 1 if n % 2 == 0 else -1
    elif a == 1:
        return 1
    elif a == 2:
        return 1 if n % 8 == 1 or n % 8 == 7 else -1 if n % 8 == 3 or n % 8 == 5 else 0
    elif a >= n:
        return jacobi(a % n, n)
    elif a % 2 == 0:
        return jacobi(2, n) * jacobi(a // 2, n)
    else:
        return -1 * jacobi(n, a) if a % 4 == 3 and n % 4 == 3 else jacobi(n, a)


def SS(num, iConfidence):
    for i in range(iConfidence):
        a = random.randint(1, num - 1)
        if gcd(a, num) > 1 or not jacobi(a, num) % num == modexp(a, (num - 1) // 2, num):
            return False
    return True


def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1
    while True:
        g = random.randint(2, p - 1)
        if not (modexp(g, (p - 1) // p1, p) == 1) and not modexp(g, (p - 1) // p2, p) == 1:
            return g


def find_prime(iNumBits, iConfidence):
    while True:
        p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))
        while p % 2 == 0:
            p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))
        while not SS(p, iConfidence):
            p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))
            while p % 2 == 0:
                p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))
        p = p * 2 + 1
        if SS(p, iConfidence):
            return p


def encode(sPlaintext, iNumBits):
    byte_array = bytearray(sPlaintext, 'utf-16')
    z = []
    if iNumBits % 8 != 0:
        raise ValueError("Number of bits must be a multiple of 8")
    k = iNumBits // 8
    j = -1 * k
    num = 0
    for i in range(len(byte_array)):
        if i % k == 0:
            j += k
            num = 0
            z.append(0)
        z[j // k] += byte_array[i] * (2 ** (8 * (i % k)))
    return z


def decode(aiPlaintext, iNumBits):
    bytes_array = []
    k = iNumBits // 8
    for num in aiPlaintext:
        for i in range(k):
            temp = num
            for j in range(i + 1, k):
                temp = temp % (2 ** (8 * j))
            letter = temp // (2 ** (8 * i))
            bytes_array.append(letter)
            num = num - (letter * (2 ** (8 * i)))
    decodedText = bytearray(b for b in bytes_array).decode('utf-16')
    return decodedText


def elgamal_generate_keys(iNumBits=256, iConfidence=32):
    p = find_prime(iNumBits, iConfidence)
    g = find_primitive_root(p)
    g = modexp(g, 2, p)
    x = random.randint(1, (p - 1) // 2)
    h = modexp(g, x, p)
    publicKey = {'p': p, 'g': g, 'h': h, 'iNumBits': iNumBits}
    privateKey = {'p': p, 'g': g, 'x': x, 'iNumBits': iNumBits}
    return {'privateKey': privateKey, 'publicKey': publicKey}


def encrypt(key, sPlaintext):
    z = encode(sPlaintext, key['iNumBits'])
    cipher_pairs = []
    for i in z:
        y = random.randint(0, key['p'])
        c = modexp(key['g'], y, key['p'])
        d = (i * modexp(key['h'], y, key['p'])) % key['p']
        cipher_pairs.append([c, d])
    encryptedStr = ""
    for pair in cipher_pairs:
        encryptedStr += str(pair[0]) + ' ' + str(pair[1]) + ' '
    return encryptedStr


def decrypt(key_tuple, cipher):
    plaintext = []
    p, g, x = key_tuple
    cipherArray = cipher.split()
    if not len(cipherArray) % 2 == 0:
        return "Malformed Cipher Text"
    for i in range(0, len(cipherArray), 2):
        c = int(cipherArray[i])
        d = int(cipherArray[i + 1])
        s = modexp(c, x, p)
        plain = (d * modexp(s, p - 2, p)) % p
        plaintext.append(plain)
    decryptedText = decode(plaintext, len(bin(p)) - 2)
    decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])
    return decryptedText


# # Generate keys
# keys = elgamal_generate_keys()
#
# # Extract public and private keys
# public_key = keys['publicKey']
# private_key = keys['privateKey']
# print(public_key)
# # Original message
# original_message = "Hello, this is a test message!"
#
# # Encrypt using the public key
# encrypted_message = encrypt(public_key, original_message)
#
# # Decrypt using the private key
# decrypted_message = decrypt((private_key['p'], private_key['g'], private_key['x']), encrypted_message)
#
# # Display results
# print("Original Message:", original_message)
# print("Encrypted Message:", encrypted_message)
# print("Decrypted Message:", decrypted_message)
