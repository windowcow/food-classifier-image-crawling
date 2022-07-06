import os
import urllib
from urllib.parse import quote_plus
from selenium.webdriver.common.by import By

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
import time
import sys


start_dir = os.getcwd()
start_dir

# 초기 설정 값

# 스크롤 하고 로딩 기다리는 시간 (초)
SCROLL_PAUSE_SEC = 2

driver = webdriver.Chrome(ChromeDriverManager().install())


def download_images_with_keyword(keyword: str):
    # 최대 1분, 혹은 스크롤이 맨 아래까지 갈 때까지 아래로 스크롤
    try:
        scroll_down()
    except:
        pass

    # url만들기
    base_url = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="
    target_url = base_url + quote_plus(keyword)

    # driver가 target_url을 열도록 함
    driver.get(target_url)

    time.sleep(2)
    elements = driver.find_elements(By.CLASS_NAME, "_image._listImage")

    time.sleep(2)
    # elements은 이미지 다운로드할 수 있는 elements이 담긴 리스트

    # keyword와 같은 이름의 폴더를 만든다, pass는 이미 있는 경우를 위한거
    try:
        os.mkdir(keyword)
    except:
        pass

    # 만든 폴더로 작업 디렉토리를 옮긴다
    os.chdir(keyword)

    n = 0
    for element in elements:

        n += 1
        # element의 src 속성을 src_url에 저장
        src_url = element.get_attribute("src")

        # 그 url에서 다운로드 받는다, n은 몇 번째 사진인지
        urllib.request.urlretrieve(src_url, f"{keyword}_{n}")
        time.sleep(2)
    os.chdir(start_dir)
    return 0


def scroll_down():
    start_time = time.time()
    SCROLL_PAUSE_SEC = 2

    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        spent_time = time.time() - start_time()
        if (spent_time > 60):
            break

        # 끝까지 스크롤 다운
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


if __name__ == "__main__":
    sys.argv[1]
    download_images_with_keyword(sys.argv[1])
