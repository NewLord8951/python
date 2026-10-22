import socket
 
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 5001))
print("UDP-сервер запущен...")

data, addr = server.recvfrom(1024)
print(addr)
server.sendto(f"Привет, {data.decode('utf-8')}!".encode("utf-8"), addr)
server.close()