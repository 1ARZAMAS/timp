import socket
import threading

HOST = '127.0.0.1'
PORT = 1234

def handle_client(conn, addr):
    print(f"Подключился клиент {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[{addr}] >> {data.decode()}")
            conn.sendall(data)
    print(f"Клиент {addr} отключился")

# Основной сервер
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Активных подключений: {threading.active_count() - 1}")
