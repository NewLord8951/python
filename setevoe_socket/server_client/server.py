import socket
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()
print("Сервер ждёт клиента...")
 
conn, addr = server.accept()
print("Подключился клиент:", addr)
data = conn.recv(1024)
conn.sendall(data)
conn.close()
server.close()