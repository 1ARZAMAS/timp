import socket

HOST = '127.0.0.1'
PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Подключено к серверу.")

    while True:
        msg = input("Введите сообщение (или 'exit' для выхода): ")
        if msg.lower() == 'exit':
            break
        client_socket.sendall(msg.encode())
        data = client_socket.recv(1024)
        print(f"Сервер ответил: {data.decode()}")
