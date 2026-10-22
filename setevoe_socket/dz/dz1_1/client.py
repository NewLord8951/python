import socket
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 1111))
imya = input("Введите имя: ")
client.sendall(imya.encode("utf-8"))
data = client.recv(1024)
q = data.decode("utf-8")
print("Ответ:", q)
client.close()