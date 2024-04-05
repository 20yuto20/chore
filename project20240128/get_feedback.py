import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import warnings
import os
import time
from gspread.exceptions import APIError


##ドライブとシート操作に必要なAPI情報
SP_CREDENTIAL_FILE = 'secret.json'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, scope)
client = gspread.authorize(creds)

##今回目的とするcsv
accepted_students = pd.read_csv('accepted_students.csv')

##今回情報を取得してくる先
sheet_mapping = {}
with open('sheet_id.txt', 'r') as file:
    for line in file:
        name, sheet_id = line.strip().split(': ')
        sheet_mapping[name.strip()] = sheet_id.strip()
        
##今回の目的のcsvと企業情報が格納されているものが一致するかどうかを判断する関数

unmatched_sheets = []

def fetch_student_info_from_sheet(partial_sheet_name, student_name, client, sheet_mapping):
    matched_sheet_id = None
    
    # 名前が含まれているものを探す
    for name, sheet_id in sheet_mapping.items():
        if partial_sheet_name in name:
            matched_sheet_id = sheet_id
            break
    if not matched_sheet_id:
        print(f'一致するものが見つかりませんでした: {partial_sheet_name}')
        unmatched_sheets.append((partial_sheet_name, None))  # 一致しなかったシートの情報をリストに追加
        return None
    
    # シートに入りこみ、データフレームとして情報を取得
    sheet = client.open_by_key(matched_sheet_id).sheet1
    data = sheet.get_all_values()
    header = data[0]  # 1行目をヘッダーとして扱う
    
    # データ行を取得
    matched_df = pd.DataFrame(columns=header)
    for row in data[2:]:  # 2行目からデータが始まると仮定
        # 学生名に半角の空白があるのでそれを削除
        modified_student_name = row[header.index('学生名')].replace(' ', '')
        
        # 空白を削除した学生名を比較
        if modified_student_name == student_name.replace(' ', ''):
             # 一致する行をDataFrameに追加
            matched_df = matched_df.append(pd.Series(row, index=header), ignore_index=True)

    if not matched_df.empty:
        #DataFrameに情報を格納し終えたら格納したトリガーとして企業名を追加する
        matched_df["企業名"] = partial_sheet_name 
        return matched_df  # 一致する行があればDataFrameを返す
    else:
        return None  # 一致する行がなければNoneを返す

##関数をもとにして情報を学生ごと分けてディレクトリ内に保存をする

# FutureWarningを非表示にする
warnings.simplefilter(action='ignore', category=FutureWarning)

# 保存先ディレクトリのパス
save_dir = ''

# リクエストのカウンター
count = 0

# 各学生ごとにCSVとして情報を出力
for index, row in accepted_students.iterrows():
    print(row['企業名'], row['学生名'])
    
    # APIの制限対策として3回関数が呼び出されたら1分待機
    if count > 0 and count % 3 == 0:
        print("APIのレート制限に達するのを避けるために1分間待機します...")
        time.sleep(60)  # 1分待機
    
    try:
        # fetch_student_info_from_sheet関数を呼び出して必要な情報を取得
        info = fetch_student_info_from_sheet(row['企業名'], row['学生名'], client, sheet_mapping)
        
        # infoがNoneでない、かつDataFrameである場合のみ処理
        if info is not None and isinstance(info, pd.DataFrame) and not info.empty:
            # 学生名_feedback.csvとして保存
            csv_filename = f"{row['学生名']}_feedback.csv"
            csv_path = os.path.join(save_dir, csv_filename)
            info.to_csv(csv_path, index=False)
            print(f"{csv_filename} を {save_dir} に保存しました.")
    
    except APIError as api_error:
        # APIのエラーが発生した場合、エラーメッセージを表示して10分待機
        print(f"APIエラー: {api_error}")
        print("10分間待機します...")
        time.sleep(600)  # 10分待機
    
    count += 1  # カウンターを関数を呼び出すたびに増やす
    time.sleep(1)  # 1秒待機

# 処理完了後、未マッチのシート情報を出力
if unmatched_sheets:
    print("未マッチのシート情報:")
    for name, _ in unmatched_sheets:
        print(f"- {name}")
