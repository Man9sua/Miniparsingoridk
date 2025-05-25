import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# URL для логина
login_url = 'https://eduway.kz/login'
username = "Mansua"
password = "Mansur09"  # Используйте безопасный способ хранения пароля, например, переменные окружения

# Настраиваем сессию для работы с requests
session = requests.Session()

# Функция для получения CSRF токена
def get_login_token(session):
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем скрытое поле для CSRF-токена
    csrf_token = soup.find('input', {'name': '_csrf'})
    
    # Если находим токен, возвращаем его значение, иначе None
    return csrf_token['value'] if csrf_token else None

# Попытка входа в систему
def login_with_requests(session, username, password):
    csrf_token = get_login_token(session)
    if not csrf_token:
        print("CSRF token not found")
        return False

    data = {
        'username': username,
        'password': password,
        '_csrf': csrf_token
    }

    response = session.post(login_url, data=data, allow_redirects=True)
    if 'student' in response.url:
        print("Login successful")
        return True
    else:
        print("Login failed")
        return False

# Пытаемся выполнить вход
if login_with_requests(session, username, password):
    # Настраиваем Selenium для перехода на страницу после логина
    driver_path = 'drivers/chromedriver.exe'
    service = Service(driver_path)
    driver = webdriver.Chrome(service = service)

    try:
        # Переносим cookies из requests в браузер
        driver.get("https://eduway.kz/student")  # Инициализируем сессию в браузере
        for cookie in session.cookies:
            driver.add_cookie({'name': cookie.name, 'value': cookie.value})

        # Переходим на страницу с результатами экзаменов
        driver.get("https://eduway.kz/student/exam-results")
        time.sleep(2)  # Даем время на загрузку страницы

        # Переходим на страницу с конкретными результатами экзамена
        driver.get("https://eduway.kz/student/exam-results/exam/29")
        time.sleep(2)

        # Получаем содержимое страницы
        page_content = driver.find_element(By.TAG_NAME, 'body').text
        print("Содержимое страницы:")
        print(page_content)

    finally:
        driver.quit()
else:
    print("Не удалось выполнить вход через requests.")
