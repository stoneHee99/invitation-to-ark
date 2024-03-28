from src.login import perform_login
from src.course_selector import get_course, select_course
from src.lecture_selector import get_lecture, select_lecture
from src.video_downloader import get_video, download_video
from src.alert_handler import handle_alert

import time

def main():
    email = input("이메일: ")
    password = input("비밀번호: ")

    driver = perform_login(email, password)

    time.sleep(2)

    courses = get_course(driver);
    course_titles = [course.text for course in courses]

    select_course(courses, course_titles)

    print("강의를 불러오고 있습니다 잠시만 기다려주세요")
    time.sleep(5)

    get_lecture(driver)


    while True:
        lecture_selected, lecture_title = select_lecture(driver)
        if lecture_selected:
            video_element = get_video(driver)
            download_video(video_element, lecture_title)
            handle_alert(driver)

        driver.switch_to.default_content()

        continue_download = input("더 다운로드할 강의가 있습니까? (y/n): ")
        handle_alert(driver)
        if continue_download.lower() != 'y':
            break

if __name__ == "__main__":
    main()

