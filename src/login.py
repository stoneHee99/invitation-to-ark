from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By

def perform_login(email, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--mute-audio")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://skillflo.io/auth/signin")

    email_input = driver.find_element(By.CSS_SELECTOR, "input[data-e2e='email']")
    email_input.send_keys(email)

    password_input = driver.find_element(By.CSS_SELECTOR, "input[data-e2e='password']")
    password_input.send_keys(password)

    login_button = driver.find_element(By.CSS_SELECTOR, "button[data-e2e='login-btn']")
    login_button.click()
    print("")
    print("로그인 중")
    print("")

    return driver;