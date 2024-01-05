import base64
import socket


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


def decode_token(token):
    decoded_data = base64.b64decode(token).decode()
    voter_id, secret_number = map(int, decoded_data.split(':'))
    return voter_id, secret_number


def choose_candidate(candidates):
    while True:
        candidate = int(input('Введіть номер кандидата:'))
        if candidate in candidates:
            break
        else:
            print('Кандидат невірний!')
            continue

    return candidate


