import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 1111))
server.listen()
print("Сервер ждёт клиента...")

while True:
    conn, addr = server.accept()
    print("Подключился клиент:", addr)
    with conn:
        q = conn.recv(2048)
        data = q.decode("utf-8")
        conn.sendall(data.upper().encode("utf-8"))
    if data.strip().lower() == 'exit':
        break

server.close()
