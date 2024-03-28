from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_course(driver):
    driver.get("https://skillflo.io/mypage/course")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.course-title")))

    courses = driver.find_elements(By.CSS_SELECTOR, "div.course-title")
    return courses

def select_course(courses, course_titles):
    print("강의명 리스트:")
    for index, title in enumerate(course_titles):
        print(f"{index}: {title}")

    selected_index = int(input("강의 인덱스를 입력하세요: "))
    if 0 <= selected_index < len(course_titles):
        courses[selected_index].click()
    else:
        print("잘못된 인덱스입니다.")