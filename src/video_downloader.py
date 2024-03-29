from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import requests

def get_video(driver):
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body')))

    kollus_player_iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[data-e2e="kollus-player"]'))
    )

    driver.switch_to.frame(kollus_player_iframe)

    return WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "kollus_player_html5_api"))
    )

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


def download_video(video_element, title):
    current_directory = os.getcwd()
    video_url = video_element.get_attribute('src')
    num_parts = 4
    final_filename = os.path.join(current_directory,
                                  title.replace(" ", "_") + ".mp4")
    response = requests.head(video_url)
    content_length = int(response.headers['Content-Length'])

    part_filenames = []
    tqdm_bar = tqdm(total=content_length, unit='iB', unit_scale=True)

    with ThreadPoolExecutor(max_workers=num_parts) as executor:
        futures = [executor.submit(download_chunk, video_url, {
            "Range": f"bytes={i * content_length // num_parts}-{(i + 1) * content_length // num_parts - 1}"},
                                   i * content_length // num_parts, (i + 1) * content_length // num_parts - 1, i,
                                   tqdm_bar) for i in range(num_parts)]

        for future in as_completed(futures):
            part_filenames.append(future.result())
    tqdm_bar.close()

    downloaded_size = sum(os.path.getsize(f) for f in part_filenames)
    if downloaded_size != content_length:
        print("비디오 다운로드 중 오류가 발생했습니다. 다운로드한 파일이 불완전하거나 손상될 수 있습니다.")
        for part_filename in part_filenames:
            os.remove(part_filename)
        return

    merge_files(part_filenames, final_filename)
    print(f"Video successfully downloaded and merged as {final_filename}")