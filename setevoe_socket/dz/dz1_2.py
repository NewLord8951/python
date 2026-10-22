import socket
 
host = ["python.org", "yandex.ru", "journal.top-academy.ru", "github.com"]

i = 0
while i < len(host):
    try:
        ip = socket.gethostbyname(host[i])
        print(f"{host[i]} - {ip}")
    except OSError:
        print("иди на")
    i+=1