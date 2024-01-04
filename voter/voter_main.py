from voter_functions import *

login = input('Login:')
password = input('Password:')
authorization = (login, password)
send_data(str(authorization), 5002)

