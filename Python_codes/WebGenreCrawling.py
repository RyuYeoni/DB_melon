#멜론차트 //*[@id="gnb_menu"]/ul[1]/li[1]/a/span[2]
# 월간차트 //*[@id="gnb_menu"]/ul[1]/li[1]/div/ul/li[5]/a/span

# 2023 11월 월간차트를 장르별로 9개를 크롤링하여 곡 제목, 아티스트 이름, 앨범이름을 엑셀 파일에 저장
# 이후에 엑셀 파일에 장르별로 ID 부여하고, 중복값 제거해 나가면서, 아티스트이름,곡에 대한 ID 부여해서 데이터셋 완성

from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# 크롬 옵션 지정 지정
options = webdriver.ChromeOptions()

# 헤드리스 옵션 지정
# options.add_argument('--headless')

# 크롤링 막는 것을 피하기 위해 에이전트 입력 (사람처럼 보이게 하기)
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
options.add_argument('user-agent= '+ UserAgent)

# 드라이브 설정 (자동 다운로드 및 대기)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
driver.get(url='https://www.melon.com/index.htm')

driver.find_element(By.XPATH, '//*[@id="gnb_menu"]/ul[1]/li[1]/a/span[2]').click() # 멜론차트
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="gnb_menu"]/ul[1]/li[1]/div/ul/li[5]/a/span').click() # 월간
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="GN0100"]/a/span').click() # 장르
time.sleep(2)

# //*[@id="GN0100"]/a/span : 발라드
# //*[@id="GN0200"]/a/span : 댄스
# //*[@id="GN0300"]/a/span : 랩/힙합
# //*[@id="GN0400"]/a/span : R&B/Soul
# //*[@id="GN0500"]/a/span : 인디음악
# //*[@id="GN0600"]/a/span : 록/메탈
# //*[@id="GN0700"]/a/span : 트로트
# //*[@id="GN0800"]/a/span : 포크/블루스
# //*[@id="GN0900"]/a/span : POP


html = driver.page_source
soup = bs(html, 'html.parser')

songs = soup.select('tbody > tr')

song_list = []

for song in songs:
    title = song.find('div',class_='ellipsis rank01').text.strip().replace('\n','')
    artist = song.find('div', class_='ellipsis rank02').find('a').text.strip().replace('\n','')
    album = song.find('div',class_='ellipsis rank03').text.strip().replace('\n','')
    song_list.append([title,artist,album])

df = pd.DataFrame(song_list, columns=['title','artist','album'])


# 저장할 절대 주소
df.to_excel('/mnt/c/Users/Jose/Documents/Homeworks/MelonChart_goo.xlsx',index=False)