import pickle

from vk_functions import *
from bbs import *
from elgamal import *

# Binary codes for change texts colors in console
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'


voter_ids = eval(receive_data(5010).decode('utf-8'))
print(voter_ids)

ids_and_key_pairs = {}
ids_and_private_keys = {}

for voter_id in voter_ids:
    public_key, private_key = generate_keys()
    ids_and_key_pairs[voter_id] = (private_key, public_key)
    ids_and_private_keys[voter_id] = private_key

print("ids_and_key_pairs:", ids_and_key_pairs)
print("ids_and_private_keys:", ids_and_private_keys)

tokens = []
for voter_id, (private_key, public_key) in ids_and_key_pairs.items():
    token = generate_token(voter_id, public_key)
    tokens.append(token)
print("tokens:", tokens)

send_data(str(tokens), 5001)
result = []
voted_voters_ids = []

# ------------ELGAMAL-----------------
keys = elgamal_generate_keys()
public_key_elgamal = keys['publicKey']
private_key_elgamal = keys['privateKey']
serialized_public_key_elgamal = pickle.dumps(public_key_elgamal)
#---------------------------------------

while True:
    if input('Введіть exit, якщо хочете вийти') == 'exit':
        print(result)
        break

    send_data(serialized_public_key_elgamal, 4999)
    encrypted_message = receive_data(5006).decode('utf-8')
    message = eval(decrypt((private_key_elgamal['p'], private_key_elgamal['g'], private_key_elgamal['x']), encrypted_message))
    print(message)

    encrypted_bullet = message[0]
    x0 = message[1]
    voter_id = message[2]
    print(encrypted_bullet, x0, voter_id)

    p, q = ids_and_private_keys[voter_id]
    binary_bullet = decrypt_bbs(encrypted_bullet, p, q, x0)
    print(binary_bullet)

    bullet = int(''.join(map(str, binary_bullet)), 2)
    print(bullet)
    if voter_id not in voted_voters_ids:
        voted_voters_ids.append(voter_id)
        result.append(bullet)
    else:
        print(f'{RED}Даний виборець вже проголосував{RESET}')


