import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# URL
login_url = 'https://eduway.kz/login'
username = "urnickname"
password = "ifitneeds"  


session = requests.Session()


def get_login_token(session):
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    csrf_token = soup.find('input', {'name': '_csrf'})
    
    
    return csrf_token['value'] if csrf_token else None


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


if login_with_requests(session, username, password):
   
    driver_path = 'drivers/chromedriver.exe'
    service = Service(driver_path)
    driver = webdriver.Chrome(service = service)

    try:
     
        driver.get("https://eduway.kz/student")  
        for cookie in session.cookies:
            driver.add_cookie({'name': cookie.name, 'value': cookie.value})

       
        driver.get("https://eduway.kz/student/exam-results")
        time.sleep(2)  

        
        driver.get("https://eduway.kz/student/exam-results/exam/29")
        time.sleep(2)

       
        page_content = driver.find_element(By.TAG_NAME, 'body').text
        print("Содержимое страницы:")
        print(page_content)

    finally:
        driver.quit()
else:
    print("Не удалось выполнить вход через requests.")
