import io
import pickle

from voter_functions import *
from bbs import *
from elgamal import *

candidates = [1, 2, 3, 4]
# ------------ELGAMAL-----------------
public_key_elgamal = pickle.load(io.BytesIO(receive_data(4999)))
#---------------------------------------

login = input('Login:')
password = input('Password:')
authorization = (login, password)
send_data(str(authorization), 5002)

if receive_data(5003) == b'0':
    raise Exception('Невірний логін чи пароль!')

token = input('Введіть токен:')
send_data(token, 5004)

if receive_data(5005) == b'0':
    raise Exception('Невірний токен!')


voter_id, public_key_bbs = decode_token(token)
print(voter_id, public_key_bbs)

bullet = choose_candidate(candidates)

binary_bullet = [int(bit) for bit in format(bullet, '08b')]


x0 = generate_x0_from_public_key(public_key_bbs)

encrypted_bullet = encrypt_bbs(binary_bullet, public_key_bbs, x0)


print("Початкове повідомлення:", binary_bullet)
print("Зашифроване повідомлення:", encrypted_bullet)

#E2(E1(M), x0, ID)

message = (encrypted_bullet, x0, voter_id)
encrypted_message = encrypt(public_key_elgamal, str(message))
print(encrypted_message)

send_data(str(encrypted_message), 5006)
