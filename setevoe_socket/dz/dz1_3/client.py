import socket
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 1111))
while True:
    soo = input("Введите сообщение: ")
    client.sendall(soo.encode("utf-8"))
    data = client.recv(2048)
    print("Ответ:", data.decode("utf-8"))
    if soo.strip().lower() == 'exit':
        break