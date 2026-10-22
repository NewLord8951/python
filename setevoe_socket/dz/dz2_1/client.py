import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(3)

try:
    name = input("Введите имя: ")
    client.sendto(name.encode("utf-8"), ("127.0.0.1", 5001))
    data, addr = client.recvfrom(1024)
    print("Ответ:", data.decode("utf-8"))
except ConnectionError:
    print("Сервер недоступен")
finally:
    client.close()