import hashlib
import os
import socket
import threading
 
SAVE_DIR = "received"
MAX_SIZE = 10 * 1024 * 1024
os.makedirs(SAVE_DIR, exist_ok=True)
 
def reply(conn, text):
    conn.sendall((text + "\n").encode("utf-8"))
 
def parse_put(line):
    parts = line.split(" ", 2)
    if len(parts) != 3 or not parts[1].isdigit():
        return None
    name = os.path.basename(parts[2])
    if name in ("", ".", ".."):
        return None
    return name, int(parts[1])
 
def receive_file(f, path, size):
    sha = hashlib.sha256()
    left = size
    with open(path, "wb") as out:
        while left > 0:
            chunk = f.read(min(4096, left))
            if not chunk:
                break
            out.write(chunk)
            sha.update(chunk)
            left -= len(chunk)
    return left == 0, sha.hexdigest()
 
def handle_put(conn, f, line):
    request = parse_put(line)
    if request is None:
        reply(conn, "ERROR bad header")
        return
    name, size = request
    if size > MAX_SIZE:
        reply(conn, "ERROR file too big")
        return
    reply(conn, "READY")
    path = os.path.join(SAVE_DIR, name)
    complete, digest = receive_file(f, path, size)
    if complete:
        reply(conn, "OK " + digest)
        print("Получен файл:", name, size, "байт")
    else:
        reply(conn, "ERROR incomplete")
 
def handle_client(conn, addr):
    f = conn.makefile("rb")
    line = f.readline().decode("utf-8").strip()
    if line.startswith("PUT "):
        handle_put(conn, f, line)
    else:
        reply(conn, "ERROR unknown command")
    f.close()
    conn.close()

def listt():
    for elem in os.listdir(SAVE_DIR):
        sorted(elem)
        conn.sendall(elem.encode("utf-8"))
    


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 6000))
server.listen()
print("Файловый сервер запущен...")
 
while True:
    conn, addr = server.accept()
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.start()