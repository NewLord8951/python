import socket
 
name = socket.gethostname()
ip = socket.gethostbyname(name)
print("Компьютер:", name)
print("IP-адрес:", ip)