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


def encrypt_message(private_key, message, seed, n_bits):

    bbs_generator = blum_blum_shub(*private_key, seed, n_bits)
    bits = list(bbs_generator)
    encrypted_message = [m ^ b for m, b in zip(message, bits)]
    return encrypted_message


def decrypt_message(encrypted_message, private_key, seed, n_bits):
    bbs_generator = blum_blum_shub(*private_key, seed, n_bits)
    bits = list(bbs_generator)
    decrypted_message = [em ^ b for em, b in zip(encrypted_message, bits)]
    return decrypted_message


private_key, public_key = generate_keys()

# Ваше повідомлення у вигляді цифри
message_number = 2

# Перетворення вашого повідомлення на бінарне представлення
message = [int(bit) for bit in format(message_number, '08b')]

# Кількість бітів, які потрібно згенерувати
n_bits = len(message)

# Шифрування повідомлення
encrypted_message = encrypt_message(private_key, message, 12345, n_bits)

# Виведення результатів
print("Зашифроване повідомлення:", encrypted_message)
print("Приватний ключ:", private_key)
print("Публічний ключ:", public_key)

# Розшифрування повідомлення
decrypted_message = decrypt_message(encrypted_message, private_key, 12345, n_bits)

# Виведення результату
print("Розшифроване повідомлення:", decrypted_message)

# Перетворення розшифрованого повідомлення назад у цифру
decrypted_message_number = int(''.join(map(str, decrypted_message)), 2)
print("Розшифроване повідомлення у вигляді цифри:", decrypted_message_number)

# import random
#
# def generate_prime_pair():
#     # Генерація двох простих чисел
#     p = random.randint(2**16, 2**32)
#     q = random.randint(2**16, 2**32)
#     return p, q
#
# # Ваш список
# lst = [1, 2, 23, 102, 3]
#
# # Створення словника
# dct = {key: generate_prime_pair() for key in lst}
#
# # Виведення словника
# print(dct)

# import random
# import math
# import sys
#
# def gcd(a, b):
#     while b != 0:
#         c = a % b
#         a = b
#         b = c
#     return a
#
# def modexp(base, exp, modulus):
#     return pow(base, exp, modulus)
#
# def jacobi(a, n):
#     if a == 0:
#         return 1 if n == 1 else 0
#     elif a == -1:
#         return 1 if n % 2 == 0 else -1
#     elif a == 1:
#         return 1
#     elif a == 2:
#         return 1 if n % 8 == 1 or n % 8 == 7 else -1 if n % 8 == 3 or n % 8 == 5 else 0
#     elif a >= n:
#         return jacobi(a % n, n)
#     elif a % 2 == 0:
#         return jacobi(2, n) * jacobi(a // 2, n)
#     else:
#         return -1 * jacobi(n, a) if a % 4 == 3 and n % 4 == 3 else jacobi(n, a)
#
# def SS(num, iConfidence):
#     for i in range(iConfidence):
#         a = random.randint(1, num - 1)
#         if gcd(a, num) > 1 or not jacobi(a, num) % num == modexp(a, (num - 1) // 2, num):
#             return False
#     return True
#
# def find_primitive_root(p):
#     if p == 2:
#         return 1
#     p1 = 2
#     p2 = (p - 1) // p1
#     while True:
#         g = random.randint(2, p - 1)
#         if not (modexp(g, (p - 1) // p1, p) == 1) and not modexp(g, (p - 1) // p2, p) == 1:
#             return g
#
# def find_prime(iNumBits, iConfidence):
#     while True:
#         p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))
#         while p % 2 == 0:
#             p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))
#         while not SS(p, iConfidence):
#             p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))
#             while p % 2 == 0:
#                 p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))
#         p = p * 2 + 1
#         if SS(p, iConfidence):
#             return p
#
# def encode(sPlaintext, iNumBits):
#     byte_array = bytearray(sPlaintext, 'utf-16')
#     z = []
#     if iNumBits % 8 != 0:
#         raise ValueError("Number of bits must be a multiple of 8")
#     k = iNumBits // 8
#     j = -1 * k
#     num = 0
#     for i in range(len(byte_array)):
#         if i % k == 0:
#             j += k
#             num = 0
#             z.append(0)
#         z[j // k] += byte_array[i] * (2 ** (8 * (i % k)))
#     return z
#
# def decode(aiPlaintext, iNumBits):
#     bytes_array = []
#     k = iNumBits // 8
#     for num in aiPlaintext:
#         for i in range(k):
#             temp = num
#             for j in range(i + 1, k):
#                 temp = temp % (2 ** (8 * j))
#             letter = temp // (2 ** (8 * i))
#             bytes_array.append(letter)
#             num = num - (letter * (2 ** (8 * i)))
#     decodedText = bytearray(b for b in bytes_array).decode('utf-16')
#     return decodedText
#
# def generate_keys(iNumBits=256, iConfidence=32):
#     p = find_prime(iNumBits, iConfidence)
#     g = find_primitive_root(p)
#     g = modexp(g, 2, p)
#     x = random.randint(1, (p - 1) // 2)
#     h = modexp(g, x, p)
#     publicKey = {'p': p, 'g': g, 'h': h, 'iNumBits': iNumBits}
#     privateKey = {'p': p, 'g': g, 'x': x, 'iNumBits': iNumBits}
#     return {'privateKey': privateKey, 'publicKey': publicKey}
#
# def encrypt(key, sPlaintext):
#     z = encode(sPlaintext, key['iNumBits'])
#     cipher_pairs = []
#     for i in z:
#         y = random.randint(0, key['p'])
#         c = modexp(key['g'], y, key['p'])
#         d = (i * modexp(key['h'], y, key['p'])) % key['p']
#         cipher_pairs.append([c, d])
#     encryptedStr = ""
#     for pair in cipher_pairs:
#         encryptedStr += str(pair[0]) + ' ' + str(pair[1]) + ' '
#     return encryptedStr
#
# def decrypt(key_tuple, cipher):
#     plaintext = []
#     p, g, x = key_tuple
#     cipherArray = cipher.split()
#     if not len(cipherArray) % 2 == 0:
#         return "Malformed Cipher Text"
#     for i in range(0, len(cipherArray), 2):
#         c = int(cipherArray[i])
#         d = int(cipherArray[i + 1])
#         s = modexp(c, x, p)
#         plain = (d * modexp(s, p - 2, p)) % p
#         plaintext.append(plain)
#     decryptedText = decode(plaintext, len(bin(p)) - 2)
#     decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])
#     return decryptedText
#
# # Generate keys
# keys = generate_keys()
#
# # Extract public and private keys
# public_key = keys['publicKey']
# private_key = keys['privateKey']
#
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
#
