import socket
import random


def send_data(data, port):
    s = socket.socket()
    s.connect(('127.0.0.1', port))
    if isinstance(data, str):
        s.send(data.encode())
    else:
        s.send(data)
    s.close()


def receive_data(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', port))
    s.listen(1)

    c, addr = s.accept()
    received_data = b''
    while True:
        chunk = c.recv(262144)
        if not chunk:
            break
        received_data += chunk

    c.close()
    s.close()
    return received_data


def generate_id():
    return random.randint(10000, 99999)


def check_user(login, password, users):
    for user in users:
        if user['login'] == login and user['password'] == password:
            return True
    return False


def check_token(login, serial_number_token, users):
    for user in users:
        if user['login'] == login and user['serial_number_token'] == serial_number_token:
            return True
    return False
