from vk_functions import *
from bbs import *

voter_ids = eval(receive_data(5000).decode('utf-8'))
print(voter_ids)

private_key, public_key = generate_keys()

ids_and_private_keys = {key: private_key for key in voter_ids}
print(ids_and_private_keys)

tokens = []
for voter_id in voter_ids:
    tokens.append(generate_token(voter_id, public_key))
print(tokens)

send_data(str(tokens), 5001)
