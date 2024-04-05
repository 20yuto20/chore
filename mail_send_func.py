import csv
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

# CCのメールアドレス
cc_address = ""

# CSVファイルのパス
csv_file_path = ""

# SMTPサーバー情報
smtp_server = ""  # SMTPサーバーアドレスを設定
smtp_port = 465  # SMTPポート番号を設定
smtp_username = ""  # SMTPユーザー名を設定
smtp_password = ""  # SMTPパスワードを設定

# メール送信者情報
from_address = ""
from_name = ""

def send_mail(to_address, get_last_name, get_first_name):
    # メール内容
    subject = ""
    body = f"""

    """

    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header(from_name, 'utf-8')), from_address))
    msg['To'] = to_address
    msg['Cc'] = cc_address
    msg['Subject'] = subject

    text = MIMEText(body, 'plain', 'utf-8')
    msg.attach(text)

    # SMTPサーバーに接続してメール送信
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(from_address, [to_address, cc_address], msg.as_string())
        print(f"メールを {to_address} に送信しました。{cc_address}をCCに追加しています。")
    except Exception as e:
        print(f"メール送信エラー: {str(e)}")

# CSVファイルからメールアドレス読み込み
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # ヘッダー行をスキップ

    sent_count = 0
    for row in csv_reader:
        email_address = row[3] # メールアドレスの列の位置を適切に設定
        last_name = row[1]
        first_name = row[2]
        if email_address:
            send_mail(email_address, last_name, first_name)
            # 1秒待ってから次のメールを送信
            time.sleep(1)
            sent_count += 1
            if sent_count == 25:
                print("25件送信しました。次は1分30秒待機します。")
                time.sleep(90)  # 1分30秒待機
                sent_count = 0  # カウンターをリセット