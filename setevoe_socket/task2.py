import socket
 
sites = ["python.org", "yandex.ru", "journal.top-academy.ru", "github.com"]
for site in sites:
    print(site, "-", socket.gethostbyname(site))