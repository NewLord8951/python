import requests
import json
from urllib3.exceptions import InsecureRequestWarning

# Отключаем предупреждения SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class PasswordChecker:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.found_credentials = []
        
    def load_password_list(self, filename="passwords.txt"):
        """Загружает список паролей из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            # Стандартный список если файла нет
            return [
                "admin", "password", "1234", "12345", "123456", "12345678",
                "123456789", "password123", "admin123", "root", "default",
                "pass", "0000", "1111", "123", "secret", "qwerty", "password1"
            ]
    
    def check_basic_auth(self, url, username, password):
        """Проверяет Basic Authentication"""
        try:
            response = requests.get(
                url,
                auth=(username, password),
                timeout=5,
                verify=False,
                allow_redirects=False
            )
            return response.status_code == 200
        except:
            return False
    
    def check_login_form(self, url, username, password):
        """Проверяет вход через HTML форму"""
        try:
            # Разные варианты полей формы
            form_variants = [
                {"username": username, "password": password},
                {"user": username, "pass": password},
                {"login": username, "password": password},
                {"admin": username, "pwd": password}
            ]
            
            for form_data in form_variants:
                response = requests.post(
                    url,
                    data=form_data,
                    timeout=5,
                    verify=False,
                    allow_redirects=True
                )
                
                # Проверяем признаки успешного входа
                if response.status_code == 200:
                    if any(keyword in response.text.lower() for keyword in 
                          ["logout", "welcome", "dashboard", "status"]):
                        return True
                        
            return False
        except:
            return False
    
    def run_check(self):
        """Запускает проверку"""
        print(f"🎯 Начинаем проверку для {self.target_ip}")
        
        passwords = self.load_password_list()
        usernames = ["admin", "root", "administrator", "user"]
        ports = [80, 443, 8080]
        
        for port in ports:
            for protocol in ['http', 'https']:
                base_url = f"{protocol}://{self.target_ip}:{port}"
                
                # Пробуем разные эндпоинты
                endpoints = ["/", "/admin", "/login", "/web", "/gui"]
                
                for endpoint in endpoints:
                    url = base_url + endpoint
                    
                    print(f"🔍 Проверяем {url}")
                    
                    for username in usernames:
                        for password in passwords:
                            print(f"   Testing: {username}:{password}", end="\r")
                            
                            # Проверяем оба метода
                            if self.check_basic_auth(url, username, password):
                                print(f"\n✅ Найден Basic Auth: {username}:{password} на {url}")
                                self.found_credentials.append({
                                    "url": url,
                                    "username": username,
                                    "password": password,
                                    "method": "basic_auth"
                                })
                                return True
                                
                            if self.check_login_form(url, username, password):
                                print(f"\n✅ Найден доступ через форму: {username}:{password} на {url}")
                                self.found_credentials.append({
                                    "url": url,
                                    "username": username,
                                    "password": password,
                                    "method": "form_login"
                                })
                                return True
        
        print("\n❌ Доступные учетные данные не найдены")
        return False

# Использование
checker = PasswordChecker("192.168.88.1")
checker.run_check()
