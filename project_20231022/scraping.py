#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import os
import re
import pandas as pd
import csv
import math

# 切り上げのためにmathモジュールをインポート

# ヘッダーを設定
HEADER = [
    'city',
    'ward',
    'access_time',
    'train_line',
    'station',
    'price',
    'area',
    'room_layout',
    'direction',
    'year',
    'num_floor',
    'num_room'
]

# URLを設定
base_url = 'https://www.nomu.com/mansion/SearchList/?pkg=mansion&wide=14&type=area&wide_name=kanagawa&area_group_cd=C&area_id[]=14101&area_id[]=14102&area_id[]=14103&area_id[]=14104&area_id[]=14105&area_id[]=14106&area_id[]=14107&area_id[]=14108&area_id[]=14109&area_id[]=14110&area_id[]=14111&area_id[]=14112&area_id[]=14113&area_id[]=14114&area_id[]=14115&area_id[]=14116&area_id[]=14117&area_id[]=14118&area_id[]=14131&area_id[]=14132&area_id[]=14133&area_id[]=14134&area_id[]=14135&area_id[]=14136&area_id[]=14137&area_id[]=14151&area_id[]=14152&area_id[]=14153&area_id[]=14201&area_id[]=14203&area_id[]=14204&area_id[]=14205&area_id[]=14207&area_id[]=14208&area_id[]=14210&area_id[]=14212&area_id[]=14213&area_id[]=14215&area_id[]=14216&area_id[]=14301&area_id[]=143201&pager_page='

# ページ数を計算
response = requests.get(base_url + '1')
soup = BeautifulSoup(response.text, 'html.parser')
total_items = int(soup.find('div', class_='search_total').find('span').text)
items_per_page = 30
total_pages = math.ceil(total_items / items_per_page)

# データを格納する空のリストを作成
data = []

# クロール済みHTMLファイルが保存されたディレクトリ
crawled_dir = 'code_crawling'

# 各HTMLファイルをスクレイピング
for page_count in range(1, total_pages + 1):
    # クローリング対象のHTMLファイルのリストを取得
    html_file = f'page_{page_count}.html'

    with open(os.path.join(crawled_dir, html_file), 'r') as file:
        html_content = file.read()
    bs = BeautifulSoup(html_content, 'html.parser')

    # 所在地の取得
    location_elements = bs.find_all('p', class_='item_location')
    # 駅からの所要時間と最寄りの路線と駅の名前の取得
    access_elements = bs.find_all('p', class_='item_access')
    # 価格の取得
    price_elements = bs.find_all('p', class_='item_price')
    # 面積、間取り、方位の取得
    td_elements_1 = bs.find_all('td', class_='item_td item_4')
    # 年、階数、部屋数の取得
    td_elements_2 = bs.find_all('td', class_='item_td item_5')

    # ページ内のデータを取得
    for i in range(len(location_elements)):
        # 所在地のテキストを取得し、前後の空白を削除
        location_text = location_elements[i].text.strip()

        # 駅からの所要時間と最寄りの路線と駅の名前のテキストを取得し、前後の空白を削除
        access_text = access_elements[i].text.strip()

        # 価格の要素を取得
        price_element = price_elements[i]

        # 価格のテキストを取得し、各<span>要素内のテキストを結合
        price = ''.join([span.get_text() for span in price_element.find_all('span', class_='num')])

        # 面積、間取り、方位のテキストを取得し、正規表現を用いて情報を抽出
        text = td_elements_1[i].get_text(strip=True)
        area_match = re.search(r'(\d+\.\d+)', text)
        room_layout_match = re.search(r'(\d{1}[LDK+S]+)', text)
        direction_match = re.search(r'([東西南北]+)$', text)

        # 年、階数、部屋数のテキストを取得し、必要な情報を抽出
        year = td_elements_2[i].find('p').get_text().strip().split('年')[0]
        num_floor = td_elements_2[i].find_all('p')[1].get_text().strip().split('/')[1].replace('階建', '')
        num_room = td_elements_2[i].find_all('p')[2].get_text().strip().replace('戸', '')

        # 市と区の初期値を設定
        city = "NA"
        ward = "NA"

        # 所在地に「横浜市」または「川崎市」が含まれているか確認
        if "横浜市" in location_text or "川崎市" in location_text:
            # 市を取得し、"市"を含める
            city = location_text.split("市")[0] + "市"

            # 区を正規表現を用いて抽出
            ward_match = re.search(r"(?:横浜市|川崎市)(.+)区", location_text)
            if ward_match:
                ward = ward_match.group(1) + "区"
        else:
            # 市のみを取得
            city_match = re.search(r"(.+市)", location_text)
            if city_match:
                city = city_match.group(1)

        # 駅からの所要時間を正規表現を用いて
        access_time_match = re.search(r'\d+', access_text)
    
        # 最寄りの路線を正規表現を用いて抽出
        train_line_match = re.search(r'(\S+)「', access_text)
    
        # 駅の名前を正規表現を用いて抽出
        station_match = re.search(r'「([^「]+)」', access_text)
    
        # 抽出した情報を変数に代入し、取得できない場合は"NA"を設定
        access_time = access_time_match.group() if access_time_match else "NA"
        train_line = train_line_match.group(1) if train_line_match else "NA"
        station = station_match.group(1) if station_match else "NA"
    
        # 面積、間取り、方位の情報を取得し、取得できない場合は"NA"を設定
        area = area_match.group(1) if area_match else "NA"
        room_layout = room_layout_match.group(1) if room_layout_match else "NA"
        direction = direction_match.group(1) if direction_match else "NA"
    
        # データリストに情報を追加
        data.append([
            city,
            ward,
            access_time,
            train_line,
            station,
            price,
            area,
            room_layout,
            direction,
            year,
            num_floor,
            num_room,
        ])

# データをPandas DataFrameに変換
df = pd.DataFrame(data, columns=HEADER)

# データをCSVファイルに保存
if not os.path.exists('result_file'):
    os.mkdir('result_file')

csv_file_path = 'result_file/result.csv'
df.to_csv(csv_file_path, index=False, encoding='shift-jis')

print("CSVファイルにデータを保存しました:", csv_file_path)

# 検収条件
# CSVファイルの行数をカウント
with open(csv_file_path, 'r', encoding='shift-jis') as csvfile:
    csvreader = csv.reader(csvfile)
    # ヘッダー行をスキップ
    next(csvreader, None)
    row_count = sum(1 for row in csvreader)

# 行数を検証
if row_count == total_items:
    print("データの数は一致しています")
else:
    print("データの数は一致しませんでした")
