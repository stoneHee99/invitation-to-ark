from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_lecture(driver):
    current_url = driver.current_url
    modified_url = current_url.split('?')[0].replace('course-detail', 'classroom')

    driver.get(modified_url)
    wait_time = 10

    WebDriverWait(driver, wait_time).until(EC.url_contains("/content/"))

    wait_time = 10
    WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located((By.TAG_NAME, "footer"))
    )

    script = """
    document.getElementById('portal-container').style.display = 'none';
    """
    driver.execute_script(script)

    time.sleep(3)

    script = """
    var elements = document.querySelectorAll('div[class^="SenderButtonView__"]');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.display = 'none';
    }
    """
    driver.execute_script(script)

    time.sleep(5)

    svg_elements = driver.find_elements(By.CSS_SELECTOR, "svg path[fill='#AAAAAA']")

    for element in svg_elements:
        ActionChains(driver).move_to_element(element).click().perform()

    svg_elements2 = driver.find_elements(By.CSS_SELECTOR, "svg path[fill='#AAAAAA']")

    for element in svg_elements2:
        ActionChains(driver).move_to_element(element).click().perform()

def select_lecture(driver):
    index_links = driver.find_elements(By.XPATH, '//div[@data-e2e="index-link"]')
    titles = [link.find_element(By.CLASS_NAME, "info-title").text for link in index_links]

    print("강의 리스트:")
    for index, title in enumerate(titles):
        print(f"{index}: {title}")

    selected_index = int(input("강의 인덱스를 입력하세요: "))
    if 0 <= selected_index < len(titles):
        index_links[selected_index].click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body')))
        return True, titles[selected_index]
    else:
        print("잘못된 인덱스입니다.")
        return False, None