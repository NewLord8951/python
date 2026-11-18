import hashlib
import os
import socket
 
def send_file(sock, path, size):
    sha = hashlib.sha256()
    sent = 0
    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sock.sendall(chunk)
            sha.update(chunk)
            sent += len(chunk)
            print(f"Отправлено {sent} из {size} байт")
    return sha.hexdigest()
 
path = input("Файл для отправки: ")
size = os.path.getsize(path)
name = os.path.basename(path)
 
sock = socket.create_connection(("127.0.0.1", 6000))
reader = sock.makefile("r", encoding="utf-8")
sock.sendall(f"PUT {size} {name}\n".encode("utf-8"))
 
answer = reader.readline().strip()
if answer == "READY":
    digest = send_file(sock, path, size)
    answer = reader.readline().strip()
    if answer == "OK " + digest:
        print("Файл получен, контрольная сумма совпала")
    else:
        print("Ошибка передачи:", answer)
else:
    print("Сервер отказал:", answer)
sock.close()