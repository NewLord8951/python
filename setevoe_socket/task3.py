import socket
 
host = "python.org"
port = int(input("Введите порт для проверки: "))
 
try:
    with socket.create_connection((host, port), timeout=3):
        print(f"Порт {port} на {host} открыт")
except OSError:
    print(f"Порт {port} на {host} недоступен")