from br_functions import *

potential_amount_of_voters = 9

voter_ids = []
for voter in range(potential_amount_of_voters):
    voter_ids.append(generate_id())
print(voter_ids)

send_data(str(voter_ids), 5000)

tokens = eval(receive_data(5001).decode('utf-8'))
print(tokens)

serial_numbers_of_tokens = {i: token for i, token in enumerate(tokens, 1)}

voter_1 = dict(name='Alisa', serial_number_token=1, login='alisa@gmail.com', password='76345')
voter_2 = dict(name='Bob', serial_number_token=2, login='bob@gmail.com', password='12345')
voter_3 = dict(name='Charlie', serial_number_token=3, login='charlie@gmail.com', password='23456')
voter_4 = dict(name='Dave', serial_number_token=4, login='dave@gmail.com', password='34567')
voter_5 = dict(name='Eve', serial_number_token=5, login='eve@gmail.com', password='45678')
voter_6 = dict(name='Frank', serial_number_token=6, login='frank@gmail.com', password='56789')
voter_7 = dict(name='Grace', serial_number_token=7, login='grace@gmail.com', password='67890')
voter_8 = dict(name='Heidi', serial_number_token=8, login='heidi@gmail.com', password='78901')
voter_9 = dict(name='Ivan', serial_number_token=9, login='ivan@gmail.com', password='89012')

users = [voter_1, voter_2, voter_3, voter_4, voter_5, voter_6, voter_7, voter_8, voter_9]

login, password = eval(receive_data(5002).decode('utf-8'))

print(check_user(login, password, users))

