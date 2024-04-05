import requests
from bs4 import BeautifulSoup
import time
import os
import math 

# ディレクトリを作成
if not os.path.exists('code_crawling'):
    os.mkdir('code_crawling')

# URLを設定
base_url = 'https://kotonaru.co.jp/internships?page='

# サイトのページ数を取得
response = requests.get(base_url + '1')
response.encoding = response.apparent_encoding
bs = BeautifulSoup(response.text, 'html.parser')
last_page_element = bs.find('li', class_='pager_last')
total_pages = int(last_page_element.find('a')['data-pager-page'])

# ページ数を動的に設定
for page_number in range(1, total_pages + 1):
    response = requests.get(base_url + str(page_number))
    time.sleep(1)
    response.encoding = response.apparent_encoding
    bs = BeautifulSoup(response.text, 'html.parser')

    with open('code_crawling/realestate_{}.html'.format(page_number), 'w') as file:
        file.write(response.text)

# 検収条件
# クロールしたHTMLの数を取得
html_files = [f for f in os.listdir('code_crawling') if f.endswith('.html')]
crawled_html_count = len(html_files)

# 検収条件を満たすかどうかを確認
if crawled_html_count == total_pages:
    print("クロールで取得したHTMLの数とサイトのページ数は一致しています")
else:
    print("クロールで取得したHTMLの数とサイトのページ数は一致していません")
