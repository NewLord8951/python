import socket
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5000))
 
while True:
    text = input("Введите сообщение (exit — выход): ")
    if text == "exit":
        break
    client.sendall(text.encode("utf-8"))
    data = client.recv(1024)
    print("Ответ:", data.decode("utf-8"))
 
client.close()
