#CC(Correct Code)
#シートが複数ある時はリスト化してfor文を用いて一つ一つ取り出すのが肝

import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Google Drive API セットアップ
DR_CREDENTIAL_FILE = 'secret.json'
DR_SCOPE = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(DR_CREDENTIAL_FILE, DR_SCOPE)
drive_service = build('drive', 'v3', credentials=credentials)

# 複数のフォルダID
folder_ids = [
    '',  # 最初のフォルダID
    ''   # 2番目のフォルダID
]

# サブフォルダを取得する関数
def get_subfolders(service, folder_id):
    subfolders = []
    page_token = None

    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()
        subfolders.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    return subfolders

# スプレッドシートを取得する関数
def get_spreadsheets(service, folder_id, file):
    page_token = None

    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()
        for spreadsheet in response.get('files', []):
            spreadsheet_id = spreadsheet['id']
            spreadsheet_name = spreadsheet['name']

            if '学生フィードバック' in spreadsheet_name:
                file.write(f'{spreadsheet_name}: {spreadsheet_id}\n')

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

# sheet_id.txt ファイルを開いて各フォルダごとに処理
with open('sheet_id.txt', 'a') as file:  # 'a'モードで既存の内容を保持しつつ追記
    for folder_id in folder_ids:
        subfolders = get_subfolders(drive_service, folder_id)
        for subfolder in subfolders:
            subfolder_id = subfolder['id']
            subfolder_name = subfolder['name']
            
            # サブフォルダ名も記録
            file.write(f'Folder: {subfolder_name}\n')
            
            # サブフォルダ内のスプレッドシート一覧を取得して記録
            get_spreadsheets(drive_service, subfolder_id, file)

print('記入が完了しました。')
