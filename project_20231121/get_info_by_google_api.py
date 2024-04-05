import pandas as pd
import requests

# Google Maps Directions APIのキーを設定
api_key = ''

# 福井駅の緯度と経度
fukui_station_coords = '36.061,136.223'

# CSVファイルから大学の緯度経度情報を読み込む
univs_df = pd.read_csv('r0501univs_utf8.csv', on_bad_lines='error', delimiter='\t')

# ヘッダーの調査

# 移動時間が2時間以内の大学を格納するリストを初期化
reachable_univs = []

# 各大学に対して移動時間を調べる
for index, row in univs_df.iterrows():
    # 大学の郵便番号を取得し、上2桁を抽出
    zip_prefix = str(row['zip'])[:2]
    
    # 指定された地域番号に該当する場合のみ移動時間を調べる
    if zip_prefix in ['91', '92', '93', '94', '95', '52', '61', '50']:
        univ_coords = f"{row['lat']},{row['lon']}"

        # Google Maps Directions APIを使用して移動時間を取得
        directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={fukui_station_coords}&destination={univ_coords}&mode=driving&key={api_key}"

        response = requests.get(directions_url)
        directions_data = response.json()

        if directions_data['status'] == 'OK':
            # ルートが見つかった場合、最初のルートの移動時間（秒）を取得
            travel_time_secs = directions_data['routes'][0]['legs'][0]['duration']['value']

            # 移動時間が3600秒（1時間）以内の場合、リストに追加
            if travel_time_secs <= 7200:
                # リストに大学名を追加
                reachable_univs.append(row['name'])

# 結果をDataFrameに変換
reachable_univs_df = pd.DataFrame(reachable_univs, columns=['reachable_universities'])

# 結果を表示
print(reachable_univs_df)
