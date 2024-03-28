from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def download_chunk(url, headers, start, end, part_num, tqdm_bar):
    """
    파일의 특정 부분을 다운로드하는 함수입니다. tqdm 진행률 표시줄을 업데이트합니다.
    """
    local_filename = f"part_{part_num}.tmp"
    with requests.get(url, headers=headers, stream=True) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                tqdm_bar.update(len(chunk))
    return local_filename


def merge_files(part_filenames, final_filename):
    """
    여러 부분 파일들을 하나의 파일로 병합합니다.
    """
    with open(final_filename, 'wb') as final_file:
        for part_filename in part_filenames:
            with open(part_filename, 'rb') as part_file:
                final_file.write(part_file.read())
            os.remove(part_filename)  # 병합 후 부분 파일 삭제


def download_video(url, num_parts, final_filename):
    """
    비디오를 여러 부분으로 나누어 다운로드하고 병합하는 함수입니다.
    """
    response = requests.head(url)
    content_length = int(response.headers['Content-Length'])

    part_filenames = []
    tqdm_bar = tqdm(total=content_length, unit='iB', unit_scale=True)

    with ThreadPoolExecutor(max_workers=num_parts) as executor:
        futures = [executor.submit(download_chunk, url, {
            "Range": f"bytes={i * content_length // num_parts}-{(i + 1) * content_length // num_parts - 1}"},
                                   i * content_length // num_parts, (i + 1) * content_length // num_parts - 1, i,
                                   tqdm_bar) for i in range(num_parts)]

        for future in as_completed(futures):
            part_filenames.append(future.result())

    tqdm_bar.close()

    # 모든 부분을 다운로드한 후 파일 병합
    merge_files(part_filenames, final_filename)

    print(f"Video successfully downloaded and merged as {final_filename}")


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--mute-audio")

# Service 객체를 사용하여 ChromeDriverManager의 인스턴스를 명시적으로 경로로 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 로그인 페이지로 이동
driver.get("https://skillflo.io/auth/signin")

# 사용자로부터 로그인 정보 입력받기
email = input("이메일: ")
password = input("비밀번호: ")

# 이메일 입력
email_input = driver.find_element(By.CSS_SELECTOR, "input[data-e2e='email']")
email_input.send_keys(email)

# 비밀번호 입력
password_input = driver.find_element(By.CSS_SELECTOR, "input[data-e2e='password']")
password_input.send_keys(password)

# 로그인 버튼 클릭
login_button = driver.find_element(By.CSS_SELECTOR, "button[data-e2e='login-btn']")
login_button.click()

print("----로그인 중----잠깐만--기다려-주세요----")
time.sleep(2)  # 필요한 경우 페이지 로딩 대기

driver.get("https://skillflo.io/mypage/course")

# 페이지가 완전히 로드될 때까지 기다립니다.
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.course-title")))

# 'course-title' 클래스를 가진 모든 div 태그를 찾아 강의명을 추출합니다.
courses = driver.find_elements(By.CSS_SELECTOR, "div.course-title")
course_titles = [course.text for course in courses]



while True:
    print("강의명 리스트:")
    for index, title in enumerate(course_titles):
        print(f"{index}: {title}")

    # 사용자로부터 강의 인덱스 입력 받기
    selected_index = int(input("강의 인덱스를 입력하세요: "))
    try:
        # 입력값을 정수로 변환
        selected_index = int(selected_index)

        if 0 <= selected_index < len(course_titles):
            courses[selected_index].click()
            break;
        else:
            print("잘못된 인덱스입니다. 다시 입력해주세요.")
            continue
    except ValueError:
        print("유효한 숫자를 입력해주세요.")


print("강의를 불러오고 있습니다 잠시만 기다려주세요")
time.sleep(5)  # 강의 페이지 로드 대기

current_url = driver.current_url

# URL 수정: 'course-detail'을 'classroom'으로 변경하고, 요청 파라미터 삭제
modified_url = current_url.split('?')[0].replace('course-detail', 'classroom')

# 수정된 URL로 이동
driver.get(modified_url)
wait_time = 10

# WebDriverWait와 EC를 사용하여 페이지가 완전히 로드될 때까지 대기
WebDriverWait(driver, wait_time).until(EC.url_contains("/content/"))

wait_time = 10
WebDriverWait(driver, wait_time).until(
    EC.visibility_of_element_located((By.TAG_NAME, "footer"))
)

script = """
document.getElementById('portal-container').style.display = 'none';
"""
driver.execute_script(script)

time.sleep(5)

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

while True:

    index_links = driver.find_elements(By.XPATH, '//div[@data-e2e="index-link"]')

    titles = []
    for index_link in index_links:
        try:
            title = index_link.find_element(By.CLASS_NAME, "info-title").text
            titles.append(title)
        except Exception as e:
            print(f"Error: {e}")

    for index, title in enumerate(titles):
        print(f"{index}: {title}")

    # 사용자로부터 title의 인덱스 입력 받기
    selected_title_index = input("선택할 title의 인덱스를 입력하세요: ")


    try:
        # 입력값을 정수로 변환
        selected_title_index = int(selected_title_index)
        # 선택된 title이 titles 리스트 범위 내에 있는지 확인
        if 0 <= selected_title_index < len(titles):
            # 선택된 title에 해당하는 index_links 요소 클릭
            index_links[selected_title_index].click()
            # 주의: 클릭 후 페이지가 새로 로드될 경우, 필요한 요소가 로드될 때까지 대기해야 할 수 있습니다.
            print(f"{titles[selected_title_index]} 페이지로 이동합니다.")
        else:
            print("잘못된 인덱스입니다. 다시 입력해주세요.")
    except ValueError:
        print("프로그램을 끝냅니다");
        break;

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body')))

    # 'data-e2e="kollus-player"' 속성을 가진 iframe 요소를 다시 찾습니다.
    kollus_player_iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[data-e2e="kollus-player"]'))
    )

    # 찾은 iframe으로 컨테이너를 전환합니다.
    driver.switch_to.frame(kollus_player_iframe)

    # 이제 iframe 내의 요소들과 상호작용할 수 있습니다. 예를 들어, 비디오 요소를 찾는 코드를 실행할 수 있습니다.
    video_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "kollus_player_html5_api"))
    )

    current_directory = os.getcwd()

    video_url = video_element.get_attribute('src')  # 비디오 URL 추출
    num_parts = 4  # 다운로드할 부분의 수를 정의 (네트워크 속도와 서버의 응답 능력에 따라 조정)
    final_filename = os.path.join(current_directory,
                                  titles[selected_title_index].replace(" ", "_") + ".mp4")

    download_video(video_url, num_parts, final_filename)

    print(f"Video successfully downloaded and saved as {final_filename}")

    driver.switch_to.default_content()


